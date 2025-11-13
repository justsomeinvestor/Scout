# Risk Management

## Overview
Comprehensive risk management strategies and frameworks across all timeframes - from RS momentum trading (minutes-hours) to long-term investment positions (months-years). This unified approach ensures consistent risk controls regardless of strategy or timeframe.

## Multi-Timeframe Position Sizing

### RS Trading Position Sizing (Short-term)

**Risk-Based Formula**
```
Position Size = (Account × Risk%) / (Entry Price - Stop Loss)
Risk% = 1-2% per trade based on RS score and market conditions
```

**RS Score-Based Risk Allocation**
- **RS Score 12-14**: 2% risk (highest conviction)
- **RS Score 10-12**: 1.5% risk (strong signal)
- **RS Score 8-10**: 1% risk (minimum threshold)
- **RS Score <8**: No trade (below threshold)

**Daily Risk Limits (RS Trading)**
- **Maximum daily loss**: -2% of account (immediate stop)
- **Reduced trading**: -1.5% daily loss (50% position size)
- **Alert level**: -1% daily loss (review and adjust)
- **Position limits**: Max 5 concurrent, max 3 same sector

**Time-Based Risk Scaling**
- **9:30-10:30 AM**: Full position size (optimal momentum period)
- **10:30-11:30 AM**: 75% size (fading momentum)
- **11:30-2:00 PM**: 50% size (lunch consolidation)
- **2:00-4:00 PM**: 75% size (power hour setup)
- **After 3:30 PM**: 25% size (day-ending risk)

### Investment Position Sizing (Medium to Long-term)

## Position Sizing

### Investment Risk-Based Position Sizing
- **Low Risk Stocks (Score 85-100)**: Up to 5% position size
- **Medium Risk Stocks (Score 65-84)**: Up to 3% position size
- **High Risk Stocks (Score 45-64)**: Up to 2% position size
- **Speculative Positions (Score <45)**: Up to 1% position size

### Cross-System Risk Integration
- **Total RS Trading Exposure**: Maximum 15% of portfolio
- **Total Investment Exposure**: Maximum 80% of portfolio
- **Options Exposure**: Maximum 10% of portfolio
- **Cash Reserve**: Minimum 5% for opportunities/margin

**Correlation Monitoring**
- Monitor overlap between RS trades and investment positions
- Reduce investment position size if actively trading same sector via RS
- Track total exposure to any single stock across all strategies

### Sector Concentration Limits (Combined)
- **Maximum per sector**: 20% of portfolio (all strategies combined)
- **High-risk sectors**: 15% maximum (including RS trades)
- **Defensive sectors**: Up to 25% allowed
- **RS + Investment overlap**: Max 10% additional if same sector

### Correlation-Based Adjustments
- Reduce position sizes for highly correlated holdings
- Monitor portfolio beta and adjust for market regime
- Consider factor exposures (growth vs. value, size, momentum)

## Stop Loss Strategies
*Rules and methodologies for setting and managing stop losses*

## Portfolio Risk Limits
*Overall portfolio risk parameters and limits*

## Risk Assessment Framework (10 points in our scoring system)

### Systematic Risk Factors (5 points)
- **Beta Analysis (3 points)**:
  - Low risk (β < 0.8): 3 points
  - Moderate risk (β 0.8-1.3): 2 points
  - High risk (β > 1.3): 1 point
- **Sector Risk (2 points)**:
  - Defensive sector: 2 points
  - Cyclical sector: 1 point
  - High-risk sector: 0 points

### Company-Specific Risks (5 points)
- **Financial Risk (3 points)**:
  - Strong balance sheet, low debt: 3 points
  - Moderate leverage: 2 points
  - High leverage concerns: 0 points
- **Business Risk (2 points)**:
  - Diversified revenue, strong moat: 2 points
  - Concentrated business model: 1 point
  - High business risk: 0 points

### Risk-Adjusted Scoring Formula
```
Risk-Adjusted Score = Raw Score × (1 - Volatility Penalty)
Volatility Penalty = min(0.2, (Stock Volatility - Sector Volatility) / Sector Volatility)
```

## Risk Monitoring
*Ongoing risk monitoring and adjustment procedures*

## Cycle-Based Risk Management

### Position Sizing for Cycle Strategies

**Maximum Exposure Limits:**
- **Never exceed 10-20% of total portfolio** for any cycle-based strategy
- **Individual tactical positions**: 2-5% maximum
- **Strategic cycle investments**: 5-10% maximum
- **Speculative cycle plays**: 1-2% maximum

**Kelly Criterion Application:**
- Use historical success rates and average returns for optimal sizing
- **Practical implementation: 25-50% of theoretical optimal size**
- Account for parameter uncertainty and changing market conditions
- Regular recalibration based on performance data

### Dynamic Risk Adjustment by Market Regime

**High Volatility Periods (VIX >25):**
- Reduce position sizes by 30%
- Widen stop-loss levels to accommodate increased price movement
- Focus on most reliable cycle patterns only
- Increase cash allocation by 10-15%

**Correlation Breakdown Periods:**
- **Reduce overall portfolio risk by 50%** as diversification deteriorates
- Monitor correlation matrices daily during stress periods
- High volatility increases correlations by 50-100%
- Recovery to normal correlations requires 3-6 months post-crisis

**Normal Market Conditions:**
- Standard cycle-based position sizing
- Monitor for regime change indicators
- Maintain diversification across cycle types

### Cycle Diversification Framework

**Multiple Cycle Types (Monitor at least 5 simultaneously):**
- Business cycle positioning (long-term)
- Seasonal patterns (tactical)
- Presidential cycle effects (medium-term)
- Technical cycles (short-term)
- Quantitative statistical cycles (systematic)

**Convergence Signals:**
- Highest probability when multiple cycles align
- Weight positions based on number of confirming cycles
- Reduce size when cycles conflict

### Transaction Cost Management

**Cost-Benefit Analysis:**
- Cycle returns must exceed 0.5% to justify implementation
- Use low-cost ETFs for shorter-duration strategies
- Monthly rebalancing optimal for cost/benefit trade-off
- Focus on patterns producing >1.5% returns for individual securities

**Implementation Efficiency:**
- Batch trades during optimal timing windows
- Use limit orders during low volatility periods
- Consider market impact for larger positions

## Historical Risk Events
*Lessons learned from past risk events*

## Options-Specific Risk Management (Friday/0DTE Framework)

### Non-Negotiable Risk Guardrails

**Daily Loss Limits:**
- **Maximum daily loss**: -2R (or -1% of account)
- **Stop trading immediately** if daily limit hit
- **Reset next session** - no revenge trading

**Per-Trade Risk Allocation:**
- **Naked debit options**: ≤0.25R maximum
- **Defined-risk spreads**: ≤0.5R maximum  
- **Premium selling strategies**: ≤0.5R maximum risk
- **Speculative plays**: ≤0.1R maximum

**Position Concentration Limits:**
- **Before noon ET**: Maximum 2 concurrent risk positions
- **After noon ET**: Maximum 3 concurrent risk positions
- **Power hour (3-4pm ET)**: Maximum 1 new position
- **Never exceed 1.5R total** in options at any time

### Assignment and Exercise Risk Controls

**European vs American Style Management:**
- **SPX/SPXW (European)**: No early assignment risk, preferred for late-day strategies
- **SPY/QQQ/Singles (American)**: Assignment possible, must manage before 3:50 ET

**Weekend Assignment Prevention:**
- **No naked short options** into weekend
- **Convert to defined-risk** by 3:50 ET Friday
- **Close or hedge** any unwanted assignment exposure
- **Pin risk management**: Monitor large strike OI, close shorts near pins

**Exercise Timing Rules:**
- **Last trading**: 4:00 PM ET
- **Exercise deadline**: ~5:30 PM ET (verify with broker)
- **Broker cutoffs**: Often earlier than OCC - confirm your specific times
- **Weekend positions**: Only defined-risk structures allowed

### Time-Based Risk Management

**Session Risk Progression:**

**9:35-10:15 ET (Opening Hour):**
- **Strategy**: Directional debit spreads only
- **Risk**: 0.25R maximum per trade
- **Focus**: Wait for first pullback/structure
- **Avoid**: Naked premium purchases

**10:15-13:00 ET (Midday):**
- **Strategy**: Iron flies/condors if range-bound
- **Risk**: 0.5R maximum defined-risk
- **Focus**: VWAP compression plays
- **Monitor**: Realized vs implied volatility

**15:00-16:00 ET (Power Hour):**
- **Strategy**: Pin plays and risk reduction
- **Risk**: 0.25R maximum new positions
- **Focus**: Proactive short strike management
- **Deadline**: All American-style shorts managed by 3:50 ET

### Options Greeks Risk Monitoring

**Theta Decay Management:**
- **0DTE acceleration**: Expect rapid time decay final 2 hours
- **Long premium**: Needs strong momentum or IV expansion to overcome theta
- **Short premium**: Benefits from time decay, monitor pin risk

**Delta Exposure Guidelines:**
- **Debit spreads**: 30-40Δ long strikes preferred
- **Iron flies**: Wings at 0.20-0.25Δ for optimal risk/reward
- **BWB**: Align max profit within 0.3% of target pin level

**Vega Risk Controls:**
- **IV crush protection**: Use spreads vs. naked options on news days
- **Expansion plays**: Only with strong momentum + volume confirmation
- **Range strategies**: Benefit from IV compression into close

### Position Management Rules

**Entry Discipline:**
- **Wait 5-10 minutes** after market open for spreads to tighten
- **Use limit orders** only, work mid-price
- **No market orders** on options (wide spreads)
- **Structure confirmation** required before entry

**Exit Management:**
- **Scaling**: Take 50% at 1R, trail remainder
- **Stop loss**: Structure-based OR 50% of debit (whichever first)
- **No averaging down** on 0DTE positions
- **Trail to MFE-50%** (half of max favorable excursion)

**End-of-Day Protocols:**
- **3:50 ET deadline** for American-style short management
- **Flatten discretionary risk** before close
- **Keep only defined-risk** positions into weekend
- **Document lessons learned** for next session

---
*Last Updated: September 26, 2025*  
*Cross-references: [Master Plan](../master-plan/master-plan.md), [Market Analysis](../market-analysis/market-analysis.md), [Portfolio Tracking](../portfolio-tracking/portfolio-tracking.md), [Trading Psychology](../trading-psychology/trading-psychology.md)*  
*System Version: 1.0 - Complete Professional Framework*