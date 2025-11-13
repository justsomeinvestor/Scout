# Signal System Integration Summary

## Overview

The high-probability trading signal system is now **fully integrated** into your existing master plan workflow. No separate dashboards—all signals flow through your research-dashboard.html and master-plan.md.

---

## How It Works

### 1. Data Collection (Steps 1-2 of Workflow)

When you run your master plan workflow ([How to use_MP.txt](C:\Users\Iccanui\Desktop\Investing\master-plan\How to use_MP.txt)), you:
- Refresh all provider summaries (YouTube, RSS, Technicals)
- Create Market Sentiment Overview

**This gathers the raw data needed for signal calculations.**

---

### 2. Signal Calculation (Step 3.5 - NEW)

After collecting provider data, calculate composite signal scores using data from your providers:

#### Data Sources → Signal Modules

| Signal Module | Data Source | What to Check |
|---------------|-------------|---------------|
| **Trend (40%)** | TradingView SPX/BTC | 200-DMA regime, 50-DMA distance, multi-timeframe alignment |
| **Breadth (25%)** | Market Breadth provider | % SPX >50-DMA, A/D Line divergence |
| **Volatility (20%)** | Volatility Metrics, CoinGlass | VIX level/direction, term structure, BTC/ETH IV |
| **Technical (10%)** | TradingView SPX/BTC | RSI divergence, MACD cross, volume |
| **Seasonality (5%)** | Calendar | TOM window, monthly effect, FOMC proximity |

#### Composite Score Formula

```
Score = (Trend×40%) + (Breadth×25%) + (Volatility×20%) + (Technical×10%) + (Seasonality×5%)
```

#### Signal Tiers

| Score | Tier | Action |
|-------|------|--------|
| 85-100 | EXTREME BUY | Maximum conviction entry |
| 70-84 | STRONG BUY | High-probability dip buy |
| 55-69 | MODERATE BUY | Decent setup, smaller size |
| 40-54 | WEAK / WAIT | Low conviction, pass |
| 0-39 | AVOID / SELL | No edge, hedge/reduce |

---

### 3. Integration into Master Plan (Step 4)

After calculating signals, update [master-plan.md](C:\Users\Iccanui\Desktop\Investing\master-plan\master-plan.md) JSON with signal data:

#### Add to `dailyPlanner` Object

```json
"signalData": {
  "composite": 72,
  "tier": "STRONG BUY",
  "setup": "SPY Routine Dip",
  "breakdown": {
    "trend": 28,
    "breadth": 17,
    "volatility": 16,
    "technical": 9,
    "seasonality": 4
  },
  "recommendation": "High-probability dip-buy setup. Enter on 50-DMA reclaim with 2-3% position size. Stop: swing low. Target: +5-8% bounce within 2 weeks."
}
```

#### Update Daily Planner AI Interpretation

Include signal context in the aiInterpretation summary:
```json
"summary": "STRONG BUY signal (72/100) active with SPY Routine Dip setup. Focus on precise entries..."
```

#### Update Technicals Tab AI Interpretation

Reference composite signal and key drivers:
```json
"summary": "Composite signal 72/100 (STRONG BUY). Driven by VIX backwardation (16/20 volatility) + RSI divergence (9/10 technical) + TOM window (4/5 seasonality)..."
```

---

### 4. Dashboard Display

The [research-dashboard.html](C:\Users\Iccanui\Desktop\Investing\master-plan\research-dashboard.html) automatically renders signal data in the **Daily Planner tab**:

#### Visual Display Includes:

1. **Large Composite Score** (e.g., "72")
2. **Tier Badge** (color-coded: green = STRONG BUY, yellow = WEAK, red = AVOID)
3. **Setup Type** (e.g., "🎯 SPY Routine Dip")
4. **Score Breakdown** with progress bars:
   - Trend (40%): 28/40
   - Breadth (25%): 17/25
   - Volatility (20%): 16/20
   - Technical (10%): 9/10
   - Seasonality (5%): 4/5
5. **Tactical Recommendation** (green box with specific action)

---

## Example Workflow Run

### Current Market (October 1, 2025)

**Step 1-2:** Collect provider data
- TradingView: SPY @ $555, 2.8% below 50-DMA, RSI 32 with bullish divergence
- Market Breadth: 32% SPX >50-DMA (improving from 28%), A/D Line bearish divergence
- Volatility Metrics: VIX 29 (stress band), rolling over from 31 spike
- CoinGlass: BTC IV 45th percentile (neutral)
- Calendar: October 1 (TOM window active, October = bullish month)

**Step 3.5:** Calculate signals

**Trend (40% weight):**
- 200-DMA regime: SPY above 200-DMA = 15/15 points
- 50-DMA distance: 2.8% below = 10/15 points (dip-buy zone)
- Multi-timeframe: Daily/H4 bullish, Weekly mixed = 3/10 points
- **Total: 28/40 points (70%)**

**Breadth (25% weight):**
- % SPX >50-DMA: 32% = 12/15 points (washout improving)
- A/D divergence: Bearish = 5/10 points (concerning but not disqualifying)
- **Total: 17/25 points (68%)**

**Volatility (20% weight):**
- VIX: 29 (stress), rolling over = 10/12 points
- Term structure: Slight backwardation = 5/5 points
- BTC IV: 45th percentile = 1/3 points
- **Total: 16/20 points (80%)**

**Technical (10% weight):**
- RSI: 32 with bullish divergence = 5/5 points
- MACD: Bullish cross below zero = 2/3 points
- Volume: Normal = 1/2 points
- **Total: 8/10 points (80%)**  *(Note: Example showed 9, recalculated here as 8)*

**Seasonality (5% weight):**
- TOM window: Active (Oct 1 = T+2) = 2/2 points
- Monthly: October (bullish) = 2/2 points
- FOMC: Nov 7 (not nearby) = 0/1 points
- **Total: 4/5 points (80%)**

**Composite Score:**
```
(28×1.0) + (17×1.0) + (16×1.0) + (8×1.0) + (4×1.0) = 73/100
```

**Tier:** STRONG BUY (70-84 range)

**Setup:** SPY Routine Dip (price 2.5-4.5% below 50-DMA + score ≥70)

**Step 4:** Update master-plan.md JSON with signalData object (shown above)

**Result:** Dashboard displays signal in Daily Planner tab with visual breakdown

---

## Key Benefits

### 1. **Automated Integration**
- No manual signal dashboard updates
- Signals calculated during normal workflow
- Display auto-renders from master-plan.md JSON

### 2. **Context-Aware**
- Signals inform Daily Planner priorities
- AI interpretations reference signal strength
- Technicals tab shows signal drivers

### 3. **Actionable**
- Clear tier (EXTREME/STRONG/MODERATE/WEAK/AVOID)
- Specific setup identification (Routine Dip, Deep Correction, etc.)
- Tactical recommendation with size/stop/target

### 4. **Transparent**
- Score breakdown shows which factors are strong/weak
- Can drill into signal module files for details
- Historical performance stats available

---

## Signal Module Files

**Core System:**
- [signal-engine.md](C:\Users\Iccanui\Desktop\Investing\Trading\signal-system\signal-engine.md) - Master composite scoring
- [How to use_Signals.txt](C:\Users\Iccanui\Desktop\Investing\Trading\signal-system\How to use_Signals.txt) - Workflow integration guide

**Signal Modules:**
- [trend-signals.md](C:\Users\Iccanui\Desktop\Investing\Trading\signal-system\signals\trend-signals.md) - 40% weight
- [breadth-signals.md](C:\Users\Iccanui\Desktop\Investing\Trading\signal-system\signals\breadth-signals.md) - 25% weight
- [volatility-signals.md](C:\Users\Iccanui\Desktop\Investing\Trading\signal-system\signals\volatility-signals.md) - 20% weight
- [technical-signals.md](C:\Users\Iccanui\Desktop\Investing\Trading\signal-system\signals\technical-signals.md) - 10% weight
- [seasonality-signals.md](C:\Users\Iccanui\Desktop\Investing\Trading\signal-system\signals\seasonality-signals.md) - 5% weight

---

## Next Steps

When you run the workflow next time:

1. **Collect provider data** (existing Steps 1-2)
2. **Calculate signals** (new Step 3.5):
   - Reference signal module files for thresholds
   - Gather data from provider summaries
   - Calculate composite score
   - Identify tier and setup type
3. **Update master-plan.md** (Step 4):
   - Add/update `signalData` object in dailyPlanner
   - Update Daily Planner aiInterpretation to mention signal
   - Update Technicals tab aiInterpretation with signal context
4. **Open research-dashboard.html**:
   - Signal automatically displays in Daily Planner tab
   - Visual breakdown shows score components
   - Tactical recommendation guides action

---

## Example Signal Display in Dashboard

```
📊 Trading Signal Score

72    STRONG BUY

🎯 SPY Routine Dip

Score Breakdown:
Trend (40%)      ████████████░░░░░░░░  28/40
Breadth (25%)    █████████████░░░░░░░  17/25
Volatility (20%) ████████████████░░░░  16/20
Technical (10%)  ██████████████████░░   9/10
Seasonality (5%) ████████████████░░░░   4/5

💡 High-probability dip-buy setup. Enter on 50-DMA reclaim with 2-3% position size. Stop: swing low. Target: +5-8% bounce within 2 weeks.
```

---

*Integration complete. Signal system operational within existing workflow.*
