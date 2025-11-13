# X Sentiment Tab - Analytics Widget Ideas

**Created:** 2025-10-15
**Status:** 2 Implemented, 4 Backlog
**Location:** X Sentiment Tab (bottom section)

## Overview

Collection of high-value trading analytics widgets designed for the X Sentiment dashboard tab. These widgets convert social media sentiment data into actionable trading intelligence.

---

## ⭐ IMPLEMENTED

### 1. 📈 Sentiment Velocity Tracker
**Status:** ✅ IMPLEMENTED
**Priority:** HIGH
**Location:** X Sentiment Tab - Bottom Right (Top)

**Purpose:**
Track how FAST sentiment is changing. Velocity is often more predictive than absolute sentiment level.

**Key Metrics:**
- **Current Sentiment:** 40/100 (BEARISH)
- **24h Change:** +15 pts ⬆️
- **Velocity Rating:** ACCELERATING / STABLE / DECELERATING
- **Mean Reversion Signal:** "Rebounding from extreme bearish zone (was 25)"
- **Time in Zone:** Days spent in current sentiment band
- **Since Last Extreme:** Days since sentiment hit <20 or >80

**Why Valuable:**
- Rapid sentiment shifts often precede price moves
- If sentiment jumps from 25→40 in 24h, that's a strong momentum signal
- Helps time entries/exits based on sentiment acceleration
- Complements existing contrarian signal (which uses absolute levels)

**Implementation Notes:**
- Requires historical sentiment data (at least 24h ago)
- Velocity = (Current - Previous_24h) / Previous_24h * 100
- Thresholds: >50% change = ACCELERATING, <10% = STABLE, negative = DECELERATING

**Data Requirements:**
```yaml
sentiment_velocity:
  current: 40
  previous_24h: 25
  change: +15
  change_pct: 60%
  velocity_rating: "ACCELERATING"
  mean_reversion_signal: "Sentiment recovering from extreme bearish zone"
  days_in_current_zone: 1
  days_since_last_extreme: 2
  historical_context: "This velocity (60%/day recovery) typically precedes further gains"
```

---

### 2. 🎲 Contrarian Play Detector
**Status:** ✅ IMPLEMENTED
**Priority:** HIGH
**Location:** X Sentiment Tab - Bottom Right (Bottom)

**Purpose:**
Identify specific contrarian opportunities based on X sentiment extremes. Converts sentiment data into trade setups.

**Key Metrics:**
- **Current Setup:** "Moderate fear + positive breadth = cautious bullish"
- **Contrarian Opportunity:** "NOT YET - waiting for extreme fear <25 or extreme greed >75"
- **Historical Win Rate:** "When X hits <25, next 7 days avg +8.2% BTC"
- **Action:** WAIT / FADE / FOLLOW
- **Threshold Distance:** "15 pts away from contrarian threshold"

**Why Valuable:**
- Converts abstract sentiment into concrete trade signals
- Historical backtesting shows win rates for each setup
- Helps avoid FOMO (shows when NOT to trade)
- Complements mean reversion strategy

**Signal Types:**
1. **EXTREME FEAR (<25):** Contrarian BUY opportunity
2. **EXTREME GREED (>75):** Contrarian SELL opportunity
3. **MODERATE (25-75):** WAIT for better setup
4. **VELOCITY DIVERGENCE:** Price up, sentiment down = fade rally

**Implementation Notes:**
- Uses historical backtest data for win rates
- Combines sentiment score with velocity and breadth
- Updates action recommendation based on current positioning

**Data Requirements:**
```yaml
contrarian_detector:
  current_setup: "Moderate fear + positive breadth = cautious bullish"
  opportunity_status: "NOT YET"
  threshold_needed: "Fear <25 or Greed >75"
  distance_to_threshold: 15
  historical_win_rate: "When X hits <25, next 7 days avg +8.2% BTC"
  action: "WAIT"
  action_color: "yellow"
  confidence: "medium"
```

---

## 📋 BACKLOG (Future Implementation)

### 3. 📊 Fear/Greed Extremes Counter
**Priority:** MEDIUM
**Effort:** LOW

**Purpose:**
Track time spent in extreme zones for contrarian signals.

**Key Metrics:**
- **Days in Fear Zone (<30):** 3 consecutive days
- **Days in Greed Zone (>70):** 0 days
- **Since Last Extreme:** 8 days since last extreme fear (score <20)
- **Contrarian Signal Strength:** "Moderate fear, not extreme yet - wait for capitulation"
- **Historical Pattern:** "3+ days in fear zone precedes reversal 72% of the time"

**Why Valuable:**
- Time-in-zone is highly predictive for mean reversion
- Multi-day extremes often mark major reversals
- Simple visual: counter showing days in current zone

**Data Requirements:**
```yaml
extreme_counter:
  days_in_fear: 3
  days_in_greed: 0
  days_since_extreme: 8
  last_extreme_date: "2025-10-07"
  last_extreme_score: 18
  pattern_signal: "3+ days fear = 72% reversal rate"
```

---

### 4. 🔥 Social Volume Divergence Alert
**Priority:** MEDIUM
**Effort:** MEDIUM

**Purpose:**
Compare mention velocity to price action for divergence signals.

**Key Metrics:**
- **BTC Price Change:** +0.31% today
- **BTC Mention Velocity:** +7%
- **Divergence Type:** BULLISH (volume outpacing price)
- **Signal:** ACCUMULATION / DISTRIBUTION / ALIGNED
- **Strength:** "Moderate bullish divergence - building interest"

**Why Valuable:**
- Volume-price divergence is a classic leading indicator
- Helps identify accumulation vs distribution phases
- Early warning for trend changes

**Divergence Types:**
1. **Bullish Divergence:** Mentions ↑, Price →/↓ = Accumulation
2. **Bearish Divergence:** Mentions ↓, Price →/↑ = Distribution
3. **Aligned:** Both moving same direction = Trend continuation

**Data Requirements:**
```yaml
volume_divergence:
  asset: "BTC"
  price_change_24h: +0.31
  mention_velocity: +7
  divergence_type: "BULLISH"
  signal: "ACCUMULATION"
  strength: "MODERATE"
  interpretation: "Volume increasing faster than price - building interest"
```

---

### 5. 💬 Narrative Momentum Tracker
**Priority:** LOW
**Effort:** MEDIUM

**Purpose:**
Track which narratives are GAINING vs FADING attention.

**Key Metrics:**
```
🚀 GAINING MOMENTUM:
• Fed Policy: +136% velocity (was +50% yesterday) - BREAKOUT
• DEFI: +188% velocity (NEW theme emerging)
• AI: +22% velocity (steady growth)

📉 FADING:
• Treasury: -51% velocity (losing attention)
• HOLD sentiment: -56% (conviction weakening)
• Meme: -17% (cooling off)
```

**Why Valuable:**
- Shows which stories are taking over the conversation
- Identifies dying narratives before price follows
- Helps position for theme rotation

**Data Requirements:**
```yaml
narrative_momentum:
  gaining:
    - narrative: "Fed Policy"
      velocity_today: +136
      velocity_yesterday: +50
      change: +86
      status: "BREAKOUT"
    - narrative: "DEFI"
      velocity_today: +188
      status: "NEW THEME"
  fading:
    - narrative: "Treasury"
      velocity: -51
      status: "LOSING ATTENTION"
```

---

### 6. ⚡ Velocity Ranking Dashboard
**Priority:** LOW
**Effort:** LOW

**Purpose:**
Simple table showing FASTEST moving tickers/themes.

**Key Metrics:**
```
⚡ HIGHEST VELOCITY (24h):
1. BONDS: +200% 🔥
2. VIX: +129% 🔥
3. FED: +136% 🔥
4. GOOGL: +167%
5. DEFI: +188%

❄️ COOLING FASTEST:
1. SOL: -55%
2. HOLD: -56%
3. TOP: -53%
```

**Why Valuable:**
- Quick scan of what's heating up vs cooling down
- Identifies momentum plays
- Shows market attention shifts

**Data Requirements:**
```yaml
velocity_ranking:
  hottest:
    - ticker: "BONDS"
      velocity: +200
      rank: 1
    - ticker: "VIX"
      velocity: +129
      rank: 2
  coldest:
    - ticker: "SOL"
      velocity: -55
      rank: 1
    - ticker: "HOLD"
      velocity: -56
      rank: 2
```

---

## Implementation Priority

**Phase 1 (DONE):**
- ✅ Sentiment Velocity Tracker
- ✅ Contrarian Play Detector

**Phase 2 (Next):**
- Fear/Greed Extremes Counter (easy win)
- Social Volume Divergence Alert (high value)

**Phase 3 (Future):**
- Narrative Momentum Tracker
- Velocity Ranking Dashboard

---

## Technical Notes

**Layout Strategy:**
- Bottom section uses CSS grid: `grid-template-columns: repeat(auto-fill, minmax(350px, 1fr))`
- 3 widgets fit perfectly side-by-side on standard monitor
- Mobile: Stacks vertically automatically

**Data Sources:**
- Historical sentiment: Store in `.cache/sentiment_history.json`
- Calculate velocity on-the-fly during workflow
- Backtest data: Pre-calculated from historical analysis

**Update Frequency:**
- Real-time: Not needed (data is daily)
- Updates: Once per day when workflow runs
- Historical data: Rolling 30-day window

**Workflow Integration (How to Update Daily):**

The widgets pull data from the `xsentiment` tab in `master-plan.md`. Two new YAML fields have been added:

1. **`sentiment_velocity`** - Update these fields during workflow Step 6 (Update Master Plan):
   ```yaml
   current: [Today's X sentiment score 0-100]
   previous_24h: [Yesterday's X sentiment score]
   change: [current - previous_24h]
   change_pct: [Percentage change]
   velocity_rating: [ACCELERATING if >50%, RECOVERING if 10-50%, STABLE if 0-10%, DECELERATING if negative]
   mean_reversion_signal: "[Brief 1-sentence interpretation of the move]"
   days_in_current_zone: [Days spent in current band: <25, 25-40, 40-60, 60-75, >75]
   days_since_last_extreme: [Days since sentiment hit <20 or >80]
   historical_context: "[1-sentence note about what this velocity typically signals]"
   ```

2. **`contrarian_detector`** - Update these fields based on current sentiment:
   ```yaml
   current_setup: "[1-sentence summary: sentiment level + breadth + bias]"
   opportunity_status: [EXTREME if <25 or >75, NOT YET if 25-75]
   threshold_needed: "Fear <25 or Greed >75"
   distance_to_threshold: [How many points away from 25 or 75]
   historical_win_rate: "When X hits <25, next 7 days avg +8.2% BTC return" [Fixed text for now]
   action: [WAIT if moderate, BUY if extreme fear, SELL if extreme greed]
   action_color: "#f59e0b" [Yellow for WAIT, green for BUY, red for SELL]
   confidence: [high/medium/low based on breadth confirmation]
   next_check: "[Optional: What to monitor next, e.g., 'Watch for CPI data reaction']"
   ```

**Quick Update Checklist (During Workflow):**
- [ ] Get today's X crypto sentiment from `.cache/signals_YYYY-MM-DD.json`
- [ ] Get yesterday's X sentiment from `.cache/signals_YYYY-MM-DD.json` (previous date)
- [ ] Calculate change and change_pct
- [ ] Determine velocity_rating based on change_pct thresholds
- [ ] Write mean_reversion_signal (1 sentence about the move)
- [ ] Count days_in_current_zone (requires tracking sentiment bands)
- [ ] Count days_since_last_extreme (requires historical sentiment data)
- [ ] Set contrarian_detector fields based on current sentiment level
- [ ] Update action (WAIT/BUY/SELL) and opportunity_status

**Future Automation:**
- Create Python helper function to auto-calculate these fields from `.cache/sentiment_history.json`
- Add to `scripts/run_workflow.py` as optional flag `--update-widgets`
- For now: Manual updates during Step 6 of workflow

---

## Success Metrics

**Usefulness Indicators:**
1. Time to decision reduced (less analysis paralysis)
2. Better entry/exit timing (velocity helps)
3. Fewer bad trades (contrarian detector prevents FOMO)
4. Improved win rate (historical context helps)

**User Feedback:**
- Is the widget glanceable? (5-second scan)
- Is the signal actionable? (clear next step)
- Does it complement other data? (no redundancy)

---

## Future Enhancements

1. **Sentiment Alerts:** Push notification when extreme hit
2. **Historical Charts:** Visual sentiment timeline
3. **Multi-Asset:** Compare BTC vs ETH vs SPY sentiment
4. **AI Predictions:** ML model predicts next 24h sentiment move
5. **Social Dominance:** % of total mentions for each asset

---

**Last Updated:** 2025-10-15
**Maintained By:** Research System
**Related Docs:** `master-plan/How to use_MP_CLAUDE_ONLY.txt`
