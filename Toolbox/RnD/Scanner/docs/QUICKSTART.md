# Quick Start Guide - Barchart Scraper Testing

**Status:** Week 1 - Scraper Infrastructure Build
**Current Phase:** Testing Barchart Options Scraper

---

## 📋 Prerequisites

Before running the tests, ensure you have:

1. **Python 3.12+** installed
2. **Required packages** installed:
   ```bash
   cd RnD/Scanner
   pip install -r requirements.txt
   ```

3. **Internet connection** (for scraping Barchart.com)

---

## 🧪 Running the Barchart Scraper Test

We've built the **Barchart Options Scraper** - now we need to validate it works correctly.

### Method 1: Using Batch File (Windows)

```bash
cd RnD/Scanner
test_barchart_scraper.bat
```

### Method 2: Using Python Script (Cross-Platform)

```bash
cd RnD/Scanner
python test_barchart_scraper.py
```

### Method 3: Direct Test (Advanced)

```bash
cd RnD/Scanner
python scanner/scrapers/test_barchart.py
```

---

## 📊 What the Test Does

The test script will:

1. **Scrape 5 tickers:** SPY, AAPL, TSLA, NVDA, AMD
2. **Validate data quality:**
   - Stock price extraction
   - Options chain structure
   - Contract data (strikes, volume, OI, IV)
   - Multiple expiration dates
3. **Test unusual activity detection:**
   - Volume/OI ratios
   - Call/put flow bias
4. **Verify caching:** Ensures data is cached properly
5. **Rate limiting:** Respects 2-3 second delays between tickers

**Expected Duration:** ~60 seconds total

---

## ✅ Expected Results

### Success Case (What We Hope to See)

```
================================================================================
                        TEST SUMMARY
================================================================================

Total Tests: 5
Passed: 5
Failed: 0
Success Rate: 100.0%
Total Time: 58.3s

✓ SPY
  Stock Price: $601.50
  Expirations: 2
  Total Contracts: 245 calls, 238 puts
  Scrape Time: 4.23s
  Cache: ✓ Working

✓ AAPL
  ...

================================================================================
                        FINAL VERDICT
================================================================================

✓ ALL TESTS PASSED! ✓

The Barchart scraper is working correctly.
You can proceed to build the other scrapers.
```

### Partial Success (Some Fixes Needed)

If 3-4 out of 5 tickers pass:
- **Review errors** for failed tickers
- May need to adjust HTML parsing logic
- Check if Barchart changed their website structure
- Try manually visiting: `https://www.barchart.com/stocks/quotes/SPY/options`

### Complete Failure (Debugging Required)

If 0 tickers pass:
- **Check internet connection**
- **Verify Barchart.com is accessible**
- May need to update scraper HTML selectors
- Barchart may have changed their website structure

---

## 🔍 Troubleshooting

### Error: "No module named 'requests'"

**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Error: "Failed to fetch URL" or "HTTP 403"

**Cause:** Barchart may be blocking automated requests

**Solutions:**
1. Try again in a few minutes (temporary rate limit)
2. Check if Barchart.com is accessible in your browser
3. May need to add more realistic user-agent headers

### Error: "No options data found"

**Cause:** HTML structure changed on Barchart website

**Solutions:**
1. Manually visit: `https://www.barchart.com/stocks/quotes/SPY/options`
2. Check if options data is displayed
3. If structure changed, we'll need to update the parser

### Error: "No contracts found"

**Cause:** HTML parsing may not be extracting tables correctly

**Next Steps:**
- This is expected in RnD - we may need to iterate on the HTML parser
- The test will save detailed results to `data/test_results/`
- We'll review and adjust the scraper logic

---

## 📁 Test Output Files

Test results are automatically saved to:
```
RnD/Scanner/data/test_results/barchart_test_YYYYMMDD_HHMMSS.json
```

Contains:
- Test date/time
- Pass/fail status per ticker
- Data quality metrics
- Timing information
- Error messages (if any)

---

## 🎯 What Happens Next?

### If Tests Pass (100% or 80%+):
1. ✅ Mark Barchart scraper as validated
2. ✅ Proceed to build **Finviz Fundamentals Scraper**
3. ✅ Continue with remaining scrapers

### If Tests Fail (<50% pass rate):
1. ⚠️ Debug Barchart scraper
2. ⚠️ Update HTML parsing logic
3. ⚠️ Retest until passing
4. ⚠️ Then proceed to other scrapers

---

## 🐛 Known Limitations (RnD Phase)

Since this is RnD, the scraper may have issues:

1. **HTML Structure Dependency:**
   - Barchart can change their HTML at any time
   - May require periodic updates to selectors

2. **Data Completeness:**
   - Some fields (Greeks, IV) may not be extracted initially
   - We'll iterate and improve as needed

3. **Rate Limiting:**
   - Barchart may rate-limit if we scrape too aggressively
   - Test respects 2-3 second delays

4. **No Real-Time Updates:**
   - Cache is 5 minutes (by design)
   - Not suitable for second-by-second updates

These are **acceptable in RnD** - we'll refine as we validate the approach.

---

## 📝 Reporting Results

After running the test, please note:

1. **Pass/Fail Status:** Did all 5 tickers work?
2. **Data Quality:** Were strikes, volumes, prices extracted?
3. **Errors:** Any specific error messages?
4. **Timing:** Did scraping complete in ~60 seconds?

Share results so we can:
- Proceed to next scrapers (if passing)
- Debug issues (if failing)
- Adjust parsing logic (if partial success)

---

## 🚀 Next Steps After Testing

Once Barchart test passes:
1. Build **Finviz Fundamentals Scraper** (float, sector, volume)
2. Build **Finviz Screener Scraper** (universe selection)
3. Build **Yahoo Finance Stats Scraper** (fallback)
4. Build **MarketWatch Earnings Calendar**
5. Test all scrapers together for 48 hours

Then proceed to **Week 2: Core Scanner + Real-Time Data**

---

**Remember:** This is RnD! Expect some failures and iteration. That's the point of testing in RnD first.

**Location:** `RnD/Scanner/` (stays here until proven reliable)
**Status:** Testing Phase 🧪
