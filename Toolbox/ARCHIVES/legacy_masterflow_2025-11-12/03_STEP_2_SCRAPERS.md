# STEP 2: RUN SCRAPERS - Collect Fresh Data

**Date:** 2025-11-01
**Purpose:** Scrape RSS, YouTube, X/Twitter, and Technical data in parallel

---

## WHAT IT DOES

Collects fresh market data from all sources:
- **X/Twitter**: Crypto list, Macro list, Technicals list, Bookmarks
- **YouTube**: Transcripts from 8+ channels
- **RSS**: MarketWatch, CNBC, Federal Reserve feeds
- **Technical Data**: SPY/QQQ options data, market breadth

---

## HOW TO RUN

**Command:**
```bash
python -u "c:\Users\Iccanui\Desktop\Investing\scripts\automation\run_all_scrapers.py"
```

**Important:** Use `-u` flag for **unbuffered output** (real-time display in terminal)

**Expected Duration:** 10-15 minutes

---

## VISIBLE TERMINAL WINDOW

**The script automatically opens a NEW PowerShell window** so you can watch progress.

**How it works:**
1. Script detects it's not running with `--visible` flag
2. Relaunches itself in a new PowerShell console window
3. New window shows real-time scraper output
4. Window stays open at end (press Enter to close)

**What you'll see:**
```
======================================================================
🚀 SCRAPER ORCHESTRATOR - PARALLEL MODE
======================================================================
Started: 2025-11-01 09:15:23
======================================================================

Execution order (OPTIMIZED - PARALLEL):
  PARALLEL (concurrent):
    • X/Twitter scraper (lists + bookmarks)
    • YouTube transcript scraper
    • RSS feed scraper
  SEQUENTIAL (after parallel completes):
    • X data archival
    • Options data scraper (SPY/QQQ)

Expected duration: 10-15 minutes
======================================================================

======================================================================
📡 PHASE 1: PARALLEL SCRAPERS (X + YouTube + RSS)
======================================================================
Launching 3 scrapers in parallel...

✅ RSS scraper completed successfully (2.3s)
✅ YouTube scraper completed successfully (8.7s)
✅ X/Twitter scraper completed successfully (9.2s)

======================================================================
📡 Running X Data Archival
======================================================================
...
```

---

## EXECUTION FLOW

### PHASE 1: PARALLEL (All 3 run simultaneously)

**1. X/Twitter Scraper** (~8-10 min)
- Lists: Crypto (400+ posts), Macro (200+ posts), Technicals (100+ posts)
- Bookmarks: Latest bookmarked posts
- Output: `Research/X/{Category}/x_list_posts_YYYYMMDD*.json`

**2. YouTube Transcript Scraper** (~3-5 min)
- 8+ channels processed
- Extracts video transcripts
- Output: `Research/YouTube/{Channel}/YYYY-MM-DD*.md`

**3. RSS Feed Scraper** (~1-2 min)
- MarketWatch (Top Stories, Business News)
- CNBC (News & Analysis, Investing)
- Federal Reserve (Press Releases)
- Output: `Research/RSS/{Provider}/YYYY-MM-DD*.md`

### PHASE 2: SEQUENTIAL (After Phase 1 completes)

**4. X Data Archival** (~30 sec)
- Converts day's tweets to daily archives
- Prepares data for analysis
- Output: `Research/X/{Category}/x_list_posts_YYYYMMDD_archived.json`

**5. Options Data Scraper** (~1 min)
- SPY/QQQ options data (max pain, P/C ratios, IV%)
- SPX/BTC technical levels
- Market breadth (A/D ratio)
- VIX data
- Output: `Research/.cache/YYYY-MM-DD_technical_data.json`

---

## OUTPUT LOCATIONS

```
Research/
├── RSS/
│   ├── MarketWatch/
│   │   └── YYYY-MM-DD_MarketWatch_*.md
│   ├── CNBC/
│   │   └── YYYY-MM-DD_CNBC_*.md
│   └── FederalReserve/
│       └── YYYY-MM-DD_FederalReserve_*.md
│
├── YouTube/
│   ├── {ChannelName}/
│   │   └── YYYY-MM-DD_{ChannelName}_*.md
│   └── (8+ channels)
│
├── X/
│   ├── Crypto/
│   │   ├── x_list_posts_YYYYMMDD*.json
│   │   └── x_list_posts_YYYYMMDD_archived.json
│   ├── Macro/
│   │   ├── x_list_posts_YYYYMMDD*.json
│   │   └── x_list_posts_YYYYMMDD_archived.json
│   ├── Technicals/
│   │   ├── x_list_posts_YYYYMMDD*.json
│   │   └── x_list_posts_YYYYMMDD_archived.json
│   └── Bookmarks/
│       └── x_bookmarks_posts_YYYYMMDD.json
│
└── .cache/
    ├── YYYY-MM-DD_technical_data.json
    ├── YYYY-MM-DD_market_data.json
    └── YYYY-MM-DD_options_data.json
```

---

## VERIFICATION

**After scrapers complete, verify:**

1. **Check terminal output:**
   - [ ] All scrapers show "✅ completed successfully"
   - [ ] No "❌ failed" messages
   - [ ] Final summary shows all succeeded

2. **Check files exist:**
   ```bash
   # Quick check for today's data
   ls Research/RSS/*/2025-11-01*.md
   ls Research/YouTube/*/2025-11-01*.md
   ls Research/X/*/x_list_posts_20251101*.json
   ls Research/.cache/2025-11-01_technical_data.json
   ```

3. **Expected file counts:**
   - RSS: 3+ articles (MarketWatch, CNBC, FedReserve)
   - YouTube: 8+ transcripts (one per channel)
   - X: 4 JSON files (Crypto, Macro, Technicals, Bookmarks)
   - Technical: 1 JSON file (technical_data)

---

## TROUBLESHOOTING

### Terminal window doesn't appear
**Problem:** Script runs but no visible window shows up

**Solution:**
- Make sure you're running from PowerShell or Command Prompt
- Check if window opened in background (alt-tab to find it)
- If still not visible, run with `--visible` flag manually:
  ```bash
  python run_all_scrapers.py --visible
  ```

---

### Scraper fails with "timeout"
**Problem:** Scraper takes >30 minutes and times out

**Causes:**
- Network connection issues
- Website blocking automated access
- Chrome/Selenium issues with X scraper

**Solution:**
- Check internet connection
- Restart and try again
- Check X scraper profile configuration

---

### Missing data files after completion
**Problem:** Some files not created even though scraper says success

**Check:**
1. Look for error messages in terminal (scroll up)
2. Check if provider websites are accessible
3. Verify scraper configuration files exist
4. Check disk space

**Solution:**
- Re-run just the failed scraper if possible
- Check logs for specific error messages

---

### X/Twitter scraper fails
**Problem:** X scraper times out or fails authentication

**Common causes:**
- Chrome profile path wrong
- Selenium/ChromeDriver version mismatch
- Twitter session expired

**Solution:**
- Check `Scraper/x_scraper.py` configuration
- Verify Chrome profile path
- May need to re-login to Twitter in Chrome

---

### YouTube scraper fails
**Problem:** YouTube transcripts not downloading

**Common causes:**
- Video has no transcript/captions
- Channel deleted/privated video
- API rate limit

**Solution:**
- Check which channel failed (terminal shows progress)
- Verify video URLs still accessible
- Skip problematic channels for now

---

## MONITORING FOR ERRORS

**What to watch in terminal:**

**✅ Good signs:**
```
✅ RSS scraper completed successfully (2.3s)
✅ YouTube scraper completed successfully (8.7s)
✅ X/Twitter scraper completed successfully (9.2s)
```

**❌ Bad signs:**
```
❌ X/Twitter scraper failed (exit code: 1)
⏱️  YouTube scraper timed out after 1800.0 seconds
```

**⚠️ Warning signs (may be OK):**
```
Warning: Could not fetch transcript for video XYZ
Skipping channel ABC (no new videos)
```

---

## WORKFLOW METADATA

**The scraper automatically updates workflow metadata** in `Journal/account_state.json`:

```json
{
  "last_workflow_run": "2025-11-01",
  "last_workflow_type": "recon",
  "last_workflow_status": "success",
  "last_workflow_timestamp": "2025-11-01T14:32:15Z",
  "data_freshness": "FRESH"
}
```

This metadata is used to track when data was last collected.

---

## WHEN COMPLETE

**Terminal will show:**
```
======================================================================
✅ ALL SCRAPERS COMPLETED
======================================================================
Total time: 12.4 minutes
Success: 5/5 scrapers
Data freshness: FRESH

Press Enter to close...
```

**Next step:** Tell Claude "scraper complete" to proceed to **STEP 3: Process Data**

---

## NEXT STEP

After scrapers complete successfully:
→ Say **"scraper complete"** to proceed to **STEP 3: Process & Update Master Plan**

---

**Status:** Documented
**Script Location:** `scripts/automation/run_all_scrapers.py`
**Duration:** 10-15 minutes (parallel execution)
**Last Updated:** 2025-11-01
