# Dashboard Stale Sections Complete Mapping

**Date:** 2025-11-01
**Discovery Method:** Automated timestamp scanner
**Total Stale Sections:** 18
**Status:** Requires comprehensive update procedure

---

## Executive Summary

The automated scanner discovered **18 stale sections** in dashboard.json (all from Oct 31). Only 3 sections are current (Nov 1).

This document maps each of the 18 stale sections to:
- Data source (where to get the update)
- Update priority (critical/high/medium/low)
- Complexity level
- Implementation status

---

## Stale Sections by Priority

### CRITICAL (Must Update - User-Facing)

These sections appear directly on the dashboard and impact user experience.

#### 1. `dashboard.quickActionsUpdated` & `dashboard.quickActions[]`
- **Age:** 2.2 hours old
- **Impact:** HIGH - Immediate Actions cards visible at top
- **Source:** master-plan.md IMMEDIATE IMPLICATIONS
- **Sections:** 4 cards (RISK, HEDGE, ENTRY, CATALYST)
- **Status:** ✅ DOCUMENTED (See DASHBOARD_UPDATE_GUIDE.md Step 6)
- **Priority:** CRITICAL

#### 2. `dashboard.riskItemsUpdated` & `dashboard.riskItems[]`
- **Age:** 9.2 hours old
- **Impact:** HIGH - Risk monitoring list visible in dashboard
- **Source:** master-plan.md KEY RISKS TO TRACK
- **Sections:** 5 items
- **Status:** ✅ DOCUMENTED (See DASHBOARD_UPDATE_GUIDE.md Step 7)
- **Priority:** CRITICAL

#### 3. `dashboard.providerConsensusUpdated` & `dashboard.providerConsensus.updatedAt`
- **Age:** 9.2 hours old
- **Impact:** MEDIUM - Themes displayed in dashboard
- **Source:** prep file Step 3E (Cross-Source Synthesis)
- **Sections:** 5 theme items
- **Status:** ✅ DOCUMENTED (See DASHBOARD_UPDATE_GUIDE.md Step 8)
- **Priority:** CRITICAL

---

### HIGH (Tab Contents - Important for Analytics)

These sections are in the tab views users interact with frequently.

#### 4. `dashboard.tabs[0].aiInterpretation.updatedAt` (Portfolio Tab)
- **Age:** 9.2 hours
- **Tab:** Portfolio
- **Impact:** MEDIUM - AI summary of portfolio analysis
- **Source:** TBD - portfolio-specific analysis
- **Status:** ⚠️ PARTIALLY DOCUMENTED
- **Priority:** HIGH

#### 5. `dashboard.tabs[0].portfolioRecommendation.updatedAt` (Portfolio Tab)
- **Age:** 9.2 hours
- **Tab:** Portfolio
- **Impact:** MEDIUM - Portfolio allocation recommendations
- **Source:** master-plan.md positioning guidance
- **Status:** ⚠️ PARTIALLY DOCUMENTED
- **Priority:** HIGH

#### 6. `dashboard.tabs[1].aiInterpretation.updatedAt` (Markets Tab)
- **Age:** 9.2 hours
- **Tab:** Markets
- **Impact:** MEDIUM - AI summary of market analysis
- **Source:** prep file sections 3A-3D + technical_data.json
- **Status:** ⚠️ PARTIALLY DOCUMENTED
- **Priority:** HIGH

#### 7. `dashboard.tabs[2].aiInterpretation.updatedAt` (X/Sentiment Tab)
- **Age:** 9.2 hours
- **Tab:** X Sentiment
- **Impact:** MEDIUM - AI summary of sentiment analysis
- **Source:** prep file Step 3D (X/Twitter Analysis)
- **Status:** ⚠️ PARTIALLY DOCUMENTED
- **Priority:** HIGH

#### 8. `dashboard.tabs[2].crypto_trending.updatedAt` (X/Sentiment Tab)
- **Age:** 9.2 hours
- **Tab:** X Sentiment
- **Impact:** LOW - Trending crypto narratives
- **Source:** prep file Step 3D (X/Twitter Analysis) - Trending Tickers
- **Status:** ❌ NOT DOCUMENTED
- **Priority:** HIGH

#### 9. `dashboard.tabs[2].macro_trending.updatedAt` (X/Sentiment Tab)
- **Age:** 9.2 hours
- **Tab:** X Sentiment
- **Impact:** LOW - Trending macro narratives
- **Source:** prep file Step 3D (X/Twitter Analysis) - Key Narratives
- **Status:** ❌ NOT DOCUMENTED
- **Priority:** HIGH

#### 10. `dashboard.tabs[2].contrarian_detector.updatedAt` (X/Sentiment Tab)
- **Age:** 9.2 hours
- **Tab:** X Sentiment
- **Impact:** LOW - Contrarian signals from sentiment
- **Source:** prep file Step 3E (Cross-Source Divergences)
- **Status:** ❌ NOT DOCUMENTED
- **Priority:** HIGH

#### 11. `dashboard.tabs[3].aiInterpretation.updatedAt` (News Catalysts Tab)
- **Age:** 9.2 hours
- **Tab:** News Catalysts
- **Impact:** MEDIUM - AI summary of upcoming catalysts
- **Source:** master-plan.md TACTICAL PLAYBOOK section
- **Status:** ⚠️ PARTIALLY DOCUMENTED
- **Priority:** HIGH

#### 12. `dashboard.tabs[4].aiInterpretation.updatedAt` (Technicals Tab)
- **Age:** 9.2 hours
- **Tab:** Technicals
- **Impact:** HIGH - AI interpretation of technical setup
- **Source:** technical_data.json (all sections)
- **Status:** ✅ DOCUMENTED (See DASHBOARD_UPDATE_GUIDE.md Step 9)
- **Priority:** HIGH

---

### MEDIUM (Technical Metrics - Used for Calculations)

These are detailed technical data used for analysis but not directly user-visible.

#### 13. `dashboard.tabs[4].tradingSignalScore.updatedAt`
- **Age:** 9.2 hours
- **Tab:** Technicals
- **Impact:** MEDIUM - Trading signal score calculation
- **Source:** technical_data.json + prep file Step 3F
- **Status:** ❌ NOT DOCUMENTED
- **Priority:** MEDIUM

#### 14. `dashboard.tabs[4].spxTechnicals.updatedAt`
- **Age:** 9.2 hours
- **Tab:** Technicals
- **Impact:** MEDIUM - SPX technical data
- **Source:** technical_data.json spx_levels section
- **Status:** ❌ NOT DOCUMENTED
- **Priority:** MEDIUM

#### 15. `dashboard.tabs[4].bitcoinTechnicals.updatedAt`
- **Age:** 9.2 hours
- **Tab:** Technicals
- **Impact:** MEDIUM - BTC technical data
- **Source:** technical_data.json btc_levels section
- **Status:** ❌ NOT DOCUMENTED
- **Priority:** MEDIUM

#### 16. `dashboard.tabs[4].optionsAIInterpretation.updatedAt`
- **Age:** 9.2 hours
- **Tab:** Technicals
- **Impact:** MEDIUM - Options market AI interpretation
- **Source:** technical_data.json spy_options + qqq_options
- **Status:** ❌ NOT DOCUMENTED
- **Priority:** MEDIUM

#### 17. `dashboard.tabs[4].unusualActivity.updatedAt`
- **Age:** 9.2 hours
- **Tab:** Technicals
- **Impact:** LOW - Unusual activity detection
- **Source:** technical_data.json (if available) or manual detection
- **Status:** ❌ NOT DOCUMENTED
- **Priority:** MEDIUM

---

## Update Implementation Plan

### Phase 1: Critical Sections (USER-FACING) - 3 sections

These are the most important for user experience and are already documented.

1. **quickActions** (4 cards) - 10 min
   - Reference: DASHBOARD_UPDATE_GUIDE.md Step 6
   - Automation: Can be scripted

2. **riskItems** (5 items) - 5 min
   - Reference: DASHBOARD_UPDATE_GUIDE.md Step 7
   - Automation: Can be scripted

3. **providerConsensus** (5 themes) - 5 min
   - Reference: DASHBOARD_UPDATE_GUIDE.md Step 8
   - Automation: Can be scripted

**Subtotal Phase 1:** 20 minutes

### Phase 2: Tab AI Interpretations (HIGH PRIORITY) - 5 sections

These directly affect what users see in each tab.

1. **tabs[4].aiInterpretation** (Technicals) - 5 min
   - Reference: DASHBOARD_UPDATE_GUIDE.md Step 9
   - Automation: Partly scriptable

2. **tabs[2].aiInterpretation** (X/Sentiment) - 5 min
   - Source: prep file Step 3D
   - Automation: Requires parsing + synthesis

3. **tabs[1].aiInterpretation** (Markets) - 5 min
   - Source: prep file + technical_data
   - Automation: Complex

4. **tabs[3].aiInterpretation** (News Catalysts) - 5 min
   - Source: master-plan.md + catalysts
   - Automation: Requires logic

5. **tabs[0].aiInterpretation** (Portfolio) - 5 min
   - Source: account_state.json (not currently used)
   - Automation: Requires account access

6. **tabs[0].portfolioRecommendation** - 3 min
   - Source: master-plan.md positioning
   - Automation: Scriptable

**Subtotal Phase 2:** 28 minutes

### Phase 3: Trending/Sentiment Data (MEDIUM PRIORITY) - 3 sections

These are supporting analytics data.

1. **tabs[2].crypto_trending** - 5 min
2. **tabs[2].macro_trending** - 5 min
3. **tabs[2].contrarian_detector** - 5 min

**Subtotal Phase 3:** 15 minutes

### Phase 4: Technical Metrics (MEDIUM PRIORITY) - 4 sections

These are detailed technical data.

1. **tabs[4].tradingSignalScore** - 5 min
2. **tabs[4].spxTechnicals** - 3 min
3. **tabs[4].bitcoinTechnicals** - 3 min
4. **tabs[4].optionsAIInterpretation** - 5 min
5. **tabs[4].unusualActivity** - 5 min

**Subtotal Phase 4:** 21 minutes

---

## Total Update Time Estimate

| Phase | Sections | Time | Status |
|---|---|---|---|
| Phase 1 (Critical) | 3 | 20 min | ✅ DOCUMENTED |
| Phase 2 (High) | 6 | 28 min | ⚠️ PARTIAL |
| Phase 3 (Medium) | 3 | 15 min | ❌ NOT DOC |
| Phase 4 (Medium) | 5 | 21 min | ❌ NOT DOC |
| **TOTAL** | **18** | **84 min** | |

---

## Recommended Approach

Given complexity, recommend **phased rollout**:

1. **Immediate (This Session):** Execute Phase 1 (3 critical sections) - 20 min
2. **Next Session:** Add Phase 2 (6 tab AI interpretations) - 28 min
3. **Later:** Phases 3-4 (supporting data) - 36 min

This ensures:
- ✅ User-visible data is always fresh
- ✅ Tab summaries are current
- ✅ Supporting data updated incrementally
- ✅ System remains stable

---

## Data Source Reference

| Source File | Used By | How |
|---|---|---|
| `master-plan.md` | quickActions, riskItems, portfolio, catalysts tabs | Extract sections |
| `prep file Step 3*` | providerConsensus, sentiment tabs, markets tab | Extract sections |
| `technical_data.json` | technicals tab all subsections | Extract JSON fields |
| `account_state.json` | portfolio tab (not yet used) | Account metrics |

---

**Status:** Complete Mapping of All 18 Stale Sections
**Next Action:** Execute Phase 1 Updates (3 critical sections)
**Last Updated:** 2025-11-01
