# Scout Market Intelligence System - Complete Workflow

**Date:** 2025-11-11
**System:** Scout (Unified market intelligence)
**Duration:** ~15-20 minutes (data collection) + ~40 minutes (AI processing)

---

## OVERVIEW

Scout is a unified market intelligence system with **single entry point** execution.

**What it does:**
1. **Cleanup** - Remove stale cache files (~30 seconds)
2. **Collect** - Gather data from all sources (~5-10 minutes)
3. **Process** - AI analysis and dashboard generation (~40 minutes - MANUAL)

**Simplified Architecture:**
- Single command: `python scout/scout.py`
- No external orchestrators
- Direct scraper integration
- Graceful error handling

**Output Files:**
- `scout/dash.md` - Market intelligence markdown
- `scout/dash.html` - Interactive dashboard (320KB self-contained)

---

## QUICK START

### For Users

**Run complete data collection:**
```bash
python scout/scout.py
```

That's it! Scout will:
1. Clean old cache files
2. Collect X/Twitter data (local scraper)
3. Collect YouTube/RSS/Market data (API server)
4. Pause for manual AI processing step

### For Claude AI

When user says **"run Scout"** or **"collect data"**, execute:

```bash
python scout/scout.py
```

**Do not use run_in_background** - Scout shows real-time progress.

**After collection completes:**
- Inform user that data collection is complete
- Remind user that Step 3 (AI processing) is manual
- Wait for user to request AI analysis

---

## SYSTEM ARCHITECTURE

### Data Sources

| Source | Method | Location | Time |
|--------|--------|----------|------|
| X/Twitter | Local scraper | `Scraper/x_scraper.py` | 3-5 min |
| Market Data | API server | 192.168.10.56:3000 | Instant |
| YouTube | API server | 192.168.10.56:3000 | Instant |
| RSS News | API server | 192.168.10.56:3000 | Instant |

### Directory Structure

```
scout/
├── scout.py              # ⭐ Main entry point
├── dash.md               # Output: Market analysis
├── dash.html             # Output: Interactive dashboard
├── config.py             # Configuration
├── README.md             # Quick start guide
└── SCOUT_SYSTEM_SUMMARY.md  # Complete documentation

Research/
├── X/                    # X/Twitter posts (local scraper)
│   ├── Technicals/
│   ├── Crypto/
│   ├── Macro/
│   └── Bookmarks/
└── .cache/               # Technical data cache

Scraper/
├── x_scraper.py          # ⭐ X/Twitter scraper (optimized)
├── youtube_scraper.py    # Legacy (use API)
└── rss_scraper.py        # Legacy (use API)

scripts/trading/
└── api_client.py         # ⭐ API server client

config.py                 # System configuration
```

---

## WORKFLOW STEPS

### Step 1: Cleanup (~30 seconds)

**Purpose:** Remove stale cache files while preserving important data

**Executed by:** `scout/scout.py` → `Toolbox/scripts/cleanup/scout_cleanup.py`

**What it does:**
- Removes category overviews older than 1 day
- Removes cached files older than 1 day
- Preserves signal history files
- Shows deletion summary

**Output:**
```
======================================================================
[1/5] CLEANUP
======================================================================
Removing stale cache files...
  paths_removed=4
  total_reclaimed=2.1 MB
[OK] Cleanup complete
```

**Time:** 30 seconds

---

### Step 2: Data Collection (~5-10 minutes)

**Purpose:** Collect fresh data from all sources

**Executed by:** `scout/scout.py` (direct integration)

#### Phase 2A: X/Twitter Collection (3-5 minutes)

**Method:** Local Selenium scraper

**Requirements:**
- Chrome browser with logged-in X/Twitter profile
- Chrome profile path: `C:\Users\Iccanui\AppData\Local\Google\Chrome\User Data`
- Debug port 9222 available

**Lists scraped:**
- Technicals
- Crypto
- Macro
- Bookmarks

**Output files:**
```
Research/X/Technicals/x_list_posts_YYYYMMDDHHMMSS.json
Research/X/Crypto/x_list_posts_YYYYMMDDHHMMSS.json
Research/X/Macro/x_list_posts_YYYYMMDDHHMMSS.json
Research/X/Bookmarks/x_list_posts_YYYYMMDDHHMMSS.json
```

**Optimizations applied:**
- X_MAX_NO_NEW: 10 (was 30 - 66% faster)
- X_WAIT_TIMEOUT: 2 sec (was 4 - 50% faster)
- stale_timeout: 180 sec (was 300 - 40% faster)

**Expected results:** 400-600 posts in 3-5 minutes

**Progress shown:** Real-time console output
- List name being scraped
- Scroll count
- New posts found
- Completion status

#### Phase 2B: API Data Collection (Instant)

**Method:** API server at 192.168.10.56:3000

**Endpoints:**
- `/api/summary` - Market data (SPY, QQQ, VIX, Max Pain)
- `/api/youtube/latest` - YouTube transcripts with Ollama summaries
- `/api/rss/latest` - RSS news articles

**Requirements:**
- API server must be online
- Network connectivity to 192.168.10.56

**Health check performed automatically:**
```
[2-4/4] API Server Collection
----------------------------------------------------------------------
[OK] API server online
  ✅ Market data: 3 ETFs, 35 max pain records
  ✅ YouTube: 22 videos
  ✅ RSS News: 50 articles

[OK] API collection complete - 3/3 sources
```

**Graceful degradation:**
- If API offline, Scout continues with X data only
- Partial failure still allows workflow to proceed

#### Collection Summary

**After collection completes:**
```
======================================================================
COLLECTION SUMMARY
======================================================================
Success: 2/2 sources
  ✅ X Twitter: success
  ✅ Api Data: success

Verifying collected data...
  ✅ X/Twitter: 4 files
  ✅ Technical Data: Found
```

**Time:** 5-10 minutes total (3-5 min X scraper + instant API)

---

### Step 3: AI Processing (~40 minutes - MANUAL)

**Purpose:** Analyze collected data and generate insights

**Status:** MANUAL STEP REQUIRED

**Why manual?**
- Requires deep analysis and synthesis
- AI needs to read and understand all data sources
- Generate contextual insights and signal calculations
- Update dash.md with comprehensive analysis

**Scout pauses here:**
```
======================================================================
[3/5] AI PROCESSING
======================================================================

⚠️  MANUAL STEP REQUIRED:
The AI processing phase requires manual execution through Claude.

Data has been collected and is ready for analysis in:
  - Research/X/
  - Research/.cache/YYYY-MM-DD_technical_data.json
  - API server data (YouTube/RSS via API)

Next steps:
  1. Review collected data
  2. Run Step 3 analysis (see Toolbox/MasterFlow/05_STEP_3_PROCESS_DATA.md)
  3. Generate dash.md output

Scout collector phase complete!
```

**Documentation:** See [05_STEP_3_PROCESS_DATA.md](05_STEP_3_PROCESS_DATA.md)

**AI Analysis Components:**
1. RSS Analysis - Market themes and sentiment
2. YouTube Analysis - Analyst insights and consensus
3. Technical Analysis - Key levels and signals
4. X/Twitter Analysis - Sentiment and trending tickers
5. Cross-Source Synthesis - Pattern identification
6. Signal Calculation - Weighted score (0-100)
7. Dashboard Update - Generate dash.md

**Time:** ~40 minutes

---

## CONFIGURATION

### API Server (config.py)

```python
config.api.base_url = "http://192.168.10.56:3000"
config.api.timeout = 30
config.api.retry_attempts = 3
```

### X Scraper (Scraper/x_scraper.py)

```python
# Performance tuning
X_MAX_NO_NEW = 10          # Stop after 10 consecutive no-new sweeps
X_WAIT_TIMEOUT = 2         # Wait 2 seconds after scroll
X_STALE_TIMEOUT = 180      # Exit if no new posts for 3 minutes

# Chrome settings
CHROME_PROFILE_PATH = "C:\\Users\\Iccanui\\AppData\\Local\\Google\\Chrome\\User Data"
CHROME_DEBUG_PORT = 9222
```

**Lists to scrape:**
```python
X_LISTS = [
    ("Technicals", "https://x.com/i/lists/..."),
    ("Crypto", "https://x.com/i/lists/..."),
    ("Macro", "https://x.com/i/lists/..."),
    ("Bookmarks", "https://x.com/i/bookmarks"),
]
```

---

## ERROR HANDLING

### Graceful Degradation

Scout continues even if individual sources fail:

**If X scraper fails:**
- API data still collected
- Workflow continues
- Partial success reported

**If API server offline:**
- X scraper still runs
- Local data collected
- Partial success reported

**Collection success criteria:**
- 2/2 sources = Success
- 1/2 sources = Partial (continues)
- 0/2 sources = Failed (stops)

### Common Issues

#### X Scraper Timeout
**Symptom:** Scraper appears stuck, no new posts
**Cause:** Network slow, X/Twitter loading issues
**Solution:** Optimized timeout parameters (already applied)
- If still happens: Check internet connection
- Restart Chrome and try again

#### API Server Offline
**Symptom:** "API server offline" message
**Cause:** Server at 192.168.10.56:3000 not responding
**Solution:**
1. Check server is running
2. Verify network connectivity: `curl http://192.168.10.56:3000/api/summary`
3. Restart API server if needed
4. Scout will still collect X data

#### Chrome Profile Not Found
**Symptom:** X scraper can't connect to Chrome
**Cause:** Chrome not running or profile path incorrect
**Solution:**
1. Close all Chrome windows
2. Verify profile path in config.py
3. Check debug port 9222 is available
4. Restart Scout

---

## VERIFICATION

### After Data Collection

**Check collected files:**
```bash
# X/Twitter posts (should have 4 files for today)
ls Research/X/*/x_list_posts_*.json

# API data (check server responded)
curl http://192.168.10.56:3000/api/summary

# Technical data cached
ls Research/.cache/*_technical_data.json
```

**Expected results:**
- 4 X/Twitter JSON files (one per list)
- API server responds with market data
- Technical data cache file exists

### After Complete Workflow (with Step 3)

**Check output files:**
```bash
# Dashboard markdown (should have today's date)
grep "Date:" scout/dash.md

# Dashboard HTML (should be 320KB+)
ls -lh scout/dash.html
```

**Verification checklist:**
- [ ] X scraper collected 400+ posts
- [ ] API server provided market/YouTube/RSS data
- [ ] No critical errors in output
- [ ] dash.md updated with today's analysis
- [ ] dash.html opens in browser successfully

---

## COMPARISON: Old vs New

### Entry Points

**Old System (Archived):**
```bash
python scripts/automation/run_workflow.py YYYY-MM-DD
python scripts/automation/scout_update.py YYYY-MM-DD
python scripts/automation/run_recon.py
python scripts/automation/run_all_scrapers.py
```
- Multiple scripts, unclear which to use
- Date parameter required
- Complex orchestration

**New System (Scout):**
```bash
python scout/scout.py
```
- Single entry point
- No parameters needed
- Automatic date handling

### Workflow Complexity

**Old System:**
- 10+ orchestrator scripts
- 50+ sync scripts
- ~10,000 lines of code
- Complex error recovery

**New System:**
- 1 main script (289 lines)
- Direct scraper integration
- ~500 lines of code total
- Simple error handling

### Output Files

**Old System:**
```
Research/.cache/YYYY-MM-DD_dash-prep.md
Research/.cache/dashboard.json
```

**New System:**
```
scout/dash.md
scout/dash.html
```

**Simplified:** Removed dashboard.json (data embedded in HTML)

---

## TROUBLESHOOTING

### "Cleanup script not found"
**Symptom:** [WARN] Cleanup script not found, skipping...
**Cause:** scout_cleanup.py missing
**Impact:** Low - cleanup skipped, old files remain
**Solution:** Restore from `Toolbox/BACKUPS/` or ignore if not critical

### "X scraper not found"
**Symptom:** [SKIP] X scraper not found
**Cause:** Scraper/x_scraper.py missing or moved
**Impact:** High - X data not collected
**Solution:** Restore x_scraper.py from backup

### "API collection failed"
**Symptom:** [ERROR] API collection failed
**Cause:** Server offline or network issue
**Impact:** Medium - YouTube/RSS/Market data not collected
**Solution:**
1. Check server: `curl http://192.168.10.56:3000/api/summary`
2. Verify network connectivity
3. Restart API server if needed

### Session Crashes During Step 3
**Symptom:** AI processing interrupted
**Cause:** Context window limit, memory issue
**Impact:** Medium - need to resume analysis
**Solution:**
1. Check which data sources were analyzed
2. Resume from last completed section
3. See Step 3 documentation for recovery

---

## BACKUPS AND ROLLBACK

### Archives

**Legacy system preserved:** `Toolbox/ARCHIVES/legacy_2025-11-11/`
- All old scripts intact
- Can restore if needed
- See ARCHIVE_README.md for details

**Scraper test files:** `Toolbox/ARCHIVES/scraper_test_files_2025-11-11/`
- Debug and test scripts
- Safe to delete after verification

### Pre-Scout Backups

**Original files:** `Toolbox/BACKUPS/`
- dash-prep_2025-11-11_pre-scout.md
- research-dashboard_2025-11-11_pre-scout.html
- dashboard_2025-11-11_pre-scout.json

### Rollback Procedure

**If Scout system fails:**
```bash
# Restore old system from archive
cp -r Toolbox/ARCHIVES/legacy_2025-11-11/automation_scripts scripts/automation

# Restore old output files
cp Toolbox/BACKUPS/dash-prep_2025-11-11_pre-scout.md scout/dash.md
cp Toolbox/BACKUPS/research-dashboard_2025-11-11_pre-scout.html scout/dash.html

# Old workflow command
python scripts/automation/run_workflow.py 2025-11-11
```

**Nothing was deleted** - Complete rollback capability maintained

---

## TIMING BREAKDOWN

| Phase | Duration | Details |
|-------|----------|---------|
| Cleanup | 30 sec | Remove stale cache files |
| X Scraper | 3-5 min | Optimized collection (4 lists) |
| API Collection | Instant | Market/YouTube/RSS data |
| **Data Collection Total** | **5-10 min** | **Fully automated** |
| AI Processing (Manual) | 40 min | Analysis and insights generation |
| **Complete Workflow** | **50-60 min** | **Including AI processing** |

---

## DOCUMENTATION

### Scout System
- `scout/README.md` - Quick start guide
- `scout/SCOUT_SYSTEM_SUMMARY.md` - Complete documentation
- `DATA_SOURCES_AUDIT.md` - Data source verification
- `PROJECT_STRUCTURE.md` - Directory layout

### Workflow Guides
- `00_SCOUT_WORKFLOW.md` - This document
- `01_SYSTEM_OUTPUTS.md` - Output file specifications
- `02_STEP_1_CLEANUP.md` - Cleanup details
- `03_STEP_2_SCRAPERS.md` - Scraper documentation
- `05_STEP_3_PROCESS_DATA.md` - AI processing guide

### Session Logs
- `Toolbox/CHANGELOGS/SCOUT_SESSION_5_HANDOFF_2025-11-11.md` - Latest session
- Previous changelogs in CHANGELOGS/ directory

---

## QUICK REFERENCE

### Daily Usage
```bash
# Run complete data collection
python scout/scout.py

# Check API server health
curl http://192.168.10.56:3000/api/summary

# Verify collected data
ls Research/X/*/x_list_posts_*.json

# Open dashboard
start scout/dash.html
```

### Troubleshooting
```bash
# Check Scout configuration
cat config.py | grep api

# Test X scraper manually
python Scraper/x_scraper.py

# View API client code
cat scripts/trading/api_client.py
```

### Archives
```bash
# View archived legacy system
ls Toolbox/ARCHIVES/legacy_2025-11-11/

# View scraper test files
ls Toolbox/ARCHIVES/scraper_test_files_2025-11-11/

# View backups
ls Toolbox/BACKUPS/
```

---

## SUCCESS METRICS

**Scout is successful when:**
- ✅ Single command execution: `python scout/scout.py`
- ✅ Data collection completes in 5-10 minutes
- ✅ All 4 data sources collected (X, Market, YouTube, RSS)
- ✅ Graceful handling of partial failures
- ✅ Real-time progress visibility
- ✅ No manual orchestration required
- ✅ 95% code reduction from legacy system
- ✅ Maintainable codebase (~500 lines total)

**Current Status:** ✅ All metrics achieved (as of 2025-11-11)

---

**Last Updated:** 2025-11-11
**System Version:** Scout 1.0
**Status:** Production Ready (data collection phase)
**Next:** Complete Step 3 AI processing integration
