# Scout AI Processing Workflow

**Purpose:** Process fresh scraped data through AI analysis to generate market intelligence dashboard
**Duration:** ~40-55 minutes total (5-8 min preprocessing + 27-37 min analysis + 10-15 min dashboard update)
**Starting Point:** Scraper has completed, fresh data ready in Research/ directories

---

## QUICK START

**You are starting here because:**
- ✅ Scraper (`python scout/scout.py`) has completed successfully
- ✅ Fresh data collected from X/Twitter, API server (YouTube/RSS/Market)
- ⏸️ AI processing required (this workflow)

**What you'll do:**
1. **Phase 0:** Run Ollama preprocessing (5-8 min - compress large files)
2. **Phase 1:** Build analysis prep file (27-37 min - Steps 3A-3F)
3. **Phase 2:** Update dashboard (10-15 min - Step 3G)

**Output:** Updated `scout/dash.md` with today's market signal score

---

## PHASE 0: CHECK API SERVER (~30 seconds)

### ⚠️ DATA IS ON THE API SERVER

**Why this changed:**
- Scraper sends data to API server (192.168.10.56:3000)
- API server runs Ollama preprocessing automatically
- Summaries are in the API responses (`"summary"` field)
- Local Ollama scripts are FALLBACK ONLY (rarely needed)

**Quick check (do this first):**

```bash
# Check if API server has preprocessed summaries
curl -s http://192.168.10.56:3000/api/youtube/latest | grep -q '"summary"' && echo "✅ Summaries ready" || echo "❌ Need preprocessing"
```

**Decision tree:**

1. **If you see `"summary":` fields populated in API response:**
   → ✅ **SKIP to Phase 1** - data is ready
   → No need to run local Ollama scripts

2. **If summaries are null or missing (RARE):**
   → Run local scripts as fallback:
   ```bash
   python Toolbox/scripts/youtube_summarizer_ollama.py
   python Toolbox/scripts/x_summarizer_ollama.py
   ```

**99% of the time:** API server already has summaries → proceed directly to Phase 1

**Time:** 30 seconds (just an API check)

**Documentation:** See `Toolbox/06_OLLAMA_INTEGRATION.md` for details

---

## PHASE 1: BUILD PREP FILE (~27-37 min)

### Prep File Overview

**Location:** `Research/.cache/YYYY-MM-DD_dash-prep.md`

**Purpose:**
- Single source of truth for all analysis
- Checkpoint system for crash recovery
- Progressive build (fill sections as completed)
- Token-efficient (read one file instead of 4+)

### Critical Protocol: Create Skeleton FIRST

**Before any analysis, create full file structure:**

```markdown
# Dash Prep - [Date]

**Status:** In Progress
**Created:** [Timestamp]
**Last Updated:** [Timestamp]

---

## 📰 RSS Analysis (Step 3A - Pending)
[To be completed]

## 📺 YouTube Analysis (Step 3B - Pending)
[To be completed]

## 📊 Technical Analysis (Step 3C - Pending)
[To be completed]

## 🐦 X/Twitter Analysis (Step 3D - Pending)
[To be completed]

## 🔗 Cross-Source Synthesis (Step 3E - Pending)
[To be completed]

## 📈 Signal Calculation (Step 3F - Pending)
[To be completed]
```

**Why this matters:** If session crashes, you can resume from last completed section.

---

### STEP 3A: RSS Analysis (~8-10 min)

**Input data:**
- API endpoint: `http://192.168.10.56:3000/api/rss/latest`
- OR local files: `Research/RSS/*/YYYY-MM-DD_*.md`

**Process:**
1. Read all RSS articles from today
2. Identify 5-7 top market themes
3. Assess sentiment (Bullish/Bearish/Neutral %)
4. Rate market impact (HIGH/MEDIUM/LOW)
5. Note key catalysts and risks

**Output to prep file:**
```markdown
## 📰 RSS Analysis (Step 3A - Complete ✅)

**Articles Analyzed:** [count] articles ([sources])
**Overall Sentiment:** Bullish X%, Bearish Y%, Neutral Z%

**Top Market Drivers:**
1. **[Theme Name]** - Impact: HIGH
   - [Key points]
   - [Market implications]

2. **[Theme Name]** - Impact: MEDIUM
   - [Key points]
   - [Market implications]

[... 5-7 themes total ...]

**Key Takeaways:**
- Consensus view: [what most sources agree on]
- Divergence: [where sources disagree]
- Notable catalysts: [upcoming events]
```

**After completion:** Update prep file, change "Pending" to "Complete ✅"

---

### STEP 3B: YouTube Analysis (~8-10 min)

**Prerequisites:** ⚠️ Phase 0 Ollama preprocessing must be complete

**Input files:** Ollama summaries (NOT raw transcripts)
```
Research/.cache/YYYY-MM-DD_youtube_summary_{Channel}.md
```

**Process:**
1. Read Ollama's 2k-char summaries (never read 80k+ char raw transcripts)
2. Extract consensus views by channel
3. Identify themes across multiple channels
4. Note diverging opinions
5. Extract specific price levels/targets mentioned

**Output to prep file:**
```markdown
## 📺 YouTube Analysis (Step 3B - Complete ✅)

**Channels Analyzed:** [count] channels

**Channel Summaries:**
- **[Channel Name]:** [Key message, bias, notable calls]
- **[Channel Name]:** [Key message, bias, notable calls]

**Consensus Themes:**
1. [What multiple channels agree on]
2. [What multiple channels agree on]

**Diverging Views:**
- **Bullish:** [Who and why]
- **Bearish:** [Who and why]

**Specific Levels Mentioned:**
- SPY: [Support/resistance]
- QQQ: [Support/resistance]
- BTC: [Support/resistance]

**Key Takeaways:** [2-3 sentence synthesis]
```

**After completion:** Update prep file, mark "Complete ✅"

---

### STEP 3C: Technical Analysis (~5-8 min)

**Input data:**
- API endpoint: `http://192.168.10.56:3000/api/summary`
- OR cached file: `Research/.cache/YYYY-MM-DD_technical_data.json`

**Process:**
1. Extract key levels (SPY, QQQ, VIX, BTC)
2. Assess market breadth (volume, P/C ratios, A/D ratios)
3. Check volatility (VIX level, IV percentiles)
4. Review options data (max pain, IV rank, P/C ratios)
5. Calculate technical component scores

**Output to prep file:**
```markdown
## 📊 Technical Analysis (Step 3C - Complete ✅)

**Data Source:** [API/Cache file timestamp]

**Major Indices:**
- **SPY:** $[price], IV [%], P/C [ratio], Support/Resistance [levels]
- **QQQ:** $[price], IV [%], P/C [ratio], Max Pain $[price]
- **VIX:** [level] ([% change]) - [Assessment: Elevated/Normal/Low]
- **BTC:** $[price], IV [%], Support/Resistance [levels]

**Market Breadth:**
- Volume trends: [Strong/Weak/Neutral]
- Put/Call ratios: [Bullish/Bearish implications]
- Advance/Decline: [Ratio and assessment]

**Volatility Assessment:**
- VIX: [Level and interpretation]
- IV vs HV: [Premium/discount assessment]
- Volatility regime: [Low/Normal/Elevated]

**Options Data:**
- Max pain analysis: [Current vs max pain, implications]
- IV rank: [Percentile and meaning]
- Open Interest: [Notable positioning]

**Technical Score:** [X/100] based on trend + breadth + volatility
```

**After completion:** Update prep file, mark "Complete ✅"

---

### STEP 3D: X/Twitter Analysis (~3-5 min)

**Prerequisites:** ⚠️ Phase 0 Ollama preprocessing must be complete

**Input files:** Ollama summaries (NOT raw JSON posts)
```
Research/.cache/YYYY-MM-DD_x_summary_Technicals.md
Research/.cache/YYYY-MM-DD_x_summary_Crypto.md
Research/.cache/YYYY-MM-DD_x_summary_Macro.md
Research/.cache/YYYY-MM-DD_x_summary_Bookmarks.md
```

**Process:**
1. Read Ollama-generated category summaries
2. Extract sentiment by category
3. Identify trending tickers across categories
4. Note key themes and narratives
5. Synthesize cross-category insights

**Output to prep file:**
```markdown
## 🐦 X/Twitter Analysis (Step 3D - Complete ✅)

**Posts Analyzed:** [count] posts across 4 categories (via Ollama summaries)

**Sentiment by Category:**
- **Technicals:** Bullish [%], Bearish [%], Neutral [%] - [Key themes]
- **Crypto:** Bullish [%], Bearish [%], Neutral [%] - [Key themes]
- **Macro:** Bullish [%], Bearish [%], Neutral [%] - [Key themes]
- **Bookmarks:** [Notable saved posts]

**Trending Tickers:**
1. [Ticker] - [Sentiment] - [Why trending]
2. [Ticker] - [Sentiment] - [Why trending]

**Key Narratives:**
- [Theme 1]: [Description and market implications]
- [Theme 2]: [Description and market implications]

**Overall X Sentiment:** [Bullish/Bearish/Mixed] - [Brief reasoning]
```

**After completion:** Update prep file, mark "Complete ✅"

---

### STEP 3E: Cross-Source Synthesis (~3-5 min)

**Input:** All 4 completed sections (3A-3D) from prep file

**Process:**
1. Read all completed sections in prep file
2. Identify HIGH-CONFIDENCE themes (3+ sources agree)
3. Identify DIVERGENCES (sources conflict)
4. Find patterns across data sources
5. Assign confidence levels to themes

**Output to prep file:**
```markdown
## 🔗 Cross-Source Synthesis (Step 3E - Complete ✅)

**High-Confidence Themes (Cross-Source Agreement):**
✅ [Theme] - Sources: RSS ✓ YouTube ✓ X ✓ Technical ✓
✅ [Theme] - Sources: RSS ✓ YouTube ✓ X ✓

**Divergences (Uncertainty Areas):**
- RSS says: [View]
- YouTube says: [Different view]
- X says: [Yet another view]
- Resolution: [How to interpret the conflict]

**Source-Specific Insights:**
- **RSS only:** [Unique insight from news]
- **YouTube only:** [Unique analyst perspective]
- **X only:** [Unique sentiment/narrative]
- **Technical only:** [Unique market structure insight]

**Pattern Recognition:**
[What patterns emerge when viewing all sources together?]

**Confidence Levels:**
- High confidence (3+ sources): [List themes]
- Medium confidence (2 sources): [List themes]
- Low confidence (1 source): [List themes]
```

**After completion:** Update prep file, mark "Complete ✅"

---

### STEP 3F: Signal Calculation (~3-5 min)

**Input:** All previous sections + technical data

**Process:**
1. Score each component (0-100 scale):
   - **Trend (30% weight):** SPY/QQQ direction, moving averages
   - **Breadth (25% weight):** P/C ratios, volume, A/D ratio
   - **Volatility (20% weight):** VIX level (inverted - high VIX = low score)
   - **Sentiment (15% weight):** Average of RSS/YouTube/X sentiment
   - **Technical (10% weight):** Support/resistance, indicators

2. Calculate weighted average:
   ```
   Signal = (Trend × 0.30) + (Breadth × 0.25) + (Volatility × 0.20) +
            (Sentiment × 0.15) + (Technical × 0.10)
   ```

3. Assign tier:
   - 0-33: WEAK (Bearish, defensive positioning)
   - 34-66: MODERATE (Mixed signals, balanced approach)
   - 67-83: STRONG (Bullish, controlled risk-on)
   - 84-100: EXTREME (Very bullish, euphoria warning)

**Output to prep file:**
```markdown
## 📈 Signal Calculation (Step 3F - Complete ✅)

**SIGNAL SCORE:** XX.XX / 100
**SIGNAL TIER:** [WEAK/MODERATE/STRONG/EXTREME]

**Component Breakdown:**
| Component | Score | Weight | Contribution | Reasoning |
|-----------|-------|--------|--------------|-----------|
| Trend | XX/100 | 30% | +XX.X pts | [Why this score] |
| Breadth | XX/100 | 25% | +XX.X pts | [Why this score] |
| Volatility | XX/100 | 20% | +XX.X pts | [Why this score] |
| Sentiment | XX/100 | 15% | +XX.X pts | [Why this score] |
| Technical | XX/100 | 10% | +XX.X pts | [Why this score] |
| **TOTAL** | - | 100% | **XX.XX** | - |

**Tier Assignment Logic:**
Score XX.XX falls into [TIER] range (X-Y), indicating [market interpretation]

**Key Drivers:**
- **Positive factors:** [What's supporting the signal]
- **Negative factors:** [What's dragging down the signal]
- **Wildcard:** [Major uncertainty or catalyst ahead]

**Signal Confidence:** [High/Medium/Low] based on cross-source agreement from Step 3E
```

**After completion:** Update prep file, mark "Complete ✅"

---

## PHASE 2: UPDATE DASHBOARD (~10-15 min)

### STEP 3G: Update scout/dash.md

**Input:** Complete prep file from `Research/.cache/YYYY-MM-DD_dash-prep.md`

**Process:**
1. Read complete prep file (single source of truth)
2. Update all sections of `scout/dash.md`:
   - Executive Summary (synthesize top-level narrative)
   - Market Signal Score (component table + tier)
   - Source Analysis Summary (RSS/YouTube/Technical/X breakdowns)
   - Actionable Recommendations (position sizing, risk management)
   - Key Risks & Monitoring Points (top 5-7 risks)
   - Performance Tracking (system metrics)
3. Update timestamps at bottom

**Dashboard structure:**
```markdown
# Scout Market Intelligence Dashboard

**Generated:** YYYY-MM-DD | **Signal:** XX.XX/100 ([TIER]) | **Status:** Production Ready

---

## Executive Summary
[2-3 paragraph synthesis from prep file: market conditions, signal interpretation, recommended strategy]

---

## 🎯 Market Signal Score: XX.XX/100

### Tier: [TIER] ([Upper/Lower Range])
- **Signal Momentum:** [Improving/Stable/Deteriorating]
- **Confidence:** [High/Medium/Low] based on source agreement
- **Risk Level:** [Current risk assessment]

### Component Breakdown:
[Copy table from prep file Step 3F]

---

## 📊 Source Analysis Summary

### 1️⃣ RSS Article Analysis
[Summarize from prep file Step 3A: themes, sentiment, catalysts]

### 2️⃣ YouTube Video Analysis
[Summarize from prep file Step 3B: analyst consensus, divergences, levels]

### 3️⃣ Technical Analysis
[Summarize from prep file Step 3C: market levels, breadth, volatility, options]

### 4️⃣ X/Twitter Sentiment Analysis
[Summarize from prep file Step 3D: category sentiment, trending tickers, narratives]

### 5️⃣ Cross-Source Synthesis
[Summarize from prep file Step 3E: high-confidence themes, divergences, patterns]

---

## 📋 Actionable Recommendations
[Position sizing, entry/exit criteria, risk management based on signal tier]

---

## ⚠️ Key Risks & Monitoring Points
[Top 5-7 risks identified across all sources, with monitoring triggers]

---

*Last Updated: [YYYY-MM-DD HH:MM UTC]*
```

**Verification:**
```bash
# Check dash.md updated today
grep "Last Updated" scout/dash.md

# Check signal score present
grep "Signal Score:" scout/dash.md
```

**Time:** 10-15 minutes

---

## CRASH RECOVERY

**If session crashes during any step:**

1. **Check prep file status:**
   ```bash
   cat Research/.cache/YYYY-MM-DD_dash-prep.md
   ```

2. **Find last completed section:**
   - Look for sections marked "Complete ✅"
   - Identify first section still marked "Pending"

3. **Resume from checkpoint:**
   - Continue from the first incomplete step
   - All previous analysis preserved in prep file
   - No data loss, no need to restart

**Example recovery:**
```markdown
## 📰 RSS Analysis (Step 3A - Complete ✅)
[Analysis present]

## 📺 YouTube Analysis (Step 3B - Complete ✅)
[Analysis present]

## 📊 Technical Analysis (Step 3C - Pending)
[To be completed]  ← RESUME HERE
```

---

## VERIFICATION CHECKLIST

**After complete workflow:**

- [ ] Ollama summaries exist (YouTube + X categories)
- [ ] Prep file exists: `Research/.cache/YYYY-MM-DD_dash-prep.md`
- [ ] All 6 sections marked "Complete ✅"
- [ ] scout/dash.md updated with today's date
- [ ] Signal score calculated (0-100)
- [ ] Signal tier assigned (WEAK/MODERATE/STRONG/EXTREME)
- [ ] Dashboard opens successfully

**Quick verification commands:**
```bash
# Check all prep file sections complete
grep "Complete ✅" Research/.cache/YYYY-MM-DD_dash-prep.md | wc -l
# Should output: 6

# Check dashboard updated
grep "Generated:" scout/dash.md
# Should show: today's date
```

---

## APPENDIX A: DATA SOURCES

### API Server

**Base URL:** `http://192.168.10.56:3000`

**Endpoints:**
- `/api/summary` - Market data (SPY, QQQ, VIX, Max Pain)
- `/api/youtube/latest` - YouTube videos with Ollama summaries
- `/api/rss/latest` - RSS news articles

**Health check:**
```bash
curl http://192.168.10.56:3000/api/summary
```

### Directory Structure

```
Research/
├── X/                              # X/Twitter posts (JSON files)
│   ├── Technicals/
│   ├── Crypto/
│   ├── Macro/
│   └── Bookmarks/
├── .cache/                         # Ollama summaries + prep files
│   ├── YYYY-MM-DD_youtube_summary_*.md
│   ├── YYYY-MM-DD_x_summary_*.md
│   ├── YYYY-MM-DD_dash-prep.md
│   └── YYYY-MM-DD_technical_data.json
└── RSS/                            # RSS articles (local fallback)
    ├── CNBC/
    ├── MarketWatch/
    └── FederalReserve/

scout/
├── dash.md                         # Output: Market intelligence markdown
└── dash.html                       # Output: Interactive dashboard
```

---

## APPENDIX B: TROUBLESHOOTING

### Ollama Server Offline
**Symptom:** Preprocessing scripts fail to connect
**Solution:**
1. Check Ollama server: `curl http://192.168.10.52:11434/api/version`
2. Restart Ollama server if needed
3. Re-run preprocessing scripts

### X Data Missing
**Symptom:** No X summary files generated
**Solution:**
1. Check if X scraper ran: `ls Research/X/*/x_list_posts_YYYYMMDD*.json`
2. If no files: Run scraper `python scout/scout.py`
3. If files exist: Re-run X summarizer

### API Server Offline
**Symptom:** Technical analysis step has no data
**Solution:**
1. Check server: `curl http://192.168.10.56:3000/api/summary`
2. Verify network connectivity to 192.168.10.56
3. Use cached technical_data.json if available
4. If neither available: Skip technical analysis, adjust signal weights

### Session Crashes During Analysis
**Symptom:** Claude conversation interrupted mid-workflow
**Solution:**
1. Open prep file: `cat Research/.cache/YYYY-MM-DD_dash-prep.md`
2. Find last "Complete ✅" section
3. Resume from next incomplete section
4. No data loss - all completed analysis preserved

### Signal Calculation Unclear
**Symptom:** Don't know how to score components
**Solution:**
- **Trend:** 70+ = strong uptrend, 30-70 = choppy, <30 = downtrend
- **Breadth:** Based on A/D ratio and up-volume % (high = strong)
- **Volatility:** Inverse (VIX 30+ = score 20, VIX 10-15 = score 80)
- **Sentiment:** Average RSS/YouTube/X (weight toward consensus)
- **Technical:** Support held = higher score, resistance broken = higher

---

## COMMAND REFERENCE

See [COMMAND_REFERENCE.md](COMMAND_REFERENCE.md) for quick copy-paste commands.

---

**Last Updated:** 2025-11-14
**Status:** Active workflow (assumes scraper completed)
**Previous Version:** Archived to `Toolbox/ARCHIVES/legacy_workflow_2025-11-14/`
