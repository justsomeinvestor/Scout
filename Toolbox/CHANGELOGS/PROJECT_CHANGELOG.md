# Project Changelog - Trading Command Center Development

**Project Start Date:** 2025-10-19
**Current Date:** 2025-10-24
**Session Phase:** Phase 2 (Wingman System & Data Quality) - IN PROGRESS

---

## Latest Updates (2025-10-24)

### Update 2025-10-24C: Dashboard UI Polish (Analyst Consensus)
**Date:** 2025-10-24
**Priority:** Medium - User Experience
**Status:** ✅ Complete

**Problem:**
Analyst Consensus section badges (CAUTIOUSLY BULLISH, BEARISH, MIXED, NEUTRAL) looked cluttered and competed with topic text for attention. Visual hierarchy was confusing with prominent boxes/borders creating noise.

**Solution Implemented:**

**Badge Redesign**:
- Changed from side-by-side to vertical stack (badge ABOVE topic)
- Made badges very subtle: tiny pills with minimal styling
- Removed borders, reduced opacity to 0.75
- Very light background (10% color opacity)
- Small font (0.65em) with light weight (500)
- Badge acts as metadata label, not main element

**Visual Hierarchy**:
- Topic text remains bold and prominent (dominant element)
- Badge provides context without competing for attention
- Tight 6px gap creates unified visual unit
- Left column aligned to flex-start (top aligned)

**Files Modified:**
1. `master-plan/research-dashboard.html`
   - Line 855: Changed alignment from `center` to `flex-start`
   - Lines 3449-3479: Restructured badge/topic layout to vertical stack
   - Badge styling: minimal padding, no border, subtle colors

**Result:**
```
   [cautiously bullish]  ← Tiny, subtle pill (metadata)
FEAR EXTREMES AT CRITICAL SUPPORT  ← Bold topic (main focus)
Description text follows naturally...
```

**Benefits:**
- ✅ Clean, professional appearance
- ✅ Clear visual hierarchy (topic dominates)
- ✅ No competing elements or visual clutter
- ✅ Badges provide context without distraction

**Rationale:** Dashboard UI should guide user attention to important information (topic) while providing supporting context (sentiment) without creating visual noise.

---

### Update 2025-10-24B: Economic Calendar CSV Automation
**Date:** 2025-10-24
**Priority:** High - Data Quality
**Status:** ✅ Complete

**Problem:**
Economic calendar showed stale data (Oct 15-16 events when today is Oct 24). Calendar was manually maintained in master-plan.md and never updated.

**Solution Implemented:**

**CSV-Based Automation**:
- Created `parse_economic_calendar.py` to parse monthly CSV file from `Research/Macro/calendar-event-list.csv`
- Filters for USD + HIGH/MEDIUM impact events only
- Categorizes: today[], thisWeek[], nextWeek[], keyDates[], summary
- Smart event name cleanup (CPI, NFP, FOMC abbreviations)
- Intelligent summary generation (prioritizes FOMC > Inflation > Employment)

**Workflow Integration**:
- Created `update_economic_calendar.py` standalone update script
- Integrated as Phase 2.5 in `update_master_plan.py`
- Runs automatically during daily workflow
- Updates Macro Environment section in master-plan.md

**Monthly Maintenance**:
- Download economic calendar CSV once per month
- Save as `Research/Macro/calendar-event-list.csv`
- Calendar auto-updates daily from CSV

**Files Created/Modified:**
1. NEW: `scripts/processing/parse_economic_calendar.py` (289 lines)
2. NEW: `scripts/automation/update_economic_calendar.py` (128 lines)
3. UPDATED: `scripts/automation/update_master_plan.py` (added Phase 2.5)
4. UPDATED: `.env` (added FMP_API_KEY for future use)

**Testing Results:**
- ✅ CSV parsing: 29 events (6 today, 15 this week, 8 next week)
- ✅ Master plan update: Calendar refreshed with Oct 24-Nov 7 events
- ✅ Summary: "FOMC decision scheduled Oct 29 is the key event..."

**Benefits:**
- ✅ Always fresh calendar data (auto-updates daily)
- ✅ Zero daily maintenance (just download CSV monthly)
- ✅ Smart filtering and categorization
- ✅ Clean event names and intelligent summaries

**Documentation:**
- Created: `toolbox/ECONOMIC_CALENDAR_AUTOMATION.md`

**Rationale:** Stale calendar data leads to missed events and bad trading decisions. CSV-based automation provides fresh data with minimal maintenance.

---

### Update 2025-10-24A: Contrarian Detector Automation + Hard Fail Data Validation
**Date:** 2025-10-24
**Priority:** Critical - Trading Decision Support
**Status:** ✅ Complete

**Problem:**
1. Contrarian Detector widget was manually maintained and went stale immediately after workflow runs
2. Script silently used fallback values (50/100) when data sources missing
3. Dashboard showed outdated contrarian signals that could lead to bad trading decisions

**Solution Implemented:**

**Part 1: Full Automation**
- Created `calculate_contrarian_detector()` method in `update_x_sentiment_tab.py` (lines 714-815)
- Auto-generates all 9 contrarian detector fields based on real-time X sentiment
- Opportunity detection: EXTREME (≤20 or ≥85), ACTIVE (21-25 or 75-84), NOT YET (26-74)
- Actions: BUY (extreme fear), SELL (extreme greed), FADE (high greed), WAIT (neutral)
- Dynamic thresholds, historical win rates, confidence levels, monitoring guidance

**Part 2: Hard Fail Data Validation**
- Added strict validation that exits with error code 1 if crypto/macro data missing
- Removed silent fallback values that created dangerous false signals
- Clear error messages: "❌ CRITICAL ERROR: CRYPTO SENTIMENT DATA MISSING"
- Warning: "⚠️ DO NOT TRADE ON STALE DATA ⚠️"
- Master-plan.md NOT updated if data invalid

**Files Modified:**
1. `scripts/automation/update_x_sentiment_tab.py`
   - Lines 714-815: New `calculate_contrarian_detector()` method
   - Lines 520-542: Hard fail validation (removed fallback values)
   - Lines 664-666: Integration into `update_xsentiment_tab()`
   - Lines 112-119: Updated success message logic

**Testing Results:**
- ✅ Missing data: Script exits with code 1, no master-plan.md update
- ✅ Valid data: All 9 fields auto-populate with fresh calculations
- ✅ Current state (60/100): Status=NOT YET, Action=WAIT, Confidence=low

**Benefits:**
- ✅ Always fresh data or script fails loudly
- ✅ Zero maintenance required
- ✅ Clear BUY/SELL/FADE/WAIT signals with confidence levels
- ✅ Historical backtesting context for each zone
- ✅ Dynamic monitoring guidance

**Documentation:**
- Created: `toolbox/CONTRARIAN_DETECTOR_AUTOMATION.md` (full technical spec)

**Rationale:** Zero-tolerance for stale data in trading decisions. Contrarian signals are high-stakes - must be accurate or not shown at all.

---

## Summary

This document captures all architectural decisions, technical pivots, and implementation milestones chronologically. Created for handoff purposes to allow new AI contractors to understand the evolution of this system.

---

## Phase 2: Wingman Trading Partner System (2025-10-21)

### Decision 2.1: Automated Scraper Data Verification System
**Date:** 2025-10-21 - Session 5
**Problem:** Wingman manually checking scraper data freshness was error-prone. Missed CNBC 10-21 data while reporting only 10-20 data available. Critical failure in data quality verification.
**Root Cause:** Manual Glob pattern checking vulnerable to human/AI oversight errors.
**Impact:** Bad data → Bad trading signals → Real financial loss (mission-critical failure)

**Solution Implemented:**
- Created `scripts/utilities/verify_scraper_data.py` (336 lines)
- Programmatic verification of ALL scraper outputs for target date
- Checks: RSS (5 providers), YouTube (19 channels), X/Twitter (4 categories), Technical data
- Exit codes: 0 = all fresh, 1 = script error, 2 = data incomplete/stale
- Detailed failure reporting with missing providers listed

**Workflow Integration:**
- Updated Wingman Protocol: WINGMAP PREP now requires verification FIRST
- Updated `Toolbox/INSTRUCTIONS/Research/How_to_use_Research.txt` Step 0A
- If verification fails → STOP workflow and report to Pilot
- If verification passes → Proceed automatically

**Files Modified:**
1. NEW: `scripts/utilities/verify_scraper_data.py`
2. UPDATED: `Toolbox/INSTRUCTIONS/Domains/Journal_Trading_Partner_Protocol.txt`
3. UPDATED: `Toolbox/INSTRUCTIONS/Research/How_to_use_Research.txt`
4. UPDATED: `Journal/command-center.html` (added wingmap prep command reference)

**Rationale:** Zero-tolerance for data quality failures. Automation prevents human error. Mission-critical safeguard.

### Decision 2.2: "wingmap prep" Command Integration
**Date:** 2025-10-21 - Session 5
**Decision:** Create voice-activated trigger for full research workflow (like "wingman recon")
**Implementation:**
- Command: "wingmap prep"
- Triggers: Full research processing pipeline (Steps 0-4)
- Duration: ~30-45 minutes
- Prerequisites: "wingman recon" must run first
- Includes automated data verification as Step 0A

**Command Flow:**
```
1. User: "wingmap prep"
2. Wingman: Run verify_scraper_data.py
3. If exit code = 2: STOP and report failures
4. If exit code = 0: Execute Steps 0B-4 (web searches, summaries, signals)
5. Report: Composite signal score + tier
```

**Command Center Documentation:**
- Added to Data Collection Control section
- Listed alongside "wingman recon"
- Visible in Command Reference accordion

**Rationale:** Consistent UX with existing commands. Clear prerequisite chain (recon → prep). Automated quality gates.

### Decision 2.3: "wingman dash" Command Integration
**Date:** 2025-10-21 - Session 6
**Decision:** Create voice-activated trigger for dashboard update workflow (completing the command trilogy)
**Implementation:**
- Command: "wingman dash"
- Triggers: Dashboard update workflow (Steps 6-9 from How_to_use_MP_CLAUDE_ONLY.txt)
- Duration: ~20-25 minutes
- Prerequisites: "wingmap prep" must complete first
- Command: `python scripts/automation/run_workflow.py YYYY-MM-DD --skip-fetch --skip-signals`

**Command Flow:**
```
1. User: "wingman dash"
2. Wingman: Verify signals_YYYY-MM-DD.json exists + Market Sentiment Overview exists
3. If files missing: STOP and report to Commander
4. If files exist: Execute Steps 6-9 (master plan sync, tabs update, verification)
5. Report: Dashboard URL + completion status
```

**What Gets Updated:**
- master-plan/master-plan.md (YAML + markdown sections)
- master-plan/research-dashboard.html (visual dashboard)
- Journal/account_state.json (balance tracking)
- Research/.processing_log.json (audit trail)

**Command Center Documentation:**
- Added to Data Collection Control section
- Listed after "wingmap prep" (logical sequence: recon → prep → dash)
- Documented in Journal_Trading_Partner_Protocol.txt

**Rationale:** Completes the daily workflow command trinity. --skip flags prevent redundant processing (data already scraped via recon, signals already calculated via prep). Fast dashboard sync (20-25 min vs 45+ min full workflow).

### Decision 2.4: Terminology Update (Pilot → Commander)
**Date:** 2025-10-21 - Session 6
**Decision:** Update all references from "Pilot" to "Commander" per user request
**Implementation:**
- Global find/replace in Journal_Trading_Partner_Protocol.txt
- Updated 30+ instances throughout protocol
- "Wingman" remains unchanged (AI assistant callsign)

**Rationale:**
- User preference: "i want to be called commander"
- Maintains military/aviation theme (Commander-Wingman relationship)
- More authoritative command structure terminology

**Impact:** All protocol documentation now uses "Commander" consistently. Command structure preserved (Commander commands, Wingman executes).

### Decision 2.5: "wingman dash" Workflow Automation Enhancement
**Date:** 2025-10-21 - Session 6
**Problem:** "wingman dash" command ran scripts but didn't complete AI curation workflow. Commander observed: "many sections aren't updated" because AI wasn't parsing stale section reports or updating them.

**Root Cause:**
- verify_timestamps.py output was human-readable text, not machine-readable
- AI had to manually inspect console output to find stale sections
- No structured task list for AI to process
- Protocol didn't explicitly document AI's role in updating stale sections

**Solution Implemented:**

**1. Machine-Readable Stale Section Reports**
- Added `--json` flag to verify_timestamps.py
- Outputs structured JSON: `{"stale_sections": [...], "health_percentage": 75.0}`
- JSON saved to: Research/.cache/stale_sections_YYYY-MM-DD.json

**2. Workflow Integration**
- Modified run_workflow.py Phase 4.5 to save JSON output automatically
- Console message: "[AI TASK LIST] Read: Research/.cache/stale_sections_2025-10-21.json"
- AI now has explicit file to read for task list

**3. Protocol Documentation**
- Expanded "WINGMAN DASH" section in Journal_Trading_Partner_Protocol.txt
- Added 6-phase detailed execution protocol:
  - Phase 1: Run automated scripts
  - Phase 2: Parse stale section JSON (AI reads task list)
  - Phase 3: Update each stale section (AI curates content)
  - Phase 4: Re-verify timestamps (AI confirms 100% current)
  - Phase 5: Portfolio advisor
  - Phase 6: Report completion
- Explicit instructions: "AI CRITICAL - MANDATORY" for phases 2-4

**4. Section Update Guidance**
- Protocol now documents what each section type requires:
  - sentimentCards: Tone matching signal tier
  - quickActions: CRITICAL - must match tier guidance
  - All aiInterpretations: Fresh narratives with TODAY's data
- References AI_NARRATIVE_UPDATE_INSTRUCTIONS.md for detailed guidance

**Files Modified:**
1. NEW FLAG: `scripts/utilities/verify_timestamps.py` (--json option)
2. UPDATED: `scripts/automation/run_workflow.py` (Phase 4.5 JSON save)
3. UPDATED: `Toolbox/INSTRUCTIONS/Domains/Journal_Trading_Partner_Protocol.txt` (detailed execution protocol)
4. UPDATED: `Toolbox/INSTRUCTIONS/Research/How_to_use_MP_CLAUDE_ONLY.txt` (Step 7 AI automation note)

**Command Flow (Before):**
```
User: "wingman dash"
→ AI runs scripts
→ Scripts report stale sections (text output)
→ AI sees warnings
→ AI reports completion ❌ (stale sections ignored)
```

**Command Flow (After):**
```
User: "wingman dash"
→ AI runs scripts
→ Scripts save stale_sections_2025-10-21.json
→ AI reads JSON: ["sentimentCardsUpdated", "quickActionsUpdated"]
→ AI updates those 2 sections with fresh content
→ AI re-verifies timestamps (all current)
→ AI reports: "Dashboard updated. Health: 100%." ✅
```

**Rationale:**
- Automation enables AI to systematically process stale sections
- JSON format eliminates ambiguity (no text parsing needed)
- Explicit protocol prevents AI from skipping curation steps
- Health percentage provides objective completion metric
- Re-verification ensures nothing missed

**Expected Behavior:**
- If 0 stale sections: 5 min total (scripts only)
- If 3-5 stale sections: 20-25 min (scripts + light curation)
- If 10-15 stale sections: 45-60 min (scripts + full curation)
- All sections 100% current when complete

**Key Success Metric:** Dashboard health percentage = 100% at completion

---

## Phase 1: Command Center Dashboard Creation

### Decision 1.1: Replace Journal with Command Center
**Date:** 2025-10-19 - Message 1-3
**Decision:** Traditional journal structure inadequate for real-time trading operations
**Action Taken:**
- Created `Journal/COMMAND_CENTER.md` (markdown reference)
- Created `Journal/command-center.html` (interactive visual dashboard)
- Theme: Military/aviation command center (dark blue/cyan)
- Rationale: Visual dashboards provide faster threat assessment than text journals

### Decision 1.2: Theme & Styling (Initial)
**Date:** 2025-10-19 - Message 4
**Decision:** Dark blue/cyan color scheme matching tactical operations aesthetic
**Colors Selected:**
- Primary: #0a0e27 (deep blue)
- Accent 1: #00d4ff (bright cyan)
- Accent 2: #ff6b35 (orange warning)
- Text: #e6f1ff (pale blue)
- Neutral: #8892b0 (medium grey)
- Rationale: High contrast for fast visual scanning; military theme reinforces command structure

### Decision 1.3: Font Size Adjustment (Round 1)
**Date:** 2025-10-19 - Message 5
**User Feedback:** "everything is a little small"
**Action Taken:**
- h1: 28px → 42px (+50%)
- status-indicator: 14px → 18px
- panel-header: 16px → 20px (+25%)
- instrument-name: 13px → 16px (+23%)
- metric-value: 12px → 15px (+25%)
- signal-score: 32px → 48px (+50%)
- signal-tier: 18px → 24px (+33%)
- Rationale: Trading dashboard requires instant visual comprehension; larger fonts reduce cognitive load

### Decision 1.4: Text Color Brightness Adjustment
**Date:** 2025-10-19 - Message 5
**User Feedback:** "the grey is hard to read"
**Action Taken:**
- text-color: #e6f1ff → #ffffff (pure white, +20% brightness)
- neutral-color: #8892b0 → #b8c5d6 (brighter grey, +40% brightness)
- label-colors: Various increases (+10-15% brightness)
- line-height: 1.6 → 1.8 (better spacing)
- Rationale: WCAG contrast compliance; extended trading hours require minimal eye strain

---

## Phase 2: Prospecting Workflow Integration

### Decision 2.1: Conversation as Journal
**Date:** 2025-10-19 - Message 6
**Decision:** Convert daily conversation into trading journal instead of maintaining separate journal file
**Rationale:**
- Reduces context switching (one interface)
- Natural language capture of market observations
- Wingman provides real-time threat assessment
- Auto-wrap at EOD creates permanent record
**Action Taken:**
- Created `Research/AI/` folder as "research storage and build area"
- Created `Research/AI/2025-10-19_SESSION_SUMMARY.md` (daily prospecting canvas)
- Created `Journal/EOD_WRAP_HANDLER.md` (documentation of auto-wrap process)
- Created `Journal/PROSPECTING_WORKFLOW.md` (complete daily operations guide)

### Decision 2.2: Trade Recording Format
**Date:** 2025-10-19 - Message 6
**Format Standardized:**
```
[TICKER] [DIRECTION] [SIZE] @ [PRICE], stop [X], target [Y]
```
**Rationale:** Machine-readable format for automated parsing; compatible with journaling system
**Example:** `NVDA SHORT 100 @ 192.50, stop 194, target 188`

### Decision 2.3: EOD Automation Process
**Date:** 2025-10-19 - Message 6
**Seven-Step Process Defined:**
1. Collect all session data
2. Parse trade entries
3. Generate formatted journal entry
4. Append to `Journal/Journal.md`
5. Update `Journal/command-center.html` (reset for next day)
6. Log entry to index
7. Reset `.session_state.json` for next session
**Rationale:** Eliminates manual journal entry creation; ensures data consistency

---

## Phase 3: Planners Integration (Weekly + Daily)

### Decision 3.1: Rename Daily Planner Tab to "Planners"
**Date:** 2025-10-19 - Message 9
**Decision:** Expand "Daily Planner" tab scope to include both weekly and daily planning
**Action Taken:**
- Identified `master-plan/research-dashboard.html` as integration point
- Planned: Rename tab from "Daily Planner" to "Planners"
- Planned: Add two subsections:
  - Weekly Planner (reads from `Research/AI/[WEEK]_WEEKLY_METRICS.md`)
  - Daily Planner (reads from `Research/AI/[DATE]_DAILY_METRICS.md`)
**Rationale:** Single interface for viewing weekly strategy + daily execution

### Decision 3.2: Two-Tier Metrics System
**Date:** 2025-10-19 - Message 9
**Architecture Decision:**
- **Tier 1 (Weekly):** Comprehensive metrics collected Sunday morning
  - Signal progression (5-day trend)
  - Sentiment analysis (bullish/neutral/bearish)
  - Market structure (breadth, VIX, divergences)
  - Portfolio health (cash %, YTD, constraints)
  - Provider consensus (major narratives)
  - Economic calendar (week's events)
  - Trigger stack (3 trading ideas with R:R, probability)
  - Risk management (position sizing, max loss)
  - File: `Research/AI/[WEEK]_WEEKLY_METRICS.md`

- **Tier 2 (Daily):** Daily execution plan filtered from weekly
  - Today's 3 priorities (inherited from weekly trigger stack)
  - Key levels (support/resistance for day's setup)
  - Market signal status (current vs. Sunday's forecast)
  - Risk management (today's position limits)
  - Pre-market checklist
  - Trade execution log
  - EOD summary
  - File: `Research/AI/[DATE]_DAILY_METRICS.md`

**Rationale:** Weekly foundation prevents analysis drift; daily filters focus execution

### Decision 3.3: Create SUNDAY_WEEKLY_PLANNER.md
**Date:** 2025-10-19 - Message 8
**Five-Phase Ritual Designed:**
1. Context Load (5 min) - Verify master plan workflow, load dashboard
2. Metrics Collection (10 min) - Signal, sentiment, breadth, portfolio, consensus
3. Weekly Planning (15 min) - Calendar, setup identification, trigger stack, risk mgmt
4. Daily Prep Templates (5 min) - Create Mon-Fri daily planner templates
5. Execution Checklist (5 min) - Verify readiness for Monday
**Total Time:** ~40 minutes
**Output:** `Research/AI/[WEEK]_WEEKLY_METRICS.md`
**Rationale:** Structured Sunday prep prevents mid-week analysis paralysis

### Decision 3.4: Create Templates for Reusability
**Date:** 2025-10-19 - Message 10
**Files Created:**
- `Journal/DAILY_PLANNER_TEMPLATE.md` - Blueprint for daily files
- `Research/AI/2025-10-19_WEEKLY_METRICS.md` - Example completed file
- `Journal/PLANNERS_INTEGRATION_GUIDE.md` - Complete architecture documentation
**Rationale:** Templates reduce daily decision-making; examples clarify expected data structure

---

## Phase 4: Real-Time Trading Intelligence System

### Decision 4.1: Real-Time Analysis Engine Architecture
**Date:** 2025-10-19 - Message 11-12
**User Request:** Build system that analyzes tickers on-demand
**Architecture Designed:**
- **Input:** Ticker symbol (e.g., "analyze NVDA")
- **Process:**
  1. Fetch live price (Yahoo Finance API)
  2. Pull SPY/QQQ context (from loaded master-plan data)
  3. Check X sentiment (from morning scraper)
  4. Apply CMT TA rules (from Toolbox/Rules/)
  5. Web search for catalysts/news
  6. Calculate probability score (weighted formula)
- **Output:** BUY/WAIT/AVOID + full thesis + entry/stop/target levels
**Rationale:** One-sentence input, complete thesis output accelerates decision-making

### Decision 4.2: Probability Weighting Framework
**Date:** 2025-10-19 - Message 13
**Weights Determined:**
- Technical Analysis (CMT Level 2): 40%
- Market Context (breadth, SPY/QQQ, relative strength): 25%
- Sentiment (X posts, provider consensus): 15%
- Volume (profile, OI for options): 10%
- Seasonality (monthly, yearly, presidential, decadal patterns): 10%
**Rationale:** TA foundation (40%) since user is trained; market context prevents mean reversion blindness; sentiment as confirmation; volume as entry validation; seasonality as long-term bias
**Scoring Scale:** 0-100 → AVOID (0-33) / WAIT (34-66) / BUY (67-100)

### Decision 4.3: CMT Level 2 Standards Selection
**Date:** 2025-10-19 - Message 13
**Decision:** Use Chartered Market Technician Level 2 standards (not Level 1)
**Components:**
- Chart Patterns (H&S, triangles, channels, flags)
- Trend Analysis (HMA, moving averages, trend lines)
- Momentum Indicators (RSI, MACD, divergences)
- Volume Analysis (OBV, volume profile, volume by price)
- Support/Resistance (key levels, breakout zones, pivots)
**Rationale:** CMT Level 2 adds pattern recognition + divergence analysis; user specifically requested this standard

### Decision 4.4: Data Sources Confirmed
**Date:** 2025-10-19 - Message 13
**Live Prices:** Yahoo Finance API (free tier acceptable)
**Sentiment:** Existing X scraper system (owned by user)
**TA Rules:** CMT Level 2 standards (web research + user knowledge)
**Seasonality:** Web search for yearly, decade, presidential cycles
**Probabilistic Scoring:** Weighted formula (user unsure on initial weights, web search to refine)
**Rationale:** Free data sources minimize operational costs; leverage existing scraper; web-sourced historical patterns

---

## Phase 5: System Architecture Clarification

### Decision 5.1: "Matrix Upload" Concept
**Date:** 2025-10-19 - Message 14
**Decision:** Morning data collection → Processing → Wingman loads with full context
**User's Exact Words:** "We can kinda load up data into the persona like we load kung fu into neo's brain in the matrix"
**Implementation Pattern:**
1. Run `@Toolbox/INSTRUCTIONS/Research/How_to_use_Research.txt` → Collect intelligence
2. Run `@Toolbox/INSTRUCTIONS/Workflows/How_to_use_MP_CLAUDE_ONLY.txt` → Process data, update dashboard
3. Command "Load Wingman" → Matrix upload begins
4. Wingman ingests: Account state, rules, master-plan, dashboard, weekly/daily metrics, X sentiment
5. Wingman becomes "educated on the situation"
6. During day: Mention ticker → Wingman analyzes with full loaded context
**Rationale:** Prevents context loss between sessions; ensures analysis consistency; rules always applied

### Decision 5.2: Complete Morning Ritual Sequence
**Date:** 2025-10-19 - Message 16
**User Confirmed Exact Workflow:**
```
Step 1: @Toolbox/INSTRUCTIONS/Research/How_to_use_Research.txt
        → Collects data (X sentiment, RSS, YouTube, web search)

Step 2: @Toolbox/INSTRUCTIONS/Workflows/How_to_use_MP_CLAUDE_ONLY.txt
        → Processes data, adds AI insight
        → Updates: master-plan/master-plan.md
        → Updates: master-plan/research-dashboard.html

Step 3: "Load Wingman" (Matrix Upload)
        → Persona loads
        → Rules load
        → Data loads into LLM memory
        → "✓ Full context ingested. Ready to analyze tickers."

Step 4: During Day
        → User mentions ticker
        → Wingman analyzes using loaded rules + data
        → Returns BUY/WAIT/AVOID + thesis

Step 5: EOD Wrap
        → "eod wrap" command
        → Wingman auto-generates journal entry
        → Updates dashboard + account state
```
**Rationale:** User explicitly confirmed this architecture; it's the complete vision

---

## Phase 6: Rule-Based Trading System

### Decision 6.1: Toolbox/Rules Folder Structure
**Date:** 2025-10-19 - Message 12
**User Request:** "tackle the trading system" with rule tracking
**Architecture Designed:**
```
Toolbox/Rules/
├── CMT_Level_2_TA_Rules.md             [TA standards]
├── Seasonality_Database.md             [Historical patterns]
├── Probability_Scoring_Framework.md    [Weighting system]
└── Risk_Management_Rules.md            [Position sizing, stops]
```
**Load Mechanism:** Rules loaded when "Load Wingman" executes
**Application:** All trade ideas automatically evaluated against rules (no manual lookup)
**Rationale:** Centralized rule repository prevents analyst bias; automatic rule application ensures consistency

### Decision 6.2: When Wingman Loads
**Date:** 2025-10-19 - Message 12
**Decision:** Rules auto-load along with Wingman persona
**Process:**
1. "Load Wingman" command issued
2. System reads all Rule files
3. Rules indexed into decision engine
4. CMT standards available for all analysis
5. Seasonality patterns cached
6. Probability weights initialized
**Rationale:** Rules integrated into persona prevents external lookup; faster analysis

---

## Phase 7: Integration of All Components

### Decision 7.1: System as Single Coherent Unit
**Date:** 2025-10-19 - Message 15-16
**Vision Clarified:** All components work together as integrated system
**Data Flow:**
```
Raw Market Intelligence
        ↓
Morning Data Scraping
        ↓
Master Plan Processing
        ↓
Research Dashboard Update
        ↓
Matrix Upload (Wingman Load)
        ↓
Full Context in LLM Memory
        ↓
Real-Time Analysis Engine Ready
        ↓
During Day: Ticker Mention → Instant Analysis
        ↓
EOD Wrap: Journal Generation + Dashboard Reset
```
**Key Insight:** No analysis happens in isolation; every decision references loaded rules and master plan data

---

## Implementation Status Summary

| Component | Status | Date Created | File(s) |
|-----------|--------|--------------|---------|
| Command Center Dashboard | ✅ COMPLETE | 2025-10-19 | COMMAND_CENTER.md, command-center.html |
| Prospecting Workflow | ✅ COMPLETE | 2025-10-19 | PROSPECTING_WORKFLOW.md, 2025-10-19_SESSION_SUMMARY.md |
| EOD Automation | ✅ COMPLETE | 2025-10-19 | EOD_WRAP_HANDLER.md |
| Sunday Weekly Planner | ✅ COMPLETE | 2025-10-19 | SUNDAY_WEEKLY_PLANNER.md |
| Weekly Metrics Template | ✅ COMPLETE | 2025-10-19 | 2025-10-19_WEEKLY_METRICS.md |
| Daily Planner Template | ✅ COMPLETE | 2025-10-19 | DAILY_PLANNER_TEMPLATE.md |
| Planners Integration Guide | ✅ COMPLETE | 2025-10-19 | PLANNERS_INTEGRATION_GUIDE.md |
| CMT TA Rules System | ⏳ PENDING | — | CMT_Level_2_TA_Rules.md |
| Seasonality Database | ⏳ PENDING | — | Seasonality_Database.md |
| Probability Framework | ⏳ PENDING | — | Probability_Scoring_Framework.md |
| Risk Management Rules | ⏳ PENDING | — | Risk_Management_Rules.md |
| Real-Time Analysis Engine | ⏳ PENDING | — | scripts/trading/analyze_ticker.py |
| Matrix Upload System | ⏳ PENDING | — | scripts/trading/matrix_upload.py |
| Planners Tab Integration | ⏳ PENDING | — | research-dashboard.html (edit) |

---

## Key Decisions Not Yet Made

1. **Optional Enhancement:** Should backtesting framework be included in Phase 2?
2. **Optional Enhancement:** Should machine learning weight adjustment be included in Phase 3?
3. **Optional Enhancement:** Should alert system for key level breaks be implemented?
4. **Technical Detail:** What is minimum probability threshold for trade execution (default: 60%)?
5. **Technical Detail:** What are position sizing formulas in risk management rules?

---

## Dependencies & Blockers

**Current:** None - All Phase 1 complete and ready for Phase 2

**Potential Phase 2 Blockers:**
- Yahoo Finance API rate limits (potential solution: upgrade to premium)
- X scraper data availability (depends on existing system)
- Web search integration (depends on API availability)

---

## Error History & Resolutions

### Error 1: File Edit Before Read
**Date:** 2025-10-19 - Message 8
**Issue:** Attempted to edit `SUNDAY_WEEKLY_PLANNER.md` without reading it first
**Error Message:** "File has not been read yet. Read it first before writing to it."
**Resolution:** Read file first (offset 75, limit 100), then executed edits successfully
**Lesson:** Always read files before editing in this API

### Error 2: Windows Path Formatting
**Date:** 2025-10-19 - Message 6
**Issue:** Bash commands failed with Windows backslash paths
**Error Message:** Path interpretation errors
**Resolution:** Converted to forward slashes: `c:\Users\` → `/c/Users/`
**Lesson:** Windows paths require escaping or conversion in bash context

---

## User Feedback Integration

| Feedback | Date | Response |
|----------|------|----------|
| "everything is a little small" | 2025-10-19 | Increased all font sizes by 25-50% |
| "the grey is hard to read" | 2025-10-19 | Brightened all text colors by 20-40% |
| "Do you understand your role?" | 2025-10-19 | Confirmed Wingman threat assessment, file updates, P&L tracking, record keeping |
| "I want to be able to wrap up this conversation and you will wrap the day up" | 2025-10-19 | Built EOD automation process |
| Clarified complete Matrix Upload pattern | 2025-10-19 | Confirmed understanding; documented complete workflow |

---

## Next Phase Recommendations

**Phase 2 (Rules & Real-Time Engine):**
1. Create CMT Level 2 TA Rules markdown with clear decision tree
2. Build Seasonality Database from web research
3. Implement Probability Scoring Framework (formula + examples)
4. Create Risk Management Rules (position sizing based on account size)
5. Develop Real-Time Analysis Engine (Python script)
6. Build Matrix Upload System (context loader)
7. Integrate Planners tab into research-dashboard.html
8. Manual testing with live tickers to validate scoring

**Estimated Phase 2 Duration:** 4-6 hours of AI development

---

## Technical Debt & Improvements

- **None currently** - Phase 1 architecture is clean and well-documented

---

## Sign-Off

**Phase 1 Complete:** 2025-10-19
**Handoff Status:** Documentation phase
**Next AI Contractor Start Point:** Create Toolbox/Rules/ files (Phase 2 beginning)
