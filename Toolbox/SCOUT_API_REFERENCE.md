# Scout API Reference
**Version:** 1.0
**Server:** 192.168.10.56:3000
**Last Updated:** 2025-11-08

---

## Overview

The Scout system uses a dedicated API server for market data collection, eliminating the need for local scraping of financial data. This reference documents all available endpoints, request/response formats, and usage patterns.

**Base URL:** `http://192.168.10.56:3000`

**API Client:** `scripts/trading/api_client.py`

---

## Quick Start

### Python Client Usage

```python
from scripts.trading.api_client import get_client

# Context manager (recommended)
with get_client() as api:
    # Health check
    if api.is_healthy():
        # Get all data in one call
        summary = api.get_summary()
        print(summary)

# Or manual management
api = MarketDataAPI()
data = api.get_spy_data()
api.close()
```

### Direct HTTP Requests

```bash
# Health check
curl http://192.168.10.56:3000/health

# Get summary
curl http://192.168.10.56:3000/api/summary

# Get SPY data
curl http://192.168.10.56:3000/api/latest/SPY
```

---

## Health & Status Endpoints

### GET /health
**Purpose:** Basic server health check

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-11-08T15:30:00.000Z"
}
```

**Python:**
```python
health = api.health_check()
# {'status': 'ok', 'timestamp': '2025-11-08T15:30:00.000Z'}
```

**Use Case:** Quick connectivity test

---

### GET /api/status
**Purpose:** Comprehensive system health with database metrics

**Response:**
```json
{
  "success": true,
  "database": {
    "connected": true,
    "size": "10.5 MB",
    "path": "/var/data/market_data.db"
  },
  "tables": {
    "etf_data": {
      "rowCount": 1250,
      "latestTimestamp": "2025-11-08T15:25:00.000Z"
    },
    "vix_data": {
      "rowCount": 890,
      "latestTimestamp": "2025-11-08T15:25:00.000Z"
    },
    "max_pain_data": {
      "rowCount": 3500,
      "latestTimestamp": "2025-11-08T15:20:00.000Z"
    },
    "chat_messages": {
      "rowCount": 450,
      "latestTimestamp": "2025-11-08T15:15:00.000Z"
    }
  },
  "lastScrape": {
    "timestamp": "2025-11-08T15:25:00.000Z",
    "duration": "45.3s",
    "success": true
  },
  "health": {
    "status": "healthy",
    "checks": {
      "database": "ok",
      "diskSpace": "ok",
      "lastScrape": "ok"
    }
  }
}
```

**Python:**
```python
status = api.get_status()
print(f"ETF rows: {status['tables']['etf_data']['rowCount']}")
print(f"Last scrape: {status['lastScrape']['timestamp']}")
```

**Use Case:** Detailed diagnostics, data freshness checks

---

### GET /api/summary
**Purpose:** Get ALL latest data from ALL tables in one call

**Response:**
```json
{
  "success": true,
  "timestamp": "2025-11-08T15:30:00.000Z",
  "etf_data": {
    "count": 2,
    "data": [
      {
        "symbol": "SPY",
        "timestamp": "2025-11-08T15:25:00.000Z",
        "currentPrice": 585.42,
        "impliedVolatility": 12.5,
        "putCallOIRatio": 0.85,
        "putCallVolRatio": 1.2,
        "optionsVolume": 1250000,
        "dailyChange": 1.25,
        "dailyChangePercent": 0.21
      },
      {
        "symbol": "QQQ",
        "timestamp": "2025-11-08T15:25:00.000Z",
        "currentPrice": 425.18,
        "impliedVolatility": 15.3,
        "putCallOIRatio": 0.92,
        "putCallVolRatio": 1.1,
        "optionsVolume": 850000,
        "dailyChange": 2.15,
        "dailyChangePercent": 0.51
      }
    ]
  },
  "vix_data": {
    "count": 1,
    "data": {
      "timestamp": "2025-11-08T15:25:00.000Z",
      "currentPrice": 14.25,
      "change": -0.35,
      "changePercent": -2.4,
      "vix1m": 14.5,
      "vix3m": 15.2,
      "vix6m": 16.1,
      "termStructure": "normal"
    }
  },
  "max_pain_data": {
    "count": 70,
    "spy_weekly": [
      {
        "symbol": "SPY",
        "expiration_date": "Nov 11, 2025",
        "max_pain_price": 583.0,
        "days_until_expiry": 3,
        "total_oi": 2500000,
        "timestamp": "2025-11-08T15:20:00.000Z"
      }
    ],
    "qqq_weekly": [
      {
        "symbol": "QQQ",
        "expiration_date": "Nov 11, 2025",
        "max_pain_price": 423.0,
        "days_until_expiry": 3,
        "total_oi": 1800000,
        "timestamp": "2025-11-08T15:20:00.000Z"
      }
    ]
  },
  "chat_messages": {
    "count": 50,
    "data": [
      {
        "timestamp": "2025-11-08T15:15:00.000Z",
        "username": "trader123",
        "message": "Market looking bullish on SPY",
        "scrape_timestamp": "2025-11-08T15:20:00.000Z"
      }
    ]
  },
  "status": {
    "database_connected": true,
    "last_scrape": "2025-11-08T15:25:00.000Z"
  }
}
```

**Python:**
```python
summary = api.get_summary()

# Access different sections
spy_data = summary['etf_data']['data'][0]
vix_data = summary['vix_data']['data']
max_pain_spy = summary['max_pain_data']['spy_weekly'][0]
chat = summary['chat_messages']['data']
```

**Use Case:** **PRIMARY ENDPOINT** for Scout dashboard updates - get everything in one call

**Performance:** Single HTTP request vs. 5+ separate calls

---

## ETF Data Endpoints

### GET /api/latest
**Purpose:** Get latest data for all ETF symbols (SPY, QQQ)

**Response:**
```json
{
  "success": true,
  "count": 2,
  "data": [
    {
      "symbol": "SPY",
      "timestamp": "2025-11-08T15:25:00.000Z",
      "currentPrice": 585.42,
      "impliedVolatility": 12.5,
      "putCallOIRatio": 0.85,
      "putCallVolRatio": 1.2,
      "optionsVolume": 1250000,
      "dailyChange": 1.25,
      "dailyChangePercent": 0.21
    },
    {
      "symbol": "QQQ",
      "timestamp": "2025-11-08T15:25:00.000Z",
      "currentPrice": 425.18,
      "impliedVolatility": 15.3,
      "putCallOIRatio": 0.92,
      "putCallVolRatio": 1.1,
      "optionsVolume": 850000,
      "dailyChange": 2.15,
      "dailyChangePercent": 0.51
    }
  ]
}
```

**Python:**
```python
all_etf = api.get_latest_all_etf()
for etf in all_etf['data']:
    print(f"{etf['symbol']}: ${etf['currentPrice']}")
```

---

### GET /api/latest/{symbol}
**Purpose:** Get latest data for specific symbol (SPY, QQQ, VIX)

**Parameters:**
- `symbol` (path) - Stock symbol (case insensitive)

**Response (ETF):**
```json
{
  "success": true,
  "data": {
    "symbol": "SPY",
    "timestamp": "2025-11-08T15:25:00.000Z",
    "currentPrice": 585.42,
    "impliedVolatility": 12.5,
    "putCallOIRatio": 0.85,
    "putCallVolRatio": 1.2,
    "optionsVolume": 1250000,
    "dailyChange": 1.25,
    "dailyChangePercent": 0.21
  }
}
```

**Response (VIX):**
```json
{
  "success": true,
  "data": {
    "timestamp": "2025-11-08T15:25:00.000Z",
    "currentPrice": 14.25,
    "change": -0.35,
    "changePercent": -2.4,
    "vix1m": 14.5,
    "vix3m": 15.2,
    "vix6m": 16.1,
    "termStructure": "normal"
  }
}
```

**Python:**
```python
spy = api.get_spy_data()
qqq = api.get_qqq_data()
vix = api.get_vix_data()

print(f"SPY: ${spy['data']['currentPrice']}")
print(f"VIX: {vix['data']['currentPrice']}")
```

---

### GET /api/historical/{symbol}
**Purpose:** Get historical data for a symbol

**Parameters:**
- `symbol` (path) - Stock symbol
- `start` (query, optional) - Start date (YYYY-MM-DD)
- `end` (query, optional) - End date (YYYY-MM-DD)

**Response:**
```json
{
  "success": true,
  "symbol": "SPY",
  "count": 50,
  "data": [
    {
      "timestamp": "2025-11-08T15:00:00.000Z",
      "currentPrice": 585.42,
      "impliedVolatility": 12.5,
      "putCallOIRatio": 0.85
    },
    {
      "timestamp": "2025-11-08T14:00:00.000Z",
      "currentPrice": 584.20,
      "impliedVolatility": 12.6,
      "putCallOIRatio": 0.87
    }
  ]
}
```

**Python:**
```python
# Get last 7 days
history = api.get_historical('SPY', start_date='2025-11-01', end_date='2025-11-08')

# All available history
all_history = api.get_historical('SPY')
```

---

## Max Pain Endpoints

### GET /api/maxpain/{symbol}
**Purpose:** Get latest max pain data for ALL expirations (35+ expirations)

**Parameters:**
- `symbol` (path) - Stock symbol (SPY, QQQ)

**Response:**
```json
{
  "success": true,
  "symbol": "SPY",
  "count": 35,
  "data": [
    {
      "expiration_date": "Nov 11, 2025",
      "max_pain_price": 583.0,
      "days_until_expiry": 3,
      "total_oi": 2500000,
      "timestamp": "2025-11-08T15:20:00.000Z"
    },
    {
      "expiration_date": "Nov 18, 2025",
      "max_pain_price": 580.0,
      "days_until_expiry": 10,
      "total_oi": 1800000,
      "timestamp": "2025-11-08T15:20:00.000Z"
    }
  ]
}
```

**Python:**
```python
all_expirations = api.get_maxpain('SPY')
print(f"Total expirations: {all_expirations['count']}")
```

---

### GET /api/maxpain/{symbol}/weekly
**Purpose:** Get weekly max pain expirations (≤7 days)

**Response:**
```json
{
  "success": true,
  "symbol": "SPY",
  "count": 2,
  "data": [
    {
      "expiration_date": "Nov 11, 2025",
      "max_pain_price": 583.0,
      "days_until_expiry": 3,
      "total_oi": 2500000,
      "timestamp": "2025-11-08T15:20:00.000Z"
    }
  ]
}
```

**Python:**
```python
weekly = api.get_maxpain_weekly('SPY')
nearest = weekly['data'][0]
print(f"Nearest expiration: {nearest['expiration_date']} @ ${nearest['max_pain_price']}")
```

**Use Case:** Short-term max pain levels for trading

---

### GET /api/maxpain/{symbol}/monthly
**Purpose:** Get monthly max pain expirations (~30 days)

**Response:**
```json
{
  "success": true,
  "symbol": "SPY",
  "count": 4,
  "data": [...]
}
```

**Python:**
```python
monthly = api.get_maxpain_monthly('SPY')
```

**Use Case:** Medium-term max pain levels

---

### GET /api/maxpain/{symbol}/history
**Purpose:** Get max pain data for the last N days

**Parameters:**
- `days` (query) - Number of days of history (default: 7)

**Response:**
```json
{
  "success": true,
  "symbol": "SPY",
  "days": 7,
  "count": 245,
  "data": [...]
}
```

**Python:**
```python
# Last 7 days
history = api.get_maxpain_history('SPY', days=7)

# Last 30 days
month_history = api.get_maxpain_history('SPY', days=30)
```

**Use Case:** Track how max pain changed over time

---

### GET /api/maxpain/{symbol}/expiration/{date}
**Purpose:** Track how max pain for a specific expiration changed over time

**Parameters:**
- `symbol` (path) - Stock symbol
- `date` (path) - Expiration date (e.g., "Nov 12, 2025")

**Response:**
```json
{
  "success": true,
  "symbol": "SPY",
  "expirationDate": "Nov 12, 2025",
  "data": [
    {
      "timestamp": "2025-11-08T15:00:00.000Z",
      "max_pain_price": 583.0,
      "total_oi": 2500000,
      "days_until_expiry": 4
    },
    {
      "timestamp": "2025-11-08T14:00:00.000Z",
      "max_pain_price": 584.0,
      "total_oi": 2480000,
      "days_until_expiry": 4
    }
  ]
}
```

**Python:**
```python
expiration_track = api.track_expiration('SPY', 'Nov 12, 2025')
```

**Use Case:** See how max pain moved throughout the day for specific expiration

---

## Chat Message Endpoints

### GET /api/chat/latest
**Purpose:** Get all chat messages from most recent scrape

**Response:**
```json
{
  "success": true,
  "count": 50,
  "data": [
    {
      "timestamp": "2025-11-08T15:15:00.000Z",
      "username": "trader123",
      "message": "SPY looking bullish today",
      "scrape_timestamp": "2025-11-08T15:20:00.000Z"
    },
    {
      "timestamp": "2025-11-08T15:14:30.000Z",
      "username": "bear_market_guy",
      "message": "VIX too low, expecting correction",
      "scrape_timestamp": "2025-11-08T15:20:00.000Z"
    }
  ]
}
```

**Python:**
```python
chat = api.get_chat_latest()
for msg in chat['data']:
    print(f"{msg['username']}: {msg['message']}")
```

**Use Case:** Market sentiment analysis from wallstreet.io chat

---

### GET /api/chat/user/{username}
**Purpose:** Get chat messages from specific user

**Parameters:**
- `username` (path) - Username (case sensitive)

**Response:**
```json
{
  "success": true,
  "username": "trader123",
  "count": 10,
  "data": [...]
}
```

**Python:**
```python
user_messages = api.get_chat_by_user('trader123')
```

---

### GET /api/chat/user/{username}/latest
**Purpose:** Get latest messages from specific user

**Python:**
```python
latest = api.get_chat_by_user('trader123', latest_only=True)
```

---

### GET /api/chat/history
**Purpose:** Get chat messages from last N days

**Parameters:**
- `days` (query) - Number of days (default: 7)

**Response:**
```json
{
  "success": true,
  "days": 7,
  "count": 350,
  "data": [...]
}
```

**Python:**
```python
week = api.get_chat_history(days=7)
month = api.get_chat_history(days=30)
```

---

## Scrape History Endpoints

### GET /api/history
**Purpose:** Get recent scrape metadata showing execution history

**Parameters:**
- `limit` (query) - Number of records (default: 10)

**Response:**
```json
{
  "success": true,
  "count": 10,
  "data": [
    {
      "timestamp": "2025-11-08T15:25:00.000Z",
      "duration": "45.3s",
      "success": true,
      "etf_records": 2,
      "vix_records": 1,
      "maxpain_records": 70,
      "chat_records": 50
    },
    {
      "timestamp": "2025-11-08T15:10:00.000Z",
      "duration": "42.1s",
      "success": true,
      "etf_records": 2,
      "vix_records": 1,
      "maxpain_records": 68,
      "chat_records": 48
    }
  ]
}
```

**Python:**
```python
history = api.get_scrape_history(limit=20)
```

**Use Case:** Monitor scraper reliability and performance

---

## Export & Backup Endpoints

### GET /api/export/json
**Purpose:** Export all data as JSON file

**Parameters:**
- `metadata` (query) - Include system metadata (default: true)

**Response:** Binary JSON file

**Python:**
```python
# Export with metadata
json_data = api.export_json(include_metadata=True)

# Save to file
with open('export.json', 'wb') as f:
    f.write(json_data)
```

**Use Case:** Full data backup, archival

---

### GET /api/export/csv
**Purpose:** Export specific table as CSV

**Parameters:**
- `table` (query) - Table name (etf_data, vix_data, max_pain_data, chat_messages, scrape_metadata)

**Response:** Binary CSV file

**Python:**
```python
# Export ETF data as CSV
csv_data = api.export_csv('etf_data')

with open('etf_data.csv', 'wb') as f:
    f.write(csv_data)
```

**Use Case:** Data analysis in Excel/spreadsheets

---

### POST /api/backup
**Purpose:** Create timestamped database backup on server

**Response:**
```json
{
  "success": true,
  "message": "Backup created successfully",
  "backupPath": "/var/backups/market_data_2025-11-08_15-30-00.db",
  "timestamp": "2025-11-08T15:30:00.000Z"
}
```

**Python:**
```python
backup = api.create_backup()
print(f"Backup created: {backup['backupPath']}")
```

**Use Case:** Pre-migration backups, disaster recovery

---

## Helper Methods

### is_healthy()
**Purpose:** Quick health check (returns boolean)

**Python:**
```python
if api.is_healthy():
    print("Server is up!")
else:
    print("Server is down!")
```

---

### is_data_fresh(max_age_hours)
**Purpose:** Check if latest data is fresh (< max_age_hours old)

**Parameters:**
- `max_age_hours` (int) - Maximum age in hours (default: 1)

**Python:**
```python
if api.is_data_fresh(max_age_hours=1):
    print("Data is fresh (< 1 hour old)")
else:
    print("Data is stale")
```

---

### get_data_age_minutes()
**Purpose:** Get age of latest data in minutes

**Returns:** Float (minutes) or None if unavailable

**Python:**
```python
age = api.get_data_age_minutes()
if age:
    print(f"Data is {age:.1f} minutes old")
```

---

## Error Handling

### Error Response Format
```json
{
  "success": false,
  "error": "Error message",
  "statusCode": 404
}
```

### Common Errors

**404 Not Found:**
```json
{
  "success": false,
  "error": "Resource not found: /api/latest/INVALID"
}
```

**500 Server Error:**
```json
{
  "success": false,
  "error": "Database connection failed"
}
```

### Python Error Handling

```python
from scripts.trading.api_client import APIClientError

try:
    data = api.get_spy_data()
except APIClientError as e:
    print(f"API error: {e}")
    # Handle error (use cached data, retry, etc.)
```

---

## Best Practices

### 1. Use /api/summary for Bulk Updates
**DO:**
```python
# One call gets everything
summary = api.get_summary()
spy = summary['etf_data']['data'][0]
vix = summary['vix_data']['data']
maxpain = summary['max_pain_data']['spy_weekly']
```

**DON'T:**
```python
# Multiple calls (slow!)
spy = api.get_spy_data()
qqq = api.get_qqq_data()
vix = api.get_vix_data()
maxpain = api.get_maxpain_weekly('SPY')
```

### 2. Check Data Freshness First
```python
if not api.is_data_fresh(max_age_hours=1):
    print("Warning: Data is stale, consider re-scraping")
```

### 3. Use Context Manager
```python
# Good - automatically closes connection
with get_client() as api:
    data = api.get_summary()

# Bad - must manually close
api = MarketDataAPI()
data = api.get_summary()
api.close()  # Easy to forget!
```

### 4. Handle Errors Gracefully
```python
try:
    summary = api.get_summary()
except APIClientError:
    # Fallback to cached data
    summary = load_cached_data()
```

### 5. Validate Data Before Use
```python
summary = api.get_summary()

if summary.get('success') and summary.get('etf_data', {}).get('count', 0) > 0:
    # Data is valid
    spy = summary['etf_data']['data'][0]
else:
    # Data is invalid/missing
    print("Error: No ETF data available")
```

---

## Scout Integration

### Typical Scout Update Workflow

```python
from scripts.trading.api_client import get_client

def scout_collect_market_data():
    """Collect all market data for Scout dashboard"""

    with get_client() as api:
        # 1. Health check
        if not api.is_healthy():
            raise Exception("API server unavailable")

        # 2. Check data freshness
        age_minutes = api.get_data_age_minutes()
        if age_minutes and age_minutes > 60:
            print(f"Warning: Data is {age_minutes:.0f} minutes old")

        # 3. Get everything in one call
        summary = api.get_summary()

        # 4. Validate
        if not summary.get('success'):
            raise Exception("API returned error")

        # 5. Extract what we need
        market_data = {
            'timestamp': summary['timestamp'],
            'spy': summary['etf_data']['data'][0],
            'qqq': summary['etf_data']['data'][1],
            'vix': summary['vix_data']['data'],
            'maxpain_spy': summary['max_pain_data']['spy_weekly'][0],
            'maxpain_qqq': summary['max_pain_data']['qqq_weekly'][0],
            'chat': summary['chat_messages']['data'][:10],  # Top 10
            'data_age_minutes': age_minutes
        }

        return market_data

# Use in Scout update
market_data = scout_collect_market_data()
# Transform to dashboard format
# Build dashboard.json
```

---

## Performance

### Response Times (Typical)
- `/health` - <10ms
- `/api/status` - <50ms
- `/api/latest/{symbol}` - <100ms
- `/api/summary` - <200ms (all data)
- `/api/maxpain/{symbol}` - <150ms
- `/api/export/json` - 1-2s (large file)

### Optimization Tips
1. Use `/api/summary` instead of multiple calls (5x faster)
2. Check freshness before fetching (avoid unnecessary calls)
3. Cache responses when appropriate
4. Use weekly/monthly filters for max pain (smaller responses)

---

## Changelog

### v1.0 (2025-11-08)
- Initial API reference documentation
- Documented all endpoints from `api_client.py`
- Added Scout integration examples
- Added best practices section

---

## Support

**Server Issues:** Check server logs on 192.168.10.56
**Client Issues:** Review `scripts/trading/api_client.py`
**Documentation:** See `SCOUT_SYSTEM_GUIDE.md`

---

**Last Verified:** 2025-11-08
**API Version:** 1.0
**Client Version:** 1.0
