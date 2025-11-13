# Dashboard.json Complete Update Guide

**Date:** 2025-11-01
**Purpose:** Step-by-step instructions for updating ALL dashboard.json sections
**Audience:** Claude AI (Step 3H automation)

---

## Overview

This guide provides detailed procedures for updating every stale section in dashboard.json. It's organized by update priority and data source dependency.

**Total Sections to Update:** 6
**Estimated Time:** 25-35 minutes
**Target Completion:** All timestamps = 2025-11-01

---

## Prerequisites

Before starting updates, have these files open/available:

1. **scout/dashboard.json** - OBSOLETE (removed in Session 6)
2. **scout/dash.md** - Data source for most sections
3. **Research/.cache/2025-11-01_dash-prep.md** - Data source for themes
4. **Research/.cache/2025-11-01_technical_data.json** - Data source for tech metrics

---

## Update Procedure: Metadata Fields

### Step 1: Update pageTitle

**Field Location:** `dashboard.pageTitle`

**Current Value:** "Investment Research Dashboard - October 31, 2025"

**Procedure:**
1. Determine today's date: 2025-11-01 → "November 1, 2025"
2. Replace string: `"Investment Research Dashboard - November 1, 2025"`
3. Verify format matches: `"... - [Month] [Day], [Year]"`

**New Value:**
```
"Investment Research Dashboard - November 1, 2025"
```

---

### Step 2: Update dateBadge

**Field Location:** `dashboard.dateBadge`

**Current Value:** "October 31, 2025"

**Procedure:**
1. Extract date from pageTitle
2. Replace: `"November 1, 2025"`
3. Verify format: `"[Month] [Day], [Year]"`

**New Value:**
```
"November 1, 2025"
```

---

### Step 3: Update lastUpdated

**Field Location:** `dashboard.lastUpdated`

**Current Value:** "2025-10-31T21:45:00Z"

**Procedure:**
1. Get current UTC timestamp
2. Format as ISO 8601: `YYYY-MM-DDTHH:MM:SSZ`
3. Replace with: `"2025-11-01T[CURRENT_TIME]Z"`

**Example Value:**
```
"2025-11-01T20:30:00Z"
```

---

## Update Procedure: Sentiment Cards

### Step 4: Update Sentiment Cards (4 cards)

**Field Location:** `dashboard.sentimentCards[]`

**Data Source:** `scout/dash.md` → Eagle Eye Macro Overview → STATE OF PLAY

**Procedure for Each Card:**

1. **Read source section** (master-plan.md lines 24-30)
2. **Extract card data** (value, detail, color)
3. **Update sentimentCards[i]**
4. **Update sentimentCardsUpdated timestamp**

### Card 0: Equities

**JSON Path:** `dashboard.sentimentCards[0]`

**Fields to Update:**
```json
{
  "id": "equities",
  "label": "Equities",
  "value": "[NEW]",
  "detail": "[NEW]",
  "detailColor": "[COLOR]"
}
```

**Extract from master-plan.md:**
- Look for "🟡 STATE OF PLAY" section
- Find "**Composite moves to MODERATE (54.1/100)**" line
- Extract: equity market state description

**New Values (Nov 1):**
```json
{
  "value": "CONSOLIDATION PHASE",
  "detail": "Signal 54/100 • Neutral-Bullish (SPX 6,840, spinning-top, lacks conviction)",
  "detailColor": "#f59e0b"
}
```

### Card 1: Crypto

**JSON Path:** `dashboard.sentimentCards[1]`

**Extract from master-plan.md:**
- Find stablecoin/crypto reference in STATE OF PLAY
- Extract crypto adoption narrative

**New Values (Nov 1):**
```json
{
  "value": "INSTITUTIONAL ADOPTION",
  "detail": "Stablecoin acceleration (Visa 8 countries, Circle layer-1), IPO pipeline Q4",
  "detailColor": "#10b981"
}
```

### Card 2: Liquidity Cycle

**JSON Path:** `dashboard.sentimentCards[2]`

**Extract from master-plan.md:**
- Find Buffett/cash position reference in STATE OF PLAY
- Extract: institutional positioning narrative

**New Values (Nov 1):**
```json
{
  "value": "BUFFETT DEFENSIVE SIGNAL",
  "detail": "Record $381B cash hoarding + zero buybacks = institutional caution flag",
  "detailColor": "#ef4444"
}
```

### Card 3: Macro

**JSON Path:** `dashboard.sentimentCards[3]`

**Extract from master-plan.md:**
- Find macro uncertainty reference in STATE OF PLAY
- Extract: Fed/CPI uncertainty narrative

**New Values (Nov 1):**
```json
{
  "value": "MIXED SIGNALS",
  "detail": "CPI awaited, Fed pivot uncertain, Big Tech earnings mixed (AI vs ads)",
  "detailColor": "#f59e0b"
}
```

**Update Timestamp:**
```json
"sentimentCardsUpdated": "2025-11-01T[CURRENT_TIME]Z"
```

---

## Update Procedure: Sentiment History

### Step 5: Append to Sentiment History

**Field Location:** `dashboard.sentimentHistory[]`

**Data Source:** `Research/.cache/2025-11-01_dash-prep.md` → Step 3F

**Procedure:**
1. Read prep file Step 3F (Signal Calculation section)
2. Extract: "PRELIMINARY SIGNAL: 54.1 / 100"
3. Determine tier: 54.1 → "MODERATE"
4. Append new entry to sentimentHistory array

**Signal Score Tiers:**
- 0-30: WEAK
- 31-60: MODERATE
- 61-80: STRONG
- 81-100: EXTREME

**New Entry to Append:**
```json
{
  "date": "2025-11-01",
  "score": 54.1,
  "label": "MODERATE"
}
```

**Important:** APPEND to array (don't replace entire array)

**Update Timestamp:**
```json
"sentimentHistoryUpdated": "2025-11-01T[CURRENT_TIME]Z"
```

---

## Update Procedure: Quick Actions

### Step 6: Update Quick Actions (4 cards)

**Field Location:** `dashboard.quickActions[]`

**Data Source:** `scout/dash.md` → IMMEDIATE IMPLICATIONS (table rows 34-40)

**Structure:** 4 action items with types: risk, hedge, entry, catalyst

**Procedure for Each Card:**

1. Read IMMEDIATE IMPLICATIONS table from master-plan.md
2. Extract row relevant to action type
3. Update quickActions[i] with new title, value, description
4. Set urgency level

### Card 0: RISK

**JSON Path:** `dashboard.quickActions[0]`

**Extract from master-plan.md:**
- Row: "Positioning" (line 36)
- Cell: Guidance and Details columns

**Update Fields:**
```json
{
  "type": "risk",
  "title": "MARKET AT CONSOLIDATION POINT",
  "value": "Signal Score: 54/100 (CONSOLIDATION)",
  "description": "Consolidation hold, selectively rebalance. 50-60% equities / 15-25% crypto / 15-20% bonds / 5-10% cash. Rotate OUT of Vegas/hospitality, INTO quality tech with pricing power",
  "urgency": "critical"
}
```

### Card 1: HEDGE

**JSON Path:** `dashboard.quickActions[1]`

**Extract from master-plan.md:**
- Row: "Hedging" (line 37)

**Update Fields:**
```json
{
  "type": "hedge",
  "title": "FED UNCERTAINTY + BUFFETT CAUTION",
  "value": "Reduce VIX protection, add put spreads",
  "description": "SPY IV 64% offers attractive put-sell opportunities; QQQ IV 68% provides hedge cost relief. Sell 665/660 put spreads on SPY if holding long; BTC support strong at 104.7k",
  "urgency": "high"
}
```

### Card 2: ENTRY

**JSON Path:** `dashboard.quickActions[2]`

**Extract from master-plan.md:**
- Row: "Execution" (line 40)

**Update Fields:**
```json
{
  "type": "entry",
  "title": "BUY DIPS AT KEY SUPPORT",
  "value": "SPX $6,703-$6,498, BTC $106.9K-$104.7K",
  "description": "Spinning-top pattern suggests next impulse (up or down) requires catalyst. Fed/CPI data still ahead; stage buy orders at support (SPX 6,703/6,498), sell at resistance (6,977/7,182)",
  "urgency": "medium"
}
```

### Card 3: CATALYST

**JSON Path:** `dashboard.quickActions[3]`

**Extract from master-plan.md:**
- Row: "Execution" (line 40) or upcoming catalysts

**Update Fields:**
```json
{
  "type": "catalyst",
  "title": "NEXT CATALYST: Q4 EARNINGS + FED",
  "value": "Monitor breadth, volatility structure",
  "description": "Prepare for volatility expansion into November. Fed/CPI data still ahead; stage buy orders at support. Key catalyst: Q4 earnings quality + trade developments",
  "urgency": "medium"
}
```

**Update Timestamp:**
```json
"quickActionsUpdated": "2025-11-01T[CURRENT_TIME]Z"
```

---

## Update Procedure: Risk Items

### Step 7: Update Risk Items (5 items)

**Field Location:** `dashboard.riskItems[]`

**Data Source:** `scout/dash.md` → "⚠️ KEY RISKS TO TRACK" (lines 42-49)

**Procedure:**
1. Read KEY RISKS section from master-plan.md
2. Extract each risk title and description
3. Replace riskItems array with new 5 items

**Current Count:** 4 items
**New Count:** 5 items

**Replace Entire Array With:**

```json
[
  {
    "title": "Buffett's trade signal",
    "description": "Record $381B cash + zero buybacks = strongest caution flag in years. If Berkshire continues selling, watch for institutional copycat behavior (potential de-risking cascade). Monitor: Berkshire stock (BRK.A/BRK.B) and insurance sector weakness."
  },
  {
    "title": "Crypto divergence from equities",
    "description": "Bloomberg Galaxy Crypto Index up only 8% YTD (vs S&P 500 +20%). Crypto underperformance could force rotation trades if risk sentiment deteriorates. Monitor: BTC/SPX correlation daily for breakpoints."
  },
  {
    "title": "Vegas contagion risk",
    "description": "Caesars/Win earnings weakness signals consumer discretionary stress. Monitor leisure spending in Q3 reports; could foreshadow broader retail slowdown. Watch: Caesars (CZR) and Win Resorts (WRN) for further deterioration."
  },
  {
    "title": "Repo surge warning",
    "description": "SRF demand hit $20.4B (highest since 2021)—signals banks hoarding liquidity. Watch for Fed policy shifts if trend continues. Monitor: Repo facility data, Fed balance sheet changes."
  },
  {
    "title": "Stablecoin regulation",
    "description": "Democrats' 'Genie' framework + Fed 'skinny master account' talks could accelerate or stall crypto institutional adoption. Monitor regulatory clarity in next 30 days. Watch: Fed regulatory announcements."
  }
]
```

**Update Timestamp:**
```json
"riskItemsUpdated": "2025-11-01T[CURRENT_TIME]Z"
```

---

## Update Procedure: Provider Consensus

### Step 8: Update Provider Consensus Themes

**Field Location:** `dashboard.providerConsensus`

**Data Source:** `Research/.cache/2025-11-01_dash-prep.md` → Step 3E (Cross-Source Synthesis)

**Procedure:**
1. Read prep file Step 3E section
2. Extract: High-Confidence Themes
3. Convert to sentiment-tagged list
4. Update providerConsensus.themes array

**Replace Entire providerConsensus Object With:**

```json
{
  "updatedAt": "2025-11-01T[CURRENT_TIME]Z",
  "themes": [
    {
      "theme": "CONSOLIDATION PHASE",
      "description": "Cross-source agreement: SPX stuck in 6,703-6,977 range with spinning-top pattern. Buffett's defensiveness + institutional caution = market waiting for catalyst before next impulse.",
      "sentiment": "NEUTRAL"
    },
    {
      "theme": "INSTITUTIONAL DEFENSIVENESS",
      "description": "Buffett record $381B cash + zero buybacks = strongest caution in years. SRF surge ($20.4B) shows banks hoarding liquidity. Professional money preparing for volatility.",
      "sentiment": "BEARISH"
    },
    {
      "theme": "STABLECOIN INFRASTRUCTURE MATURITY",
      "description": "Visa 8 stablecoins × 40 countries, Circle/USDT layer-1, Mastercard $2B Zero Hash deal = institutional crypto adoption accelerating. Securitize + Consensus IPOs backed by BlackRock/JP Morgan.",
      "sentiment": "BULLISH"
    },
    {
      "theme": "EARNINGS QUALITY CRITICAL",
      "description": "Big Tech mixed: AI spending accelerating but digital ads (not AI) driving current growth. Vegas weakness (Caesars -20% operating income) signals consumer discretionary stress. Quality bifurcation = rotation trade.",
      "sentiment": "NEUTRAL"
    },
    {
      "theme": "FED/CPI UNCERTAINTY MANAGEABLE",
      "description": "No imminent catalyst priced (CPI/Fed already known). Focus shifts to Q4 earnings quality and trade developments. Macro headwinds present but not panic-level.",
      "sentiment": "NEUTRAL"
    }
  ]
}
```

**Update Timestamp:**
```json
"providerConsensusUpdated": "2025-11-01T[CURRENT_TIME]Z"
```

---

## Update Procedure: Technicals Tab

### Step 9: Update Technicals Tab AI Interpretation

**Field Location:** `dashboard.tabs[4].aiInterpretation`

**Data Source:** `Research/.cache/2025-11-01_technical_data.json` (all sections)

**Procedure:**
1. Read technical_data.json
2. Extract current levels, breadth, volatility
3. Synthesize into technical interpretation
4. Update aiInterpretation.summary

**Find tab:** `dashboard.tabs[4]` (id: "technicals")

**Update Structure:**
```json
{
  "updatedAt": "2025-11-01T[CURRENT_TIME]Z",
  "summary": "[NEW_SUMMARY]"
}
```

**New Summary (from technical_data.json):**

```
Technical Analysis Update - November 1, 2025:

SPX STRUCTURE: 6,840 (neutral momentum, RSI 61, bullish bias but consolidating)
- Support: 6,703 (medium), 6,498 (strong)
- Resistance: 6,977 (medium), 7,182 (strong)
- Pattern: Spinning-top = consolidation, awaits catalyst for next impulse

BREADTH: AD ratio 1.33 (neutral), 3,056 advancers vs 2,303 decliners
- 117 new highs vs 248 new lows = mixed signals
- Status: Neutral (lacks thrust for +25 points)

VOLATILITY: SPY IV 64%, QQQ IV 68% (elevated but stabilizing)
- Not panic levels (would be >80)
- Not risk-on (would be <40)
- Max pain levels: SPY 683, QQQ 629 = range-bound theta decay

BTC STRUCTURE: 110,199 (neutral momentum, consolidating)
- Strong support: 104,700
- Medium support: 106,900
- Resistance: 112,400 (medium), 115,700 (strong)

ASSESSMENT: Consolidation with bullish bias; ready for next impulse (up/down) on catalyst. Fed/CPI data still ahead. VIX stabilizing. Breadth at neutral = not yet confirming breakout. Technical setup is "prepare mode" not "go mode".
```

**Update Timestamp (nested):**
```json
"aiInterpretation.updatedAt": "2025-11-01T[CURRENT_TIME]Z"
```

---

## Verification Checklist

After completing all 9 update procedures:

- [ ] pageTitle updated to "November 1, 2025"
- [ ] dateBadge updated to "November 1, 2025"
- [ ] lastUpdated shows 2025-11-01 timestamp
- [ ] All 4 sentimentCards updated with Nov 1 values
- [ ] sentimentCardsUpdated = 2025-11-01
- [ ] New sentimentHistory entry appended (Nov 1, score 54.1)
- [ ] sentimentHistoryUpdated = 2025-11-01
- [ ] All 4 quickActions updated with Nov 1 data
- [ ] quickActionsUpdated = 2025-11-01
- [ ] All 5 riskItems replaced with Nov 1 risks
- [ ] riskItemsUpdated = 2025-11-01
- [ ] providerConsensus themes updated (5 themes)
- [ ] providerConsensusUpdated = 2025-11-01
- [ ] Technicals tab aiInterpretation.updatedAt = 2025-11-01

---

## Testing

### Manual Test (After Updates)

1. **Validate JSON Syntax**
```bash
python -m json.tool scout/dashboard.json > /dev/null && echo "Valid JSON"
```

2. **Check Signal Score**
```bash
grep -i "score.*54" scout/dashboard.json
# Should show: 54.1 in sentimentHistory
```

3. **Verify Date Consistency**
```bash
grep "2025-11-01" scout/dashboard.json | wc -l
# Should show: 8+ matches (metadata + timestamps)
```

4. **Visual Test**
- Open `scout/dash.html` in browser
- Confirm top date badge shows "November 1, 2025"
- Confirm sentiment cards show updated values
- Confirm "Immediate Actions" section shows Nov 1 data

---

## Troubleshooting

### JSON Validation Errors

**Error:** "Trailing comma" or "Invalid JSON"
**Solution:** Check that arrays/objects don't end with comma (`,]` or `},`)

**Error:** "Unexpected character"
**Solution:** Ensure all quotes are standard ASCII quotes (`"`) not smart quotes

### Date Format Issues

**Error:** Multiple date formats mixed
**Solution:** All timestamps should be ISO 8601: `YYYY-MM-DDTHH:MM:SSZ`

### Missing Data

**Error:** Can't find data source section
**Solution:** Check DASHBOARD_SECTION_MAPPING.md for exact line numbers in source files

---

## Time Estimate

| Task | Time |
|---|---|
| Metadata (steps 1-3) | 2 min |
| Sentiment Cards (step 4) | 5 min |
| Sentiment History (step 5) | 2 min |
| Quick Actions (step 6) | 8 min |
| Risk Items (step 7) | 5 min |
| Provider Consensus (step 8) | 5 min |
| Technicals (step 9) | 5 min |
| Verification & Testing | 5 min |
| **TOTAL** | **37 min** |

---

**Status:** Complete Update Guide
**References:** See DASHBOARD_TIMESTAMP_AUDIT.md and DASHBOARD_SECTION_MAPPING.md for details
**Last Updated:** 2025-11-01
