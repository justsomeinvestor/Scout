#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Fetch options data 3–4x/day and write ONE JSON your dashboard reads.

- Providers: Polygon (if POLYGON_API_KEY is present) or yfinance (fallback).
- Cache: disk TTL so re-runs don't hit vendors.
- Robust: retries + token-bucket; yfinance uses last close (5d) so it works pre-market.
- Output: C:\Users\Iccanui\Desktop\Investing\Research\.cache\optionsData.json
"""

import os, sys, json, time, random, argparse
from datetime import datetime, timedelta
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

try:
    import pandas as pd
except ImportError:
    print("[ERROR] pandas is required. Run: pip install pandas requests yfinance")
    sys.exit(1)

try:
    import yfinance as yf
except Exception:
    yf = None

# ---- constants (writes where your AI expects) ----
CACHE_DIR = Path(r"C:\Users\Iccanui\Desktop\Investing\Research\.cache")
OUTFILE   = CACHE_DIR / "optionsData.json"
CACHE_TTL_MIN_DEFAULT = 180  # slower refresh to avoid vendor calls
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# simple run lock to avoid overlapping jobs
RUNLOCK = CACHE_DIR / "options_fetch.lock"

class RunLock:
    def __enter__(self):
        try:
            if RUNLOCK.exists():
                # if a stale lock older than 10 minutes, ignore it; else skip
                mtime = RUNLOCK.stat().st_mtime
                if time.time() - mtime < 600:
                    print("[SKIP] Another fetch is running (lock present).")
                    sys.exit(0)
        except Exception:
            pass
        try:
            RUNLOCK.write_text(str(os.getpid()), encoding="utf-8")
        except Exception:
            pass
        return self

    def __exit__(self, *_):
        try:
            RUNLOCK.unlink(missing_ok=True)
        except Exception:
            pass

# ------- polite limiter (conservative for Yahoo) -------
class TokenBucket:
    def __init__(self, rate_per_sec=0.2, burst=1):  # 0.2 rps = ~1 call / 5s
        self.rate = rate_per_sec
        self.capacity = burst
        self.tokens = burst
        self.t0 = time.monotonic()
    def take(self, cost=1.0):
        now = time.monotonic()
        self.tokens = min(self.capacity, self.tokens + (now - self.t0) * self.rate)
        self.t0 = now
        if self.tokens < cost:
            time.sleep((cost - self.tokens) / self.rate)
            self.tokens = 0
        else:
            self.tokens -= cost

BUCKET = TokenBucket()  # slower than before

def make_session():
    s = requests.Session()
    # real browser UA helps avoid 999s
    s.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
    })
    retry = Retry(
        total=7, read=7, connect=7,
        backoff_factor=1.2,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET", "POST"]),
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=2, pool_maxsize=2)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s

SESSION = make_session()

# ---- cache helpers ----
def cache_path(date_str: str, ticker: str) -> Path:
    return CACHE_DIR / f"{date_str}_{ticker}_options.json"

def load_cache(path: Path, ttl_minutes: int):
    if not path.exists(): return None
    try:
        with path.open("r", encoding="utf-8") as f: data = json.load(f)
        ts = data.get("_fetched_at"); 
        if not ts: return None
        if datetime.now() - datetime.fromisoformat(ts) <= timedelta(minutes=ttl_minutes): return data
    except Exception: return None
    return None

def save_cache(path: Path, data: dict):
    obj = dict(data); obj["_fetched_at"] = datetime.now().isoformat()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f: json.dump(obj, f, indent=2)

# ---- computations ----
def max_pain(calls: pd.DataFrame, puts: pd.DataFrame, spot: float) -> float:
    price_range = spot * 0.10
    strikes = sorted(set(calls['strike'].tolist() + puts['strike'].tolist()))
    strikes = [s for s in strikes if abs(s - spot) <= price_range]
    best_k, best_val = spot, float('inf')
    for k in strikes:
        c = calls[calls['strike'] > k]; p = puts[puts['strike'] < k]
        call_pain = 0 if c.empty else (c['openInterest']*(c['strike']-k)).sum()
        put_pain  = 0 if p.empty else (p['openInterest']*(k-p['strike'])).sum()
        tot = float(call_pain + put_pain)
        if tot < best_val: best_val, best_k = tot, k
    return float(best_k)

def put_call_ratio(calls: pd.DataFrame, puts: pd.DataFrame) -> float:
    co = float(calls['openInterest'].sum()); po = float(puts['openInterest'].sum())
    return (po / co) if co > 0 else 0.0

def iv_percentile(calls: pd.DataFrame, puts: pd.DataFrame) -> float:
    try:
        a = pd.concat([calls, puts])
        if 'impliedVolatility' not in a.columns: return 50.0
        med, mn, mx = float(a['impliedVolatility'].median()), float(a['impliedVolatility'].min()), float(a['impliedVolatility'].max())
        return 100.0*(med-mn)/(mx-mn) if mx>mn else 50.0
    except Exception: return 50.0

def key_levels(calls: pd.DataFrame, puts: pd.DataFrame, spot: float, mp: float):
    lvls = []
    mc = calls[calls['strike']==mp]; mp_ = puts[puts['strike']==mp]
    if not mc.empty or not mp_.empty:
        tot = int((mc['openInterest'].sum() if not mc.empty else 0) + (mp_['openInterest'].sum() if not mp_.empty else 0))
        lvls.append({'strike': f"{mp:.0f}", 'type':'Max Pain','gamma':'N/A','oi': f"{tot/1000:.0f}K"})
    cw = calls.nlargest(1, 'openInterest')
    if not cw.empty:
        lvls.append({'strike': f"{cw['strike'].iloc[0]:.0f}", 'type':'Call Wall','gamma':'N/A','oi': f"{int(cw['openInterest'].iloc[0])/1000:.0f}K"})
    pw = puts.nlargest(1, 'openInterest')
    if not pw.empty:
        lvls.append({'strike': f"{pw['strike'].iloc[0]:.0f}", 'type':'Put Wall','gamma':'N/A','oi': f"{int(pw['openInterest'].iloc[0])/1000:.0f}K"})
    rng = spot*0.02; near = calls[abs(calls['strike']-spot) <= rng]
    if not near.empty:
        hg = near.nlargest(1, 'openInterest')
        lvls.append({'strike': f"{hg['strike'].iloc[0]:.0f}", 'type':'High Gamma','gamma':'N/A','oi': f"{int(hg['openInterest'].iloc[0])/1000:.0f}K"})
    sup = puts[puts['strike']<spot].nlargest(1, 'openInterest')
    if not sup.empty:
        lvls.append({'strike': f"{sup['strike'].iloc[0]:.0f}", 'type':'Put Interest','gamma':'N/A','oi': f"{int(sup['openInterest'].iloc[0])/1000:.0f}K"})
    return lvls[:5]

# ---- providers (Polygon v3 snapshot; filter locally) ----
def polygon_chain(ticker: str):
    key = os.getenv("POLYGON_API_KEY", "").strip()
    if not key: raise RuntimeError("POLYGON_API_KEY not set")
    # underlying last close (prev agg)
    BUCKET.take()
    r = SESSION.get(f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev", params={"apiKey": key})
    r.raise_for_status(); spot = float(r.json()["results"][0]["c"])
    # full chain snapshot (v3)
    BUCKET.take()
    r2 = SESSION.get(f"https://api.polygon.io/v3/snapshot/options/{ticker}", params={"apiKey": key})
    r2.raise_for_status(); j = r2.json()
    if "results" not in j or not j["results"]: raise RuntimeError(f"Polygon chain snapshot empty for {ticker}")
    # Build DataFrames
    calls, puts = [], []
    for o in j["results"]:
        try:
            kind = o["contract_type"]
            strike = float(o["strike_price"])
            oi = int(o.get("open_interest", 0) or 0)
            iv = float(o.get("implied_volatility", 0.0) or 0.0)
            row = {"strike": strike, "openInterest": oi, "impliedVolatility": iv}
            (calls if kind == "call" else puts).append(row)
        except Exception:
            continue
    calls_df = pd.DataFrame(calls if calls else [{"strike": spot, "openInterest": 0, "impliedVolatility": 0.0}])
    puts_df  = pd.DataFrame(puts  if puts  else [{"strike": spot, "openInterest": 0, "impliedVolatility": 0.0}])
    # choose nearest expiry from snapshot (if present), else set later
    expiry = None
    try:
        expiries = sorted({o["expiration_date"] for o in j["results"]})
        expiry = expiries[0] if expiries else None
    except Exception:
        pass
    return spot, (expiry or ""), calls_df, puts_df

def yfinance_chain(ticker: str):
    """
    Hybrid: get spot from Polygon equities (no options plan needed), then pull the
    nearest-expiry chain from yfinance. This avoids Yahoo 'possibly delisted' on price.
    """
    if yf is None:
        raise RuntimeError("yfinance not installed; install it or use Polygon.")

    stock = yf.Ticker(ticker, session=SESSION)

    # --- price via Polygon equities (works even without Options plan) ---
    spot = None
    poly_key = os.getenv("POLYGON_API_KEY", "").strip()
    if poly_key:
        try:
            BUCKET.take()
            r = SESSION.get(
                f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev",
                params={"apiKey": poly_key, "adjusted": "true"},
                timeout=15,
            )
            r.raise_for_status()
            spot = float(r.json()["results"][0]["c"])
        except Exception:
            spot = None

    # --- fallback: Yahoo price (5d last close) ---
    if spot is None:
        BUCKET.take()
        hist = stock.history(period="5d")
        if (
            hist is None
            or hist.empty
            or "Close" not in hist
            or hist["Close"].dropna().empty
        ):
            raise RuntimeError(f"yfinance: no price data for {ticker}")
        spot = float(hist["Close"].dropna().iloc[-1])

    # --- nearest expiry (polite throttle/jitter) ---
    BUCKET.take(); time.sleep(0.5 + random.random())
    expirations = list(stock.options or [])
    if not expirations:
        raise RuntimeError(f"yfinance: no options for {ticker}")
    expiry = expirations[0]

    # --- chain (polite throttle/jitter) ---
    BUCKET.take(); time.sleep(1.0 + random.random() * 1.5)
    chain = stock.option_chain(expiry)
    calls = chain.calls.fillna(0)
    puts = chain.puts.fillna(0)
    return spot, expiry, calls, puts

def fetch_chain(ticker: str, provider: str):
    last_err = None
    order = [("polygon", polygon_chain)] if (provider=="polygon" or (provider=="auto" and os.getenv("POLYGON_API_KEY","").strip())) else []
    if provider in ("yfinance","auto"): order.append(("yfinance", yfinance_chain))
    for name, fn in order:
        try: return name, fn(ticker)
        except Exception as e: last_err = e; time.sleep(0.6 + random.random()*0.6)
    raise last_err if last_err else RuntimeError("no providers available")

# ---- core ----
def compute_payload(date_str: str, ticker: str, ttl_minutes: int, provider: str):
    cp = cache_path(date_str, ticker)
    cached = load_cache(cp, ttl_minutes)
    if cached: return cached
    for attempt in range(5):
        try:
            src, (spot, expiry, calls, puts) = fetch_chain(ticker, provider)
            mp = max_pain(calls, puts, spot)
            pcr = put_call_ratio(calls, puts)
            ivp = iv_percentile(calls, puts)
            toi = int(calls['openInterest'].sum() + puts['openInterest'].sum())
            levels = key_levels(calls, puts, spot, mp)
            payload = {
                "ticker": ticker,
                "date": date_str,
                "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M ET"),
                "currentPrice": round(spot, 2),
                "expiration": expiry,
                "maxPain": f"${mp:.0f}",
                "putCallRatio": f"{pcr:.2f}",
                "ivPercentile": f"{ivp:.0f}%",
                "totalOI": f"{toi:,}",
                "keyLevels": levels,
                "source": src
            }
            save_cache(cp, payload); return payload
        except Exception as e:
            last_err = e; time.sleep((2**attempt)*0.7 + random.random()*0.6)
    raise last_err

def main():
    with RunLock():
        ap = argparse.ArgumentParser()
        ap.add_argument("--tickers", nargs="+", default=["SPY","QQQ"])
        ap.add_argument("--ttl-min", type=int, default=CACHE_TTL_MIN_DEFAULT)
        ap.add_argument("--provider", choices=["auto","polygon","yfinance"], default="auto")
        args = ap.parse_args()

        date_str = datetime.now().strftime("%Y-%m-%d")
        result = {}
        failures = []
        for t in args.tickers:
            t = t.upper()
            try:
                p = compute_payload(date_str, t, args.ttl_min, args.provider)
                result[t] = {k: p[k] for k in ("lastUpdated","maxPain","putCallRatio","ivPercentile","totalOI","keyLevels","currentPrice","expiration","source")}
            except Exception as e:
                failures.append(t)
                result[t] = {"error": str(e)}
            # polite gap between symbols (Yahoo is sensitive to bursts)
            time.sleep(2.0 + random.random() * 2.0)  # 2-4s

        payload = {
            "date": date_str,
            "generatedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "source": args.provider,
            "tickers": result
        }

        with OUTFILE.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        print(f"[OK] wrote {OUTFILE} with {len(result)} tickers")
        if failures:
            print(f"[WARN] Failed tickers: {', '.join(failures)}")

if __name__ == "__main__":
    main()
