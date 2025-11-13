# Legacy System Archive - 2025-11-11

**Archive Date:** 2025-11-11
**Reason:** Consolidated into unified Scout system
**Status:** Preserved for reference

---

## What's Archived Here

This directory contains the previous "Wingman/MasterFlow" system that was consolidated into the simplified "Scout" system on 2025-11-11.

**All code is preserved** - nothing was deleted. This archive allows rolling back if needed.

---

## Archived Components

### automation_scripts/
**Original Location:** `scripts/automation/`
**Contents:**
- run_workflow.py (724 lines) - Previous main orchestrator
- scout_update.py (650 lines) - Dashboard update workflow
- run_all_scrapers.py - Scraper orchestration (still used by Scout)
- run_recon.py - Data collection phase
- update_master_plan.py (849 lines) - Master plan updates
- Various sync scripts (10+ files)

**Why Archived:**
- Replaced by unified `scout/scout.py` (200 lines)
- Complex multi-script workflows consolidated
- Some scripts still functional but redundant

### processing_scripts/
**Original Location:** `scripts/processing/`
**Contents:**
- calculate_signals.py (764 lines) - Signal calculation
- fetch_market_data.py - Market data fetching
- fetch_technical_data.py - Technical data collection
- Various processing utilities

**Why Archived:**
- Signal calculation integrated into scout workflow
- Some functions may be restored if needed
- Preserved for reference

### utility_scripts/
**Original Location:** `scripts/utilities/`
**Contents:**
- sync_social_tab.py (401 lines)
- sync_technicals_tab.py (512 lines)
- sync_news_tab.py (290 lines)
- sync_daily_planner.py (396 lines)
- verify_timestamps.py (529 lines)
- verify_consistency.py (340 lines)
- 10+ other sync scripts

**Why Archived:**
- Dashboard syncing integrated into Scout
- Individual sync operations consolidated
- Verification logic simplified

### PROJECTS/
**Original Location:** `Toolbox/PROJECTS/`
**Contents:**
- WINGMAN_PREP_DASH_CONSOLIDATION/
- WINGMAN_PREP_OPTIMIZATION/
- Morning_Prep_Optimization/
- Various project planning documents

**Why Archived:**
- Completed migration projects
- Historical planning documents
- No longer actively developed

### Wingman_docs/
**Original Location:** `Toolbox/Wingman/`
**Contents:**
- Wingman system documentation
- Protocol guides
- Reference materials

**Why Archived:**
- "Wingman" terminology deprecated
- Replaced by "Scout" system
- Historical reference only

### debug_selenium/
**Original Location:** `Toolbox/debug_selenium/`
**Contents:**
- 8 HTML debug dump files (~12MB)
- Selenium debugging artifacts

**Why Archived:**
- Large debug files no longer needed
- Scrapers stable and working
- Freed up 12MB disk space

### old_master_plan/
**Original Location:** `master-plan/`
**Contents:**
- master-plan.md (original)
- research-dashboard.html (original)
- dashboard.json (original)
- Various archive folders

**Why Archived:**
- Renamed to dash.md / dash.html in scout/
- Structure consolidated
- Backups exist in Toolbox/BACKUPS/

---

## What's Still Active

**Not Archived (Still in Use):**
- `Scraper/` - Original scrapers (X, YouTube, RSS)
- `Research/` - Data storage
- `Toolbox/MasterFlow/` - Current documentation
- `Toolbox/BACKUPS/` - Safety backups
- `Toolbox/scripts/cleanup/` - Cleanup utilities
- `config.py` - System configuration (copied to scout/)
- `scout/` - New unified system

---

## How to Restore

If you need to roll back or reference old code:

### 1. View Archive Contents
```bash
ls Toolbox/ARCHIVES/legacy_2025-11-11/
```

### 2. Restore Individual Files
```bash
# Example: Restore calculate_signals.py
cp Toolbox/ARCHIVES/legacy_2025-11-11/processing_scripts/calculate_signals.py scripts/processing/
```

### 3. Restore Complete Folder
```bash
# Example: Restore all automation scripts
cp -r Toolbox/ARCHIVES/legacy_2025-11-11/automation_scripts scripts/automation
```

### 4. Full System Rollback
```bash
# Restore from backups
cp Toolbox/BACKUPS/master-plan_2025-11-11_pre-scout.md master-plan/master-plan.md
cp Toolbox/BACKUPS/research-dashboard_2025-11-11_pre-scout.html master-plan/research-dashboard.html

# Restore archived scripts
cp -r Toolbox/ARCHIVES/legacy_2025-11-11/automation_scripts scripts/automation
cp -r Toolbox/ARCHIVES/legacy_2025-11-11/processing_scripts scripts/processing
cp -r Toolbox/ARCHIVES/legacy_2025-11-11/utility_scripts scripts/utilities
```

---

## Key Differences: Old vs New

### Entry Points

**Old System:**
- `python scripts/automation/run_workflow.py YYYY-MM-DD`
- `python scripts/automation/scout_update.py YYYY-MM-DD`
- `python scripts/automation/run_recon.py`
- Multiple options, unclear which to use

**New System:**
- `python scout/scout.py`
- Single entry point, no ambiguity

### Workflow Complexity

**Old System:**
- 3-phase execution (RECON → PREP → DASH)
- 10+ sync scripts
- Complex orchestration
- ~10,000+ lines of code

**New System:**
- Unified workflow
- Integrated processing
- Simple orchestration
- ~500 lines of code

### Documentation

**Old System:**
- Scattered across multiple locations
- Wingman vs Scout confusion
- Multiple README files

**New System:**
- Consolidated in scout/ and Toolbox/MasterFlow/
- Clear naming (Scout only)
- Single source of truth

---

## Statistics

**Files Archived:** 100+
**Lines of Code:** ~10,000
**Disk Space Freed:** ~15MB (after removing duplicates and debug files)
**Reduction:** 95% code reduction while maintaining functionality

---

## Important Notes

1. **Nothing was deleted** - All code preserved in this archive
2. **Backups exist** - See Toolbox/BACKUPS/ for pre-archive state
3. **Fully reversible** - Can restore any component if needed
4. **No data loss** - All Research/ data intact
5. **Scrapers unchanged** - Original scrapers still work

---

## References

**Migration Documentation:**
- Toolbox/CHANGELOGS/CHANGELOG_2025-11-11_Scout_Rebuild.md

**New System Documentation:**
- scout/README.md
- scout/SCOUT_SYSTEM_SUMMARY.md
- Toolbox/MasterFlow/00_COMPLETE_WORKFLOW.md

**Backups:**
- Toolbox/BACKUPS/master-plan_2025-11-11_pre-scout.md
- Toolbox/BACKUPS/research-dashboard_2025-11-11_pre-scout.html
- Toolbox/BACKUPS/dashboard_2025-11-11_pre-scout.json

---

**Archive Created:** 2025-11-11
**Preserved By:** Claude AI Assistant
**Purpose:** Historical reference and rollback capability
**Status:** Complete and verified
