# Dashboard.json Section-to-Source Mapping

**Date:** 2025-11-01
**Purpose:** Complete mapping of dashboard.json sections to their data sources
**Used by:** Step 3H (Update Dashboard JSON) in the workflow

---

## Quick Reference Table

| Dashboard Section | Data Type | Source File | Source Section | Update Frequency |
|---|---|---|---|---|
| `pageTitle`, `dateBadge` | string | System | Today's date | Daily |
| `lastUpdated` | timestamp | System | Current UTC | Daily |
| `sentimentCards` | array(4) | scout/dash.md | EAGLE EYE OVERVIEW | Daily |
| `sentimentHistory` | array | System | Append new entry | Daily |
| `quickActions` | array(4) | scout/dash.md | IMMEDIATE IMPLICATIONS | Daily |
| `riskItems` | array | scout/dash.md | KEY RISKS TO TRACK | Daily |
| `providerConsensus` | object | prep file | Step 3E (Cross-Source) | Daily |
| `tabs[*].aiInterpretation` | nested obj | prep file | Steps 3A-3D + technical | Daily |
| `tabs[*].technicals` | nested obj | technical_data.json | All sections | Daily |

---

## Detailed Mappings

### 1. Metadata Fields

#### `pageTitle` & `dateBadge`
- **Current Value:** "Investment Research Dashboard - October 31, 2025"
- **Update Format:** `"Investment Research Dashboard - [Month] [Day], [Year]"`
- **Example:** "Investment Research Dashboard - November 1, 2025"
- **Source:** System (today's date)

#### `lastUpdated`
- **Current Value:** "2025-10-31T21:45:00Z"
- **Update Format:** ISO 8601 UTC timestamp
- **Example:** "2025-11-01T20:35:00Z"
- **Source:** System (current time when running update script)

---

### 2. Sentiment Cards

#### Field Location
```json
dashboard.sentimentCards[] (array of 4 objects)
```

#### Card 0: Equities
- **Current Label:** "EQUITIES"
- **Current Value:** "INFLECTION POINT"
- **Current Detail:** "Signal 64/100 • Neutral-Bullish (breadth diverging, support holding)"

**Update from:** `scout/dash.md` → Eagle Eye Macro Overview → STATE OF PLAY

**Nov 1 Content:**
```
Value: "CONSOLIDATION PHASE"
Detail: "Signal 54/100 • Neutral-Bullish (SPX 6,840, spinning-top, lacks conviction)"
Color: "#f59e0b" (orange)
```

#### Card 1: Crypto
- **Current Label:** "CRYPTO"
- **Current Value:** "ACCUMULATING (Funded)"

**Update from:** `scout/dash.md` → Eagle Eye Macro Overview → STATE OF PLAY

**Nov 1 Content:**
```
Value: "INSTITUTIONAL ADOPTION"
Detail: "Stablecoin acceleration (Visa 8 countries, Circle layer-1), IPO pipeline Q4"
Color: "#10b981" (green)
```

#### Card 2: Liquidity Cycle
- **Current Label:** "LIQUIDITY CYCLE"
- **Current Value:** "INSTITUTIONAL INTEGRATION"

**Update from:** `scout/dash.md` → Eagle Eye Macro Overview → STATE OF PLAY

**Nov 1 Content:**
```
Value: "BUFFETT DEFENSIVE SIGNAL"
Detail: "Record $381B cash hoarding + zero buybacks = institutional caution flag"
Color: "#ef4444" (red)
```

#### Card 3: Macro
- **Current Label:** "MACRO"
- **Current Value:** "FED UNCERTAIN"

**Update from:** `scout/dash.md` → Eagle Eye Macro Overview → STATE OF PLAY

**Nov 1 Content:**
```
Value: "MIXED SIGNALS"
Detail: "CPI awaited, Fed pivot uncertain, Big Tech earnings mixed (AI vs ads)"
Color: "#f59e0b" (orange)
```

#### Timestamp Update
```json
"sentimentCardsUpdated": "2025-11-01T[CURRENT_TIME]Z"
```

---

### 3. Sentiment History

#### Field Location
```json
dashboard.sentimentHistory[] (array of date/score objects)
```

#### Current Structure
```json
{
  "date": "2025-10-31",
  "score": 64,
  "label": "MODERATE-BULLISH"
}
```

#### Nov 1 Update
- **Action:** APPEND new entry (don't replace)
- **New Entry:**
```json
{
  "date": "2025-11-01",
  "score": 54.1,
  "label": "MODERATE"
}
```

**Data Source:** `Research/.cache/2025-11-01_dash-prep.md` → Step 3F (Signal Calculation)

**Timestamp Update:**
```json
"sentimentHistoryUpdated": "2025-11-01T[CURRENT_TIME]Z"
```

---

### 4. Quick Actions (Immediate Actions Cards)

#### Field Location
```json
dashboard.quickActions[] (array of 4 objects)
```

#### Current Structure
```json
{
  "type": "risk|hedge|entry|catalyst",
  "icon": "[emoji]",
  "title": "[TITLE]",
  "value": "[Value summary]",
  "description": "[Detailed description]",
  "urgency": "critical|high|medium|low"
}
```

#### Card Mapping

**Card 0: RISK**
- **Type:** risk
- **Icon:** ⚠️
- **Update from:** `scout/dash.md` → IMMEDIATE IMPLICATIONS → Positioning row
- **Nov 1 Title:** "MARKET AT CONSOLIDATION POINT"
- **Nov 1 Value:** "Signal Score: 54/100 (CONSOLIDATION)"
- **Nov 1 Description:** [From "Positioning" cell: "Consolidation hold, selectively rebalance. 50-60% equities / 15-25% crypto / 15-20% bonds / 5-10% cash. Rotate OUT of Vegas/hospitality, INTO quality tech"]
- **Urgency:** critical

**Card 1: HEDGE**
- **Type:** hedge
- **Icon:** 🛡️
- **Update from:** `scout/dash.md` → IMMEDIATE IMPLICATIONS → Hedging row
- **Nov 1 Title:** "FED UNCERTAINTY + BUFFETT CAUTION"
- **Nov 1 Value:** "Reduce VIX protection, add put spreads"
- **Nov 1 Description:** [From "Hedging" cell: "SPY IV 64% offers attractive put-sell opportunities; QQQ IV 68% provides hedge cost relief. Sell 665/660 put spreads on SPY if holding long; BTC support strong at 104.7k"]
- **Urgency:** high

**Card 2: ENTRY**
- **Type:** entry
- **Icon:** 📊
- **Update from:** `scout/dash.md` → IMMEDIATE IMPLICATIONS → Execution row
- **Nov 1 Title:** "BUY DIPS AT KEY SUPPORT"
- **Nov 1 Value:** "SPX $6,703-$6,498, BTC $106.9K-$104.7K"
- **Nov 1 Description:** [From "Execution" cell: "Spinning-top pattern suggests next impulse (up or down) requires catalyst. Fed/CPI data still ahead; stage buy orders at support (SPX 6,703/6,498), sell at resistance (6,977/7,182)"]
- **Urgency:** medium

**Card 3: CATALYST**
- **Type:** catalyst
- **Icon:** 📅
- **Update from:** `scout/dash.md` → IMMEDIATE IMPLICATIONS → relevant row
- **Nov 1 Title:** "NEXT CATALYST: Q4 EARNINGS + FED"
- **Nov 1 Value:** "Monitor breadth, volatility structure"
- **Nov 1 Description:** [From "Execution" cell: "Prepare for volatility expansion into November. Fed/CPI data still ahead; stage buy orders at support"]
- **Urgency:** medium

#### Timestamp Update
```json
"quickActionsUpdated": "2025-11-01T[CURRENT_TIME]Z"
```

---

### 5. Risk Items

#### Field Location
```json
dashboard.riskItems[] (array of 4+ objects)
```

#### Current Structure
```json
{
  "title": "[Risk title]",
  "description": "[Detailed description of risk + monitoring guidance]"
}
```

#### Nov 1 Risk Items

**Update from:** `scout/dash.md` → "⚠️ KEY RISKS TO TRACK" section (lines 42-49)

**Risk 1:**
```json
{
  "title": "Buffett's trade signal",
  "description": "Record $381B cash + zero buybacks = strongest caution flag in years. If Berkshire continues selling, watch for institutional copycat behavior (potential de-risking cascade). Monitor: Berkshire stock (BRK.A/BRK.B) and insurance sector weakness as early warning."
}
```

**Risk 2:**
```json
{
  "title": "Crypto divergence from equities",
  "description": "Bloomberg Galaxy Crypto Index up only 8% YTD (matching bonds) vs S&P 500 +20%. Crypto underperformance could force rotation trades if risk sentiment deteriorates. Monitor: BTC/SPX correlation daily for breakpoints."
}
```

**Risk 3:**
```json
{
  "title": "Vegas contagion risk",
  "description": "Caesars/Win earnings weakness signals consumer discretionary stress. Monitor leisure spending in next Q3 reports; could foreshadow broader retail slowdown. Watch: Caesars (CZR) and Win Resorts (WRN) for further deterioration."
}
```

**Risk 4:**
```json
{
  "title": "Repo surge warning",
  "description": "SRF demand hit $20.4B (highest since 2021)—signals banks hoarding liquidity. Watch for Fed policy shifts if this trend continues into November. Monitor: Repo facility data, Fed balance sheet changes."
}
```

**Risk 5:**
```json
{
  "title": "Stablecoin regulation",
  "description": "Democrats' 'Genie' framework + Fed 'skinny master account' talks could accelerate or stall crypto institutional adoption. Monitor regulatory clarity in next 30 days. Watch: Fed announcements, regulatory guidance on stablecoins."
}
```

#### Timestamp Update
```json
"riskItemsUpdated": "2025-11-01T[CURRENT_TIME]Z"
```

---

### 6. Provider Consensus

#### Field Location
```json
dashboard.providerConsensus (object with themes array)
```

#### Current Structure
```json
{
  "updatedAt": "2025-10-31T14:45:00Z",
  "themes": [
    {
      "theme": "[Theme name]",
      "description": "[Description]",
      "sentiment": "BULLISH|NEUTRAL|BEARISH"
    }
  ]
}
```

#### Nov 1 Update

**Update from:** `Research/.cache/2025-11-01_dash-prep.md` → Step 3E (Cross-Source Synthesis)

**New Themes:**

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

#### Timestamp Update
```json
"providerConsensusUpdated": "2025-11-01T[CURRENT_TIME]Z"
```

---

### 7. Tabs (Advanced Sections)

#### Tab Structure
Each tab is an object with multiple nested fields:
```json
tabs[i] {
  "id": "tab_id",
  "label": "Tab Label",
  "aiInterpretation": {...},
  "tradingSignalScore": "X.X/10",
  "[other_fields]": "..."
}
```

#### Tab 4 (Technicals) - AI Interpretation Update

**Field Location:**
```json
dashboard.tabs[4].aiInterpretation
```

**Current Structure:**
```json
{
  "updatedAt": "2025-10-31T14:45:00Z",
  "summary": "[AI-generated technical summary]"
}
```

**Nov 1 Update from:** `Research/.cache/2025-11-01_technical_data.json`

**New Summary (Nov 1 data):**
```
Technical Analysis Update:
- SPX 6,840 (neutral momentum, RSI 61, bullish bias)
- Support: 6,703 (medium), 6,498 (strong)
- Resistance: 6,977 (medium), 7,182 (strong)
- Breadth: AD ratio 1.33 (neutral), 3,056 adv / 2,303 dec
- Volatility: SPY IV 64%, QQQ IV 68% (elevated but stabilizing)
- Options: Max pain SPY 683, QQQ 629 = range-bound decay
- Pattern: Spinning-top = consolidation before next impulse
- Assessment: Neutral consolidation with bullish bias; await catalyst (earnings/macro data)
```

**Timestamp Update:**
```json
"aiInterpretation.updatedAt": "2025-11-01T[CURRENT_TIME]Z"
```

---

## Update Order (Recommended)

For systematic updates, process sections in this order:

1. **Metadata** (pageTitle, dateBadge, lastUpdated) - Quick, always updated
2. **Sentiment Cards** - Simple extraction from master-plan.md
3. **Sentiment History** - Append operation (idempotent)
4. **Quick Actions** - Extract from IMMEDIATE IMPLICATIONS table
5. **Risk Items** - Extract from KEY RISKS section
6. **Provider Consensus** - Extract themes from prep file Step 3E
7. **Technicals Tab** - Extract from technical_data.json

**Time Estimate:** 20-30 minutes total for all updates

---

**Next:** See `DASHBOARD_UPDATE_GUIDE.md` for step-by-step manual update procedures

**Status:** Complete Section-to-Source Mapping
**Last Updated:** 2025-11-01
