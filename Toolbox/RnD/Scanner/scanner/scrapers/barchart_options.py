"""
Barchart Options Chain Scraper

IMPORTANT: RnD Project
This code is in Research & Development (RnD/Scanner/).
Do not move to production until proven reliable (see README.md).

Scrapes options data from Barchart.com:
- Strikes, last price, bid/ask
- Volume, Open Interest
- Implied Volatility
- Greeks (delta, gamma, theta, vega) if available

Rate Limit: 2 seconds between requests
Cache: 5 minutes (options data changes frequently)
"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from .utils import (
    scrape_with_retry,
    rate_limit_delay,
    record_scraper_status,
    parse_float,
    parse_int,
    validate_ticker,
    load_from_cache,
    save_to_cache,
    parse_soup,
    log_scraper_event
)


def scrape_options_chain(
    ticker: str,
    max_expiries: int = 3,
    use_cache: bool = True,
    cache_max_age: int = 300  # 5 minutes
) -> Optional[Dict]:
    """
    Scrape options chain data from Barchart.com.

    Args:
        ticker: Stock ticker symbol (e.g., "SPY", "AAPL")
        max_expiries: Maximum number of expiry dates to fetch (default 3)
        use_cache: Whether to use cached data if available
        cache_max_age: Maximum age of cache in seconds (default 5 minutes)

    Returns:
        Dictionary with structure:
        {
            'ticker': str,
            'timestamp': str (ISO format),
            'stock_price': float,
            'expirations': [
                {
                    'date': str (YYYY-MM-DD),
                    'days_to_expiry': int,
                    'calls': [
                        {
                            'strike': float,
                            'last': float,
                            'change': float,
                            'bid': float,
                            'ask': float,
                            'volume': int,
                            'open_interest': int,
                            'iv': float (implied volatility %),
                            'delta': float (optional),
                            'gamma': float (optional),
                            'theta': float (optional),
                            'vega': float (optional)
                        },
                        ...
                    ],
                    'puts': [...same structure...]
                },
                ...
            ]
        }

        Returns None if scraping failed.
    """
    # Validate ticker
    if not validate_ticker(ticker):
        log_scraper_event('barchart_options', f"Invalid ticker: {ticker}", 'ERROR')
        record_scraper_status('barchart_options', 0, f"Invalid ticker: {ticker}")
        return None

    ticker = ticker.upper()

    # Check cache
    if use_cache:
        cached = load_from_cache('barchart_options', ticker, cache_max_age)
        if cached:
            log_scraper_event('barchart_options', f"Using cached data for {ticker}", 'INFO')
            return cached

    log_scraper_event('barchart_options', f"Scraping options chain for {ticker}", 'INFO')

    try:
        # Barchart options URL
        url = f"https://www.barchart.com/stocks/quotes/{ticker}/options"

        # Scrape with retry
        response = scrape_with_retry(
            url,
            max_retries=3,
            delay=2.0,
            timeout=15,
            user_agent='default'
        )

        if not response:
            log_scraper_event('barchart_options', f"Failed to fetch {url}", 'ERROR')
            record_scraper_status('barchart_options', 0, f"HTTP request failed for {ticker}")
            return None

        # Parse HTML
        soup = parse_soup(response.text, 'html.parser')
        if not soup:
            log_scraper_event('barchart_options', f"Failed to parse HTML for {ticker}", 'ERROR')
            record_scraper_status('barchart_options', 0, f"HTML parsing failed for {ticker}")
            return None

        # Extract stock price (from header)
        stock_price = _extract_stock_price(soup, ticker)

        # Extract expirations
        expirations_data = _extract_expirations(soup, ticker, max_expiries)

        if not expirations_data:
            log_scraper_event('barchart_options', f"No options data found for {ticker}", 'WARNING')
            record_scraper_status('barchart_options', 0, f"No options data found for {ticker}")
            return None

        # Build result
        result = {
            'ticker': ticker,
            'timestamp': datetime.now().isoformat(),
            'stock_price': stock_price,
            'expirations': expirations_data,
            'source': 'barchart.com',
            'cache_age_seconds': 0  # Fresh data
        }

        # Save to cache
        if use_cache:
            save_to_cache('barchart_options', ticker, result)

        # Record success
        total_contracts = sum(
            len(exp.get('calls', [])) + len(exp.get('puts', []))
            for exp in expirations_data
        )
        log_scraper_event('barchart_options', f"Successfully scraped {total_contracts} contracts for {ticker}", 'INFO')
        record_scraper_status('barchart_options', total_contracts)

        # Rate limit
        rate_limit_delay('barchart')

        return result

    except Exception as e:
        log_scraper_event('barchart_options', f"Error scraping {ticker}: {e}", 'ERROR')
        record_scraper_status('barchart_options', 0, str(e))
        return None


def _extract_stock_price(soup, ticker: str) -> float:
    """
    Extract current stock price from Barchart page.

    Args:
        soup: BeautifulSoup object
        ticker: Stock ticker

    Returns:
        Stock price (float) or 0.0 if not found
    """
    try:
        # Look for price in header (common pattern: <span class="last-change">)
        price_elem = soup.find('span', class_='last-change')
        if price_elem:
            price_text = price_elem.text.strip()
            return parse_float(price_text, 0.0)

        # Fallback: Look for any element with data-ng-bind="quote.lastPrice"
        price_elem = soup.find(attrs={'data-ng-bind': 'quote.lastPrice'})
        if price_elem:
            return parse_float(price_elem.text, 0.0)

        # Fallback: Look in meta tags
        price_meta = soup.find('meta', property='og:price:amount')
        if price_meta and price_meta.get('content'):
            return parse_float(price_meta['content'], 0.0)

    except Exception as e:
        log_scraper_event('barchart_options', f"Error extracting stock price: {e}", 'WARNING')

    return 0.0


def _extract_expirations(soup, ticker: str, max_expiries: int) -> List[Dict]:
    """
    Extract options chain data for multiple expiration dates.

    Args:
        soup: BeautifulSoup object
        ticker: Stock ticker
        max_expiries: Maximum number of expiries to extract

    Returns:
        List of expiration dictionaries
    """
    expirations = []

    try:
        # Barchart typically has tabs or dropdowns for expiration dates
        # Structure varies, so we'll try multiple approaches

        # Approach 1: Look for expiration date selectors/tabs
        expiry_selectors = soup.find_all('option', {'data-ng-repeat': re.compile(r'expiration')})
        if not expiry_selectors:
            expiry_selectors = soup.find_all('a', class_=re.compile(r'expir'))

        # Approach 2: If no clear selectors, look for tables with expiration dates
        if not expiry_selectors:
            # Default: assume single expiration shown (most recent)
            expiry_selectors = [{'value': 'default'}]

        # Process up to max_expiries
        for i, expiry_elem in enumerate(expiry_selectors[:max_expiries]):
            # Extract expiration date from element
            expiry_date = _parse_expiry_date(expiry_elem)

            # Extract calls and puts tables for this expiration
            calls_data = _extract_options_table(soup, 'call', expiry_date, i)
            puts_data = _extract_options_table(soup, 'put', expiry_date, i)

            if calls_data or puts_data:
                days_to_expiry = _calculate_days_to_expiry(expiry_date)

                expirations.append({
                    'date': expiry_date,
                    'days_to_expiry': days_to_expiry,
                    'calls': calls_data,
                    'puts': puts_data
                })

    except Exception as e:
        log_scraper_event('barchart_options', f"Error extracting expirations: {e}", 'ERROR')

    return expirations


def _parse_expiry_date(elem) -> str:
    """
    Parse expiration date from HTML element.

    Args:
        elem: HTML element (BeautifulSoup tag)

    Returns:
        Date string in YYYY-MM-DD format
    """
    try:
        if isinstance(elem, dict):
            # Default case
            # Return nearest Friday (typical options expiry)
            today = datetime.now()
            days_ahead = 4 - today.weekday()  # Friday = 4
            if days_ahead <= 0:
                days_ahead += 7
            next_friday = today + timedelta(days=days_ahead)
            return next_friday.strftime('%Y-%m-%d')

        # Extract from element text or attribute
        text = elem.text.strip() if hasattr(elem, 'text') else str(elem.get('value', ''))

        # Try to parse date formats like "Oct 30 2025", "10/30/2025", etc.
        # Common patterns
        date_patterns = [
            r'(\w{3})\s+(\d{1,2})\s+(\d{4})',  # Oct 30 2025
            r'(\d{1,2})/(\d{1,2})/(\d{4})',     # 10/30/2025
            r'(\d{4})-(\d{2})-(\d{2})',         # 2025-10-30
        ]

        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                # Parse based on pattern (simplified, expand as needed)
                if '-' in match.group(0):
                    return match.group(0)  # Already YYYY-MM-DD
                else:
                    # Convert to datetime and format
                    # This is simplified - in production, use dateutil.parser
                    pass

    except Exception as e:
        log_scraper_event('barchart_options', f"Error parsing expiry date: {e}", 'WARNING')

    # Fallback: return next Friday
    today = datetime.now()
    days_ahead = 4 - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    next_friday = today + timedelta(days=days_ahead)
    return next_friday.strftime('%Y-%m-%d')


def _calculate_days_to_expiry(expiry_date: str) -> int:
    """
    Calculate days until expiration.

    Args:
        expiry_date: Date string in YYYY-MM-DD format

    Returns:
        Number of days until expiry
    """
    try:
        expiry = datetime.strptime(expiry_date, '%Y-%m-%d')
        today = datetime.now()
        delta = expiry - today
        return max(0, delta.days)
    except:
        return 0


def _extract_options_table(soup, option_type: str, expiry_date: str, table_index: int = 0) -> List[Dict]:
    """
    Extract options data from Barchart table (calls or puts).

    Args:
        soup: BeautifulSoup object
        option_type: 'call' or 'put'
        expiry_date: Expiration date string
        table_index: Which table to extract (for multiple expiries)

    Returns:
        List of option contract dictionaries
    """
    contracts = []

    try:
        # Find options table
        # Barchart typically has separate tables or sections for calls and puts
        # Common patterns:
        # - <table class="options-table" data-option-type="call">
        # - <div id="calls-table">
        # - Tables with specific headers

        # Strategy: Find all tables, identify by headers
        tables = soup.find_all('table', class_=re.compile(r'options|quotes|barchart'))

        for table in tables:
            # Check if this is the right table by headers
            headers = table.find_all('th')
            if not headers:
                continue

            header_text = ' '.join([h.text.strip().lower() for h in headers])

            # Determine if this is calls or puts table
            is_calls = 'call' in header_text or 'calls' in header_text
            is_puts = 'put' in header_text or 'puts' in header_text

            # Skip if doesn't match requested type
            if option_type == 'call' and not is_calls:
                continue
            if option_type == 'put' and not is_puts:
                continue

            # Extract rows
            rows = table.find_all('tr')

            for row in rows[1:]:  # Skip header row
                cells = row.find_all('td')

                if len(cells) < 6:  # Need at least strike, last, volume, OI
                    continue

                try:
                    # Common column order (varies by site version):
                    # Strike, Last, Change, %Change, Bid, Ask, Volume, Open Interest, IV
                    # OR: Strike, Last, Bid, Ask, Volume, OI, IV

                    # Flexible parsing based on cell count
                    contract = _parse_option_row(cells)

                    if contract and contract.get('strike', 0) > 0:
                        contracts.append(contract)

                except Exception as e:
                    # Skip invalid rows
                    continue

            # If we found contracts, we're done
            if contracts:
                break

    except Exception as e:
        log_scraper_event('barchart_options', f"Error extracting {option_type} table: {e}", 'WARNING')

    return contracts


def _parse_option_row(cells) -> Optional[Dict]:
    """
    Parse a single option row from Barchart table.

    Args:
        cells: List of table cells (BeautifulSoup tags)

    Returns:
        Dictionary with option data or None if invalid
    """
    try:
        # Extract text from cells
        values = [cell.text.strip() for cell in cells]

        # Flexible parsing based on cell count
        if len(values) < 6:
            return None

        # Common pattern: Strike is usually first or second column
        strike = None
        for i in range(min(2, len(values))):
            parsed = parse_float(values[i], -1)
            if parsed > 0 and parsed < 10000:  # Reasonable strike range
                strike = parsed
                strike_idx = i
                break

        if not strike:
            return None

        # Build contract dict
        # This is a heuristic approach - adjust based on actual Barchart structure
        contract = {
            'strike': strike,
            'last': 0.0,
            'change': 0.0,
            'bid': 0.0,
            'ask': 0.0,
            'volume': 0,
            'open_interest': 0,
            'iv': 0.0
        }

        # Try to identify columns by patterns
        for i, val in enumerate(values):
            if i == strike_idx:
                continue

            parsed_float = parse_float(val, -999)
            parsed_int = parse_int(val, -999)

            # Last price: typically 0.01-1000 range
            if 'last' not in contract or contract['last'] == 0:
                if 0.01 < parsed_float < 1000 and '%' not in val:
                    contract['last'] = parsed_float
                    continue

            # Volume: usually large integer
            if parsed_int > 0 and parsed_int < 10_000_000:
                if contract['volume'] == 0:
                    contract['volume'] = parsed_int
                elif contract['open_interest'] == 0:
                    contract['open_interest'] = parsed_int

            # IV: usually has % sign or is 0-200 range
            if '%' in val or (10 < parsed_float < 200):
                contract['iv'] = parse_float(val.replace('%', ''), 0.0)

        return contract

    except Exception as e:
        return None


def get_unusual_activity(
    ticker: str,
    volume_oi_threshold: float = 2.0,
    min_volume: int = 100
) -> Optional[Dict]:
    """
    Identify unusual options activity for a ticker.

    Args:
        ticker: Stock ticker
        volume_oi_threshold: Minimum volume/OI ratio to flag as unusual
        min_volume: Minimum volume to consider

    Returns:
        Dictionary with:
        {
            'ticker': str,
            'timestamp': str,
            'call_flow_bias': float (calls_volume / puts_volume),
            'unusual_calls': [list of contracts with high vol/OI],
            'unusual_puts': [list of contracts with high vol/OI],
            'total_call_volume': int,
            'total_put_volume': int
        }
    """
    data = scrape_options_chain(ticker)
    if not data:
        return None

    unusual_calls = []
    unusual_puts = []
    total_call_volume = 0
    total_put_volume = 0

    try:
        for expiration in data.get('expirations', []):
            # Process calls
            for call in expiration.get('calls', []):
                volume = call.get('volume', 0)
                oi = call.get('open_interest', 1)  # Avoid division by zero
                total_call_volume += volume

                if volume >= min_volume and oi > 0:
                    vol_oi_ratio = volume / oi
                    if vol_oi_ratio >= volume_oi_threshold:
                        unusual_calls.append({
                            **call,
                            'vol_oi_ratio': vol_oi_ratio,
                            'expiration': expiration['date']
                        })

            # Process puts
            for put in expiration.get('puts', []):
                volume = put.get('volume', 0)
                oi = put.get('open_interest', 1)
                total_put_volume += volume

                if volume >= min_volume and oi > 0:
                    vol_oi_ratio = volume / oi
                    if vol_oi_ratio >= volume_oi_threshold:
                        unusual_puts.append({
                            **put,
                            'vol_oi_ratio': vol_oi_ratio,
                            'expiration': expiration['date']
                        })

        # Calculate flow bias
        call_flow_bias = (total_call_volume / (total_put_volume + 1)) if total_put_volume > 0 else 0

        return {
            'ticker': ticker,
            'timestamp': datetime.now().isoformat(),
            'call_flow_bias': round(call_flow_bias, 2),
            'unusual_calls': sorted(unusual_calls, key=lambda x: x['vol_oi_ratio'], reverse=True),
            'unusual_puts': sorted(unusual_puts, key=lambda x: x['vol_oi_ratio'], reverse=True),
            'total_call_volume': total_call_volume,
            'total_put_volume': total_put_volume
        }

    except Exception as e:
        log_scraper_event('barchart_options', f"Error analyzing unusual activity for {ticker}: {e}", 'ERROR')
        return None


if __name__ == '__main__':
    # Test scraper
    print("Testing Barchart Options Scraper...")
    print("=" * 60)

    test_ticker = 'SPY'
    print(f"\nTesting with {test_ticker}...")

    data = scrape_options_chain(test_ticker, max_expiries=2)

    if data:
        print(f"\n✓ Success!")
        print(f"Stock Price: ${data.get('stock_price', 0):.2f}")
        print(f"Expirations: {len(data.get('expirations', []))}")

        for exp in data.get('expirations', []):
            print(f"\nExpiry: {exp['date']} ({exp['days_to_expiry']} days)")
            print(f"  Calls: {len(exp['calls'])} contracts")
            print(f"  Puts: {len(exp['puts'])} contracts")

            if exp['calls']:
                print(f"  Sample call: Strike ${exp['calls'][0]['strike']}, Last ${exp['calls'][0]['last']:.2f}, Vol {exp['calls'][0]['volume']}")

        # Test unusual activity
        print(f"\n\nTesting unusual activity detection...")
        unusual = get_unusual_activity(test_ticker, volume_oi_threshold=1.5)
        if unusual:
            print(f"Call/Put Flow Bias: {unusual['call_flow_bias']:.2f}")
            print(f"Unusual Calls: {len(unusual['unusual_calls'])}")
            print(f"Unusual Puts: {len(unusual['unusual_puts'])}")
    else:
        print("\n✗ Failed to scrape data")
