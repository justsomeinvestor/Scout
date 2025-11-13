# Troubleshooting: Browser Hangs During Scraping

## Problem: Scraping Stops Mid-Run (Like Macro Getting Stuck)

**Symptoms**:
- Browser opens and starts scraping (Technicals ✓, Crypto ✓)
- During Macro (or another list), scrolling stops
- No error message in console
- Browser window still visible but frozen
- Posts stop being collected

---

## Root Causes

### 1. X.com Changed Page Structure
**Frequency**: Medium
**How to detect**: Browser is open but "articles" CSS selector finds 0 items
**Fix**: X.com updates their HTML structure - need to update CSS selector in harvest_once()

### 2. Rate Limiting / Bot Detection
**Frequency**: High (especially on larger lists like Macro with 200+ new posts)
**How to detect**: Browser loads page fine initially, then Macro fails mid-scroll
**Solution**: X.com throttles requests after many rapid scrolls
**Fix**: Add delays between scrolls

### 3. JavaScript Not Executing / Page Stuck
**Frequency**: Medium
**How to detect**: Page scroll position doesn't change, page height doesn't increase
**Fix**: Force JavaScript execution or page reload

### 4. Memory/Process Issue
**Frequency**: Low
**How to detect**: Chrome process visible in task manager but uses high RAM/CPU
**Fix**: Kill all Chrome processes and restart

### 5. Selenium Connection Lost
**Frequency**: Low
**How to detect**: Port 9222 still listening but driver commands fail
**Fix**: Reconnect or restart Chrome subprocess

---

## Immediate Fixes (When It Hangs)

### Option 1: Kill and Restart (Quickest)

```bash
# Kill all Chrome processes
taskkill /F /IM chrome.exe

# Delete corrupted profile
rmdir "C:\Users\Iccanui\AppData\Local\Google\Chrome\User Data\Scraper_Profile" /s /q

# Re-run scraper (will recreate profile from Default)
cd Scraper
python x_scraper.py
```

**Time**: ~30 seconds
**Data**: Loses current session, but saves what completed before hang

---

### Option 2: Increase Scroll Delays

**Edit**: [Scraper/x_scraper.py](../../../Scraper/x_scraper.py) Line 41

```python
# Before
X_SCROLL_INTERVAL = 0.5  # seconds between scrolls

# After (slower = less likely to trigger rate limiting)
X_SCROLL_INTERVAL = 2.0  # seconds between scrolls
```

This increases delay between scrolls, giving X.com time to:
- Load more content
- Verify requests aren't bot-like
- Stabilize page rendering

**Impact**: Takes ~4x longer but more reliable

---

### Option 3: Add Wait/Retry Logic

**Edit**: [Scraper/x_scraper.py](../../../Scraper/x_scraper.py) around line 480

```python
def wait_for_more_content(self):
    """Scroll and wait until the page height increases (new content loaded)."""
    import time

    try:
        prev_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_amount = max(600, self.driver.execute_script("return window.innerHeight") - 100)

        # Retry logic if page doesn't load
        max_retries = 3
        for attempt in range(max_retries):
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(self.scroll_interval)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height > prev_height:
                break  # Content loaded, exit retry loop
            else:
                print(f"    ⚠ Scroll attempt {attempt + 1}/{max_retries}: No new content loaded")
                if attempt == max_retries - 1:
                    print(f"    ! Stopping - page not responding")
                    break
                time.sleep(2)  # Extra wait before retry
    except Exception as e:
        print(f"    ⚠ Wait error: {e}")
        time.sleep(self.scroll_interval)
```

---

## Monitoring Active Session

### Real-Time Logging

Run with output capture to see live progress:

```bash
cd Scraper
python x_scraper.py | Tee-Object -FilePath "session.log" -Append
```

Check progress in real-time:
```bash
# PowerShell: Watch last 20 lines
Get-Content session.log -Wait -Tail 20
```

---

## Detecting What's Wrong

### Check Browser Status While Running

In another terminal (while scraper is running):

```bash
# Is Chrome still running?
tasklist | findstr chrome.exe

# Is port 9222 still listening?
netstat -ano | findstr 9222

# How much memory is Chrome using?
wmic process where name="chrome.exe" get ProcessId,WorkingSetSize
```

### Check Page State in Browser

Open browser DevTools manually (F12) while scraper runs:
1. Open Console tab
2. Type: `document.querySelectorAll('article').length`
3. Check if it returns numbers (should increase as content loads)

---

## Prevention: Configuration for Macro List

Macro list is large (~200+ new posts) so more prone to hangs. **Best settings**:

**Edit**: [Scraper/x_scraper.py](../../../Scraper/x_scraper.py)

```python
# More conservative settings for larger lists
X_SCROLL_INTERVAL = 1.5  # Slower scrolls
X_MAX_NO_NEW = 40  # Stop after 40 scrolls with no new posts (not 30)
X_CUTOFF_MODE = "last_24h"  # Focus on recent posts
X_MAX_DURATION = 1200  # 20 minute limit (not 24 hours)
```

This configuration:
- ✓ Gives page time to load
- ✓ Stops earlier (before rate limiting gets aggressive)
- ✓ Still gets ~200+ posts per run
- ✓ Completes in ~10-15 minutes

---

## Specific Fix: X.com Page Structure Changed

If browser opens but finds 0 posts:

**In harvest_once() method**, update CSS selector:

```python
# Current (may be outdated)
articles = self.driver.find_elements(By.CSS_SELECTOR, 'article[role="article"]')

# Try alternatives if above returns 0:
articles = self.driver.find_elements(By.XPATH, "//article")
articles = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="tweet"]')
articles = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="article"]')
```

**Quick diagnostic**:
1. Open X.com/i/lists/... in regular Chrome browser
2. Press F12 (DevTools)
3. Go to Console
4. Paste: `document.querySelectorAll('article').length`
5. Check what that returns

If returns 0, X.com changed their HTML structure - need to update CSS selector.

---

## Systematic Debugging Session

Create **[Scraper/test_macro_debug.py](../../../Scraper/test_macro_debug.py)**:

```python
#!/usr/bin/env python3
"""Test Macro list with detailed debugging"""

import time
from pathlib import Path
from x_scraper import TwitterListScraper

# Test just Macro list with verbose output
scraper = TwitterListScraper(
    profile_path=r"C:\Users\Iccanui\AppData\Local\Google\Chrome\User Data",
    list_url="https://x.com/i/lists/1366729121678589959",
    list_name="Macro",
    scroll_interval=2.0  # Slower for debugging
)

print("1. Setting up driver...")
scraper.setup_driver()

print("2. Opening list URL...")
scraper.driver.get(scraper.list_url)
time.sleep(3)

print("3. Checking page state...")
page_height = scraper.driver.execute_script("return document.body.scrollHeight")
article_count = len(scraper.driver.find_elements(By.CSS_SELECTOR, 'article[role="article"]'))
print(f"   - Page height: {page_height}px")
print(f"   - Articles found: {article_count}")
print(f"   - Current URL: {scraper.driver.current_url}")

if article_count == 0:
    print("   ! WARNING: No articles found - page structure may have changed!")
    print("   ! Try alternative selectors in DevTools")
else:
    print("   ✓ Articles found - proceeding with scrape")

    print("4. Starting scrape (will stop at 10 scrolls for testing)...")
    for i in range(10):
        added = scraper.harvest_once()
        print(f"   Scroll {i+1}: Found {added} new posts, Total: {len(scraper.posts)}")
        scraper.wait_for_more_content()

        # Check page state every 3 scrolls
        if (i + 1) % 3 == 0:
            height = scraper.driver.execute_script("return document.body.scrollHeight")
            print(f"   [Status] Page height: {height}px, Collected: {scraper.new_posts_count}")

print("5. Done - check results above")
scraper.driver.quit()
```

Run it:
```bash
python Scraper/test_macro_debug.py
```

---

## Understanding the "Hang" Pattern

**Normal progression**:
```
[Technicals] Collecting posts... ✓ Completed (66 new)
[Crypto] Collecting posts... ✓ Completed (252 new)
[Macro] Collecting posts...
   Collected 9 new. Total: 47 posts
   Collected 3 new. Total: 50 posts
   ...
   Collected 6 new. Total: 203 posts
   Skipped 25 existing
   ✓ Hit 50 consecutive existing posts - we've caught up!
✓ Completed (166 new)
```

**If it hangs**:
```
[Macro] Collecting posts...
   Collected 9 new. Total: 47 posts
   ...
   Collected 6 new. Total: 100 posts
   [STOPS HERE - No more output]
   [Browser visible but not scrolling]
```

**When you see this**:
1. Note the last "Collected X new" line
2. Check how many total posts
3. This helps identify if it's after X posts or at specific time

---

## Recovery: Continue from Partial Results

If scraper hangs but partial data saved:

**Files to check**:
```
Research/X/Macro/x_list_posts_*.json  # Partial data is here
```

**To continue**:
1. Rename partial file (backup)
2. Kill Chrome processes
3. Re-run scraper
4. It will detect archived file and continue

---

## Prevention Checklist

Before running Macro scraping:
- [ ] Close all other Chrome windows
- [ ] Check port 9222 is free: `netstat -ano | findstr 9222`
- [ ] Set `X_SCROLL_INTERVAL = 1.5` or higher
- [ ] Set `X_MAX_DURATION = 1200` (20 min limit)
- [ ] Clear browser cache if scraper runs daily

---

## Contact/Escalation

If hang persists after trying above fixes:

**Collect this debug info**:
```bash
# 1. Save current logs
cd Scraper
python debug_scraper_session.py
# Wait for it to hang, then Ctrl+C

# 2. Check what was happening
type scraper_logs/debug_*.log | more

# 3. Check environment
python diagnose_environment.py
```

Then review:
- When exactly did it hang (at which post count)?
- What page height was reached?
- Were there any error messages?
- How much memory was Chrome using?

---

**Last Updated**: 2025-10-19
**Related Docs**:
- LOGGING_AND_DEBUG_SETUP.md - How to capture logs
- QUICK_REFERENCE.md - Common troubleshooting

