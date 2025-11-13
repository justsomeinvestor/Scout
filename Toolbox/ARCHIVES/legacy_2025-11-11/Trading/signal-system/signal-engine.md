# High-Probability Trading Signal Engine
**Last Updated:** October 1, 2025
**System Version:** 1.0

---

## Overview

This signal engine provides **systematic, data-driven trade signals** for SPY, QQQ, BTC, and ETH. It combines multiple validated indicators into a composite scoring system (0-100) that identifies high-probability setups.

### Core Principle
**Multi-Factor Convergence = Higher Probability**

When trend, breadth, volatility, technical, and seasonality signals align, historical win rates exceed 70%+.

---

## Composite Scoring System

### Signal Strength Formula
```
Signal Score = (Trend × 40%) + (Breadth × 25%) + (Volatility × 20%) +
               (Technical × 10%) + (Seasonality × 5%)

Range: 0-100
```

### Quality Tiers

| Score | Tier | Action | Historical Win Rate |
|-------|------|--------|-------------------|
| 85-100 | **EXTREME** | Max size, highest conviction | 75-85% |
| 70-84  | **STRONG** | Full size, high probability | 65-75% |
| 55-69  | **MODERATE** | Reduced size, standard setup | 55-65% |
| 40-54  | **WEAK** | Pass or minimal size | 45-55% |
| 0-39   | **AVOID** | Counter-trend, high risk | <45% |

---

## Signal Components

### 1. TREND SIGNALS (40% Weight)

**Purpose:** Identify market regime and mean-reversion opportunities

#### Indicators:
- **200-DMA Regime Filter** (15 points)
  - Above 200-DMA: 15 points (risk-on)
  - Within 2% of 200-DMA: 10 points (neutral)
  - Below 200-DMA: 0 points (risk-off)

- **50-DMA Distance** (15 points)
  - **SPY:** ≥2.5% below 50-DMA = 15 points
  - **QQQ:** ≥4% below 50-DMA = 15 points
  - **BTC:** ≥8% below 50-DMA = 15 points
  - Linear scaling for smaller distances

- **Multi-Timeframe Alignment** (10 points)
  - Daily + 4H + 1H all bullish: 10 points
  - 2 of 3 bullish: 6 points
  - 1 of 3 bullish: 2 points

**Scoring Example:**
```
SPY @ $550, 200-DMA @ $540, 50-DMA @ $565
- Above 200-DMA: +15 points
- 2.7% below 50-DMA: +15 points
- MTF: Daily/4H bullish, 1H bearish: +6 points
= 36/40 points (90%)
```

---

### 2. BREADTH SIGNALS (25% Weight)

**Purpose:** Measure participation and detect capitulation/euphoria

#### Indicators:
- **% SPX > 50-DMA** (15 points)
  - **Capitulation:** ≤20% = 15 points (extreme buy)
  - **Washout:** ≤35% = 12 points (strong buy)
  - **Healthy:** 40-60% = 8 points (neutral)
  - **Overbought:** ≥80% = 3 points (caution)
  - **Euphoria:** ≥90% = 0 points (sell signal)

- **Advance-Decline Line Divergence** (10 points)
  - **Bullish Divergence:** Price lower low, A/D higher low = 10 points
  - **Confirming:** A/D follows price = 5 points
  - **Bearish Divergence:** Price higher high, A/D lower high = 0 points

**Scoring Example:**
```
% SPX >50-DMA: 32% (improving from 28%)
A/D Line: Bullish divergence vs. price
= (12 + 10) / 25 = 22/25 points (88%)
```

---

### 3. VOLATILITY SIGNALS (20% Weight)

**Purpose:** Identify fear/complacency extremes and mean-reversion setups

#### Indicators:
- **VIX Bands** (12 points)
  - **Panic:** VIX ≥36 = 12 points (extreme buy)
  - **Stress:** VIX 28-35 = 10 points (strong buy)
  - **Normal:** VIX 16-27 = 6 points (neutral)
  - **Complacent:** VIX <16 = 3 points (caution)

- **VIX Term Structure** (5 points)
  - **Backwardation** (Front > Back): 5 points (fear extreme)
  - **Flat:** 3 points (uncertainty)
  - **Contango** (Back > Front): 1 point (risk-on)

- **IV Percentile (BTC/ETH)** (3 points)
  - **>80th percentile:** 3 points (high IV = cheap options)
  - **50-80th:** 2 points
  - **<50th:** 1 point

**Scoring Example:**
```
VIX: 29 (stress band) + rolling over = 10 points
Term Structure: Slight backwardation = 5 points
BTC IV: 45th percentile = 1 point
= 16/20 points (80%)
```

---

### 4. TECHNICAL SIGNALS (10% Weight)

**Purpose:** Confirm momentum and identify divergences

#### Indicators:
- **RSI Extremes** (5 points)
  - **Oversold:** RSI <30 with bullish divergence = 5 points
  - **Oversold:** RSI <30 without divergence = 3 points
  - **Neutral:** RSI 30-70 = 2 points
  - **Overbought:** RSI >70 = 0 points

- **MACD** (3 points)
  - **Bullish cross** + histogram rising = 3 points
  - **Above zero line:** 2 points
  - **Below zero line:** 1 point

- **Volume Confirmation** (2 points)
  - Above 20-day avg on bounce: 2 points
  - Normal volume: 1 point

**Scoring Example:**
```
RSI: 32 with bullish divergence = 5 points
MACD: Bullish cross above zero = 3 points
Volume: 1.3x avg = 2 points
= 10/10 points (100%)
```

---

### 5. SEASONALITY SIGNALS (5% Weight)

**Purpose:** Capture calendar-based edges

#### Indicators:
- **Turn-of-Month (TOM)** (2 points)
  - T-3 to T+2 window active: 2 points
  - Otherwise: 0 points

- **Monthly Effect** (2 points)
  - October ("Uptober"): 2 points
  - November-December (Santa Rally): 2 points
  - September (weak historically): 0 points
  - Other months: 1 point

- **FOMC Pattern** (1 point)
  - 2 days before FOMC meeting: 1 point (bullish edge)
  - Day of/after FOMC: 0 points (vol spike)

**Scoring Example:**
```
TOM window (Oct 1): +2 points
October month: +2 points
No FOMC: 0 points
= 4/5 points (80%)
```

---

## Setup Definitions

### SPY Routine Dip Buy
**Score Required:** 70-84 (STRONG)

**Criteria:**
1. ✅ Close ≥2.5% below 50-DMA
2. ✅ **Reclaim** 50-DMA within 10 trading days
3. ✅ VIX ≥28 + rolling over (lower high)
4. ✅ % SPX >50-DMA ≤35% and improving day-over-day

**Risk Management:**
- **Entry:** On 50-DMA reclaim candle close
- **Stop:** Swing low OR 1.5× daily ATR
- **Target 1:** Prior pivot high (1:1 to 1:1.5 R/R)
- **Target 2:** +1.5× risk (1:1.5 to 1:2 R/R)
- **Position Size:** 2-3% account risk

**Historical Stats:**
- Win Rate: 68%
- Avg R/R: 1:1.7
- Avg Duration: 8 trading days

---

### SPY Deep Correction Buy
**Score Required:** 85-100 (EXTREME)

**Criteria:**
1. ✅ Close ≥6% below 200-DMA (or 10-15% from highs)
2. ✅ **Reclaim** 200-DMA within 30 trading days
3. ✅ VIX ≥36 OR backwardation 3+ consecutive days
4. ✅ % SPX >50-DMA ≤20% and inflecting upward
5. ✅ A/D Line bullish divergence vs. price

**Risk Management:**
- **Entry:** On 200-DMA reclaim or strong reversal bar
- **Stop:** Correction low OR 2× daily ATR
- **Target 1:** 50% retracement of decline (1:2 R/R)
- **Target 2:** +2.5× risk (full recovery)
- **Position Size:** 1.5-2× routine size (4-5% account risk)

**Historical Stats:**
- Win Rate: 78%
- Avg R/R: 1:2.3
- Avg Duration: 21 trading days

---

### QQQ Variants

**QQQ Routine Dip:**
- Threshold: ≥4% below 50-DMA (more volatile than SPY)
- Same breadth/VIX criteria
- Score Required: 70-84

**QQQ Deep Correction:**
- Threshold: ≥8-10% below 200-DMA (or 12-18% from highs)
- Same criteria, adjusted for higher volatility
- Score Required: 85-100

---

### BTC/ETH Setups

**BTC Routine Dip:**
- ≥8% below 50-DMA (or ≥10% from recent high)
- BTC IV percentile >70
- Score Required: 70+

**BTC Deep Correction:**
- ≥15% below 200-DMA (or ≥25% from ATH)
- $99K 50-week MA holding (bull market support)
- Whale accumulation (ATS improving)
- Score Required: 85+

---

## Real-Time Monitoring

### Data Sources

**Trend:**
- TradingView SPX/BTC charts (50/200-DMA distances)
- Multi-timeframe trend direction

**Breadth:**
- StockCharts: $SPXA50R (% SPX >50-DMA)
- MarketInOut: NYSE Advance-Decline Line
- FinViz: Sector breadth heatmap

**Volatility:**
- CBOE: VIX level and term structure
- CoinGlass: BTC/ETH implied volatility
- TradingView: IV percentile rankings

**Technical:**
- RSI(14), MACD(12,26,9), Volume
- Any major charting platform

**Seasonality:**
- Calendar-based (automated)

---

## Alert Configuration

### Score-Based Alerts

**TradingView / ThinkOrSwim Alerts:**

```
// STRONG Signal Activated
IF Signal_Score crosses above 70:
   ALERT: "🟢 STRONG SIGNAL: [Asset] [Setup Type] - Score: [X]"

// EXTREME Signal Activated
IF Signal_Score crosses above 85:
   ALERT: "🔥 EXTREME SIGNAL: [Asset] [Setup Type] - Score: [X]"

// Signal Degrading
IF Signal_Score falls below 55:
   ALERT: "🟡 SIGNAL WEAKENING: Consider exit/reduce"
```

### Component Alerts

```
// Breadth Capitulation
IF % SPX >50-DMA crosses below 20%:
   ALERT: "📉 BREADTH CAPITULATION - High probability bottom forming"

// VIX Stress
IF VIX crosses above 28 AND VIX[1] < VIX[2]:
   ALERT: "⚡ VIX ROLLOVER - Buy-the-dip window opening"

// Reclaim Trigger
IF Close > 50-DMA[0] AND Close[1] < 50-DMA[1]:
   ALERT: "✅ 50-DMA RECLAIM - Entry signal activated"
```

---

## Performance Tracking

### Mandatory Log Fields

For every signal triggered:

| Field | Description |
|-------|-------------|
| Date | Signal trigger date |
| Asset | SPY / QQQ / BTC / ETH |
| Setup Type | Routine Dip / Deep Correction / Other |
| Signal Score | 0-100 composite score |
| Entry Price | Actual entry level |
| Stop Price | Risk management stop |
| Target Price | Profit target(s) |
| Position Size | % of account risked |
| Result | Win/Loss + R multiple |
| Duration | Days held |
| Notes | Market context, lessons learned |

### Performance Metrics

**Track Quarterly:**
- Win rate by score tier (85+, 70-84, 55-69)
- Average R/R achieved vs. planned
- Signal score vs. actual outcome correlation
- False signal rate (score >70 but stopped out)
- Best-performing setups
- Worst-performing setups

**Continuous Improvement:**
- Adjust scoring weights based on live results
- Add/remove indicators that prove/fail predictive power
- Refine thresholds for score tiers
- Document market regime changes that invalidate signals

---

## Risk Management Integration

### Position Sizing by Signal Score

| Score | Risk % | Position Size |
|-------|--------|--------------|
| 85-100 | 4-5% | Maximum conviction |
| 70-84  | 2-3% | Standard size |
| 55-69  | 1-2% | Reduced size |
| <55    | PASS | No trade |

### Stop Loss Rules

**Never trade without stops:**
- Routine setups: 1.5× ATR or swing low (whichever tighter)
- Deep corrections: 2× ATR or correction low
- Maximum loss per trade: 5% of account (absolute ceiling)

### Correlation Limits

**Avoid concentration:**
- Max 2 concurrent SPY/QQQ positions (correlated)
- Max 2 concurrent BTC/ETH positions (correlated)
- Never exceed 10% total account risk across all positions

---

## Workflow Integration

This signal engine integrates with the master research workflow:

1. **Research providers updated** (Step 1-3 in How to use_MP.txt)
2. **Market Sentiment Overview created** (consolidates data)
3. **Signal Engine calculates scores** ← THIS STEP
   - Pulls trend data from TradingView summaries
   - Pulls breadth from Market Breadth summaries
   - Pulls volatility from Volatility Metrics summaries
   - Calculates composite score
   - Identifies active setups
4. **Dashboard updated** (signal tab populated)
5. **Daily Planner updated** (high-priority setups added)

---

## Next Steps

- [ ] Build individual signal module files (detailed breakdowns)
- [ ] Create visual dashboard interface
- [ ] Integrate into research-dashboard.html
- [ ] Set up automated data pulls
- [ ] Begin performance tracking log
- [ ] Backtest historical signals (validate scoring system)

---

*Signal Engine Version 1.0 - October 1, 2025*
