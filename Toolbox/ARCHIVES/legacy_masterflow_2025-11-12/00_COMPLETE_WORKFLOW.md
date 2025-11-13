# Complete Research Workflow - Start to Finish

**Date:** 2025-11-01
**Purpose:** Master guide for the complete research workflow (hybrid automation + AI)
**Duration:** ~45-60 minutes total

---

## OVERVIEW

This is the complete 3-step workflow to update the master plan with fresh market data.

**What it does:**
1. **Clean old data files** (Python automation)
2. **Scrape fresh data** from all sources (Python automation)
3. **Process data → Update scout/dash.md** (Claude automation - AI does the work)

**ALL 3 STEPS ARE AUTOMATED.** When you say "run the workflow", Claude executes all steps automatically.

**Output files:**
- `scout/dash.md` - Updated daily market analysis
- `scout/dashboard.json` - OBSOLETE (removed in Session 6)
- `scout/dash.html` - Visual dashboard

---

## HOW THE AUTOMATION WORKS

| Step | Automation Type | What Happens | Duration |
|------|------|----------|----------|
| **Step 1: Cleanup** | Python script | Script deletes old cached files | 30 seconds |
| **Step 2: Scrapers** | Python script | Script scrapes RSS/YouTube/X/Technical data | 10-15 minutes |
| **Step 3: Process Data** | **Claude AI** | **Claude reads all data, synthesizes analysis, updates scout/dash.md** | **35-50 minutes** |

**Step 3 - Claude AI automation:**
- Claude reads all RSS articles and synthesizes market themes
- Claude reads all YouTube transcripts and extracts analyst insights
- Claude reads technical data and calculates scores
- Claude reads X/Twitter posts and assesses sentiment
- Claude performs cross-source synthesis (patterns/divergences)
- Claude calculates weighted signal score with reasoning
- Claude updates scout/dash.md with all findings

**The key difference:** Steps 1-2 use Python scripts. Step 3 uses Claude AI as the automation engine (reading, thinking, synthesizing, writing).

---

## QUICK START

**🚫 CRITICAL: NEVER USE "start cmd /k" IN THIS WORKFLOW**
- "start cmd /k" breaks Claude automation
- Always use: `python "path/to/script.py"` with `run_in_background=true`
- Monitor with BashOutput tool

**For Claude (AI):**

When user says **"run the workflow"** or **"update master plan"**, execute:

1. **STEP 1: Cleanup** (~30 seconds)
   ```bash
   python Toolbox/scripts/cleanup/scout_cleanup.py
   ```

2. **STEP 2: Scrapers** (~10-15 minutes)
   ```bash
   python "scripts/automation/run_all_scrapers.py"
   ```

   **⚠️ WAIT FOR USER CONFIRMATION before proceeding to Step 3!**

3. **STEP 3: Process Data** (~40-60 minutes)
   - **3-PREP: Ollama YouTube preprocessing** (Run FIRST before analysis)
     ```bash
     python "Toolbox/scripts/youtube_summarizer_ollama.py"
     ```
   - 3A: Read RSS → Write analysis to prep file
   - 3B: Read YouTube Ollama summaries → Append to prep file
   - 3C: Read Technical data → Append to prep file
   - 3D: Read X/Twitter → Append to prep file
   - 3E: Cross-source synthesis → Append to prep file
   - 3F: Calculate signal score → Append to prep file
   - 3G: Update scout/dash.md from complete prep file
   - 3H: Update dashboard.json with latest analysis data

**For User (Human):**

Just say: **"run the workflow"** and Claude will execute all steps.

---

## STEP-BY-STEP BREAKDOWN

### STEP 1: CLEAN OLD DATA (~30 seconds)

**Purpose:** Remove outdated cached files while preserving signal history

**Documentation:** [02_STEP_1_CLEANUP.md](02_STEP_1_CLEANUP.md)

**Command:**
```bash
python Toolbox/scripts/cleanup/scout_cleanup.py
```

**What it does:**
- Removes category overviews older than 1 day
- Removes cached files older than 1 day
- **Preserves** signals_*.json for trend tracking
- Shows summary of deletions

**Expected output:**
```
=== Wingman Cleanup - 2025-11-01 ===
Category overviews: 4 deleted
Cached files: 3 deleted
Signal files: 2 preserved
Cleanup complete!
```

**Time:** 30 seconds

---

### STEP 2: RUN SCRAPERS (~10-15 minutes)

**Purpose:** Collect fresh data from all sources

**Documentation:** [03_STEP_2_SCRAPERS.md](03_STEP_2_SCRAPERS.md)

**Command:**
```bash
python "scripts/automation/run_all_scrapers.py"
```

**Important:**
- DO NOT use "start cmd /k" - it breaks Claude automation

**What it does:**
- **Phase 1 (Parallel):** X/Twitter + YouTube + RSS scrapers run simultaneously
- **Phase 2 (Sequential):** X data archival → Options data scraper

**Output files:**
```
Research/RSS/*/YYYY-MM-DD*.md (3+ articles)
Research/YouTube/*/YYYY-MM-DD*.md (8+ transcripts)
Research/X/*/x_list_posts_YYYYMMDD*.json (4 files)
Research/.cache/YYYY-MM-DD_technical_data.json (1 file)
```

**Visible terminal window:** Script automatically opens a new PowerShell window showing progress.

**Verification:**
- All scrapers show "✅ completed successfully"
- No "❌ failed" messages
- Files exist in expected locations

**Time:** 10-15 minutes

---

### STEP 3: PROCESS DATA (~35-50 minutes)

**Purpose:** Analyze scraped data and update scout/dash.md

**Documentation:** [05_STEP_3_PROCESS_DATA.md](05_STEP_3_PROCESS_DATA.md)

**Key Innovation:** Single consolidated prep file with checkpoints for crash resistance.

**Workflow:**

#### Phase 0: Ollama Preprocessing (~2-3 min) **⚠️ RUN THIS FIRST**

**IMPORTANT:** YouTube transcripts are 80k+ characters. Ollama must preprocess them BEFORE Claude can analyze.

**Command:**
```bash
python "Toolbox/scripts/youtube_summarizer_ollama.py"
```

**Claude Behavior:**
1. **Kick off the script** using Bash tool with `run_in_background=true`
2. **Inform user:** "Ollama preprocessing started (ID: xxxxx). This will take 2-3 minutes."
3. **⚠️ WAIT FOR USER CONFIRMATION** - DO NOT proceed until user confirms completion
4. **Proceed to Phase 1** only after user confirmation

**DO NOT use "start cmd /k" - it breaks Claude automation**

**What it does:**
- Reads ALL YouTube transcripts (full 80k+ chars each)
- Summarizes each video using Ollama (local LLM)
- Saves summaries to: `Research/.cache/YYYY-MM-DD_youtube_summary_{channel}.md`
- Creates readable 2k-char summaries for Claude

**Expected output:**
```
[OK] Found 4 transcripts to process
[VIDEO] Processing: Meet Kevin... (27,009 chars)
   [OK] Summary generated (2483 chars)
   [SAVED] 2025-11-01_youtube_summary_Meet Kevin.md
...
Successfully processed: 4
```

**Documentation:** [06_OLLAMA_INTEGRATION.md](06_OLLAMA_INTEGRATION.md)

**Time:** 2-3 minutes

#### Phase 1: Build Prep File (Steps 3A-F) (~30-40 min)

**Output file:** `Research/.cache/YYYY-MM-DD_dash-prep.md`

**3A: RSS Analysis** (~8-10 min)
- Read all RSS articles from today
- Identify top 5-7 market themes
- Assess sentiment and impact
- Write section to prep file with ✅ marker

**3B: YouTube Analysis** (~8-10 min) **⚡ Reads Ollama Summaries**
- **Prerequisites:** Phase 0 Ollama preprocessing MUST be complete
- Read Ollama's summaries from `Research/.cache/YYYY-MM-DD_youtube_summary_*.md`
- Synthesize channel views and consensus
- Identify divergence across analysts
- Append section to prep file with ✅ marker
- See: [06_OLLAMA_INTEGRATION.md](06_OLLAMA_INTEGRATION.md)

**3C: Technical Analysis** (~5-8 min)
- Read technical_data.json
- Extract key levels, breadth, volatility
- Calculate technical score
- Append section to prep file with ✅ marker

**3D: X/Twitter Analysis** (~5-8 min)
- Read X archived JSON files
- Extract sentiment by category
- Identify trending tickers and narratives
- Append section to prep file with ✅ marker

**3E: Cross-Source Synthesis** (~3-5 min)
- Compare all 4 data sources
- Find high-confidence themes (cross-source agreement)
- Note divergences and source-specific insights
- Append section to prep file with ✅ marker

**3F: Signal Calculation** (~3-5 min)
- Calculate weighted signal score (0-100)
- Break down by components (Trend/Breadth/Volatility/Sentiment/Technical)
- Assign tier (WEAK/MODERATE/STRONG/EXTREME)
- Append section to prep file with ✅ marker

**Prep file structure:**
```markdown
# Master Plan Prep - November 1, 2025

Status: Complete
Created: 2025-11-01 09:00 UTC
Last Updated: 2025-11-01 09:45 UTC

---

## 📰 RSS Analysis (Step 3A - Complete ✅)
[Analysis content]

## 📺 YouTube Analysis (Step 3B - Complete ✅)
[Analysis content]

## 📊 Technical Analysis (Step 3C - Complete ✅)
[Analysis content]

## 🐦 X/Twitter Analysis (Step 3D - Complete ✅)
[Analysis content]

## 🔗 Cross-Source Synthesis (Step 3E - Complete ✅)
[Analysis content]

## 📈 Signal Calculation (Step 3F - Complete ✅)
[Analysis content]
```

#### Phase 2: Update Master Plan (Step 3G) (~5-10 min)

**Input:** Complete prep file from Steps 3A-F

**Process:**
1. Read complete `YYYY-MM-DD_dash-prep.md`
2. Update scout/dash.md Section 1: Eagle Eye Macro Overview
3. Update scout/dash.md Section 2: Market Sentiment Alignment
4. Update scout/dash.md Section 3: Current Signal Status
5. Update timestamp at bottom

**Time:** 5-10 minutes

#### Phase 3: Update Dashboard (Step 3H) (~5 min)

**Input:** Complete prep file from Steps 3A-F, scout/dash.md from Step 3G

**Process:**
1. Read complete `YYYY-MM-DD_dash-prep.md`
2. Extract key data: signal score, signal tier, sentiment cards, risk items
3. Update `dashboard.json` with:
   - New date and timestamps
   - Updated sentiment cards (Equities, Crypto, Liquidity, Macro)
   - Add new entry to sentiment history with today's score
   - Replace risk items with today's top 5 risks
   - Update portfolio recommendations from prep file analysis

**Files to Update:**
```bash
scout/dashboard.json (OBSOLETE - removed in Session 6)
```

**See detailed documentation:** [07_STEP_3H_DASHBOARD_JSON.md](Docs/07_STEP_3H_DASHBOARD_JSON.md)

**Time:** 20 minutes (Phase 1: scan + update + verify)

Note: Phases 2-4 documented in Docs/ for future enhancement

**Total Step 3 time:** 50-70 minutes (Phase 1 complete)

---

## CRASH RECOVERY

**If workflow crashes:**

**After Step 1:** Just rerun Step 1 (cleanup is idempotent)

**After Step 2:** Check if data files exist:
```bash
ls Research/RSS/*/2025-11-01*.md
ls Research/YouTube/*/2025-11-01*.md
ls Research/X/*/x_list_posts_20251101*.json
```
If files exist, skip Step 2 and proceed to Step 3.

**During Step 3:**
1. Check prep file: `cat Research/.cache/2025-11-01_dash-prep.md`
2. Find last section with "Complete ✅"
3. Resume from next incomplete section
4. All completed analysis is preserved!

**No data loss!** The checkpoint system ensures you can always resume.

---

## VERIFICATION

**After complete workflow:**

- [ ] Cleanup completed (signal files preserved)
- [ ] All scrapers succeeded (✅ markers in terminal)
- [ ] Data files exist for today's date
- [ ] Prep file exists with all 6 sections marked complete
- [ ] scout/dash.md updated with today's date
- [ ] Signal score calculated and matches prep file
- [ ] dashboard.json updated with today's date and signal data
- [ ] research-dashboard.html displays Nov 1 data when opened

**Quick verification commands:**
```bash
# Check prep file complete
grep "Complete ✅" Research/.cache/2025-11-01_dash-prep.md | wc -l
# Should show: 6

# Check dashboard updated
grep "Last Updated" scout/dash.md
# Should show: November 1, 2025

# Check signal score matches
grep "Signal Score" scout/dash.md
grep "PRELIMINARY SIGNAL" Research/.cache/2025-11-01_dash-prep.md
# Should match
```

---

## TOKEN EFFICIENCY

**Old approach:** Multiple intermediate files (~16,000 tokens to read)
**New approach:** Single consolidated prep file (~8,000-10,000 tokens to read)
**Savings:** 40-50% token reduction while maintaining full data fidelity!

---

## TIMING BREAKDOWN

| Step | Duration | Details |
|------|----------|---------|
| Step 1: Cleanup | 30 sec | Remove old cached files |
| Step 2: Scrapers | 10-15 min | Parallel data collection |
| **Step 3-PREP: Ollama preprocessing** | **2-3 min** | **Preprocess YouTube transcripts (RUN FIRST)** |
| Step 3A-F: Prep file | 30-40 min | Progressive analysis with checkpoints |
| Step 3G: Master plan update | 5-10 min | Update 3 sections from prep file |
| Step 3H: Dashboard update | 5 min | Update dashboard.json for visual display |
| **TOTAL** | **50-75 min** | Complete workflow end-to-end |

---

## DETAILED DOCUMENTATION

Each step has complete documentation:

- [01_SYSTEM_OUTPUTS.md](01_SYSTEM_OUTPUTS.md) - Output files and structure
- [02_STEP_1_CLEANUP.md](02_STEP_1_CLEANUP.md) - Cleanup script usage
- [03_STEP_2_SCRAPERS.md](03_STEP_2_SCRAPERS.md) - Scraper execution
- [04_MASTER_PLAN_CLEANUP_LOG.md](04_MASTER_PLAN_CLEANUP_LOG.md) - Master plan refactor notes
- [05_STEP_3_PROCESS_DATA.md](05_STEP_3_PROCESS_DATA.md) - AI analysis workflow

---

## TROUBLESHOOTING

### Scraper fails
**Solution:** See [03_STEP_2_SCRAPERS.md](03_STEP_2_SCRAPERS.md) troubleshooting section

### Can't find data files
**Check:**
1. Verify scrapers completed successfully
2. Check Research/* folders for today's date
3. Rerun Step 2 if needed

### Session crashes during Step 3
**Solution:**
1. Read prep file to find last completed section
2. Resume from next section (see Step 3 doc)
3. No need to redo completed sections!

### Signal calculation unclear
**Solution:** See [05_STEP_3_PROCESS_DATA.md](05_STEP_3_PROCESS_DATA.md) signal calculation section

---

## WHEN COMPLETE

**Success indicators:**
- ✅ scout/dash.md shows today's date
- ✅ Signal score calculated and documented
- ✅ All 3 dashboard sections updated
- ✅ Prep file exists with 6 complete sections

**Next action:**
→ Open `scout/dash.html` in browser to view updated dashboard!

---

**Status:** Complete Workflow Documentation
**Approach:** First principles rebuild - simplified 3-step process
**Innovation:** Consolidated checkpoint prep file (40-50% token savings)
**Crash Resistant:** Resume from any section
**Last Updated:** 2025-11-01
