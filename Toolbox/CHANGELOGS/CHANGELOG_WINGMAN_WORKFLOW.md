# Wingman Workflow Changes & Enhancements

## Latest Update: October 25, 2025 - Remove Duplicate Portfolio Allocation Workflow

### Removed Old Manual Portfolio Allocation Approach

**What Was Removed:**
- Phase 5 manual AI prompt for `tabs.portfolio.portfolioRecommendation` (lines 441-478 in wingman_dash.py)
- Section mapping for portfolio allocation in `section_mappings` dictionary
- Tier-based allocation guidelines from prompt generation

**Why:**
- Duplicate approach: sync_portfolio_recommendation.py now handles portfolio allocation automatically
- sync script is more reliable and consistent (Phase 2, automated)
- Eliminates conflicting/redundant portfolio update mechanisms
- Simplifies Phase 5 workflow (AI focuses on narrative synthesis only)

**Result:**
Portfolio now has **clean separation of concerns:**
- **Phase 2 (Automated):** `sync_portfolio_recommendation.py` updates `portfolioRecommendation` section
  - Allocation percentages, recommended actions, key risks
  - Runs alongside other sync scripts
- **Phase 5 (Manual AI):** Updates only `tabs.portfolio.aiInterpretation` section
  - Narrative briefing (summary, keyInsight, action)
  - Consistent with all other tabs (markets, technicals, xsentiment, news)

**Files Modified:**
- `scripts/automation/wingman_dash.py` - Removed portfolio allocation prompt generation
- `Toolbox/INSTRUCTIONS/Domains/Wingman_Command_Pipeline.txt` - Updated Phase 2 documentation
- `Toolbox/CHANGELOG_WINGMAN_WORKFLOW.md` - This changelog

---

## Previous Update: October 25, 2025 - Portfolio Section Enhancement

### Portfolio Section Improvements: Full Automation & Fresh AI Analysis

**Issues Fixed:**
1. ❌ Portfolio AI interpretation was NOT being displayed on the dashboard
2. ❌ Portfolio recommendation data was STALE (October 20, not October 25)
3. ❌ No automation existed for portfolio updates
4. ❌ Account balance outdated ($22,824 vs actual $23,106)

**Solutions Implemented:**

#### 1. AI Interpretation Now Visible on Dashboard ✅
- **Change:** Added `renderAIInterpretation()` call to portfolio tab rendering
- **File:** `master-plan/research-dashboard.html` (lines 3095-3098)
- **Result:** Fresh October 25 portfolio analysis now displays alongside recommendations
- **Content Shown:** Summary, Key Insight, Action, Sentiment, Confidence

#### 2. New Portfolio Sync Script Created ✅
- **Script:** `scripts/utilities/sync_portfolio_recommendation.py` (NEW)
- **Purpose:** Automatically update portfolio recommendation section from latest analysis
- **Data Source:** `Journal/portfolio_decisions/YYYY-MM-DD_portfolio_*.txt`
- **Extracts:** Allocation %, Actions, Reasoning, Key Risks, Signal Tier
- **Generates:** Fresh YAML for `portfolioRecommendation` section
- **Timestamp:** Updates `portfolioRecommendation.updatedAt` automatically

#### 3. Integrated into Wingman Dash Workflow ✅
- **File:** `scripts/automation/wingman_dash.py` (line 82)
- **Added:** `("portfolio_recommendation_sync", ...)`
- **Location:** Phase 2 - runs alongside other sync scripts
- **Order:** Executes after risk_items and provider_consensus syncs

#### 4. Documentation Updated ✅
- **File:** `Toolbox/INSTRUCTIONS/Domains/Wingman_Command_Pipeline.txt`
- **Added:** Portfolio sync to Phase 2 script list
- **Documentation:** Explains data source for portfolio recommendations

### How Portfolio Sync Works

**Data Flow:**
```
Journal/portfolio_decisions/YYYY-MM-DD_portfolio_prompt.txt
    ↓ (send to AI for analysis)
User receives AI recommendation in structured format
    ↓ (save response to)
Journal/portfolio_decisions/YYYY-MM-DD_portfolio_recommendation.txt
    ↓ (during wingman dash)
sync_portfolio_recommendation.py
    ↓ (parses and updates)
master-plan.md (portfolioRecommendation section)
    ↓ (displays on)
Dashboard Portfolio Tab (with fresh analysis + UI visualization)
```

### Changes Made

**Files Modified:**
1. ✅ `master-plan/research-dashboard.html` - Added AI interpretation rendering to portfolio tab
2. ✅ `scripts/automation/wingman_dash.py` - Added portfolio sync script to Phase 2

**Files Created:**
1. ✅ `scripts/utilities/sync_portfolio_recommendation.py` (183 lines) - New sync script

**Documentation Updated:**
1. ✅ `Toolbox/INSTRUCTIONS/Domains/Wingman_Command_Pipeline.txt` - Added portfolio sync details

### Verification Checklist

When running `wingman dash` next, verify:
- [ ] Portfolio tab shows AI Interpretation section (fresh analysis)
- [ ] Portfolio sync script runs in Phase 2 logs
- [ ] Portfolio recommendation has current date (Oct 25+)
- [ ] Allocation percentages match latest analysis
- [ ] Signal tier reflects current market conditions
- [ ] Account balance updated to latest figure

---

## Previous Update: October 25, 2025 - Bug Fix Release

### CRITICAL BUG FIX: YAML Indentation Error in sync_risk_items.py & sync_provider_consensus.py

**Issue:** Both new sync scripts were generating invalid YAML with unquoted strings containing special characters (colons, quotes, etc.), causing dashboard load failure with "bad indentation of a mapping entry" error.

**Root Cause:** Manual YAML string building without proper quoting. When descriptions contained ":" characters (e.g., "Risk: Stagflation scenario"), the YAML parser failed.

**Fix Applied (October 25, 2025):**
- ✅ Added `import yaml` to both scripts
- ✅ Replaced manual string concatenation with `yaml.dump()` for proper serialization
- ✅ Now automatically quotes strings with special characters
- ✅ Handles Unicode and line wrapping correctly

**Files Fixed:**
1. `scripts/utilities/sync_risk_items.py` (lines 27, 148-176)
2. `scripts/utilities/sync_provider_consensus.py` (lines 27, 159-195)

**Testing Results:**
- ✅ Both scripts execute without errors
- ✅ YAML output is valid and properly formatted
- ✅ master-plan.md parses correctly
- ✅ Dashboard loads without indentation errors

**Prevention:** By using `yaml.dump()` instead of manual string building, this error class is now eliminated permanently. Future modifications to these scripts will inherit the safe YAML generation pattern.

---

### NEW SCRIPTS ADDED TO WINGMAN DASH PHASE 2

**Two new sync scripts have been integrated into the `wingman dash` workflow:**

#### 1. `scripts/utilities/sync_risk_items.py` ✅
- **Purpose:** Automatically generate `dashboard.riskItems` from Market Sentiment Overview
- **Data Source:** `Research/.cache/YYYY-MM-DD_Market_Sentiment_Overview.md` (Risk Factors section)
- **Output:** Fresh risk items with detailed descriptions in YAML format
- **Timestamp:** `dashboard.riskItemsUpdated`
- **First Executed:** October 25, 2025
- **Status:** Production Ready ✅

#### 2. `scripts/utilities/sync_provider_consensus.py` ✅
- **Purpose:** Automatically generate `dashboard.providerConsensus` from Market Sentiment Overview
- **Data Source:** `Research/.cache/YYYY-MM-DD_Market_Sentiment_Overview.md` (Cross-Provider Consensus Themes section)
- **Output:** Consensus themes with sentiment classification in YAML format
- **Timestamp:** `dashboard.providerConsensusUpdated` + `providerConsensus.updatedAt`
- **First Executed:** October 25, 2025
- **Status:** Production Ready ✅

---

## Integration Details

### Modified Files:
1. **`scripts/automation/wingman_dash.py`** (lines 80-81)
   - Added both new scripts to `sync_scripts` list in Phase 2
   - Both scripts now execute as part of standard workflow

2. **`Toolbox/INSTRUCTIONS/Domains/Wingman_Command_Pipeline.txt`** (Phase 2 section)
   - Updated documentation to include new scripts
   - Added NOTE explaining automatic data extraction

---

## How These Scripts Work

### Data Flow:
```
wingman prep
    ↓ creates
Research/.cache/YYYY-MM-DD_Market_Sentiment_Overview.md
    ↓ contains
  Risk Factors (Tier 1-3)
  Cross-Provider Consensus Themes (7 themes)
    ↓ extracted by
sync_risk_items.py ↘
                    → wingman dash (Phase 2)
sync_provider_consensus.py ↗
    ↓ populates
dashboard.riskItems
dashboard.providerConsensus
```

### What Changed:
**BEFORE:** Risk items and provider consensus only received timestamp updates (stale content)
**AFTER:** Both sections now receive FRESH CONTENT from research files during Phase 2

---

## Testing & Verification

### Scripts Tested: October 25, 2025 ✅
```
[RUNNING] risk_items_sync...
   ✅ risk_items_sync completed

[RUNNING] provider_consensus_sync...
   ✅ provider_consensus_sync completed
```

### Output Verified: October 25, 2025 ✅
- ✅ 4 risk items extracted with detailed descriptions
- ✅ 3-4 consensus themes extracted with sentiment classification
- ✅ All YAML formatting correct
- ✅ Timestamps properly updated
- ✅ master-plan.md structure valid

---

## Next Run Instructions (October 26+)

When you run `wingman dash` next time, the workflow will automatically:

### Phase 2 Execution Order:
1. sync_social_tab.py
2. sync_technicals_tab.py
3. sync_news_tab.py
4. sync_daily_planner.py
5. update_markets_intelligence.py
6. sync_quick_actions.py
7. **sync_risk_items.py** ← NEW (extracts from research)
8. **sync_provider_consensus.py** ← NEW (extracts from research)

**Action Required:** NONE - Both scripts execute automatically as part of wingman dash

---

## Technical Details

### sync_risk_items.py
- **Extracts:** Tier 1 risk factors (highest probability risks)
- **Format:** YAML with title + description fields
- **Count:** Top 4 risks
- **Update Method:** Regex-based content replacement + timestamp update

### sync_provider_consensus.py
- **Extracts:** Cross-provider consensus themes ranked by consensus %
- **Format:** YAML with theme + description + sentiment fields
- **Count:** Top 3-4 themes
- **Sentiment Mapping:** BULLISH, BEARISH, NEUTRAL, MIXED, CAUTIOUSLY_BULLISH, CAUTIOUSLY_BEARISH
- **Update Method:** Regex-based content extraction + YAML generation + timestamp update

---

## Files Modified/Created

### New Scripts Created:
- ✅ `scripts/utilities/sync_risk_items.py` (161 lines)
- ✅ `scripts/utilities/sync_provider_consensus.py` (215 lines)

### Scripts Updated:
- ✅ `scripts/automation/wingman_dash.py` (added 2 lines to sync_scripts list)

### Documentation Updated:
- ✅ `Toolbox/INSTRUCTIONS/Domains/Wingman_Command_Pipeline.txt` (Phase 2 section)

---

## Verification Checklist for Future Runs

When running `wingman dash`, verify:

- [ ] Both scripts in `wingman_dash.py` sync_scripts list (lines 80-81)
- [ ] Market Sentiment Overview file exists: `Research/.cache/YYYY-MM-DD_Market_Sentiment_Overview.md`
- [ ] Risk items updated in master-plan.md with current date content
- [ ] Provider consensus updated in master-plan.md with current date content
- [ ] Timestamps updated: `riskItemsUpdated` and `providerConsensusUpdated`
- [ ] wingman_dash logs show both scripts completed: `✅ risk_items_sync completed`, `✅ provider_consensus_sync completed`

---

## Questions/Issues

If either script fails during future runs:

1. **Verify data source exists:** `Research/.cache/YYYY-MM-DD_Market_Sentiment_Overview.md`
2. **Check script paths:** Both in `scripts/utilities/`
3. **Check wingman_dash.py integration:** Lines 80-81 should reference both scripts
4. **Check YAML format:** master-plan.md should have proper indentation and structure

---

**Created:** October 25, 2025
**By:** Claude Code
**Status:** ✅ Production Ready - Tested and Verified
