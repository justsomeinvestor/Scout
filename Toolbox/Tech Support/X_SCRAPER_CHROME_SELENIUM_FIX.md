# X/Twitter Scraper - Chrome & Selenium Integration Fix

## Problem Summary

The X/Twitter scraper (x_scraper.py) was failing to initialize Chrome WebDriver with errors:
- "Chrome failed to start: crashed"
- "DevToolsActivePort file doesn't exist"
- "cannot connect to chrome at 127.0.0.1:9222"

The root cause: **Selenium was trying to launch Chrome directly, which caused profile locking conflicts.**

---

## Solution Overview

Use a **hybrid approach**:
1. **Launch Chrome via subprocess** (bypassing Selenium's launch mechanism)
2. **Enable remote debugging** on port 9222
3. **Connect Selenium** to the already-running Chrome instance using `debuggerAddress` (NOT by launching new Chrome)
4. **Use a separate Scraper_Profile** (not Default) to avoid profile locking issues

---

## Step-by-Step Implementation

### 1. Kill Existing Chrome Processes
```python
subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'],
              capture_output=True, timeout=5)
time.sleep(2)
```

### 2. Prepare Scraper_Profile (Copy from Default if needed)
```python
if not scraper_profile.exists() and default_profile.exists():
    shutil.copytree(default_profile, scraper_profile)
```

This ensures authentication is preserved in the scraped profile.

### 3. Launch Chrome via Subprocess with Remote Debugging
```python
subprocess.Popen([
    chrome_path,
    f'--user-data-dir={scraper_profile}',
    f'--remote-debugging-port=9222'
], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
```

**KEY POINT**: We use `Scraper_Profile` (non-standard directory), NOT `Default`. Chrome 136+ security restrictions require this.

### 4. Wait for Debugging Port to Be Ready
```python
port_ready = False
for attempt in range(15):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(("127.0.0.1", 9222))
        sock.close()
        if result == 0:
            port_ready = True
            break
    except Exception:
        pass
    time.sleep(1)
```

### 5. Connect Selenium to Running Chrome (NOT launching new Chrome)
```python
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
self.driver = webdriver.Chrome(options=options)
```

**CRITICAL**: When using `debuggerAddress`, Selenium connects to an EXISTING Chrome instance without launching new one.

### 6. Verify Connection
```python
self.driver.get("https://x.com")
time.sleep(3)
```

---

## Why This Works

| Issue | Previous Approach | Solution |
|-------|------------------|----------|
| **Profile Locking** | Selenium launches Chrome with Default profile; multiple instances conflict | Use Scraper_Profile (non-standard dir) + subprocess launch |
| **DevTools Port Conflict** | Selenium's internal launch doesn't expose port | Subprocess launch with `--remote-debugging-port=9222` |
| **Chrome 136+ Security** | Default profile directory blocked from listening on arbitrary ports | Use separate Scraper_Profile directory |
| **Connection Failures** | Trying to connect before port is ready | Explicit port availability check with retries |

---

## Code Location

**File**: [Scraper/x_scraper.py](../../../Scraper/x_scraper.py)

**Method**: `TwitterListScraper.setup_driver()` (lines 213-309)

```python
def setup_driver(self):
    """Set up Chrome with Scraper_Profile + Selenium debugger connection."""
    import shutil
    from pathlib import Path
    import socket

    # 1. Kill existing processes
    # 2. Prepare Scraper_Profile
    # 3. Launch Chrome via subprocess
    # 4. Wait for port 9222
    # 5. Connect Selenium via debuggerAddress
    # 6. Verify connection
```

---

## Profile Authentication

### Initial Setup (One-Time)
1. Run [Scraper/setup_scraper_profile.py](../../../Scraper/setup_scraper_profile.py)
2. Opens Chrome with Scraper_Profile
3. Manually log into X.com
4. Browser stays open for manual interaction
5. Close when done

### Subsequent Runs
- Scraper_Profile contains cached authentication
- x_scraper.py automatically copies Default → Scraper_Profile if Scraper_Profile doesn't exist
- Logged-in session is preserved

---

## Files Modified/Created

1. **[Scraper/x_scraper.py](../../../Scraper/x_scraper.py)**
   - Updated `setup_driver()` method with hybrid approach
   - Uses Scraper_Profile instead of Default

2. **[Scraper/bookmarks_scraper.py](../../../Scraper/bookmarks_scraper.py)**
   - Applied same fix for X Bookmarks scraper

3. **[scripts/automation/run_all_scrapers.py](../../../scripts/automation/run_all_scrapers.py)**
   - Re-enabled X scrapers (were previously skipped)
   - Run X scrapers FIRST before other data scrapers
   - Fixed execution order

### Test Scripts (for verification)

1. **test_chrome_simple.py** - Basic subprocess launch ✓
2. **test_chrome_x.py** - Subprocess launch with X.com URL ✓
3. **test_selenium_scraper_profile.py** - Complete integration test ✓
4. **setup_scraper_profile.py** - Manual authentication setup ✓

---

## Debugging Commands

### Check if Chrome is running
```bash
tasklist | findstr chrome.exe
```

### Check if port 9222 is listening
```bash
netstat -ano | findstr 9222
```

### Kill all Chrome processes
```bash
taskkill /F /IM chrome.exe
```

### Monitor scraper execution
```bash
cd Scraper && python x_scraper.py
```

---

## Configuration

**File**: [Scraper/x_scraper.py](../../../Scraper/x_scraper.py) (lines 34-50)

```python
# X (Twitter) Configuration
X_CHROME_PROFILE_PATH = r"C:\Users\Iccanui\AppData\Local\Google\Chrome\User Data"
X_LISTS = [
    ("Technicals", "https://x.com/i/lists/1479448773449314306"),
    ("Crypto", "https://x.com/i/lists/1430346349375938572"),
    ("Macro", "https://x.com/i/lists/1366729121678589959")
]
X_SCROLL_INTERVAL = 0.5  # seconds between scrolls
X_MAX_POSTS = 0          # 0 = unlimited
X_MAX_DURATION = 86400   # 24 hours (safety)
X_CUTOFF_MODE = "last_24h"  # Options: "since_last", "last_24h", None
```

---

## Troubleshooting

### Issue: "DevToolsActivePort file doesn't exist"
- **Cause**: Chrome didn't launch properly or profile locked
- **Fix**: Kill Chrome, ensure no `chrome.exe` processes, restart scraper

### Issue: Port 9222 never becomes ready
- **Cause**: Chrome launch failed or profile issues
- **Fix**:
  - Check if Default profile exists
  - Delete Scraper_Profile and let it be recreated
  - Verify Chrome path: `C:\Program Files\Google\Chrome\Application\chrome.exe`

### Issue: "Not logged in - showing login page"
- **Cause**: Scraper_Profile lost authentication
- **Fix**: Run `setup_scraper_profile.py` to re-authenticate manually

### Issue: Selenium can't find elements after navigation
- **Cause**: Page didn't fully load
- **Fix**: Increase wait time in `self.driver.get()` calls (currently 3 seconds)

---

## Key Learnings

1. **Selenium Launch vs External Launch**
   - When launching Chrome externally (subprocess), Selenium MUST connect via `debuggerAddress`
   - DO NOT use any driver options that would launch a new Chrome instance

2. **Chrome 136+ Security**
   - Default profile directory has restrictions on remote-debugging-port
   - Non-standard profile directories (like Scraper_Profile) don't have this restriction

3. **Profile Management**
   - Separate profiles for different purposes (Default for user, Scraper_Profile for automation)
   - Profile copy-on-first-run ensures authentication portability

4. **Port Availability**
   - Always verify port is listening before connecting Selenium
   - Use socket connection test instead of relying on process startup

---

## Related Documentation

- [CHROME_SELENIUM_INTEGRATION_SOLUTION.md](../DOCUMENTATION/CHROME_SELENIUM_INTEGRATION_SOLUTION.md) - Detailed problem-solving journey
- [Scraper_README.md](../../INSTRUCTIONS/Domains/Scraper_README.md) - General scraper usage

---

## Success Metrics

After implementing this fix:

✓ Chrome launches successfully with Scraper_Profile
✓ Port 9222 becomes available immediately (1-2 attempts)
✓ Selenium connects without crashes
✓ X.com pages load and are authenticated
✓ Posts are harvested from X lists (Technicals, Crypto, Macro)
✓ Data is saved to JSON files
✓ Script can run in parallel with other scrapers

---

**Last Updated**: 2025-10-19
**Status**: ✓ WORKING
**Tested**: Yes - Verified with test_selenium_scraper_profile.py
