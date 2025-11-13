# Trading Signal System - Quick Start Guide

## Overview

The Trading Signal Score system generates a **0-100 composite score** that identifies high-probability dip-buying opportunities for SPY, QQQ, BTC, and ETH.

**Formula:**
```
Score = (Trend × 40%) + (Breadth × 25%) + (Volatility × 20%) + (Technical × 10%) + (Seasonality × 5%)
```

**Signal Tiers:**
- **85-100 (EXTREME)**: Rare, maximum conviction setups
- **70-84 (STRONG)**: High-probability dip-buy opportunities
- **55-69 (MODERATE)**: Standard setups, reduced size
- **40-54 (WEAK)**: Pass or minimal size
- **0-39 (AVOID)**: Counter-trend, high risk

---

## Daily Workflow

### **Quick Command (Recommended)**

```bash
# Calculate signals for today and update dashboard
python scripts/run_daily_signals.py 2025-10-12 --update-master-plan
```

This runs:
1. Fetch market data (VIX, crypto prices, etc.)
2. Calculate signal scores from data + TradingView summaries
3. Update master-plan.md JSON with signal data
4. Dashboard auto-displays the signals

### **Manual Step-by-Step**

If you prefer more control:

```bash
# Step 1: Fetch market data (optional if already done)
python scripts/fetch_market_data.py 2025-10-12

# Step 2: Calculate signals
python scripts/calculate_signals.py 2025-10-12

# Step 3: View results
# Open: Research/.cache/signals_2025-10-12.json

# Step 4: (Optional) Manually copy signalData into master-plan.md
```

---

## Understanding the Scores

### **Component Breakdown**

**Trend (40% weight - 40 points max)**
- Measures: Position vs. 50/200-day moving averages
- **High score**: SPY/BTC below 50-DMA (dip-buy opportunity)
- **Low score**: Far above moving averages (overextended)

**Breadth (25% weight - 25 points max)**
- Measures: % of stocks above 50-DMA, A/D line divergences
- **High score**: <35% above 50-DMA (capitulation/washout)
- **Low score**: >80% above 50-DMA (euphoria/overbought)
- **Adjustment**: X sentiment contrarian logic adds/subtracts up to ±2 points

**Volatility (20% weight - 20 points max)**
- Measures: VIX level, Bitcoin implied volatility percentile
- **High score**: VIX >28 (fear/stress = dip-buy opportunity)
- **Low score**: VIX <16 (complacency = no edge)

**Technical (10% weight - 10 points max)**
- Measures: RSI, MACD, momentum
- **High score**: RSI <40 (oversold/pullback)
- **Low score**: RSI >70 (overbought)

**Seasonality (5% weight - 5 points max)**
- Measures: Historical monthly patterns
- **High score**: October-December (bullish months)
- **Low score**: September (historically weak)

---

## Example Interpretation

### **Scenario 1: STRONG Signal (Score: 72)**

```
Composite: 72/100 (STRONG)

Breakdown:
  Trend:       28/40 (70%) - SPY 2.5% below 50-DMA, above 200-DMA
  Breadth:     17/25 (68%) - 32% above 50-DMA (washout improving)
  Volatility:  16/20 (80%) - VIX 29 (stress), rolling over
  Technical:    9/10 (90%) - RSI 32 with bullish divergence
  Seasonality:  4/5  (80%) - October + TOM window

Recommendation:
"High-probability dip-buy setup. Enter on 50-DMA reclaim with 2-3% position size.
Stop: swing low. Target: +5-8% bounce within 2 weeks."
```

**What to do:**
- ✅ **Enter trades** on confirmation (e.g., SPY reclaims 50-DMA)
- ✅ Use **full position size** (2-3% of account)
- ✅ Set **tight stops** below recent swing low
- ✅ Target **5-8% bounce** over 1-2 weeks

---

### **Scenario 2: WEAK Signal (Score: 42)**

```
Composite: 42/100 (WEAK)

Breakdown:
  Trend:       17/40 (43%) - Mixed signals, no clear dip
  Breadth:      5/25 (20%) - Only 10% of assets moving together
  Volatility:  10/20 (50%) - VIX 21 (elevated but not extreme)
  Technical:    5/10 (50%) - RSI 55 (neutral)
  Seasonality:  5/5  (100%) - October (bullish month)

Recommendation:
"WEAK/AVOID signal. Low conviction - no edge. Focus on capital preservation
and wait for better setups (score >70)."
```

**What to do:**
- ❌ **Don't add new positions**
- ❌ No edge in current setup
- ✅ **Preserve capital** - wait for score >70
- ✅ **Review risk** - consider reducing existing exposure
- ✅ **Monitor daily** for signal improvement

---

## Integration with Your Workflow

The signal system plugs into **Step 4.5** of your master plan workflow:

```
Standard Master Plan Workflow:
1. Update provider summaries (YouTube, RSS, Technicals)
2. Create Market Sentiment Overview
3. Align the Master Plan
4. **[NEW] Generate Trading Signals** ← THIS STEP
5. Document & Organize
```

After running the signal calculator:
- **Daily Planner tab** shows the composite score with visual breakdown
- **Quick Actions** section suggests tactical responses
- **Recommendation** provides specific entry/exit guidance

---

## Viewing in Dashboard

After running signals and updating master-plan.md:

1. Open `master-plan/research-dashboard.html` in browser
2. Navigate to **Daily Planner** tab
3. See **Trading Signal Score** section with:
   - Large composite score (e.g., "72")
   - Color-coded tier badge (green = STRONG, yellow = WEAK, red = AVOID)
   - Score breakdown with progress bars
   - Tactical recommendation

---

## Data Sources Used

The calculator uses **hybrid approach**:

### **Primary Data (from `fetch_market_data.py`)**
- Fear & Greed Index (alternative.me)
- VIX, SPY, QQQ prices (Yahoo Finance)
- BTC, ETH, SOL prices (CoinGecko)
- Economic indicators (FRED - optional)

### **Enriched Data (from TradingView summaries)**
- SPX/BTC price vs. 50/200-DMA
- RSI values
- Support/resistance levels

### **Sentiment Data (from X summaries)**
- X Crypto sentiment (0-100)
- X Macro sentiment (0-100)
- Contrarian adjustment logic

If API data is missing, the calculator **gracefully falls back** to parsing your existing markdown summaries.

---

## Troubleshooting

### **"Market data not found" error**

```bash
# Run the data fetcher first:
python scripts/fetch_market_data.py 2025-10-12

# Or skip the fetch step if you already have summaries:
python scripts/run_daily_signals.py 2025-10-12 --skip-fetch
```

### **Scores seem off**

- Check that TradingView summaries were generated for today
- Verify VIX and crypto data in `Research/.cache/YYYY-MM-DD_market_data.json`
- Look at detailed logs - calculator shows how each component is scored

### **Dashboard not showing signals**

- Ensure you ran with `--update-master-plan` flag
- Check that `signalData` object exists in master-plan.md JSON
- Refresh browser (Ctrl+F5) to clear cache

---

## Performance Tracking (Recommended)

To validate the system's effectiveness, track your trades:

**When you take a trade based on a signal:**
1. Log the **signal score** at entry
2. Log **entry price, stop, target**
3. Log **outcome** (win/loss, R multiple)
4. Log **duration** (days held)

**Review quarterly:**
- Do 70+ scores really win 65%+ of the time?
- Are EXTREME signals (85+) worth the larger size?
- Which components are most predictive?
- Adjust weights based on real results

---

## Advanced Usage

### **Run for multiple dates**

```bash
# Calculate historical signals
python scripts/calculate_signals.py 2025-10-10
python scripts/calculate_signals.py 2025-10-11
python scripts/calculate_signals.py 2025-10-12
```

### **Backtest validation**

Compare historical signals to actual market outcomes:
- Did 70+ scores precede bounces?
- Did <40 scores precede further selloffs?
- Use data to refine thresholds

### **Custom weights**

Edit `scripts/calculate_signals.py` line 49-55 to adjust component weights:

```python
WEIGHTS = {
    'trend': 0.40,      # Increase if trend is most predictive
    'breadth': 0.25,    # Increase if breadth matters more
    'volatility': 0.20,
    'technical': 0.10,
    'seasonality': 0.05
}
```

---

## Quick Reference

| Score | Tier | Action | Position Size |
|-------|------|--------|--------------|
| 85-100 | EXTREME | Max conviction entry | 4-5% risk |
| 70-84 | STRONG | Full size dip-buy | 2-3% risk |
| 55-69 | MODERATE | Reduced size | 1-2% risk |
| 40-54 | WEAK | Pass or minimal | <1% risk |
| 0-39 | AVOID | Do not trade | 0% risk |

**Key Insight:** The system is designed to **identify dip-buying opportunities**, not chase momentum. Lower breadth + higher volatility = better score (contrarian).

---

## Support

For issues or questions:
- Check detailed logs from `python scripts/calculate_signals.py`
- Review signal module files in `Trading/signal-system/signals/`
- See full documentation in `signal-engine.md` and `INTEGRATION_SUMMARY.md`

**Remember:** This is a tool to guide decisions, not a crystal ball. Always use proper risk management and position sizing regardless of signal strength.

---

*Signal System v2.0 - Enhanced with Summary Parsing - October 2025*
