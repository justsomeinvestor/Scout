#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick test to verify Polygon.io API works for SPX and VIX indices.
Usage: python test_indices.py YOUR_API_KEY
or: set POLYGON_API_KEY=YOUR_KEY & python test_indices.py
"""

import sys
import os
import requests
import json

# Get API key from argument or environment
api_key = sys.argv[1] if len(sys.argv) > 1 else os.getenv('POLYGON_API_KEY')

if not api_key:
    print("ERROR: API key not provided")
    print("Usage: python test_indices.py YOUR_KEY")
    print("or: set POLYGON_API_KEY=YOUR_KEY & python test_indices.py")
    sys.exit(1)

print("\n" + "="*70)
print("POLYGON.IO INDICES API TEST")
print("="*70 + "\n")

def test_index(index_symbol, name, min_price, max_price):
    """Test a single index"""
    print(f"[{index_symbol}] Testing {name}...")

    try:
        # Step 1: Verify ticker exists using reference endpoint with market=indices filter
        print(f"   Step 1: Verifying ticker exists...")
        ref_url = f"https://api.polygon.io/v3/reference/tickers?ticker={index_symbol}&market=indices&apiKey={api_key}"
        ref_response = requests.get(ref_url, timeout=10)

        if ref_response.status_code != 200:
            print(f"   ERROR: Could not find ticker {index_symbol} (HTTP {ref_response.status_code})")
            return False

        ref_data = ref_response.json()
        if ref_data.get('status') != 'OK' or not ref_data.get('results'):
            print(f"   ERROR: Ticker {index_symbol} not found in indices market")
            return False

        ticker_info = ref_data['results'][0]
        print(f"   Found: {ticker_info.get('name', 'Unknown')}")

        # Step 2: Get current price using aggregates endpoint
        print(f"   Step 2: Fetching current price...")
        agg_url = f"https://api.polygon.io/v2/aggs/ticker/{index_symbol}/prev?apiKey={api_key}"
        agg_response = requests.get(agg_url, timeout=10)

        if agg_response.status_code != 200:
            print(f"   ERROR: Could not fetch aggregates (HTTP {agg_response.status_code})")
            print(f"   Response: {agg_response.text[:200]}")
            return False

        agg_data = agg_response.json()

        if agg_data.get('status') != 'OK':
            print(f"   ERROR: {agg_data.get('message', 'Unknown error')}")
            return False

        # Extract price from aggregates response
        if 'results' not in agg_data or not agg_data['results']:
            print(f"   ERROR: No aggregates data available")
            return False

        agg_result = agg_data['results'][0]
        current_price = agg_result.get('c')  # close price

        if not current_price:
            print(f"   ERROR: Could not extract price")
            print(f"   Available fields: {list(agg_result.keys())}")
            return False

        # Validate price range
        if not (min_price < current_price < max_price):
            print(f"   ERROR: Price {current_price} outside expected range ({min_price}-{max_price})")
            return False

        # Extract change info if available
        open_price = agg_result.get('o')
        change = current_price - open_price if open_price else None
        change_pct = (change / open_price * 100) if change and open_price else None

        print(f"   ✓ Price: ${current_price:,.2f}")
        if change is not None:
            print(f"   ✓ Change: {change:+.2f} ({change_pct:+.2f}%)")
        print(f"   ✓ Valid range")
        print(f"   ✓ SUCCESS")
        return True

    except requests.exceptions.RequestException as e:
        print(f"   ERROR: Network error - {e}")
        return False
    except Exception as e:
        print(f"   ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


# Test both indices
spx_ok = test_index("I:SPX", "S&P 500 Index", 6000, 7500)
vix_ok = test_index("I:VIX", "Volatility Index", 5, 80)

# Summary
print("="*70)
if spx_ok and vix_ok:
    print("[PASS] BOTH INDICES WORKING - Ready for production!")
    print("="*70 + "\n")
    sys.exit(0)
else:
    print("[FAIL] SOME TESTS FAILED - Review above")
    print("="*70 + "\n")
    sys.exit(1)
