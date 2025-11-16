# ⚠️ DEPRECATED - Archived 2025-11-12

**This document is archived for reference only.**

**NOTE:** dashboard.json was removed in Session 6. This file documents obsolete functionality.

**Current workflow:** See `Toolbox/MasterFlow/SCOUT_AI_WORKFLOW.md` (active AI processing workflow)

---

# STEP 3H: UPDATE DASHBOARD JSON - Field Mapping Reference

**Date:** 2025-11-01
**Purpose:** Detailed field mapping from prep file analysis to dashboard.json structure
**Duration:** ~5 minutes

---

## OVERVIEW

Step 3H converts the Markdown analysis from the prep file into structured JSON that feeds `research-dashboard.html`. This allows the visual dashboard to display today's market analysis without needing to parse Markdown.

**Key Principle:** One source of truth (prep file) → Two output formats (Markdown for humans via master-plan.md, JSON for machines via dashboard.json).

---

## FIELD MAPPING

### Top-Level Metadata

```json
{
  "dashboard": {
    "pageTitle": "Investment Research Dashboard - November 1, 2025",
    "dateBadge": "November 1, 2025",
    "lastUpdated": "2025-11-01T14:30:00Z",
    ...
  }
}
```

**Source Data:**
- `pageTitle` & `dateBadge`: Today's date (from system date when running Step 3H)
- `lastUpdated`: ISO timestamp when this update was completed

---

### Sentiment Cards (4 Cards)

**Purpose:** High-level sentiment across 4 major categories

**Location in dashboard.json:**
```json
"sentimentCards": [
  {"id": "equities", ...},
  {"id": "crypto", ...},
  {"id": "liquidity", ...},
  {"id": "macro", ...}
]
```

#### Card 1: Equities

**Source:** Step 3A (RSS) + Step 3E (Cross-Source Synthesis)

**Data to Extract:**
- Current market sentiment from Step 3A RSS analysis
- Key themes about equity market state

**JSON Structure:**
```json
{
  "id": "equities",
  "label": "Equities",
  "value": "[1-2 sentence sentiment]",
  "status": "[BULLISH / CONSOLIDATING / BEARISH]",
  "confidence": "[High / Medium / Low]",
  "description": "[3-4 bullet points from RSS analysis]"
}
```

**Example from Nov 1 prep file:**
```json
{
  "id": "equities",
  "label": "Equities",
  "value": "CONSOLIDATION PHASE (SPX 6,840 neutral momentum, spinning-top pattern)",
  "status": "CONSOLIDATING",
  "confidence": "High",
  "description": [
    "SPX stuck in 6,703-6,977 range with bullish bias but no conviction",
    "Breadth AD ratio 1.33 suggests mild advance, lacks thrust",
    "Buffett record $381B cash = institutional caution signal",
    "Next impulse (up/down) requires catalyst (earnings/macro data)"
  ]
}
```

#### Card 2: Crypto

**Source:** Step 3A (RSS) + Step 3E (Cross-Source Synthesis)

**Data to Extract:**
- Crypto market sentiment from RSS analysis
- Key themes about crypto adoption/regulation

**JSON Structure:**
```json
{
  "id": "crypto",
  "label": "Crypto",
  "value": "[1-2 sentence sentiment]",
  "status": "[BULLISH / CONSOLIDATING / BEARISH]",
  "confidence": "[High / Medium / Low]",
  "description": "[3-4 bullet points from RSS analysis]"
}
```

**Example from Nov 1 prep file:**
```json
{
  "id": "crypto",
  "label": "Crypto",
  "value": "INSTITUTIONAL ADOPTION ACCELERATION (Stablecoin layer-1, IPO pipeline)",
  "status": "BULLISH",
  "confidence": "Medium",
  "description": [
    "Circle/USDT layer-1 infrastructure + Visa 8 stablecoins × 40 countries",
    "Mastercard $2B Zero Hash deal signals institutional commitment",
    "Securitize + Consensus IPO pipeline (BlackRock/JP Morgan backing)",
    "BTC strong support 104.7k/106.9k, resistance 112.4k/115.7k"
  ]
}
```

#### Card 3: Liquidity Cycle

**Source:** Step 3E (Cross-Source Synthesis) + Step 3C (Technical Analysis)

**Data to Extract:**
- Institutional positioning/cash flow insights
- Fed/liquidity themes

**JSON Structure:**
```json
{
  "id": "liquidity",
  "label": "Liquidity Cycle",
  "value": "[1-2 sentence sentiment]",
  "status": "[ABUNDANT / NORMAL / STRESSED]",
  "confidence": "[High / Medium / Low]",
  "description": "[3-4 bullet points from analysis]"
}
```

**Example from Nov 1 prep file:**
```json
{
  "id": "liquidity",
  "label": "Liquidity Cycle",
  "value": "DEFENSIVE POSITIONING (Buffett's $381B cash hoarding + SRF surge)",
  "status": "STRESSED",
  "confidence": "High",
  "description": [
    "Buffett zero buybacks in positive earnings quarter = institutional red flag",
    "SRF demand $20.4B (highest since 2021) = banks hoarding liquidity",
    "Fed policy shift could accelerate if repo trends continue",
    "Watch for institutional copycat selling if Berkshire continues de-risking"
  ]
}
```

#### Card 4: Macro

**Source:** Step 3B (YouTube) + Step 3D (X/Twitter) + Step 3E (Cross-Source Synthesis)

**Data to Extract:**
- Macro environment sentiment (CPI, Fed, economic indicators)
- Analyst consensus from YouTube + Twitter

**JSON Structure:**
```json
{
  "id": "macro",
  "label": "Macro",
  "value": "[1-2 sentence sentiment]",
  "status": "[TAILWIND / NEUTRAL / HEADWIND]",
  "confidence": "[High / Medium / Low]",
  "description": "[3-4 bullet points from analysis]"
}
```

**Example from Nov 1 prep file:**
```json
{
  "id": "macro",
  "label": "Macro",
  "value": "MIXED SIGNALS (CPI awaited, Fed pivot narrative, earnings quality critical)",
  "status": "NEUTRAL",
  "confidence": "Medium",
  "description": [
    "Big Tech earnings mixed: AI spending accelerates but ads (not AI) drive growth",
    "Professional investors prepared for volatility per Buffett positioning",
    "CPI data still ahead; fed cuts attractive in rate-cut environment",
    "Retail sentiment Greedy but professionals rotating defensive"
  ]
}
```

---

### Sentiment History

**Purpose:** Track signal score progression over time (X-axis for dashboard graph)

**Location in dashboard.json:**
```json
"sentimentHistory": [
  {"date": "2025-10-31", "score": 64, "label": "MODERATE-BULLISH"},
  {"date": "2025-11-01", "score": 54, "label": "MODERATE"}
]
```

**Source Data:**
- From prep file Step 3F: Signal score for today
- From previous day's dashboard.json: Historical scores

**Process:**
1. Read today's signal score from prep file Step 3F (e.g., "54.1 / 100")
2. Read historical scores from current dashboard.json sentimentHistory
3. Append today's entry: `{"date": "2025-11-01", "score": 54, "label": "MODERATE"}`

**Tier Mapping:**
| Score | Label |
|-------|-------|
| 0-30 | WEAK |
| 31-60 | MODERATE |
| 61-80 | STRONG |
| 81-100 | EXTREME |

**Keep last 30 days** (approx) to show recent trend.

---

### Risk Items

**Purpose:** Top 5 risks to monitor from master-plan.md

**Location in dashboard.json:**
```json
"riskItems": [
  {"risk": "Buffett cascades", "monitor": "Watch Berkshire stock weakness..."},
  {"risk": "Vegas contagion", "monitor": "Monitor leisure spending..."},
  ...
]
```

**Source Data:**
From master-plan.md section "⚠️ KEY RISKS TO TRACK":
1. **Buffett's trade signal** → Watch Berkshire/insurance sector weakness
2. **Crypto divergence from equities** → Monitor BTC/SPX correlation
3. **Vegas contagion risk** → Monitor discretionary earnings
4. **Repo surge warning** → Watch SRF demand, Fed policy shifts
5. **Stablecoin regulation** → Monitor regulatory clarity

**JSON Structure:**
```json
{
  "risk": "[Risk name from master-plan]",
  "monitor": "[How to track this risk from master-plan guidance]",
  "priority": "[HIGH / MEDIUM / LOW]",
  "impact": "[What happens if this risk materializes]"
}
```

**Example from Nov 1:**
```json
[
  {
    "risk": "Buffett cascades",
    "monitor": "Watch Berkshire stock (BRK.A/BRK.B) and insurance sector weakness as early warning",
    "priority": "HIGH",
    "impact": "Liquidity deterioration, institutional copycat de-risking"
  },
  {
    "risk": "Earnings recession in discretionary",
    "monitor": "Vegas data (Caesars -20% operating income) could signal broader consumer slowdown",
    "priority": "HIGH",
    "impact": "Consumer spending slowdown, retail stocks weakness"
  },
  {
    "risk": "Stablecoin regulatory shock",
    "monitor": "Fed 'skinny master account' regulatory announcements",
    "priority": "MEDIUM",
    "impact": "Crypto infrastructure IPOs crater, institutional adoption stalls"
  },
  {
    "risk": "Crypto-equity divergence",
    "monitor": "Monitor BTC/SPX correlation daily",
    "priority": "MEDIUM",
    "impact": "Professional crypto deleveraging, potential cascade"
  },
  {
    "risk": "Options volatility inversion",
    "monitor": "Watch for breakouts above SPX 6,977 failing at resistance",
    "priority": "MEDIUM",
    "impact": "Institutions limiting upside, rally potential limited"
  }
]
```

---

### Portfolio Recommendation

**Purpose:** Strategic positioning advice based on analysis

**Location in dashboard.json:**
```json
"portfolioRecommendation": {
  "stance": "[Description of current market stance]",
  "allocation": {
    "equities": "50-60%",
    "crypto": "15-25%",
    "bonds": "15-20%",
    "cash": "5-10%"
  },
  "rotation": "[Specific sector rotation advice]",
  "hedging": "[Hedging strategy]"
}
```

**Source Data:**
From master-plan.md section "IMMEDIATE IMPLICATIONS" table, row "Positioning"

**Example from Nov 1:**
```json
{
  "stance": "Consolidation hold, selectively rebalance",
  "allocation": {
    "equities": "50-60%",
    "crypto": "15-25% (Solana/ETH showing resilience)",
    "bonds": "15-20% (Fed cuts attractive)",
    "cash": "5-10%"
  },
  "rotation": "Rotate OUT of Vegas/hospitality, INTO quality tech with pricing power",
  "hedging": "Sell SPY 665/660 put spreads for 0.30-0.50 credit; add QQQ 615/610 puts",
  "opportunities": [
    "Short Vegas/hospitality (Caesars, Win) if breaking Q3 lows",
    "Selectively long quality infrastructure (ADS, PANW, CRWD, MSFT)",
    "BTC buying zone at 104.7k-106.9k with 2% stop"
  ]
}
```

---

### Tabs Section (Advanced)

**Purpose:** Multi-tab dashboard with detailed views

**Standard Tabs:**
- Portfolio (holdings, allocation)
- Markets (indices, breadth, technicals)
- News Catalysts (upcoming events, Fed calendar)
- X Sentiment (Twitter/X sentiment by category)
- Technicals (SPX/QQQ/BTC levels, support/resistance)

**Source Data:**
- From prep file all sections (3A-3F)
- From technical_data.json
- From X/Twitter posts analysis

**See full dashboard.json structure** in source file for complete tab definitions.

---

## STEP-BY-STEP EXECUTION

### 1. Read Prep File
```bash
cat Research/.cache/2025-11-01_dash-prep.md
```

Extract:
- Step 3A: Sentiment card values (Equities, Crypto)
- Step 3B: YouTube analysis (Macro, narrative)
- Step 3C: Technical insights (Liquidity card, breadth/volatility)
- Step 3D: Twitter sentiment (X/Twitter card)
- Step 3E: Cross-source themes (Card descriptions)
- Step 3F: Signal score & tier (Sentiment history)

### 2. Read Master Plan (Updated)
```bash
cat master-plan/master-plan.md
```

Extract:
- KEY RISKS TO TRACK (rows 43-48) → Risk items
- IMMEDIATE IMPLICATIONS table (rows 34-40) → Portfolio recommendation

### 3. Update Dashboard.json
Use Edit tool to update:
- pageTitle, dateBadge, lastUpdated (metadata)
- sentimentCards[4] (Equities, Crypto, Liquidity, Macro)
- sentimentHistory (append today's entry)
- riskItems[5] (top 5 risks)
- portfolioRecommendation (allocation, stance, actions)

### 4. Verify JSON
```bash
python -m json.tool master-plan/dashboard.json > /dev/null && echo "Valid JSON"
```

### 5. Visual Test
- Open `master-plan/research-dashboard.html` in browser
- Confirm Nov 1, 2025 date displays
- Confirm sentiment cards updated
- Confirm graph shows new signal score point

---

## COMMON PITFALLS

❌ **Trailing comma in JSON** → Invalid JSON, dashboard won't load
✅ **Solution:** Check all arrays/objects end with `}` or `]`, not `},`

❌ **Mixing Markdown and JSON** → Syntax error
✅ **Solution:** Keep prep file (Markdown) separate from dashboard.json (pure JSON)

❌ **Hardcoding dates** → Dashboard becomes stale next day
✅ **Solution:** Always use dynamic date from system when running Step 3H

❌ **Forgetting to append to sentimentHistory** → Graph doesn't update
✅ **Solution:** Append new entry; don't replace entire array

❌ **Signal score mismatch** → Confusing/contradictory dashboard
✅ **Solution:** Verify score in dashboard = score in master-plan.md

---

## VERIFICATION CHECKLIST

After updating dashboard.json:

- [ ] All dates updated to today
- [ ] Signal score matches master-plan.md
- [ ] sentimentHistory appended (not replaced)
- [ ] 4 sentiment cards have values from prep file
- [ ] 5 risk items populated from master-plan.md
- [ ] portfolio allocation, rotation, hedging updated
- [ ] JSON validates (no syntax errors)
- [ ] Browser displays Nov 1 data when opened

---

**Status:** Complete Step 3H Documentation
**Next:** See QUICK_REFERENCE.md for automated update (recommended) or follow manual steps above
**Comprehensive System:** See DASHBOARD_SYSTEM_COMPLETE.md for full dashboard management system
**Last Updated:** 2025-11-01
