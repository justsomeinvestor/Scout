# X Scraper - Quick Reference & Troubleshooting

## Running the Scraper

### Standard Execution
```bash
cd Scraper
python x_scraper.py
```

### Expected Output
```
============================================================
X (TWITTER) LIST SCRAPER
============================================================

Will scrape 3 Twitter/X lists sequentially...

============================================================
[1/3] Scraping X List: Technicals
============================================================

    Loading existing data from x_list_posts_20251019_archived.json (TODAY'S ARCHIVED)
    Found 9 existing posts, 9 unique IDs
    ✓ Using archived file = FAST duplicate detection
Opening Chrome with Scraper_Profile...
    Killing existing Chrome processes...
    Done. Waiting 2 seconds...
    Preparing Scraper_Profile...
    Using existing Scraper_Profile
    Launching Chrome via subprocess...
    Chrome subprocess launched with --remote-debugging-port=9222
    Waiting for debugging port to be ready...
    ✓ Debugging port is ready (attempt 1)
    Connecting Selenium to Chrome...
    ✓ Selenium connected to Chrome
    Verifying connection by navigating to X.com...
    ✓ Connected and navigated successfully
    Opening https://x.com/i/lists/1479448773449314306
    Starting to collect posts...
    [harvesting posts...]
```

---

## One-Time Setup: Manual Authentication

### First Time Only
1. Run authentication setup:
   ```bash
   cd Scraper
   python setup_scraper_profile.py
   ```

2. Wait for Chrome to open with Scraper_Profile
3. Log into X.com manually
4. Close Chrome when done

5. Scraper_Profile will now be saved with authentication and reused for all future scraper runs

---

## Common Errors & Fixes

### ❌ "Chrome failed to start: crashed"

**Cause**: Chrome process not cleaned up from previous run

**Fix**:
```bash
taskkill /F /IM chrome.exe
```
Then re-run the scraper.

---

### ❌ "DevToolsActivePort file doesn't exist"

**Cause**: Profile is locked or Chrome didn't start properly

**Fix**:
1. Kill all Chrome processes:
   ```bash
   taskkill /F /IM chrome.exe
   ```

2. Delete the corrupted Scraper_Profile:
   ```bash
   rmdir "C:\Users\Iccanui\AppData\Local\Google\Chrome\User Data\Scraper_Profile" /s /q
   ```

3. Run scraper again (will auto-recreate profile from Default)

---

### ❌ "Not logged in - showing login page"

**Cause**: Scraper_Profile lost authentication cache

**Fix**:
1. Run setup script again:
   ```bash
   python setup_scraper_profile.py
   ```

2. Log in manually again

3. Close Chrome and retry scraper

---

### ❌ Port 9222 never becomes ready

**Cause**: Chrome subprocess failed to launch

**Fix**:
1. Check if Default profile exists:
   ```bash
   dir "C:\Users\Iccanui\AppData\Local\Google\Chrome\User Data\Default"
   ```

2. Check Chrome installation:
   ```bash
   dir "C:\Program Files\Google\Chrome\Application\chrome.exe"
   ```

3. If issue persists, delete Scraper_Profile and recreate it

---

## Advanced: Running Multiple Scrapers in Parallel

### From Orchestrator
```bash
cd scripts/automation
python run_all_scrapers.py
```

This will:
1. Run X scraper FIRST (highest priority)
2. Run X Bookmarks scraper
3. Run other data scrapers in parallel
4. Archive results

---

## File Locations

| File | Location |
|------|----------|
| X Scraper | Scraper/x_scraper.py |
| Bookmarks Scraper | Scraper/bookmarks_scraper.py |
| Output (Technicals) | Research/X/Technicals/x_list_posts_*.json |
| Output (Crypto) | Research/X/Crypto/x_list_posts_*.json |
| Output (Macro) | Research/X/Macro/x_list_posts_*.json |
| Chrome Profile | C:\Users\Iccanui\AppData\Local\Google\Chrome\User Data\Scraper_Profile |

---

## Useful Commands

### Monitor Running Process
```bash
# See if x_scraper.py is running
tasklist | findstr python

# See if Chrome is running
tasklist | findstr chrome
```

### Check Port Status
```bash
# Check if port 9222 is listening
netstat -ano | findstr 9222
```

### View Latest Output
```bash
# Show most recent saved posts
type "Research\X\Technicals\x_list_posts_*.json" | more
```

---

## Configuration

**Edit**: [Scraper/x_scraper.py](../../../Scraper/x_scraper.py) lines 34-50

```python
X_SCROLL_INTERVAL = 0.5      # Seconds between scrolls (lower = faster but more load)
X_MAX_POSTS = 0              # 0 = unlimited, or set number
X_MAX_DURATION = 86400       # Max seconds to run (24 hours = safety limit)
X_CUTOFF_MODE = "last_24h"   # "since_last" or "last_24h" or None
X_MAX_NO_NEW = 30            # Stop after N scrolls with no new posts
```

---

## Performance Tips

- **Fastest**: Use `X_CUTOFF_MODE = "last_24h"` with `X_MAX_NO_NEW = 10`
- **Most Complete**: Use `X_CUTOFF_MODE = None` with `X_MAX_NO_NEW = 30`
- **Parallel**: Run X scraper FIRST, then other scrapers in parallel

---

## Support Contact

For detailed technical information, see:
- [X_SCRAPER_CHROME_SELENIUM_FIX.md](./X_SCRAPER_CHROME_SELENIUM_FIX.md)

---

**Last Updated**: 2025-10-19
**Status**: ✓ WORKING
