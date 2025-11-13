# STEP 3: PROCESS DATA - Create Analysis & Update Dashboard

**Date:** 2025-11-12 (Updated with X Ollama integration)
**Purpose:** Read scraped data, synthesize analysis, update scout/dash.md
**Duration:** ~35-50 minutes total (5-8 min Ollama preprocessing + 30-40 min Claude analysis)

---

## OVERVIEW

Step 3 has three phases:
1. **Phase 0 (Ollama Preprocessing):** Preprocess YouTube transcripts + X posts (5-8 min) **⚠️ RUN FIRST**
2. **Phase 1 (Steps 3A-F):** Build consolidated prep file (27-37 min - reduced thanks to Ollama)
3. **Phase 2 (Steps 3G-H):** Update scout/dash.md and dashboard.json (10-15 min)

**Key Innovation:** Single checkpoint file instead of multiple intermediate files.

---

## CONSOLIDATED PREP FILE

**Location:** `Research/.cache/YYYY-MM-DD_dash-prep.md`

**Purpose:**
- Single source of truth for all analysis
- Crash-resistant checkpointing (resume from any section)
- Token-efficient (read one file instead of 4+)
- Preserves data fidelity (all analysis in one place)
- Progressive build (fill in sections as completed)

**⚠️ CRITICAL FILE CREATION PROTOCOL:**

**STEP 1: Create Complete Skeleton FIRST**
Before starting any analysis, create the full file structure with ALL section headers (3A-F) marked as "Pending":

```markdown
# Dash Prep - November 1, 2025

**Status:** In Progress
**Created:** 2025-11-01 09:00 UTC
**Last Updated:** 2025-11-01 09:00 UTC

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

**STEP 2: Fill Sections Progressively**
As you complete each analysis step:
1. Read the prep file
2. Replace "[To be completed]" with actual analysis content
3. Change "Pending" to "Complete ✅" in the section header
4. Update "Last Updated" timestamp at top
5. Write the updated file back

**Example After Step 3A:**
```markdown
## 📰 RSS Analysis (Step 3A - Complete ✅)
[Actual RSS analysis with themes, sentiment, takeaways]

## 📺 YouTube Analysis (Step 3B - Pending)
[To be completed]
```

**Final Structure (All Complete):**
```markdown
## 📰 RSS Analysis (Step 3A - Complete ✅)
[Completed analysis]

## 📺 YouTube Analysis (Step 3B - Complete ✅)
[Completed analysis]

## 📊 Technical Analysis (Step 3C - Complete ✅)
[Completed analysis]

## 🐦 X/Twitter Analysis (Step 3D - Complete ✅)
[Completed analysis]

## 🔗 Cross-Source Synthesis (Step 3E - Complete ✅)
[Completed analysis]

## 📈 Signal Calculation (Step 3F - Complete ✅)
[Completed analysis]
```

---

## PHASE 0: OLLAMA PREPROCESSING (~5-8 min) **⚠️ RUN THIS FIRST**

**Purpose:** Preprocess large data files (YouTube transcripts + X posts) so Claude can analyze them efficiently

**IMPORTANT:**
- YouTube transcripts: 80k+ characters each
- X posts: 900+ posts = ~500k tokens
- Claude cannot reliably process this much data. Ollama (local LLM) must preprocess FIRST.

**Commands (run BOTH):**
```bash
# 1. YouTube Summarizer (~2-3 min)
start cmd /k "cd c:\Users\Iccanui\Desktop\Investing-fail && python Toolbox\scripts\youtube_summarizer_ollama.py"

# 2. X Post Summarizer (~3-5 min)
start cmd /k "cd c:\Users\Iccanui\Desktop\Investing-fail && python Toolbox\scripts\x_summarizer_ollama.py"
```

**Claude Behavior:**
1. **Kick off BOTH scripts** using Bash tool (opens NEW terminal windows for monitoring)
2. **Inform user:** "Ollama preprocessing started for YouTube and X posts. This will take 5-8 minutes total. Let me know when both complete."
3. **Go into standby** - DO NOT spin wheels or waste tokens waiting
4. **Wait for user confirmation** that both processes are complete before proceeding to Step 3A

**What it does:**

**YouTube Summarizer:**
1. Finds all YouTube transcripts from today
2. For each transcript (80k+ chars):
   - Reads FULL file (no limits)
   - Sends to Ollama with summarization prompt
   - Saves summary (~2k chars) to `Research/.cache/YYYY-MM-DD_youtube_summary_{channel}.md`
3. Reports success/failure

**X Post Summarizer:**
1. Finds latest X post files for each category (Technicals, Crypto, Macro, Bookmarks)
2. For each category (~100-500 posts):
   - Loads all posts from JSON
   - Selects top 100 by engagement (likes + retweets)
   - Sends to Ollama with investment-focused analysis prompt
   - Saves summary (~3-5k chars) to `Research/.cache/YYYY-MM-DD_x_summary_{category}.md`
3. Reports total posts analyzed (typically ~900 posts across 4 categories)

**Expected output (YouTube):**
```
======================================================================
YouTube Transcript Summarizer (Ollama)
======================================================================
Date: 2025-11-01
Ollama: http://192.168.10.52:11434/api/generate
Model: gpt-oss:20b
======================================================================

[OK] Found 4 transcripts to process:
   - Meet Kevin: 2025-11-01_WdTJjOO6cY4_The Las Vegas Economy...
   - Unchained: 2025-11-01_aFXQbfiJt5o_How the Competition...

[VIDEO] Processing: Meet Kevin...
   Transcript length: 27,009 characters
   Sending to Ollama...
   [OK] Summary generated (2483 characters)
   [SAVED] 2025-11-01_youtube_summary_Meet Kevin.md

SUMMARY
======================================================================
Total transcripts: 4
Successfully processed: 4
Failed: 0
======================================================================
```

**Expected output (X Posts):**
```
======================================================================
X/Twitter Post Summarizer (Ollama)
======================================================================
Date: 2025-11-12
Ollama: http://192.168.10.52:11434/api/generate
Model: gpt-oss:20b
======================================================================

[OK] Found 4 categories to process:
   - Technicals: x_list_posts_20251111182054.json
   - Crypto: x_list_posts_20251111182326.json

[CATEGORY] Processing: Technicals
   Total posts: 226
   Posts in prompt: 100 (top by engagement)
   Sending to Ollama...
   [OK] Summary generated (4234 characters)
   [SAVED] 2025-11-12_x_summary_Technicals.md

SUMMARY
======================================================================
Total categories: 4
Successfully processed: 4
Total posts analyzed: 900
======================================================================
```

**Verification:**
```bash
# Check YouTube summaries exist
ls Research/.cache/2025-11-01_youtube_summary_*.md

# Should see files like:
# 2025-11-01_youtube_summary_Meet Kevin.md
# 2025-11-01_youtube_summary_Unchained.md

# Check X summaries exist
ls Research/.cache/2025-11-12_x_summary_*.md

# Should see files like:
# 2025-11-12_x_summary_Technicals.md
# 2025-11-12_x_summary_Crypto.md
# 2025-11-12_x_summary_Macro.md
# 2025-11-12_x_summary_Bookmarks.md
```

**Token Savings:**
- **YouTube:** 97.5% reduction (80k chars → 2k chars per video)
- **X Posts:** 97.8% reduction (900 posts/93k tokens → 4 summaries/2k tokens)
- **Coverage:** 100% of content analyzed by Ollama

**Documentation:** [06_OLLAMA_INTEGRATION.md](06_OLLAMA_INTEGRATION.md)

**Time:** 5-8 minutes total (2-3 min YouTube + 3-5 min X posts)

---

## STEP 3A: RSS ANALYSIS (~8-10 min)

**Input Files:**
```bash
Research/RSS/CNBC/YYYY-MM-DD_*.md
Research/RSS/MarketWatch/YYYY-MM-DD_*.md
Research/RSS/FederalReserve/YYYY-MM-DD_*.md
```

**Process:**
1. **FIRST:** Create prep file skeleton with ALL sections (3A-F) marked "Pending" (see File Creation Protocol above)
2. Read all RSS articles from today
3. Identify top market drivers (5-7 themes)
4. Assess sentiment (Bullish/Bearish/Neutral %)
5. Rate market impact (HIGH/MEDIUM/LOW)
6. Note key catalysts and risks
7. **Update prep file:** Replace Step 3A "[To be completed]" with analysis, change to "Complete ✅"

**Output to Prep File:**
```markdown
## 📰 RSS Analysis (Step 3A - Complete ✅)

**Articles Analyzed:** 19 articles (CNBC: 13, MarketWatch: 6)
**Overall Sentiment:** Bullish 40%, Bearish 35%, Neutral 25%

**Top Market Drivers:**
1. **Theme Name** - Impact: HIGH
   - Key points
   - Market implications

2. **Theme Name** - Impact: MEDIUM
   - Key points
   - Market implications

[Continue for 5-7 themes]

**Key Takeaways:**
- Consensus view: [what most sources agree on]
- Divergence: [where sources disagree]
- Notable catalysts: [upcoming events mentioned]
```

**Time:** 8-10 minutes

---

## STEP 3B: YOUTUBE ANALYSIS (~8-10 min)

**Prerequisites:** Phase 0 Ollama preprocessing MUST be complete

**⚡ READS OLLAMA SUMMARIES** - See [06_OLLAMA_INTEGRATION.md](06_OLLAMA_INTEGRATION.md)

**Input Files:**
```bash
Research/.cache/YYYY-MM-DD_youtube_summary_{Channel}.md  # Ollama summaries (NOT raw transcripts)
```

**IMPORTANT:**
- YouTube transcripts are 80k+ characters - too large for Claude
- Phase 0 creates readable 2k-char summaries using Ollama
- Claude reads ONLY the summaries (never the raw transcripts)

**Process:**
1. Read Ollama's summaries from `Research/.cache/YYYY-MM-DD_youtube_summary_*.md`
2. Extract consensus analyst views by channel
3. Identify consensus themes across channels
4. Note diverging opinions
5. Extract specific levels/targets mentioned

**Output to Prep File:**
```markdown
## 📺 YouTube Analysis (Step 3B - Complete ✅)

**Channels Analyzed:** 8 channels

**Channel Summaries:**
- **Channel Name:** [Key message, bias, notable calls]
- **Channel Name:** [Key message, bias, notable calls]

**Consensus Themes:**
1. [What multiple channels agree on]
2. [What multiple channels agree on]

**Diverging Views:**
- **Bullish:** [Who's bullish and why]
- **Bearish:** [Who's bearish and why]

**Specific Levels Mentioned:**
- SPX: [Support/resistance levels cited]
- BTC: [Support/resistance levels cited]

**Key Takeaways:**
[2-3 sentence synthesis]
```

**Time:** 8-10 minutes

---

## STEP 3C: TECHNICAL ANALYSIS (~5-8 min)

**Input File:**
```bash
Research/.cache/YYYY-MM-DD_technical_data.json
```

**Process:**
1. Read technical_data.json
2. Extract key levels (SPX, BTC, QQQ)
3. Assess breadth (A/D ratio, up-volume %)
4. Check volatility (VIX, BTC IV)
5. Review options data (max pain, P/C ratios)

**Output to Prep File:**
```markdown
## 📊 Technical Analysis (Step 3C - Complete ✅)

**Data Source:** technical_data.json

**Major Indices:**
- **SPX:** Current [price], Support [levels], Resistance [levels]
- **QQQ:** Current [price], Support [levels], Resistance [levels]
- **BTC:** Current [price], Support [levels], Resistance [levels]

**Market Breadth:**
- NYSE A/D: [ratio]
- Nasdaq A/D: [ratio]
- Up-volume %: [percentage]
- Assessment: [Strong/Weak/Neutral]

**Volatility:**
- VIX: [level] ([change])
- BTC IV: [percentage]
- Assessment: [Elevated/Normal/Low]

**Options Data:**
- SPY Max Pain: [price]
- QQQ Max Pain: [price]
- Put/Call Ratio: [ratio]

**Technical Score:** [0-100] based on trend + breadth + volatility
```

**Time:** 5-8 minutes

---

## STEP 3D: X/TWITTER ANALYSIS (~3-5 min)

**Prerequisites:** Phase 0 Ollama preprocessing complete (X summarizer)

**Input Files:**
```bash
Research/.cache/YYYY-MM-DD_x_summary_Technicals.md
Research/.cache/YYYY-MM-DD_x_summary_Crypto.md
Research/.cache/YYYY-MM-DD_x_summary_Macro.md
Research/.cache/YYYY-MM-DD_x_summary_Bookmarks.md
```

**Process:**
1. Read Ollama-generated X summaries (NOT raw JSON)
2. Extract sentiment by category from summaries
3. Identify trending tickers across categories
4. Note key themes and narratives
5. Synthesize cross-category insights

**Output to Prep File:**
```markdown
## 🐦 X/Twitter Analysis (Step 3D - Complete ✅)

**Posts Analyzed:** [count] posts across 3 categories + bookmarks

**Sentiment by Category:**
- **Crypto:** Bullish [%], Bearish [%], Neutral [%]
- **Macro:** Bullish [%], Bearish [%], Neutral [%]
- **Technicals:** Bullish [%], Bearish [%], Neutral [%]

**Trending Tickers:**
1. [Ticker] - [sentiment] - [why trending]
2. [Ticker] - [sentiment] - [why trending]

**Key Narratives:**
- [Theme 1]: [description]
- [Theme 2]: [description]

**Notable from Bookmarks:**
- [Key saved post and why it matters]

**Overall X Sentiment:** [Bullish/Bearish/Mixed]
```

**Time:** 3-5 minutes (thanks to Ollama preprocessing)

---

## STEP 3E: CROSS-SOURCE SYNTHESIS (~3-5 min)

**Input:** Previous 4 sections of prep file

**Process:**
1. Read all 4 completed sections
2. Identify where sources AGREE (high-confidence themes)
3. Identify where sources DIVERGE (uncertainty)
4. Find patterns across data sources
5. Note what's unique to each source

**Output to Prep File:**
```markdown
## 🔗 Cross-Source Synthesis (Step 3E - Complete ✅)

**High-Confidence Themes (Cross-Source Agreement):**
1. [Theme] - Mentioned in: RSS ✓ YouTube ✓ X ✓ Technicals ✓
2. [Theme] - Mentioned in: RSS ✓ YouTube ✓ X ✓

**Divergences (Uncertainty Areas):**
- RSS says: [view]
- YouTube says: [different view]
- Resolution: [how to interpret the divergence]

**Source-Specific Insights:**
- **RSS only:** [unique insight not mentioned elsewhere]
- **YouTube only:** [unique insight not mentioned elsewhere]
- **X only:** [unique insight not mentioned elsewhere]
- **Technical only:** [unique insight not mentioned elsewhere]

**Pattern Recognition:**
[What patterns emerge when looking at all sources together?]

**Confidence Assessment:**
- High confidence: [themes with 3+ source agreement]
- Medium confidence: [themes with 2 source agreement]
- Low confidence: [themes with 1 source only]
```

**Time:** 3-5 minutes

---

## STEP 3F: SIGNAL CALCULATION (~3-5 min)

**Input:** All previous sections + technical_data.json

**Process:**
1. Calculate preliminary signal score
2. Break down by components (Trend/Breadth/Volatility/Sentiment/Technical)
3. Provide reasoning for score
4. Assign tier (WEAK/MODERATE/STRONG/EXTREME)
5. Note any manual adjustments

**Output to Prep File:**
```markdown
## 📈 Signal Calculation (Step 3F - Complete ✅)

**PRELIMINARY SIGNAL:** XX / 100
**SIGNAL TIER:** [WEAK / MODERATE / STRONG / EXTREME]

**Component Breakdown:**
| Component | Score | Weight | Contribution | Reasoning |
|-----------|-------|--------|--------------|-----------|
| Trend | XX/100 | 30% | XX pts | [Why this score] |
| Breadth | XX/100 | 25% | XX pts | [Why this score] |
| Volatility | XX/100 | 20% | XX pts | [Why this score] |
| Sentiment | XX/100 | 15% | XX pts | [Why this score] |
| Technical | XX/100 | 10% | XX pts | [Why this score] |
| **TOTAL** | - | 100% | **XX pts** | - |

**Calculation Method:**
```
Signal = (Trend × 0.30) + (Breadth × 0.25) + (Volatility × 0.20) +
         (Sentiment × 0.15) + (Technical × 0.10)
```

**Tier Assignment:**
- 0-30: WEAK (Avoid / Defensive)
- 31-60: MODERATE (Selective / Cautious)
- 61-80: STRONG (Bullish / Add Risk)
- 81-100: EXTREME (Max Risk / Euphoria Warning)

**Current Tier Logic:**
Score of XX falls into [TIER] range, meaning [interpretation]

**Manual Adjustments:** [None / ±X points because...]

**Key Drivers of Score:**
- **Positive factors:** [what's supporting the signal]
- **Negative factors:** [what's dragging down the signal]
- **Wildcard:** [any major uncertainty or catalyst ahead]

**Signal Confidence:** [High / Medium / Low] based on source agreement
```

**Time:** 3-5 minutes

---

## STEP 3G: UPDATE MASTER PLAN (~5-10 min)

**Input:** Complete prep file from Steps 3A-F

**Process:**
1. Read complete `YYYY-MM-DD_dash-prep.md`
2. Update scout/dash.md Section 1: Eagle Eye Macro Overview
3. Update scout/dash.md Section 2: Market Sentiment Alignment
4. Update scout/dash.md Section 3: Current Signal Status
5. Update timestamp at bottom

**Files to Update:**
```bash
scout/dash.md
```

**Sections to Update:**

### Section 1: Eagle Eye Macro Overview
```markdown
## 🎯 EAGLE EYE MACRO OVERVIEW

### 🔴 STATE OF PLAY
- [Pull from prep file: key themes, signal score, major developments]

### 📊 IMMEDIATE IMPLICATIONS
[Update table with current positioning guidance]

### ⚠️ KEY RISKS TO TRACK
[Pull from prep file: top 5 risks identified across sources]

### 📅 WEEKEND TASKS & SUNDAY PREP
[Update with current week's tasks]

### 📌 TACTICAL PLAYBOOK (NEXT 1-2 WEEKS)
[Update scenarios and probability weights]

### ✅ ACTION CHECKLIST
[Update with current action items]
```

### Section 2: Market Sentiment Alignment
```markdown
## 📊 MARKET SENTIMENT ALIGNMENT

### Convictions (Consensus Views)
[Pull from prep file: high-confidence themes]

### Opportunities & Actions (Tactical Execution)
[Pull from prep file: actionable opportunities]

### Risks & Monitoring (Red Flags)
[Pull from prep file: key risks to monitor]
```

### Section 3: Current Signal Status
```markdown
## 📈 CURRENT SIGNAL STATUS

**Signal Score:** [XX] / 100
**Signal Tier:** [TIER]
**Market Stance:** [Risk-On / Risk-Off / Neutral]
**Last Calculated:** [Date]

**Signal Components:**
- Trend: [Score] ([Improving/Deteriorating/Stable])
- Breadth: [Score] ([Strong/Weak/Neutral])
- Volatility: [Level] ([Elevated/Normal/Low])
- Technical: [Assessment]
- Sentiment: [Assessment]
```

### Bottom Timestamp
```markdown
---

*Last Updated: [Date]*
*Next Review: After market close or major catalyst*
*System Version: 4.0 - Simplified Daily Research Workflow*
```

**Time:** 5-10 minutes

---

## STEP 3H: UPDATE DASHBOARD JSON (~5 min)

**Input:** Complete prep file from Steps 3A-F, updated scout/dash.md from Step 3G

**Purpose:** Update the machine-readable JSON data that feeds research-dashboard.html

**Files to Update:**
```bash
scout/dashboard.json (OBSOLETE - removed in Session 6)
```

**Process:**

1. **Extract key data from prep file:**
   - Signal score and tier from Step 3F
   - Sentiment cards content (Equities, Crypto, Liquidity, Macro)
   - Risk items (top 5 from scout/dash.md)
   - Portfolio recommendations from sentiment analysis

2. **Update JSON structure:**
   ```json
   {
     "dashboard": {
       "pageTitle": "Investment Research Dashboard - [Today's Date]",
       "dateBadge": "[Today's Date]",
       "lastUpdated": "[ISO Timestamp]",
       "sentimentCards": [
         {"id": "equities", "label": "Equities", "value": "[From Step 3G analysis]"},
         {"id": "crypto", "label": "Crypto", "value": "[From Step 3G analysis]"},
         {"id": "liquidity", "label": "Liquidity Cycle", "value": "[From Step 3G analysis]"},
         {"id": "macro", "label": "Macro", "value": "[From Step 3G analysis]"}
       ],
       "sentimentHistory": [
         {"date": "[Previous dates]", "score": XX, "label": "[Previous tier]"},
         {"date": "[Today]", "score": XX, "label": "[Today's tier]"}
       ],
       "riskItems": [
         {"risk": "[Risk 1 from scout/dash.md]", "monitor": "[How to track]"},
         {"risk": "[Risk 2]", "monitor": "[How to track]"},
         ...
       ]
     }
   }
   ```

3. **Verification:**
   - Valid JSON syntax (no trailing commas, proper quotes)
   - All dates updated to today
   - Signal score matches scout/dash.md
   - Open `research-dashboard.html` in browser to confirm visual display

**See detailed field mapping:** [07_STEP_3H_DASHBOARD_JSON.md](Docs/07_STEP_3H_DASHBOARD_JSON.md)

**Time:** 5 minutes

---

## CRASH RECOVERY

**If session crashes during Step 3:**

1. **Check prep file status:**
   ```bash
   cat Research/.cache/YYYY-MM-DD_dash-prep.md
   ```

2. **Find last completed section:**
   - Look for section with "Complete ✅"
   - Resume from next section

3. **Resume workflow:**
   - If crashed during 3A-F: Continue building prep file from last checkpoint
   - If crashed during 3G: Prep file is complete, just update scout/dash.md

**No data loss!** All completed analysis is saved in the prep file.

---

## VERIFICATION

**After Step 3 completes:**

- [ ] Prep file exists: `Research/.cache/YYYY-MM-DD_dash-prep.md`
- [ ] All 6 sections complete (3A-F have ✅ markers)
- [ ] scout/dash.md updated with today's date
- [ ] Signal score calculated and matches prep file
- [ ] All 3 dashboard sections updated

**Quick check:**
```bash
# Check prep file exists and is complete
ls Research/.cache/2025-11-01_dash-prep.md

# Verify all sections marked complete
grep "Complete ✅" Research/.cache/2025-11-01_dash-prep.md | wc -l
# Should show: 6

# Check scout/dash.md updated today
grep "Last Updated" scout/dash.md
# Should show: November 1, 2025
```

---

## TOKEN EFFICIENCY

**Old approach (multiple files):**
- 4 category overviews: ~3,000 tokens each = 12,000 tokens
- 2 cached files: ~2,000 tokens each = 4,000 tokens
- **Total reading:** ~16,000 tokens

**New approach (single prep file):**
- 1 consolidated prep file: ~8,000-10,000 tokens
- **Total reading:** ~8,000-10,000 tokens

**Savings:** ~40-50% token reduction while maintaining data fidelity!

---

## TROUBLESHOOTING

### Prep file sections incomplete
**Problem:** Session crashed, some sections missing

**Solution:**
1. Read prep file to see what's complete
2. Resume from first incomplete section
3. Continue workflow

### Can't read X JSON files (too large)
**Problem:** X archived JSON files are >500KB

**Solution:**
- Use `jq` to extract key fields only
- Or read file with higher token limit
- Or sample first 100 posts only

### Signal calculation unclear
**Problem:** Don't know how to score components

**Solution:**
- Trend: Based on moving averages, price action
- Breadth: Based on A/D ratio, up-volume %
- Volatility: Inverse score (high vol = low score)
- Sentiment: Average of RSS/YouTube/X sentiment
- Technical: Support/resistance, indicators

---

## NEXT STEP

After Step 3 completes:
→ **scout/dash.md is updated and ready**
→ **Open research-dashboard.html in browser to view**
→ **Workflow complete!**

---

**Status:** Documented
**Approach:** Consolidated prep file with checkpoints
**Token Efficiency:** 40-50% reduction vs old approach
**Crash Resistant:** Resume from any section
**Last Updated:** 2025-11-01
