# Options Fetch (3–4×/day) — Setup

This pair of files lets you fetch **max pain**, **PCR**, **IV percentile (rough)**, **total OI**, and **key levels** a few times per day **without rate limits**, writing a single JSON your dashboard can read.

## Files
- `options_fetch_3x_daily.py` — main script
- Output is written to `Research/.cache/optionsData.json` by default

## Providers
- **Primary:** Polygon (if `POLYGON_API_KEY` is set in the environment)
- **Fallback:** `yfinance` (no key required) — fine at 3–4 runs per day with caching

> Recommendation: If you want authoritative Max Pain each morning, wire in official **OCC EOD Open Interest** as a later enhancement; the script is structured so you can replace the OI arrays before the max-pain calculation.

## Install
```bash
pip install pandas requests yfinance
# optional but recommended: a Polygon key
export POLYGON_API_KEY=pk_XXXXXXXXXXXXXXXXXXXX
```

## Run examples
Fetch SPY, QQQ, NVDA, cache results for 120 minutes:
```bash
python options_fetch_3x_daily.py --tickers SPY QQQ NVDA --ttl-min 120
```

Write to a custom output path:
```bash
python options_fetch_3x_daily.py --tickers SPY QQQ --outfile Research/.cache/optionsData.json
```

## Cron (3×/day during market days)
**Times below are US/Eastern.** Adjust for your server’s timezone.

```cron
# 9:20 ET (pre-market read), 12:05 ET (midday), 15:40 ET (into close)
20 9 * * 1-5  /usr/bin/env python3 /path/to/options_fetch_3x_daily.py --tickers SPY QQQ NVDA --ttl-min 120 >> /var/log/options_fetch.log 2>&1
05 12 * * 1-5 /usr/bin/env python3 /path/to/options_fetch_3x_daily.py --tickers SPY QQQ NVDA --ttl-min 120 >> /var/log/options_fetch.log 2>&1
40 15 * * 1-5 /usr/bin/env python3 /path/to/options_fetch_3x_daily.py --tickers SPY QQQ NVDA --ttl-min 120 >> /var/log/options_fetch.log 2>&1
```

## Output schema (example)
```json
{
  "SPY": {
    "lastUpdated": "2025-10-16 12:31 ET",
    "maxPain": "$605",
    "putCallRatio": "0.88",
    "ivPercentile": "47%",
    "totalOI": "12,345,678",
    "keyLevels": [
      {"strike":"600","type":"Put Wall","gamma":"N/A","oi":"450K"},
      {"strike":"610","type":"Call Wall","gamma":"N/A","oi":"520K"},
      {"strike":"605","type":"Max Pain","gamma":"N/A","oi":"310K"}
    ],
    "currentPrice": 607.12,
    "expiration": "2025-10-17",
    "source": "polygon"
  },
  "QQQ": { "...": "..." }
}
```

## Tips
- Keep `--ttl-min` ≥ 60 so mid‑day reruns never touch the vendor if you already ran recently.
- Batch all tickers in **one** process so retries/keep‑alive are shared (less chance of throttling).
- If you add more symbols later, stagger run times or bump `ttl-min`.
- For rapid quotes/greeks, consider a streaming source and keep chain refreshes infrequent.
