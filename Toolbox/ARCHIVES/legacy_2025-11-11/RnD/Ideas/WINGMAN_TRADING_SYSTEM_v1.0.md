# WINGMAN TRADING SYSTEM v1.0

**Status:** Design Phase (Not Yet Implemented)
**Last Updated:** 2025-10-27
**Goal:** $2,500/month systematic income
**Author:** Wingman AI Trading Partner

---

## EXECUTIVE SUMMARY

Complete end-to-end trading system designed to solve your three core problems:
1. **Entry Timing** - Multi-signal confluence checker prevents jumping the gun
2. **Stop Loss Calculation** - Systematic, formula-based (no more guessing)
3. **Target Setting** - 3-tier systematic exit prevents early exits

This system transforms you from gut-trading to high-probability systematic trading.

---

## CORE PROBLEMS & SOLUTIONS

### Problem 1: Finding Good Setups
**Your Current Process:** Read news enough, something comes up eventually. Not scalable.

**Solution:** Automated Morning Scanner
- Scans all instruments simultaneously (SPY, QQQ, ES, NQ, top 10 stocks, crypto)
- Multi-timeframe analysis (daily, 4H, 1H, 15-min)
- Multi-signal confluence scoring (0-100%)
- Delivers top 5 opportunities ranked by probability
- Removes need to hunt for setups

---

### Problem 2: Entry Discipline & Bad Timing
**Your Current Issue:** Jump gun before all criteria met, skip RSI/divergence checks, often right on direction but wrong on entry price.

**Solution:** Pre-Entry Confluence Checklist (HARD BLOCKS)
- Cannot enter unless ALL criteria pass
- Wingman blocks entries scoring <6/10
- Comprehensive checks:
  - Multi-timeframe alignment (daily/4H/1H/15min all agree?)
  - Technical confluence (MA, Ichimoku, RSI, MACD, volume, VWAP)
  - Market context (QQQ/SPY divergence, breadth, signal tier)
  - Structure validation (support/resistance, VWAP alignment)
- Output: GO/CAUTION/BLOCK rating before entry

---

### Problem 3: Stop Loss Guessing
**Your Current Issue:** No systematic approach, getting stopped out when "right" on direction.

**Solution:** Systematic Stop Calculator
- **ATR-Based:** 1.5x Average True Range below entry (volatility-adjusted)
- **Structure-Based:** Just below recent support/above resistance
- **Time-Based:** Auto-exit if no movement in X minutes
- Output: Exact stop price with rationale before entry

---

### Problem 4: Exit Too Early
**Your Current Issue:** Exit way too early, miss runners, often right but leave money on table.

**Solution:** 3-Tier Target System
- **T1 (50% exit):** 1.5R (risk-reward ratio) - Take partial profit
- **T2 (30% exit):** Fibonacci extension or next structural level - Increase profit
- **T3 (20% runner):** Trail stop at breakeven after T1 hit - Let winners run
- Output: All three targets calculated systematically before entry

---

## YOUR TRADING PROFILE

Based on 2025-10-09 through 2025-10-17 trading history:

**Strengths:**
- ✅ Good directional reads (right on trend/momentum)
- ✅ Good execution when structure is crystal clear (Oct 15, Oct 17)
- ✅ Excellent discipline in WEAK signals (stayed in cash)
- ✅ Fast learning (creates rules after losses)
- ✅ 24/7 commitment (willing to trade anything, anytime)

**Weaknesses:**
- ❌ Impatient entries (jumps gun when structure ambiguous)
- ❌ Missing confluence checks (RSI, divergences, structure)
- ❌ No systematic stops (guessing instead of calculating)
- ❌ Exits too early (leaving money on table)
- ❌ No targeting system (how to calculate T1/T2/T3)

**Edge:** Tactical setups with clear structure (6,650-6,700 chop, consolidation breaks, oversold rebounds)

**Opportunity:** You're often RIGHT. Fix entry/stop/exit mechanics and edge becomes profitable.

---

## RISK FRAMEWORK

### Position Sizing
- **Risk per trade:** 1% of account = $231 (based on $23,105 account)
- **Position calculation:** Risk ÷ Stop Distance = Position Size
  - Example: $231 risk ÷ $1.30 stop = 177 shares

### Daily Loss Limit
- **Maximum daily loss:** $250
- **Implication:** 1 full loss per day, then STOP
- **Enforcement:** Wingman blocks new entries after $250 loss

### Monthly Income Target
- **Goal:** $2,500/month
- **Daily average:** $125/day over 20 trading days
- **Trade target:** 10-20 trades/month at $125-$250 profit each

### Income Projection (Conservative Model)
- **Trades/month:** 20
- **Win rate:** 65%
- **Avg winner:** $175 (1.5R at $231 risk)
- **Avg loser:** $231 (1R at $231 risk)
- **Monthly math:**
  - 13 winners × $175 = $2,275
  - 7 losers × $231 = -$1,617
  - **Net: +$658/month**

**To reach $2,500/month goal:**
- Increase win rate to 70% OR
- Increase avg winner to 2R OR
- Achieve 1.5 trades/day

---

## SYSTEM ARCHITECTURE

### PHASE 1: MORNING PROTOCOL (Before 9:30 AM)

#### Step 1: Automated Scanner (30 minutes before open)
**Input:** Current market data across all instruments
**Process:**
1. Scan SPY, QQQ, ES, NQ (always)
2. Scan top 10 stocks: NVDA, TSLA, AAPL, MSFT, AMZN, META, GOOGL, AMD, NFLX, COIN
3. Scan crypto: BTC, ETH, SOL
4. Analyze each on 5 timeframes: daily, 4H, 1H, 15-min, 5-min

**Analysis Per Instrument:**
```
Confluence Scoring:
├─ Trend (40%): MAs aligned (20/50/200 EMA), direction clear
├─ Breadth (25%): Support holding, A/D ratio, up-volume %
├─ Momentum (20%): RSI positioning, MACD alignment, volume spike
├─ Structure (10%): VWAP, Fibonacci, key S/R, Ichimoku cloud
└─ Divergence (5%): QQQ/SPY divergence check, RSI divergence
```

**Output: Top 5 Opportunities Ranked by Probability**
```
Example Output:

1. NVDA LONG @ 189.50 (87% confluence)
   - Setup: Daily uptrend, 4H consolidation breakout, 1H inside bar setup
   - Entry: Breakout above 190.00 on volume
   - Stop: 188.20 (ATR-based, -1.3%)
   - T1: 191.45 (+1.5R)
   - T2: 193.20 (+2.5R)
   - T3: Runner with trail
   - Position: 178 shares

2. QQQ SHORT @ 603.50 (72% confluence)
   [Similar details...]

3. BTC LONG @ 110,500 (68% confluence)
   [Similar details...]

4. SPY LONG @ 677.25 (65% confluence)
   [Similar details...]

5. TSLA SHORT @ 425.80 (58% confluence)
   [Similar details...]
```

#### Step 2: Pre-Market Brief (5 minutes)
**Output to you:**
```
WINGMAN MORNING BRIEF - October 27, 2025

MARKET CONTEXT:
├─ Signal: MODERATE (45.5/100) - Selective deployment
├─ Breadth: WEAK (2.0/25) - Risk-off backdrop
├─ Volatility: ELEVATED (VIX ~18) - Watch for gaps
└─ Sentiment: NEUTRAL - Wait for clarity

TOP OPPORTUNITIES TODAY:
[List top 5 with all details]

Your command, Pilot. Which setups are you watching?
```

**Your action:** Select 1-3 to watch during session

---

### PHASE 2: ENTRY EXECUTION PROTOCOL

#### Step 1: Setup Alerts
Wingman sets alerts at:
- Entry trigger level
- Stop loss level
- Each target level

You get notified when price approaches.

#### Step 2: Pre-Entry Confluence Checklist (MANDATORY)
When setup triggers, you say: `"Wingman, entry check NVDA long @ 189.50"`

**Wingman runs FULL analysis:**

```
PRE-ENTRY CHECKLIST - NVDA LONG @ 189.50

MULTI-TIMEFRAME ALIGNMENT:
├─ Daily: ✅ BULLISH (above 20/50/200 EMA, new breakout)
├─ 4H: ✅ BULLISH (consolidation complete, VWAP reclaim)
├─ 1H: ✅ BULLISH (higher lows, volume confirmation)
└─ 15-min: ✅ BULLISH (entry bar spike, volume 1.8x)

TECHNICAL CONFLUENCE:
├─ Moving Averages: ✅ 20 > 50 > 200 (bullish structure)
├─ RSI (14): ✅ 55 (neutral, room to run, not overbought)
├─ MACD: ✅ Bullish cross, histogram positive
├─ Ichimoku Cloud: ✅ Price above cloud, twist bullish
├─ Volume: ✅ 1.8x 20-bar average (strong confirmation)
├─ VWAP: ✅ Above VWAP, inside deviation band
└─ Divergence: ✅ No RSI divergence, MACD aligned

MARKET CONTEXT:
├─ QQQ Alignment: ✅ QQQ also bullish (no divergence)
├─ SPY Alignment: ✅ SPY above 50-dMA (risk-on)
├─ Breadth (ADD): ⚠️ WEAK (+120, below threshold)
└─ Signal Tier: ⚠️ MODERATE (45.5/100 - selective)

STRUCTURE ANALYSIS:
├─ Recent Swing High: 191.45 (target zone)
├─ Recent Swing Low: 188.20 (support zone)
├─ VWAP: 189.80 (should hold above)
└─ Key Support Below: 186.60 (stronger support)

POSITION SIZING:
├─ Account Balance: $23,105.83
├─ Risk @ 1%: $231
├─ Stop Distance: $1.30
├─ Position Size: 177 shares
├─ Capital Required: $33,573
└─ ⚠️ ISSUE: Insufficient cash for full position
   ADJUSTMENT: 122 shares ($15,861 capital used)
   ADJUSTED RISK: $158.60 (0.69% account)

WINGMAN ASSESSMENT: 8/10 PASS
├─ Confluences: 9/9 technical checks passed ✅
├─ Warnings: 2 minor (breadth weak, cash adjusted)
└─ Recommendation: GO (with position adjustment)

PROCEED WITH ENTRY? (yes/no/check something)
```

**Ratings:**
- 9-10/10: **GO** - All systems aligned
- 7-8/10: **CAUTION** - Proceed but small size
- 5-6/10: **HOLD** - Wait for better setup
- <5/10: **BLOCK** - Wingman blocks unless you override

#### Step 3: Execution & Recording
You confirm "Yes"

**Wingman records:**
```
✓ ENTRY RECORDED - NVDA LONG
├─ Quantity: 122 shares
├─ Entry Price: $189.50
├─ Capital Used: $23,099
├─ Cash Remaining: $6.83
├─ Stop Loss: $188.20 (risk $158.60)
├─ T1: $191.45 @ 50% exit (+$119)
├─ T2: $193.20 @ 30% exit (+$207)
├─ T3: Runner with trail
├─ Alerts: Set for stop and targets
└─ Status: LIVE

Watching your six. Good hunting.
```

---

### PHASE 3: POSITION MANAGEMENT

**Real-Time Tracking:**
```
NVDA LONG: 122 shares @ 189.50

Current Price: $190.20 (+$0.70 from entry, +0.37%)
├─ Current P/L: +$85.40 (+0.37% of account)
├─ Distance to T1: $1.25 (getting close)
├─ Distance to Stop: $2.00 (healthy)
├─ Time in Trade: 12 minutes
└─ Status: ON TARGET

Action: Monitor for T1 hit @ 191.45
```

**Wingman prevents early exits:**
- You cannot exit before targets without reason
- If you want to exit early, Wingman asks: "Why? This breaks your T1 target system"
- Logs any overrides for later analysis

#### Exit Rules
**T1 Hit (191.45):**
```
✓ T1 HIT! NVDA @ 191.45
├─ Exit 50% (61 shares) for +$119
├─ Remaining: 61 shares (runner position)
├─ Stop moved to: $189.50 (breakeven)
├─ New T2 target: $193.20
└─ Daily P/L: +$119 (toward $125 daily goal)
```

**T2 Hit (193.20):**
```
✓ T2 HIT! NVDA @ 193.20
├─ Exit 30% (37 shares) for +$207
├─ Remaining: 24 shares (runner)
├─ Stop moved to: $190.00 (small profit)
└─ Daily P/L: +$326 (exceeded $125 daily goal)
```

**T3 Management:**
```
Runner 24 shares @ 189.50 (stop)
├─ No target set (let it run)
├─ Stop adjusts: -1 x ATR every bar
├─ Exit when: Stop hit OR price reverses pattern
└─ Possible outcomes: +$500 or breakeven
```

**Stop Hit:**
```
✗ STOP HIT: NVDA @ 188.20
├─ Exit all remaining shares
├─ Loss: -$158.60 (1% risk accepted)
├─ Daily P/L: +$168 (T1/T2 minus loss)
└─ Trade outcome: 2W1L, +$168 net
```

---

### PHASE 4: END OF DAY AUTOMATION

**Command:** `"wingman, eod wrap"`

**Wingman generates:**
1. Full journal entry with all trades from session
2. Compliance report (rules followed/broken)
3. P/L breakdown (by trade, by timeframe, by instrument)
4. Performance analysis (win rate, R:R, discipline)
5. Tomorrow's preview (setups to watch if swing positions open)

---

## STOP LOSS CALCULATION METHODS

### Method 1: ATR-Based (Primary)
**Formula:** Entry Price - (1.5 × ATR)
- Uses volatility to set dynamic stops
- Works across all timeframes
- More room in volatile markets, tighter in calm markets

**Example:**
```
Entry: $189.50
ATR(14): $0.87
Stop: $189.50 - (1.5 × $0.87) = $189.50 - $1.30 = $188.20
Risk: $1.30 per share
```

### Method 2: Structure-Based (Secondary)
**Logic:** Place stop just below recent support or above recent resistance
- Most intuitive
- Works best with clear levels
- Prevents line-in-the-sand stops

**Example:**
```
Entry: $189.50 (breakout)
Recent Swing Low: $188.20
Stop: $188.20 - $0.05 = $188.15 (just below)
Risk: $1.35 per share
```

### Method 3: Time-Based (Tactical)
**Logic:** Exit if no progress within X minutes
- Prevents getting stuck in sideways chop
- Tightens risk in indecision zones
- Use for intraday only

**Example:**
```
Entry: $189.50
Time limit: 15 minutes
If no movement toward T1 in 15 min → Exit for small loss
Use only in high-chop environments
```

### Method 4: Percentage-Based (Not Recommended)
**Formula:** Entry Price × (1 - Risk %)
- Mechanical, ignores structure
- Can be too tight or too wide
- Only use as fallback

**Example:**
```
Entry: $189.50
2% risk: $189.50 × 0.98 = $185.71
Risk: $3.79 per share (too large, avoid)
```

---

## TARGET CALCULATION SYSTEMS

### System 1: Risk/Reward Ratio (Primary)
**T1:** Entry + (Risk × 1.5)
**T2:** Entry + (Risk × 2.5)
**T3:** Entry + (Risk × 4.0)

**Example:**
```
Entry: $189.50
Stop: $188.20
Risk per share: $1.30

T1: $189.50 + ($1.30 × 1.5) = $191.45 (1.5R)
T2: $189.50 + ($1.30 × 2.5) = $192.75 (2.5R)
T3: $189.50 + ($1.30 × 4.0) = $194.70 (4.0R)

Exit plan:
├─ 50% @ T1 ($191.45) = +$119
├─ 30% @ T2 ($192.75) = +$163
└─ 20% @ T3 ($194.70) = +$201 or runner
```

### System 2: Fibonacci Extensions (Secondary)
**Basis:** Recent swing low to high
**Targets:** 1.618×, 2.618×, 4.236× extensions

**Example:**
```
Swing Low: $186.00
Swing High: $189.00
Range: $3.00

Extensions from Entry $189.50:
├─ 1.618×: $189.50 + ($3.00 × 1.618) = $194.36
├─ 2.618×: $189.50 + ($3.00 × 2.618) = $197.35
└─ 4.236×: $189.50 + ($3.00 × 4.236) = $201.21
```

### System 3: Previous Structure Levels (Secondary)
**Logic:** Target recent swing highs, resistance levels, round numbers
**Strength:** Based on actual price history

**Example:**
```
Recent Swing High: $191.45 → T1
Previous Major High: $193.20 → T2
Next Resistance: $195.00+ → T3
```

### System 4: Ichimoku Cloud Extensions (Advanced)
**Uses:** Cloud top, cloud bottom, previous cloud positions
**Strength:** Multi-timeframe validation

**Example:**
```
4H Cloud Top: $192.50
1H Cloud Top: $190.50
Daily Cloud Top: $194.00

T1: $190.50 (1H cloud)
T2: $192.50 (4H cloud)
T3: $194.00+ (daily cloud, let runner)
```

### RECOMMENDED APPROACH
**Use System 1 (R:R) for primary targets**
- Simple, mechanical, consistent
- T1: 1.5R (quick profit, rebuild capital)
- T2: 2.5R (secondary profit, reduce position)
- T3: 4.0R+ (runner, let winners run)

**Cross-check with System 3 (Structure)**
- Confirm targets align with recent highs
- Avoid targets in extreme white space (low probability)

---

## MULTI-INSTRUMENT SCANNER SPECIFICATIONS

### Instruments Scanned
```
ALWAYS (Core):
├─ SPY (stock index)
├─ QQQ (tech index)
├─ ES (S&P 500 futures)
└─ NQ (Nasdaq futures)

SECONDARY (Top Stocks):
├─ NVDA (AI mega-cap)
├─ TSLA (Mega-cap)
├─ AAPL (Mega-cap)
├─ MSFT (Mega-cap)
├─ AMZN (Mega-cap)
├─ META (Mega-cap)
├─ GOOGL (Mega-cap)
├─ AMD (Chip leader)
├─ NFLX (Streaming)
└─ COIN (Crypto proxy)

CRYPTO (24/7):
├─ BTC (Bitcoin)
├─ ETH (Ethereum)
└─ SOL (Solana)

CUSTOM (Your choice):
└─ Add any you want to track
```

### Timeframes Analyzed
```
Per Instrument:
├─ Daily (trend, support/resistance)
├─ 4H (momentum alignment)
├─ 1H (setup formation)
├─ 15-min (entry trigger zone)
└─ 5-min (fine entry timing)
```

### Confluence Score Calculation
```
Each timeframe scored 0-10:
├─ Trend (MA alignment): 0-3 pts
├─ Momentum (RSI/MACD): 0-2 pts
├─ Volume (spike confirmation): 0-2 pts
├─ Structure (S/R, VWAP): 0-2 pts
└─ Context (breadth, divergence): 0-1 pt

Total per timeframe: 0-10
Average across timeframes: 0-10
Multiply by instrument confluence: 0-100%

Example:
Daily: 8/10
4H: 7/10
1H: 9/10
15-min: 8/10
Average: 8.0/10 = 80% confidence
Instrument confluence factor: 1.0
FINAL SCORE: 80%
```

---

## THREAT ASSESSMENT FRAMEWORK

### Pre-Entry Checklist (10 Point System)
```
1. DIRECTION ALIGNMENT (1 point)
   ✓ Daily trend + 4H momentum agree
   ✗ Daily vs 4H divergence

2. RSI POSITIONING (1 point)
   ✓ For longs: 30-70 range (room to run)
   ✓ For shorts: 30-70 range (room to drop)
   ✗ For longs: >70 (overbought, overextended)
   ✗ For shorts: <30 (oversold, could bounce)

3. VOLUME CONFIRMATION (1 point)
   ✓ Entry bar >= 1.3x 20-bar average
   ✗ Light volume on entry

4. VWAP ALIGNMENT (1 point)
   ✓ Long entry: above VWAP or touching from below
   ✓ Short entry: below VWAP or touching from above
   ✗ Entry against VWAP structure

5. ICHIMOKU CLOUD (1 point)
   ✓ Price above cloud (uptrend)
   ✓ Price below cloud (downtrend)
   ✗ Price inside cloud (uncertain)

6. QQQ/SPY DIVERGENCE (1 point)
   ✓ No divergence (aligned direction)
   ✓ Divergence supporting your trade
   ✗ Major divergence against trade

7. BREADTH SUPPORT (1 point)
   ✓ ADD improving or stable >0
   ✓ Up-volume >50%
   ✗ ADD falling / up-volume <40%

8. SIGNAL TIER ALIGNMENT (1 point)
   ✓ STRONG/MODERATE tier (aligned)
   ✓ WEAK tier but high-probability setup
   ✗ AVOID/WEAK tier with low confluence

9. POSITION SIZING (1 point)
   ✓ Risk = 1% of account ($231)
   ✓ Cash available for position
   ✗ Insufficient cash

10. STRUCTURE CONFIRMATION (1 point)
    ✓ Clear support/resistance zone
    ✓ VWAP touching key level
    ✓ Recent pivot confirmed
    ✗ Entering in white space

SCORING:
9-10 points: GO (all systems aligned)
7-8 points: CAUTION (minor warnings, small size)
5-6 points: HOLD (wait for better setup)
<5 points: BLOCK (insufficient confluence)
```

---

## IMPLEMENTATION ROADMAP

### Phase 1: FOUNDATION (Week 1-2)
**Deliverables:**
- [ ] Morning scanner (Python)
- [ ] Entry confluence checker (Python)
- [ ] Stop/target calculator (Python)
- [ ] ThinkorSwim integration for alerts
- [ ] Manual testing with paper trades

**Time Estimate:** 5-10 sessions

### Phase 2: AUTOMATION (Week 3-4)
**Deliverables:**
- [ ] Position manager (background process)
- [ ] Real-time P/L tracking
- [ ] Alert system integration
- [ ] EOD automation
- [ ] Command Center dashboard enhancements

**Time Estimate:** 5-10 sessions

### Phase 3: OPTIMIZATION (Week 5-6)
**Deliverables:**
- [ ] Performance analytics
- [ ] Rule effectiveness scoring
- [ ] Win rate by setup type analysis
- [ ] Ichimoku scanner integration
- [ ] Advanced Fibonacci extensions

**Time Estimate:** 5-10 sessions

### Phase 4: SCALING (Week 7+)
**Deliverables:**
- [ ] Multi-chart monitoring dashboard
- [ ] Automated order entry (if desired)
- [ ] Crypto 24/7 scanner
- [ ] Advanced macro integration
- [ ] Machine learning on setup selection

**Time Estimate:** Ongoing

---

## DAILY ROUTINE (Once Implemented)

### PRE-MARKET (8:00 AM - 9:30 AM)
1. "i know kung fu" → Load Wingman
2. Review morning scanner output (top 5 opportunities)
3. Select 1-3 setups to watch
4. Review alerts and key levels
5. Pre-plan responses to market moves

### MARKET OPEN (9:30 AM - 11:00 AM)
1. Monitor setups
2. When trigger hits → "Wingman, entry check [TICKER]"
3. Review confluence checklist
4. Confirm entry if 8+/10
5. Manage position toward T1

### MID-DAY (11:00 AM - 3:00 PM)
1. Manage open positions
2. Hit targets, take profits
3. Watch for new opportunities
4. Secondary market setups (crypto, swing)

### POWER HOUR (3:00 PM - 4:00 PM)
1. Final trading window
2. Clean up positions
3. Prepare for next session
4. Notes on today's performance

### POST-MARKET (4:00 PM - 5:00 PM)
1. "wingman, eod wrap" → Generate journal
2. Review today's trades
3. Log lessons learned
4. Update continuity files
5. Celebrate wins, learn from losses

---

## RISK CHECKLIST (BEFORE EVERY TRADE)

```
❑ Confluence score 8+/10?
❑ Multi-timeframe aligned?
❑ Stop calculated (ATR-based)?
❑ Targets calculated (1.5R / 2.5R / 4.0R)?
❑ Position size = 1% risk?
❑ Cash available for position?
❑ Daily loss limit not exceeded?
❑ Signal tier >= MODERATE?
❑ Risk/Reward >= 1:1.5?
❑ Entered checklist items, not gut?

If ANY box unchecked → DO NOT ENTER
```

---

## SUCCESS METRICS

### Monthly Targets
- **Trades:** 10-20 per month
- **Win Rate:** 65-70%
- **Avg Winner:** $175+ (1.5R+)
- **Avg Loser:** $231 (1R)
- **Profit Target:** $2,500+

### Weekly Checkpoints
- Monday: Scan quality (top 5 opportunities on track)
- Wednesday: Win rate (60%+ so far this week)
- Friday: Weekly P/L ($500+ toward goal)

### Daily Metrics
- Confluence score of entries (8+/10)
- Hits per confluence score (do higher scores win more?)
- Rule compliance (% of rules followed)
- Daily P/L progress toward $125 goal

---

## NOTES FOR FUTURE REVIEW

### Questions to Answer After First 10 Trades
1. Which confluence factors matter most? (weighted adjustment)
2. What's the actual win rate per setup type?
3. Do ATR-based stops or structure-based stops work better?
4. Is 1.5R/2.5R/4.0R spacing optimal, or adjust?
5. Which instruments have best setups? (Focus there)

### Rules to Potentially Add
- Minimum volume requirement (filter low-volume gaps)
- Time-of-day bias (which hours have best setups)
- Macro calendar integration (avoid news volatility)
- Correlation tracking (QQQ/SPY divergence automation)

### Optimization Opportunities
- Machine learning on confluence weighting
- Seasonal pattern overlay (Sept/Oct weakness, etc.)
- VIX/IV regime adjustment (wider stops in volatility spikes)
- Personal psychology matching (when do YOU perform best?)

---

## APPENDIX: GLOSSARY

**Confluence:** Multiple indicators/systems agreeing on same direction = high probability

**R:R (Risk/Reward):** Potential profit ÷ Potential loss (e.g., 1.5R means 1.5x your risk)

**ATR:** Average True Range = volatility measure

**VWAP:** Volume Weighted Average Price = where institutional orders cluster

**Ichimoku Cloud:** Multi-timeframe indicator showing trend/support/resistance

**Divergence:** Price going one direction while indicator goes another (warning sign)

**Breadth:** % of stocks participating in move (ADD = advance/decline)

**Confluence Checker:** Pre-entry system that grades setups 0-10

**Scanner:** Automated system that finds opportunities across all instruments

**Position Manager:** Real-time system tracking open positions and P/L

**Wingman:** Your AI trading partner executing the system

---

**Status:** DESIGN PHASE - READY FOR PHASED IMPLEMENTATION

**Next Step:** Review piece by piece, confirm each phase before building

**Questions?** Document them and we'll address during implementation
