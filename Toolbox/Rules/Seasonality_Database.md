# Seasonality Database - Trading Patterns

**Purpose:** Historical seasonal patterns affecting equity markets
**Data Source:** 50+ years historical research, Stock Market Almanac data
**Framework:** Applied via Probability Scoring Engine (10% weight in overall score)
**Last Updated:** 2025-10-19

---

## Table of Contents

1. [Monthly Patterns](#monthly-patterns)
2. [Seasonal Six-Month Cycles](#seasonal-six-month-cycles)
3. [Presidential Election Cycles](#presidential-election-cycles)
4. [Volatility Seasonality](#volatility-seasonality)
5. [Decadal & Long-Term Cycles](#decadal--long-term-cycles)
6. [Special Seasonal Events](#special-seasonal-events)
7. [Current Market Position](#current-market-position-2025)
8. [Scoring Application](#scoring-application)

---

## Monthly Patterns

### Historical Data: S&P 500 Average Returns by Month (Since 1950)

| Month | Avg Return | Win Rate | Rank | Signal |
|-------|-----------|----------|------|--------|
| January | +0.7% | 60% | 7th | Neutral (mixed) |
| February | +0.5% | 55% | 10th | Weak |
| March | +1.4% | 65% | 2nd | Bullish |
| April | +1.8% | 68% | 1st | Very Bullish |
| May | +0.3% | 61% | 8th | Neutral |
| June | +0.1% | 52% | 11th | Weak |
| July | +1.0% | 65% | 5th | Neutral |
| August | +0.6% | 55% | 9th | Weak |
| September | -0.6% | 32% | 12th | Bearish ❌ |
| October | +0.8% | 60% | 6th | Neutral (volatile) |
| November | +1.4% | 64% | 3rd | Bullish |
| December | +1.3% | 67% | 4th | Bullish |

**Key Insights:**
- **Best Months:** April (1.8%), March (1.4%), November (1.4%), December (1.3%)
- **Worst Month:** September (-0.6%, only month with negative average)
- **October:** Paradox - historically volatile but average positive
- **May-October Period:** Known as "sell in May and go away" season

**Scoring Application:**

For months ranked 1-2 (April, March): +15 points to bullish score
For months ranked 3-4 (Nov, Dec): +12 points to bullish score
For months ranked 5-7 (July, Oct, Jan): +5 points (neutral)
For months ranked 8-10 (May, Aug, Feb): 0 points (flat)
For month ranked 11 (June): -5 points (slightly bearish)
For month ranked 12 (September): -15 points ⚠️ (bearish)

---

## Seasonal Six-Month Cycles

### The "Sell in May and Go Away" Pattern

**Definition:** Historically weaker stock performance May through October vs. November through April

**Historical Data (Since 1950):**

| Period | Avg Return | Win Rate | Performance |
|--------|-----------|----------|-------------|
| November - April | +6-7% average | 75% | **STRONG** ✓ |
| May - October | +1-2% average | 65% | Weak |
| May 1 - Oct 31 (50yr avg) | +3.86% | — | Positive but lackluster |

**Explanation:**
- May-October averages ~1.8% total return over 6 months
- November-April averages ~6-7% total return over 6 months
- Returns from May-October positive 65% of the time
- But Nov-April positive 75% of the time

**Why This Happens:**
- Summer vacation season (historically lower trading volume)
- Lower trading volume = lower liquidity
- Lack of catalysts and news in summer
- Hedge fund rebalancing in September
- End of summer margin calls

**Important Caveat (Last 11 Years):**
- May-October average return: +4.9% (median: +3.1%)
- Win rate improved to 82%
- Pattern weakening in modern markets

**Scoring Application:**

- If currently May-September: -8 points to bullish score (seasonal headwind)
- If currently October (Halloween effect): -10 points (volatility spike risk)
- If currently November-April: +10 points (seasonal tailwind)
- If currently December (Santa rally): +15 points (strongest seasonal)

---

## Presidential Election Cycles

### The 4-Year Presidential Cycle

**Overview:** Stock market returns follow a predictable 4-year pattern aligned with presidential terms

**Historical Data (Dow Jones since 1896):**

| Year in Cycle | Avg Return | Recent (50yr) | Strength | Notes |
|----------------|-----------|---------------|----------|-------|
| **Year 1** (Post-election) | 3% | 7.9% | Weak | New president focused on agenda |
| **Year 2** (Midterm) | 4% | 4.6% | Weak | Consolidation phase |
| **Year 3** (Pre-election) | 10.2% | 17.2% | **Strong** ✓ | President stimulates economy |
| **Year 4** (Election year) | 6% | 7.3% | Moderate | Policy uncertainty |

**Current Cycle Position (2025):**
- 2024 was Year 4 (Election year)
- 2025 = **Year 1** (Post-election year)
- Expected return: ~7-8% (historically weak)
- 2026 = Year 2 (Midterm, historically weakest)
- 2027 = **Year 3** (Pre-election, historically strongest) ⬆️

**Why This Pattern Exists:**
- Years 1-2: President pursues agenda (sometimes deflationary or restrictive)
- Year 3: President stimulates economy to boost re-election chances
- Year 4: Market uncertainty from potential leadership change

**Data Confidence:**
- Pattern holds ~65% of the time
- More reliable in earlier decades; weakening in modern era
- Recent disruptions: financial crisis (2008), pandemic (2020), inflation (2022)

**Scoring Application:**

- Current Year 1 (2025): -8 points (historical weakness phase)
- In Year 2 (Midterm): -10 points (historically weakest year)
- In Year 3 (Pre-election): +15 points (historically strongest)
- In Year 4 (Election): +5 points (neutral/uncertain)

---

## Volatility Seasonality

### VIX Seasonal Patterns

**Definition:** Historical patterns in market volatility (VIX index)

**High-Volatility Months (Historical):**

| Month | VIX Avg | Rank | Reason |
|-------|---------|------|--------|
| **September** | Highest | 1st | Autumn downturn season |
| **October** | High | 2nd | "Crash month" history |
| **November** | High | 3rd | Post-election uncertainty |
| May-June | Moderate | — | Summer doldrums |

**Low-Volatility Months:**

| Month | VIX Avg | Reason |
|-------|---------|--------|
| April | Low | Pre-summer calm |
| December (except last week) | Low | Holiday season |
| January | Low | New year optimism |

**The "Halloween Effect":**
- Volatility spike from late September through October
- Pattern reflects the "sell in May" transition period
- October: Average 10.13 VIX (but can range 10-30+)
- Halloween to May Day (Nov 1 - May 1) = highest risk period historically

**Volatility Scoring Application:**

For High-Volatility Months (Sept, Oct, Nov):
- Widen stops by 30-50% to account for spike risk
- Reduce position size by 20-30%
- Increase profit target (higher moves likely)
- Require higher confirmation levels

For Low-Volatility Months (April, Dec, Jan):
- Tighter stops acceptable
- Can increase position size slightly
- Lower moves expected
- Still require confirmation

---

## Decadal & Long-Term Cycles

### Secular Bull vs. Bear Markets

**Definition:** Long-term (10+ year) trends in stock market direction

**Historical Patterns (Since 1960s):**

| Period | Type | Duration | Total Return | Avg Annual |
|--------|------|----------|--------------|-----------|
| 1982-2000 | Bull | 18 years | +582% | 10%+ |
| 2000-2009 | Bear | 9 years | -57% | -6%+ |
| 2009-2022 | Bull | 13 years | +401% | 14%+ |
| 2022-? | Transition | — | Mixed | — |

**Characteristics of Bull Markets (Secular):**
- Low starting valuations (P/E < 10)
- Strong earnings growth
- Rising productivity
- Low inflation
- Duration: 12-20 years average
- Total return: 300-600%

**Characteristics of Bear Markets (Secular):**
- High starting valuations (P/E > 20)
- Weak earnings growth
- Low productivity
- High inflation or deflation
- Duration: 7-15 years average
- Total return: -50% to -80%

**Current Cycle Position (2025):**
- 2022 marked potential bear market start (valuations fell)
- 2023-2024 recovery phase
- Status: Ambiguous - early bull or continued weakness?
- Historical bear markets last 7-15 years

**Scoring Application:**

In Early Bull Market Phase (2009-2022 pattern):
- +20 points to bullish trades (secular tailwind)

In Mid Bull Market Phase (strong growth):
- +15 points to bullish trades

In Late Bull Market Phase (valuations high):
- -10 points (reduce bullish bias)

In Secular Bear Market (weak earnings):
- -20 points (bearish bias)

---

## Special Seasonal Events

### 1. The January Effect (Weak Effect Today)

**Historical Definition:** Stock market rises in January due to tax-loss harvesting recovery

**Modern Reality:**
- Originally strong pattern (1950s-1980s)
- Has weakened significantly in modern era
- January 2025: historically neutral (positive 60% of time, +0.7% avg)

**Scoring:** 0 to +5 points (minimal effect)

---

### 2. The Santa Claus Rally

**Definition:** Stock rally from Christmas through New Year (Dec 25 - Jan 5)

**Historical Data:**
- Occurs ~75% of the time since 1969
- Average gain: +1-2% during period
- Most reliable seasonal pattern
- Lower volume, retail investor buying

**Current Status (2024-2025):**
- Should expect strength Dec 24, 2024 - Jan 5, 2025
- Watch for reversal in early January after holiday

**Scoring:**
- Dec 20 - Jan 5: +10 points (strong seasonal tailwind)
- Jan 6+: Pattern reverses, remove bonus

---

### 3. The "Worst Month" - September

**Unique Characteristic:** Only month with negative average return (-0.6%)

**Why September is Weak:**
- Hedge fund rebalancing
- End of summer vacation season
- Increased trading after Labor Day
- Historical crash dates: 1929, 1987, 2001 all in September/October
- Institutional traders resume after summer

**Historical September Stats:**
- Win rate: Only 32% (loses 68% of the time)
- Average return: -0.6%
- Maximum pain month: Highest historical volatility

**Scoring Application:**
When September arrives:
- Reduce bullish score by -15 points (major seasonal headwind)
- Increase stop distances by 30%
- Reduce position size by 25%
- Require extra confirmation for long trades

---

### 4. Best Quarter - Q4 (October-December Exception)

**Note:** While October is volatile, Q4 overall is strong

**Q4 Performance Stats:**
- November: +1.4% avg (3rd best month)
- December: +1.3% avg (4th best month)
- Q4 Average: Strong, ~3-4% typical

**October Paradox:**
- High volatility but positive 60% of time
- Often ends weak, but can recover in November
- "Buy the dip" strategy often works in late October

**Scoring:**
- November 1+: +12 points seasonal bonus
- October 1-15: Neutral (high volatility period)
- October 25+: Can shift bullish (+8 points) as Nov approaches

---

## Current Market Position (2025)

### Today's Date: October 19, 2025

**Current Seasonal Situation:**

1. **Month: October (Volatile month)**
   - Volatility spike risk: -10 points
   - Positive bias historically but risky: +3 points
   - Late October: Trending toward November strength

2. **Season: Transition from "Sell in May" to "Buy in November"**
   - We're in the last days of weak season
   - November 1 marks seasonal turning point
   - Prepare for Q4 strength

3. **Presidential Cycle: Year 1 (2025)**
   - Post-election year (weaker on average)
   - Headwind: -8 points
   - But Q4 strength typically overrides this

4. **Decadal Position: Uncertain (post-bear market recovery)**
   - Could be early bull or continued consolidation
   - Assume neutral: 0 points

5. **VIX Seasonality: Late October decline expected**
   - September-October volatility peak past
   - November typically calms down
   - Expect lower VIX through Q4

**Combined Seasonal Score (October 19, 2025):**
- Late October transitional period
- Bearish seasonality declining (was -10, now -5)
- November strength building (anticipate +12)
- Overall: Neutral to slightly bullish as month ends

---

## Scoring Application

### How Seasonality is Scored (0-100 Scale)

**Step 1: Identify Current Month & Seasonal Position**
- Check calendar month (Jan-Dec)
- Check presidential cycle year (1-4)
- Check market season (May-Oct weak, Nov-Apr strong)
- Check VIX seasonality (high risk months vs. calm months)

**Step 2: Assign Base Seasonal Score**

**Bullish Months (April, March, Nov, Dec):**
- Base: +12 to +15 points

**Neutral Months (May, Jul, Oct, Aug, Jan, Feb):**
- Base: -5 to +5 points (varies)

**Bearish Months (June, Sept):**
- Base: -15 to -5 points

**Step 3: Adjust for Special Events**

- If Dec 20 - Jan 5: +10 extra points (Santa rally)
- If September: -10 extra points (worst month)
- If High volatility month (Sept-Oct-Nov): Adjust stops/position size
- If Presidential Year 3: +15 points
- If Presidential Year 2: -10 points

**Step 4: Calculate Final Seasonal Component**

Final Seasonal Score (0-100) used as component in:
```
Total Probability = (0.40 × TA_Score)
                  + (0.25 × Context_Score)
                  + (0.15 × Sentiment_Score)
                  + (0.10 × Volume_Score)
                  + (0.10 × Seasonality_Score)  ← This component
```

**Example:**
```
Month: April (bullish): +15
Market Position: May-Oct weak season (April ends it): -0
Presidential Cycle: Year 1 (weakness): -8
Special Events: None: 0

SEASONAL SCORE: 15 - 8 = +7 points
As 0-100 component: Base 50 + 7 = 57 points
In probability formula: 57 × 0.10 = 5.7 points of final score
```

---

## Quick Reference: Monthly Seasonal Adjustments

| Month | Seasonal Bias | Points | Notes |
|-------|---------------|--------|-------|
| January | Neutral (weak) | -3 | Tax recovery over |
| February | Weak | -5 | Second-worst month historically |
| March | Bullish | +12 | Spring strength begins |
| April | **Very Bullish** | +15 | Best month historically |
| May | Weak/Neutral | -5 | "Sell in May" starts |
| June | Weak | -8 | Second-weakest month |
| July | Neutral | +3 | Summer relief rally |
| August | Weak | -5 | Summer doldrums |
| September | **Very Bearish** | -15 | Only negative month |
| October | Volatile (neutral) | 0 | Paradox: high vol but positive 60% |
| November | Bullish | +12 | Q4 strength begins |
| December | **Bullish** | +13 | Strong finish + Santa rally |

---

## Integration with Real-Time Analysis Engine

When analyzing a ticker, the engine will:

1. **Identify current month** from system date
2. **Look up seasonal bias** from this database
3. **Apply presidential cycle position** (automatically calculated)
4. **Assess volatility seasonality** if in high-vol months
5. **Add to seasonal score component** (weighted 10% in final probability)

**Example Trade Analysis Output:**

```
TICKER: SPY
DATE: October 19, 2025

SEASONALITY ASSESSMENT:
- Current Month: October (volatile but positive 60%)
- Season: End of "weak season", beginning of Q4 strength
- Presidential Cycle: Year 1 (post-election headwind)
- VIX Seasonality: Volatility declining, good entry month

SEASONAL SCORE: 55/100
- Month adjustment: -2 (late October, improving)
- Presidential cycle: -8 (Year 1 weakness)
- Transition bonus: +15 (late Oct → Nov strength)

INTERPRETATION: Neutral-to-bullish seasonal setup.
November traditionally strong, September weakness ending.
Consider entry with tight stops due to late-month volatility.
```

---

**Seasonality Database Complete**
**Effective Date:** 2025-10-19
**Version:** 1.0
**Data Sources:** 50+ years historical; Stock Market Almanac; CMT standards
**Confidence Level:** 65% accuracy (historical patterns, not predictive guarantee)
