# Scout Workflow - Command Reference

Quick copy-paste commands for Scout AI processing workflow.

---

## PHASE 0: OLLAMA PREPROCESSING

### Run Preprocessing Scripts

```bash
# YouTube summarizer (2-3 min)
python Toolbox\scripts\youtube_summarizer_ollama.py

# X post summarizer (3-5 min)
python Toolbox\scripts\x_summarizer_ollama.py
```

### Verify Ollama Server Online

```bash
# Check Ollama server responds
curl http://192.168.10.52:11434/api/version
```

### Verify Preprocessing Complete

```bash
# Check YouTube summaries exist (should see 5-10 files)
ls Research\.cache\*_youtube_summary_*.md

# Check X summaries exist (should see 4 files)
ls Research\.cache\*_x_summary_*.md

# Count files (PowerShell)
(Get-ChildItem Research\.cache\*_youtube_summary_*.md).Count
(Get-ChildItem Research\.cache\*_x_summary_*.md).Count
```

---

## PHASE 1: ANALYSIS WORKFLOW

### Check Data Sources Available

```bash
# Check API server online
curl http://192.168.10.56:3000/api/summary

# Check X data collected today
ls Research\X\*\x_list_posts_*.json

# Check API server provides all endpoints
curl http://192.168.10.56:3000/api/youtube/latest
curl http://192.168.10.56:3000/api/rss/latest
```

### Monitor Prep File Progress

```bash
# View prep file
cat Research\.cache\YYYY-MM-DD_dash-prep.md

# Count completed sections (should reach 6 when done)
grep "Complete ✅" Research\.cache\YYYY-MM-DD_dash-prep.md | measure

# Check last updated timestamp
head -10 Research\.cache\YYYY-MM-DD_dash-prep.md
```

---

## PHASE 2: DASHBOARD UPDATE

### Verify Dashboard Updated

```bash
# Check dash.md last updated timestamp
grep "Last Updated:" scout\dash.md

# Check signal score present
grep "Signal Score:" scout\dash.md

# Check generated date matches today
grep "Generated:" scout\dash.md
```

### Open Dashboard

```bash
# Open in default browser
start scout\dash.html

# Or open markdown file
start scout\dash.md
```

---

## VERIFICATION & TROUBLESHOOTING

### Complete Workflow Verification

```bash
# Full verification checklist (PowerShell)
Write-Host "=== Scout Workflow Verification ===" -ForegroundColor Cyan

# 1. Check Ollama summaries
$youtubeCount = (Get-ChildItem Research\.cache\*_youtube_summary_*.md -ErrorAction SilentlyContinue).Count
$xCount = (Get-ChildItem Research\.cache\*_x_summary_*.md -ErrorAction SilentlyContinue).Count
Write-Host "Ollama summaries: YouTube=$youtubeCount, X=$xCount" -ForegroundColor $(if ($youtubeCount -gt 0 -and $xCount -eq 4) {"Green"} else {"Red"})

# 2. Check prep file complete
$prepFile = Get-ChildItem Research\.cache\*_dash-prep.md -ErrorAction SilentlyContinue | Select-Object -First 1
if ($prepFile) {
    $completedCount = (Select-String "Complete ✅" $prepFile.FullName).Matches.Count
    Write-Host "Prep file sections complete: $completedCount/6" -ForegroundColor $(if ($completedCount -eq 6) {"Green"} else {"Yellow"})
} else {
    Write-Host "Prep file: NOT FOUND" -ForegroundColor Red
}

# 3. Check dashboard updated
if (Test-Path scout\dash.md) {
    $lastUpdated = Select-String "Last Updated:" scout\dash.md | Select-Object -First 1
    Write-Host "Dashboard: $lastUpdated" -ForegroundColor Green
} else {
    Write-Host "Dashboard: NOT FOUND" -ForegroundColor Red
}
```

### Crash Recovery

```bash
# Find prep file for today
ls Research\.cache\*_dash-prep.md

# View which sections are complete
grep "Complete ✅\|Pending" Research\.cache\YYYY-MM-DD_dash-prep.md

# Check section headers with status
Select-String "##.*\(Step 3.*\)" Research\.cache\YYYY-MM-DD_dash-prep.md
```

### Check Scraper Data

```bash
# List today's X post files
ls Research\X\Technicals\x_list_posts_*.json
ls Research\X\Crypto\x_list_posts_*.json
ls Research\X\Macro\x_list_posts_*.json
ls Research\X\Bookmarks\x_list_posts_*.json

# Check file sizes (should be 50-500KB each)
dir Research\X\*\x_list_posts_*.json
```

### Server Health Checks

```bash
# API server health
curl http://192.168.10.56:3000/api/summary

# Ollama server health
curl http://192.168.10.52:11434/api/version

# Check both servers (PowerShell)
Write-Host "=== Server Health Check ===" -ForegroundColor Cyan
try {
    $api = Invoke-WebRequest -Uri "http://192.168.10.56:3000/api/summary" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "API Server: ONLINE" -ForegroundColor Green
} catch {
    Write-Host "API Server: OFFLINE" -ForegroundColor Red
}

try {
    $ollama = Invoke-WebRequest -Uri "http://192.168.10.52:11434/api/version" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "Ollama Server: ONLINE" -ForegroundColor Green
} catch {
    Write-Host "Ollama Server: OFFLINE" -ForegroundColor Red
}
```

---

## FILE PATHS QUICK REFERENCE

### Input Data Sources

```
# X/Twitter posts (JSON)
Research\X\Technicals\x_list_posts_YYYYMMDDHHMMSS.json
Research\X\Crypto\x_list_posts_YYYYMMDDHHMMSS.json
Research\X\Macro\x_list_posts_YYYYMMDDHHMMSS.json
Research\X\Bookmarks\x_list_posts_YYYYMMDDHHMMSS.json

# API server data (query endpoints)
http://192.168.10.56:3000/api/summary
http://192.168.10.56:3000/api/youtube/latest
http://192.168.10.56:3000/api/rss/latest

# Ollama summaries (generated in Phase 0)
Research\.cache\YYYY-MM-DD_youtube_summary_{Channel}.md
Research\.cache\YYYY-MM-DD_x_summary_Technicals.md
Research\.cache\YYYY-MM-DD_x_summary_Crypto.md
Research\.cache\YYYY-MM-DD_x_summary_Macro.md
Research\.cache\YYYY-MM-DD_x_summary_Bookmarks.md

# Technical data cache
Research\.cache\YYYY-MM-DD_technical_data.json
```

### Output Files

```
# Analysis checkpoint file
Research\.cache\YYYY-MM-DD_dash-prep.md

# Final dashboard outputs
scout\dash.md
scout\dash.html
```

### Ollama Scripts

```
# Preprocessing scripts
Toolbox\scripts\youtube_summarizer_ollama.py
Toolbox\scripts\x_summarizer_ollama.py
```

---

## TIMING REFERENCE

| Phase | Duration | Details |
|-------|----------|---------|
| **Phase 0:** Ollama Preprocessing | 5-8 min | YouTube (2-3 min) + X posts (3-5 min) |
| **Phase 1:** Build Prep File | 27-37 min | Steps 3A-3F progressive analysis |
| - Step 3A: RSS | 8-10 min | Analyze news articles, themes, sentiment |
| - Step 3B: YouTube | 8-10 min | Read summaries, extract consensus |
| - Step 3C: Technical | 5-8 min | Market levels, breadth, volatility |
| - Step 3D: X/Twitter | 3-5 min | Read summaries, sentiment by category |
| - Step 3E: Synthesis | 3-5 min | Cross-source patterns, confidence |
| - Step 3F: Signal Calc | 3-5 min | Component scoring, weighted total |
| **Phase 2:** Update Dashboard | 10-15 min | Generate scout/dash.md from prep file |
| **TOTAL** | **42-60 min** | Complete end-to-end workflow |

---

## COMMON PATTERNS

### Daily Workflow Execution

```bash
# 1. Scraper completes (already done before you start)
# python scout\scout.py

# 2. Run Ollama preprocessing (5-8 min)
python Toolbox\scripts\youtube_summarizer_ollama.py
python Toolbox\scripts\x_summarizer_ollama.py

# 3. Verify preprocessing complete
ls Research\.cache\*_youtube_summary_*.md
ls Research\.cache\*_x_summary_*.md

# 4. Claude AI processes data (27-37 min)
# - Creates prep file skeleton
# - Executes Steps 3A-3F
# - Marks each complete with ✅

# 5. Claude updates dashboard (10-15 min)
# - Reads complete prep file
# - Updates scout/dash.md

# 6. Verify completion
grep "Last Updated:" scout\dash.md
start scout\dash.html
```

### Resume After Crash

```bash
# 1. Find prep file
ls Research\.cache\*_dash-prep.md

# 2. Check progress
grep "Complete ✅" Research\.cache\YYYY-MM-DD_dash-prep.md

# 3. Identify next step
# Count: 0 complete → Start at 3A
# Count: 1 complete → Continue at 3B
# Count: 2 complete → Continue at 3C
# Count: 3 complete → Continue at 3D
# Count: 4 complete → Continue at 3E
# Count: 5 complete → Continue at 3F
# Count: 6 complete → Proceed to dashboard update (3G)

# 4. Resume workflow from that step
```

---

**Last Updated:** 2025-11-14
**Related Docs:** [SCOUT_AI_WORKFLOW.md](SCOUT_AI_WORKFLOW.md)
