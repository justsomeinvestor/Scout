# Trading Levels Dashboard - Implementation Plan

**Created:** 2025-10-15
**Status:** In Progress
**Goal:** Transform the Technicals tab into a live, actionable intraday trading levels dashboard

---

## Problem Statement

The current Technicals tab shows static options data that's manually entered and quickly goes stale. We have a working options data fetcher (`fetch_options_data.py`) but it's not integrated into the workflow, so the dashboard never gets fresh data.

**What's Missing:**
- No automatic options data updates during intraday refreshes
- Options intelligence exists but isn't actionable
- Close probability widget is vague ("48% lower") without context
- No time-based strategy adaptation (10 AM vs 3 PM matters!)

---

## What We Already Have ✅

### Working Infrastructure
- **`fetch_options_data.py`** - Fetches from Yahoo Finance API (free)
  - Calculates: Max Pain, Put/Call Ratio, IV Percentile, Total OI
  - Identifies: Call Walls, Put Walls, High Gamma strikes
  - Saves to: `Research/.cache/YYYY-MM-DD_options_data.json`

### Existing Workflows
- **`run_intraday_update.py`** - Fast 2-3 minute refresh cycle
  - Fetches market data (prices, Fear & Greed, VIX)
  - Calculates signals
  - Updates master-plan.md
  - **DOESN'T** fetch options data (yet!)

### Dashboard Display
- **`research-dashboard.html`** (lines 2523-2591)
  - Renders Close Probability widget
  - Shows Options Intelligence section
  - Data comes from `master-plan.md` YAML (manual/stale)

---

## The Solution - 3 Core Parts

### Part 1: Wire Up Automatic Options Data Collection

**Modify: `scripts/run_intraday_update.py`**

Add options data fetch to the workflow:

```python
# After Phase 1: Fetch Market Data
# ADD NEW: Phase 1.5: Fetch Options Data
print("\n" + "="*70)
print("📊 PHASE 1.5: FETCH OPTIONS DATA")
print("="*70)

options_script = scripts_dir / "fetch_options_data.py"
result = run_script(options_script, date_str, "SPY")
results['options'] = result

if not result['success']:
    print("\n⚠️  Phase 1.5 Warning: Options data fetch failed (continuing)")
else:
    print(f"\n✅ Phase 1.5 Complete ({result['elapsed']:.1f}s)")
```

**Result:** Every intraday update (every time prices change) automatically pulls fresh options data.

---

### Part 2: Auto-Update Options Data in Master Plan

**Modify: `scripts/update_master_plan.py`**

Load options data from cache and inject into master-plan.md:

```python
def load_data(self):
    # ... existing code ...

    # ADD: Load options data (optional)
    options_file = self.cache_dir / f"{self.date_str}_options_data.json"
    if options_file.exists():
        with open(options_file) as f:
            self.options_data = json.load(f)
        print(f"   [OK] Options data loaded")
    else:
        print(f"   [WARN] Options data not found (optional)")

def update_master_plan(self):
    # ... existing updates ...

    # ADD: Update optionsData section
    if self.options_data:
        self.update_options_section()

def update_options_section(self):
    """Update optionsData and closeProbability in technicals tab"""
    # Find technicals tab and update:
    # - optionsData.SPY (max pain, P/C, IV, key levels)
    # - closeProbability.SPY (intraday bias)
```

**Result:** Options data flows from fetch → cache → master-plan.md automatically.

---

### Part 3: Enhance Options Intelligence

**Modify: `scripts/fetch_options_data.py`**

Add three new calculations:

#### 3A. Intraday Directional Bias (replaces static close probability)

```python
def calculate_intraday_bias(self, current_price, max_pain, put_call_ratio, iv_percentile):
    """
    Calculate directional bias based on options positioning + time of day

    Logic:
    - If price > max_pain + late day (after 2pm) = bearish lean (gravity down)
    - If price < max_pain + late day = bullish lean (gravity up)
    - If P/C ratio elevated (>1.0) = more hedging = bearish tilt
    - If IV percentile high (>70) = expensive protection = cautious
    """

    now = datetime.now()
    est_time = now.astimezone(timezone('America/New_York'))
    hour = est_time.hour
    minute = est_time.minute
    time_minutes = hour * 60 + minute

    # Market hours: 9:30 AM - 4:00 PM ET (570 - 960 minutes)
    is_late_day = time_minutes >= 840  # After 2:00 PM

    distance_from_max_pain = current_price - max_pain

    # Calculate probability lean
    bearish_factors = 0
    bullish_factors = 0

    if distance_from_max_pain > 2 and is_late_day:
        bearish_factors += 2  # Strong bearish (price above max pain late)
    elif distance_from_max_pain > 2:
        bearish_factors += 1  # Mild bearish

    if distance_from_max_pain < -2 and is_late_day:
        bullish_factors += 2  # Strong bullish (price below max pain late)
    elif distance_from_max_pain < -2:
        bullish_factors += 1  # Mild bullish

    if put_call_ratio > 1.0:
        bearish_factors += 1  # Elevated hedging

    if iv_percentile > 70:
        bearish_factors += 1  # Expensive protection

    # Calculate lean percentage
    total_factors = bearish_factors + bullish_factors
    if total_factors == 0:
        lean = "Neutral"
        probability = 50
    elif bearish_factors > bullish_factors:
        lean = "Bearish Lean"
        probability = 50 + (bearish_factors / total_factors * 20)
    else:
        lean = "Bullish Lean"
        probability = 50 + (bullish_factors / total_factors * 20)

    # Generate WHY explanation
    reasons = []
    if abs(distance_from_max_pain) > 2:
        direction = "above" if distance_from_max_pain > 0 else "below"
        reasons.append(f"Price {direction} max pain (${current_price:.0f} vs ${max_pain:.0f}) = dealer {'selling' if direction == 'above' else 'buying'}")

    if put_call_ratio > 1.0:
        reasons.append(f"Put/Call ratio {put_call_ratio:.2f} (elevated hedging demand)")

    if iv_percentile > 70:
        reasons.append(f"IV percentile {iv_percentile:.0f}% (expensive protection)")

    if is_late_day:
        reasons.append(f"{est_time.strftime('%I:%M %p')} - Gravity toward max pain increases")

    return {
        "lean": lean,
        "probability": int(probability),
        "reasons": reasons,
        "timeContext": "LATE SESSION" if is_late_day else "EARLY SESSION"
    }
```

#### 3B. Resistance/Support Level Tagging

```python
def classify_level_importance(self, strike, oi, level_type, current_price, max_pain):
    """
    Tag each level with importance and actionable context

    Returns:
    - importance: "HARD WALL" | "Soft Resistance" | "STRUCTURAL"
    - context: What to watch for / what happens here
    """

    if level_type == "Call Wall" and strike > current_price:
        if oi > 100000:
            return {
                "importance": "🔴 HARD WALL",
                "context": f"→ Dealers sell into strength above ${strike}",
                "note": "80% rejection rate (high OI concentration)"
            }
        else:
            return {
                "importance": "🟡 Soft Resistance",
                "context": f"→ Breakout triggers squeeze to next level",
                "note": ""
            }

    elif level_type == "Max Pain":
        return {
            "importance": "🟢 MAX PAIN",
            "context": f"→ Magnetic pull for EOD close",
            "note": "High gamma support (dealers buy dips)"
        }

    elif level_type == "Put Wall" and strike < current_price:
        if strike == max_pain:
            return {
                "importance": "🟢 STRUCTURAL SUPPORT",
                "context": f"→ Dealer positioning + max pain alignment",
                "note": "Strong support zone"
            }
        else:
            return {
                "importance": "🟡 Support Level",
                "context": f"→ Put interest concentration",
                "note": ""
            }

    # Gamma flip levels
    if level_type == "High Gamma":
        if strike < current_price:
            return {
                "importance": "🔴 GAMMA FLIP",
                "context": f"→ Break = dealer hedging accelerates selling",
                "note": "Likely cascade to next support"
            }

    return {
        "importance": level_type,
        "context": "",
        "note": ""
    }
```

#### 3C. Time-Based Strategy Adjustments

```python
def get_time_based_strategy(self, current_time_et):
    """
    Provide time-specific trading context

    Returns strategy adjustments based on time of day
    """
    hour = current_time_et.hour
    minute = current_time_et.minute
    time_minutes = hour * 60 + minute

    # 9:30-10:30 AM - Opening hour
    if 570 <= time_minutes <= 630:
        return {
            "session": "OPENING HOUR",
            "notes": [
                "⚠️  High volatility - wide spreads",
                "⚠️  Dealer positioning establishing",
                "✅ Wait for initial range to form (10:00 AM)"
            ]
        }

    # 10:30 AM - 2:00 PM - Midday
    elif 630 <= time_minutes <= 840:
        return {
            "session": "MIDDAY SESSION",
            "notes": [
                "✅ Most reliable price action",
                "⚠️  Max pain magnetism LOW (dealer positioning fluid)",
                "✅ Trend-following preferred over mean reversion"
            ]
        }

    # 2:00 PM - 4:00 PM - Late session
    elif 840 <= time_minutes <= 960:
        return {
            "session": "LATE SESSION",
            "notes": [
                "⚠️  Max pain magnetism HIGH (last 90 min)",
                "⚠️  Gamma exposure increases into close",
                "✅ Good time to fade moves away from max pain",
                "✅ Position squaring creates reversals"
            ]
        }

    # After hours
    else:
        return {
            "session": "AFTER HOURS",
            "notes": [
                "⚠️  Low liquidity - wide spreads",
                "⚠️  Options data reflects RTH positioning",
                "❌ Not recommended for options-based strategies"
            ]
        }
```

**Output Format (add to JSON):**

```json
{
  "ticker": "SPY",
  "maxPain": "$660",
  "putCallRatio": "1.05",
  "ivPercentile": "92%",

  "intradayBias": {
    "lean": "Bearish Lean",
    "probability": 60,
    "reasons": [
      "Price above max pain ($667 vs $660) = dealer selling",
      "Put/Call ratio 1.05 (elevated hedging demand)",
      "IV percentile 92% (expensive protection)",
      "2:45 PM - Gravity toward max pain increases"
    ],
    "timeContext": "LATE SESSION",
    "actionable": "Watch: If $665 breaks → accelerates to $660"
  },

  "keyLevels": [
    {
      "strike": "670",
      "type": "Call Wall",
      "importance": "🔴 HARD WALL",
      "context": "→ Dealers sell into strength above here",
      "note": "80% rejection rate (high OI concentration)",
      "oi": "140K",
      "gamma": "N/A"
    },
    {
      "strike": "660",
      "type": "Max Pain",
      "importance": "🟢 MAX PAIN",
      "context": "→ Magnetic pull for EOD close",
      "note": "High gamma support (dealers buy dips)",
      "oi": "210K",
      "gamma": "N/A"
    }
  ],

  "timeBasedStrategy": {
    "session": "LATE SESSION",
    "notes": [
      "⚠️  Max pain magnetism HIGH (last 90 min)",
      "⚠️  Gamma exposure increases into close",
      "✅ Good time to fade moves away from max pain"
    ]
  }
}
```

---

### Part 4: Rebuild Dashboard UI

**Modify: `master-plan/research-dashboard.html`** (lines 2523-2591)

Replace the existing technicals rendering with new structure:

```javascript
// Special handling for technicals tab
if (tab.id === 'technicals') {
    // Render AI Interpretation first (keep existing)
    if (tab.aiInterpretation) {
        contentEl.innerHTML += renderAIInterpretation(tab.aiInterpretation);
    }

    // NEW: Render Trading Levels Dashboard
    if (tab.optionsData && tab.optionsData.SPY) {
        const tradingLevelsHTML = renderTradingLevelsDashboard(
            tab.optionsData.SPY,
            dashboard.metrics
        );
        contentEl.innerHTML += tradingLevelsHTML;
    }
}

function renderTradingLevelsDashboard(optionsData, metrics) {
    const currentPrice = metrics?.find(m => m.label === 'SPY Current')?.value ?? '—';
    const vix = metrics?.find(m => m.label === 'VIX')?.value ?? '—';

    return `
        <div class="trading-levels-dashboard">
            <!-- Header: Current Status -->
            <div class="levels-header">
                <h3 class="section-title">📊 Trading Levels - SPY</h3>
                <div class="current-metrics">
                    <span class="metric">Current: <strong>${currentPrice}</strong></span>
                    <span class="metric">Max Pain: <strong>${optionsData.maxPain}</strong></span>
                    <span class="metric">VIX: <strong>${vix}</strong></span>
                    <span class="refresh-badge">Updated: ${optionsData.lastUpdated}</span>
                </div>
            </div>

            <!-- Resistance Levels -->
            <div class="levels-section">
                <h4 class="levels-section-title">RESISTANCE LEVELS</h4>
                <div class="levels-container">
                    ${renderLevels(optionsData.keyLevels, 'resistance', currentPrice)}
                </div>
            </div>

            <!-- Current Price Line -->
            <div class="current-price-line">
                ━━━━━━━━  CURRENT: ${currentPrice}  ━━━━━━━━
            </div>

            <!-- Support Levels -->
            <div class="levels-section">
                <h4 class="levels-section-title">SUPPORT LEVELS</h4>
                <div class="levels-container">
                    ${renderLevels(optionsData.keyLevels, 'support', currentPrice)}
                </div>
            </div>

            <!-- Intraday Bias -->
            ${renderIntradayBias(optionsData.intradayBias)}

            <!-- Time-Based Context -->
            ${renderTimeContext(optionsData.timeBasedStrategy)}
        </div>
    `;
}

function renderLevels(keyLevels, type, currentPrice) {
    // Filter levels by type (resistance = above current, support = below current)
    const currentPriceNum = parseFloat(currentPrice.replace(/[$,]/g, ''));

    const filtered = keyLevels.filter(level => {
        const strikeNum = parseFloat(level.strike);
        return type === 'resistance' ? strikeNum > currentPriceNum : strikeNum < currentPriceNum;
    });

    if (filtered.length === 0) {
        return '<div class="no-levels">No significant levels identified</div>';
    }

    return filtered.map(level => `
        <div class="level-card">
            <div class="level-header">
                <span class="level-importance">${level.importance}</span>
                <span class="level-strike">$${level.strike}</span>
            </div>
            <div class="level-stats">
                <span>OI: ${level.oi}</span>
                ${level.gamma !== 'N/A' ? `<span>Gamma: ${level.gamma}</span>` : ''}
            </div>
            <div class="level-context">${level.context}</div>
            ${level.note ? `<div class="level-note">${level.note}</div>` : ''}
        </div>
    `).join('');
}

function renderIntradayBias(intradayBias) {
    if (!intradayBias) return '';

    return `
        <div class="intraday-bias-section">
            <h4 class="section-title">INTRADAY BIAS</h4>
            <div class="bias-card">
                <div class="bias-header">
                    <span class="bias-icon">📉</span>
                    <span class="bias-label">${intradayBias.lean} (${intradayBias.probability}% probability)</span>
                </div>

                <div class="bias-reasons">
                    <strong>WHY:</strong>
                    <ul>
                        ${intradayBias.reasons.map(r => `<li>${r}</li>`).join('')}
                    </ul>
                </div>

                ${intradayBias.actionable ? `
                    <div class="bias-action">
                        <strong>WATCH:</strong> ${intradayBias.actionable}
                    </div>
                ` : ''}
            </div>
        </div>
    `;
}

function renderTimeContext(timeStrategy) {
    if (!timeStrategy) return '';

    return `
        <div class="time-context-section">
            <h4 class="section-title">TIME-BASED CONTEXT</h4>
            <div class="time-card">
                <div class="time-header">${timeStrategy.session}</div>
                <ul class="time-notes">
                    ${timeStrategy.notes.map(note => `<li>${note}</li>`).join('')}
                </ul>
            </div>
        </div>
    `;
}
```

**Add CSS Styles:**

```css
/* Trading Levels Dashboard */
.trading-levels-dashboard {
    margin-top: 25px;
    padding: 20px;
    background: rgba(139, 92, 246, 0.05);
    border: 1px solid rgba(139, 92, 246, 0.2);
    border-radius: 12px;
}

.levels-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 1px solid rgba(139, 92, 246, 0.2);
}

.current-metrics {
    display: flex;
    gap: 15px;
    font-size: 0.9em;
}

.current-metrics .metric strong {
    color: #8b5cf6;
    margin-left: 4px;
}

.levels-section {
    margin: 20px 0;
}

.levels-section-title {
    color: #8b5cf6;
    font-size: 0.9em;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-bottom: 10px;
}

.levels-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.level-card {
    background: rgba(139, 92, 246, 0.1);
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 8px;
    padding: 12px;
}

.level-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.level-importance {
    font-weight: 600;
    font-size: 0.95em;
}

.level-strike {
    font-size: 1.2em;
    font-weight: 700;
    color: #8b5cf6;
}

.level-stats {
    display: flex;
    gap: 15px;
    font-size: 0.85em;
    color: #9ca3af;
    margin-bottom: 8px;
}

.level-context {
    color: #e0e6f0;
    font-size: 0.9em;
    margin-bottom: 5px;
}

.level-note {
    color: #9ca3af;
    font-size: 0.85em;
    font-style: italic;
}

.current-price-line {
    text-align: center;
    color: #8b5cf6;
    font-weight: 600;
    font-size: 1.1em;
    margin: 20px 0;
    padding: 10px 0;
    border-top: 2px solid rgba(139, 92, 246, 0.3);
    border-bottom: 2px solid rgba(139, 92, 246, 0.3);
}

.intraday-bias-section,
.time-context-section {
    margin-top: 20px;
    padding: 15px;
    background: rgba(139, 92, 246, 0.08);
    border-radius: 8px;
}

.bias-card,
.time-card {
    background: rgba(139, 92, 246, 0.1);
    padding: 15px;
    border-radius: 8px;
}

.bias-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 15px;
    font-size: 1.1em;
    font-weight: 600;
    color: #8b5cf6;
}

.bias-reasons ul,
.time-notes {
    list-style: none;
    padding: 0;
    margin: 10px 0;
}

.bias-reasons li,
.time-notes li {
    padding: 5px 0;
    padding-left: 20px;
    position: relative;
}

.bias-reasons li:before {
    content: "•";
    position: absolute;
    left: 0;
    color: #8b5cf6;
}

.bias-action {
    margin-top: 15px;
    padding: 10px;
    background: rgba(139, 92, 246, 0.15);
    border-left: 3px solid #8b5cf6;
    border-radius: 4px;
}

.time-header {
    font-weight: 600;
    color: #8b5cf6;
    margin-bottom: 10px;
    font-size: 1.05em;
}
```

---

## Implementation Order

### ✅ Phase 1: Wire Up Data Flow (Foundation)
1. Modify `run_intraday_update.py` - add options fetch call
2. Modify `update_master_plan.py` - load and inject options data
3. **Test:** Run intraday update, verify options data flows to master-plan.md

### ✅ Phase 2: Enhance Intelligence (Brain)
4. Modify `fetch_options_data.py` - add intraday bias calculation
5. Modify `fetch_options_data.py` - add level classification
6. Modify `fetch_options_data.py` - add time-based strategy
7. **Test:** Run fetch script, verify JSON output has new fields

### ✅ Phase 3: Rebuild UI (Display)
8. Modify `research-dashboard.html` - replace technicals section
9. Add new CSS styles for trading levels
10. **Test:** Open dashboard, verify new layout renders correctly

### ✅ Phase 4: End-to-End Test
11. Run full intraday workflow
12. Verify data flows: fetch → cache → master-plan → dashboard
13. Check during different times of day (test time-based logic)

---

## Success Metrics

- [ ] Options data updates automatically every intraday refresh
- [ ] Dashboard shows fresh data (< 5 minutes old)
- [ ] Each level has clear actionable context
- [ ] Intraday bias explains WHY with options positioning
- [ ] Time-based strategy adapts throughout trading day
- [ ] Zero manual data entry required

---

## Future Enhancements (Post-MVP)

1. **Real Gamma Exposure**
   - Integrate Greeks API (need paid service or broker API)
   - Calculate actual GEX instead of "N/A"

2. **Multi-Ticker Support**
   - Add QQQ, IWM options data
   - Compare SPY vs QQQ positioning

3. **Historical Tracking**
   - Archive options data daily
   - Show "max pain accuracy" over time
   - Track level rejection rates

4. **Alert System**
   - Notify when price approaches key level
   - Alert on gamma flip crossings
   - Warn when dealer positioning shifts dramatically

5. **Broker Integration**
   - TDAmeritrade API for real Greeks
   - IBKR for more accurate OI data
   - Real-time streaming (vs 15-min delay Yahoo)

---

## Task Tracking

- [x] Document plan and save to RnD/Ideas
- [ ] Phase 1: Wire up data flow
- [ ] Phase 2: Enhance intelligence
- [ ] Phase 3: Rebuild UI
- [ ] Phase 4: End-to-end testing

---

**Next Action:** Start with Phase 1 - modify `run_intraday_update.py` to add options fetch call.
