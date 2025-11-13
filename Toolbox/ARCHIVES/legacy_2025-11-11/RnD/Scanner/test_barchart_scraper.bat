@echo off
REM Test Barchart Options Scraper
REM Run from RnD/Scanner/ directory

echo.
echo ================================================================================
echo  Testing Barchart Options Scraper
echo ================================================================================
echo.
echo This will test scraping options data from Barchart.com with 5 tickers:
echo   - SPY, AAPL, TSLA, NVDA, AMD
echo.
echo Estimated time: ~60 seconds (with rate limiting)
echo.

python scanner\scrapers\test_barchart.py

echo.
echo ================================================================================
echo Test complete! Check output above for results.
echo ================================================================================
echo.
pause
