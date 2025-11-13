# Daily Trade Plan Workflow

**Purpose:** Generate ready-to-trade daily plan for each ticker/index
**Trigger:** Each morning at 9:30 AM ET (or on-demand)
**Output:** Formatted trade plan in Command Center (bullish + bearish scenarios)
**Format:** Clean, scannable, action-ready

---

## 🎯 What Gets Generated Each Morning

For each ticker you monitor (SPX, ES, QQQ, individual stocks):

```
$TICKER TRADE PLAN 📈 📉

BULLISH PLAN: [TICKER] above [LEVEL] | [OPTION PLAY if applicable] 📈
T: [Target 1], [Target 2] SL [Stop Loss]

BEARISH PLAN: [TICKER] under [LEVEL] | [OPTION PLAY if applicable] 📉
T: [Target 1], [Target 2] SL [Stop Loss]

[KEY CONTEXT SENTENCE 1]
[KEY CONTEXT SENTENCE 2]
[KEY CONTEXT SENTENCE 3]

[CURRENT SITUATION ASSESSMENT]
```

---

## 📋 DAILY PLAN COMPONENTS

### 1. **Bullish Setup**
- **Entry Condition:** Price above key support/resistance level
- **Option Play:** Call option if applicable (ticker + expiration + strike)
- **Targets:** T1 (conservative), T2 (aggressive)
- **Stop Loss:** Clear level if thesis breaks

### 2. **Bearish Setup**
- **Entry Condition:** Price below key support/resistance level
- **Option Play:** Put option if applicable
- **Targets:** T1 (conservative), T2 (aggressive)
- **Stop Loss:** Clear level if thesis breaks

### 3. **Context (3-4 sentences)**
- Week/month overview (what happened)
- Key levels tested/held
- Current position relative to key levels
- What would confirm each thesis

### 4. **Current Situation**
- Where is price RIGHT NOW
- What's the bias
- Which scenario is more likely TODAY

---

## 🚀 HOW TO TRIGGER IT

### Command to Use:
```
"Create daily trade plans for [TICKER]"
or
"Generate daily plans for SPX, ES, QQQ"
or
"Build my morning trade plans"
```

### What Claude Does:
1. Loads research-dashboard.html
2. Finds current price for ticker
3. Identifies key support/resistance levels
4. Finds bullish and bearish entry conditions
5. Sets targets and stop losses
6. Adds relevant options plays
7. Pulls 3-4 context sentences
8. Formats in the template style
9. Displays in Command Center

---

## 📊 STRUCTURE BREAKDOWN

### LEVEL EXTRACTION (From Research Dashboard)

**For SPX Example:**
```
Current Price: 6645
Weekly High: 6762
Weekly Low: 6500
Resistance Levels: 6700, 6762
Support Levels: 6600, 6550
Key Zone: 6640 (mid-week support)
Options Chain: Call open interest at 6700, Puts at 6550
```

### BULLISH PLAN LOGIC:
```
IF price > [lowest resistance] THEN
  Entry = above that level
  Target 1 = next resistance
  Target 2 = higher resistance
  Stop Loss = below the level that breaks thesis
  Options = call strike at/above entry level
ENDIF
```

### BEARISH PLAN LOGIC:
```
IF price < [lowest support] THEN
  Entry = below that level
  Target 1 = next support
  Target 2 = lower support
  Stop Loss = above the level that breaks thesis
  Options = put strike at/below entry level
ENDIF
```

### CONTEXT PULL (From Research Dashboard):
```
• What the week showed
• Key levels that held or broke
• Current position in trading range
• What would trigger breakout
```

---

## 💾 TEMPLATE FORMAT (Copy-Paste Ready)

```markdown
## $SPX TRADE PLAN 📈 📉

**BULLISH PLAN:** SPX above 6640 | SPX Oct 22 6700C 📈
- T: 6700, 6762
- SL: 6600

**BEARISH PLAN:** SPX under 6600 | SPX Oct 22 6550P 📉
- T: 6550, 6500
- SL: 6640

**CONTEXT:**
SPX had an extremely volatile week. SPX tried to break under 6550 a few times and held. SPX managed to close above the 6640 support level.

**TODAY'S BIAS:**
If SPX can reclaim 6700 we can see 6762 again. Calls can work above 6640 this week.
```

---

## 🎯 DAILY PLAN DASHBOARD

In Command Center, create new panel: **"📊 Morning Trade Plans"**

```
┌────────────────────────────────────────────┐
│  📊 MORNING TRADE PLANS                    │
├────────────────────────────────────────────┤
│                                            │
│  🔴 $SPX TRADE PLAN                       │
│  ├─ BULLISH: Above 6640 → 6700/6762      │
│  ├─ BEARISH: Below 6600 → 6550/6500      │
│  ├─ Current: 6645 (BULLISH BIAS)         │
│  └─ [View Full Plan]                     │
│                                            │
│  🔴 $ES TRADE PLAN                        │
│  ├─ BULLISH: Above 5650 → 5680/5700      │
│  ├─ BEARISH: Below 5600 → 5550/5500      │
│  ├─ Current: 5655 (BULLISH BIAS)         │
│  └─ [View Full Plan]                     │
│                                            │
│  🟢 $QQQ TRADE PLAN                       │
│  ├─ BULLISH: Above 365 → 375/385         │
│  ├─ BEARISH: Below 360 → 350/340         │
│  ├─ Current: 367 (BULLISH BIAS)          │
│  └─ [View Full Plan]                     │
│                                            │
│  ⚪ $NVDA TRADE PLAN                      │
│  ├─ BULLISH: Above 130 → 135/140         │
│  ├─ BEARISH: Below 125 → 120/115         │
│  ├─ Current: 132 (BULLISH BIAS)          │
│  └─ [View Full Plan]                     │
│                                            │
│  [Generated: 9:30 AM ET]                  │
│  [Last Updated: 12:00 PM ET]              │
│  [Refresh Plans]                          │
└────────────────────────────────────────────┘
```

Each plan expandable to show full context/bias

---

## 🔧 IMPLEMENTATION STEPS

### Step 1: Define Your Watchlist
Create list of tickers to generate plans for:
```
Primary: SPX, ES, QQQ
Secondary: NVDA, AAPL, TSLA
Options: XLK, SKEW, VIX
```

### Step 2: Set Daily Schedule
```
9:30 AM: "Generate daily trade plans"
12:00 PM: "Update trade plans with latest data"
3:30 PM: "EOD trade plan review - what worked"
```

### Step 3: Extract Key Data Points
From research-dashboard.html for each ticker:
- Current price
- Weekly high/low
- Major support/resistance (3-5 levels)
- Open interest for relevant options
- Recent price action (held support? broke resistance?)
- Volatility context

### Step 4: Build Plans
For each ticker:
- Set bullish entry condition + targets + stop
- Set bearish entry condition + targets + stop
- Pull 3-4 context sentences
- Assess today's bias

### Step 5: Display
Add to Command Center "Morning Trade Plans" panel
Make it scannable - quick view of each setup

---

## 📱 MOBILE/QUICK VIEW FORMAT

For quick reference during trading:

```
SPX: 📈 6640-6700-6762 | 📉 6600-6550-6500 | BIAS: 📈

ES: 📈 5650-5680-5700 | 📉 5600-5550-5500 | BIAS: 📈

QQQ: 📈 365-375-385 | 📉 360-350-340 | BIAS: 📈

NVDA: 📈 130-135-140 | 📉 125-120-115 | BIAS: 📈
```

---

## 🎯 COMMANDS TO USE

### Generate:
```
"Create daily trade plans for SPX"
"Generate morning plans for SPX, ES, QQQ"
"Build daily trade plan for NVDA"
"What's the SPX trade plan?"
```

### Update:
```
"Update trade plans with latest data"
"Refresh plans at 12:00 PM"
"Recalculate targets if price moves"
```

### Review:
```
"EOD trade plan review"
"Which plans worked today?"
"Performance by plan"
"Adjust tomorrow's levels based on today"
```

### View:
```
"Show me all morning trade plans"
"SPX plan details"
"Options for bullish SPX scenario"
"Which scenario is more likely?"
```

---

## 💡 PRO TIPS

### 1. **Keep Levels Clean**
- Round numbers when possible (6700, 6600, not 6673)
- Easy to remember and communicate
- Match resistance/support from chart

### 2. **Options Alignment**
- Call strikes near bullish targets
- Put strikes near bearish targets
- Use weekly or monthly based on your style

### 3. **Context Must Include**
- What the WEEK looked like
- What held vs broke
- Current status relative to weekly range
- What would confirm breakout

### 4. **Bias Assessment**
- Based on which level price is closer to
- Consider what held/broke this week
- Factor in current momentum
- Simple: "BULLISH" or "BEARISH" or "NEUTRAL"

### 5. **Update Schedule**
- 9:30 AM: Generate fresh plans
- 12:00 PM: Quick update if price moved significantly
- 3:30 PM: Final assessment before close
- Next morning: Fresh plans

---

## ✅ DAILY PLAN CHECKLIST

Before you trade, check:

- [ ] Plan generated before market open
- [ ] Bullish targets are above entry
- [ ] Bearish targets are below entry
- [ ] Stop loss is clear and makes sense
- [ ] Options plays align with targets
- [ ] Context explains why those levels matter
- [ ] Bias is justified by current position
- [ ] You understand both scenarios
- [ ] You know which would break thesis

---

## 🔗 INTEGRATION

### Inputs:
- `master-plan/research-dashboard.html`
- Current price data
- Weekly chart levels
- Options chain data

### Outputs:
- Command Center "Morning Plans" panel
- Daily plan markdown files
- Quick reference view
- Historical plan archive

### Connects To:
- RESEARCH_DASHBOARD_TO_SIGNALS_WORKFLOW.md
- JOURNAL_ANALYSIS_WORKFLOW.md
- LIVE_SESSION_YYYY-MM-DD.md (log which plans executed)

---

## 📊 EXAMPLE - FULL SPX PLAN

```
$SPX TRADE PLAN 📈 📉

BULLISH PLAN: SPX above 6640 | SPX Oct 22 6700C 📈
T: 6700, 6762 SL 6600

BEARISH PLAN: SPX under 6600 | SPX Oct 22 6550P 📉
T: 6550, 6500 SL 6640

CONTEXT:
SPX had an extremely volatile week. Price tested support at 6550 multiple
times and held. SPX closed above the key 6640 midpoint support level Friday,
suggesting buyers are stepping in.

LEVELS:
- Weekly High: 6762 (resistance)
- Key Resistance: 6700 (first target)
- Midpoint: 6640 (support that held)
- Key Support: 6600 (first target down)
- Weekly Low: 6500 (major support)

TODAY'S BIAS:
Bullish bias this week. If SPX reclaims 6700, we're eyeing 6762 again.
Calls work above 6640. Need to hold 6600 for puts to work.

KEY SETUP CONFIRMATIONS:
- Bullish: Price > 6640 + volume + closes above 6700
- Bearish: Price < 6600 + breaks 6640 support + closes under 6550
```

---

## 🎓 LEARNING PATH

### Day 1: Generate First Plans
- Tell Claude: "Create daily trade plans for SPX, ES, QQQ"
- Review the format and levels
- Understand bullish and bearish scenarios

### Days 2-5: Execute Plans
- Trade the plans you're most confident in
- Log entry/exit in journal
- Note which plans worked

### Week 2+: Refine Levels
- Track win rate by plan
- Adjust targets based on how price behaved
- Optimize stop loss placement

---

**Status:** Ready to implement
**Best Paired With:** RESEARCH_DASHBOARD_TO_SIGNALS_WORKFLOW.md
**Update Frequency:** Daily (9:30 AM, 12:00 PM, 3:30 PM ET)

---

Last Updated: October 19, 2025
