# Scout Project - Clean Structure

**Last Updated:** 2025-11-11
**Status:** Production Ready - Fully Cleaned

---

## Root Directory (Clean)

```
Investing-fail/
├── .env                    # Environment variables (API keys)
├── .gitignore              # Git ignore rules
├── .nojekyll               # GitHub pages config
├── CLAUDE.md               # Project rules for AI assistants
├── README.md               # Project overview and quick start
├── requirements.txt        # Python dependencies
│
├── scout/                  # ⭐ CORE SYSTEM - Single entry point
├── Scraper/                # Data collectors (X/Twitter scraper)
├── Research/               # Collected data storage
├── scripts/                # Minimal support scripts
│   ├── scout/              # Scout collector module
│   └── trading/            # API client for market data
└── Toolbox/                # Documentation and archives
```

**Total Active Directories:** 6 core folders
**Archived:** Everything else moved to `Toolbox/ARCHIVES/legacy_2025-11-11/`

---

## Core Directories

### 1. scout/ (Primary System)

```
scout/
├── scout.py                    # 🎯 MASTER ENTRY POINT
├── config.py                   # System configuration
├── collectors/
│   ├── core.py                 # Parallel data collection
│   └── __init__.py             # Module exports
├── dash.md                     # Market intelligence output
├── dash.html                   # Web dashboard
├── README.md                   # Quick start guide
└── SCOUT_SYSTEM_SUMMARY.md     # Complete reference
```

**Purpose:** Unified market intelligence system
**Command:** `cd scout && python scout.py`
**Size:** 380KB

### 2. Scraper/ (Data Collectors)

```
Scraper/
├── x_scraper.py               # X/Twitter scraper (local)
├── youtube_scraper.py         # YouTube API integration
├── rss_scraper.py             # RSS feed collector
├── channels.txt               # YouTube channel list
├── rss_feeds.json             # RSS feed configuration
└── requirements.txt           # Scraper dependencies
```

**Purpose:** Data collection from external sources
**Used By:** `scout.py` → calls scrapers via subprocess
**Note:** YouTube and RSS now primarily via API server

### 3. Research/ (Data Storage)

```
Research/
├── X/                         # X/Twitter posts by list
│   ├── Technicals/
│   ├── Crypto/
│   ├── Macro/
│   └── Bookmarks/
├── .cache/                    # Temporary processing files
│   └── YYYY-MM-DD_technical_data.json
└── [Other data folders]
```

**Purpose:** Stores all collected market intelligence data
**Size:** ~3MB (grows over time)
**Cleanup:** Managed by `Toolbox/scripts/cleanup/wingman_cleanup.py`

### 4. scripts/ (Minimal Support)

```
scripts/
├── scout/
│   ├── collector.py           # Core collection logic
│   └── __init__.py
└── trading/
    └── api_client.py          # API server integration (192.168.10.56:3000)
```

**Purpose:** Essential support modules for scout
**Size:** Minimal (~50KB)
**Note:** Everything else archived

### 5. Toolbox/ (Documentation & Archives)

```
Toolbox/
├── MasterFlow/                # Complete workflow documentation
│   ├── 00_COMPLETE_WORKFLOW.md
│   ├── 05_STEP_3_PROCESS_DATA.md
│   └── [Other guides]
├── ARCHIVES/                  # Historical code (safe to reference)
│   └── legacy_2025-11-11/     # Complete old system (15MB)
│       ├── automation_scripts/
│       ├── processing_scripts/
│       ├── utility_scripts/
│       ├── PROJECTS/
│       ├── Wingman_docs/
│       ├── master-plan_original/
│       ├── root_files/
│       ├── scripts_old/
│       └── ARCHIVE_README.md
├── BACKUPS/                   # Safety backups
│   ├── master-plan_2025-11-11_pre-scout.md
│   ├── research-dashboard_2025-11-11_pre-scout.html
│   └── dashboard_2025-11-11_pre-scout.json
├── CHANGELOGS/                # Session logs
│   └── CHANGELOG_2025-11-11_Scout_Rebuild.md
├── scripts/                   # Utility scripts
│   └── cleanup/
│       └── wingman_cleanup.py
└── INSTRUCTIONS/              # Reference documentation
```

**Purpose:** Documentation, archives, backups
**Size:** ~20MB (mostly archives)

### 6. .github/, .git/, .venv/ (Infrastructure)

**Hidden Directories:**
- `.git/` - Git version control
- `.github/` - GitHub configuration
- `.venv/`, `.venv_run/` - Python virtual environments
- `.conda/` - Conda environment
- `.claude/` - Claude Code configuration
- `.pytest_cache/` - Test cache
- `__pycache__/` - Python cache

**Purpose:** Development infrastructure
**Note:** Not shown in normal directory listings

---

## What Was Archived

**Moved to `Toolbox/ARCHIVES/legacy_2025-11-11/`:**

1. **Root Files:**
   - API.md (old API docs)
   - get-pip.py (installer - 2MB)
   - index.html (old dashboard)
   - recon.log (debug log)
   - run_scout_collector.bat (old batch file)
   - SCOUT_REBUILD_COMPLETE.md (moved to archives)
   - .claude_system_context.txt (old context)
   - .wingman_initialization.txt (deprecated)
   - config.py (duplicate - we use scout/config.py)

2. **Unused Directories:**
   - debug_selenium/ (12MB debug files)
   - logs/ (old logs)
   - RnD/ (research & development - archived projects)
   - Tickers/ (ticker-specific studies)
   - Trading/ (old trading scripts)
   - trading-psychology/ (reference docs)
   - scoutcollectors/ (duplicate)
   - master-plan/ (renamed to scout/dash.*)

3. **Scripts Archived:**
   - scripts/ai/ (AI processing - archived)
   - scripts/analysis/ (old analysis scripts)
   - scripts/automation/ (complex workflows - replaced by scout.py)
   - scripts/capture/ (data capture utilities)
   - scripts/config/ (configuration scripts)
   - scripts/dashboard/ (old dashboard scripts)
   - scripts/prep/ (preparation phase scripts)
   - scripts/processing/ (signal calculation - archived)
   - scripts/research/ (research utilities)
   - scripts/scrapers/ (old scraper logic)
   - scripts/tests/ (test files)
   - scripts/utilities/ (sync scripts - replaced)
   - scripts/validation/ (validation scripts)

**Total Archived:** ~15MB, 100+ files

---

## File Count Summary

| Directory | Before | After | Change |
|-----------|--------|-------|--------|
| Root files | 20+ | 5 | -75% |
| Root directories | 20+ | 6 | -70% |
| scripts/ subdirs | 15+ | 2 | -87% |
| Total active code | ~10,000 lines | ~500 lines | -95% |
| Disk usage (active) | ~30MB | ~4MB | -87% |

---

## Essential Files Only

**What You Need:**

```
scout/scout.py              # Run this
scout/dash.html             # View this
scout/config.py             # Configure this
Scraper/x_scraper.py        # X data collection
scripts/trading/api_client.py  # API integration
Research/                   # Your data
Toolbox/MasterFlow/         # Documentation
```

**Everything else is archived and can be ignored.**

---

## Usage

**Run Scout:**
```bash
cd scout/
python scout.py
```

**View Dashboard:**
```bash
open scout/dash.html  # macOS
start scout/dash.html # Windows
```

**That's it. Two commands.**

---

## Archive Access

**To reference old code:**
```bash
cd Toolbox/ARCHIVES/legacy_2025-11-11/
ls  # Browse archived components
```

**To restore (if needed):**
See `Toolbox/ARCHIVES/legacy_2025-11-11/ARCHIVE_README.md`

---

**Project Status:** ✅ Clean, Focused, Production Ready
**Maintenance:** Minimal - only 6 active directories
**Documentation:** Complete in Toolbox/MasterFlow/
**Last Cleaned:** 2025-11-11
