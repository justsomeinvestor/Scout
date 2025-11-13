# Risk Management Rules

**Purpose:** Mechanical trading rules to protect capital and enforce discipline
**Philosophy:** Never risk more than you can afford; preserve capital; let winners run
**Framework Version:** 1.0
**Last Updated:** 2025-10-19

---

## Table of Contents

1. [Position Sizing Rules](#position-sizing-rules)
2. [Stop Loss Placement Standards](#stop-loss-placement-standards)
3. [Profit Target Standards](#profit-target-standards)
4. [Risk/Reward Requirements](#riskReward-requirements)
5. [Account Protection Rules](#account-protection-rules)
6. [Pre-Trade Checklist](#pre-trade-checklist)
7. [Trade Management Rules](#trade-management-rules)
8. [Exit Rules](#exit-rules)

---

## Position Sizing Rules

### Core Principle

**Never risk more than 2% of account on single trade.**

This ensures that even 10 consecutive losses only result in ~18% drawdown (recoverable)

### The Formula

```
POSITION_SIZE = (ACCOUNT_SIZE × RISK_PERCENTAGE) / (ENTRY_PRICE - STOP_PRICE)

Example:
  Account: $20,000
  Risk: 2% ($400)
  Entry: 192.50
  Stop: 190.00
  Distance: 2.50

  Position Size = $400 / $2.50 = 160 shares
```

### Risk Percentage Guidelines (By Account Size)

| Account Size | Recommended Risk % | $ Risk per Trade |
|---|---|---|
| $5,000 | 1% | $50 |
| $10,000 | 1.5% | $150 |
| $20,000 | 2% | $400 |
| $50,000 | 2% | $1,000 |
| $100,000 | 1.5% | $1,500 |
| $250,000 | 1% | $2,500 |
| $500,000+ | 0.5% | $2,500 |

**Rationale:**
- Smaller accounts: More aggressive (need growth)
- Medium accounts: Standard 2% (proven optimal)
- Large accounts: More conservative (absolute $ risk stays same)

### Volatility Adjustments

**Increase Risk % if volatility is LOW (VIX < 12):**
- Normal risk: 2%
- Low volatility: Can increase to 2.5%
- Rationale: Tighter stops needed = smaller distance = more shares = higher risk $

**Decrease Risk % if volatility is HIGH (VIX > 25):**
- Normal risk: 2%
- High volatility: Reduce to 1-1.5%
- Rationale: Wider stops needed = larger distance = same $ risk

### Sector/Instrument Adjustments

| Instrument | Base Risk | Adjustment | Reason |
|---|---|---|---|
| Large cap (SPY) | 2% | +0.5% | Less volatile |
| Tech (QQQ) | 2% | -0.5% | More volatile |
| Small cap (Russell) | 2% | -1.0% | Highly volatile |
| Futures (ES) | 1% | — | High leverage |
| Options (calls/puts) | 1% | — | Decay risk |

### Portfolio Heat (Maximum Concurrent Risk)

**Maximum total $ at risk simultaneously:**

| Account Size | Max Portfolio Heat |
|---|---|
| $20,000 | $800 (4 trades at $200 each) |
| $50,000 | $2,500 (5 trades at $500 each) |
| $100,000 | $4,000 (4 trades at $1,000 each) |
| $250,000 | $7,500 (5 trades at $1,500 each) |

**Rule:** Never have more than 5 concurrent open trades

**Why:**
- Prevents "death by 1000 cuts"
- Ensures attention to each trade
- Limits catastrophic loss scenarios

### Example Position Sizing Decision

```
Account: $23,000
Current Portfolio Heat: $400 (1 open trade)
Max Heat Allowed: $920
Remaining Heat Budget: $520

New Setup Analysis:
  Ticker: NVDA
  Entry: 192.50
  Stop: 190.00
  Risk Distance: $2.50

Position Size Calculation:
  Can risk: Min($400, 2% of $23,000) = $400
  Position Size: $400 / $2.50 = 160 shares

Compliance Check:
  New portfolio heat: $400 + $400 = $800
  Max allowed: $920
  Status: ✓ APPROVED (under limit)

Execution: Buy 160 shares NVDA at $192.50
```

---

## Stop Loss Placement Standards

### Core Principle

**Stops must be placed at a LOGICAL price level, not arbitrary distance**

Stop should be where "the setup is broken"

### Stop Loss Rules by Pattern Type

#### Chart Pattern Stops

**Head & Shoulders Breakdown:**
- Stop: Just above right shoulder high
- Example: Right shoulder = 193.00 → Stop = 193.25
- Reasoning: If price reclaims shoulder, pattern fails

**Triangle Breakout:**
- Stop: Opposite side of triangle from breakout direction
- Example: Ascending triangle breaks up → Stop just below upper trendline
- Reasoning: Breakout failure indicated

**Flag/Pennant Breakout:**
- Stop: Just beyond the rectangle/pennant opposite side
- Example: Bullish flag → Stop just below flag low
- Reasoning: Mean reversion into flag indicates failure

**Wedge Breakout:**
- Stop: Opposite side of wedge from entry
- Example: Bullish wedge breakout → Stop below support
- Reasoning: Wedge support breaks = trend failed

#### Trend-Based Stops

**Moving Average Support Bounce:**
- Stop: Just below the EMA that provided support
- Example: Price bounces off EMA 50 → Stop 1-2% below EMA 50
- Reasoning: If MA penetrated, trend broken

**Trendline Bounce:**
- Stop: Just beyond the trendline opposite side
- Example: Uptrend line support at 190 → Stop at 189.75
- Reasoning: Trendline break = trend failure

**Divergence Breakout:**
- Stop: Just beyond the swing low/high (opposite of entry)
- Example: Bullish divergence, price breaks swing high → Stop below swing low
- Reasoning: If swings reset lower, divergence failed

#### Level-Based Stops

**Support/Resistance Breakout:**
- Stop: Just beyond the support/resistance level broken
- Example: Breaks above 192 resistance → Stop at 191.50
- Reasoning: Rejection back below level = false breakout

**Pivot Point Stop:**
- Stop: Opposite pivot from target
- Example: Long entry → Stop at S1 or S2
- Reasoning: Pivot penetration = loss of support

### Stop Loss Distance Guidelines

**Minimum Stop Distance** (to avoid whipsaws):
- Large cap (SPY, large tech): 1-2% from entry
- Mid-cap: 2-3% from entry
- Small cap: 3-5% from entry
- Futures: 0.5-1% from entry (points)

**Maximum Stop Distance** (to limit loss):
- Any trade: Not more than 5% from entry
- Exceptions: Earnings setups can be 7-10%

**VIX Adjustments:**
- If VIX < 12 (low volatility): Tighter stops (minimum 0.75%)
- If VIX > 30 (high volatility): Wider stops (maximum 5%)

### Stop Loss Examples

```
Example 1: NVDA Resistance Breakout
  Setup: Breaks above $192 resistance
  Entry: $192.50
  Previous resistance level: $190.00
  Logic stop: Just below $191.00 (below support)

  Distance: $192.50 - $191.00 = $1.50
  Percentage: $1.50 / $192.50 = 0.78%
  Status: ✓ Good (within 1-2% for large cap)

Example 2: H&S Breakdown
  Setup: H&S top breaks neckline
  Neckline: $100.00
  Entry: $99.50 (just below neckline)
  Right shoulder high: $102.00
  Logic stop: Just above $102.00
  Stop: $102.25

  Distance: $102.25 - $99.50 = $2.75
  Percentage: $2.75 / $99.50 = 2.76%
  Status: ✓ Good (within 2-3% for pattern)

Example 3: Flag Breakout (Aggressive)
  Setup: Flag breakout
  Entry: $50.00
  Flag high: $50.50
  Flag low: $49.50
  Logic stop: Just below flag low: $49.25

  Distance: $50.00 - $49.25 = $0.75
  Percentage: $0.75 / $50.00 = 1.5%
  Status: ✓ Excellent (tight for flag)
```

---

## Profit Target Standards

### Core Principle

**Targets should be based on TECHNICAL LEVELS, not random percentages**

Target levels come from:
- Resistance levels
- Fibonacci extensions
- Previous swing highs/lows
- Chart pattern measurements

### Profit Target Rules by Pattern Type

#### Chart Pattern Targets

**Head & Shoulders Breakdown:**
- Measure: Distance from head to neckline
- Target: Project that distance below neckline
- Example: Head-neckline = 8 pts → Target = neckline - 8

**Triangle Breakout:**
- Measure: Triangle width at entry point
- Target: Add (or subtract) that width to breakout point
- Example: Triangle width = 12 pts → Target = breakout + 12

**Flag/Pennant:**
- Measure: Flagpole height
- Target: Project flagpole height from breakout
- Example: Flagpole = 20 pts → Target = breakout + 20

**Wedge:**
- Measure: Wedge height at entry
- Target: Project from breakout in direction of move
- Example: Wedge height = 10 pts → Target = breakout + 10

#### Fibonacci Targets

**For Bounces (Retracements):**
- Primary Target: 38.2% retracement
- Secondary Target: 61.8% retracement
- Example: Prior low $100, high $120, retest pullback → Target $117.19 (38.2%)

**For Continuations (Extensions):**
- Primary Target: 161.8% extension
- Secondary Target: 261.8% extension
- Example: Initial move $100→$110 (10 pts up), target pullback, then $110 + (1.618×10) = $126.18

#### Resistance Level Targets

**Primary Target:** Next major resistance level
- Example: Current price $100, entry, next resistance $108 → Target $108

**Secondary Target:** Resistance level beyond that
- Example: $108 primary, $115 secondary

**Tertiary Target:** Major zone or psychological level
- Example: $120 round number, ATH previous

#### Trailing Stops

**Once trade goes 1R in profit (1:1 R:R achieved):**
- Move stop to breakeven (eliminate loss risk)
- Then move stop up by 50% of gains

**Example:**
```
Entry: $100
Stop: $98
Risk: $2 (2R potential with $104 target)

Price moves to $102 (1R gained):
  Move stop to $100 (breakeven)

Price moves to $104 (achieved 2R):
  Move stop to $101 (trailing)

Price moves to $106 (4R gained):
  Move stop to $103 (trailing)

Price moves to $108 (5R gained):
  Move stop to $105 (trailing)

If hits $105 stop: Locked in 5R profit
```

### Partial Profit Taking

**Scale out strategy for larger positions:**

| Trade Portion | Target Level | Action |
|---|---|---|
| 25% | First target (1R) | Close 25% at first target |
| 25% | Second target (2R) | Close 25% at second target |
| 25% | Third target (3R) | Close 25% at third target |
| 25% | Trail stop or max target | Let final 25% run |

**Example:**
```
Position: 100 shares @ $100
Total Risk: $200 (stop at $98)

- 25 shares closed at $102 (1R, +$50)
- 25 shares closed at $104 (2R, +$100)
- 25 shares closed at $106 (3R, +$150)
- 25 shares trail stop at $105 (5R+, +$250+)

Total profit: $550+ (minimum, could be much higher)
```

---

## Risk/Reward Requirements

### Minimum R:R by Setup Type

| Setup Quality | Min R:R | Examples | Notes |
|---|---|---|---|
| High conviction (prob 80%+) | 1:1 | Perfect H&S, clear divergence | Can be lower |
| Good setup (prob 67-79%) | 1:1.5 | Clear pattern, good volume | Standard |
| Moderate setup (prob 51-66%) | 1:2 | Partial confirmation | Required |
| Borderline (prob 34-50%) | 1:3 | Mixed signals | Need strong R:R |
| Wait/Avoid | N/A | — | Don't trade |

### Why These Minimums?

```
If Win Rate = 65%:

With 1:1 R:R:
  Expected profit = (0.65 × 1) + (0.35 × -1) = 0.30 per trade

With 1:1.5 R:R:
  Expected profit = (0.65 × 1.5) + (0.35 × -1) = 0.635 per trade

With 1:2 R:R:
  Expected profit = (0.65 × 2) + (0.35 × -1) = 0.95 per trade
```

Higher R:R compensates for win rate uncertainty

### R:R Calculation Examples

```
Example 1: NVDA Setup
  Entry: 192.50
  Stop: 190.00
  Target: 198.50

  Risk: 192.50 - 190.00 = $2.50
  Reward: 198.50 - 192.50 = $6.00
  R:R = $6.00 / $2.50 = 1:2.4
  Status: ✓ Excellent (well above 1:2 minimum)

Example 2: SPY Support Bounce
  Entry: 425.00
  Stop: 423.00
  Target: 428.00

  Risk: 425.00 - 423.00 = $2.00
  Reward: 428.00 - 425.00 = $3.00
  R:R = $3.00 / $2.00 = 1:1.5
  Status: ✓ Good (meets minimum for this quality)

Example 3: Weak Setup (WAIT)
  Entry: 100.00
  Stop: 98.00
  Target: 101.00

  Risk: 100.00 - 98.00 = $2.00
  Reward: 101.00 - 100.00 = $1.00
  R:R = $1.00 / $2.00 = 1:0.5
  Status: ✗ FAIL (1R negative, skip setup)
```

---

## Account Protection Rules

### Daily Loss Limit

**Maximum daily loss before stopping:**

| Account | Daily Max Loss | Rule |
|---|---|---|
| $20,000 | $400 (2%) | Lose $400 → Stop trading |
| $50,000 | $1,000 (2%) | Lose $1,000 → Stop trading |
| $100,000 | $2,000 (2%) | Lose $2,000 → Stop trading |

**Why:**
- Prevents emotional revenge trading
- Forces reset and reflection
- Protects against catastrophic days

### Weekly Loss Limit

**Maximum weekly loss before pausing:**

| Account | Weekly Max Loss | Rule |
|---|---|---|
| $20,000 | $600 (3%) | Lose $600 → Pause until Monday |
| $50,000 | $1,500 (3%) | Lose $1,500 → Pause until Monday |
| $100,000 | $3,000 (3%) | Lose $3,000 → Pause until Monday |

**Why:**
- Prevents compounding losses
- Forces weekend reflection
- Resets mental state

### Maximum Drawdown Tolerance

**Stop all trading if account drops X% from peak:**

| Drawdown | Action | Duration |
|---|---|---|
| 5% | Review trades, tighten rules | Continue with caution |
| 10% | Pause 1 week, journal analysis | Limited trading only |
| 15% | Pause 2 weeks, full review | No new trades |
| 20%+ | Pause 1 month, restart | Back to basics |

**Why:**
- Protects remaining capital
- Forces systematic analysis
- Prevents "hole digging"

---

## Pre-Trade Checklist

**Before EVERY trade, verify:**

```
☐ 1. Probability Score?
     Yes: Score ≥ 67 (BUY signal)
     No: SKIP this trade

☐ 2. R:R Ratio?
     Yes: R:R ≥ minimum for quality
     No: ADJUST targets or SKIP

☐ 3. Position Size?
     Calculate: (Account Risk% / Stop Distance) = Shares

☐ 4. Stop Loss Placement?
     Logical level (not arbitrary distance)

☐ 5. Portfolio Heat?
     New heat < Max allowed?

☐ 6. Account Protected?
     Daily loss limit not hit?
     Weekly loss limit not hit?

☐ 7. Volume Present?
     Yes: Volume > 20-day average
     No: REDUCE position size 25%

☐ 8. Timeframe?
     Market hours: Yes (continue)
     Pre/after hours: SKIP

☐ 9. News Risk?
     Earnings today? Pre-earnings volatility spike
     Fed announcement? Extreme volatility expected
     If yes: REDUCE position size 25-50%

☐ 10. Final Confirmation?
     Ready to enter? Last chance to say NO
```

---

## Trade Management Rules

### Entry Management

**Once Position is Open:**

1. **Set stops immediately** - Don't wait for perfect price
2. **Verify position size** - Math correct?
3. **Log trade** - Time, price, reason
4. **Watch for 5 minutes** - Initial move confirmation

### Mid-Trade Management

**While position is open:**

```
Every 15 minutes:
  - Check price vs. stop (update if breached)
  - Check price vs. target (lock in if close)
  - Check for news that changes thesis

If hits 50% of target:
  - Close 25% of position (lock in half profit)
  - Move stop to breakeven on remaining

If hits target 1:
  - Close 25% of position (full profit on portion)
  - Raise stop on remaining

If against you 30% of stop:
  - Reassess thesis
  - If thesis broken: Exit immediately
  - If thesis intact: Raise stop or exit half
```

### Exit Triggers

**Exit IMMEDIATELY if any of these occur:**

```
1. Stop loss hit (automatic)
2. Target hit (close at least 25%)
3. Thesis breaks (e.g., support broken despite short setup)
4. Major news that changes outlook (earnings miss, etc.)
5. Time stop hit (if trade lasts > X days)
6. Daily loss limit exceeded
7. Gaps significantly against position (overnight)
```

---

## Exit Rules

### Rule-Based Exits

**Exit position when ANY of these occur:**

| Condition | Action | Reason |
|---|---|---|
| Stop loss triggered | Close 100% | Risk limit exceeded |
| First target hit (1R) | Close 25% | Lock in profit |
| Second target hit (2R) | Close 25% | Secure more profit |
| Divergence reverses | Close remaining | Entry thesis broken |
| Support breaks (in long) | Close 100% | Technical failure |
| Resistance breaks (in short) | Close 100% | Technical failure |
| Volume dries up | Close or reduce | Conviction weakening |
| Time stop (7 days+) | Close remaining | Cut assignment |

### Time-Based Exits

**If trade hasn't moved in X days, consider exit:**

| Timeframe | Rule | Action |
|---|---|---|
| 1-hour trade | 4 hours no movement | Exit 50%, trail 50% |
| 4-hour trade | 2 days no movement | Reassess, likely exit |
| Daily trade | 5 days no movement | Exit position |
| Weekly trade | 3 weeks no movement | Exit position |

### Profit Protection Strategy

**Once achieved 1R (1:1 R:R):**

1. Close 25% (lock in profit)
2. Move stop to **breakeven** on remaining 75%
3. This eliminates loss risk while keeping profit potential

**Once achieved 2R:**

1. Close 25% (more profit secured)
2. Move stop to **1R profit level** on remaining
3. Now guaranteed to make profit, just question is how much

**Once achieved 3R+:**

1. Close 25% more
2. Trail remaining 25% with trailing stop
3. Let winner run while protecting gains

---

## Risk Calculation Worksheet

**Use this template for every trade:**

```
TRADE ANALYSIS TEMPLATE

Ticker: ____________
Entry Price: ____________
Stop Price: ____________
Target Price: ____________

RISK CALCULATION:
Stop Distance: ____________ (Entry - Stop)
Risk %: ____________ (Stop Dist / Entry Price)
Account Size: ____________
Allowed Risk $: ____________ (Account × 2%)
Position Size: ____________ (Risk $ / Stop Distance)

R:R VERIFICATION:
Reward Amount: ____________ (Target - Entry)
R:R Ratio: ____________ (Reward / Risk)
Minimum R:R for Setup: ____________
Pass/Fail: ____________

PORTFOLIO CHECK:
Current Heat: ____________
New Trade Heat: ____________
Total Heat with New: ____________
Max Allowed: ____________
Pass/Fail: ____________

FINAL CHECKLIST:
☐ Probability Score ≥ 67
☐ R:R Meets Minimum
☐ Position Size Calculated Correctly
☐ Portfolio Heat Under Limit
☐ Daily Loss Limit Not Hit
☐ Entry Has Volume

READY TO TRADE: ☐ YES ☐ NO

If NO, what's missing? ___________________________
```

---

**Risk Management Rules Complete**
**Effective Date:** 2025-10-19
**Version:** 1.0
**Philosophy:** Capital preservation above all else
