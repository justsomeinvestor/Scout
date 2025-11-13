Portfolio Tab Improvement Plan
Overview
Enhance the Portfolio tab with visual deltas, health scoring, execution helpers, and confidence indicators to make it a truly powerful AI fund manager interface.
Proposed Improvements
1. Visual Delta Indicators ⭐ HIGH IMPACT
What: Show exact changes between current and target allocations with arrows and color coding
Add percentage point delta badges (e.g., "+10%" or "-5%") next to each allocation
Use directional arrows (↑ ↓ →) to show direction of change
Color code: Green for increases, Red for decreases, Gray for no change
Calculate dollar amounts for each delta
Why: Makes it instantly clear what needs to change without mental math
2. Allocation Health Score ⭐ HIGH IMPACT
What: Single 0-100 metric showing how well current allocation aligns with signal
Visual gauge/progress bar showing alignment score
Formula: Based on distance from optimal allocation for current signal tier
Color-coded zones: Red (<40), Yellow (40-60), Green (60-80), Blue (80-100)
Warning if misalignment is severe (score <40)
Why: One number to show portfolio positioning quality at a glance
3. Execution Helper ⭐ HIGH IMPACT
What: Calculate exact trades needed with current market prices
Fetch current prices for SPLG, BTC from latest data
Calculate exact shares/units to buy or sell
Show estimated transaction costs (0.1% assumption)
"Copy to Clipboard" button for quick execution
Format: Ready-to-paste trade list
Why: Removes friction between recommendation and execution
4. Confidence Indicators ⭐ MEDIUM IMPACT
What: Show AI confidence level for each recommendation
Overall confidence score (Low/Medium/High) based on:
Signal strength (how far from tier boundaries)
Data freshness (all sources updated today?)
Consensus level (X sentiment vs technicals alignment)
Per-action confidence tags
"High conviction" vs "low conviction" visual badges
Why: Helps prioritize which recommendations to follow first
5. Historical Context 🔵 NICE TO HAVE
What: Show previous recommendation and whether you followed it
Previous date and allocation
"You followed: Yes/No/Partial"
Simple 7-day allocation history sparkline
Track: Did following the AI help?
Why: Builds trust and accountability over time
6. Enhanced Risk Display 🔵 NICE TO HAVE
What: Show portfolio risk metrics (current vs target)
Expected volatility comparison
Beta to SPX/BTC
Max drawdown estimate
Downside protection score
Why: Quantifies risk reduction/increase from recommended changes
Implementation Priority
Phase 1 (Implement First):
Visual Delta Indicators
Allocation Health Score
Execution Helper
Phase 2 (If user wants more): 4. Confidence Indicators 5. Enhanced Risk Display 6. Historical Context
Technical Approach
Changes to master-plan.md:
Add allocationHealthScore field to portfolioRecommendation
Add confidenceLevel field
Add executionDetails object with prices and shares
Changes to research-dashboard.html:
Add delta calculation function
Add health score gauge rendering
Add execution helper section with copy button
Enhance CSS for new visual elements
Changes to ai_portfolio_advisor.py:
Calculate health score based on signal vs allocation
Determine confidence level from data quality
Fetch current market prices
Calculate exact shares needed
Example Enhanced Output
💼 Portfolio Health: 45/100 (Misaligned) ⚠️

Current → Target Allocation:
Cash:     50% → 60% [+10% ↑ +$5,000]
Equities: 30% → 25% [-5% ↓ -$2,500]
Crypto:   20% → 10% [-10% ↓ -$5,000]
Hedges:    0% →  5% [+5% ↑ +$2,500]

📋 Exact Trades (High Confidence):
→ Sell 52 shares SPLG @ $48.12 = $2,502
→ Sell 0.0427 BTC @ $116,800 = $4,987
→ Buy 125 VIX calls @ $20.00 = $2,500

[Copy Trade List] button

Confidence: HIGH (Signal 38 pts below MODERATE tier)
Ready to implement Phase 1 improvements?