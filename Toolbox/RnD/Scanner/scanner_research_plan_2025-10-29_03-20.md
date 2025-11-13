# Real‑Time Scanner Research Plan (Stocks, Options, Crypto)

**Owner:** Daryll  
**Version:** 2025-10-29_03-20  
**Goal:** Design a modular, real‑time scanning system to surface high‑probability trade ideas intraday (and swing), starting with **stocks**, then **options overlays**, then **crypto**, with logging/backtests to iterate toward true edge.

---

## 0) Design Principles

- **Modular first:** ship independent modules (Stocks ▶ Options ▶ Crypto ▶ Integration).  
- **Evidence‑driven:** scanners generate *candidates*; edge comes from execution, risk, and iteration. Log everything and review weekly.  
- **Low‑latency where it matters:** real‑time quotes/volume for intraday; batch is fine for fundamentals.  
- **Observability:** every alert has a trace (inputs, filters passed, chart snapshot if possible).  
- **Config‑driven:** all thresholds and watchlists live in editable config, not code.

---

## 1) What Successful Intraday Scanners Focus On (Synthesis)

- **Relative Volume (RVOL):** prioritize symbols trading at 2×–5× their average.  
- **% Change from Open & Momentum:** movers *after* the open matter more than prior close gaps.  
- **Liquidity Filters:** min average daily volume (e.g., ≥ 2M shares), spreads within limits.  
- **Float / Supply:** small float can amplify moves; prefer bounded ranges for risk control.  
- **Catalyst/News:** earnings, guidance, FDA, M&A, sector sympathy; de‑prioritize no‑news pops.  
- **Structure/Pattern:** breakout + pullback (bull flags), opening range break (ORB), VWAP reclaim, range expansions.  
- **Discipline:** scanners are idea engines; risk management & playbook define P&L.

> Implementation takeaway: a flexible rule engine where each of the above is a pluggable filter/scorer.

---

## 2) System Modules & Phases

### Phase 1 — **Stocks (no options yet)**
**Inputs**
- Real‑time: last price, bid/ask, volume, % from open, intraday candles (1m/5m).  
- Meta: average volume, float, sector/industry, fundamentals (optional).  
- Optional: news flags (earnings today/this week, PRs).

**Filters (starter set)**
- Price between `$2–$50` (configurable).  
- Avg Daily Volume ≥ `2,000,000` shares.  
- RVOL ≥ `3.0` (see §3.1 formula).  
- |%Change from Open| ≥ `3%`.  
- Optional: Float ≤ `20M`.  
- Optional: “Earnings today/this week = true”.

**Pattern/Setup checks (rankers)**
- **VWAP tests:** above VWAP and holding; reclaim after failed breakdown.  
- **Opening Range Break (ORB):** 1m/5m ORH/ORL breaks with volume.  
- **Bull flag:** flagpole impulse, 38–50% pullback, tight consolidation, break on rising volume.  
- **Range expansion:** current true range ≥ `k ×` 20‑day ATR intraday pace.

**Outputs**
- Sorted candidate table (Score, Ticker, RVOL, %FromOpen, Liquidity, Notes).  
- Realtime alerts (desktop/Telegram/Slack).  
- Structured logs for backtest.

---

### Phase 2 — **Options Overlay (per‑symbol augmentation)**
**Inputs**
- Option chain (near‑dated expiries), per‑strike **volume**, **open interest**, **IV**, **IV change**.  
- Optional: “unusual flow” heuristics (volume/OI ratios, sweeps).

**Overlay signals**
- Directional bias if call/put volume skew & IV change align with stock momentum.  
- Liquidity guardrails: spreads ≤ threshold, min volume/OI.  
- Contract picker: ATM/near‑ATM weeklys for momentum; farther OTM only with strong trend.

**Outputs**
- For each stock candidate: 0–3 suggested contracts with risk notes (theta, spreads, IV crush near earnings).

---

### Phase 3 — **Swing/Position Scans**
- Daily/Weekly structure: higher‑highs, breakouts from multi‑week bases, 20/50/200‑MA alignment.  
- Sector/ETF relative strength (e.g., peers, SMH/XLF leadership).  
- Lower alert frequency, larger R:R plays.

---

### Phase 4 — **Crypto Module**
**Inputs**
- Realtime price/volume, 1m/5m bars via exchange websockets (e.g., Binance, Coinbase).  
- Market meta: total market cap dominance, funding rates (if available), perp basis.

**Filters**
- RVOL‑style vs 30‑day baseline, % move thresholds, range breaks, session VWAP/AVWAP from significant anchors.  
- Venue/liquidity screens; exclude illiquid alts early.

**Outputs**
- Candidate list + alerts parallel to stocks module.

---

### Phase 5 — **Integration & Alert Bus**
- Unified alert feed (Redis pub/sub, NATS, or WebSocket).  
- Single dashboard with tabs: *Stocks*, *Options*, *Crypto*, *Logs/Backtests*.  
- Broker connectors (manual first; automate later).

---

## 3) Signals, Math & Heuristics

### 3.1 Relative Volume (RVOL)
- **Definition:** intraday pace vs typical pace.  
- **Simple formula:**  
  `RVOL_now = Volume_so_far_today / AvgDailyVolume` (crude).  
- **Better intraday pace:**  
  `RVOL_pace = (Volume_so_far_today / Minutes_elapsed) / (AvgVolume_per_min_over_baseline)`  
  where baseline uses last 20 sessions.  
- **Thresholds:** 2.0 (interesting), 3.0 (hot), 5.0+ (on fire).

### 3.2 % Change from Open
`pct_from_open = (Last - Open) / Open × 100`  
Use absolute value for move scanners, signed for directional screens.

### 3.3 ORB (Opening Range Break)
- Define first `N` minutes high/low (N=1/5).  
- Long trigger: price > ORH with volume ≥ `x ×` mean per‑bar.  
- Short trigger: price < ORL with volume confirmation.

### 3.4 VWAP & Reclaims
- Maintain session VWAP; signal when price reclaims and holds above for `m` bars with declining downside volume.

### 3.5 Bull Flag Heuristic (intraday)
- Impulse: `k ×` ATR burst.  
- Pullback: 38–50% of pole, contracting range/volume.  
- Entry: break of flag high with increasing volume; stop under flag low.

---

## 4) Data & APIs (swappable)

- **Equities quotes/candles:** Finnhub (free/paid), Polygon, Alpaca, IEX Cloud.  
- **Fundamentals/Float:** Finnhub, Polygon, SEC scrape as backup.  
- **News/Catalysts:** Finnhub news, Benzinga (paid), scraping PR wires; earnings calendars.  
- **Options:** Tradier, Polygon (paid tiers), Intrinio, ORATS (paid, rich options analytics).  
- **Crypto:** Exchange websockets (Binance, Coinbase), CoinGecko/CoinMarketCap for meta.  
- **Charts:** Local calc; optional TradingView widget for visualization (manual).

> Start with Finnhub + one exchange websocket for crypto; add options vendor once Phase 2 begins.

---

## 5) Architecture (proposed)

- **Ingestion**  
  - Equities: websocket/stream if available; else pull every 1–5s.  
  - Crypto: native exchange websockets.  
  - Store to **Timeseries DB** (QuestDB/TimescaleDB) or light **SQLite** for prototype.

- **Compute Layer**  
  - Python services (FastAPI) compute RVOL, ORB, VWAP, patterns per bar.  
  - **Rule/Score Engine:** JSON/YAML‑driven; each rule returns a score; final rank = weighted sum.

- **State & Messaging**  
  - Redis for latest symbol state + pub/sub alerts.  
  - Background workers (RQ/Celery) for heavier tasks.

- **UI / Ops**  
  - Streamlit or React dashboard; sortable grids; per‑symbol drill‑downs.  
  - Telemetry: Prometheus + Grafana (optional later).

---

## 6) Config Examples

### 6.1 YAML Rule Config (starter)
```yaml
universe:
  equities: ["NYSE", "NASDAQ"]
  min_price: 2
  max_price: 50
  min_avg_dollar_vol: 2_000_000
filters:
  rvol:
    method: intraday_pace
    min: 3.0
  pct_from_open:
    min: 3.0
  float:
    max: 20_000_000
  earnings_window_days: 7
rank:
  weights:
    rvol: 0.45
    pct_from_open: 0.25
    vwap_reclaim: 0.15
    orb_break: 0.15
alerts:
  channels: ["desktop", "telegram"]
  throttle_seconds: 60
```

### 6.2 Contract Picker (options)
```yaml
options_overlay:
  expiries: ["0DTE", "1w"]
  moneyness: ["ATM", "±1 strike"]
  min_volume: 200
  max_spread_bps: 75
  iv_change_min: 3.0  # pct points
  flow_bias_min_ratio: 1.5  # calls:puts or vice versa
```

---

## 7) Backtesting & Analytics

- Log every alert with snapshot of metrics & price path for T+1/T+5/close.  
- Daily recap auto‑report: hit rate, avg move after alert, best/worst rules.  
- Weekly rule audit: adjust thresholds, re‑weight scores; deprecate noisy rules.

---

## 8) Risk & Playbook (execution matters)

- **Position sizing:** fixed‑fraction risk per trade (e.g., 0.25–0.5% acct).  
- **Stops:** structure‑based (flag low, VWAP loss) vs fixed ATR.  
- **Avoid:** illiquid names, wide spreads, news‑less spikes, chasing extended moves.  
- **Journaling:** attach reason for entry, exit plan, and outcome to each alert.

---

## 9) Build Plan (for Engineering AI)

1. **Scaffold**: repo with `ingestion/`, `signals/`, `rules/`, `ui/`, `storage/`.  
2. **Ingestion**: Finnhub equities + 1 crypto websocket; write 1m bars + ticks to DB.  
3. **Signals**: implement RVOL, %FromOpen, VWAP, ORB, ATR. Unit tests.  
4. **Rule Engine**: YAML‑driven filters + weighted score; output ranked list per bar.  
5. **Alerts**: Redis pub/sub + Telegram/desktop notifier; throttling + dedupe.  
6. **UI**: minimal grid (ticker, score, rvol, %open, notes), detail page with mini‑chart.  
7. **Logging**: append JSONL per alert; nightly summary notebook.  
8. **Options Overlay (Phase 2)**: pluggable provider, contract picker, liquidity guards.  
9. **Crypto Module (Phase 4)**: mirror signals with exchange data.  
10. **Backtests**: replay recorded day; compute post‑alert forward returns.

---

## 10) Nice‑to‑Have (Later)

- Sector momentum model; AVWAP anchors from events; sentiment/NLP on headlines; auto‑chart snapshots; broker API hooks; Monte‑Carlo of rule combos.

---

## 11) Open Questions for Daryll

- Trading hours focus (first 90m? all day?), overnight holds?  
- Options broker/data source preference?  
- Alert channel preferences?  
- Universe constraints (no OTC/pennies?), sector biases?  
- Risk budget per trade and per day?

---

### TL;DR
Start with an **intraday equities scanner** focused on **RVOL + % from open + VWAP/ORB** with hard liquidity guards. Log everything. Add **options overlay** and **crypto** once core signal quality is proven. Iterate rules weekly based on measured post‑alert outcomes.
