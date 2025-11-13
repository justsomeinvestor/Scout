# Research Dashboard to Trading Signals Workflow

**Purpose:** Transform comprehensive research dashboard analysis into distilled, actionable trading signals for intraday and swing trading
**Trigger:** At market open + during session when updating thesis
**Output:** Command Center Signal Cards + Trading Thesis + High-Quality Trade Setup Ideas
**Status:** Interactive Claude workflow (runs on-demand via command)

---

## 🎯 CORE MISSION

Transform the massive data in `master-plan/research-dashboard.html` into:
1. **Single Thesis** - Your market bias for the day (bullish/bearish/neutral with conviction)
2. **Top 3-5 Trade Setups** - Highest probability setups ready to execute
3. **Key Metrics Dashboard** - Critical levels, support/resistance, catalyst windows
4. **Signal Quality Score** - Confidence composite for each trade (similar to research dashboard signal-score-card)

---

## 🚀 QUICK START COMMAND

When you want the AI to run this workflow, use:

```
"Generate trading signals from research dashboard"
OR
"Build my trading thesis and top setups"
OR
"Create signal cards from current research"
```

---

## 📊 WORKFLOW EXECUTION STEPS

### STEP 1: Load and Analyze Research Dashboard
**What to do:**
- Read `master-plan/research-dashboard.html`
- Extract key data from these sections:
  - Sentiment Overview cards (bullish/bearish indicators)
  - Provider Consensus data (what % of signals agree)
  - AI Interpretation (technical analysis + market context)
  - Economic Calendar (upcoming catalysts/news)
  - Trading Levels (support/resistance for major indices + popular stocks)
  - Quick Actions panel (high-priority trade ideas)
  - Signal Score cards (composite analysis)

**Output format:** Create an internal analysis noting:
- Current market bias (tone: bullish/bearish/neutral)
- Confidence level (high/medium/low)
- Primary catalyst or driver
- Time horizon (intraday/swing)

**Example insight:**
```
RESEARCH ANALYSIS SUMMARY:
- Bias: CAUTIOUSLY BULLISH (60% conviction)
- Driver: Tech oversold, breadth improving, but Fed uncertainty high
- Timeframe: Intraday bias to long ES, swing thesis: hold longs through FOMC
- Risk: If CPI hotter than expected → flip bearish
```

---

### STEP 2: Identify Top Trade Setups

Based on research dashboard analysis, identify your TOP 3-5 setups:

**For EACH setup, extract:**
1. **Asset/Ticker**
   - Which stock/index is this for?
   - Example: "ES (S&P 500 futures)", "NVDA", "QQQ"

2. **Direction**
   - LONG or SHORT
   - Conviction: HIGH / MEDIUM / LOW

3. **Entry Zone**
   - Where would you enter?
   - Support level vs resistance level
   - Example: "LONG ES 5650-5655 at support"

4. **Why This Setup?**
   - What from research dashboard supports this?
   - Pick 2-3 key reasons:
     - TA confirmation (chart pattern)
     - Provider consensus (% of signals bullish)
     - Sentiment alignment (research AI says this is likely)
     - Catalyst timing (economic event window)
     - Volume flow (options data if available)

5. **Stop Loss & Profit Target**
   - Stop: Below nearest support/resistance
   - PT1, PT2: Scale out points
   - Risk/Reward ratio

6. **Quality Score** (0-100)
   - Based on research dashboard signal components
   - See QUALITY SCORING section below

---

### STEP 3: Build the Trading Thesis

Create a 2-3 sentence thesis that would guide your trading day:

**Template:**
```
TODAY'S THESIS:
"[Market Condition]: [Primary Driver].
Bias: [Direction] with [Conviction].
Playbook: [Action].
Risk: [What could break this thesis]"
```

**Real Example:**
```
TODAY'S THESIS:
"Tech stocks rebounding after oversold conditions and positive breadth breadth
signals. Bias: Moderately bullish on ES through first hour, watching for
resistance at 5680. Playbook: Long ES bounces at 5650 support, scale at 5680
resistance. Risk: If CPI prints hot → entire thesis breaks, watch for gap down.
```

---

### STEP 4: Quality Scoring (Create Signal Card)

Similar to research-dashboard.html `.signal-score-card`, create a quality score for each setup:

**5 Components to Rate (each 0-100):**

1. **Technical Confirmation** (40% weight)
   - Does chart pattern support entry?
   - Are key levels aligned?
   - Example: "Double bottom at support = 85/100"

2. **Provider Consensus** (20% weight)
   - What % of research signals agree?
   - From research dashboard consensus data
   - Example: "73% bullish sentiment = 73/100"

3. **Sentiment Alignment** (15% weight)
   - Is AI interpretation bullish/bearish?
   - Does it match your thesis?
   - Example: "AI is cautiously bullish = 75/100"

4. **Catalyst Timing** (15% weight)
   - Are there economic events?
   - Does timing work for your trade?
   - Example: "CPI after market close = neutral 50/100"

5. **Volume/Flow Quality** (10% weight)
   - Options flow supporting direction?
   - Volume confirms move?
   - Example: "Call OI increased = 70/100"

**Composite Score Formula:**
```
Signal Quality = (TA × 0.40) + (Consensus × 0.20) + (Sentiment × 0.15) +
                 (Catalyst × 0.15) + (Volume × 0.10)
```

**Tier Assignment:**
- 90-100: EXTREME QUALITY (Trade with full conviction)
- 75-89: STRONG QUALITY (Trade with standard sizing)
- 60-74: MODERATE QUALITY (Smaller size, tight stops)
- 45-59: WEAK QUALITY (Low conviction, avoid if no edge)
- Below 45: AVOID (Skip this setup)

---

### STEP 5: Populate Command Center Signal Cards

Create signal cards in the format shown in research-dashboard.html, but simplified for intraday/swing action:

**Signal Card Format:**

```html
<div class="signal-score-card">
  <div class="signal-header">
    <div class="signal-composite-score">78</div>
    <div class="signal-tier tier-strong-buy">STRONG BUY</div>
  </div>

  <div class="signal-setup">📈 ES Long at Support 5650-5655</div>

  <div class="signal-breakdown">
    <div class="breakdown-title">QUALITY COMPONENTS</div>
    <div class="breakdown-grid">
      <div class="breakdown-item">
        <div class="breakdown-label">Technical</div>
        <div class="breakdown-bar-container">
          <div class="breakdown-bar" style="width: 85%"></div>
        </div>
        <div class="breakdown-value">85</div>
      </div>

      <div class="breakdown-item">
        <div class="breakdown-label">Consensus</div>
        <div class="breakdown-bar-container">
          <div class="breakdown-bar" style="width: 73%"></div>
        </div>
        <div class="breakdown-value">73</div>
      </div>

      <div class="breakdown-item">
        <div class="breakdown-label">Sentiment</div>
        <div class="breakdown-bar-container">
          <div class="breakdown-bar" style="width: 75%"></div>
        </div>
        <div class="breakdown-value">75</div>
      </div>

      <div class="breakdown-item">
        <div class="breakdown-label">Catalyst</div>
        <div class="breakdown-bar-container">
          <div class="breakdown-bar" style="width: 70%"></div>
        </div>
        <div class="breakdown-value">70</div>
      </div>

      <div class="breakdown-item">
        <div class="breakdown-label">Volume</div>
        <div class="breakdown-bar-container">
          <div class="breakdown-bar" style="width: 80%"></div>
        </div>
        <div class="breakdown-value">80</div>
      </div>
    </div>
  </div>

  <div class="signal-recommendation">
    ✅ <strong>Setup Quality: STRONG</strong><br>
    Double bottom at 5650 support with provider consensus at 73% bullish.
    Breadth improving, AI interpretation shows modest upside bias. Entry at
    support with 1% stop below 5640. Targets at 5680 (resistance) and 5700
    (higher resistance). Risk/Reward: 1:3
  </div>
</div>
```

---

## 📋 EXTRACTION CHECKLIST

When executing this workflow, pull these data points FROM research-dashboard.html:

### Market Sentiment Section
- [ ] Current overall sentiment (bullish/bearish/neutral)
- [ ] Sentiment trend (improving/declining/stable)
- [ ] Individual stock sentiments for your watchlist
- [ ] Sentiment arrows (up/down/neutral indicators)

### Provider Consensus Section
- [ ] % bullish across providers
- [ ] % bearish across providers
- [ ] Major divergences (where providers disagree)
- [ ] Consensus strength (high agreement vs scattered opinion)

### AI Interpretation Section
- [ ] Market tone (bullish/bearish/neutral/cautiously bullish/etc)
- [ ] Primary technical setup
- [ ] Key resistance/support levels
- [ ] Risk factors mentioned
- [ ] Catalyst events flagged

### Economic Calendar
- [ ] High impact events coming today
- [ ] Timing of events (pre/post market, during session)
- [ ] Previous vs Expected vs Actual for recent data
- [ ] Fed speaks, economic data, earnings key dates

### Trading Levels Section
- [ ] Current price for main indices
- [ ] Resistance levels (R1, R2, R3)
- [ ] Support levels (S1, S2, S3)
- [ ] Pivot levels if available
- [ ] Key levels for each watchlist stock

### Quick Actions Panel
- [ ] Urgent trade ideas already flagged
- [ ] Urgency level (high/medium/low)
- [ ] Setup descriptions for these trades

### Options Intelligence (if available)
- [ ] Call vs put volume
- [ ] Open interest by strike
- [ ] IV Rank/percentile
- [ ] Flow patterns

---

## 🎯 OUTPUT FORMAT FOR COMMAND CENTER

The final signal cards should be added to a new panel in command-center.html:

**Panel Name:** "🎲 Today's Trading Signals"

**Structure:**
```
┌─────────────────────────────────────────┐
│  🎲 TODAY'S TRADING SIGNALS              │
├─────────────────────────────────────────┤
│                                         │
│  📌 TODAY'S THESIS                      │
│  ├─ Bias: Cautiously Bullish (60%)      │
│  ├─ Driver: Tech oversold rebound       │
│  └─ Risk: Hot CPI breaks thesis         │
│                                         │
├─────────────────────────────────────────┤
│                                         │
│  🔴 SIGNAL #1: ES Long 5650-5655        │
│  ├─ Quality Score: 78/100               │
│  ├─ Tier: STRONG BUY                    │
│  ├─ Stop: 5640 | PT1: 5680 | PT2: 5700│
│  └─ R/R: 1:3                            │
│                                         │
│  🔴 SIGNAL #2: QQQ Long 365-367         │
│  ├─ Quality Score: 72/100               │
│  ├─ Tier: MODERATE BUY                  │
│  ├─ Stop: 360 | PT1: 375 | PT2: 385    │
│  └─ R/R: 1:2.5                          │
│                                         │
│  🔴 SIGNAL #3: NVDA Short 130-132       │
│  ├─ Quality Score: 65/100               │
│  ├─ Tier: WEAK SELL                     │
│  ├─ Stop: 135 | PT1: 125 | PT2: 120    │
│  └─ R/R: 1:2                            │
│                                         │
└─────────────────────────────────────────┘
```

Each signal card should show:
- Setup description
- Composite quality score (0-100)
- Quality tier badge (EXTREME/STRONG/MODERATE/WEAK/AVOID)
- Component breakdown (Technical/Consensus/Sentiment/Catalyst/Volume)
- Entry/Stop/Targets
- Risk/Reward ratio
- Brief reasoning

---

## 🔄 REFRESH FREQUENCY

Run this workflow at these times:

1. **Market Open (9:30 AM ET)**
   - Load fresh research dashboard data
   - Build initial thesis and top 3-5 setups
   - Populate signal cards in Command Center

2. **Mid-Session (12:00 PM ET)**
   - Review if thesis still valid
   - Update signals if new catalyst emerged
   - Add new setups if old ones no longer valid

3. **Before Close (3:30 PM ET)**
   - Final review of day's setup quality
   - Flag setup changes for next day's session
   - Note what worked vs what didn't

4. **On-Demand**
   - After major news breaks
   - When new research dashboard data available
   - When market structure changes (e.g., SPY breaks key level)

---

## ⚠️ QUALITY GUARDRAILS

**Only populate signal cards if:**
- [ ] Setup has Quality Score ≥ 60 (avoid low-probability trades)
- [ ] Stop loss is clearly defined (not more than 2% of account risk)
- [ ] R/R ratio is ≥ 1:1.5 minimum
- [ ] You have 2+ reasons from research dashboard supporting this
- [ ] Catalyst timing makes sense for your trading style

**Skip setup if:**
- [ ] Quality Score < 45 (too weak)
- [ ] No clear support/resistance defined
- [ ] Research dashboard is conflicted (providers split 50/50)
- [ ] Economic calendar shows black swan risk (FOMC decision, NFP)

---

## 📝 EXAMPLE SESSION

**9:30 AM - Market Open**

User: "Generate trading signals from research dashboard"

Claude:
1. Loads research-dashboard.html
2. Extracts current sentiment (73% bullish, AI: cautiously bullish)
3. Identifies top setups:
   - ES long at 5650 (78/100 quality)
   - QQQ long at 365 (72/100 quality)
   - NVDA short at 130 (65/100 quality)
4. Creates thesis: "Tech rebound after oversold conditions. Bias: moderately bullish through first hour."
5. Populates signal cards in Command Center with all data

**12:00 PM - Mid-Session Update**

User: "Check research, any new signals?"

Claude:
1. Refreshes research-dashboard.html
2. Sentiment now 68% bullish (shifted down from 73%)
3. Two original setups still valid, removes NVDA short (quality dropped to 55)
4. Adds new setup: SPY long at resistance 665 (70/100 quality) based on provider consensus shift
5. Updates Command Center, flags thesis still valid but watch for divergence

**16:00 PM - End of Day**

User: "EOD signal review"

Claude:
1. Reviews which signals worked, which didn't
2. Logs performance to journal for future pattern analysis
3. Notes what changed from morning thesis
4. Flags lessons for tomorrow's research

---

## 🔗 INTEGRATION POINTS

**Connected to:**
- `master-plan/research-dashboard.html` (data source)
- `Journal/command-center.html` (output destination)
- `Journal/LIVE_SESSION_YYYY-MM-DD.md` (log which setups were executed)
- `scripts/journal/analyze_trends.py` (later: analyze which signal scores predict wins)

**Complements:**
- `JOURNAL_ANALYSIS_WORKFLOW.md` (end-of-day analysis uses these signals)
- `QUICK_COMMANDS_USER_GUIDE.md` (trigger via voice commands)
- `How_to_use_MP_CLAUDE_ONLY.txt` (master plan workflow integration)

---

## 💡 TIPS FOR BEST RESULTS

1. **Be Specific About Score Components**
   - Don't estimate, extract actual numbers from research dashboard
   - If consensus says "73% bullish" → use 73 for consensus score

2. **Match Your Trading Style**
   - For intraday: Weight technical (40%) more heavily
   - For swing: Weight sentiment (20%) and catalyst (20%) equally

3. **Quality Over Quantity**
   - Better to have 2 strong signals (75+) than 5 weak ones
   - Only trade what research dashboard strongly supports

4. **Update Aggressively**
   - If thesis breaks, recreate signals immediately
   - Don't force an outdated thesis to work

5. **Track What Works**
   - Which signal scores correlate with your wins?
   - Adjust weighting over time based on results

---

## ✅ SUCCESS CRITERIA

This workflow is working if:
- [ ] You execute trades from the signal cards
- [ ] Quality score ≥ 70 trades have ≥ 70% win rate
- [ ] Quality score 60-69 trades have ≥ 60% win rate
- [ ] You avoid most trades with quality < 60
- [ ] End-of-day review shows setup correlation to price targets

---

**Last Updated:** 2025-10-19
**Status:** Active - Ready for use
