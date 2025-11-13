# WINGMAN PREP OPTIMIZATION PLAN - October 30, 2025

**Status:** PLANNING PHASE (Ready for implementation)
**Last Updated:** 2025-10-30 15:45 UTC
**Session:** Claude Code - Oct 30 session

---

## EXECUTIVE SUMMARY

Optimization project to improve WINGMAN PREP workflow efficiency by replacing web searches with direct API calls and parallelizing provider summaries.

**Expected Impact:**
- PREP time reduction: 57-69 min → 20-28 min (60-65% faster)
- Token savings: ~12,000 tokens per run
- Quality: No degradation (same or better)
- Risk: LOW (all changes documented and reversible)

---

## PROJECT SCOPE

### Phase 1: Quick Wins (Implementation in progress)

**Three optimization changes:**

1. **Replace Web Searches with Direct API Calls**
   - Status: PLANNING
   - Scope: Create `scripts/prep/fetch_fresh_technical_data.py`
   - Calls: Finnhub (SPX), CoinGecko (BTC, ETH, SOL), Alternative.me (F&G), NYSE scraper (Breadth), Finnhub (VIX)
   - Impact: 17 minutes saved, fresh data guaranteed
   - Risk: LOW

2. **Add Solana to CoinGecko API**
   - Status: PLANNING
   - Scope: 1-line modification to CoinGecko call
   - Impact: 3 minutes saved
   - Risk: LOW

3. **Parallelize PREP Step 1 Provider Summaries**
   - Status: PLANNING
   - Scope: Update How_to_use_Research.txt to specify parallel Task execution
   - Impact: 32-34 minutes saved
   - Risk: LOW

---

## IMPLEMENTATION CHECKLIST

### Stage 1: Documentation Updates
- [ ] Update `Toolbox/INSTRUCTIONS/Research/How_to_use_Research.txt`
  - [ ] Step 1: Add parallel Task execution pattern for RSS, YouTube, Technical, X
  - [ ] Step 1.3: Replace web searches with "Call fetch_fresh_technical_data.py for current data"
  - [ ] Add fallback instructions if API calls fail

- [ ] Create `scripts/prep/fetch_fresh_technical_data.py` skeleton
  - [ ] Document API calls needed
  - [ ] Document JSON output structure
  - [ ] Document error handling

### Stage 2: Python Implementation
- [ ] Implement `scripts/prep/fetch_fresh_technical_data.py`
  - [ ] Finnhub: SPX price, 50/200 MA
  - [ ] CoinGecko: BTC, ETH, SOL prices
  - [ ] Alternative.me: Fear & Greed Index
  - [ ] NYSE scraper: Market Breadth (call existing scraper)
  - [ ] Finnhub: VIX current level
  - [ ] Return structured JSON matching signals calculator expectations

- [ ] Modify CoinGecko API call
  - [ ] Add 'solana' to crypto list
  - [ ] Verify SOL data in output

### Stage 3: Integration & Testing
- [ ] Test fetch_fresh_technical_data.py with live APIs
  - [ ] Verify all API calls succeed
  - [ ] Check data freshness (timestamps)
  - [ ] Validate JSON structure
  - [ ] Test fallback behavior if API fails

- [ ] Test parallel PREP Step 1 execution
  - [ ] Launch 4 Task agents simultaneously
  - [ ] Verify all complete without conflicts
  - [ ] Compare timing to sequential execution

- [ ] Full WINGMAN PREP workflow test
  - [ ] Run complete RECON → PREP → DASH cycle
  - [ ] Verify signals calculation produces output
  - [ ] Check dashboard update completes successfully
  - [ ] Confirm all 16+ research files created

- [ ] Quality validation
  - [ ] Compare signal scores to previous methodology
  - [ ] Verify no data gaps
  - [ ] Check for new errors or warnings

### Stage 4: Documentation & Deployment
- [ ] Update WINGMAN_WORKFLOW_GUIDE.txt with new timing expectations
- [ ] Document optimization changes in CHANGELOG
- [ ] Create rollback instructions (documented below)
- [ ] Deploy optimization and monitor for 3-5 trading days

---

## CURRENT STATE (Oct 30 Session)

### Where We Left Off
- ✅ Completed root cause analysis of data freshness failure
- ✅ Understood correct RECON → PREP → DASH architecture
- ✅ Completed comprehensive optimization research
- ✅ User approved optimization approach (API calls instead of web searches)
- ⚠️ **INCOMPLETE:** Bookmarks archived file missing (verification gate blocking WINGMAN PREP execution)
  - X/Twitter Bookmarks posts file exists (1 item)
  - X/Twitter Bookmarks archived file MISSING
  - Verification script exit code: 2 (INCOMPLETE)
  - User chose to defer and focus on optimization first

### Current Blocking Issue
- WINGMAN PREP verification gate failing due to missing X Bookmarks archived file
- Options:
  1. Re-run WINGMAN RECON (full scraper re-execution)
  2. Skip Bookmarks file (lose 1 bookmark data point)
  3. Implement optimization first, then re-run PREP

### Recommended Next Action
**Implement optimization first, THEN re-run full WINGMAN RECON to complete PREP workflow.**

This way:
1. Optimization is documented and ready for future use
2. Next PREP workflow will use new optimized approach
3. Fresh data collected with new optimized system

---

## TECHNICAL SPECIFICATIONS

### API Data Requirements

**What signals calculator NEEDS (from `calculate_signals.py`):**

```json
{
  "date": "2025-10-30",
  "spx": {
    "price": 6890.59,
    "ma_50": 6750.00,
    "ma_200": 6500.00,
    "rsi": 52
  },
  "btc": {
    "price": 109975,
    "ma_50": 108000,
    "ma_200": 95000,
    "rsi": 45
  },
  "sol": {
    "price": 192.45,
    "24h_change": 3.2
  },
  "breadth": {
    "pct_above_50dma": 57.25,
    "ad_ratio": 0.38
  },
  "volatility": {
    "vix": 18.5,
    "btc_iv_percentile": 58
  },
  "fear_greed": {
    "value": 39,
    "classification": "fear"
  }
}
```

### API Endpoints to Call

**Finnhub (existing, configured):**
- Endpoint: `/quote` - GET `/quote?symbol=SPX&token=XXX`
- Data: Current price for SPX
- Rate limit: 60 calls/min (free tier)

**Finnhub Candles (existing, configured):**
- Endpoint: `/stock/candle` - GET `/stock/candle?symbol=SPX&resolution=D&...&token=XXX`
- Data: OHLCV candles for MA/RSI calculation
- Note: May need to calculate 50/200 MA locally from candles

**CoinGecko (existing, configured):**
- Endpoint: `/simple/price` - GET `/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&...`
- Data: BTC, ETH, SOL prices, 24h change
- Rate limit: No auth needed for free tier

**Alternative.me (free, no auth):**
- Endpoint: `/fng/` - GET `/fng/?limit=1&format=json`
- Data: Fear & Greed Index value (0-100)
- Rate limit: Reasonable (no published limit)

**NYSE Market Breadth (scraper exists):**
- Method: Use existing `scrape_market_breadth.py` or call NYSE API directly
- Data: Advance/decline ratio, breadth thrust
- Timing: Will likely call existing scraper

**VIX (Finnhub):**
- Endpoint: `/quote` - GET `/quote?symbol=VIX&token=XXX`
- Data: Current VIX level
- Rate limit: 60 calls/min (same as SPX)

### Error Handling

If API calls fail:
1. **Primary source fails:** Use secondary source (fallback)
2. **All sources fail:** Log error and skip that metric
3. **Critical metric (SPX) fails:** Block PREP execution and report

Example fallback chain:
- SPX price: Finnhub → Alpha Vantage → Yahoo Finance
- BTC price: CoinGecko → Binance API → Fallback to previous value

---

## ROLLBACK PLAN

If issues arise during implementation:

### Rollback Step 1: Revert to Previous PREP Workflow
**Files to revert:**
1. `Toolbox/INSTRUCTIONS/Research/How_to_use_Research.txt`
   - Restore Step 1 instructions to sequential provider summaries
   - Restore Step 1.3 to web search instructions

2. Remove `scripts/prep/fetch_fresh_technical_data.py`
   - Delete new script if it exists
   - Return to web search approach

3. Revert CoinGecko call if modified
   - Remove 'solana' from crypto list if needed

**Expected outcome:** PREP returns to previous 57-69 minute execution time

### Rollback Step 2: Clear Optimization Changes
- Remove optimization documentation from CHANGELOG
- Revert any timing updates in workflow guides
- Reset to pre-optimization baseline

**Timeline for rollback:** ~5 minutes

---

## TESTING STRATEGY

### Pre-Deployment Testing (Current Session)

1. **Unit Test: API calls work**
   - [ ] Call each API individually
   - [ ] Verify JSON response structure
   - [ ] Check data freshness (timestamps)
   - [ ] Test error conditions (API down, rate limited, etc.)

2. **Integration Test: fetch_fresh_technical_data.py**
   - [ ] Run script standalone
   - [ ] Verify output JSON matches expected structure
   - [ ] Compare against signals calculator input requirements

3. **Workflow Test: Parallel Step 1**
   - [ ] Launch 4 Task agents simultaneously
   - [ ] Verify all complete without blocking each other
   - [ ] Measure actual time savings

### Post-Deployment Testing (Next 3-5 trading days)

1. **Daily Execution**
   - [ ] RECON → PREP → DASH cycle completes
   - [ ] All 16+ research files created successfully
   - [ ] Signals calculation produces output
   - [ ] Dashboard updates without errors

2. **Quality Comparison**
   - [ ] Signal scores similar to previous methodology
   - [ ] Key themes identify similar insights
   - [ ] No new errors or data gaps
   - [ ] API data freshness confirmed

3. **Performance Measurement**
   - [ ] PREP execution time (target: 20-28 min)
   - [ ] Token usage (target: 12K tokens saved)
   - [ ] Error rates (target: <1%)

---

## DOCUMENTATION CHANGES NEEDED

### Files to Update

1. **`Toolbox/INSTRUCTIONS/Research/How_to_use_Research.txt`**
   - Step 1: Add parallel execution pattern
   - Step 1.3: Replace web searches with API calls
   - Add new section: "API Call Best Practices"
   - Add error handling instructions

2. **`Toolbox/INSTRUCTIONS/Domains/WINGMAN_WORKFLOW_GUIDE.txt`**
   - Update PREP timing expectations: 57-69 min → 20-28 min
   - Add notes about API freshness vs. cached data
   - Document new parallel execution pattern

3. **Create new file: `scripts/prep/TECHNICAL_DATA_API_GUIDE.md`**
   - Document fetch_fresh_technical_data.py usage
   - Document API endpoints and rate limits
   - Document error handling and fallbacks

4. **Update `Toolbox/CHANGELOGS/CHANGELOG_2025-10-30.md`**
   - Log optimization implementation
   - Note API changes
   - Document testing results

---

## RISK ASSESSMENT

### Implementation Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| API rate limiting | Low | Medium | Implement backoff logic, monitor usage |
| API unavailability | Low | Medium | Fallback to cached data or previous values |
| Parallel execution conflicts | Low | Low | Use independent data sources, test thoroughly |
| Signals calculator incompatibility | Low | High | Validate JSON structure before deployment |
| Performance degradation | Very Low | Medium | Measure timing, have rollback ready |

### Quality Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Data freshness gaps | Low | Low | Verify timestamps, compare to previous methods |
| Missing data fields | Low | Medium | Comprehensive validation of JSON structure |
| Incomplete API responses | Low | Medium | Fallback to secondary source, log errors |

**Overall Risk Level: LOW** - All changes documented, reversible, with fallback strategies

---

## SUCCESS CRITERIA

✅ PREP completes in 20-28 minutes (down from 57-69 min)
✅ All 16+ research files created successfully
✅ Signals calculation produces valid output (composite score 0-100)
✅ Dashboard updates without errors
✅ Quality matches or exceeds previous runs (signal accuracy verified)
✅ No data gaps or missing fields
✅ API calls demonstrate fresh data (timestamps current)
✅ Parallel execution confirmed faster than sequential

---

## ESTIMATED TIMELINE

**Implementation Effort:**
- Documentation updates: 1-2 hours
- Python implementation: 2-3 hours
- Testing & validation: 2-3 hours
- Deployment & monitoring: 1-2 hours
- **Total: 6-10 hours** (can be split across sessions)

**Recommended Approach:**
1. Complete documentation & specification (this session) ✅
2. Implement Python script (next session)
3. Test with live APIs (next session)
4. Deployment & 3-day monitoring (after validation)

---

## SESSION CONTINUITY NOTES

### For Next Session (If Session Limit Reached)

**Status Summary:**
- Optimization plan documented and approved
- Research completed, specifications defined
- Ready to implement fetch_fresh_technical_data.py
- WINGMAN PREP blocked due to missing Bookmarks archive (not critical for optimization)

**Next Steps:**
1. Create `scripts/prep/fetch_fresh_technical_data.py`
2. Implement API calls per specification (see "API Endpoints to Call")
3. Test script with live APIs
4. Update How_to_use_Research.txt instructions
5. Run full RECON → PREP → DASH cycle to validate

**Files Changed This Session:**
- None (documentation only)

**Files To Change Next Session:**
- `scripts/prep/fetch_fresh_technical_data.py` (create new)
- `Toolbox/INSTRUCTIONS/Research/How_to_use_Research.txt` (update)
- `Toolbox/INSTRUCTIONS/Domains/WINGMAN_WORKFLOW_GUIDE.txt` (update)

**Questions for Next Session:**
- Should MA/RSI be calculated from Finnhub candles, or fetch from TradingView-like source?
- Acceptable latency for API calls (target: <2 sec per script execution)?
- Should we implement caching for error resilience, or fresh-only approach?

---

## APPROVAL & SIGN-OFF

**Plan Created By:** Wingman (Claude Code)
**Plan Approved By:** [User - trading decision maker]
**Date Approved:** 2025-10-30
**Status:** READY FOR IMPLEMENTATION

**Approval Note:** User confirmed preference for fresh API calls instead of cached data, approved all three optimization changes (API replacement, add SOL, parallelize Step 1).

---

**Document Revision History:**
- v1.0 (2025-10-30 15:45 UTC): Initial comprehensive plan created, all specifications documented, ready for next session implementation
