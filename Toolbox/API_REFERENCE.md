# Unified Data Collection System - API Reference

**Version:** 2.4.0
**Last Updated:** November 2025

## Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Data Sources](#data-sources)
- [API Endpoints](#api-endpoints)
  - [ETF & VIX Data](#etf--vix-data-endpoints)
  - [Max Pain Data](#max-pain-data-endpoints)
  - [Chat Messages](#chat-messages-endpoints)
  - [RSS News](#rss-news-endpoints)
  - [YouTube Transcripts](#youtube-transcripts-endpoints)
  - [Feed Configuration](#feed-configuration-endpoints)
  - [System Management](#system-management-endpoints)
- [Data Schemas](#data-schemas)
- [Example Use Cases](#example-use-cases)
- [Network Access](#network-access)

---

## Overview

The **Unified Data Collection System** is a comprehensive market data aggregation platform that scrapes, stores, and serves:
- ETF volatility metrics (SPY, QQQ)
- VIX volatility index data
- Options max pain analysis (35+ expirations per symbol)
- Trading community chat messages
- Financial news RSS feeds (today's articles only)
- YouTube financial analysis with AI-generated summaries

All data is stored in SQLite and accessible via a REST API on port 3000.

---

## Quick Start

### Starting the API Server

```bash
# Install dependencies
npm install

# Start the API server
npm run api
```

The server will be available at:
- **Base URL:** `http://localhost:3000`
- **Web Dashboard:** `http://localhost:3000/`
- **API Documentation:** `http://localhost:3000/api/docs`
- **System Status:** `http://localhost:3000/api/status`

### Running the Data Scraper

```bash
# Run all scrapers (5 phases)
npm run scrape
```

This executes:
1. **Phase 1:** ETF Data (SPY, QQQ, VIX)
2. **Phase 2:** Max Pain Data (SPY, QQQ)
3. **Phase 3:** Chat Messages (wallstreet.io)
4. **Phase 4:** RSS Feeds (today's articles only)
5. **Phase 5:** YouTube Transcripts with AI summaries

---

## Architecture

### Database Structure

The system uses **SQLite** with 9 separate tables:

| Table | Purpose | Records Per Scrape |
|-------|---------|-------------------|
| `etf_data` | SPY, QQQ volatility metrics | 2 rows |
| `vix_data` | VIX index data | 1 row |
| `max_pain_data` | Options max pain tracking | 35+ rows per symbol |
| `chat_messages` | Trading chat messages | 50-100 rows |
| `rss_articles` | Financial news articles | Variable (today only) |
| `youtube_transcripts` | Video transcripts + AI summaries | Variable |
| `rss_feed_config` | RSS feed configuration | N/A (config) |
| `youtube_channel_config` | YouTube channel configuration | N/A (config) |
| `scrape_metadata` | Scraper execution history | 1 row per scrape |

**Database Location:** `data/etf_data.db`

### Scraper Frequency

- **Recommended:** Once per hour (24x per day)
- **Rate Limiting:** 10-second delays between symbols
- **RSS Filtering:** Only articles published today (UTC)

---

## Data Sources

| Data Type | Source | Update Frequency |
|-----------|--------|------------------|
| ETF Data (SPY, QQQ) | Barchart.com | Real-time |
| VIX Data | Barchart.com | Real-time |
| Max Pain | optioncharts.io | Real-time |
| Chat Messages | wallstreet.io | Real-time |
| RSS Feeds | Multiple providers (configurable) | Varies |
| YouTube | Channels (configurable) | Varies |

---

## API Endpoints

### Base URL
```
http://localhost:3000
```

All successful responses include:
```json
{
  "success": true,
  ...
}
```

All error responses include:
```json
{
  "success": false,
  "error": "Error message here"
}
```

---

## ETF & VIX Data Endpoints

### GET `/api/latest`
Get latest data for **all symbols** (SPY, QQQ, VIX).

**Example:**
```bash
curl http://localhost:3000/api/latest
```

**Response:**
```json
{
  "success": true,
  "count": 3,
  "data": [
    {
      "symbol": "SPY",
      "timestamp": "2025-11-13T10:30:00.000Z",
      "current_price": 450.23,
      "implied_volatility": "12.34%",
      "historical_volatility": "11.56%",
      "iv_percentile": "45.6%",
      "iv_rank": "0.456",
      "volume": 123456789,
      "open_interest": 9876543,
      "put_call_vol_ratio": 0.87,
      "put_call_oi_ratio": 0.92,
      "iv_30day": "12.10%",
      "hv_30day": "11.40%"
    },
    {
      "symbol": "QQQ",
      "timestamp": "2025-11-13T10:30:00.000Z",
      "current_price": 380.45,
      ...
    },
    {
      "symbol": "VIX",
      "timestamp": "2025-11-13T10:30:00.000Z",
      "current_price": 15.67,
      "change": "+0.45",
      "change_percent": "+2.95%",
      "day_range": "15.20 - 15.90",
      "week_52_range": "12.45 - 28.90",
      "volume": "N/A",
      "prev_close": 15.22
    }
  ]
}
```

---

### GET `/api/latest/:symbol`
Get latest data for a **specific symbol** (case-insensitive).

**Parameters:**
- `symbol` (path): `SPY`, `QQQ`, or `VIX`

**Example:**
```bash
curl http://localhost:3000/api/latest/SPY
```

**Response:**
```json
{
  "success": true,
  "data": {
    "symbol": "SPY",
    "timestamp": "2025-11-13T10:30:00.000Z",
    "current_price": 450.23,
    "implied_volatility": "12.34%",
    "historical_volatility": "11.56%",
    "iv_percentile": "45.6%",
    "iv_rank": "0.456",
    "volume": 123456789,
    "open_interest": 9876543,
    "put_call_vol_ratio": 0.87,
    "put_call_oi_ratio": 0.92,
    "iv_30day": "12.10%",
    "hv_30day": "11.40%"
  }
}
```

---

### GET `/api/historical/:symbol`
Get historical data for a symbol with optional date filtering.

**Parameters:**
- `symbol` (path): Symbol name
- `start` (query, optional): Start date in `YYYY-MM-DD` format
- `end` (query, optional): End date in `YYYY-MM-DD` format

**Example:**
```bash
curl "http://localhost:3000/api/historical/SPY?start=2025-01-01&end=2025-01-31"
```

**Response:**
```json
{
  "success": true,
  "symbol": "SPY",
  "count": 150,
  "filters": {
    "startDate": "2025-01-01",
    "endDate": "2025-01-31"
  },
  "data": [
    {
      "symbol": "SPY",
      "timestamp": "2025-01-31T15:00:00.000Z",
      "current_price": 448.50,
      ...
    },
    ...
  ]
}
```

---

### GET `/api/all`
Get **all data** from ETF and VIX tables (⚠️ large dataset).

**Example:**
```bash
curl http://localhost:3000/api/all
```

---

## Max Pain Data Endpoints

Max Pain endpoints return data from the **most recent scrape** by default. Each scrape produces 35+ expirations per symbol.

### GET `/api/maxpain/:symbol`
Get latest max pain data for all expirations.

**Parameters:**
- `symbol` (path): `SPY` or `QQQ` only

**Example:**
```bash
curl http://localhost:3000/api/maxpain/SPY
```

**Response:**
```json
{
  "success": true,
  "symbol": "SPY",
  "count": 38,
  "data": [
    {
      "symbol": "SPY",
      "scrape_timestamp": "2025-11-13T10:35:00.000Z",
      "expiration_date": "Nov 15, 2025",
      "days_until_expiry": 2,
      "max_pain_price": 448.00
    },
    {
      "expiration_date": "Nov 22, 2025",
      "days_until_expiry": 9,
      "max_pain_price": 445.50
    },
    ...
  ]
}
```

---

### GET `/api/maxpain/:symbol/weekly`
Get max pain for **weekly expirations** (7 days or less).

**Example:**
```bash
curl http://localhost:3000/api/maxpain/SPY/weekly
```

**Response:**
```json
{
  "success": true,
  "symbol": "SPY",
  "count": 2,
  "data": [
    {
      "expiration_date": "Nov 15, 2025",
      "days_until_expiry": 2,
      "max_pain_price": 448.00
    },
    {
      "expiration_date": "Nov 18, 2025",
      "days_until_expiry": 5,
      "max_pain_price": 447.00
    }
  ]
}
```

---

### GET `/api/maxpain/:symbol/monthly`
Get max pain for **monthly expirations** (around 30 days out).

**Example:**
```bash
curl http://localhost:3000/api/maxpain/SPY/monthly
```

---

### GET `/api/maxpain/:symbol/history`
Get max pain history across multiple scrapes.

**Parameters:**
- `symbol` (path): Symbol name
- `days` (query, optional): Number of days to look back (default: 7)

**Example:**
```bash
curl "http://localhost:3000/api/maxpain/SPY/history?days=14"
```

**Response:**
```json
{
  "success": true,
  "symbol": "SPY",
  "days": 14,
  "count": 500,
  "data": [
    {
      "scrape_timestamp": "2025-11-13T10:35:00.000Z",
      "expiration_date": "Nov 15, 2025",
      "days_until_expiry": 2,
      "max_pain_price": 448.00
    },
    {
      "scrape_timestamp": "2025-11-13T09:30:00.000Z",
      "expiration_date": "Nov 15, 2025",
      "days_until_expiry": 2,
      "max_pain_price": 447.50
    },
    ...
  ]
}
```

---

### GET `/api/maxpain/:symbol/expiration/:date`
Track how max pain for a **specific expiration date** changed over time.

**Parameters:**
- `symbol` (path): Symbol name
- `date` (path): Expiration date (URL encoded, e.g., `Nov%2015%2C%202025`)

**Example:**
```bash
curl "http://localhost:3000/api/maxpain/SPY/expiration/Nov%2015%2C%202025"
```

**Response:**
```json
{
  "success": true,
  "symbol": "SPY",
  "expirationDate": "Nov 15, 2025",
  "count": 24,
  "data": [
    {
      "scrape_timestamp": "2025-11-13T10:35:00.000Z",
      "days_until_expiry": 2,
      "max_pain_price": 448.00
    },
    {
      "scrape_timestamp": "2025-11-13T09:30:00.000Z",
      "days_until_expiry": 2,
      "max_pain_price": 447.50
    },
    ...
  ]
}
```

---

## Chat Messages Endpoints

### GET `/api/chat/latest`
Get latest chat messages from wallstreet.io community.

**Parameters:**
- `limit` (query, optional): Number of messages to return (default: 100)

**Example:**
```bash
curl "http://localhost:3000/api/chat/latest?limit=50"
```

**Response:**
```json
{
  "success": true,
  "count": 50,
  "data": [
    {
      "username": "fetersynergy",
      "message_text": "SPY looking bullish today. 450 calls printing.",
      "message_timestamp": "10:40 am",
      "scrape_timestamp": "2025-11-13T10:40:00.000Z"
    },
    ...
  ]
}
```

---

### GET `/api/chat/user/:username`
Get all chat messages from a specific user.

**Parameters:**
- `username` (path): Username to search for

**Example:**
```bash
curl http://localhost:3000/api/chat/user/fetersynergy
```

---

### GET `/api/chat/user/:username/latest`
Get latest messages from a specific user.

**Example:**
```bash
curl http://localhost:3000/api/chat/user/fetersynergy/latest
```

---

### GET `/api/chat/history`
Get chat message history with time filtering.

**Parameters:**
- `days` (query, optional): Number of days to look back (default: 7)

**Example:**
```bash
curl "http://localhost:3000/api/chat/history?days=30"
```

---

## RSS News Endpoints

**Note:** RSS scraper filters articles to **today's publications only** (UTC calendar day).

### GET `/api/rss/latest`
Get latest RSS articles across all providers.

**Parameters:**
- `limit` (query, optional): Number of articles to return (default: 20)

**Example:**
```bash
curl "http://localhost:3000/api/rss/latest?limit=10"
```

**Response:**
```json
{
  "success": true,
  "count": 10,
  "data": [
    {
      "id": 1234,
      "article_id": "a1b2c3",
      "provider": "MarketWatch",
      "feed_name": "Top Stories",
      "title": "Fed signals potential rate cut in Q1 2025",
      "link": "https://marketwatch.com/article/...",
      "author": "Jane Doe",
      "content": "Full article text...",
      "summary": "The Federal Reserve indicated...",
      "published_date": "2025-11-13T09:15:00.000Z",
      "scraped_at": "2025-11-13T10:20:00.000Z",
      "tags": "economy, fed, rates"
    },
    ...
  ]
}
```

---

### GET `/api/rss/provider/:provider`
Get RSS articles from a specific provider.

**Parameters:**
- `provider` (path): Provider name (e.g., `MarketWatch`)
- `limit` (query, optional): Number of articles (default: 20)

**Example:**
```bash
curl "http://localhost:3000/api/rss/provider/MarketWatch?limit=5"
```

---

### GET `/api/rss/article/:id`
Get a single RSS article by ID.

**Parameters:**
- `id` (path): Article ID (integer)

**Example:**
```bash
curl http://localhost:3000/api/rss/article/1234
```

---

### GET `/api/rss/providers`
Get list of all RSS providers.

**Example:**
```bash
curl http://localhost:3000/api/rss/providers
```

**Response:**
```json
{
  "success": true,
  "count": 5,
  "data": [
    "MarketWatch",
    "Bloomberg",
    "Reuters",
    "CNBC",
    "WSJ"
  ]
}
```

---

### GET `/api/rss/stats`
Get RSS statistics.

**Example:**
```bash
curl http://localhost:3000/api/rss/stats
```

**Response:**
```json
{
  "success": true,
  "totalArticles": 350,
  "totalProviders": 5,
  "providers": [
    "MarketWatch",
    "Bloomberg",
    ...
  ]
}
```

---

### POST `/api/rss/scrape`
Manually trigger RSS scraper.

**Example:**
```bash
curl -X POST http://localhost:3000/api/rss/scrape
```

**Response:**
```json
{
  "success": true,
  "message": "RSS scrape completed successfully",
  "timestamp": "2025-11-13T10:45:00.000Z"
}
```

---

## YouTube Transcripts Endpoints

### GET `/api/youtube/latest`
Get latest YouTube transcripts with AI summaries.

**Parameters:**
- `limit` (query, optional): Number of transcripts (default: 20)

**Example:**
```bash
curl "http://localhost:3000/api/youtube/latest?limit=5"
```

**Response:**
```json
{
  "success": true,
  "count": 5,
  "data": [
    {
      "id": 567,
      "video_id": "dQw4w9WgXcQ",
      "channel_handle": "@financialguru",
      "channel_name": "Financial Guru",
      "title": "Stock Market Analysis - November 2025",
      "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
      "transcript": "Full transcript text...",
      "published_date": "2025-11-12T14:00:00.000Z",
      "scraped_at": "2025-11-13T10:15:00.000Z",
      "summary": "The analyst discusses current market conditions...",
      "summary_generated_at": "2025-11-13T10:17:00.000Z",
      "ollama_model": "llama3.2:3b",
      "summary_error": null
    },
    ...
  ]
}
```

---

### GET `/api/youtube/channel/:channelHandle`
Get transcripts from a specific YouTube channel.

**Parameters:**
- `channelHandle` (path): Channel handle (e.g., `@financialguru`)
- `limit` (query, optional): Number of transcripts (default: 10)

**Example:**
```bash
curl "http://localhost:3000/api/youtube/channel/@financialguru?limit=5"
```

---

### GET `/api/youtube/transcript/:videoId`
Get a single transcript by video ID.

**Parameters:**
- `videoId` (path): YouTube video ID

**Example:**
```bash
curl http://localhost:3000/api/youtube/transcript/dQw4w9WgXcQ
```

---

### GET `/api/youtube/channels`
Get list of all YouTube channels being tracked.

**Example:**
```bash
curl http://localhost:3000/api/youtube/channels
```

**Response:**
```json
{
  "success": true,
  "count": 3,
  "data": [
    "@financialguru",
    "@stockanalyst",
    "@marketwatch"
  ]
}
```

---

### GET `/api/youtube/stats`
Get YouTube statistics including summary generation metrics.

**Example:**
```bash
curl http://localhost:3000/api/youtube/stats
```

**Response:**
```json
{
  "success": true,
  "totalTranscripts": 45,
  "totalChannels": 3,
  "successfulSummaries": 42,
  "failedSummaries": 3,
  "errorRate": "6.7%",
  "channels": ["@financialguru", "@stockanalyst", "@marketwatch"],
  "recentErrors": [
    {
      "video_id": "xyz123",
      "channel_name": "Financial Guru",
      "title": "Market Analysis",
      "summary_error": "Ollama connection timeout",
      "scraped_at": "2025-11-13T09:30:00.000Z"
    }
  ]
}
```

---

### POST `/api/youtube/scrape`
Manually trigger YouTube scraper.

**Example:**
```bash
curl -X POST http://localhost:3000/api/youtube/scrape
```

---

## Feed Configuration Endpoints

Manage RSS and YouTube feed sources dynamically via API.

### RSS Feed Configuration

#### GET `/api/config/rss`
Get all RSS feed configurations.

**Parameters:**
- `enabled` (query, optional): Filter by enabled status (`true`/`false`)

**Example:**
```bash
curl "http://localhost:3000/api/config/rss?enabled=true"
```

**Response:**
```json
{
  "success": true,
  "count": 8,
  "data": [
    {
      "id": 1,
      "provider": "MarketWatch",
      "feed_name": "Top Stories",
      "feed_url": "https://www.marketwatch.com/rss/topstories",
      "enabled": true,
      "priority": 5,
      "error_count": 0,
      "last_scraped_at": "2025-11-13T10:20:00.000Z",
      "created_at": "2025-11-01T12:00:00.000Z",
      "updated_at": "2025-11-13T10:20:00.000Z"
    },
    ...
  ]
}
```

---

#### POST `/api/config/rss`
Create a new RSS feed configuration.

**Request Body:**
```json
{
  "provider": "Bloomberg",
  "feed_name": "Markets",
  "feed_url": "https://www.bloomberg.com/markets.rss",
  "enabled": true,
  "priority": 7
}
```

**Response:**
```json
{
  "success": true,
  "id": 9,
  "message": "RSS feed created successfully"
}
```

---

#### PUT `/api/config/rss/:id`
Update an existing RSS feed configuration.

**Request Body:**
```json
{
  "priority": 8,
  "enabled": true
}
```

---

#### DELETE `/api/config/rss/:id`
Delete an RSS feed configuration.

**Example:**
```bash
curl -X DELETE http://localhost:3000/api/config/rss/9
```

---

#### POST `/api/config/rss/:id/toggle`
Toggle RSS feed enabled/disabled status.

**Example:**
```bash
curl -X POST http://localhost:3000/api/config/rss/9/toggle
```

**Response:**
```json
{
  "success": true,
  "enabled": false,
  "message": "RSS feed disabled successfully"
}
```

---

### YouTube Channel Configuration

#### GET `/api/config/youtube`
Get all YouTube channel configurations.

**Parameters:**
- `enabled` (query, optional): Filter by enabled status

**Example:**
```bash
curl "http://localhost:3000/api/config/youtube?enabled=true"
```

---

#### POST `/api/config/youtube`
Create a new YouTube channel configuration.

**Request Body:**
```json
{
  "channel_handle": "@newfinancechannel",
  "channel_name": "New Finance Channel",
  "weight": 7,
  "category": "Technical Analysis",
  "description": "Daily TA and market insights",
  "enabled": true
}
```

---

#### PUT `/api/config/youtube/:id`
Update YouTube channel configuration.

---

#### DELETE `/api/config/youtube/:id`
Delete YouTube channel configuration.

---

#### POST `/api/config/youtube/:id/toggle`
Toggle YouTube channel enabled/disabled status.

---

#### GET `/api/config/stats`
Get feed configuration statistics.

**Example:**
```bash
curl http://localhost:3000/api/config/stats
```

**Response:**
```json
{
  "success": true,
  "data": {
    "rss": {
      "total": 8,
      "enabled": 7,
      "disabled": 1,
      "providers": 5,
      "byProvider": {
        "MarketWatch": 2,
        "Bloomberg": 3,
        "Reuters": 1,
        "CNBC": 1,
        "WSJ": 1
      }
    },
    "youtube": {
      "total": 5,
      "enabled": 4,
      "disabled": 1,
      "categories": 3,
      "byCategory": {
        "Technical Analysis": 2,
        "News": 1,
        "Market Commentary": 2
      }
    }
  }
}
```

---

## System Management Endpoints

### GET `/api/docs`
Get comprehensive API documentation (returns this reference as JSON).

**Example:**
```bash
curl http://localhost:3000/api/docs
```

---

### GET `/api/status`
Get comprehensive system status across all tables.

**Example:**
```bash
curl http://localhost:3000/api/status
```

**Response:**
```json
{
  "success": true,
  "database": {
    "path": "data/etf_data.db",
    "size": "1.23 MB",
    "tables": [
      "etf_data",
      "vix_data",
      "max_pain_data",
      "chat_messages",
      "rss_articles",
      "youtube_transcripts",
      "rss_feed_config",
      "youtube_channel_config",
      "scrape_metadata"
    ]
  },
  "tables": {
    "etf_data": {
      "exists": true,
      "rowCount": 150
    },
    "vix_data": {
      "exists": true,
      "rowCount": 75
    },
    "max_pain_data": {
      "exists": true,
      "rowCount": 2800
    },
    "chat_messages": {
      "exists": true,
      "rowCount": 1200
    },
    "rss_articles": {
      "exists": true,
      "rowCount": 350
    },
    "youtube_transcripts": {
      "exists": true,
      "rowCount": 45
    }
  },
  "lastScrape": {
    "timestamp": "2025-11-13T10:30:00.000Z",
    "duration": 45230,
    "success": true,
    "etf_success": true,
    "etf_count": 2,
    "vix_success": true,
    "maxpain_success": true,
    "maxpain_count": 76,
    "chat_success": true,
    "chat_count": 50,
    "rss_success": true,
    "rss_count": 12,
    "youtube_success": true,
    "youtube_count": 3,
    "errors": ""
  },
  "health": {
    "healthy": true,
    "errors": []
  }
}
```

---

### GET `/api/summary`
Get all latest data from ALL tables in one API call.

**Example:**
```bash
curl http://localhost:3000/api/summary
```

**Response:**
```json
{
  "success": true,
  "timestamp": "2025-11-13T10:45:00.000Z",
  "system": {
    "database": {
      "path": "data/etf_data.db",
      "size": "1.23 MB"
    },
    "lastScrape": {
      "timestamp": "2025-11-13T10:30:00.000Z",
      "duration": 45230,
      "success": true
    }
  },
  "data": {
    "etf": [...],
    "vix": {...},
    "maxPain": [...],
    "chat": [...]
  },
  "rss": {
    "latest": [...],
    "count": 5
  },
  "youtube": {
    "latest": [...],
    "count": 5
  },
  "counts": {
    "etf": 2,
    "vix": 1,
    "maxPain": 76,
    "chat": 50,
    "rss": 5,
    "youtube": 5
  }
}
```

---

### GET `/api/history`
Get scrape execution history with timestamps.

**Parameters:**
- `limit` (query, optional): Number of history records (default: 10)

**Example:**
```bash
curl "http://localhost:3000/api/history?limit=5"
```

**Response:**
```json
{
  "success": true,
  "count": 5,
  "data": [
    {
      "scrape_timestamp": "2025-11-13T10:30:00.000Z",
      "duration_ms": 45230,
      "success": true,
      "etf_success": true,
      "etf_count": 2,
      "vix_success": true,
      "maxpain_success": true,
      "maxpain_count": 76,
      "chat_success": true,
      "chat_count": 50,
      "rss_success": true,
      "rss_count": 12,
      "youtube_success": true,
      "youtube_count": 3,
      "errors": ""
    },
    ...
  ]
}
```

---

### GET `/api/export/json`
Export all data as downloadable JSON file.

**Parameters:**
- `metadata` (query, optional): Include metadata (default: `true`)

**Example:**
```bash
curl "http://localhost:3000/api/export/json?metadata=false" -O -J
```

**Response:** File download (`etf_data_export_2025-11-13.json`)

---

### GET `/api/export/csv`
Export data as CSV (per-table or info about all tables).

**Parameters:**
- `table` (query, optional): Specific table name (`etf_data`, `vix_data`, `max_pain_data`, `chat_messages`, `rss_articles`, `youtube_transcripts`)

**Example:**
```bash
# Get info about available tables
curl http://localhost:3000/api/export/csv

# Download specific table
curl "http://localhost:3000/api/export/csv?table=etf_data" -O -J
```

**Response (no table specified):**
```json
{
  "success": true,
  "message": "CSV export ready. Use ?table=<table_name> to download a specific table",
  "availableTables": [
    "etf_data",
    "vix_data",
    "max_pain_data",
    "chat_messages",
    "rss_articles",
    "youtube_transcripts"
  ],
  "urls": [
    {
      "table": "etf_data",
      "url": "/api/export/csv?table=etf_data"
    },
    ...
  ]
}
```

---

### POST `/api/backup`
Create a timestamped database backup.

**Example:**
```bash
curl -X POST http://localhost:3000/api/backup
```

**Response:**
```json
{
  "success": true,
  "message": "Database backup created successfully",
  "backupPath": "data/backups/etf_data_2025-11-13_10-45-00.db",
  "timestamp": "2025-11-13T10:45:00.000Z"
}
```

---

### GET `/health`
Simple health check endpoint for monitoring.

**Example:**
```bash
curl http://localhost:3000/health
```

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-11-13T10:45:00.000Z"
}
```

---

## Data Schemas

### ETF Data (SPY, QQQ)
```typescript
{
  symbol: string;              // "SPY" or "QQQ"
  timestamp: string;           // ISO 8601 timestamp
  current_price: number;       // Current price
  implied_volatility: string;  // "12.34%"
  historical_volatility: string; // "11.56%"
  iv_percentile: string;       // "45.6%"
  iv_rank: string;            // "0.456"
  volume: number;              // Daily volume
  open_interest: number;       // Total open interest
  put_call_vol_ratio: number;  // 0.87
  put_call_oi_ratio: number;   // 0.92
  iv_30day: string;           // "12.10%"
  hv_30day: string;           // "11.40%"
}
```

### VIX Data
```typescript
{
  symbol: "VIX";
  timestamp: string;           // ISO 8601 timestamp
  current_price: number;       // VIX index value
  change: string;              // "+0.45"
  change_percent: string;      // "+2.95%"
  day_range: string;           // "15.20 - 15.90"
  week_52_range: string;       // "12.45 - 28.90"
  volume: string;              // "N/A" or volume
  prev_close: number;          // Previous close
}
```

### Max Pain Data
```typescript
{
  symbol: string;              // "SPY" or "QQQ"
  scrape_timestamp: string;    // ISO 8601 timestamp
  expiration_date: string;     // "Nov 15, 2025"
  days_until_expiry: number;   // 2
  max_pain_price: number;      // 448.00
}
```

### Chat Message
```typescript
{
  username: string;            // "fetersynergy"
  message_text: string;        // Message content
  message_timestamp: string;   // "10:40 am"
  scrape_timestamp: string;    // ISO 8601 timestamp
}
```

### RSS Article
```typescript
{
  id: number;                  // Database ID
  article_id: string;          // Unique hash
  provider: string;            // "MarketWatch"
  feed_name: string;           // "Top Stories"
  title: string;               // Article title
  link: string;                // Article URL
  author?: string;             // Author name (optional)
  content?: string;            // Full content (optional)
  summary?: string;            // Article summary (optional)
  published_date: string;      // ISO 8601 timestamp
  scraped_at: string;          // ISO 8601 timestamp
  tags?: string;               // "economy, fed, rates" (optional)
}
```

### YouTube Transcript
```typescript
{
  id: number;                  // Database ID
  video_id: string;            // YouTube video ID
  channel_handle: string;      // "@financialguru"
  channel_name: string;        // "Financial Guru"
  title: string;               // Video title
  url: string;                 // YouTube URL
  transcript: string;          // Full transcript text
  published_date: string;      // ISO 8601 timestamp
  scraped_at: string;          // ISO 8601 timestamp
  summary?: string;            // AI-generated summary (optional)
  summary_generated_at?: string; // ISO 8601 timestamp (optional)
  ollama_model?: string;       // "llama3.2:3b" (optional)
  summary_error?: string;      // Error message if summary failed (optional)
}
```

---

## Example Use Cases

### 1. Market Dashboard
Fetch all latest data for a real-time dashboard:

```bash
curl http://localhost:3000/api/summary
```

### 2. Options Analysis
Track how max pain for a specific expiration changed today:

```bash
curl "http://localhost:3000/api/maxpain/SPY/expiration/Nov%2015%2C%202025"
```

### 3. Volatility Alert System
Monitor VIX for sudden spikes:

```bash
# Fetch latest VIX
curl http://localhost:3000/api/latest/VIX

# Compare to historical VIX
curl http://localhost:3000/api/historical/VIX
```

### 4. News Aggregation
Fetch today's financial news:

```bash
curl "http://localhost:3000/api/rss/latest?limit=50"
```

### 5. YouTube Content Analysis
Get AI summaries of latest financial videos:

```bash
curl "http://localhost:3000/api/youtube/latest?limit=10"
```

### 6. Chat Sentiment Analysis
Fetch recent chat messages for sentiment analysis:

```bash
curl "http://localhost:3000/api/chat/latest?limit=100"
```

### 7. Data Export for Analysis
Export all data to JSON for offline analysis:

```bash
curl "http://localhost:3000/api/export/json" -O -J
```

---

## Network Access

### Accessing from Other Computers

The API is accessible from other computers on your local network.

**To access from another machine:**

1. Find the server's IP address:
   ```bash
   # Windows
   ipconfig

   # Linux/Mac
   ifconfig
   ```

2. Use the server's IP instead of `localhost`:
   ```bash
   curl http://192.168.1.100:3000/api/latest
   ```

### CORS Configuration

The API includes CORS headers allowing access from any origin:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

### Web Dashboard Access

The web dashboard is also accessible from other computers:
```
http://192.168.1.100:3000/
```

---

## Rate Limiting

**Scraper Rate Limiting:**
- 10-second delays between symbols
- 30-second delays after errors
- 2-second delays between RSS feeds

**API Rate Limiting:**
- No rate limiting implemented
- Recommend client-side throttling if making many requests

---

## Error Handling

All errors return consistent format:
```json
{
  "success": false,
  "error": "Descriptive error message"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `404` - Resource not found
- `500` - Server error

---

## Support

For issues, feature requests, or questions:
- Check the web dashboard at `http://localhost:3000/`
- Review the system status at `/api/status`
- Examine scrape history at `/api/history`

---

## Changelog

**v2.4.0 (November 2025)**
- Added RSS date filtering (today's articles only)
- Database-backed RSS/YouTube feed configuration
- Feed management via Settings UI

**v2.3.0 (November 2025)**
- Integrated RSS and YouTube scrapers into main workflow
- Added Phase 4 (RSS) and Phase 5 (YouTube) to scraper

**v2.0.0 (November 2025)**
- Initial unified system release
- Combined ETF, VIX, Max Pain, and Chat data
- Web dashboard with modern dark theme

---

**End of API Reference**
