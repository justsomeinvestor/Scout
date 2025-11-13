"""
Cache Manager Module: Handles JSON caching of market data
TTL: 5 minutes (300 seconds)
Location: data/cache/[TICKER].json
"""

import json
import os
import logging
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/cache_manager.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CacheManager:
    """
    Manages JSON-based caching with TTL (Time To Live)
    """

    def __init__(self, cache_dir: str = 'data/cache'):
        """
        Initialize cache manager

        Args:
            cache_dir: Directory to store cache files
        """
        self.cache_dir = cache_dir
        self.default_ttl = 300  # 5 minutes in seconds

        # Create cache directory if it doesn't exist
        Path(self.cache_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Cache manager initialized with directory: {self.cache_dir}")

    def _get_cache_file(self, ticker: str) -> str:
        """
        Get full path to cache file for ticker

        Args:
            ticker: Stock ticker symbol

        Returns:
            Full file path
        """
        return os.path.join(self.cache_dir, f"{ticker.upper()}.json")

    def save(self, ticker: str, data: Dict) -> bool:
        """
        Save ticker data to cache with timestamp

        Args:
            ticker: Stock ticker symbol
            data: Data to cache (dict)

        Returns:
            True if successful, False otherwise
        """
        if not ticker or not data:
            logger.error(f"Invalid ticker or data for cache save")
            return False

        try:
            # Add metadata
            cache_entry = {
                'ticker': ticker.upper(),
                'timestamp': datetime.now().isoformat(),
                'data': data
            }

            # Write to JSON file
            cache_file = self._get_cache_file(ticker)
            with open(cache_file, 'w') as f:
                json.dump(cache_entry, f, indent=2)

            logger.info(f"Saved cache for {ticker}")
            return True

        except IOError as e:
            logger.error(f"IO error saving cache for {ticker}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error saving cache for {ticker}: {e}")
            return False

    def get(self, ticker: str) -> Optional[Dict]:
        """
        Retrieve ticker data from cache

        Args:
            ticker: Stock ticker symbol

        Returns:
            Data dict if found and not stale, None otherwise
        """
        if not ticker:
            logger.error("Invalid ticker for cache get")
            return None

        cache_file = self._get_cache_file(ticker)

        # Check if file exists
        if not os.path.exists(cache_file):
            logger.debug(f"Cache miss for {ticker} (file not found)")
            return None

        try:
            with open(cache_file, 'r') as f:
                cache_entry = json.load(f)

            # Check if stale
            if self.is_stale(ticker):
                logger.debug(f"Cache stale for {ticker}")
                return None

            logger.info(f"Cache hit for {ticker}")
            return cache_entry.get('data')

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error reading cache for {ticker}: {e}")
            return None
        except IOError as e:
            logger.error(f"IO error reading cache for {ticker}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading cache for {ticker}: {e}")
            return None

    def is_stale(self, ticker: str, ttl: int = None) -> bool:
        """
        Check if cached data is older than TTL

        Args:
            ticker: Stock ticker symbol
            ttl: TTL in seconds (default: 300 = 5 minutes)

        Returns:
            True if stale or not found, False if fresh
        """
        if ttl is None:
            ttl = self.default_ttl

        cache_file = self._get_cache_file(ticker)

        # Not found = stale
        if not os.path.exists(cache_file):
            return True

        try:
            with open(cache_file, 'r') as f:
                cache_entry = json.load(f)

            timestamp_str = cache_entry.get('timestamp')
            if not timestamp_str:
                logger.warning(f"No timestamp in cache for {ticker}")
                return True

            # Parse timestamp
            cache_time = datetime.fromisoformat(timestamp_str)
            current_time = datetime.now()

            # Check age
            age = (current_time - cache_time).total_seconds()
            is_stale = age > ttl

            if is_stale:
                logger.debug(f"Cache for {ticker} is {age:.0f}s old (TTL: {ttl}s)")
            else:
                logger.debug(f"Cache for {ticker} is fresh ({age:.0f}s old)")

            return is_stale

        except Exception as e:
            logger.error(f"Error checking staleness for {ticker}: {e}")
            return True

    def clear(self, ticker: str = None) -> bool:
        """
        Clear cache for specific ticker or all tickers

        Args:
            ticker: Stock ticker to clear, or None to clear all

        Returns:
            True if successful
        """
        try:
            if ticker is None:
                # Clear all cache files
                cache_files = [f for f in os.listdir(self.cache_dir) if f.endswith('.json')]
                for cache_file in cache_files:
                    file_path = os.path.join(self.cache_dir, cache_file)
                    os.remove(file_path)
                    logger.info(f"Cleared cache file: {cache_file}")
                logger.info(f"Cleared all cache ({len(cache_files)} files)")
                return True
            else:
                # Clear specific ticker
                cache_file = self._get_cache_file(ticker)
                if os.path.exists(cache_file):
                    os.remove(cache_file)
                    logger.info(f"Cleared cache for {ticker}")
                return True

        except OSError as e:
            logger.error(f"OS error clearing cache: {e}")
            return False
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False

    def get_all(self) -> Dict[str, Dict]:
        """
        Get all cached data for all tickers

        Returns:
            Dict mapping tickers to their cached data (non-stale only)
        """
        all_data = {}

        try:
            cache_files = [f for f in os.listdir(self.cache_dir) if f.endswith('.json')]

            for cache_file in cache_files:
                ticker = cache_file.replace('.json', '')

                # Get non-stale data only
                data = self.get(ticker)
                if data is not None:
                    all_data[ticker] = data

            logger.info(f"Retrieved cache data for {len(all_data)} tickers")
            return all_data

        except OSError as e:
            logger.error(f"Error listing cache directory: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error getting all cache: {e}")
            return {}

    def get_cache_status(self) -> Dict:
        """
        Get cache statistics and status

        Returns:
            Dict with: entries (count), total_size (bytes), oldest (datetime), newest (datetime)
        """
        try:
            cache_files = [f for f in os.listdir(self.cache_dir) if f.endswith('.json')]

            if not cache_files:
                return {
                    'entries': 0,
                    'total_size': 0,
                    'oldest': None,
                    'newest': None,
                    'timestamp': datetime.now().isoformat()
                }

            total_size = 0
            oldest_time = None
            newest_time = None

            for cache_file in cache_files:
                file_path = os.path.join(self.cache_dir, cache_file)
                total_size += os.path.getsize(file_path)

                # Get timestamps
                with open(file_path, 'r') as f:
                    cache_entry = json.load(f)
                    timestamp_str = cache_entry.get('timestamp')
                    if timestamp_str:
                        cache_time = datetime.fromisoformat(timestamp_str)
                        if oldest_time is None or cache_time < oldest_time:
                            oldest_time = cache_time
                        if newest_time is None or cache_time > newest_time:
                            newest_time = cache_time

            status = {
                'entries': len(cache_files),
                'total_size_bytes': total_size,
                'oldest_entry': oldest_time.isoformat() if oldest_time else None,
                'newest_entry': newest_time.isoformat() if newest_time else None,
                'timestamp': datetime.now().isoformat()
            }

            logger.info(f"Cache status: {status['entries']} entries, {total_size} bytes")
            return status

        except Exception as e:
            logger.error(f"Error getting cache status: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def get_tickers_in_cache(self) -> List[str]:
        """
        Get list of all tickers currently in cache

        Returns:
            List of ticker symbols
        """
        try:
            cache_files = [f for f in os.listdir(self.cache_dir) if f.endswith('.json')]
            tickers = [f.replace('.json', '') for f in cache_files]
            return sorted(tickers)

        except OSError as e:
            logger.error(f"Error listing tickers in cache: {e}")
            return []
