"""
Test script for Barchart Options Scraper

IMPORTANT: RnD Project
Run this to validate the Barchart scraper works correctly.

Tests with 5 popular tickers:
- SPY (high volume ETF)
- AAPL (mega cap stock)
- TSLA (high volatility stock)
- NVDA (active options)
- AMD (tech stock)
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scanner.scrapers.barchart_options import (
    scrape_options_chain,
    get_unusual_activity
)
from scanner.scrapers.utils import log_scraper_event


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def print_info(text):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


def test_single_ticker(ticker: str, test_num: int, total_tests: int) -> dict:
    """
    Test scraping a single ticker.

    Args:
        ticker: Stock symbol
        test_num: Current test number
        total_tests: Total number of tests

    Returns:
        dict with test results
    """
    print(f"\n{Colors.BOLD}[{test_num}/{total_tests}] Testing {ticker}...{Colors.ENDC}")
    print("-" * 70)

    result = {
        'ticker': ticker,
        'success': False,
        'error': None,
        'data_quality': {},
        'timing': {}
    }

    try:
        # Test 1: Basic scraping
        print(f"  Scraping options chain...")
        start_time = time.time()

        data = scrape_options_chain(ticker, max_expiries=2, use_cache=False)

        elapsed = time.time() - start_time
        result['timing']['scrape_time'] = elapsed

        if not data:
            result['error'] = "No data returned"
            print_error(f"  Failed to scrape {ticker} - no data returned")
            return result

        print_success(f"  Scraped in {elapsed:.2f}s")

        # Test 2: Data validation
        print(f"  Validating data structure...")

        # Check required fields
        required_fields = ['ticker', 'timestamp', 'stock_price', 'expirations']
        missing_fields = [f for f in required_fields if f not in data]

        if missing_fields:
            result['error'] = f"Missing fields: {missing_fields}"
            print_error(f"  Missing required fields: {missing_fields}")
            return result

        print_success(f"  All required fields present")

        # Test 3: Data quality checks
        print(f"  Checking data quality...")

        stock_price = data.get('stock_price', 0)
        expirations = data.get('expirations', [])
        num_expirations = len(expirations)

        result['data_quality']['stock_price'] = stock_price
        result['data_quality']['num_expirations'] = num_expirations

        # Stock price validation
        if stock_price > 0:
            print_success(f"  Stock price: ${stock_price:.2f}")
        else:
            print_warning(f"  Stock price missing or invalid: {stock_price}")

        # Expirations validation
        if num_expirations > 0:
            print_success(f"  Found {num_expirations} expiration dates")

            total_calls = 0
            total_puts = 0

            for i, exp in enumerate(expirations):
                calls = exp.get('calls', [])
                puts = exp.get('puts', [])
                expiry_date = exp.get('date', 'Unknown')
                days_to_expiry = exp.get('days_to_expiry', 0)

                total_calls += len(calls)
                total_puts += len(puts)

                print_info(f"    Expiry {i+1}: {expiry_date} ({days_to_expiry} days)")
                print(f"      Calls: {len(calls)} contracts")
                print(f"      Puts: {len(puts)} contracts")

                # Sample contract validation
                if calls:
                    sample_call = calls[0]
                    strike = sample_call.get('strike', 0)
                    last = sample_call.get('last', 0)
                    volume = sample_call.get('volume', 0)
                    oi = sample_call.get('open_interest', 0)
                    iv = sample_call.get('iv', 0)

                    print(f"      Sample call: Strike ${strike}, Last ${last:.2f}, Vol {volume}, OI {oi}, IV {iv:.1f}%")

                    # Validate sample data quality
                    if strike <= 0:
                        print_warning(f"      Invalid strike: {strike}")
                    if last < 0:
                        print_warning(f"      Invalid last price: {last}")

            result['data_quality']['total_calls'] = total_calls
            result['data_quality']['total_puts'] = total_puts

            if total_calls == 0 and total_puts == 0:
                print_warning(f"  No contracts found (may indicate scraping issue)")
            else:
                print_success(f"  Total: {total_calls} calls, {total_puts} puts")

        else:
            print_error(f"  No expirations found")
            result['error'] = "No expirations found"
            return result

        # Test 4: Unusual activity detection
        print(f"  Testing unusual activity detection...")
        start_time = time.time()

        unusual = get_unusual_activity(ticker, volume_oi_threshold=1.5, min_volume=50)

        if unusual:
            elapsed = time.time() - start_time
            result['timing']['unusual_activity_time'] = elapsed

            call_bias = unusual.get('call_flow_bias', 0)
            unusual_calls = len(unusual.get('unusual_calls', []))
            unusual_puts = len(unusual.get('unusual_puts', []))

            print_success(f"  Analyzed in {elapsed:.2f}s")
            print_info(f"    Call/Put Flow Bias: {call_bias:.2f}")
            print_info(f"    Unusual call contracts: {unusual_calls}")
            print_info(f"    Unusual put contracts: {unusual_puts}")

            result['data_quality']['unusual_calls'] = unusual_calls
            result['data_quality']['unusual_puts'] = unusual_puts
            result['data_quality']['call_flow_bias'] = call_bias
        else:
            print_warning(f"  Unusual activity analysis returned no data")

        # Test 5: Cache validation
        print(f"  Testing cache...")
        start_time = time.time()

        cached_data = scrape_options_chain(ticker, use_cache=True)
        elapsed = time.time() - start_time

        if cached_data and elapsed < 0.5:  # Should be near-instant
            print_success(f"  Cache working (retrieved in {elapsed:.3f}s)")
            result['data_quality']['cache_working'] = True
        else:
            print_warning(f"  Cache may not be working correctly")
            result['data_quality']['cache_working'] = False

        # Overall success
        result['success'] = True
        print_success(f"  {ticker} PASSED all tests!")

    except Exception as e:
        result['error'] = str(e)
        print_error(f"  {ticker} FAILED: {e}")
        import traceback
        print(f"\n{Colors.FAIL}Traceback:{Colors.ENDC}")
        traceback.print_exc()

    return result


def run_all_tests():
    """Run tests on all tickers"""
    print_header("BARCHART OPTIONS SCRAPER TEST SUITE")

    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Purpose: Validate Barchart scraper before building other scrapers")
    print()

    # Test tickers
    tickers = ['SPY', 'AAPL', 'TSLA', 'NVDA', 'AMD']

    print(f"Testing {len(tickers)} tickers: {', '.join(tickers)}")
    print(f"Estimated time: ~{len(tickers) * 15} seconds (with rate limiting)")

    input(f"\n{Colors.WARNING}Press Enter to start tests (or Ctrl+C to cancel)...{Colors.ENDC}")

    # Run tests
    results = []
    start_time = time.time()

    for i, ticker in enumerate(tickers, 1):
        result = test_single_ticker(ticker, i, len(tickers))
        results.append(result)

        # Rate limiting between tickers
        if i < len(tickers):
            wait_time = 3
            print(f"\n{Colors.OKCYAN}Rate limiting: waiting {wait_time}s before next ticker...{Colors.ENDC}")
            time.sleep(wait_time)

    total_time = time.time() - start_time

    # Summary report
    print_header("TEST SUMMARY")

    passed = sum(1 for r in results if r['success'])
    failed = len(results) - passed

    print(f"Total Tests: {len(results)}")
    print(f"Passed: {Colors.OKGREEN}{passed}{Colors.ENDC}")
    print(f"Failed: {Colors.FAIL}{failed}{Colors.ENDC}")
    print(f"Success Rate: {(passed/len(results)*100):.1f}%")
    print(f"Total Time: {total_time:.1f}s")
    print()

    # Detailed results
    print(f"\n{Colors.BOLD}Detailed Results:{Colors.ENDC}")
    print("-" * 70)

    for r in results:
        ticker = r['ticker']
        if r['success']:
            quality = r['data_quality']
            print(f"\n{Colors.OKGREEN}✓ {ticker}{Colors.ENDC}")
            print(f"  Stock Price: ${quality.get('stock_price', 0):.2f}")
            print(f"  Expirations: {quality.get('num_expirations', 0)}")
            print(f"  Total Contracts: {quality.get('total_calls', 0)} calls, {quality.get('total_puts', 0)} puts")
            print(f"  Scrape Time: {r['timing'].get('scrape_time', 0):.2f}s")
            print(f"  Cache: {'✓ Working' if quality.get('cache_working') else '✗ Not Working'}")

            # Flag potential issues
            if quality.get('total_calls', 0) == 0 and quality.get('total_puts', 0) == 0:
                print_warning(f"  ⚠ No contracts found - may indicate HTML structure change")
            elif quality.get('stock_price', 0) == 0:
                print_warning(f"  ⚠ Stock price not extracted - may need parser update")
        else:
            print(f"\n{Colors.FAIL}✗ {ticker}{Colors.ENDC}")
            print(f"  Error: {r['error']}")

    # Save results to file
    results_file = Path(__file__).parent.parent.parent / 'data' / 'test_results' / f"barchart_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    results_file.parent.mkdir(parents=True, exist_ok=True)

    with open(results_file, 'w') as f:
        json.dump({
            'test_date': datetime.now().isoformat(),
            'total_time': total_time,
            'passed': passed,
            'failed': failed,
            'results': results
        }, f, indent=2)

    print(f"\n{Colors.OKCYAN}Results saved to: {results_file}{Colors.ENDC}")

    # Final verdict
    print_header("FINAL VERDICT")

    if passed == len(results):
        print_success("ALL TESTS PASSED! ✓")
        print(f"\n{Colors.OKGREEN}The Barchart scraper is working correctly.{Colors.ENDC}")
        print(f"{Colors.OKGREEN}You can proceed to build the other scrapers.{Colors.ENDC}")
        return 0
    elif passed > 0:
        print_warning(f"PARTIAL SUCCESS: {passed}/{len(results)} passed")
        print(f"\n{Colors.WARNING}Some tickers failed. Review errors above.{Colors.ENDC}")
        print(f"{Colors.WARNING}May need to adjust HTML parsing logic.{Colors.ENDC}")
        return 1
    else:
        print_error("ALL TESTS FAILED! ✗")
        print(f"\n{Colors.FAIL}Barchart scraper needs debugging.{Colors.ENDC}")
        print(f"{Colors.FAIL}Check HTML structure at barchart.com/stocks/quotes/SPY/options{Colors.ENDC}")
        return 2


if __name__ == '__main__':
    try:
        exit_code = run_all_tests()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Tests cancelled by user.{Colors.ENDC}")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n{Colors.FAIL}Unexpected error: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
