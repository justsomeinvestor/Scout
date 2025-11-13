# Toolbox/TECH_SUPPORT - X Scraper Support Documentation

Complete technical support and debugging resources for the X/Twitter scraper.

---

## 📋 Documentation Map

### Getting Started
- **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** ← Start here
  - How to run the scraper
  - Common errors and quick fixes
  - Performance tuning
  - File locations

### Understanding the Solution
- **[SOLUTION_SUMMARY.md](./SOLUTION_SUMMARY.md)**
  - High-level overview of the problem and fix
  - Before/after comparison
  - Success metrics
  - Impact assessment

- **[X_SCRAPER_CHROME_SELENIUM_FIX.md](./X_SCRAPER_CHROME_SELENIUM_FIX.md)**
  - Deep technical explanation
  - Implementation walkthrough
  - Why each step is necessary
  - Configuration options

### Debugging & Monitoring
- **[LOGGING_AND_DEBUG_SETUP.md](./LOGGING_AND_DEBUG_SETUP.md)**
  - How to enable detailed logging
  - Real-time monitoring techniques
  - Environment diagnostics
  - Capturing session logs

- **[TROUBLESHOOTING_HANGS.md](./TROUBLESHOOTING_HANGS.md)**
  - What to do if browser freezes
  - Common hang scenarios
  - Root causes and fixes
  - Prevention checklist

---

## 🚀 Quick Start

### Run the Scraper
```bash
cd Scraper
python x_scraper.py
```

### Enable Detailed Logging
```bash
cd Scraper
python x_scraper.py > session_$(date +%Y%m%d_%H%M%S).log 2>&1
```

### First Time Setup (Authentication)
```bash
cd Scraper
python setup_scraper_profile.py
# Manually log into X.com
# Close browser
```

---

## 🔧 Common Solutions

### Problem: "Chrome failed to start: crashed"
**Solution**: See [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) → "Common Errors & Fixes"
```bash
taskkill /F /IM chrome.exe
```

### Problem: Browser hangs during scraping
**Solution**: See [TROUBLESHOOTING_HANGS.md](./TROUBLESHOOTING_HANGS.md)
- Check log files for where it stopped
- Increase scroll delay
- Kill and restart

### Problem: "Not logged in - showing login page"
**Solution**: Re-run authentication
```bash
python setup_scraper_profile.py
```

### Problem: Need to debug a specific issue
**Solution**: See [LOGGING_AND_DEBUG_SETUP.md](./LOGGING_AND_DEBUG_SETUP.md)
- Enable file logging
- Monitor in real-time
- Check environment diagnostics

---

## 📊 Architecture Overview

### How It Works

1. **Subprocess Launch**: Chrome started independently (not via Selenium)
   ```python
   subprocess.Popen([chrome_path, '--remote-debugging-port=9222', ...])
   ```

2. **Port Verification**: Wait for remote debugging port to be ready
   ```python
   socket.connect_ex(("127.0.0.1", 9222))
   ```

3. **Selenium Connection**: Connect to already-running Chrome
   ```python
   options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
   driver = webdriver.Chrome(options=options)
   ```

4. **Profile Strategy**: Use separate Scraper_Profile (not Default)
   - Avoids security restrictions
   - Preserves authentication
   - Prevents profile conflicts

**Result**: ✅ Reliable Chrome automation without crashes

---

## 📈 Success Metrics

From successful run on 2025-10-19:

| List | Total Posts | New Posts | Time |
|------|------------|-----------|------|
| Technicals | 75 | 66 | ~3 min |
| Crypto | 405 | 252 | ~7 min |
| Macro | 204 | 166 | ~5 min |
| **Total** | **684** | **484** | **~15 min** |

---

## 🔍 File Locations

### Scraper Code
- **x_scraper.py** - Main X/Twitter list scraper
- **bookmarks_scraper.py** - X bookmarks scraper
- **setup_scraper_profile.py** - One-time authentication setup

### Output Data
- **Research/X/Technicals/** - Posts from Technicals list
- **Research/X/Crypto/** - Posts from Crypto list
- **Research/X/Macro/** - Posts from Macro list

### Chrome Profile
- `C:\Users\Iccanui\AppData\Local\Google\Chrome\User Data\Scraper_Profile`
  - Authentication cached here
  - Auto-created from Default on first run

### Debug Logs
- **scraper_logs/** - Timestamped debug logs (if logging enabled)

---

## 🛠️ Technical Stack

- **Python**: 3.12+
- **Selenium**: WebDriver for browser automation
- **Chrome**: 136+ (subprocess-launched)
- **Remote Debugging**: Port 9222 via debuggerAddress
- **Profile**: Separate Scraper_Profile for automation

---

## 📝 Configuration

Edit [Scraper/x_scraper.py](../../../Scraper/x_scraper.py) lines 34-50:

```python
X_SCROLL_INTERVAL = 0.5      # Seconds between scrolls (lower = faster but more load)
X_MAX_POSTS = 0              # 0 = unlimited, or set number
X_MAX_DURATION = 86400       # Max seconds to run (24 hours)
X_CUTOFF_MODE = "last_24h"   # "since_last" or "last_24h" or None
X_MAX_NO_NEW = 30            # Stop after N scrolls with no new posts
```

**Recommended for Macro (large list)**:
```python
X_SCROLL_INTERVAL = 1.5      # Slower to avoid rate limiting
X_MAX_DURATION = 1200        # 20 minute limit
X_MAX_NO_NEW = 40            # Allow more attempts
```

---

## 🐛 Debugging Tips

### Enable Real-Time Monitoring
```bash
# Run in one terminal
python x_scraper.py > run.log 2>&1

# In another terminal, watch live
Get-Content run.log -Wait -Tail 50
```

### Check if Something is Stuck
```bash
# Is Chrome still running?
tasklist | findstr chrome

# Is port 9222 listening?
netstat -ano | findstr 9222

# Check logs for last status
tail -50 scraper_logs/debug_*.log
```

### Diagnose Environment
```bash
python diagnose_environment.py
```

---

## 📞 Support Resources

### Inside This Folder
- See [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) for immediate help
- See [TROUBLESHOOTING_HANGS.md](./TROUBLESHOOTING_HANGS.md) if browser freezes
- See [LOGGING_AND_DEBUG_SETUP.md](./LOGGING_AND_DEBUG_SETUP.md) for detailed debugging

### Related Documentation
- [CHROME_SELENIUM_INTEGRATION_SOLUTION.md](../DOCUMENTATION/CHROME_SELENIUM_INTEGRATION_SOLUTION.md) - Detailed problem-solving journey

---

## ✅ Checklist: Before Running

- [ ] Close all other Chrome windows
- [ ] Check port 9222 is free: `netstat -ano | findstr 9222`
- [ ] Verify Chrome installed: `"C:\Program Files\Google\Chrome\Application\chrome.exe"`
- [ ] Verify profile exists: `C:\Users\Iccanui\AppData\Local\Google\Chrome\User Data\Default`
- [ ] Have ~30-45 minutes available (full run: Technicals, Crypto, Macro)

---

## 🔄 Workflow

```
1. First Time Setup
   └─ python setup_scraper_profile.py
   └─ Manually log into X.com

2. Standard Run
   └─ cd Scraper
   └─ python x_scraper.py
   └─ Result: JSON files in Research/X/{list_name}/

3. Debug If Needed
   └─ Check logs: scraper_logs/debug_*.log
   └─ Run diagnostics: python diagnose_environment.py
   └─ See TROUBLESHOOTING_HANGS.md for solutions
```

---

**Documentation Status**: ✅ Complete
**Last Updated**: 2025-10-19
**Version**: 1.0
