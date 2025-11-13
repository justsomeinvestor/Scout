# Manual Workflow Steps (When AI Has Shell Issues)

## Problem: AI Cannot Execute Commands

If your research AI encounters `@lydell/node-pty` errors and **cannot execute any shell commands** (PowerShell, CMD, or Python), it means the AI is configured to use a Node.js-based shell that has missing binaries.

**You have two options:**

---

## Option 1: Run Commands Manually in PowerShell (RECOMMENDED)

Open PowerShell in the Investing directory and run commands yourself:

### Step 0: Run Scrapers

```powershell
# Navigate to project directory
cd C:\Users\Iccanui\Desktop\Investing

# Option A: Use batch file
.\run_scrapers.bat

# Option B: Direct Python call
python scripts\run_all_scrapers.py

# Option C: Use PowerShell script
powershell -File scripts\run_scrapers.ps1
```

### Verify Scrapers Completed

After scrapers finish, verify the data:

```powershell
# Check YouTube transcripts (replace date)
dir /O-D /T:W Research\YouTube\*\2025-10-16*.md | Select-Object -First 10

# Check RSS articles (replace date)
dir /O-D /T:W Research\RSS\*\2025-10-16*.md | Select-Object -First 10

# Check X data (replace date - use YYYYMMDD format)
dir /O-D /T:W Research\X\*\*20251016*.json | Select-Object -First 5

# Check archived X files
dir Research\X\Crypto\*_archived.json | Select-Object -First 3
dir Research\X\Macro\*_archived.json | Select-Object -First 3

# Check options data
dir Research\.cache\*_options_data.json | Select-Object -First 3
```

### Then Continue with AI

Once scrapers complete, tell your AI:

```
The scrapers have completed successfully. I've verified the data exists.

Please proceed with STEP 1 of the workflow:
- Create individual provider summaries
- Read from Research/YouTube, Research/RSS, Research/X folders
- Today's date is: 2025-10-16

Skip STEP 0 (scrapers) since I ran them manually.
```

---

## Option 2: Configure Your AI to Use Native Shell

Your research AI needs to be configured to use **Windows CMD** or **PowerShell** instead of Node.js shell.

### For Google Gemini / Google AI Studio:

1. Check if there's a shell configuration setting
2. Look for options like "Execution Environment" or "Terminal Type"
3. Change from "Node.js" to "PowerShell" or "CMD"

### For Custom AI Interfaces:

If you built this interface yourself, modify the shell execution code to use:
- `child_process.spawn('powershell.exe', ['-Command', 'python scripts\\run_all_scrapers.py'])`
- Instead of: Node-pty or similar wrappers

### For Third-Party AI Platforms:

Contact the platform support and report:
- The `@lydell/node-pty` package has missing Windows binaries
- Request native PowerShell/CMD support instead

---

## Option 3: Hybrid Approach (Best for Now)

1. **You run STEP 0 manually** (scrapers) in PowerShell
2. **AI handles STEPS 1-3** (reading files and creating summaries)

The AI doesn't need shell access for Steps 1-3 since those are file read/write operations.

### Quick Start:

```powershell
# 1. Run this in PowerShell
cd C:\Users\Iccanui\Desktop\Investing
python scripts\run_all_scrapers.py

# 2. Wait for completion (5-10 minutes)

# 3. Tell your AI:
"Scrapers completed. Please start at STEP 1 and create provider summaries for today's date: 2025-10-16"
```

---

## Step-by-Step Manual Commands (if needed)

If the orchestrator script fails, run scrapers individually:

```powershell
cd C:\Users\Iccanui\Desktop\Investing

# Run each scraper
python Scraper\youtube_scraper.py
python Scraper\rss_scraper.py
python Scraper\x_scraper.py
python Scraper\bookmarks_scraper.py

# Archive X data (replace date)
python scripts\archive_x_daily.py 2025-10-16

# Fetch options data (replace date)
python scripts\fetch_options_data.py 2025-10-16 SPY

# Process X trends (replace date)
python Research\X\Trends\process_trends.py 2025-10-16
```

---

## What Your AI CAN Do (Without Shell Access)

Your AI can still handle these tasks without running commands:

✅ **Read files** - All content reading from Research folders
✅ **Write summaries** - Creating markdown summary files
✅ **Analyze data** - Processing and synthesizing information
✅ **Create reports** - Generating the final market overview

❌ **Cannot do** - Running Python scripts or shell commands

---

## Future Fix: Use a Different AI Interface

Consider using AI interfaces that support native shell execution:
- **VS Code + GitHub Copilot** - Native terminal integration
- **Cursor IDE** - Native shell support
- **Claude Desktop** (if available for your OS) - Native shell
- **Windows Terminal + GitHub Copilot CLI** - Direct PowerShell

---

## Summary: Recommended Workflow

**For now, use the hybrid approach:**

1. Open PowerShell
2. Run: `cd C:\Users\Iccanui\Desktop\Investing`
3. Run: `python scripts\run_all_scrapers.py`
4. Wait for completion (~5-10 minutes)
5. Tell AI: "Scrapers done, proceed with STEP 1 for date 2025-10-16"
6. AI handles all summary creation (Steps 1-3)

This way you get the best of both worlds:
- Manual execution for shell commands
- AI assistance for data processing and summarization

---

**Last Updated:** 2025-10-16
