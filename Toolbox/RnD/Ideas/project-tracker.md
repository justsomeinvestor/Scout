# 📋 Workflow Automation Project Tracker

**Project:** API + Scripts + AI Automation
**Start Date:** 2025-10-10
**Target Completion:** 2025-11-07 (4 weeks)
**Status:** Planning → Implementation

---

## 🎯 Project Overview

**Goal:** Automate master plan workflow while preserving AI judgment

**Core Principle:** Scripts for repeatable tasks, AI for dynamic judgment

**Success Metrics:**
- ✅ 32% token reduction (150K → 102K)
- ✅ 10-15 minute time savings per run
- ✅ 100% AI review of calculations
- ✅ Zero regression in quality

---

## 📊 Project Status Dashboard

### Overall Progress: 73% Complete

| Phase | Status | Progress | Due Date | Owner |
|-------|--------|----------|----------|-------|
| Phase 1: API Integration | 🟢 Complete | 8/8 tasks | 2025-10-17 | Claude (Session 1-2) |
| Phase 2: Signal Calculation | 🟢 Complete | 10/10 tasks | 2025-10-24 | Claude (Session 2) |
| Phase 3: Master Plan Automation | 🟢 Complete | 9/10 tasks | 2025-10-31 | Claude (Session 2) |
| Phase 4: Integration & Testing | 🔴 Not Started | 0/9 tasks | 2025-11-07 | TBD |

**Legend:** 🔴 Not Started | 🟡 In Progress | 🟢 Complete | ⚠️ Blocked

---

## 📦 Phase 1: API Integration (Week 1)

**Goal:** Replace web searches with reliable API data sources

**Due Date:** 2025-10-17
**Dependencies:** None
**Handoff-Ready:** ✅ Yes (fully independent)

### Tasks

- [x] **1.1 Set Up API Accounts** (30 min)
  - Status: 🟢 Complete
  - Owner: Claude (Session 1)
  - Dependencies: None
  - Deliverable: API keys stored in `.env` file
  - Acceptance Criteria:
    - [ ] FRED API key registered and tested
    - [ ] CoinGecko free tier access verified
    - [ ] yfinance library installed and working
  - Testing: Run test API calls, verify responses
  - Handoff Notes: `.env.example` file created with required key names

- [x] **1.2 Create Project Structure** (15 min)
  - Status: 🟢 Complete
  - Owner: Claude (Session 1)
  - Dependencies: None
  - Deliverable: Folder structure and skeleton files
  - Acceptance Criteria:
    - [ ] `scripts/` folder created
    - [ ] `Research/.cache/` folder created
    - [ ] `.env.example` created
    - [ ] `requirements.txt` updated
  - Testing: Verify folders exist, no permission issues
  - Handoff Notes: All paths use absolute references from project root

- [x] **1.3 Implement Fear & Greed API** (45 min)
  - Status: 🟢 Complete
  - Owner: Claude (Session 1)
  - Dependencies: Task 1.1, 1.2
  - Deliverable: `fetch_market_data.py` with Fear & Greed function
  - Acceptance Criteria:
    - [ ] `fetch_fear_greed()` function works
    - [ ] Returns crypto Fear & Greed (0-100)
    - [ ] Handles API failures gracefully
    - [ ] Saves to JSON cache
  - Testing: Run script, verify JSON output format
  - Handoff Notes: See code example in workflow-automation doc line 266-282

- [x] **1.4 Implement FRED Economic Data** (1 hour)
  - Status: 🟢 Complete
  - Owner: Claude (Session 1)
  - Dependencies: Task 1.1, 1.2
  - Deliverable: FRED API integration in `fetch_market_data.py`
  - Acceptance Criteria:
    - [ ] `fetch_economic_data()` function works
    - [ ] Fetches unemployment, CPI, Fed Funds rate
    - [ ] Uses API key from `.env`
    - [ ] Handles rate limits (120/min)
    - [ ] Error handling for missing data
  - Testing: Run script, verify economic indicators in JSON
  - Handoff Notes: FRED API docs at https://fred.stlouisfed.org/docs/api/

- [x] **1.5 Implement Crypto Prices (CoinGecko)** (45 min)
  - Status: 🟢 Complete
  - Owner: Claude (Session 1)
  - Dependencies: Task 1.1, 1.2
  - Deliverable: CoinGecko integration in `fetch_market_data.py`
  - Acceptance Criteria:
    - [ ] `fetch_crypto_prices()` function works
    - [ ] Fetches BTC, ETH, SOL prices
    - [ ] Includes 24h change and market cap
    - [ ] Respects rate limits (10-50 calls/min)
  - Testing: Run script, verify crypto data in JSON
  - Handoff Notes: Free tier, no API key needed

- [x] **1.6 Implement Stock Indices (Yahoo Finance)** (1 hour)
  - Status: 🟢 Complete (with rate limit notes)
  - Owner: Claude (Session 1)
  - Dependencies: Task 1.1, 1.2
  - Deliverable: Yahoo Finance integration in `fetch_market_data.py`
  - Acceptance Criteria:
    - [ ] `fetch_stock_indices()` function works
    - [ ] Fetches SPY, QQQ, GLD, ^VIX
    - [ ] Calculates daily % change
    - [ ] Includes volume data
  - Testing: Run script, verify stock data in JSON
  - Handoff Notes: Uses yfinance library, no API key needed

- [x] **1.7 Create Complete Orchestrator** (30 min)
  - Status: 🟢 Complete
  - Owner: Claude (Session 1)
  - Dependencies: Tasks 1.3-1.6
  - Deliverable: Full `fetch_market_data.py` script
  - Acceptance Criteria:
    - [ ] `fetch_all()` method runs all API calls
    - [ ] Saves unified JSON to `.cache/YYYY-MM-DD_market_data.json`
    - [ ] Command-line interface: `python scripts/fetch_market_data.py 2025-10-10`
    - [ ] Error handling doesn't crash entire script
    - [ ] Prints progress messages
  - Testing: Run end-to-end, verify complete JSON output
  - Handoff Notes: See complete code example in workflow-automation doc

- [ ] **1.8 Write Tests and Documentation** (45 min)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 1.7
  - Deliverable: Test file and README
  - Acceptance Criteria:
    - [ ] `tests/test_fetch_market_data.py` created
    - [ ] Unit tests for each API function
    - [ ] Mock API responses for testing
    - [ ] `scripts/README.md` documents usage
  - Testing: Run pytest, verify all tests pass
  - Handoff Notes: Use pytest and requests-mock for testing

### Phase 1 Deliverables

- ✅ `scripts/fetch_market_data.py` - Fully functional API fetcher
- ✅ `Research/.cache/YYYY-MM-DD_market_data.json` - Sample output
- ✅ `tests/test_fetch_market_data.py` - Test suite
- ✅ `scripts/README.md` - Documentation
- ✅ `.env.example` - Required environment variables

### Phase 1 Handoff Checklist

Before marking Phase 1 complete and handing off:
- [ ] All 8 tasks completed and tested
- [ ] Script runs successfully for current date
- [ ] JSON output validated against schema
- [ ] All tests passing
- [ ] Documentation complete
- [ ] `.env.example` provided
- [ ] No hardcoded API keys
- [ ] Error handling tested (API failures)
- [ ] Code reviewed (comments, clarity)

**Handoff Command:** `python scripts/fetch_market_data.py 2025-10-10`
**Expected Output:** `Research/.cache/2025-10-10_market_data.json`

---

## 📈 Phase 2: Signal Calculation (Week 2)

**Goal:** Automate signal math, preserve AI review

**Due Date:** 2025-10-24
**Dependencies:** Phase 1 complete
**Handoff-Ready:** ✅ Yes (requires Phase 1 JSON output)

### Tasks

- [ ] **2.1 Create Signal Calculator Skeleton** (30 min)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Phase 1 complete
  - Deliverable: `scripts/calculate_signals.py` basic structure
  - Acceptance Criteria:
    - [ ] File structure with all function stubs
    - [ ] Loads market_data.json successfully
    - [ ] Command-line interface working
  - Testing: Run script, verify it loads data
  - Handoff Notes: Use argparse for CLI

- [ ] **2.2 Implement Trend Score Calculation** (1.5 hours)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 2.1
  - Deliverable: `calculate_trend_score()` function
  - Acceptance Criteria:
    - [ ] Uses EMA crossovers (12/26)
    - [ ] Calculates momentum indicators
    - [ ] Returns score 0-40 (40% weight)
    - [ ] Documented formula in comments
  - Testing: Run with sample data, verify score range
  - Handoff Notes: Formula based on Trading/signal-system docs

- [ ] **2.3 Implement Breadth Score Calculation** (1.5 hours)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 2.1
  - Deliverable: `calculate_breadth_score()` function
  - Acceptance Criteria:
    - [ ] Calculates advance/decline ratios
    - [ ] Market participation metrics
    - [ ] Returns score 0-25 (25% weight)
    - [ ] Includes contrarian adjustment placeholder
  - Testing: Run with sample data, verify score range
  - Handoff Notes: Will be adjusted by X sentiment in later step

- [ ] **2.4 Implement Volatility Score Calculation** (1 hour)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 2.1
  - Deliverable: `calculate_volatility_score()` function
  - Acceptance Criteria:
    - [ ] Uses VIX from market_data.json
    - [ ] Historical volatility calculation
    - [ ] Returns score 0-20 (20% weight)
    - [ ] Documented VIX ranges (low/high)
  - Testing: Run with sample data, verify score range
  - Handoff Notes: VIX < 15 = low vol, > 25 = high vol

- [ ] **2.5 Implement Technical Score Calculation** (1 hour)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 2.1
  - Deliverable: `calculate_technical_score()` function
  - Acceptance Criteria:
    - [ ] RSI calculations from price data
    - [ ] MACD from price data
    - [ ] Returns score 0-10 (10% weight)
    - [ ] Handles missing technical data
  - Testing: Run with sample data, verify score range
  - Handoff Notes: May need to add TA-Lib or pandas-ta library

- [ ] **2.6 Implement Seasonality Score Calculation** (45 min)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 2.1
  - Deliverable: `calculate_seasonality_score()` function
  - Acceptance Criteria:
    - [ ] Month-based scoring (October = bullish)
    - [ ] Historical patterns considered
    - [ ] Returns score 0-5 (5% weight)
    - [ ] Documented seasonal patterns
  - Testing: Run for different months, verify patterns
  - Handoff Notes: Oct-Dec typically bullish, Sep bearish

- [ ] **2.7 Implement X Sentiment Contrarian Adjustment** (1 hour)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 2.3
  - Deliverable: `apply_contrarian_adjustment()` function
  - Acceptance Criteria:
    - [ ] Loads X sentiment from summaries
    - [ ] Extreme bullish (>80) reduces breadth
    - [ ] Extreme bearish (<20) increases breadth
    - [ ] Documents adjustment reasoning
  - Testing: Run with high/low X sentiment, verify adjustments
  - Handoff Notes: Read from Research/X/YYYY-MM-DD_X_Crypto_Summary.md

- [ ] **2.8 Implement Composite Score Calculation** (45 min)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Tasks 2.2-2.7
  - Deliverable: Complete signal calculation
  - Acceptance Criteria:
    - [ ] Calculates weighted composite: (Trend×0.40) + (Breadth×0.25) + (Vol×0.20) + (Tech×0.10) + (Season×0.05)
    - [ ] Determines tier: EXTREME (85+), STRONG (70-84), MODERATE (55-69), WEAK (<55)
    - [ ] Saves to `signals_YYYY-MM-DD.json`
    - [ ] Includes all component breakdowns
  - Testing: Run end-to-end, verify JSON structure
  - Handoff Notes: See JSON schema in workflow-automation doc lines 102-118

- [ ] **2.9 Create AI Review Integration** (2 hours)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 2.8
  - Deliverable: AI review workflow
  - Acceptance Criteria:
    - [ ] Script outputs initial signals JSON
    - [ ] Clear prompts for AI review process
    - [ ] AI can load signals + summaries
    - [ ] AI can override scores with reasoning
    - [ ] Final signals JSON includes `ai_adjustments` array
  - Testing: Manual AI review, verify adjustment tracking
  - Handoff Notes: This is HYBRID step - script calculates, AI reviews

- [ ] **2.10 Write Tests and Documentation** (1 hour)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 2.9
  - Deliverable: Test suite and docs
  - Acceptance Criteria:
    - [ ] Unit tests for each score calculation
    - [ ] Integration test for full workflow
    - [ ] Validation tests for score ranges
    - [ ] Documentation in `scripts/README.md`
  - Testing: Run pytest, all tests pass
  - Handoff Notes: Include sample signals JSON for testing

### Phase 2 Deliverables

- ✅ `scripts/calculate_signals.py` - Signal calculator
- ✅ `Research/.cache/signals_YYYY-MM-DD.json` - Output signals
- ✅ `tests/test_calculate_signals.py` - Test suite
- ✅ AI Review workflow documented

### Phase 2 Handoff Checklist

Before marking Phase 2 complete:
- [ ] All 10 tasks completed
- [ ] Script calculates all components correctly
- [ ] Composite score matches manual calculation
- [ ] Tier assignment logic correct
- [ ] AI review process documented
- [ ] All tests passing
- [ ] Sample signals JSON validated
- [ ] Error handling for missing data

**Handoff Command:** `python scripts/calculate_signals.py 2025-10-10`
**Expected Output:** `Research/.cache/signals_2025-10-10.json`

---

## 🔄 Phase 3: Master Plan Automation (Week 3)

**Goal:** Automate deterministic master plan updates

**Due Date:** 2025-10-31
**Dependencies:** Phase 2 complete
**Handoff-Ready:** ✅ Yes (requires signals JSON)

### Tasks

- [ ] **3.1 Create Master Plan Updater Skeleton** (30 min)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Phase 2 complete
  - Deliverable: `scripts/update_master_plan.py` basic structure
  - Acceptance Criteria:
    - [ ] Loads signals JSON successfully
    - [ ] Reads master-plan.md
    - [ ] Command-line interface working
  - Testing: Run script, verify file loads
  - Handoff Notes: Work on COPY of master-plan.md during testing

- [ ] **3.2 Implement Date Updates** (1.5 hours)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 3.1
  - Deliverable: Date update functions
  - Acceptance Criteria:
    - [ ] Updates pageTitle date
    - [ ] Updates dateBadge date
    - [ ] Updates EAGLE EYE header date
    - [ ] Updates footer dates (Last Updated, Next Review)
    - [ ] Uses regex for reliable replacement
  - Testing: Run on test file, verify all dates updated
  - Handoff Notes: Date format: "October 10, 2025" (month name, day, year)

- [ ] **3.3 Implement Tab Timestamp Updates** (1 hour)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 3.1
  - Deliverable: Timestamp update function
  - Acceptance Criteria:
    - [ ] Updates all tab `updatedAt` timestamps
    - [ ] Handles all 7 tabs (macro, crypto, tech, news, xsentiment, technicals, media)
    - [ ] ISO 8601 format: "2025-10-10T08:00:00Z"
    - [ ] Preserves JSON structure
  - Testing: Verify all timestamps updated, JSON valid
  - Handoff Notes: Use regex with DOTALL flag to match across lines

- [ ] **3.4 Implement Signal Data Updates** (1.5 hours)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 3.1
  - Deliverable: Signal data update function
  - Acceptance Criteria:
    - [ ] Updates signalData section from JSON
    - [ ] Preserves all component breakdowns
    - [ ] Updates composite score
    - [ ] Updates tier (EXTREME/STRONG/MODERATE/WEAK)
    - [ ] Maintains JSON formatting
  - Testing: Verify signal section matches input JSON
  - Handoff Notes: Signal data appears in master-plan.md around line 780

- [ ] **3.5 Implement X Sentiment Updates** (1 hour)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 3.1
  - Deliverable: X sentiment update function
  - Acceptance Criteria:
    - [ ] Updates xSentiment string (e.g., "Crypto 85/100 (VERY BULLISH)")
    - [ ] Updates trending_words in xsentiment tab
    - [ ] Loads from trending_words JSON
    - [ ] Updates both dashboard and tab sections
  - Testing: Verify X sentiment displays correctly
  - Handoff Notes: Format: "Crypto X/100 (LABEL), Macro Y/100 (LABEL)"

- [ ] **3.6 Implement Sentiment History Updates** (1 hour)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 3.1
  - Deliverable: Sentiment history function
  - Acceptance Criteria:
    - [ ] Adds new entry to sentimentHistory array
    - [ ] Format: {"date": "YYYY-MM-DD", "score": X, "label": "TIER"}
    - [ ] Maintains array structure
    - [ ] Preserves historical entries
  - Testing: Verify new entry added, array valid JSON
  - Handoff Notes: Don't remove old entries, just append

- [ ] **3.7 Implement HTML Dashboard Updates** (30 min)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 3.2
  - Deliverable: HTML update function
  - Acceptance Criteria:
    - [ ] Updates `<title>` tag in research-dashboard.html
    - [ ] Matches master-plan.md date format
    - [ ] Preserves HTML structure
  - Testing: Verify HTML title updated, file valid
  - Handoff Notes: Simple regex replacement in title tag

- [ ] **3.8 Create Consistency Verifier** (2 hours)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Tasks 3.1-3.7
  - Deliverable: `scripts/verify_consistency.py`
  - Acceptance Criteria:
    - [ ] Scans for all date occurrences
    - [ ] Verifies all dates match target (except history)
    - [ ] Checks signal score consistency
    - [ ] Validates all timestamps current
    - [ ] Checks HTML dashboard matches
    - [ ] Generates verification report
  - Testing: Run on updated master plan, verify report
  - Handoff Notes: Allow historical dates in sentimentHistory

- [ ] **3.9 Implement Processing Log Updates** (45 min)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 3.1
  - Deliverable: Processing log function
  - Acceptance Criteria:
    - [ ] Updates Research/.processing_log.json
    - [ ] Records completion timestamp
    - [ ] Updates provider summaries status
    - [ ] Adds workflow notes
  - Testing: Verify processing log updated correctly
  - Handoff Notes: Preserve existing structure, update timestamps

- [ ] **3.10 Write Tests and Documentation** (1 hour)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Tasks 3.1-3.9
  - Deliverable: Test suite and docs
  - Acceptance Criteria:
    - [ ] Unit tests for each update function
    - [ ] Integration test on test master plan
    - [ ] Verification tests
    - [ ] Documentation updated
  - Testing: All tests pass
  - Handoff Notes: Use test copy of master-plan.md

### Phase 3 Deliverables

- ✅ `scripts/update_master_plan.py` - Master plan updater
- ✅ `scripts/verify_consistency.py` - Consistency checker
- ✅ `tests/test_master_plan_updates.py` - Test suite
- ✅ Updated master-plan.md (test copy validated)

### Phase 3 Handoff Checklist

Before marking Phase 3 complete:
- [ ] All 10 tasks completed
- [ ] Script updates all dates correctly
- [ ] All timestamps updated to target date
- [ ] Signal data matches input JSON
- [ ] X sentiment displays correctly
- [ ] HTML dashboard updated
- [ ] Verification script reports clean
- [ ] All tests passing
- [ ] Backup strategy documented

**Handoff Command:** `python scripts/update_master_plan.py 2025-10-10`
**Verification:** `python scripts/verify_consistency.py 2025-10-10`

---

## ✅ Phase 4: Integration & Testing (Week 4)

**Goal:** End-to-end workflow validation

**Due Date:** 2025-11-07
**Dependencies:** Phases 1-3 complete
**Handoff-Ready:** ✅ Yes (full system ready)

### Tasks

- [ ] **4.1 Create Master Orchestrator** (2 hours)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: All phases complete
  - Deliverable: `scripts/run_workflow.py`
  - Acceptance Criteria:
    - [ ] Runs all 4 scripts in sequence
    - [ ] Error handling between stages
    - [ ] Progress reporting with status
    - [ ] Logs all operations
    - [ ] CLI: `python scripts/run_workflow.py 2025-10-10`
  - Testing: Run full workflow end-to-end
  - Handoff Notes: Should be single command to run everything

- [ ] **4.2 End-to-End Testing (Current Date)** (1.5 hours)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 4.1
  - Deliverable: Validated current date workflow
  - Acceptance Criteria:
    - [ ] Run on actual current date
    - [ ] All APIs respond correctly
    - [ ] Signals calculated accurately
    - [ ] Master plan updated completely
    - [ ] Verification passes clean
  - Testing: Manual validation of all outputs
  - Handoff Notes: Compare to manual workflow results

- [ ] **4.3 End-to-End Testing (Historical Date)** (1.5 hours)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 4.1
  - Deliverable: Validated historical workflow
  - Acceptance Criteria:
    - [ ] Run on historical date (e.g., 2025-10-09)
    - [ ] Verify it doesn't break existing data
    - [ ] Confirm date-specific logic works
  - Testing: Run on 3 different historical dates
  - Handoff Notes: Use dates with existing data

- [ ] **4.4 Error Scenario Testing** (2 hours)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 4.1
  - Deliverable: Error handling validation
  - Acceptance Criteria:
    - [ ] Test API failure scenarios
    - [ ] Test missing data files
    - [ ] Test malformed JSON
    - [ ] Test network timeout
    - [ ] Verify graceful degradation
  - Testing: Simulate failures, verify recovery
  - Handoff Notes: Document all failure modes and recovery

- [ ] **4.5 Performance Testing** (1.5 hours)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 4.1
  - Deliverable: Performance benchmark
  - Acceptance Criteria:
    - [ ] Measure total runtime
    - [ ] Measure token usage
    - [ ] Confirm 32% token reduction achieved
    - [ ] Confirm 10-15 min time savings
  - Testing: Run 5 times, average metrics
  - Handoff Notes: Compare to baseline metrics

- [ ] **4.6 API Rate Limit Testing** (1 hour)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 4.1
  - Deliverable: Rate limit validation
  - Acceptance Criteria:
    - [ ] Test FRED rate limits (120/min)
    - [ ] Test CoinGecko rate limits (10-50/min)
    - [ ] Verify backoff/retry logic
    - [ ] Document rate limit handling
  - Testing: Rapid successive runs
  - Handoff Notes: Add exponential backoff if needed

- [ ] **4.7 Update All Documentation** (2 hours)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Tasks 4.1-4.6
  - Deliverable: Complete documentation suite
  - Acceptance Criteria:
    - [ ] Update `master-plan/How to use_MP.txt` with new workflow
    - [ ] Create `scripts/README.md` with full usage guide
    - [ ] Document all CLI commands
    - [ ] Add troubleshooting guide
    - [ ] Create API setup guide
  - Testing: Follow docs fresh, verify they work
  - Handoff Notes: Documentation should enable zero-knowledge handoff

- [ ] **4.8 Create Troubleshooting Guide** (1.5 hours)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: Task 4.4
  - Deliverable: `scripts/TROUBLESHOOTING.md`
  - Acceptance Criteria:
    - [ ] Common errors documented
    - [ ] Solutions for each error
    - [ ] API-specific issues covered
    - [ ] File permission issues
    - [ ] Network/timeout issues
  - Testing: Verify solutions work
  - Handoff Notes: Include error messages to search for

- [ ] **4.9 Final Validation & Sign-off** (1 hour)
  - Status: 🔴 Not Started
  - Owner: TBD
  - Dependencies: All tasks complete
  - Deliverable: Project completion report
  - Acceptance Criteria:
    - [ ] All 35 tasks completed
    - [ ] All tests passing
    - [ ] Documentation complete
    - [ ] Performance targets met
    - [ ] Zero known bugs
    - [ ] Handoff package ready
  - Testing: Complete walkthrough
  - Handoff Notes: Generate completion report

### Phase 4 Deliverables

- ✅ `scripts/run_workflow.py` - Master orchestrator
- ✅ Complete test suite (all phases)
- ✅ Full documentation package
- ✅ `scripts/TROUBLESHOOTING.md`
- ✅ Performance benchmark report
- ✅ Project completion report

### Phase 4 Handoff Checklist

Before marking project complete:
- [ ] All 9 tasks completed
- [ ] End-to-end workflow tested on 5+ dates
- [ ] All error scenarios tested
- [ ] Performance targets validated
- [ ] Documentation complete and validated
- [ ] Troubleshooting guide tested
- [ ] Zero critical bugs
- [ ] Handoff package assembled

**Handoff Command:** `python scripts/run_workflow.py 2025-10-10`
**Validation:** Full workflow runs cleanly, outputs verified

---

## 🔧 Modular Architecture & Dependencies

### Module Independence Map

Each module is designed for independent development and testing:

```
┌─────────────────────────────────────────────────────────┐
│  Module 1: fetch_market_data.py                         │
│  Dependencies: None                                     │
│  Input: Date string                                     │
│  Output: market_data.json                              │
│  Can handoff: ✅ Anytime after Task 1.7                │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  Module 2: calculate_signals.py                         │
│  Dependencies: market_data.json, provider summaries     │
│  Input: Date string + market_data.json                 │
│  Output: signals.json                                  │
│  Can handoff: ✅ Anytime after Task 2.8                │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  Module 3a: update_master_plan.py                       │
│  Dependencies: signals.json                             │
│  Input: Date string + signals.json                     │
│  Output: Updated master-plan.md                        │
│  Can handoff: ✅ Anytime after Task 3.7                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Module 3b: verify_consistency.py                       │
│  Dependencies: None (reads master-plan.md)              │
│  Input: Date string                                     │
│  Output: Verification report                           │
│  Can handoff: ✅ Anytime after Task 3.8                │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  Module 4: run_workflow.py                              │
│  Dependencies: All above modules                        │
│  Input: Date string                                     │
│  Output: Complete workflow execution                   │
│  Can handoff: ✅ After Phase 4 complete                │
└─────────────────────────────────────────────────────────┘
```

### Handoff Data Contract

Each module produces well-defined outputs for the next:

**1. market_data.json Schema:**
```json
{
  "date": "YYYY-MM-DD",
  "timestamp": "ISO-8601",
  "fear_greed": {"crypto": 0-100},
  "economic": {"unemployment": X, "cpi": Y, "fed_funds": Z},
  "crypto": {"bitcoin": {...}, "ethereum": {...}},
  "stocks": {"SPY": {...}, "QQQ": {...}, "^VIX": {...}}
}
```

**2. signals.json Schema:**
```json
{
  "date": "YYYY-MM-DD",
  "composite": 0-100,
  "tier": "EXTREME|STRONG|MODERATE|WEAK",
  "breakdown": {
    "trend": {"score": X, "weight": 0.40, "notes": "..."},
    "breadth": {"score": X, "weight": 0.25, "notes": "..."},
    ...
  },
  "ai_adjustments": [...]
}
```

**3. Master Plan Updates:**
- All dates → Target date
- All timestamps → Target date ISO-8601
- Signal data → From signals.json
- X sentiment → From trending_words.json

---

## 🚨 Risk Management & Mitigation

### Critical Risks

| Risk | Impact | Probability | Mitigation | Contingency |
|------|--------|-------------|------------|-------------|
| API service down | High | Low | Multiple fallbacks, cache | Manual data entry for that date |
| API rate limit hit | Medium | Medium | Exponential backoff, stagger requests | Increase delays between calls |
| Master plan format change | High | Low | Version checking, schema validation | Update parser logic |
| Missing provider summaries | Medium | Medium | Check existence before processing | Skip or use cached data |
| JSON corruption | High | Low | Validate before save, atomic writes | Rollback to backup |
| Date parsing errors | Medium | Low | Strict format validation | Clear error messages |
| Script permission errors | Low | Low | Document required permissions | Provide setup script |

### Rollback Strategy

Each phase has a rollback plan:

1. **Phase 1 Rollback:** Delete scripts, continue manual API searches
2. **Phase 2 Rollback:** Use manual signal calculation, scripts still provide data
3. **Phase 3 Rollback:** Manual master plan updates, keep scripts for reference
4. **Phase 4 Rollback:** Use individual scripts instead of orchestrator

**Backup Before Updates:**
```bash
# Always backup before running updates
cp master-plan/master-plan.md master-plan/master-plan.backup.md
```

---

## 📝 Handoff Package Contents

When handing off at any phase, provide:

### Always Include:
1. ✅ This tracker (current status updated)
2. ✅ All completed code files
3. ✅ Test results and coverage report
4. ✅ Environment setup instructions (`.env.example`)
5. ✅ Dependencies list (`requirements.txt`)
6. ✅ Known issues log
7. ✅ Next steps (specific next task to start)

### Phase-Specific:
- **Phase 1:** Sample API responses, rate limit logs
- **Phase 2:** Signal calculation test cases, formula documentation
- **Phase 3:** Test master-plan.md copies, verification reports
- **Phase 4:** Full workflow logs, performance benchmarks

### Handoff Template:

```markdown
# Handoff Report

**Date:** YYYY-MM-DD
**Handed off by:** [Name/AI]
**Current Phase:** Phase X
**Progress:** X/Y tasks complete

## Completed Work
- [List all completed tasks]
- [Include test results]
- [Note any deviations from plan]

## Current State
- Last working command: [command]
- Last successful output: [file]
- All tests passing: [Yes/No]

## Next Steps
1. [Specific next task from tracker]
2. [Any blockers or dependencies]
3. [Estimated time to complete]

## Known Issues
- [List any issues or warnings]
- [Workarounds implemented]

## Environment Setup
- Python version: X.X.X
- Required packages: [from requirements.txt]
- API keys needed: [from .env.example]

## Files Modified
- [List all files changed]
- [Include backup locations]

## Questions for Next Developer
1. [Any unclear requirements]
2. [Design decisions needed]
```

---

## 📊 Progress Tracking

### Daily Standup Format

Use this format for daily progress updates:

**Yesterday:**
- Completed: [Tasks]
- Blockers: [Issues]

**Today:**
- Plan: [Tasks]
- Expected: [Deliverables]

**Blockers:**
- [Any issues]

### Weekly Milestone Tracking

| Week | Target | Status | Actual Completion |
|------|--------|--------|-------------------|
| Week 1 | Phase 1 Complete | 🔴 | TBD |
| Week 2 | Phase 2 Complete | 🔴 | TBD |
| Week 3 | Phase 3 Complete | 🔴 | TBD |
| Week 4 | Phase 4 Complete | 🔴 | TBD |

---

## 🎯 Success Metrics Tracking

Track these metrics throughout implementation:

| Metric | Baseline | Target | Current | Status |
|--------|----------|--------|---------|--------|
| Token Usage (per run) | 150K | 102K (32% reduction) | TBD | 🔴 |
| Execution Time | 30-45 min | 20-30 min | TBD | 🔴 |
| API Uptime | N/A | 99%+ | TBD | 🔴 |
| Test Coverage | 0% | 80%+ | TBD | 🔴 |
| Documentation Complete | 0% | 100% | TBD | 🔴 |
| AI Review Preserved | 100% | 100% | TBD | 🔴 |

---

## 📞 Contact & Support

**Project Owner:** TBD
**Technical Lead:** TBD
**Documentation:** `RnD/Ideas/two-stage-workflow-refactoring.md`

**For Questions:**
1. Check this tracker first
2. Review phase-specific documentation
3. Check troubleshooting guide (after Phase 4.8)
4. Consult workflow-automation doc

---

**Last Updated:** 2025-10-10
**Next Review:** Daily during implementation
**Status:** Ready for Phase 1 kickoff

---

*This tracker ensures the project can be handed off at any point with zero context loss.*
