
# Investment Scoring System

## Overview
This framework scores stocks quantitatively across six core pillars using sector-relative percentile ranking and applies red-flag penalties to generate a robust composite score.

## Pillars & Weights
- **Quality (25%)**
- **Growth (20%)**
- **Value (20%)**
- **Financial Strength (15%)**
- **Efficiency / Moat (10%)**
- **Technical (10%)**

## Quality Metrics
- ROIC = NOPAT / Invested Capital
- Gross Profitability = Gross Profit / Total Assets
- FCF Margin = FCF / Revenue
- Accruals Ratio = (Net Income – CFO) / Total Assets

## Growth Metrics
- 3Y Revenue CAGR
- 3Y EPS CAGR
- 3Y FCF CAGR

## Value Metrics
- EV/EBIT
- EV/EBITDA
- EV/FCF
- PEG (optional)

## Financial Strength
- Interest Coverage = EBIT / Interest Expense
- Net Debt / EBITDA
- Altman Z-Score (optional)

## Efficiency / Moat
- Working-Capital Turns = Revenue / (Current Assets – Current Liabilities)
- Cash Conversion Cycle (optional)

## Technicals
- 12-1 Momentum
- Relative Strength vs SPY (6M)
- Trend Filters (Price > 200D, 50D > 200D)
- ATR % of Price (lower better)

## Red-Flag Penalties
(-10 each, max –30)
- Altman Z < 1.8
- Interest Coverage < 2×
- High Accruals
- Beneish M > –1.78
- Dilution > 5% over 3Y
- Low Liquidity (< $2M daily avg)

## Included Files
- `investment_scoring_template.csv`
- `score_stocks.py`

## Usage
1. Fill `investment_scoring_template.csv`.
2. Run: `python score_stocks.py`
3. Output: `scores.csv` with pillar scores, flags, and composite.

