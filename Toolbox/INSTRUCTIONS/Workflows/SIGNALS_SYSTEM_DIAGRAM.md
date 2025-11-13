# Trading Signals System - Visual Architecture

## 🎲 Complete Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    MASTER PLAN RESEARCH DASHBOARD               │
│                   (master-plan/research-dashboard.html)         │
│                                                                 │
│  Contains:                                                      │
│  • Sentiment Overview (bullish/bearish cards)                  │
│  • Provider Consensus (% of signals agreeing)                  │
│  • AI Interpretation (technical analysis + tone)               │
│  • Economic Calendar (upcoming catalysts)                       │
│  • Trading Levels (support/resistance for indices + stocks)    │
│  • Signal Score Cards (composite analysis)                     │
│  • Options Intelligence (if available)                         │
│  • Risk Monitor (divergences, warnings)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │
                              ↓
                   ┌──────────────────────┐
                   │   Claude AI Workflow │
                   │  (This is YOU telling │
                   │   me what to do)     │
                   └──────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                ↓             ↓             ↓
        ┌────────────┐ ┌────────────┐ ┌──────────────┐
        │ EXTRACT    │ │ ANALYZE    │ │ SCORE        │
        │ DATA       │ │ PATTERNS   │ │ QUALITY      │
        └────────────┘ └────────────┘ └──────────────┘
            │               │               │
            ↓               ↓               ↓
        ┌────────────────────────────────────────┐
        │  Identify Top 3-5 Trading Setups       │
        │  • Direction (LONG/SHORT)              │
        │  • Entry Zone (support/resistance)     │
        │  • Stop Loss (clearly defined)         │
        │  • Profit Targets (PT1, PT2, PT3)      │
        │  • Risk/Reward Ratio                   │
        └────────────────────────────────────────┘
            │
            ↓
        ┌────────────────────────────────────────┐
        │  Calculate 5-Component Quality Score   │
        │                                        │
        │  Technical (40%)     ← Chart pattern  │
        │  Consensus (20%)     ← Provider %     │
        │  Sentiment (15%)     ← AI tone        │
        │  Catalyst (15%)      ← News timing    │
        │  Volume (10%)        ← Flow quality   │
        │                                        │
        │  COMPOSITE = Weighted Average          │
        └────────────────────────────────────────┘
            │
            ↓
        ┌────────────────────────────────────────┐
        │  Assign Quality Tier                   │
        │  • 90-100: EXTREME (Green)             │
        │  • 75-89:  STRONG (Green)              │
        │  • 60-74:  MODERATE (Blue)             │
        │  • 45-59:  WEAK (Yellow)               │
        │  • <45:    AVOID (Red)                 │
        └────────────────────────────────────────┘
            │
            ↓
        ┌────────────────────────────────────────┐
        │  Create Trading Thesis                 │
        │  (2-3 sentence market bias + playbook) │
        └────────────────────────────────────────┘
            │
            ↓
        ┌────────────────────────────────────────┐
        │  Generate HTML Signal Cards            │
        │  (Ready for display)                   │
        └────────────────────────────────────────┘
            │
            ↓
        ┌─────────────────────────────────────────────┐
        │    COMMAND CENTER - SIGNAL PANEL            │
        │  (Journal/command-center.html)              │
        │                                             │
        │  ┌─────────────────────────────────────┐  │
        │  │ 📌 TODAY'S THESIS                   │  │
        │  │ [Market bias + playbook]            │  │
        │  └─────────────────────────────────────┘  │
        │                                             │
        │  ┌─────────────────────────────────────┐  │
        │  │ 🎲 SIGNAL #1 - Score: 78           │  │
        │  │ Setup: ES Long at 5650              │  │
        │  │ Entry | Stop | PT1 | PT2 | R/R    │  │
        │  └─────────────────────────────────────┘  │
        │                                             │
        │  ┌─────────────────────────────────────┐  │
        │  │ 🎲 SIGNAL #2 - Score: 72           │  │
        │  │ Setup: QQQ Long at 365              │  │
        │  │ Entry | Stop | PT1 | PT2 | R/R    │  │
        │  └─────────────────────────────────────┘  │
        │                                             │
        │  ┌─────────────────────────────────────┐  │
        │  │ 🎲 SIGNAL #3 - Score: 65           │  │
        │  │ Setup: NVDA Short at 130            │  │
        │  │ Entry | Stop | PT1 | PT2 | R/R    │  │
        │  └─────────────────────────────────────┘  │
        └─────────────────────────────────────────────┘
            │
            ↓
        ┌─────────────────────────────────────────────┐
        │         LIVE TRADING SESSION                │
        │   (You execute trades from signal cards)    │
        │                                             │
        │  "Enter ES long at 5650" [Execute]        │
        │  "Exit QQQ for +$120" [Done]              │
        │  "Stop out NVDA short" [Loss]             │
        └─────────────────────────────────────────────┘
            │
            ↓
        ┌─────────────────────────────────────────────┐
        │      LIVE SESSION LOG (Auto-recorded)       │
        │     (Journal/LIVE_SESSION_YYYY-MM-DD.md)   │
        │                                             │
        │  • Which signals you executed              │
        │  • Entry/exit prices                       │
        │  • P&L for each trade                      │
        │  • Notes on execution                      │
        └─────────────────────────────────────────────┘
            │
            ↓
        ┌─────────────────────────────────────────────┐
        │      END-OF-DAY ANALYSIS                    │
        │   (scripts/journal/analyze_trends.py)      │
        │                                             │
        │  • Which signals had best win rate?        │
        │  • Which quality scores predicted wins?    │
        │  • What correlation with journal patterns? │
        │  • Adjust weights for tomorrow              │
        └─────────────────────────────────────────────┘
```

---

## 📊 Component Scoring Breakdown

```
EACH SIGNAL GETS SCORED ON 5 DIMENSIONS:

┌─────────────────────────────────────────────────────────────┐
│ 1. TECHNICAL CONFIRMATION (Weight: 40%)                     │
├─────────────────────────────────────────────────────────────┤
│ What: Strength of chart pattern support                     │
│ From: Research dashboard AI interpretation                  │
│ Examples:                                                   │
│   90-100: Double bottom + RSI divergence + volume confirm  │
│   70-80:  Support bounce + volume confirm                  │
│   50-60:  Minor support level touched                       │
│   30-40:  Weak pattern, no confirmation                    │
│   0-20:   Price far from key levels                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 2. PROVIDER CONSENSUS (Weight: 20%)                         │
├─────────────────────────────────────────────────────────────┤
│ What: % of research providers agreeing on bias              │
│ From: Research dashboard consensus data                     │
│ Examples:                                                   │
│   80-100: 80%+ of providers bullish/bearish                │
│   60-79:  60-80% consensus (good agreement)                │
│   50-59:  50-50 split (divergence warning)                 │
│   30-49:  Weak consensus (minority view)                   │
│   0-29:   Strong divergence (warning sign)                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 3. SENTIMENT ALIGNMENT (Weight: 15%)                        │
├─────────────────────────────────────────────────────────────┤
│ What: Does AI interpretation match our setup?              │
│ From: Research dashboard AI section tone                    │
│ Examples:                                                   │
│   85-100: "Bullish" setup + AI tone "Bullish"             │
│   70-80:  "Bullish" setup + AI tone "Cautiously bullish"  │
│   55-70:  "Bullish" setup + AI tone "Neutral"             │
│   40-55:  "Bullish" setup + AI tone "Bearish"             │
│   0-40:   Complete mismatch (red flag)                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 4. CATALYST TIMING (Weight: 15%)                            │
├─────────────────────────────────────────────────────────────┤
│ What: Does economic calendar help or hurt timing?          │
│ From: Research dashboard economic calendar                  │
│ Examples:                                                   │
│   80-100: No major catalysts next 2 hours (clear trading)  │
│   65-80:  Medium impact event but manageable               │
│   50-65:  High impact event mid-trade (risky timing)      │
│   35-50:  FOMC/NFP minutes away (avoid)                    │
│   0-35:   Black swan catalyst timing (don't trade)         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 5. VOLUME/FLOW QUALITY (Weight: 10%)                        │
├─────────────────────────────────────────────────────────────┤
│ What: Does volume/options flow confirm setup direction?    │
│ From: Research dashboard options intelligence               │
│ Examples:                                                   │
│   80-100: Heavy call buying (bullish) or put selling       │
│   65-80:  Moderate flow alignment                          │
│   50-65:  Neutral flow (no confirmation)                   │
│   35-50:  Flow showing weakness                            │
│   0-35:   Flow contradicts setup (red flag)                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎲 Quality Score Tiers & Action

```
┌──────────────┬──────────────┬────────────────────────────────┐
│ SCORE RANGE  │ TIER         │ WHAT YOU DO                    │
├──────────────┼──────────────┼────────────────────────────────┤
│              │              │                                │
│ 90-100       │ 🟢 EXTREME   │ ✅ TRADE WITH CONVICTION      │
│              │ QUALITY      │ • Full standard position       │
│              │              │ • Trade related setups         │
│              │              │ • High conviction day          │
│              │              │                                │
├──────────────┼──────────────┼────────────────────────────────┤
│              │              │                                │
│ 75-89        │ 🟢 STRONG    │ ✅ TRADE NORMALLY              │
│              │ QUALITY      │ • Standard sizing              │
│              │              │ • Normal risk management       │
│              │              │ • Primary trading setups       │
│              │              │                                │
├──────────────┼──────────────┼────────────────────────────────┤
│              │              │                                │
│ 60-74        │ 🟡 MODERATE  │ ⚠️ TRADE WITH CAUTION          │
│              │ QUALITY      │ • Reduced position size        │
│              │              │ • Tighter stop losses          │
│              │              │ • Less leverage                │
│              │              │ • Only if thesis supports      │
│              │              │                                │
├──────────────┼──────────────┼────────────────────────────────┤
│              │              │                                │
│ 45-59        │ 🔴 WEAK      │ ❌ AVOID                       │
│              │ QUALITY      │ • Too much uncertainty         │
│              │              │ • Skip unless desperate        │
│              │              │ • Wait for better setup        │
│              │              │                                │
├──────────────┼──────────────┼────────────────────────────────┤
│              │              │                                │
│ <45          │ 🔴 AVOID     │ ❌ DON'T TRADE                 │
│              │              │ • High probability of loss     │
│              │              │ • Multiple red flags           │
│              │              │ • Not worth the risk           │
│              │              │                                │
└──────────────┴──────────────┴────────────────────────────────┘
```

---

## 🕐 Daily Workflow Timeline

```
┌───────────────────────────────────────────────────────────────┐
│                   MARKET HOURS (EST)                          │
└───────────────────────────────────────────────────────────────┘

09:30 AM ━━━━━━━━━━━━━━━━ MARKET OPEN
    │
    └─► YOU: "Generate trading signals from research dashboard"
    │
    └─► CLAUDE:
        • Loads fresh research dashboard
        • Extracts current sentiment, consensus, levels
        • Identifies top 3-5 setups
        • Scores each (0-100 quality)
        • Creates thesis
        • Displays signal cards in Command Center
    │
    └─► YOU: [Review signal cards, select which to trade]

10:00 AM ━━━━━━━━━━━━━━━━ FIRST TRADES
    │
    └─► You execute Signal #1
    │   [Logs to LIVE_SESSION_YYYY-MM-DD.md]

12:00 PM ━━━━━━━━━━━━━━━━ MID-DAY CHECK
    │
    └─► YOU: "Check research, any new signals?"
    │
    └─► CLAUDE:
        • Refreshes research dashboard data
        • Updates if thesis broken or new setup emerged
        • Rebuilds signal cards if needed

14:30 PM ━━━━━━━━━━━━━━━━ THESIS VALIDATION
    │
    └─► YOU: "Is my thesis still valid?"
    │
    └─► CLAUDE: [Confirms or alerts if changed]

16:00 PM ━━━━━━━━━━━━━━━━ MARKET CLOSE / END OF DAY
    │
    └─► YOU: "EOD signal review - what worked"
    │
    └─► CLAUDE:
        • Analyzes which signals executed well
        • Logs performance to journal
        • Notes what changed from morning
        • Flags lessons for tomorrow

17:00 PM ━━━━━━━━━━━━━━━━ END OF DAY ANALYSIS
    │
    └─► CLAUDE runs: scripts/journal/analyze_trends.py
        • Which signal quality scores predicted wins?
        • Correlation between score tiers and performance
        • Historical pattern analysis
        • Recommendations for tomorrow's weighting
```

---

## 📁 File Structure

```
Investing/
│
├── Toolbox/INSTRUCTIONS/Workflows/
│   ├── README_SIGNALS_WORKFLOW.md              ← START HERE
│   ├── SIGNALS_QUICK_REFERENCE.md              ← One-page cheat sheet
│   ├── RESEARCH_DASHBOARD_TO_SIGNALS_WORKFLOW.md ← Detailed guide
│   ├── SIGNAL_CARD_HTML_TEMPLATE.md            ← Copy-paste HTML
│   └── SIGNALS_SYSTEM_DIAGRAM.md               ← This file
│
├── scripts/research/
│   └── extract_signals.py                      ← Python automation (optional)
│
├── master-plan/
│   └── research-dashboard.html                 ← Data source (your research)
│
├── Journal/
│   ├── command-center.html                     ← WHERE SIGNALS DISPLAY
│   ├── LIVE_SESSION_YYYY-MM-DD.md             ← Where trades log
│   └── ...
│
└── scripts/journal/
    ├── analyze_trends.py                       ← Post-analysis
    └── generate_feedback.py                    ← AI coaching
```

---

## 🔄 Information Flow

```
DAILY LOOP:

Morning                 During Day             Evening
═══════                 ══════════             ═══════

Generate               Execute               Analyze
Signals  ─────►    Trades from      ─────►  Performance
 (9:30)            Signal Cards       (4:00)  (5:00)
         Refresh     (10:00-3:30)       Log
         (12:00)                      to Journal
         Update
         (2:30)                    Tomorrow:
                                   Adjust
                                   Weights
```

---

## ✅ Quality Assurance

```
BEFORE YOU TRADE A SIGNAL:

┌─ Checklist ────────────────────────────────────┐
│ □ Signal quality score ≥ 60                   │
│ □ Clear entry zone defined (not vague)        │
│ □ Stop loss clearly below entry               │
│ □ Profit target(s) clearly above              │
│ □ Risk/Reward ratio ≥ 1:1.5                   │
│ □ Research dashboard still supports bias      │
│ □ No black swan catalysts in next 2 hours     │
│ □ Your thesis alignment (bullish bias ≠ short)│
│ □ Position sizing appropriate for your R:R    │
│ □ You're not already in a related trade       │
└────────────────────────────────────────────────┘

If ALL checkboxes ✓: Trade it
If ANY checkbox ✗: Skip or reduce size
```

---

## 📊 Example Session

```
9:30 AM
═══════
You:    "Generate trading signals from research dashboard"
Claude: [Loads dashboard, analyzes, scores]

        📊 THESIS: "Tech rebound after oversold.
                    Bias: Cautiously bullish through first hour.
                    Playbook: Long ES at support, scale at resistance."

        🎲 SIGNAL #1: ES Long 5650-5655 (78/100 - STRONG)
        🎲 SIGNAL #2: QQQ Long 365-367 (72/100 - MODERATE)
        🎲 SIGNAL #3: NVDA Short 130-132 (65/100 - WEAK)

10:15 AM
════════
You:    Execute SIGNAL #1 (ES long at 5652)
        "Entered ES long at 5652, stop at 5640, target 5680"
        [Auto-logs to LIVE_SESSION]

12:00 PM
════════
You:    "Check research, any new signals?"
Claude: [Refreshes data]
        "Thesis still valid - sentiment held.
         SIGNAL #1 still at 76/100, SIGNAL #2 dropped to 68,
         SIGNAL #3 fell to 55 - skip it."

14:00 PM
════════
You:    "Exit ES for +15 points"
        [Auto-logs exit, +$150 P&L]

16:00 PM
════════
You:    "EOD signal review - what worked"
Claude: "Signal #1 (78 score): HIT target, +$150
         Signal #2 (68 score): You didn't enter - good call
         Signal #3 (65 score): Avoided weakness - smart

         Pattern: Scores 75+ = 80% win rate today
                  Scores 65-74 = avoided losses"

17:00 PM
════════
CLAUDE AUTO-RUNS:
- Logs performance to journal
- Updates win rate by quality tier
- Flags: "Technical scoring is your edge"
- Tomorrow: Adjust technical weight to 45%
```

---

**Status:** 🟢 Complete System
**Last Updated:** 2025-10-19
