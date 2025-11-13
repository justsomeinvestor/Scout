# X Sentiment Tab Update Workflow

**Phase**: 3.75 (runs after Phase 3.7 - Process Trending Words)
**Script**: `scripts/automation/update_x_sentiment_tab.py`
**Purpose**: Updates the X/Twitter Sentiment Analysis tab with fresh crypto + macro sentiment data

---

## Overview

The X Sentiment tab provides real-time sentiment analysis from X/Twitter, combining:
- **Crypto sentiment** (extracted from crypto influencer posts)
- **Macro sentiment** (extracted from macro/finance influencer posts)
- **Trending tickers** with velocity indicators (NEW/RISING/STABLE/FADING)
- **Emerging alpha opportunities** (new tickers with momentum)
- **AI Narrative Briefing** (combined sentiment analysis)

---

## Data Sources Required

### 1. X Crypto Summary
**Path**: `Research/X/{date}_X_Crypto_Summary.md`
**Created By**: Manual research or AI summary generator
**Required Format**:
```markdown
## Sentiment Analysis

- **Bullish:** 245 posts (61%)
- **Bearish:** 85 posts (21%)
- **Neutral:** 70 posts (18%)
- **Sentiment Score:** 68/100
```

**Critical Fields**:
- Line ~9: `- **Sentiment Score:** XX/100` (numeric score, label generated automatically)
- Sentiment breakdown percentages (bullish/bearish/neutral posts)
- Top Narratives section (optional)
- Most Discussed Tickers/Assets (optional)

**Note**: Script automatically infers sentiment label from score (60-69 = MODERATELY BULLISH, etc.). Label in file optional but will be ignored if present.

### 2. X Macro Summary
**Path**: `Research/X/{date}_X_Macro_Summary.md`
**Created By**: Manual research or AI summary generator
**Required Format**:
```markdown
## Sentiment Analysis

- **Bullish:** 95 posts (47%)
- **Bearish:** 68 posts (34%)
- **Neutral:** 37 posts (19%)
- **Sentiment Score:** 52/100
```

**Critical Fields**:
- Line ~9: `- **Sentiment Score:** XX/100` (numeric score, label generated automatically)
- Sentiment breakdown percentages (bullish/bearish/neutral posts)
- Top Narratives section (optional)
- Most Discussed Tickers/Assets (optional)

**Note**: Script automatically infers sentiment label from score (50-59 = NEUTRAL, etc.). Label in file optional but will be ignored if present.

### 3. Trending Words JSON
**Path**: `Research/X/Trends/{date}_trending_words.json`
**Created By**: Phase 3.7 - `process_trends.py`
**Required Structure**:
```json
{
  "timestamp": "2025-10-23T...",
  "total_posts_analyzed": 361,
  "crypto_posts": 250,
  "macro_posts": 111,
  "categories": {
    "tickers_crypto": [
      {"word": "$BTC", "mentions": 24, "rank": 1, "velocity_24h": "NEW", "signal": "RISING"},
      {"word": "$ETH", "mentions": 17, "rank": 2, "velocity_24h": "NEW", "signal": "RISING"}
    ],
    "tickers_equities": [
      {"word": "$TSLA", "mentions": 10, "rank": 1, "velocity_24h": "NEW", "signal": "RISING"},
      {"word": "$SPX", "mentions": 5, "rank": 2, "velocity_24h": "NEW", "signal": "RISING"}
    ]
  }
}
```

---

## What Gets Updated

### 1. AI Narrative Briefing

Located at the top of the X Sentiment tab (AI Interpretation section).

**Before Fix** (when regex fails):
```yaml
aiInterpretation:
  summary: No crypto sentiment data available. No macro sentiment data available.
  keyInsight: 'Combined sentiment: 50/100 (NEUTRAL).'
  action: Sentiment is neutral. Wait for clearer directional signals...
  sentiment: neutral
  confidence: high
```

**After Fix** (with working regex):
```yaml
aiInterpretation:
  updatedAt: '2025-10-24T00:19:20Z'
  summary: 'Crypto sentiment: 68/100 (Moderately Bullish) Macro sentiment: 52/100 (Balanced/Mixed)'
  keyInsight: 'Combined sentiment: 60/100 (MODERATELY BULLISH).'
  action: Sentiment is constructive. Look for dips to add exposure in high-conviction areas.
  sentiment: bullish
  confidence: high
```

**Sentiment Score Calculation**:
```python
combined_score = (crypto_score + macro_score) / 2
# Example: (68 + 52) / 2 = 60
```

**Sentiment Tiers**:
- 90-100: EXTREME BULLISH
- 70-89: STRONG BULLISH
- 60-69: MODERATELY BULLISH
- 50-59: BALANCED/NEUTRAL
- 40-49: MODERATELY BEARISH
- 20-39: WEAK
- 0-19: EXTREME BEARISH

---

### 2. Crypto Trending Section

**Structure** (10 tickers + emerging + subsections):
```yaml
crypto_trending:
  top_tickers:
    - ticker: BTC
      mentions: 24
      velocity: NEW                    # NEW, +XX%, -XX%, STABLE, FADING
      signal: RISING                   # RISING, STABLE, FADING
    - ticker: ETH
      mentions: 17
      velocity: NEW
      signal: RISING
    # ... 8 more tickers (10 total)

  emerging_tickers:                    # Up to 5 tickers
    - ticker: BTC
      mentions: 24
      signal: Alpha opportunity - new entrant with momentum
    # ... criteria: velocity == "NEW" AND mentions >= 3

  key_levels: []                       # Crowdsourced price levels (future feature)
  event_risk: []                       # High-velocity events (future feature)
  updatedAt: '2025-10-24T00:19:20Z'
```

**Top Tickers Logic**:
- **Limit**: 10 tickers (line 323: `[:10]`)
- **Source**: `trending_words.json` → `categories.tickers_crypto`
- **Sorting**: By mention count (descending)
- **Velocity Calculation**: Day-over-day change vs previous day's counts
  - `NEW`: First appearance (not in yesterday's data)
  - `+XX%`: Mentions increased by XX%
  - `-XX%`: Mentions decreased by XX%
  - `STABLE`: ±5% change
  - `FADING`: Significant decrease

**Emerging Tickers Logic**:
- **Criteria**: `velocity == "NEW"` AND `mentions >= 3`
- **Limit**: 5 tickers max
- **Signal**: "Alpha opportunity - new entrant with momentum"
- **Purpose**: Identify new tickers gaining traction

---

### 3. Macro Trending Section

**Structure** (identical to crypto):
```yaml
macro_trending:
  top_tickers:                         # 10 tickers (TSLA, SPX, NFLX, NVDA, SPY, AMD, IWM, META, GOOGL, QQQ)
    - ticker: TSLA
      mentions: 10
      velocity: NEW
      signal: RISING
    # ... 9 more tickers

  emerging_tickers:                    # Up to 5 tickers
    - ticker: TSLA
      mentions: 10
      signal: Alpha opportunity - new entrant with momentum
    # ... criteria: velocity == "NEW" AND mentions >= 5 (higher threshold)

  key_levels: []
  event_risk: []
  updatedAt: '2025-10-24T00:19:20Z'
```

**Emerging Tickers Threshold Difference**:
- **Crypto**: `mentions >= 3` (lower threshold, crypto has fewer mentions)
- **Macro**: `mentions >= 5` (higher threshold, macro tickers more common)

---

## Dashboard Visual Layout

The X Sentiment tab displays in a **2-column grid**:

```
┌─────────────────────────────────────────────────────────────────┐
│ AI NARRATIVE BRIEFING                                           │
│ ├─ Summary Pulse: Crypto 68/100, Macro 52/100                  │
│ ├─ Key Insight: Combined 60/100 (MODERATELY BULLISH)           │
│ └─ Actionable Focus: Sentiment is constructive...              │
├─────────────────────────────┬───────────────────────────────────┤
│ 🔥 Crypto Trending          │ 📊 Macro Trending                 │
│ ├─ Top 10 Tickers           │ ├─ Top 10 Tickers                 │
│ │  BTC, ETH, ONE, SOL...    │ │  TSLA, SPX, NFLX, NVDA...       │
│ ├─ Emerging Tickers (5)     │ ├─ Emerging Tickers (2)           │
│ │  BTC, ETH, ONE, SOL, LINK │ │  TSLA, SPX                      │
│ ├─ Key Levels (0)           │ ├─ Key Levels (0)                 │
│ └─ Event Risk (0)           │ └─ Event Risk (0)                 │
└─────────────────────────────┴───────────────────────────────────┘
```

**Visual Balance**: Both columns show 10 tickers for symmetric layout (fixed 2025-10-24).

---

## Recent Fixes (2025-10-24)

### Issue 1: Crypto Showed Only 7 Tickers
**Problem**: Crypto column shorter than macro (7 vs 10 tickers), creating visual asymmetry.

**Root Cause**: Line 323 had `crypto_trending['top_tickers'] = top_tickers[:7]`

**Fix Applied**:
```python
# Before
crypto_trending['top_tickers'] = top_tickers[:7]

# After
crypto_trending['top_tickers'] = top_tickers[:10]
```

**Impact**: Both crypto and macro now show 10 tickers, creating perfect 2-column symmetry.

---

### Issue 2: Sentiment Score Regex Mismatch (FIXED Oct 27, 2025)
**Problem**: Script reported "CRYPTO SENTIMENT DATA MISSING" even though files existed.

**Root Cause**: Regex pattern expected label in parentheses that never existed in actual files.
```python
# OLD (WRONG - expected: "60/100 (BULLISH)")
sentiment_match = re.search(r'\*\*Sentiment Score:\*\*\s*(\d+)/100\s*\(([^)]+)\)', content)

# Actual file format (reality):
- **Sentiment Score:** 60/100     # No label in parentheses!
```

**Fix Applied** (Lines 137 + 172):
```python
# NEW (CORRECT - matches actual file format)
sentiment_match = re.search(r'\*\*Sentiment Score:\*\*\s*(\d+)/100', content)

# Then infer label from score using _infer_sentiment_label() helper
self.crypto_data['sentiment_label'] = self._infer_sentiment_label(int(sentiment_match.group(1)))
```

**Sentiment Label Tiers** (auto-generated):
- 70-100: STRONGLY/EXTREME BULLISH
- 60-69: BULLISH/MODERATELY BULLISH
- 50-59: NEUTRAL/MODERATELY BULLISH
- 40-49: NEUTRAL/MODERATELY BEARISH
- 20-39: BEARISH/WEAK
- 0-19: EXTREME BEARISH

**Impact**:
- ✅ Script now correctly extracts all sentiment scores
- ✅ Works with files that have NO label, WITH label, or different label format
- ✅ AI Narrative Briefing auto-populates with inferred labels
- ✅ Path resolution fix (repo_root) ensures files are found reliably

---

## Running the Update

### Automated (Recommended):
```bash
python scripts/automation/run_workflow.py 2025-10-23
```
The workflow automatically runs Phase 3.75 after Phase 3.7.

### Manual (For Testing):
```bash
python scripts/automation/update_x_sentiment_tab.py 2025-10-23
```

---

## Expected Console Output

**Successful Execution**:
```
============================================================
X SENTIMENT TAB UPDATER
============================================================
Date: October 23, 2025

[1/4] Loading data sources...
   [OK] Crypto summary loaded: 68/100          ← Sentiment score extracted ✅
   [OK] Macro summary loaded: 52/100           ← Sentiment score extracted ✅
   [OK] Trending words loaded: 361 posts analyzed

[2/4] Loading master plan...
   [OK] Master plan loaded (5 tabs)

[3/4] Updating X Sentiment tab...
   [OK] Found xsentiment tab at index 2
   [OK] Updated xsentiment tab
   [OK] Sentiment: 60/100 (MODERATELY BULLISH) ← Combined score ✅
   [OK] Narratives: 0
   [OK] Trending words: 14 crypto, 10 equities
   [OK] Crypto trending: 10 tickers, 5 emerging, 0 events ← 10 tickers! ✅
   [OK] Macro trending: 10 tickers, 2 emerging

[4/4] Saving master plan...
   [OK] Master plan saved
   [OK] Backup created

============================================================
✅ X SENTIMENT TAB UPDATE COMPLETE
============================================================

📊 Data Sources: 3/3 found                     ← All sources found! ✅
```

---

## Validation Checklist

After running the update, verify:

### Console Output:
- [ ] "Crypto summary loaded: XX/100" (not "N/A")
- [ ] "Macro summary loaded: XX/100" (not "N/A")
- [ ] "Data Sources: 3/3 found" (not "1/3" or "2/3")
- [ ] "Crypto trending: 10 tickers" (not "7 tickers")
- [ ] "Macro trending: 10 tickers"
- [ ] No Python errors or exceptions

### Dashboard (After Hard Refresh):
- [ ] AI Narrative Briefing shows: "Crypto sentiment: XX/100... Macro sentiment: XX/100..."
- [ ] Crypto Trending section displays 10 tickers
- [ ] Macro Trending section displays 10 tickers
- [ ] Both sections have equal visual height (side-by-side in 2-column grid)
- [ ] Emerging Tickers subsections display (if data available)
- [ ] No empty collapsed sections with orange dots

---

## Troubleshooting

### Problem: "No crypto/macro sentiment data available"
**Symptoms**:
- Console shows: "Crypto summary loaded: N/A/100"
- AI Narrative displays fallback text

**Diagnosis**:
```bash
# Check if summary files exist
ls Research/X/*_X_Crypto_Summary.md
ls Research/X/*_X_Macro_Summary.md

# Check file format (should show line ~14 with sentiment score)
grep -n "Sentiment Score" Research/X/2025-10-23_X_Crypto_Summary.md
grep -n "Sentiment Score" Research/X/2025-10-23_X_Macro_Summary.md
```

**Expected Output**:
```
14:- **Sentiment Score:** 68/100 (Moderately Bullish)
```

**Fix**:
- Ensure summary files contain `**Sentiment Score:** XX/100` format
- Verify regex pattern in update_x_sentiment_tab.py matches actual format (line 136 + 171)

---

### Problem: "Crypto trending: 7 tickers" (should be 10)
**Diagnosis**:
```bash
# Check line 323 in the script
grep -n "top_tickers\[:7\]" scripts/automation/update_x_sentiment_tab.py
```

**Expected**: No matches (should be `[:10]`)

**Fix**:
```python
# Update line 323
crypto_trending['top_tickers'] = top_tickers[:10]  # Not [:7]
```

---

### Problem: "Data Sources: 1/3 found"
**Cause**: Missing X summary files or trending_words.json

**Diagnosis**:
```bash
# Check all required files exist
ls Research/X/2025-10-23_X_Crypto_Summary.md
ls Research/X/2025-10-23_X_Macro_Summary.md
ls Research/X/Trends/2025-10-23_trending_words.json
```

**Fix**:
- Ensure Phase 3.7 (Process Trending Words) ran successfully
- Verify X data was scraped and archived for this date
- Check archived JSON files exist:
  - `Research/X/Crypto/x_list_posts_20251023_archived.json`
  - `Research/X/Macro/x_list_posts_20251023_archived.json`

---

### Problem: Empty Trending Sections (Vertical Stacking)
**Symptoms**: Crypto and Macro sections stack vertically instead of side-by-side

**Cause**: HTML structure bug (unclosed divs)

**Fix**: Verify `research-dashboard.html` has proper div closings (see `ACTUAL_FIX_GRID_LAYOUT.md`)

---

## File Structure in master-plan.md

```yaml
dashboard:
  tabs:
    - id: xsentiment
      label: 🐦 X Sentiment

      # AI Narrative Briefing (top of tab)
      aiInterpretation:
        updatedAt: '2025-10-24T00:19:20Z'
        summary: 'Crypto sentiment: 68/100 (Moderately Bullish) Macro sentiment: 52/100 (Balanced/Mixed)'
        keyInsight: 'Combined sentiment: 60/100 (MODERATELY BULLISH).'
        action: Sentiment is constructive. Look for dips to add exposure...
        sentiment: bullish
        confidence: high

      # Overall Metrics
      sentimentScore: 60                    # (crypto + macro) / 2
      sentimentTier: MODERATELY BULLISH
      sentimentTrend: stable
      contrarian_signal: 0 pts (Neutral)

      # Sentiment Breakdown (estimated from combined score)
      sentiment_breakdown:
        extreme_bullish: 5
        bullish: 30
        neutral: 35
        bearish: 20
        extreme_bearish: 5

      # Hype Cycle Indicators
      hype_cycle:
        position: Skepticism
        emoji_density: Low
        caps_lock_usage: Low
        exclamation_marks: Low

      # Crypto Trending Section
      crypto_trending:
        top_tickers:                        # 10 items
          - ticker: BTC
            mentions: 24
            velocity: NEW
            signal: RISING
          # ... 9 more tickers

        emerging_tickers:                   # 0-5 items
          - ticker: BTC
            mentions: 24
            signal: Alpha opportunity - new entrant with momentum
          # ... up to 4 more

        key_levels: []                      # Future feature
        event_risk: []                      # Future feature
        updatedAt: '2025-10-24T00:19:20Z'

      # Macro Trending Section
      macro_trending:
        top_tickers:                        # 10 items
          - ticker: TSLA
            mentions: 10
            velocity: NEW
            signal: RISING
          # ... 9 more tickers

        emerging_tickers:                   # 0-5 items
          - ticker: TSLA
            mentions: 10
            signal: Alpha opportunity - new entrant with momentum
          # ... up to 4 more

        key_levels: []
        event_risk: []
        updatedAt: '2025-10-24T00:19:20Z'

      # Additional Data (future features)
      top_narratives: []
      market_structure: {}
      market_psychology: {}
```

---

## Maintenance

### Regular Checks:
1. **Weekly**: Verify summary file format hasn't changed
2. **Monthly**: Review emerging ticker thresholds (adjust if needed)
3. **After Schema Changes**: Test regex patterns still match

### Known Issues:
- **Empty narratives**: Top Narratives extraction not yet implemented (returns [])
- **Key levels**: Crowdsourced price level extraction not implemented (returns [])
- **Event risk**: High-velocity event detection not implemented (returns [])

### Future Enhancements:
1. Extract top narratives from summary files
2. Parse key price levels from posts
3. Detect high-velocity events (VIX spikes, earnings, etc.)
4. Add historical sentiment tracking (30-day chart)
5. Sentiment correlation with price action

---

## Related Documentation

- **Phase 3.7**: `PROCESS_TRENDING_WORDS_WORKFLOW.md` (generates trending_words.json)
- **Grid Layout Fix**: `toolbox/ACTUAL_FIX_GRID_LAYOUT.md`
- **Regex Fix**: `toolbox/FIXED_CRYPTO_TICKERS_AND_AI_NARRATIVE.md`
- **Master Workflow**: `scripts/automation/run_workflow.py`

---

## Summary

**Phase**: 3.75
**Dependencies**: Phase 3.7 (Process Trending Words)
**Input**: X summaries (2 files) + trending_words.json (1 file)
**Output**: Updated xsentiment tab in master-plan.md
**Key Features**: 10+10 trending tickers, emerging alpha opportunities, AI narrative briefing
**Recent Fixes**: Regex patterns + 10-ticker limit + visual symmetry
**Status**: ✅ Production-ready, fully automated
