# X Scraper - Logging & Debugging Setup

## Current Logging

The scraper already provides **detailed console output** showing:
- ✅ Chrome launch status
- ✅ Port availability checks
- ✅ Selenium connection status
- ✅ Posts collected per scroll
- ✅ Duplicate detection
- ✅ Data saved confirmation

### Example Output Pattern
```
Opening Chrome with Scraper_Profile...
    Killing existing Chrome processes...
    Done. Waiting 2 seconds...
    ✓ Debugging port is ready (attempt 1)
    ✓ Selenium connected to Chrome
    Opening https://x.com/i/lists/1479448773449314306
      Collected 7 new, skipped 2 old. Total: 16 posts
      Collected 5 new, skipped 7 existing, skipped 2 old. Total: 21 posts
    Saved 75 total posts (66 new) to x_list_posts_20251019091755.json
```

---

## Advanced Debugging Options

### 1. Capture Output to Log File

```bash
cd Scraper
python x_scraper.py > scraper_run_$(date +%Y%m%d_%H%M%S).log 2>&1
```

This creates a timestamped log file:
```
scraper_run_20251019_161500.log
```

### 2. Monitor Browser Activity

Add verbose driver logging to x_scraper.py:

```python
from selenium.webdriver.chrome.service import Service

# Inside setup_driver() method, add:
service = Service(log_path="chromedriver.log", verbose=True)
self.driver = webdriver.Chrome(service=service, options=options)
```

This creates `chromedriver.log` with detailed browser automation events.

### 3. Add Python Logging Framework

Add to x_scraper.py (top of file):

```python
import logging
import logging.handlers
from datetime import datetime

# Setup logging
log_filename = f"scraper_logs/x_scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
os.makedirs("scraper_logs", exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
```

Then replace all `print()` with `logger.info()`:

```python
# Before
print("Opening Chrome with Scraper_Profile...")

# After
logger.info("Opening Chrome with Scraper_Profile...")
```

---

## Debugging Hangs (Like You Experienced)

When the browser seems to "hang" while scraping Macro, it could be:

### Problem: Page Load Issues

**Symptom**: Scrolling stops, no new posts found, but browser still open

**Debug**:
```python
# Inside harvest_once() method, add:
logger.debug(f"Current page height: {self.driver.execute_script('return document.body.scrollHeight')}")
logger.debug(f"Current scroll position: {self.driver.execute_script('return window.scrollY')}")
logger.debug(f"Found articles: {len(self.driver.find_elements(By.CSS_SELECTOR, 'article'))}")
```

### Problem: Timeout Waiting for Content

**Symptom**: "Waiting for port" or "Waiting for elements" takes forever

**Debug**:
```python
# Add shorter timeout for specific operations
timeout = WebDriverWait(self.driver, timeout=5)  # 5 seconds instead of default

# With explicit wait logging
logger.info(f"Waiting for articles to load (timeout: 5s)...")
try:
    timeout.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article')))
    logger.info("Articles loaded successfully")
except TimeoutException:
    logger.error("Timeout: Articles never loaded")
```

### Problem: Memory/Process Issues

**Check if something is consuming resources**:

```bash
# Monitor Chrome memory usage
tasklist | findstr chrome

# Get detailed process info
wmic process where name="chrome.exe" get ProcessId,WorkingSetSize,VirtualSize

# Check if port 9222 is actually listening
netstat -ano | findstr 9222
```

---

## Creating a Robust Debug Session

### Enhanced Test Script with Full Logging

Create **[Scraper/debug_scraper_session.py](../../../Scraper/debug_scraper_session.py)**:

```python
#!/usr/bin/env python3
"""Enhanced X Scraper with detailed debugging"""

import logging
import sys
from pathlib import Path
from datetime import datetime

# Setup logging
log_dir = Path("scraper_logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)-8s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("X_Scraper")

# Now run the scraper with enhanced logging
from x_scraper import TwitterListScraper, X_CHROME_PROFILE_PATH, X_LISTS

logger.info("=" * 70)
logger.info("Starting X Scraper with DEBUG logging")
logger.info(f"Log file: {log_file}")
logger.info("=" * 70)

for idx, (list_name, list_url) in enumerate(X_LISTS, start=1):
    logger.info(f"\n[{idx}/3] Starting list: {list_name}")
    logger.info(f"URL: {list_url}")

    try:
        scraper = TwitterListScraper(
            profile_path=X_CHROME_PROFILE_PATH,
            list_url=list_url,
            list_name=list_name
        )

        logger.info("Setting up driver...")
        scraper.setup_driver()
        logger.info("Driver setup complete")

        logger.info("Starting scrape...")
        scraper.scrape()
        logger.info(f"Scrape complete: {scraper.new_posts_count} new posts")

        logger.info("Saving and closing...")
        scraper.save_json_and_close(Path("../Research") / "X" / list_name)
        logger.info("Complete")

    except Exception as e:
        logger.exception(f"ERROR in {list_name}: {e}")

logger.info("\n" + "=" * 70)
logger.info("X Scraper session complete")
logger.info("=" * 70)
```

### Run with Debugging

```bash
cd Scraper
python debug_scraper_session.py
```

This creates a detailed log file with timestamps and severity levels.

---

## Monitoring in Real-Time

### Watch Log File Live

```bash
# Windows PowerShell
Get-Content -Path "scraper_logs/debug_*.log" -Wait -Tail 50
```

### Check Specific Metrics

Add mid-run status to harvest_once():

```python
# After collecting posts, log status
if len(self.posts) % 50 == 0:  # Every 50 posts
    logger.info(f"[PROGRESS] Total: {len(self.posts)}, "
                f"New: {self.new_posts_count}, "
                f"Browser pages height: {self.driver.execute_script('return document.body.scrollHeight')}")
```

---

## Common Issues & Debug Output

### Issue: Browser Hangs During Macro Scraping

**Expected Debug Output**:
```
[16:25:00] Starting list: Macro
[16:25:02] Setting up driver...
[16:25:03] ✓ Debugging port is ready (attempt 1)
[16:25:04] ✓ Selenium connected to Chrome
[16:25:05] Starting scrape...
[16:25:07] [PROGRESS] Total: 50, New: 48, Browser height: 12500px
[16:25:12] [PROGRESS] Total: 100, New: 96, Browser height: 24800px
[HANG HERE - No progress updates]
```

**If you see this**: Check if page is still scrolling
```python
# Add watchdog timer
start_time = time.time()
while (time.time() - start_time) < 5 * 60:  # 5 min timeout
    # ... scraping logic ...
    if no new posts in 60 seconds:
        logger.warning("No new posts found in 60 seconds, checking page...")
        logger.debug(f"Page height: {self.driver.execute_script(...)}")
        logger.debug(f"Scroll position: {self.driver.execute_script(...)}")
```

---

## Accessing Log Files

Log files are saved to: `Scraper/scraper_logs/`

View latest:
```bash
dir Scraper\scraper_logs /O:-D  # Most recent first
```

View specific run:
```bash
type Scraper\scraper_logs\debug_20251019_162500.log | more
```

Search for errors:
```bash
findstr "ERROR\|EXCEPTION" Scraper\scraper_logs\*.log
```

---

## Environment Diagnostics

Create **[Scraper/diagnose_environment.py](../../../Scraper/diagnose_environment.py)**:

```python
#!/usr/bin/env python3
"""Diagnose X Scraper environment"""

import sys
import subprocess
from pathlib import Path

print("=" * 70)
print("X SCRAPER ENVIRONMENT DIAGNOSTICS")
print("=" * 70)

# Python version
print(f"\n[1] Python Version")
print(f"    {sys.version}")

# Chrome installation
print(f"\n[2] Chrome Installation")
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if Path(chrome_path).exists():
    print(f"    ✓ Found: {chrome_path}")
    result = subprocess.run([chrome_path, "--version"], capture_output=True, text=True)
    print(f"    Version: {result.stdout.strip()}")
else:
    print(f"    ✗ Not found: {chrome_path}")

# Chrome profiles
print(f"\n[3] Chrome Profiles")
profiles_dir = Path(r"C:\Users\Iccanui\AppData\Local\Google\Chrome\User Data")
if profiles_dir.exists():
    profiles = [p for p in profiles_dir.iterdir() if p.is_dir()]
    for p in profiles:
        print(f"    - {p.name}")
else:
    print(f"    ✗ Not found: {profiles_dir}")

# Selenium version
print(f"\n[4] Selenium Version")
try:
    from selenium import __version__
    print(f"    ✓ {__version__}")
except:
    print(f"    ✗ Not installed")

# Port availability
print(f"\n[5] Port 9222 (Remote Debugging)")
result = subprocess.run(["netstat", "-ano"], capture_output=True, text=True)
if "9222" in result.stdout:
    print(f"    ⚠ Port is in use (might need cleanup)")
else:
    print(f"    ✓ Port available")

# Memory
print(f"\n[6] System Resources")
result = subprocess.run(["tasklist", "/v"], capture_output=True, text=True)
chrome_lines = [l for l in result.stdout.split('\n') if 'chrome' in l.lower()]
print(f"    Chrome processes: {len(chrome_lines)}")

print("\n" + "=" * 70)
```

Run it:
```bash
python Scraper/diagnose_environment.py
```

---

## Next Steps

To enable comprehensive logging:

1. **For current session**: Run with output capture
   ```bash
   python x_scraper.py > run.log 2>&1
   ```

2. **For ongoing monitoring**: Use debug script
   ```bash
   python debug_scraper_session.py
   ```

3. **For deep investigation**: Check environment
   ```bash
   python diagnose_environment.py
   ```

---

**Note**: All logs are timestamped and saved for later analysis. This helps identify:
- When/where processes hang
- Resource constraints
- Network issues
- Browser crashes
- Selenium connection problems

