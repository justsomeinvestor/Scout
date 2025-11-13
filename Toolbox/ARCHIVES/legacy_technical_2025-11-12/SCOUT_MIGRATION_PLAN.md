# Scout Migration Plan
**From:** Wingman 3-Phase System
**To:** Scout Unified Workflow
**Date:** 2025-11-08
**Status:** In Progress

---

## Executive Summary

This document outlines the step-by-step migration from the legacy "Wingman" system to the new "Scout" reconnaissance workflow. The migration is designed to be executed across multiple AI-assisted sessions with clear checkpoints and rollback capability.

---

## Migration Goals

### Primary Objectives
1. ✅ **Eliminate Mock Data** - All placeholders, nulls, and fake data removed
2. ✅ **Reduce Token Usage** - From ~50K+ to <10K per update cycle
3. ✅ **Simplify Workflow** - From 3-phase (RECON/PREP/DASH) to single unified script
4. ✅ **Real-time Accuracy** - Every section timestamped and verifiable
5. ✅ **Remove Journaling** - Delete trading journal integration (separate project)
6. ✅ **Rename Everything** - "Wingman" → "Scout" across codebase

### Non-Goals
- ❌ Do NOT remove the dashboard (we're fixing it, not killing it)
- ❌ Do NOT remove scrapers (they work, keep them)
- ❌ Do NOT remove API server integration (core feature)
- ❌ Do NOT rewrite dashboard.html (UI is good, just needs real data)

---

## Current State Assessment

### What's Working ✅
- API server integration (192.168.10.56:3000)
- API client (`scripts/trading/api_client.py`)
- X/Twitter scraper (`Scraper/x_scraper.py`)
- YouTube scraper (`Scraper/youtube_scraper.py`)
- RSS scraper (`Scraper/rss_scraper.py`)
- Dashboard HTML rendering (`research-dashboard.html`)
- Configuration system (`config.py`)

### What's Broken ❌
- Stale data (7 days old as of 2025-11-08)
- Mock/placeholder values in technical data
- Timestamp verification system incomplete
- Session-based AI workflows run out of context
- Token waste on data re-reading
- Multi-phase complexity (RECON → PREP → DASH)

### What's Being Removed 🗑️
- **Journaling System:**
  - `scripts/journal/wingman_commander.py`
  - `scripts/utilities/journal_parser.py`
  - `scripts/utilities/journal_ingest.py`
  - `Journal/` directory (archive, don't delete)

- **Legacy Wingman Scripts:**
  - `scripts/automation/run_wingmap_prep_agentic.py` (PREP phase)
  - `scripts/automation/wingman_dash.py` (replace with scout_update.py)
  - Toolbox Wingman docs (archive, update to Scout)

- **Wingman References:**
  - 117 files contain "wingman" - systematic rename to "scout"
  - Protocol docs, workflow guides, personas

---

## Migration Phases

### Phase 1: Foundation & Documentation ✅ (CURRENT SESSION)

**Session:** 1
**Duration:** 1 hour
**Goal:** Document everything, create recovery plan, backup critical files

#### Tasks:
- [x] Create `SCOUT_SYSTEM_GUIDE.md` (complete system documentation)
- [ ] Create `SCOUT_MIGRATION_PLAN.md` (this document)
- [ ] Create `SCOUT_SESSION_HANDOFF_TEMPLATE.md` (AI collaboration protocol)
- [ ] Create `SCOUT_API_REFERENCE.md` (complete API docs)
- [ ] Backup `dashboard.json` to `Toolbox/BACKUPS/dashboard_2025-11-08.json`
- [ ] Audit all Wingman references (117 files - create inventory)
- [ ] Create Session 1 changelog

#### Success Criteria:
- [ ] All documentation complete and readable
- [ ] Backups created
- [ ] Next session plan clear
- [ ] No code changes yet (plan only)

#### Rollback:
N/A (documentation only)

---

### Phase 2: Code Cleanup & Rename

**Session:** 2
**Duration:** 1-2 hours
**Goal:** Remove journaling, rename Wingman to Scout, archive legacy code

#### Tasks:
- [ ] **2.1 Journaling Removal**
  - [ ] Archive `Journal/` → `Toolbox/ARCHIVES/Journal_2025-11-08/`
  - [ ] Delete `scripts/journal/wingman_commander.py`
  - [ ] Delete `scripts/utilities/journal_parser.py`
  - [ ] Delete `scripts/utilities/journal_ingest.py`
  - [ ] Remove journal config from `config.py`
  - [ ] Update `.gitignore` to exclude Journal/

- [ ] **2.2 Wingman → Scout Rename**
  - [ ] Rename `scripts/automation/wingman_dash.py` → `scout_dash.py` (temp name)
  - [ ] Update all "wingman" strings to "scout" in Python files
  - [ ] Update all "Wingman" strings to "Scout" in docs
  - [ ] Update `config.py` variable names (wingman_ → scout_)
  - [ ] Rename Toolbox docs (WINGMAN_*.md → SCOUT_*.md)

- [ ] **2.3 Legacy Script Archival**
  - [ ] Archive `scripts/automation/run_wingmap_prep_agentic.py`
  - [ ] Archive `scripts/automation/run_recon.py` (may rebuild later)
  - [ ] Archive unused sync scripts in `Toolbox/ARCHIVES/`

#### Success Criteria:
- [ ] No "wingman" references in active code
- [ ] All journal files archived (not deleted)
- [ ] Code still runs (even if functionality broken)
- [ ] Git commit: "refactor: remove journaling, rename Wingman → Scout"

#### Rollback:
```bash
git reset --hard HEAD~1  # Undo commit
# Restore from Toolbox/ARCHIVES/
```

---

### Phase 3: Unified Workflow Implementation

**Session:** 3-4
**Duration:** 2-3 hours
**Goal:** Create single Scout update script, eliminate multi-phase complexity

#### Tasks:
- [ ] **3.1 Create Scout Core Module**
  ```
  scripts/scout/
  ├── __init__.py
  ├── collector.py       # Data collection (API + scrapers)
  ├── transformer.py     # Data transformation
  └── builder.py         # Dashboard JSON generation
  ```

- [ ] **3.2 Implement scout_update.py**
  - [ ] Main orchestrator script
  - [ ] Parallel data collection (API + scrapers)
  - [ ] Error handling & recovery
  - [ ] Progress logging
  - [ ] Verification checks
  - [ ] Timestamp validation

- [ ] **3.3 Data Collection (collector.py)**
  - [ ] API: Single `/api/summary` call for all market data
  - [ ] Run scrapers in parallel (asyncio or multiprocessing)
  - [ ] Cache results to avoid re-processing
  - [ ] Validation: Check for null/mock data before accepting

- [ ] **3.4 Data Transformation (transformer.py)**
  - [ ] Convert API data → dashboard format
  - [ ] Aggregate scraper results
  - [ ] Minimal AI usage (only for summaries)
  - [ ] Calculate signal scores
  - [ ] Generate risk items

- [ ] **3.5 Dashboard Builder (builder.py)**
  - [ ] Load existing dashboard.json (preserve structure)
  - [ ] Update only changed sections
  - [ ] Add timestamps to every section
  - [ ] Validate before saving
  - [ ] Create backup before overwrite

#### Success Criteria:
- [ ] `python scripts/automation/scout_update.py` runs end-to-end
- [ ] Dashboard updates in <2 minutes
- [ ] All sections have current timestamps
- [ ] No mock/placeholder data
- [ ] Token usage <10K per run

#### Rollback:
```bash
git reset --hard <commit-before-phase-3>
# Restore dashboard.json from backup
```

---

### Phase 4: Dashboard Data Quality Fix

**Session:** 5
**Duration:** 2 hours
**Goal:** Eliminate all mock data, fix broken sections, validate accuracy

#### Tasks:
- [ ] **4.1 Audit Dashboard Sections**
  - [ ] Sentiment Cards - check for real data
  - [ ] Sentiment History - verify signal scores
  - [ ] Risk Items - validate alerts
  - [ ] Portfolio Tab - check allocations
  - [ ] News Tab - verify RSS feeds
  - [ ] Technicals Tab - fix PLACEHOLDER values
  - [ ] Social Tab - verify X/Twitter data
  - [ ] Markets Intelligence - check macro data
  - [ ] Daily Planner - validate action items

- [ ] **4.2 Fix Missing Data Sources**
  - [ ] SPX levels (add API endpoint or scraper)
  - [ ] BTC levels (add API endpoint or scraper)
  - [ ] Any other PLACEHOLDER fields

- [ ] **4.3 Implement Data Age Indicators**
  - [ ] Show "Updated X minutes ago" per section
  - [ ] Color-code freshness (green <1hr, yellow <24hr, red >24hr)
  - [ ] Add "last updated" to dashboard header

- [ ] **4.4 Validation System**
  - [ ] Pre-save validation: Check for null/mock/placeholder
  - [ ] Post-save verification: Load and verify dashboard.json
  - [ ] Create validation report: `verify_dashboard_data.py`

#### Success Criteria:
- [ ] Zero "PLACEHOLDER", "null", "N/A", "mock" values
- [ ] Every section has real, current data
- [ ] Timestamps within 1 hour of current time
- [ ] Dashboard renders correctly with real data

#### Rollback:
```bash
cp Toolbox/BACKUPS/dashboard_2025-11-08.json master-plan/dashboard.json
```

---

### Phase 5: Testing & Validation

**Session:** 6
**Duration:** 1-2 hours
**Goal:** End-to-end testing, edge case handling, error recovery

#### Tasks:
- [ ] **5.1 Happy Path Testing**
  - [ ] Fresh API server data
  - [ ] All scrapers successful
  - [ ] Dashboard updates correctly
  - [ ] Timestamps accurate

- [ ] **5.2 Error Scenario Testing**
  - [ ] API server down
  - [ ] Scraper failures
  - [ ] Network timeout
  - [ ] Invalid data from API
  - [ ] Disk space issues

- [ ] **5.3 Recovery Testing**
  - [ ] Partial failure (some scrapers work)
  - [ ] Stale data fallback
  - [ ] Dashboard corruption recovery
  - [ ] Backup restore

- [ ] **5.4 Performance Testing**
  - [ ] Measure full update time
  - [ ] Measure token usage
  - [ ] Check memory usage
  - [ ] Validate parallel execution

#### Success Criteria:
- [ ] All tests pass
- [ ] Clear error messages on failures
- [ ] Graceful degradation (partial data OK)
- [ ] Recovery documented

---

### Phase 6: Production Hardening

**Session:** 7+
**Duration:** Ongoing
**Goal:** Monitoring, logging, automation, maintenance

#### Tasks:
- [ ] **6.1 Logging System**
  - [ ] Structured logs (JSON format)
  - [ ] Log rotation
  - [ ] Error tracking
  - [ ] Performance metrics

- [ ] **6.2 Monitoring**
  - [ ] Health check endpoint
  - [ ] Data freshness alerts
  - [ ] Scraper success rates
  - [ ] API server uptime

- [ ] **6.3 Automation**
  - [ ] Scheduled updates (cron/Task Scheduler)
  - [ ] Auto-recovery on failure
  - [ ] Backup automation
  - [ ] Archive cleanup

- [ ] **6.4 Documentation**
  - [ ] Update README
  - [ ] API documentation
  - [ ] Troubleshooting guide
  - [ ] Runbook for operators

#### Success Criteria:
- [ ] Scout runs unattended
- [ ] Alerts on failures
- [ ] Metrics tracked
- [ ] Documentation complete

---

## File Inventory

### Files to Delete (Archive First!)
```
scripts/journal/wingman_commander.py
scripts/utilities/journal_parser.py
scripts/utilities/journal_ingest.py
scripts/automation/run_wingmap_prep_agentic.py (legacy PREP)
Toolbox/scripts/cleanup/wingman_cleanup.py (no longer needed)
```

### Files to Rename
```
scripts/automation/wingman_dash.py → scout_dash.py → scout_update.py
Toolbox/INSTRUCTIONS/Domains/WINGMAN_*.md → SCOUT_*.md (archive originals)
Toolbox/Wingman/* → Toolbox/Scout/*
```

### Files to Create
```
scripts/scout/__init__.py
scripts/scout/collector.py
scripts/scout/transformer.py
scripts/scout/builder.py
scripts/automation/scout_update.py
scripts/utilities/verify_dashboard_data.py
Toolbox/SCOUT_SYSTEM_GUIDE.md ✅
Toolbox/SCOUT_MIGRATION_PLAN.md (this file)
Toolbox/SCOUT_SESSION_HANDOFF_TEMPLATE.md
Toolbox/SCOUT_API_REFERENCE.md
```

### Files to Modify
```
config.py (rename wingman → scout, remove journal config)
.gitignore (add Journal/ exclusion)
README.md (update documentation)
master-plan/dashboard.json (data quality fixes)
```

---

## Wingman References Audit

**Total Files:** 117 (from exploration)

**Categories:**
1. **Protocol/Documentation** (~30 files)
   - `Toolbox/INSTRUCTIONS/Domains/WINGMAN_*.md`
   - `Toolbox/Wingman/*.md`
   - `Toolbox/PROJECTS/WINGMAN_*/`

2. **Active Scripts** (~5 files)
   - `scripts/automation/wingman_dash.py`
   - `scripts/automation/run_wingmap_prep_agentic.py`
   - `scripts/journal/wingman_commander.py`

3. **Archived/Toolbox** (~80 files)
   - Old changelogs
   - Project documentation
   - Workflow guides

**Action Plan:**
- **Active Scripts:** Rename to Scout
- **Documentation:** Archive originals, create Scout versions
- **Archived Files:** Leave as-is (historical record)

---

## Rollback Strategy

### Emergency Rollback (Full System)
```bash
# 1. Restore from git
git reset --hard <commit-before-migration>

# 2. Restore dashboard.json
cp Toolbox/BACKUPS/dashboard_2025-11-08.json master-plan/dashboard.json

# 3. Restore archived files (if needed)
cp -r Toolbox/ARCHIVES/Wingman_2025-11-08/* <original-locations>
```

### Partial Rollback (Per Phase)
Each phase has specific rollback instructions in its section above.

### Backup Checklist (Before Each Phase)
- [ ] Git commit current state
- [ ] Backup dashboard.json
- [ ] Archive files being deleted
- [ ] Document current working directory state

---

## Session Handoff Protocol

### At End of Each Session:
1. **Update Changelog**
   - Create `Toolbox/CHANGELOGS/CHANGELOG_YYYY-MM-DD_scout_session_N.md`
   - Document what was completed
   - Document what failed
   - Document next steps

2. **Update Migration Plan**
   - Check off completed tasks
   - Add any new issues discovered
   - Update estimates

3. **Commit Code**
   - Clear commit message
   - Reference session number
   - No broken code in commit

4. **Handoff Document**
   - Fill out `SCOUT_SESSION_HANDOFF_TEMPLATE.md`
   - State current system status
   - List next session TODOs
   - Highlight any blockers

---

## Risk Mitigation

### High Risk Items
1. **Data Loss** → Backups before every change
2. **Dashboard Broken** → Validate before save
3. **API Server Down** → Graceful degradation
4. **Scraper Failures** → Partial success OK
5. **Session Context Loss** → Documentation + handoffs

### Contingency Plans
- **If Scout fails:** Rollback to Wingman (archived)
- **If dashboard corrupted:** Restore from backup
- **If data stale:** Manual scraper run + API check
- **If session runs long:** Clear handoff, resume next session

---

## Success Metrics

### Phase Completion
- [ ] Phase 1: Documentation ✅
- [ ] Phase 2: Cleanup & Rename
- [ ] Phase 3: Unified Workflow
- [ ] Phase 4: Data Quality
- [ ] Phase 5: Testing
- [ ] Phase 6: Production

### System Health
- [ ] Dashboard updates <2 minutes
- [ ] Token usage <10K per update
- [ ] Zero mock/placeholder data
- [ ] All sections timestamped
- [ ] Scrapers >90% success rate
- [ ] API server >99% uptime

### User Value
- [ ] Real-time market intelligence
- [ ] Accurate signal scores
- [ ] Actionable risk alerts
- [ ] Portfolio recommendations based on current data
- [ ] One-click dashboard refresh

---

## Next Steps

**Immediate (This Session):**
1. Complete Phase 1 documentation
2. Backup dashboard.json
3. Create Session 1 changelog
4. Handoff to next session

**Session 2:**
1. Remove journaling system
2. Rename Wingman → Scout
3. Archive legacy code

**Session 3-4:**
1. Build Scout unified workflow
2. Test end-to-end
3. Validate data quality

---

## Questions & Decisions

### Open Questions
- Q: Keep or delete `Journal/` directory?
  - **Decision:** Archive to `Toolbox/ARCHIVES/`, don't delete (may extract useful data later)

- Q: Keep `run_recon.py` or delete?
  - **Decision:** Archive for now, may rebuild as standalone data collector

- Q: Support partial updates (only changed data)?
  - **Decision:** Yes, Phase 3 implementation

- Q: Add API endpoints for SPX/BTC?
  - **Decision:** Build on server if needed, Phase 4

### Resolved Decisions
- ✅ Rename Wingman → Scout (confirmed)
- ✅ Remove journaling system (confirmed)
- ✅ Single unified workflow (confirmed)
- ✅ Offload data to API server (confirmed)
- ✅ Minimal AI usage (confirmed)

---

**Last Updated:** 2025-11-08
**Session:** 1
**Status:** Phase 1 In Progress
