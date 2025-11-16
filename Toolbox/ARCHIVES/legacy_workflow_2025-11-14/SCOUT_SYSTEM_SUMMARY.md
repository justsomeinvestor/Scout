# ⚠️ DEPRECATED - Archived 2025-11-14

**This document is archived for reference only.**

**Current workflow:** See `Toolbox/MasterFlow/SCOUT_AI_WORKFLOW.md` (active AI processing workflow)

---

# Scout System - Complete Summary

**Date:** 2025-11-11
**Version:** 1.0
**Status:** Production Ready (Archived)

---

## What is Scout?

**Scout is a unified market intelligence system with a single command execution.**

```bash
cd scout/
python scout.py
```

**Philosophy:** "One Command. One Workflow. One Dashboard."

---

## System Architecture

```
SCOUT WORKFLOW
==============

1. CLEANUP (30 sec)
   └─> Remove stale cache files

2. COLLECT DATA (10-15 min)
   ├─> X/Twitter (local scraper)
   ├─> YouTube (API: 192.168.10.56:3000)
   ├─> RSS (API: 192.168.10.56:3000)
   └─> Market Data (API: 192.168.10.56:3000)

3. PROCESS (40 min - manual AI step)
   ├─> Read all collected data
   ├─> Synthesize insights
   ├─> Calculate signal scores
   └─> Generate analysis

4. OUTPUT
   ├─> dash.md (market intelligence)
   └─> dash.html (web dashboard)

5. VIEW
   └─> Open dashboard in browser
```

---

## Data Sources

### Primary Sources (Working)

**1. X/Twitter (Local Scraper)**
- Location: `Scraper/x_scraper.py`
- Lists: Technicals, Crypto, Macro, Bookmarks
- Output: `Research/X/{list_name}/x_list_posts_YYYYMMDDHHMMSS.json`
- Requirement: Chrome browser with logged-in profile
- Method: Selenium automation

**2. YouTube (API Server)**
- Endpoint: `http://192.168.10.56:3000/api/youtube/latest`
- Channels: 20+ investment analysts
- Features: Transcript + Ollama summaries
- Output: Retrieved via API (not stored locally)

**3. RSS (API Server)**
- Endpoint: `http://192.168.10.56:3000/api/rss/latest`
- Providers: MarketWatch, CNBC, Federal Reserve
- Output: Retrieved via API (not stored locally)

**4. Market Data (API Server)**
- Endpoint: `http://192.168.10.56:3000/api/summary`
- Data: SPY/QQQ/VIX, max pain, chat messages
- Freshness: Real-time updates
- Output: Retrieved via API (not stored locally)

### Optional Dependencies

- **Ollama** (http://192.168.10.52:11434)
  - Used for: YouTube transcript summarization on API server
  - Status: Optional (API server handles this)

- **API Server** (http://192.168.10.56:3000)
  - Status: Required for YouTube/RSS/Market data
  - Fallback: Scout continues with X data only if offline

---

## File Structure

```
scout/
├── scout.py                  # Master orchestrator (200 lines)
├── config.py                 # System configuration
├── collectors/
│   ├── core.py               # Parallel data collection
│   └── __init__.py           # Module exports
├── dash.md                   # Market intelligence output
├── dash.html                 # Web dashboard
├── README.md                 # Quick start guide
└── SCOUT_SYSTEM_SUMMARY.md   # This file
```

---

## Key Features

### 1. Single Entry Point
- One command runs everything
- No confusion about which script to use
- Clear progress reporting

### 2. Graceful Degradation
- API server offline? → Continue with X data
- X scraper fails? → Continue with API data
- No fatal errors that block workflow

### 3. Crash Recovery
- Checkpoint system in AI processing phase
- Can resume from any step
- No data loss on interruption

### 4. Fast Execution
- Parallel data collection
- Optimized scraper logic
- Target: <60 minutes total

### 5. Clean Output
- dash.md: Structured markdown intelligence
- dash.html: Interactive web dashboard
- Clear timestamps and freshness indicators

---

## Workflow Commands

### Complete Workflow (Recommended)
```bash
cd scout/
python scout.py
```

### Individual Phases (Advanced)

**Cleanup Only:**
```bash
python Toolbox/scripts/cleanup/scout_cleanup.py
```

**Data Collection Only:**
```bash
python scripts/automation/run_all_scrapers.py
```

**View Dashboard:**
```bash
# Direct open
open scout/dash.html  # macOS
start scout/dash.html # Windows

# Or serve locally
cd scout/
python -m http.server 9000
# Open http://localhost:9000/dash.html
```

---

## Output Files

### dash.md
**Purpose:** Structured market intelligence in markdown format

**Sections:**
1. Eagle Eye Macro Overview
2. Market Sentiment Alignment
3. Current Signal Status
4. Key Risks to Track
5. Tactical Playbook

**Updated:** After Step 3 (AI processing)
**Format:** Clean markdown with tables and lists

### dash.html
**Purpose:** Interactive web dashboard

**Features:**
- Sentiment cards (Equities, Crypto, Liquidity, Macro)
- Sentiment history timeline
- Multiple tabs (Portfolio, Markets, News, Social, Technicals)
- Real-time data display
- No server required (self-contained)

**Updated:** After Step 3 (AI processing)
**Size:** ~320KB (includes embedded JavaScript)

---

## Configuration

### API Server
```python
config.api.base_url = "http://192.168.10.56:3000"
config.api.timeout = 30  # seconds
config.api.retry_attempts = 3
```

### Ollama (Optional)
```python
config.ollama.url = "http://192.168.10.52:11434"
config.ollama.model = "gpt-oss:20b"
config.ollama.timeout = 300  # seconds
```

### Paths
```python
config.paths.research = "Research/"
config.paths.cache = "Research/.cache/"
config.paths.x_dir = "Research/X/"
```

See `scout/config.py` for complete configuration.

---

## Requirements

**Python:**
- Version: 3.8+
- Dependencies: See `requirements.txt`

**External Services:**
- API Server (192.168.10.56:3000) - for YouTube/RSS/Market data
- Chrome Browser - for X scraper
- Ollama (optional) - handled by API server

**System:**
- Windows/macOS/Linux compatible
- Internet connection required
- ~500MB disk space for data storage

---

## Troubleshooting

### Scout won't run
**Check:**
1. In correct directory? (`cd scout/`)
2. Python 3.8+ installed? (`python --version`)
3. Dependencies installed? (`pip install -r ../requirements.txt`)

### API server unreachable
**Symptoms:** YouTube/RSS/Market data missing
**Fix:**
1. Check server running: `curl http://192.168.10.56:3000/health`
2. Check network connectivity
3. Scout continues with X data only

### X scraper fails
**Symptoms:** No X data collected
**Fix:**
1. Chrome browser installed?
2. Logged into Twitter/X in Chrome?
3. Profile path correct in config?
4. Try running manually: `python Scraper/x_scraper.py`

### Dashboard doesn't open
**Fix:**
1. dash.html exists? (`ls scout/dash.html`)
2. Try opening manually in browser
3. Check browser console for errors

### Data looks stale
**Check:**
1. Last updated timestamp in dash.html
2. Files in `Research/` have today's date?
3. Re-run scout.py to refresh

---

## Performance Metrics

**Target Times:**
- Cleanup: 30 seconds
- Data Collection: 10-15 minutes
- AI Processing: 40 minutes (manual)
- Total: <60 minutes

**Data Size:**
- X posts: ~400KB per run
- Technical data: ~50KB per run
- Total storage: ~500MB over time

**Code Reduction:**
- Before: ~10,000+ lines across 117 files
- After: ~500 lines in scout/ (95% reduction)

---

## System Overview

### Architecture

**Scout System:**
- Single entry point (scout.py)
- Unified workflow (Cleanup → Collect → Process → Output)
- Integrated processing
- Consolidated docs in scout/ and Toolbox/MasterFlow/
- 5 core folders

### Archived Components

**Location:** `Toolbox/ARCHIVES/legacy_2025-11-11/`

**Archived:**
- automation_scripts/ (scripts/automation/)
- processing_scripts/ (scripts/processing/)
- utility_scripts/ (scripts/utilities/)
- PROJECTS/ (old project docs)
- Wingman_docs/ (deprecated system docs)
- debug_selenium/ (debug files)
- old_master_plan/ (previous dashboard structure)

**Note:** All archived code is preserved and can be restored if needed.

---

## Documentation

**Quick Start:**
- scout/README.md - Getting started with Scout

**Complete Workflow:**
- Toolbox/MasterFlow/00_COMPLETE_WORKFLOW.md - Full workflow guide
- Toolbox/MasterFlow/05_STEP_3_PROCESS_DATA.md - AI processing details

**Reference:**
- Toolbox/SCOUT_API_REFERENCE.md - API endpoints
- CLAUDE.md - Project rules and protocols

**Change Log:**
- Toolbox/CHANGELOGS/CHANGELOG_2025-11-11_Scout_Rebuild.md - Rebuild history

---

## Support

**Issues:**
- Check `Toolbox/MasterFlow/` documentation
- Review archived code in `Toolbox/ARCHIVES/legacy_2025-11-11/`
- All backups preserved in `Toolbox/BACKUPS/`

**Contributing:**
- Follow existing code style
- Update documentation
- Test end-to-end before committing
- Never commit without passing tests (per CLAUDE.md)

---

## Success Criteria

✅ Single command execution (`python scout.py`)
✅ Complete workflow in <60 minutes
✅ All working data sources integrated
✅ Graceful degradation on failures
✅ Clean, maintainable codebase (~500 lines)
✅ Comprehensive documentation
✅ All legacy code safely archived
✅ Crash recovery system functional

---

**Scout Status:** Production Ready
**Version:** 1.0
**Last Updated:** 2025-11-11
**Maintainer:** User + Claude AI
**License:** Private (Not for redistribution)
