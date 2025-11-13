"""
Scanner scraper utilities.

IMPORTANT: RnD Project
This code is in Research & Development (RnD/Scanner/).
Do not move to production until proven reliable (see README.md).

Adapted from existing scraper infrastructure in /Scraper/.
"""

import re
import sys
import time
import json
import html
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any
import requests
from bs4 import BeautifulSoup

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass  # Fallback for older Python

# ========================================================================
# CONFIGURATION
# ========================================================================

# Paths relative to RnD/Scanner/
SCANNER_ROOT = Path(__file__).parent.parent.parent
DATA_ROOT = SCANNER_ROOT / 'data'
CACHE_ROOT = DATA_ROOT / 'cache'
LOG_ROOT = SCANNER_ROOT / 'logs'

# Create directories
CACHE_ROOT.mkdir(parents=True, exist_ok=True)
LOG_ROOT.mkdir(parents=True, exist_ok=True)

# Regex patterns
TAG_RE = re.compile(r'<[^>]+>')
BR_RE = re.compile(r'<\s*br\s*/?>', re.IGNORECASE)

# Rate limits per scraper (seconds between requests)
RATE_LIMITS = {
    'barchart': 2.0,
    'finviz': 2.0,
    'finviz_screener': 5.0,
    'yahoo': 3.0,
    'marketwatch': 5.0,
    'sec_edgar': 0.1,  # SEC allows 10 req/sec
}

# User agents
USER_AGENTS = {
    'default': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'scanner': 'Trading Scanner Research Tool (Contact: research@example.com)',  # Replace with real contact
}

# ========================================================================
# CORE UTILITIES (Copied from existing scrapers)
# ========================================================================

def sanitize_filename(name: str) -> str:
    """
    Remove invalid filename characters.

    Copied from: /Scraper/rss_scraper.py

    Args:
        name: Original filename

    Returns:
        Sanitized filename safe for all OS
    """
    return re.sub(r'[<>:"/\\|?*]', '_', str(name).strip())


def record_scraper_status(scraper_name: str, items_found: int, error_message: str = None):
    """
    Record scraper execution status for verification.
    FOOLPROOF: Wrapped in try/except - never fails even if write fails.

    Copied from: /Scraper/rss_scraper.py

    Args:
        scraper_name: Name of scraper (e.g., "barchart_options")
        items_found: Number of items found (0 is valid, means no new content)
        error_message: If scraper failed, error description
    """
    try:
        status_dir = LOG_ROOT
        status_dir.mkdir(parents=True, exist_ok=True)

        today = datetime.now().strftime('%Y-%m-%d')
        status_file = status_dir / f'scraper_status_{today}.json'

        # Load existing status or create new
        if status_file.exists():
            try:
                status_data = json.loads(status_file.read_text(encoding='utf-8'))
            except:
                status_data = {}
        else:
            status_data = {}

        # Record this scraper's status
        status_data[scraper_name] = {
            'ran': error_message is None,
            'items_found': items_found if error_message is None else 0,
            'error': error_message,
            'timestamp': datetime.now().isoformat(),
            'message': 'No new content found' if (error_message is None and items_found == 0) else (error_message or 'Scraper completed successfully')
        }

        # Write back
        status_file.write_text(json.dumps(status_data, indent=2), encoding='utf-8')
    except Exception as e:
        # Silent failure - never break the scraper because status write failed
        pass


# ========================================================================
# NEW SCANNER-SPECIFIC UTILITIES
# ========================================================================

def rate_limit_delay(scraper_name: str, override: Optional[float] = None):
    """
    Enforce rate limiting between scraper requests.

    Args:
        scraper_name: Name of scraper (must be in RATE_LIMITS)
        override: Optional override delay in seconds
    """
    delay = override or RATE_LIMITS.get(scraper_name, 2.0)
    time.sleep(delay)


def scrape_with_retry(
    url: str,
    max_retries: int = 3,
    delay: float = 2.0,
    timeout: int = 10,
    headers: Optional[Dict] = None,
    user_agent: str = 'default'
) -> Optional[requests.Response]:
    """
    Scrape URL with exponential backoff retry logic.

    Args:
        url: URL to scrape
        max_retries: Maximum number of retry attempts
        delay: Base delay between retries (exponentially increases)
        timeout: Request timeout in seconds
        headers: Optional custom headers
        user_agent: User agent key from USER_AGENTS dict

    Returns:
        Response object if successful, None if all retries failed
    """
    if headers is None:
        headers = {}

    # Add user agent
    if 'User-Agent' not in headers:
        headers['User-Agent'] = USER_AGENTS.get(user_agent, USER_AGENTS['default'])

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)

            if response.status_code == 200:
                return response
            elif response.status_code == 429:  # Rate limited
                wait_time = delay * (2 ** attempt) * 2  # Extra penalty for rate limits
                print(f"Rate limited on {url}, waiting {wait_time}s...")
                time.sleep(wait_time)
            elif response.status_code in [500, 502, 503, 504]:  # Server errors
                wait_time = delay * (2 ** attempt)
                print(f"Server error {response.status_code} on {url}, retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                # Other errors (404, 403, etc.) - don't retry
                print(f"Non-retryable error {response.status_code} on {url}")
                return None

        except requests.exceptions.Timeout:
            print(f"Timeout on {url}, attempt {attempt + 1}/{max_retries}")
            if attempt < max_retries - 1:
                time.sleep(delay * (2 ** attempt))
        except requests.exceptions.RequestException as e:
            print(f"Request exception on {url}: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay * (2 ** attempt))
        except Exception as e:
            print(f"Unexpected error on {url}: {e}")
            if attempt == max_retries - 1:
                raise

    return None


def clean_html_text(html_text: str) -> str:
    """
    Clean HTML text - remove tags, decode entities, normalize whitespace.

    Args:
        html_text: Raw HTML text

    Returns:
        Cleaned plain text
    """
    if not html_text:
        return ''

    # Replace <br> with newlines before removing tags
    text = BR_RE.sub('\n', html_text)

    # Remove all HTML tags
    text = TAG_RE.sub('', text)

    # Decode HTML entities
    text = html.unescape(text)

    # Normalize whitespace
    text = ' '.join(text.split())

    return text.strip()


def parse_float(value: Any, default: float = 0.0) -> float:
    """
    Safely parse float from string (handles K/M/B suffixes, commas, percentages).

    Examples:
        "1.5K" -> 1500.0
        "2.3M" -> 2300000.0
        "5.2B" -> 5200000000.0
        "12.5%" -> 12.5
        "1,234.56" -> 1234.56

    Args:
        value: Value to parse (string or number)
        default: Default value if parsing fails

    Returns:
        Parsed float value
    """
    if value is None or value == '' or value == 'N/A' or value == '-':
        return default

    # If already a number, return it
    if isinstance(value, (int, float)):
        return float(value)

    # Clean string
    value = str(value).strip().upper()

    # Remove commas
    value = value.replace(',', '')

    # Handle percentages
    is_percentage = '%' in value
    value = value.replace('%', '')

    # Handle K/M/B suffixes
    multiplier = 1.0
    if value.endswith('K'):
        multiplier = 1_000
        value = value[:-1]
    elif value.endswith('M'):
        multiplier = 1_000_000
        value = value[:-1]
    elif value.endswith('B'):
        multiplier = 1_000_000_000
        value = value[:-1]
    elif value.endswith('T'):
        multiplier = 1_000_000_000_000
        value = value[:-1]

    try:
        result = float(value) * multiplier
        return result
    except (ValueError, TypeError):
        return default


def parse_int(value: Any, default: int = 0) -> int:
    """
    Safely parse integer from string (handles commas, K/M/B suffixes).

    Args:
        value: Value to parse
        default: Default value if parsing fails

    Returns:
        Parsed integer value
    """
    return int(parse_float(value, float(default)))


def get_cache_path(scraper_name: str, ticker: str, date: Optional[datetime] = None) -> Path:
    """
    Get standardized cache file path for scraped data.

    Args:
        scraper_name: Name of scraper
        ticker: Stock ticker
        date: Optional date (defaults to today)

    Returns:
        Path to cache file
    """
    if date is None:
        date = datetime.now()

    date_str = date.strftime('%Y-%m-%d')
    cache_dir = CACHE_ROOT / scraper_name
    cache_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{ticker}_{date_str}.json"
    return cache_dir / filename


def load_from_cache(scraper_name: str, ticker: str, max_age_seconds: int = 86400) -> Optional[Dict]:
    """
    Load data from cache if it exists and is fresh.

    Args:
        scraper_name: Name of scraper
        ticker: Stock ticker
        max_age_seconds: Maximum age of cache in seconds (default 24 hours)

    Returns:
        Cached data dict if found and fresh, None otherwise
    """
    cache_path = get_cache_path(scraper_name, ticker)

    if not cache_path.exists():
        return None

    # Check age
    file_age = time.time() - cache_path.stat().st_mtime
    if file_age > max_age_seconds:
        return None

    try:
        data = json.loads(cache_path.read_text(encoding='utf-8'))
        return data
    except Exception as e:
        print(f"Error loading cache for {ticker}: {e}")
        return None


def save_to_cache(scraper_name: str, ticker: str, data: Dict):
    """
    Save data to cache.

    Args:
        scraper_name: Name of scraper
        ticker: Stock ticker
        data: Data to cache (must be JSON-serializable)
    """
    try:
        cache_path = get_cache_path(scraper_name, ticker)
        cache_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
    except Exception as e:
        print(f"Error saving cache for {ticker}: {e}")


def parse_soup(html: str, parser: str = 'html.parser') -> Optional[BeautifulSoup]:
    """
    Parse HTML into BeautifulSoup object with error handling.

    Args:
        html: HTML string
        parser: Parser to use ('html.parser', 'lxml', 'html5lib')

    Returns:
        BeautifulSoup object or None if parsing failed
    """
    try:
        return BeautifulSoup(html, parser)
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return None


# ========================================================================
# DATA VALIDATION
# ========================================================================

def validate_ticker(ticker: str) -> bool:
    """
    Validate ticker symbol format.

    Args:
        ticker: Ticker symbol to validate

    Returns:
        True if valid ticker format
    """
    if not ticker or not isinstance(ticker, str):
        return False

    ticker = ticker.strip().upper()

    # Basic validation: 1-5 alphanumeric characters
    if not re.match(r'^[A-Z]{1,5}$', ticker):
        return False

    return True


def validate_scraped_data(data: Dict, required_fields: list) -> bool:
    """
    Validate that scraped data contains required fields.

    Args:
        data: Scraped data dictionary
        required_fields: List of required field names

    Returns:
        True if all required fields present and non-empty
    """
    if not isinstance(data, dict):
        return False

    for field in required_fields:
        if field not in data or data[field] is None or data[field] == '':
            return False

    return True


# ========================================================================
# LOGGING
# ========================================================================

def log_scraper_event(scraper_name: str, message: str, level: str = 'INFO'):
    """
    Log scraper event with timestamp.

    Args:
        scraper_name: Name of scraper
        message: Log message
        level: Log level (INFO, WARNING, ERROR)
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] [{level}] [{scraper_name}] {message}"

    print(log_message)

    # Also write to log file
    try:
        log_file = LOG_ROOT / f"{scraper_name}_{datetime.now().strftime('%Y-%m-%d')}.log"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    except Exception:
        pass  # Silent failure for logging


# ========================================================================
# TESTING UTILITIES
# ========================================================================

def test_scraper_single(scraper_func, ticker: str, **kwargs):
    """
    Test a scraper function on a single ticker with error handling.

    Args:
        scraper_func: Scraper function to test
        ticker: Ticker symbol
        **kwargs: Additional arguments to pass to scraper

    Returns:
        Scraped data or None if failed
    """
    print(f"\n{'='*60}")
    print(f"Testing {scraper_func.__name__} for {ticker}")
    print(f"{'='*60}")

    try:
        start_time = time.time()
        data = scraper_func(ticker, **kwargs)
        elapsed = time.time() - start_time

        if data:
            print(f"✓ Success! Scraped in {elapsed:.2f}s")
            print(f"Data keys: {list(data.keys())}")
            return data
        else:
            print(f"✗ Failed - no data returned")
            return None

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == '__main__':
    # Test utilities
    print("Testing scraper utilities...")

    # Test filename sanitization
    assert sanitize_filename('SPY/AAPL:test') == 'SPY_AAPL_test'
    print("✓ sanitize_filename works")

    # Test parse_float
    assert parse_float('1.5K') == 1500.0
    assert parse_float('2.3M') == 2300000.0
    assert parse_float('5.2B') == 5200000000.0
    assert parse_float('12.5%') == 12.5
    assert parse_float('1,234.56') == 1234.56
    print("✓ parse_float works")

    # Test ticker validation
    assert validate_ticker('AAPL') == True
    assert validate_ticker('SPY') == True
    assert validate_ticker('INVALID123') == False
    print("✓ validate_ticker works")

    print("\nAll utility tests passed!")
