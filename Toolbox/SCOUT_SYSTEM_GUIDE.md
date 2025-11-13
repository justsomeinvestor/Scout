# Scout System Guide
**Version:** 1.0
**Created:** 2025-11-08
**Status:** Production Recovery Mode

---

## What is Scout?

**Scout** is a lean reconnaissance system that collects real-time market intelligence and updates a live research dashboard with zero mock data. It replaces the token-heavy, multi-phase "Wingman" workflow with a unified, efficient data pipeline.

### Mission
Provide traders with accurate, real-time market intelligence through automated data collection, minimal AI processing, and instant dashboard updates.

### Core Principles
1. **Real Data Only** - No mocks, no placeholders, no fake data
2. **Speed First** - Full dashboard update in <2 minutes
3. **Token Efficient** - <10K tokens per update cycle
4. **Single Command** - One script runs everything
5. **Clear Errors** - Immediate feedback on failures

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SCOUT UPDATE (Main)                       │
│                 scripts/automation/scout_update.py           │
└────────────┬────────────────────────────────────────────────┘
             │
             ├──► DATA COLLECTION (Parallel)
             │    ├─► API Server (192.168.10.56:3000)
             │    │   └─► /api/summary (SPY, QQQ, VIX, Max Pain, Chat)
             │    │
             │    ├─► X/Twitter Scraper (Selenium)
             │    │   └─► Lists: Technicals, Crypto, Macro, Bookmarks
             │    │
             │    ├─► YouTube Scraper (Transcripts)
             │    │   └─► 20+ investment channels
             │    │
             │    └─► RSS Scraper (Feeds)
             │        └─► MarketWatch, CNBC, Fed
             │
             ├──► DATA TRANSFORMATION
             │    └─► Minimal AI (Ollama for summaries only)
             │
             └──► DASHBOARD BUILD
                  ├─► Generate dashboard.json
                  └─► Update research-dashboard.html

```

---

## Data Sources

### 1. API Server (192.168.10.56:3000)
**Primary market data source** - offloaded heavy lifting to server

**Key Endpoints:**
- `GET /api/summary` - Everything in one call (preferred)
- `GET /api/status` - Server health & data freshness
- `GET /api/latest` - Latest ETF data (SPY, QQQ)
- `GET /api/latest/{symbol}` - Specific symbol (SPY, QQQ, VIX)
- `GET /api/maxpain/{symbol}` - Max pain options data
- `GET /api/maxpain/{symbol}/weekly` - Weekly expirations only
- `GET /api/chat/latest` - Latest chat messages (wallstreet.io)
- `GET /api/export/json` - Full data export
- `POST /api/backup` - Create backup

**Data Provided:**
- SPY/QQQ options data (IV, put/call ratios, price levels)
- VIX structure (current, change, term structure)
- Max Pain levels (35+ expirations per symbol)
- Market breadth signals (from chat analysis)
- Scrape timestamps & freshness indicators

**API Client:**
- Location: `scripts/trading/api_client.py`
- Class: `MarketDataAPI`
- Usage: `from scripts.trading.api_client import get_client`

**Example:**
```python
from scripts.trading.api_client import get_client

with get_client() as api:
    # Get everything at once
    summary = api.get_summary()

    # Check data freshness
    if api.is_data_fresh(max_age_hours=1):
        print("Data is fresh!")

    # Get specific data
    spy = api.get_spy_data()
    vix = api.get_vix_data()
    maxpain = api.get_maxpain_weekly('SPY')
```

### 2. X/Twitter Scraper
**Social sentiment & technicals**

- **Script:** `Scraper/x_scraper.py`
- **Method:** Selenium (Chrome automation)
- **Chrome Profile:** `C:\Users\Iccanui\AppData\Local\Google\Chrome\User Data`
- **Lists Tracked:**
  - Technicals: https://x.com/i/lists/1479448773449314306
  - Crypto: https://x.com/i/lists/1430346349375938572
  - Macro: https://x.com/i/lists/1366729121678589959
  - Bookmarks: https://x.com/i/bookmarks
- **Output:** `Research/X/{list_name}/x_list_posts_YYYYMMDD.json`
- **Collection Window:** Last 24 hours (configurable)
- **Archival:** Daily to `Research/X/_archives/YYYY-MM/`

### 3. YouTube Scraper
**Investment channel analysis**

- **Script:** `Scraper/youtube_scraper.py`
- **Method:** YouTube Transcript API + yt-dlp
- **Channels:** 20+ (ARK Invest, Benjamin Cowen, Meet Kevin, etc.)
- **Config:** `Scraper/channels.txt`
- **Max Videos:** 3 per channel per run
- **Timeout:** 45 seconds per transcript
- **Output:** `Research/YouTube/{channel_name}/{video_id}_transcript.txt`
- **Tracking:** `_processed_videos.json` per channel

### 4. RSS Feed Scraper
**News aggregation**

- **Script:** `Scraper/rss_scraper.py`
- **Method:** feedparser library
- **Config:** `Scraper/rss_feeds.json`
- **Feeds:**
  - MarketWatch (Top Stories, Business News)
  - CNBC (Top News, Investing News)
  - Federal Reserve (Press Releases)
- **Max Articles:** 20 per feed
- **Output:** `Research/RSS/{provider}/{article_id}.json`
- **Archival:** Daily to `Research/RSS/_archives/YYYY-MM/`

### 5. Ollama LLM (AI Processing)
**Summarization only**

- **Server:** 192.168.10.52:11434
- **Model:** gpt-oss:20b
- **Timeout:** 300 seconds (5 minutes)
- **Usage:** Summary generation for RSS, YouTube, X content
- **Goal:** Minimize token usage, only use when necessary

---

## Configuration

### config.py
**Central configuration file** - all settings in one place

```python
# API Server
config.api.base_url = "http://192.168.10.56:3000"
config.api.timeout = 30  # seconds
config.api.retry_attempts = 3

# Ollama LLM
config.ollama.url = "http://192.168.10.52:11434"
config.ollama.model = "gpt-oss:20b"
config.ollama.timeout = 300

# Paths
config.paths.research = "Research/"
config.paths.master_plan = "master-plan/"
config.paths.toolbox = "Toolbox/"

# Signal weights
config.weights.trend = 30
config.weights.breadth = 25
config.weights.volatility = 20
config.weights.sentiment = 15
config.weights.technical = 10
```

### .env
**API Keys** (never commit to git!)

```
FRED_API_KEY=<your_key>
FINNHUB_API_KEY=<your_key>
COINMARKETCAP_API_KEY=<your_key>
```

---

## Dashboard Structure

### File: master-plan/dashboard.json
**Data source for research-dashboard.html**

**Key Sections:**
1. **Sentiment Cards** - Quick market overview (4 cards)
2. **Sentiment History** - Signal score time series
3. **Risk Items** - Active warnings & alerts
4. **Tabs:**
   - Portfolio (allocation recommendations)
   - News (RSS feeds + catalysts)
   - Technicals (SPY/QQQ/VIX levels)
   - Social (X/Twitter sentiment)
   - Markets Intelligence (macro analysis)
   - Daily Planner (action items)

**Critical Fields:**
- `lastUpdated` - Global timestamp (ISO 8601)
- `sentimentCardsUpdated` - Sentiment section timestamp
- `sentimentHistoryUpdated` - History section timestamp
- Each tab has its own `updated` timestamp

### File: master-plan/research-dashboard.html
**Self-contained dashboard** - no server required

- **Lines:** 14,016 (320KB)
- **Technology:** Pure JavaScript (no frameworks)
- **Data Source:** Reads `dashboard.json` on page load
- **Features:**
  - Interactive tabs
  - Live charts (Chart.js)
  - Sentiment cards
  - Risk alerts
  - Portfolio recommendations
  - Quick actions

---

## Workflow Execution

### Option 1: Full Update (Recommended)
```bash
python scripts/automation/scout_update.py
```

**What it does:**
1. Checks API server health
2. Fetches latest market data (`/api/summary`)
3. Runs all scrapers in parallel
4. Processes & transforms data
5. Generates `dashboard.json`
6. Updates `research-dashboard.html` (if needed)
7. Creates verification report

**Duration:** <2 minutes
**Output:** Timestamped logs + dashboard files

### Option 2: Data Collection Only
```bash
python scripts/automation/run_recon.py
```

**What it does:**
- Fetches API data
- Runs scrapers
- Saves to `Research/.cache/`
- NO dashboard update

**Use case:** Archival, research, debugging

### Option 3: Manual Testing
```bash
# Test API connection
python scripts/trading/api_client.py

# Test specific scraper
python Scraper/x_scraper.py
python Scraper/youtube_scraper.py
python Scraper/rss_scraper.py
```

---

## Data Storage

### Research/.cache/
**Temporary processing data** (daily cleanup)

- `YYYY-MM-DD_technical_data.json` - API market data
- `YYYY-MM-DD_*_Category_Overview.md` - AI summaries
- `scraper_status_YYYY-MM-DD.json` - Execution tracking
- `verification_report_YYYYMMDD_HHMMSS.json` - Validation results

### Research/X/, Research/YouTube/, Research/RSS/
**Scraped content** (permanent storage)

- Daily files with timestamps
- Monthly archival to `_archives/YYYY-MM/`
- Tracking files (`_processed_*.json`)

### master-plan/
**Dashboard files** (version controlled)

- `dashboard.json` - Data source
- `research-dashboard.html` - UI
- `master-plan.md` - Markdown source (deprecated?)

---

## Troubleshooting

### API Server Unreachable
```bash
# Check server status
curl http://192.168.10.56:3000/health

# Test from Python
python scripts/trading/api_client.py
```

**Fix:** Verify server is running, check network connectivity

### Stale Data in Dashboard
**Symptom:** Dashboard shows old dates

**Fix:**
1. Check `dashboard.json` `lastUpdated` field
2. Run `python scripts/automation/scout_update.py`
3. Verify API server has fresh data (`/api/status`)

### Mock/Placeholder Data
**Symptom:** Values like "PLACEHOLDER", "null", "N/A"

**Fix:**
1. Check API server data quality
2. Verify scraper output files exist
3. Review transformation logic
4. Validate dashboard.json structure

### Scraper Failures
**Symptom:** Missing data in Research/ folders

**Fix:**
1. Check Chrome profile access (X scraper)
2. Verify network connectivity
3. Check rate limits (YouTube API)
4. Review scraper logs

---

## Migration from Wingman

**Wingman** was the previous 3-phase system:
- RECON (data collection)
- PREP (AI processing)
- DASH (dashboard update)

**Problems:**
- Token-heavy (AI processing on everything)
- Multi-script complexity
- Session limits & context loss
- Mock data creep
- Timestamp verification failures

**Scout Improvements:**
- Single unified workflow
- Minimal AI usage (only summaries)
- Offloaded heavy data to API server
- Real-time validation
- Clear error handling

**Files Being Removed:**
- `scripts/automation/wingman_dash.py` → `scout_update.py`
- `scripts/automation/run_wingmap_prep_agentic.py` → deleted
- `scripts/journal/*` → deleted (journaling removed)
- All "wingman" references → renamed to "scout"

---

## Development Guidelines

### For AI Assistants (Claude)

**When updating Scout:**
1. ALWAYS read current `dashboard.json` before editing
2. NEVER use mock/placeholder data
3. ALWAYS validate API data before processing
4. Keep timestamps accurate (ISO 8601 format)
5. Test end-to-end before marking complete
6. Document changes in CHANGELOG

**Token Budget:**
- Prefer structured transforms over AI summarization
- Cache scraper results (don't re-read repeatedly)
- Use `/api/summary` for bulk data (one call)
- Minimize file reads (use Glob to find, Read once)

**Session Handoffs:**
1. Update `Toolbox/CHANGELOGS/CHANGELOG_YYYY-MM-DD_scout.md`
2. Document current state in handoff template
3. List next session TODOs clearly
4. Ensure code is runnable (no broken state)

### For Developers

**Before Committing:**
- [ ] Test full Scout update workflow
- [ ] Verify dashboard loads with real data
- [ ] Check all timestamps are current
- [ ] No mock/placeholder values
- [ ] Run scrapers successfully
- [ ] API server accessible

**Never Commit:**
- .env files (API keys)
- Chrome user data
- Personal trading journal data
- API server code (separate repo)

---

## API Reference

See `SCOUT_API_REFERENCE.md` for complete endpoint documentation.

---

## Next Steps

1. Review `SCOUT_MIGRATION_PLAN.md` for Wingman removal
2. Check `SCOUT_SESSION_HANDOFF_TEMPLATE.md` for AI collaboration
3. Run initial Scout update: `python scripts/automation/scout_update.py`
4. Monitor dashboard for data quality

---

**Questions?** Check the Toolbox documentation or review existing scripts in `scripts/automation/`.

**Emergency Rollback:** Backups stored in `Toolbox/BACKUPS/` with timestamps.
