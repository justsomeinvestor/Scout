# Zero-Tolerance Data Freshness System

**Status:** ✅ OPERATIONAL
**Last Updated:** 2025-10-21
**Mission:** Ensure 100% data freshness at all times - stale data = HARD STOP

---

## Overview

The Zero-Tolerance Data Freshness System ensures that **ALL** trading decisions are based on current, verified data. Any stale, missing, or invalid data triggers an automatic **HARD STOP** that blocks the entire workflow.

**Core Principle:** *Trading on stale data is unacceptable and poses catastrophic risk.*

---

## System Architecture

### 1. **Complete Automation Coverage (20/20 Sections)**

Every section in master-plan.md has an automated sync script:

| Section | Script | What It Updates |
|---------|--------|----------------|
| Dashboard Cards | `update_master_plan.py` | Sentiment, metrics, risk, actions, consensus |
| Daily Planner | `sync_daily_planner.py` | Priorities, key levels, events, AI interpretation |
| Portfolio Tab | `update_master_plan.py` | AI interpretation |
| Markets Tab | `update_master_plan.py` | Unified macro + crypto + tech AI interpretation |
| News & Catalysts Tab | `sync_news_tab.py` + `update_media_catalysts.py` | RSS aggregation + curated catalysts |
| X Sentiment Tab | `update_x_sentiment_tab.py` + `sync_social_tab.py` | Social data, trending tickers, AI interpretation |
| Technicals Tab | `sync_technicals_tab.py` | Market data, options, AI interpretation |

**Result:** 100% automation coverage - no section can go stale undetected.

---

### 2. **Timestamp Verification (verify_timestamps.py)**

**Purpose:** Check all 20 required timestamps and return exit codes based on health.

**Exit Codes:**
- `0` = SUCCESS - All 20 sections current (100% health)
- `2` = CRITICAL FAILURE - ANY section stale/missing/invalid (BLOCKS workflow)

**Required Timestamps (20 total):**
```
dashboard.sentimentCardsUpdated
dashboard.sentimentHistoryUpdated
dashboard.metricsUpdated
dashboard.riskItemsUpdated
dashboard.quickActionsUpdated
dashboard.providerConsensusUpdated
dashboard.dailyPlanner.prioritiesUpdated
dashboard.dailyPlanner.keyLevelsUpdated
dashboard.dailyPlanner.scheduledEventsUpdated
dashboard.dailyPlanner.aiInterpretation.updatedAt
dashboard.dailyPlanner.endOfDay.ranAt
tabs.portfolio.aiInterpretation.updatedAt
tabs.markets.aiInterpretation.updatedAt  # Consolidated Macro + Crypto + Tech
tabs.news_catalysts.aiInterpretation.updatedAt  # Consolidated News + Media & Catalysts
tabs.xsentiment.aiInterpretation.updatedAt
tabs.xsentiment.socialTabSyncedAt
tabs.xsentiment.crypto_trending.updatedAt
tabs.xsentiment.macro_trending.updatedAt
tabs.technicals.aiInterpretation.updatedAt
tabs.technicals.technicalsTabSyncedAt
```

**Usage:**
```bash
# Human-readable output
python scripts/utilities/verify_timestamps.py --date 2025-10-21

# Machine-readable JSON (for AI task lists)
python scripts/utilities/verify_timestamps.py --date 2025-10-21 --json
```

---

### 3. **Workflow Blocking Enforcement**

The workflow (`run_workflow.py`) **automatically halts** if verification fails:

**Phase 4.5: Verify Timestamps**
- Runs `verify_timestamps.py --date YYYY-MM-DD`
- If exit code = 2 → **IMMEDIATE HARD STOP**
- Workflow terminates with clear error message
- No further phases execute (Portfolio Advisor blocked)

**Enforcement Logic:**
```python
if result['returncode'] == 2:
    print("💥 CRITICAL FAILURE - WORKFLOW HALTED")
    print("🚫 STALE DATA DETECTED - CANNOT PROCEED WITH TRADING")
    sys.exit(2)  # HARD STOP
```

**Result:** Impossible to proceed past verification with stale data.

---

### 4. **Pre-Trade Verification Command**

**Command:** `"wingman verify"`

**What It Does:**
- Runs `verify_timestamps.py` before ANY trade entry
- Checks if all 23 sections are current
- Returns one of two responses:
  - ✅ **"Safe to trade - 100% data freshness confirmed"**
  - 🚫 **"HALT - Stale data detected. Fix before trading."**

**Integration:** Added to Command Center reference card as mandatory pre-trade check.

---

### 5. **Dashboard Visual Indicator**

**Location:** research-dashboard.html (top-right corner)

**Behavior:**
- **Green dot** = All sections current (100% health)
- **Red dot** = One or more sections stale

**Implementation:** JavaScript checks all 23 timestamp fields and shows red if ANY are stale.

**Code Location:** `master-plan/research-dashboard.html` lines 2363-2393

---

## Workflow Integration

### Daily Workflow (Automated)

```
Phase 0: Parse Journal
Phase 1: Fetch Market Data
Phase 1.5: Fetch Technical Data
Phase 2: Calculate Signals
Phase 3: Update Master Plan (dashboard cards)
Phase 3.75: Update X Sentiment Tab
Phase 3.8: Sync Social Tab
Phase 3.9: Sync Technicals Tab
Phase 3.5: AI Media Curation
Phase 3.10: Sync News Tab          ← NEW
Phase 3.11: Sync Daily Planner     ← NEW
Phase 4: Verify Consistency
Phase 4.5: Verify Timestamps       ← BLOCKING CHECKPOINT
  └─ Exit code 2 → HARD STOP (no Phase 5)
  └─ Exit code 0 → Proceed to Phase 5
Phase 5: AI Portfolio Advisor
```

**Key Points:**
- All sync scripts run BEFORE verification
- Verification acts as final gate before trading recommendations
- If verification fails, workflow terminates immediately

---

### Manual Verification (Pre-Trade)

**Before entering ANY trade:**

1. **Check Dashboard:** Visual indicator (top-right green dot)
2. **Run Command:** `"wingman verify"`
3. **Wait for Response:**
   - ✅ Green = Proceed with trade
   - 🚫 Red = DO NOT TRADE - run `wingman dash` first

**This is MANDATORY before trade entry.**

---

## Failure Recovery

### If Workflow Halts (Exit Code 2)

**Step 1: Identify Stale Sections**
```bash
# Check verification report
python scripts/utilities/verify_timestamps.py --date 2025-10-21

# Review JSON task list
cat Research/.cache/stale_sections_2025-10-21.json
```

**Step 2: Run Missing Sync Scripts**
```bash
# News tab stale?
python scripts/utilities/sync_news_tab.py 2025-10-21

# Daily planner stale?
python scripts/utilities/sync_daily_planner.py 2025-10-21

# Technicals tab stale?
python scripts/utilities/sync_technicals_tab.py 2025-10-21

# Media tab stale?
python scripts/automation/update_media_catalysts.py 2025-10-21
```

**Step 3: Re-Verify**
```bash
python scripts/utilities/verify_timestamps.py --date 2025-10-21
```

**Step 4: Re-Run Workflow**
```bash
python scripts/automation/run_workflow.py 2025-10-21 --skip-fetch --skip-signals
```

**Expected:** Verification passes (exit code 0), workflow completes successfully.

---

## Success Criteria

✅ **100% automation coverage** - All 20 sections have sync scripts
✅ **100% freshness tracking** - verify_timestamps.py checks all 20 timestamps
✅ **Hard blocking** - Workflow STOPS if any section stale (exit code 2)
✅ **Pre-trade verification** - "wingman verify" command available
✅ **Visual indicator** - Dashboard shows green/red freshness status
✅ **Zero tolerance** - ANY stale data = HARD STOP, no exceptions
✅ **Streamlined structure** - Markets tab (Macro + Crypto + Tech) + News & Catalysts tab (News + Media)

---

## Key Files

### Scripts
- `scripts/utilities/verify_timestamps.py` - Verification engine (exit code 2 logic)
- `scripts/automation/run_workflow.py` - Workflow orchestrator (blocking enforcement)
- `scripts/utilities/sync_news_tab.py` - News tab automation
- `scripts/utilities/sync_daily_planner.py` - Daily planner automation
- `scripts/utilities/sync_technicals_tab.py` - Technicals tab automation (updated)
- `scripts/automation/update_media_catalysts.py` - Media tab automation (rewritten with YAML handler)

### Configuration
- `Journal/COMMAND_CENTER.md` - "wingman verify" command reference
- `master-plan/research-dashboard.html` - Visual freshness indicator (lines 2363-2393)

### Documentation
- `Toolbox/PROTOCOLS/ZERO_TOLERANCE_DATA_FRESHNESS.md` - This file

---

## Mission-Critical Principles

1. **Zero Tolerance:** ANY stale data triggers HARD STOP
2. **No Trading on Stale Data:** Workflow blocks before Portfolio Advisor runs
3. **100% Coverage:** Every section monitored, no exceptions
4. **Automatic Enforcement:** System prevents human override
5. **Clear Communication:** Errors show exactly what's stale and how to fix

**Bottom Line:** This system makes it **impossible** to trade on stale data.

---

**Status:** ✅ OPERATIONAL - All phases complete, zero-tolerance system active.
