# Scout X Scraper Timeout - Debug & Fix Plan

**Date:** 2025-11-11
**Issue:** X scraper timing out, no visibility into what's happening
**Status:** ✅ RESOLVED - See SESSION_6_CONTINUATION_2025-11-11.md for implementation

---

## RESOLUTION SUMMARY

**Problem:** No real-time visibility into X scraper progress during 10+ minute runs
**Solution:** Replaced `subprocess.run()` with `subprocess.Popen()` + real-time output streaming
**Result:** All data sources working, no timeout issues, full visibility
**Implementation:** See `Toolbox/CHANGELOGS/SESSION_6_CONTINUATION_2025-11-11.md`

---

## Original Problem Analysis (Now Resolved)

---

## Problem Analysis

###Issue 1: X Scraper Timeout
- **Symptom:** Scraper gets stuck on Crypto list (list 2/3)
- **Timeout:** 600 seconds (10 minutes) configured
- **Error message:** Says ">5 minutes" (incorrect)
- **Root cause:** Unknown - no debug output visible

### Issue 2: No Logging/Visibility
- **Symptom:** Can't see X scraper progress when run via Scout
- **Current:** `capture_output=False` but subprocess output not piping through
- **Impact:** Can't debug timeouts or failures

### Issue 3: File Output Location Confusion
- Scout looks for files in: `Research/X/{list}/`
- X scraper may be writing to: `Scraper/X/{list}/` or current directory
- Need to verify actual output location

---

## Root config.py Location - CORRECT ✅

**User concern:** "`config.py` is in root and shouldn't be"

**Analysis:** config.py SHOULD be in root because:
1. `scripts/trading/api_client.py` imports it as `import config`
2. Python import system looks in project root first
3. We have a copy in `scout/config.py` for scout-specific use
4. This is intentional architecture per Session 5 design

**Action:** No change needed - this is correct

---

## Proposed Fixes

### Fix 1: Add Scraper Logging
**File:** `scout/scout.py` → `collect_x_twitter()` method

**Changes:**
```python
# Before:
result = subprocess.run(
    [sys.executable, str(x_scraper)],
    cwd=str(self.project_root),
    capture_output=False,
    timeout=600
)

# After:
import logging
logging.basicConfig(level=logging.INFO)

print("Starting X scraper with real-time output...")
print("=" * 70)

process = subprocess.Popen(
    [sys.executable, str(x_scraper)],
    cwd=str(self.project_root),
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,  # Line buffered
    universal_newlines=True
)

# Stream output in real-time
try:
    for line in iter(process.stdout.readline, ''):
        if line:
            print(line.rstrip())

    process.wait(timeout=600)

except subprocess.TimeoutExpired:
    process.kill()
    print("[ERROR] X scraper timeout after 10 minutes")
    return 'timeout'
```

**Benefits:**
- See real-time scraper progress
- Debug where timeout occurs
- Better user experience

### Fix 2: Fix Error Message
**File:** `scout/scout.py` line 220

**Change:**
```python
# Before:
print("[ERROR] X scraper timeout (>5 minutes)")

# After:
print("[ERROR] X scraper timeout (>10 minutes)")
```

### Fix 3: Add Timeout Warnings
**File:** `scout/scout.py` → `collect_x_twitter()` method

**Add periodic status checks:**
```python
import time
import threading

def timeout_warning(process, timeout_sec):
    """Print warnings at intervals during long-running scraper"""
    intervals = [120, 300, 480]  # 2min, 5min, 8min
    start = time.time()

    for interval in intervals:
        time.sleep(interval - (time.time() - start))
        if process.poll() is None:  # Still running
            elapsed = int(time.time() - start)
            print(f"[INFO] X scraper still running... ({elapsed}s elapsed)")

# Start warning thread
warning_thread = threading.Thread(
    target=timeout_warning,
    args=(process, 600),
    daemon=True
)
warning_thread.start()
```

### Fix 4: Verify File Paths
**File:** `Scraper/x_scraper.py`

**Check:** Where does x_scraper.py actually write files?
- Look for output_dir or save path configuration
- Ensure it writes to `Research/X/{list}/` not `Scraper/X/`

---

## Testing Plan

1. **Test with logging enabled:**
   ```bash
   python scout/scout.py
   # Watch real-time output
   # Note where scraper gets stuck
   ```

2. **Test X scraper directly:**
   ```bash
   python Scraper/x_scraper.py
   # Verify it completes without timeout
   # Check output file locations
   ```

3. **Check file locations:**
   ```bash
   find . -name "x_list_posts_*.json" -mmin -30
   # Verify files are in Research/X/
   ```

4. **Verify timeout handling:**
   - If scraper takes >10 min, verify graceful timeout
   - Verify error message is accurate
   - Verify Scout continues with API collection

---

## Implementation Priority

**High:**
1. Add real-time output streaming (Fix 1)
2. Fix error message (Fix 2)
3. Verify file paths (Fix 4)

**Medium:**
3. Add timeout warnings (Fix 3)

**Low:**
4. Add performance metrics (time per list)
5. Add retry logic for failed lists

---

## Alternative: Increase Timeout

If X scraper legitimately needs more time:

**Option A:** Increase timeout to 15 minutes (900s)
```python
timeout=900  # 15 minutes (4 lists × ~3-4 min each + buffer)
```

**Option B:** Make timeout configurable in config.py
```python
# config.py
X_SCRAPER_TIMEOUT = 900  # seconds

# scout.py
timeout=config.X_SCRAPER_TIMEOUT
```

---

## Next Steps

1. Implement Fix 1 (real-time output streaming)
2. Implement Fix 2 (correct error message)
3. Test with `python scout/scout.py`
4. Check where files are actually being written
5. Adjust timeout if needed based on actual scraper performance

---

**Document Created:** 2025-11-11
**Status:** Ready for implementation
**Estimated Time:** 30 minutes
