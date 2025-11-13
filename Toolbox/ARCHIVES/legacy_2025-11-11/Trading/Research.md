# Comprehensive Investment Evaluation Template for LLM-Based Stock Analysis

## Template Overview

This universal investment evaluation template integrates professional-grade analysis across fundamental, technical, management quality, valuation, and risk dimensions. The framework provides systematic scoring criteria for generating Buy/Hold/Sell ratings across multiple timeframes and can be applied to any sector or industry.

## Section 1: Context Setting and Data Requirements

### Analysis Parameters
```
STOCK SYMBOL: [TICKER]
ANALYSIS DATE: [CURRENT DATE]
ANALYST ROLE: Expert Financial Analyst
ANALYSIS SCOPE: Comprehensive investment evaluation
TIME HORIZONS: Short-term (1-3 months), Medium-term (3-12 months), Long-term (12+ months)
SECTOR: [AUTO-DETECT]
MARKET CAP: [AUTO-CALCULATE]
```

### Required Data Inputs
**Fundamental Data:**
- Financial statements (3 years historical + current TTM)
- Key ratios: P/E, P/B, PEG, ROE, ROA, ROIC, Debt/Equity, Current Ratio, Quick Ratio
- Growth metrics: Revenue CAGR, Earnings CAGR, Free Cash Flow trends
- Profit margins: Gross, Operating, Net margins

**Technical Data:**
- Price history (2-5 years daily data)
- Volume data, moving averages (5, 10, 20, 50, 100, 200-day)
- RSI (14-period), MACD (12-26-9), Bollinger Bands (20-period, 2 std dev)
- Support/resistance levels, trend lines

**Management Data:**
- Insider ownership percentage
- Recent insider trading activity
- CEO tenure and background
- Board composition and independence metrics

**Market Data:**
- Sector ETF performance
- Peer comparison group (5-7 companies)
- Market volatility (VIX), sector beta
- Analyst consensus and sentiment data

## Section 2: Scoring Framework (100-Point System)

### Primary Analysis Categories and Weights

**A. Fundamental Analysis (40 points)**
- Financial Health & Quality (15 points)
- Growth Prospects (15 points) 
- Valuation Attractiveness (10 points)

**B. Technical Analysis (25 points)**
- Price Momentum & Trend (10 points)
- Volume & Market Structure (8 points)
- Support/Resistance Levels (7 points)

**C. Management Quality (15 points)**
- Leadership Effectiveness (8 points)
- Corporate Governance (7 points)

**D. Risk Assessment (10 points)**
- Systematic Risk Factors (5 points)
- Company-Specific Risks (5 points)

**E. Market Sentiment (10 points)**
- Analyst Consensus (5 points)
- News Sentiment & Momentum (5 points)

## Section 3: Detailed Scoring Criteria

### A. Fundamental Analysis Scoring (40 points total)

#### Financial Health & Quality (15 points)
**Metrics and Scoring:**

*Profitability Metrics (8 points):*
- **ROE Score (3 points):**
  - Excellent (>20%): 3 points
  - Very Good (15-20%): 2.5 points
  - Good (10-15%): 2 points
  - Fair (5-10%): 1 point
  - Poor (<5%): 0 points

- **ROIC Score (3 points):**
  - Exceptional (>20%): 3 points
  - Excellent (15-20%): 2.5 points
  - Good (10-15%): 2 points
  - Fair (5-10%): 1 point
  - Poor (<5%): 0 points

- **Net Margin Trend (2 points):**
  - Expanding margins (+0.5%+ annually): 2 points
  - Stable margins (±0.2%): 1.5 points
  - Declining margins (-0.5%+ annually): 0 points

*Balance Sheet Strength (7 points):*
- **Debt-to-Equity Ratio (3 points):**
  - Conservative (<0.3): 3 points
  - Moderate (0.3-0.6): 2 points
  - High (0.6-1.0): 1 point
  - Excessive (>1.0): 0 points

- **Current Ratio (2 points):**
  - Strong (>2.0): 2 points
  - Adequate (1.5-2.0): 1.5 points
  - Acceptable (1.0-1.5): 1 point
  - Concerning (<1.0): 0 points

- **Free Cash Flow Quality (2 points):**
  - FCF > Net Income: 2 points
  - FCF = 0.8-1.0x Net Income: 1.5 points
  - FCF = 0.5-0.8x Net Income: 1 point
  - FCF < 0.5x Net Income: 0 points

#### Growth Prospects (15 points)

*Revenue Growth (7 points):*
- **3-Year Revenue CAGR (4 points):**
  - Exceptional (>20%): 4 points
  - Strong (10-20%): 3 points
  - Moderate (5-10%): 2 points
  - Slow (0-5%): 1 point
  - Declining (<0%): 0 points

- **Revenue Growth Consistency (3 points):**
  - Consistent growth (no negative years): 3 points
  - Mostly consistent (1 negative year): 2 points
  - Volatile (2+ negative years): 1 point

*Earnings Growth (8 points):*
- **3-Year EPS CAGR (5 points):**
  - Exceptional (>25%): 5 points
  - Strong (15-25%): 4 points
  - Moderate (10-15%): 3 points
  - Slow (5-10%): 2 points
  - Poor (<5%): 1 point

- **Forward Growth Outlook (3 points):**
  - Accelerating growth expected: 3 points
  - Steady growth expected: 2 points
  - Slowing growth expected: 1 point
  - Declining growth expected: 0 points

#### Valuation Attractiveness (10 points)

*Absolute Valuation (5 points):*
- **P/E Ratio vs. Sector Median (3 points):**
  - Discount >20%: 3 points
  - Discount 10-20%: 2 points
  - Premium/Discount ±10%: 1.5 points
  - Premium 10-20%: 1 point
  - Premium >20%: 0 points

- **PEG Ratio (2 points):**
  - <1.0: 2 points
  - 1.0-1.5: 1.5 points
  - 1.5-2.0: 1 point
  - >2.0: 0 points

*Relative Valuation (5 points):*
- **EV/EBITDA vs. Peers (3 points):** [Same scoring as P/E]
- **P/B Ratio Relative to ROE (2 points):**
  - P/B < ROE/100: 2 points
  - P/B = ROE/100 ±20%: 1 point
  - P/B > 1.2x ROE/100: 0 points

### B. Technical Analysis Scoring (25 points total)

#### Price Momentum & Trend (10 points)

*Moving Average Analysis (4 points):*
- Price above all MAs (20, 50, 200): 4 points
- Price above 20 & 50 MA: 3 points
- Price above 20 MA only: 2 points
- Price below all MAs: 0 points

*Momentum Indicators (6 points):*
- **RSI Analysis (3 points):**
  - RSI 30-70 with bullish divergence: 3 points
  - RSI 30-70 range: 2 points
  - RSI >70 (overbought): 1 point
  - RSI <30 (oversold): 1 point (contrarian opportunity)

- **MACD Signal (3 points):**
  - MACD line above signal, expanding histogram: 3 points
  - MACD line above signal, contracting histogram: 2 points
  - MACD line below signal: 1 point
  - Negative MACD with declining histogram: 0 points

#### Volume & Market Structure (8 points)

*Volume Confirmation (4 points):*
- Volume >20% above average on up days: 4 points
- Volume moderately above average: 2 points
- Average volume: 1 point
- Low volume on price moves: 0 points

*Price Pattern Analysis (4 points):*
- Bullish pattern (breakout, flag, triangle): 4 points
- Consolidation pattern: 2 points
- No clear pattern: 1 point
- Bearish pattern: 0 points

#### Support/Resistance Levels (7 points)

*Technical Levels (4 points):*
- Multiple support levels below current price: 4 points
- Clear support level nearby: 2 points
- Near major resistance: 1 point
- Above major resistance: 3 points

*Trend Analysis (3 points):*
- Clear uptrend with higher highs/lows: 3 points
- Sideways trend: 1.5 points
- Clear downtrend: 0 points

### C. Management Quality Assessment (15 points total)

#### Leadership Effectiveness (8 points)

*Track Record (4 points):*
- Consistent outperformance vs. peers: 4 points
- Mixed performance with strategic vision: 2 points
- Average performance: 1 point
- Poor performance: 0 points

*Capital Allocation (4 points):*
- ROIC consistently > WACC by 5%+: 4 points
- ROIC > WACC: 2 points
- ROIC ≈ WACC: 1 point
- ROIC < WACC: 0 points

#### Corporate Governance (7 points)

*Insider Ownership (3 points):*
- Optimal range (15-30%): 3 points
- Adequate (10-15% or 30-40%): 2 points
- Low (<10%): 1 point
- Excessive (>50%): 1 point

*Governance Structure (4 points):*
- Independent board, strong oversight: 4 points
- Adequate governance: 2 points
- Governance concerns: 0 points

### D. Risk Assessment (10 points total)

#### Systematic Risk Factors (5 points)
- **Beta Analysis (3 points):**
  - Low risk (β < 0.8): 3 points
  - Moderate risk (β 0.8-1.3): 2 points
  - High risk (β > 1.3): 1 point

- **Sector Risk (2 points):**
  - Defensive sector: 2 points
  - Cyclical sector: 1 point
  - High-risk sector: 0 points

#### Company-Specific Risks (5 points)
- **Financial Risk (3 points):**
  - Strong balance sheet, low debt: 3 points
  - Moderate leverage: 2 points
  - High leverage concerns: 0 points

- **Business Risk (2 points):**
  - Diversified revenue, strong moat: 2 points
  - Concentrated business model: 1 point
  - High business risk: 0 points

### E. Market Sentiment (10 points total)

#### Analyst Consensus (5 points)
- Strong Buy consensus (80%+ Buy ratings): 5 points
- Buy consensus (60-80% Buy): 3 points
- Mixed consensus: 2 points
- Negative consensus: 0 points

#### News Sentiment (5 points)
- Consistently positive news flow: 5 points
- Mixed news sentiment: 2 points
- Negative news sentiment: 0 points

## Section 4: Timeframe-Specific Rating Criteria

### Composite Score to Rating Conversion

**Overall Score Calculation:**
```
Total Score = Fundamental (40) + Technical (25) + Management (15) + Risk (10) + Sentiment (10)
Percentage Score = (Total Score / 100) × 100
```

### Rating Thresholds by Timeframe

#### Short-Term Ratings (1-3 months)
*Emphasis: Technical Analysis (40%), Sentiment (25%), Fundamental (25%), Risk (10%)*

- **Strong Buy (85-100):** Excellent technical momentum + positive sentiment
- **Buy (70-84):** Good technical setup + favorable fundamentals
- **Hold (45-69):** Mixed signals or neutral outlook
- **Sell (30-44):** Weak technicals + negative sentiment
- **Strong Sell (0-29):** Poor across all measures

#### Medium-Term Ratings (3-12 months)
*Standard Weighting: Fundamental (40%), Technical (25%), Management (15%), Risk (10%), Sentiment (10%)*

- **Strong Buy (80-100):** Strong fundamentals + positive technical trends
- **Buy (65-79):** Good fundamentals + reasonable valuation
- **Hold (40-64):** Fair fundamentals + mixed outlook
- **Sell (25-39):** Weak fundamentals + negative trends
- **Strong Sell (0-24):** Poor fundamentals + significant risks

#### Long-Term Ratings (12+ months)
*Emphasis: Fundamental (50%), Management (20%), Risk (15%), Technical (10%), Sentiment (5%)*

- **Strong Buy (75-100):** Exceptional business quality + strong management
- **Buy (60-74):** Good fundamentals + reasonable valuation
- **Hold (35-59):** Average quality + fair valuation
- **Sell (20-34):** Below-average quality + overvalued
- **Strong Sell (0-19):** Poor business quality + significant risks

## Section 5: Sector-Specific Adjustments

### Technology Sector Adjustments
- Increase growth weight by 5%
- Reduce debt concern thresholds (higher acceptable D/E ratios)
- Emphasize R&D spending and innovation metrics
- Higher acceptable P/E ratios (25-40x range)

### Financial Sector Adjustments
- Focus on ROE over ROIC
- Emphasize regulatory capital ratios
- Remove traditional DCF analysis
- Use P/B and P/E ratios primarily

### Healthcare/Pharma Adjustments
- Include R&D efficiency metrics
- Consider patent cliff analysis
- Emphasize pipeline value
- Higher volatility tolerance

### Utilities Adjustments
- Lower growth expectations
- Emphasize dividend sustainability
- Focus on rate base growth
- Lower acceptable ROE ranges (8-15%)

### Industrial/Manufacturing Adjustments
- Consider capital intensity
- Emphasize through-cycle metrics
- Focus on operational leverage
- Monitor commodity price exposure

## Section 6: Professional Integration and Best Practices

### Composite Scoring Formula
```
Adjusted Score = Base Score × Sector Adjustment × Data Quality Factor × Market Regime Factor

Where:
- Sector Adjustment: 0.9-1.1 based on sector-specific considerations
- Data Quality Factor: 0.8-1.0 based on data completeness and reliability
- Market Regime Factor: 0.9-1.1 based on current market conditions
```

### Risk-Adjusted Scoring
```
Risk-Adjusted Score = Raw Score × (1 - Volatility Penalty)
Volatility Penalty = min(0.2, (Stock Volatility - Sector Volatility) / Sector Volatility)
```

### Market Regime Considerations

**Bull Market Adjustments:**
- Increase technical analysis weight to 30%
- Reduce fundamental weight to 35%
- Higher rating thresholds (add 5 points to each category)

**Bear Market Adjustments:**
- Increase fundamental weight to 45%
- Reduce technical weight to 20%
- Lower rating thresholds (subtract 5 points)

**Volatile Market Adjustments:**
- Increase risk assessment weight to 15%
- Emphasize balance sheet strength
- Add uncertainty disclaimer to all ratings

## Section 7: LLM Implementation Instructions

### Analysis Process
1. **Data Collection:** Gather all required inputs and verify data quality
2. **Sector Classification:** Identify sector and apply appropriate adjustments
3. **Systematic Scoring:** Calculate scores for each category following criteria
4. **Composite Calculation:** Compute overall scores with proper weighting
5. **Rating Assignment:** Apply timeframe-specific thresholds
6. **Quality Control:** Verify logical consistency and flag outliers
7. **Report Generation:** Structure findings with clear rationale

### Quality Control Mechanisms
- **Data Validation:** Check for missing or outlier data points
- **Logical Consistency:** Ensure scores align with qualitative assessment
- **Peer Comparison:** Validate rating relative to sector peers
- **Historical Context:** Consider company's historical performance
- **Market Context:** Factor in current market conditions

### Output Format Requirements
```
INVESTMENT ANALYSIS SUMMARY
Stock: [TICKER] | Sector: [SECTOR] | Analysis Date: [DATE]

COMPOSITE SCORES:
- Overall Score: X/100 (Y%)
- Short-term Rating: [RATING]
- Medium-term Rating: [RATING]  
- Long-term Rating: [RATING]

KEY SCORE BREAKDOWN:
- Fundamental Analysis: X/40
- Technical Analysis: X/25
- Management Quality: X/15
- Risk Assessment: X/10
- Market Sentiment: X/10

INVESTMENT THESIS:
[3-4 sentence summary of key investment points]

KEY RISKS:
[Top 3 risk factors]

PRICE TARGET:
[Calculated target with methodology]

DATA QUALITY: [High/Medium/Low] (X% complete)
CONFIDENCE LEVEL: [High/Medium/Low]
```

This comprehensive template provides systematic, professional-grade investment analysis suitable for LLM implementation while maintaining the rigor and consistency required for institutional-quality investment decisions. The framework adapts to different sectors while providing clear, quantifiable criteria for generating reliable investment ratings across multiple time horizons.