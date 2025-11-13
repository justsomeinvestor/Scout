# AI Shell Execution Instructions

## IMPORTANT: How to Run Python Scripts

**Problem:** Some AI interfaces use Node.js-based shell wrappers (like `@lydell/node-pty`) which may have missing binaries on Windows systems. This causes errors when trying to run Python commands.

**Solution:** Use one of these methods instead:

---

## Method 1: Direct PowerShell Command (RECOMMENDED)

When you need to run Python scripts, use PowerShell commands directly:

```powershell
# Run scrapers
python scripts\run_all_scrapers.py

# Run specific scripts
python scripts\archive_x_daily.py 2025-10-16

# Run options fetch
python scripts\fetch_options_data.py 2025-10-16 SPY
```

**In your AI interface:** Request execution as a "PowerShell command" or "CMD command", NOT as a generic "shell command".

---

## Method 2: Use PowerShell Wrapper Script

We've created a PowerShell wrapper that handles the execution properly:

```powershell
powershell -File scripts\run_scrapers.ps1
```

This script:
- Sets the correct working directory
- Runs the Python scraper orchestrator
- Provides clear success/failure messages
- Returns proper exit codes

---

## Method 3: Batch File Alternative

If PowerShell doesn't work, use CMD batch file:

```cmd
@echo off
cd /d C:\Users\Iccanui\Desktop\Investing
python scripts\run_all_scrapers.py
```

Save as `run_scrapers.bat` and execute:
```cmd
scripts\run_scrapers.bat
```

---

## For AI Agents: Execution Checklist

When you encounter shell execution errors:

1. ✅ **Verify Python is accessible:** Test with `python --version`
2. ✅ **Use PowerShell syntax:** Use backslashes `\` not forward slashes `/`
3. ✅ **Specify full paths:** Use `scripts\run_all_scrapers.py` not relative paths
4. ✅ **Avoid Node.js shells:** Request "PowerShell" or "CMD" execution explicitly
5. ✅ **Check working directory:** Ensure you're in `C:\Users\Iccanui\Desktop\Investing`

---

## Common Error Messages and Fixes

### Error: "@lydell/node-pty package... could not find the binary"
**Cause:** AI is using Node.js shell wrapper
**Fix:** Request PowerShell execution instead: `powershell -File scripts\run_scrapers.ps1`

### Error: "python: command not found"
**Cause:** Python not in PATH or wrong shell
**Fix:** Use full path: `C:\Python311\python.exe scripts\run_all_scrapers.py`

### Error: "No such file or directory"
**Cause:** Wrong working directory or wrong path separator
**Fix:** Verify you're in project root and use backslashes

---

## Quick Reference: Commands for Each Step

### Step 0: Run Scrapers
```powershell
# Option A: Direct Python call
python scripts\run_all_scrapers.py

# Option B: PowerShell wrapper (if Option A fails)
powershell -File scripts\run_scrapers.ps1
```

### Manual Steps (if needed)
```powershell
# Run individual scrapers
python Scraper\youtube_scraper.py
python Scraper\rss_scraper.py
python Scraper\x_scraper.py
python Scraper\bookmarks_scraper.py

# Archive X data
python scripts\archive_x_daily.py 2025-10-16

# Fetch options data
python scripts\fetch_options_data.py 2025-10-16 SPY
```

---

## Verification Commands

After scrapers complete, verify success:

```powershell
# Check for today's files (replace YYYY-MM-DD with today's date)
dir /O-D /T:W Research\YouTube\*\2025-10-16*.md | Select-Object -First 10
dir /O-D /T:W Research\RSS\*\2025-10-16*.md | Select-Object -First 10
dir /O-D /T:W Research\X\*\*20251016*.json | Select-Object -First 5

# Check archived X data
dir Research\X\Crypto\*_archived.json | Select-Object -First 5
dir Research\X\Macro\*_archived.json | Select-Object -First 5

# Check options data
dir Research\.cache\*_options_data.json | Select-Object -First 5
```

---

## Notes for User

- The PowerShell wrapper script [scripts/run_scrapers.ps1](../scripts/run_scrapers.ps1) is now available
- Show this file to your research AI before starting the workflow
- If the AI still has issues, run the commands manually in PowerShell terminal
- The Python scripts themselves are fine - it's just a shell execution issue

---

**Last Updated:** 2025-10-16
