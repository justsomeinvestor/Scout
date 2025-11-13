# Phase 3: Background Data Collector System

**Status:** IMPLEMENTATION COMPLETE (Phase 3.1)
**Date:** 2025-10-19
**Components:** 6 Python modules + 2 JavaScript files

---

## 📦 What's Implemented

### Core Modules (Python)

#### 1. `api_sources.py` - Data Fetching Layer
- **FinnhubAPI class:** Fetches real market data from Finnhub
  - `get_quote(ticker)` - Current price, change, volume
  - `get_candles(ticker, days, resolution)` - OHLCV history
  - `get_technical_indicators(ticker)` - Pre-calculated indicators
  - Rate limit handling (60 calls/min)
  - Error recovery with logging

- **YahooFinanceScraper class:** Fallback data source
  - `scrape_quote(ticker)` - HTML parsing for current price
  - `scrape_candles(ticker)` - Historical data via yfinance

- **APISourceManager class:** Intelligent failover
  - Tries Finnhub first
  - Falls back to Yahoo Finance on failure
  - Transparent to caller

**Key Features:**
- Comprehensive error handling
- Request timeout (10s)
- API rate limit enforcement
- Logging to `logs/api_sources.log`

#### 2. `cache_manager.py` - Persistent Data Storage
- **CacheManager class:** JSON-based caching with TTL
  - `save(ticker, data)` - Store market data with timestamp
  - `get(ticker)` - Retrieve if fresh (< 5 min old)
  - `is_stale(ticker, ttl)` - Check cache age
  - `clear(ticker)` - Delete cache entries
  - `get_all()` - Retrieve all cached data
  - `get_cache_status()` - Statistics and metadata
  - `get_tickers_in_cache()` - List cached tickers

**Storage:**
- Location: `data/cache/[TICKER].json`
- TTL: 5 minutes (configurable)
- Format: JSON with timestamp metadata
- Auto-creates directories

**Key Features:**
- File I/O error handling
- JSON encoding/decoding
- Automatic stale data detection
- Status reporting

#### 3. `ticker_manager.py` - Watchlist Management
- **TickerManager class:** Manages tracked tickers
  - `add_ticker(ticker)` - Add to watchlist
  - `remove_ticker(ticker)` - Remove (not if protected)
  - `is_tracked(ticker)` - Check if in watchlist
  - `get_watchlist()` - List all tracked tickers
  - `validate_ticker(ticker)` - Format validation
  - `get_protected_tickers()` - List SPY, QQQ
  - `get_custom_tickers()` - User-added tickers
  - `get_status()` - Full watchlist status

**Protected Tickers:** SPY, QQQ
- Always tracked
- Cannot be removed
- Automatically re-added if deleted

**Storage:**
- Location: `data/watchlist.json`
- Format: JSON with protected list
- Auto-creates on first run

**Validation:**
- Length: 1-5 characters
- Alphanumeric only
- Case-insensitive

#### 4. `data_collector.py` - Background Service Daemon
- **DataCollector class:** Main collection service
  - `start()` - Begin background collection loop
  - `stop()` - Gracefully halt service
  - `is_running()` - Check if active
  - `get_status()` - Full status report

**Collection Loop (5-minute cycle):**
1. Load watchlist (SPY, QQQ + custom)
2. For each ticker:
   - Fetch from Finnhub (quote + candles)
   - Calculate indicators (RSI, MACD, OBV, EMAs)
   - Detect support/resistance levels
   - Cache results
3. Write status to JSON file
4. Sleep 5 minutes
5. Repeat

**Technical Indicators Calculated:**
- **RSI** (14-period, 0-100 scale)
- **MACD** (line, signal, histogram)
- **OBV** (On-Balance Volume)
- **Moving Averages** (EMA 20, 50, 200)
- **Trend Detection** (uptrend if EMA 20 > 50 > 200)
- **Support/Resistance** (peak/trough detection)

**Threading:**
- Runs as daemon thread
- Non-blocking
- Safe to call `start()` in Wingman load

**Logging:**
- File: `logs/data_collector.log`
- Daily rotation
- Includes: timestamps, actions, errors
- Success/error counters

**Status File:**
- Location: `data/collector_status.json`
- Updated after each cycle
- Contains: running status, last run, cache info, API usage

#### 5. `analyze_ticker_v2.py` - Updated Decision Engine
- **TickerAnalyzer class:** Real decision engine with cache integration
  - `analyze(ticker)` - Main analysis method
  - Reads from cache first (fast)
  - Falls back to live API if stale/empty
  - Gets market context (SPY, QQQ) from cache
  - Returns same output format as before
  - Tracks data source (cache vs live)

**Phase 3 Enhancements:**
- `data_source` field in output (shows 'cache', 'live_api', or 'simulated')
- Graceful fallback if cache/API unavailable
- Real support/resistance levels from cache
- Real RSI, MACD, OBV values
- Market context from SPY/QQQ cache

**Output:**
```json
{
  "ticker": "NVDA",
  "probability_score": 71.5,
  "signal": "BUY",
  "data_source": "cache",
  "component_scores": {
    "technical_analysis": 80.0,
    "market_context": 55.0,
    "sentiment": 40.0,
    "volume": 50.0,
    "seasonality": 55.0
  },
  "levels": {
    "entry": 192.50,
    "stop": 190.00,
    "target": 198.50,
    "r_r_ratio": 3.25
  },
  "position_sizing": {
    "shares": 123,
    "risk_dollars": 462.06,
    "potential_profit": 1386.18
  }
}
```

### Frontend Integration (JavaScript)

#### 6. `data_collector_control.js` - Command Center Controls
- **startCollector()** - Begin background service
- **stopCollector()** - Stop service gracefully
- **restartCollector()** - Stop then start
- **addTicker(ticker)** - Add to watchlist
- **removeTicker(ticker)** - Remove from watchlist
- **getCollectorStatus()** - Poll for status
- **updateStatusDisplay()** - Update UI
- **updateTickerList()** - Refresh ticker display

**Features:**
- Real-time status polling (every 5 seconds)
- Visual feedback (running/stopped indicator)
- API rate limit display
- Success/error counters
- Protected ticker indicators (🔒 for SPY/QQQ)
- Enter key support for quick ticker add
- Auto-clear messages after 5 seconds

#### 7. `collector_api.py` - Flask Backend API
- **POST /api/collector/start** - Start service
- **POST /api/collector/stop** - Stop service
- **GET /api/collector/status** - Get current status
- **POST /api/collector/ticker/add** - Add ticker
- **POST /api/collector/ticker/remove** - Remove ticker
- **GET /api/collector/status/json** - Debug status file

**Response Format:**
```json
{
  "success": true,
  "message": "Collector started",
  "running": true,
  "last_run": "2025-10-19T14:30:00",
  "next_run": "2025-10-19T14:35:00",
  "tickers_tracked": 5,
  "cache_entries": 5,
  "watchlist": ["SPY", "QQQ", "NVDA", "TSLA", "AAPL"]
}
```

### Configuration Files

#### 8. `config/api_keys.json`
```json
{
  "finnhub": "cvb0g99r01qgjh3v2pcgcvb0g99r01qgjh3v2pd0",
  "created": "2025-10-19",
  "note": "Keep secure - contains API keys",
  "rate_limit": "60 calls per minute",
  "endpoint": "https://finnhub.io/api/v1"
}
```

#### 9. `data/watchlist.json`
```json
{
  "watchlist": ["SPY", "QQQ"],
  "protected": ["SPY", "QQQ"],
  "last_updated": "2025-10-19T00:00:00"
}
```

---

## 🚀 How to Use

### 1. Start the Collector (from Python)

```python
from scripts.trading.data_collector import DataCollector

# Initialize
collector = DataCollector(api_key='YOUR_FINNHUB_KEY')

# Start background service
collector.start()

# Service runs in background, updating every 5 minutes

# Check status
status = collector.get_status()
print(f"Running: {status['running']}")
print(f"Tickers tracked: {status['tickers_tracked']}")
print(f"Cache entries: {status['cache_entries']}")

# Stop when done
collector.stop()
```

### 2. Use in Decision Engine

```python
from scripts.trading.analyze_ticker_v2 import TickerAnalyzer

# Initialize with API key
analyzer = TickerAnalyzer(api_key='YOUR_FINNHUB_KEY')

# Analyze ticker - will use cache if available
result = analyzer.analyze('NVDA')

print(f"Signal: {result['signal']}")
print(f"Probability: {result['probability_score']}")
print(f"Data source: {result['data_source']}")  # Shows 'cache', 'live_api', etc
```

### 3. Control from Command Center

Add this to your HTML:
```html
<!-- Include after data_collector_control.js is loaded -->
<button onclick="startCollector()">Start</button>
<button onclick="stopCollector()">Stop</button>
<input id="new-ticker" placeholder="Ticker">
<button onclick="addTicker()">Add</button>
```

Include the JavaScript:
```html
<script src="scripts/dashboard/data_collector_control.js"></script>
```

Setup Flask API:
```python
from flask import Flask
from scripts.trading.collector_api import collector_bp, set_collector

app = Flask(__name__)
app.register_blueprint(collector_bp)

# After creating your collector instance:
set_collector(collector_instance)

app.run()
```

---

## 📊 Data Flow

```
┌─────────────────────────────────────────────────────────┐
│  Command Center (HTML)                                   │
│  - START/STOP/RESTART buttons                           │
│  - ADD/REMOVE ticker input                              │
│  - Live status display                                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│  JavaScript (data_collector_control.js)                 │
│  - Calls backend API                                    │
│  - Updates UI                                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│  Flask API (collector_api.py)                           │
│  - /start, /stop, /status                               │
│  - /ticker/add, /ticker/remove                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│  DataCollector (data_collector.py)                      │
│  - Background daemon thread                             │
│  - 5-minute update loop                                 │
└────────────┬──────────────────────┬─────────────────────┘
             │                      │
       ┌─────▼──────┐        ┌──────▼──────────┐
       │             │        │                │
       ↓             ↓        ↓                ↓
┌─────────────┐  ┌──────────────┐  ┌─────────────────┐
│  API Sources│  │ Ticker Mgr   │  │  Cache Manager  │
│ (Finnhub)   │  │  (watchlist) │  │  (JSON store)   │
└──────┬──────┘  └──────┬───────┘  └────────┬────────┘
       │                │                   │
       └────────────────┼───────────────────┘
                        │
                        ↓
            ┌────────────────────────┐
            │  data/cache/*.json     │
            │  (5-min fresh data)    │
            └────────────────────────┘
                        │
                        ↓
            ┌────────────────────────┐
            │  TickerAnalyzer        │
            │  (analyze_ticker_v2)   │
            │  (reads cache first)   │
            └────────────────────────┘
```

---

## 🔧 Configuration & Customization

### Change Update Interval
```python
collector = DataCollector(api_key=key, update_interval=600)  # 10 minutes
```

### Add Custom Ticker
```python
collector.ticker_manager.add_ticker('AAPL')
# or via API:
# POST /api/collector/ticker/add with {"ticker": "AAPL"}
```

### Check Cache Status
```python
cache = CacheManager()
status = cache.get_cache_status()
print(f"Entries: {status['entries']}")
print(f"Size: {status['total_size_bytes']} bytes")
```

### Access Cached Data
```python
cache = CacheManager()
nvda_data = cache.get('NVDA')
if nvda_data:
    print(f"Price: {nvda_data['quote']['price']}")
    print(f"RSI: {nvda_data['indicators']['rsi']}")
```

---

## ⚠️ Known Limitations & Future Improvements

### Current (Phase 3.1)
- ✅ Basic 5-minute collection cycle
- ✅ Finnhub API + fallback
- ✅ JSON caching
- ✅ Manual START/STOP control
- ✅ Watchlist management

### Phase 3.2 - Next Steps
- [ ] Multi-timeframe analysis (daily, 4h, 1h)
- [ ] Real pattern detection (H&S, triangles, flags)
- [ ] Trade logging and backtesting
- [ ] Automated start on Wingman load
- [ ] Database storage (SQLite) instead of JSON
- [ ] WebSocket live updates to frontend
- [ ] Error recovery with exponential backoff
- [ ] Configurable indicator periods
- [ ] Email/SMS alerts on signals

---

## 🐛 Troubleshooting

### Collector won't start
- Check API key in `config/api_keys.json`
- Ensure `logs/` and `data/` directories exist
- Check `logs/data_collector.log` for errors

### Cache not updating
- Verify collector is running: `collector.is_running()`
- Check last_run timestamp in status
- Verify watchlist has tickers: `collector.ticker_manager.get_watchlist()`

### API rate limit hit
- Collector respects 60 calls/min
- Reduce number of tracked tickers
- Increase update interval

### Analyzer using stale data
- Cache TTL is 5 minutes
- Data updates every 5 minutes
- Wait ~1 minute for first update after start

---

## 📝 File References

| File | Purpose | Lines |
|------|---------|-------|
| `api_sources.py` | Data fetching layer | 450+ |
| `cache_manager.py` | JSON caching | 280+ |
| `ticker_manager.py` | Watchlist management | 200+ |
| `data_collector.py` | Background daemon | 450+ |
| `analyze_ticker_v2.py` | Updated decision engine | 600+ |
| `data_collector_control.js` | Frontend controls | 280+ |
| `collector_api.py` | Flask backend API | 200+ |

---

## ✅ Testing Checklist

- [ ] Collector starts without errors
- [ ] Watchlist loads with SPY, QQQ
- [ ] API calls work (check logs)
- [ ] Cache files created in `data/cache/`
- [ ] Analyzer reads from cache
- [ ] Can add custom ticker (NVDA, TSLA, etc)
- [ ] Can remove custom ticker (not SPY/QQQ)
- [ ] Status updates every 5 minutes
- [ ] Graceful stop without hanging
- [ ] Frontend buttons work (with backend API)
- [ ] Error handling on API failure
- [ ] Fallback to simulated data if needed

---

**Phase 3.1 Complete** ✓
Ready for Phase 3.2 (Multi-timeframe & Pattern Detection)

