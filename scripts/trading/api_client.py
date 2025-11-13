"""
Market Data API Client

Wrapper for the ETF Data Scraper & API system running on remote server.
Provides clean interface to all API endpoints with error handling and retries.
"""

import requests
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "scout"))  # Add scout/ for config

from config import config


class APIClientError(Exception):
    """Custom exception for API client errors"""
    pass


class MarketDataAPI:
    """
    Client for Market Data API Server

    Provides methods for:
    - ETF data (SPY, QQQ, VIX)
    - Max Pain options data
    - Chat messages from wallstreet.io
    - RSS feed articles (with Ollama summaries planned)
    - YouTube transcripts (with Ollama summaries)
    - System health and status
    - Data export and backups
    """

    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        """
        Initialize API client

        Args:
            base_url: API server URL (defaults to config)
            timeout: Request timeout in seconds (defaults to config)
        """
        self.base_url = base_url or config.api.base_url
        self.timeout = timeout or config.api.timeout
        self.retry_attempts = config.api.retry_attempts
        self.retry_delay = config.api.retry_delay

        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Investment-Research-Dashboard/1.0'
        })

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """
        Make HTTP request with retry logic

        Args:
            method: HTTP method (GET, POST)
            endpoint: API endpoint path
            **kwargs: Additional arguments for requests

        Returns:
            Response JSON as dictionary

        Raises:
            APIClientError: If request fails after retries
        """
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault('timeout', self.timeout)

        last_error = None
        for attempt in range(self.retry_attempts):
            try:
                if config.debug_mode:
                    print(f"API Request: {method} {url} (attempt {attempt + 1})")

                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()

                return response.json()

            except requests.exceptions.HTTPError as e:
                # Don't retry on 404 - data not found is expected
                if e.response.status_code == 404:
                    raise APIClientError(f"Resource not found: {url}") from e
                last_error = e

            except requests.exceptions.ConnectionError as e:
                last_error = e
                print(f"Connection error (attempt {attempt + 1}/{self.retry_attempts}): {e}")

            except requests.exceptions.Timeout as e:
                last_error = e
                print(f"Request timeout (attempt {attempt + 1}/{self.retry_attempts})")

            except requests.exceptions.RequestException as e:
                last_error = e

            # Wait before retry (except on last attempt)
            if attempt < self.retry_attempts - 1:
                time.sleep(self.retry_delay)

        # All retries failed
        raise APIClientError(f"API request failed after {self.retry_attempts} attempts: {last_error}")

    # ==================== Health & Status ====================

    def health_check(self) -> Dict:
        """
        Basic server health check

        Returns:
            {"status": "ok", "timestamp": "..."}
        """
        return self._make_request('GET', '/health')

    def get_status(self) -> Dict:
        """
        Comprehensive system health with database metrics

        Returns:
            Full system status including:
            - Database connection and size
            - Table statistics (row counts, latest timestamps)
            - Last scrape information
            - Health check results
        """
        return self._make_request('GET', '/api/status')

    def get_summary(self) -> Dict:
        """
        Get ALL latest data from ALL tables in one call

        Perfect for dashboard updates - includes:
        - Latest ETF data (SPY, QQQ)
        - Latest VIX data
        - All max pain expirations
        - Recent chat messages
        - System status

        Returns:
            Complete data snapshot with counts
        """
        return self._make_request('GET', '/api/summary')

    def is_healthy(self) -> bool:
        """
        Quick health check

        Returns:
            True if API server is responding, False otherwise
        """
        try:
            result = self.health_check()
            return result.get('status') == 'ok'
        except:
            return False

    # ==================== ETF Data ====================

    def get_latest_all_etf(self) -> Dict:
        """
        Get latest data for all ETF symbols (SPY, QQQ)

        Returns:
            {"success": bool, "count": int, "data": [...]}
        """
        return self._make_request('GET', '/api/latest')

    def get_latest_symbol(self, symbol: str) -> Dict:
        """
        Get latest data for specific symbol

        Args:
            symbol: Stock symbol (SPY, QQQ, VIX) - case insensitive

        Returns:
            {"success": bool, "data": {...}}

        Note: VIX returns different fields than ETF symbols
        """
        return self._make_request('GET', f'/api/latest/{symbol.upper()}')

    def get_spy_data(self) -> Dict:
        """Get latest SPY data"""
        return self.get_latest_symbol('SPY')

    def get_qqq_data(self) -> Dict:
        """Get latest QQQ data"""
        return self.get_latest_symbol('QQQ')

    def get_vix_data(self) -> Dict:
        """Get latest VIX data"""
        return self.get_latest_symbol('VIX')

    def get_historical(self, symbol: str, start_date: Optional[str] = None,
                       end_date: Optional[str] = None) -> Dict:
        """
        Get historical data for a symbol

        Args:
            symbol: Stock symbol (SPY, QQQ, VIX)
            start_date: Start date in YYYY-MM-DD format (optional)
            end_date: End date in YYYY-MM-DD format (optional)

        Returns:
            {"success": bool, "symbol": str, "count": int, "data": [...]}
        """
        params = {}
        if start_date:
            params['start'] = start_date
        if end_date:
            params['end'] = end_date

        return self._make_request('GET', f'/api/historical/{symbol.upper()}', params=params)

    # ==================== Max Pain Data ====================

    def get_maxpain(self, symbol: str) -> Dict:
        """
        Get latest max pain data for ALL expirations (35+ expirations)

        Args:
            symbol: Stock symbol (SPY, QQQ)

        Returns:
            {"success": bool, "symbol": str, "count": int, "data": [...]}
        """
        return self._make_request('GET', f'/api/maxpain/{symbol.upper()}')

    def get_maxpain_weekly(self, symbol: str) -> Dict:
        """
        Get weekly max pain expirations (≤7 days)

        Args:
            symbol: Stock symbol (SPY, QQQ)

        Returns:
            {"success": bool, "symbol": str, "count": int, "data": [...]}
        """
        return self._make_request('GET', f'/api/maxpain/{symbol.upper()}/weekly')

    def get_maxpain_monthly(self, symbol: str) -> Dict:
        """
        Get monthly max pain expirations (~30 days)

        Args:
            symbol: Stock symbol (SPY, QQQ)

        Returns:
            {"success": bool, "symbol": str, "count": int, "data": [...]}
        """
        return self._make_request('GET', f'/api/maxpain/{symbol.upper()}/monthly')

    def get_maxpain_history(self, symbol: str, days: int = 7) -> Dict:
        """
        Get max pain data for the last N days

        Args:
            symbol: Stock symbol (SPY, QQQ)
            days: Number of days of history (default: 7)

        Returns:
            {"success": bool, "symbol": str, "days": int, "count": int, "data": [...]}
        """
        return self._make_request('GET', f'/api/maxpain/{symbol.upper()}/history',
                                   params={'days': days})

    def track_expiration(self, symbol: str, expiration_date: str) -> Dict:
        """
        Track how max pain for a specific expiration changed over time

        Args:
            symbol: Stock symbol (SPY, QQQ)
            expiration_date: Expiration date (e.g., "Nov 12, 2025")

        Returns:
            {"success": bool, "symbol": str, "expirationDate": str, "data": [...]}
        """
        from urllib.parse import quote
        encoded_date = quote(expiration_date)
        return self._make_request('GET', f'/api/maxpain/{symbol.upper()}/expiration/{encoded_date}')

    # ==================== Chat Messages ====================

    def get_chat_latest(self) -> Dict:
        """
        Get all chat messages from most recent scrape

        Returns:
            {"success": bool, "count": int, "data": [...]}
        """
        return self._make_request('GET', '/api/chat/latest')

    def get_chat_by_user(self, username: str, latest_only: bool = False) -> Dict:
        """
        Get chat messages from specific user

        Args:
            username: Username (case sensitive)
            latest_only: If True, only get messages from latest scrape

        Returns:
            {"success": bool, "username": str, "count": int, "data": [...]}
        """
        endpoint = f'/api/chat/user/{username}'
        if latest_only:
            endpoint += '/latest'
        return self._make_request('GET', endpoint)

    def get_chat_history(self, days: int = 7) -> Dict:
        """
        Get chat messages from last N days

        Args:
            days: Number of days of history (default: 7)

        Returns:
            {"success": bool, "days": int, "count": int, "data": [...]}
        """
        return self._make_request('GET', '/api/chat/history', params={'days': days})

    # ==================== RSS Feed Data ====================

    def get_rss_latest(self, limit: int = 100) -> Dict:
        """
        Get latest RSS articles from all providers

        Args:
            limit: Number of articles to return (default: 100)

        Returns:
            {"success": bool, "count": int, "data": [...]}

            Each article includes:
            - id, article_id, provider, feed_name
            - title, link, author
            - content, summary
            - published_date, scraped_at, tags
        """
        return self._make_request('GET', '/api/rss/latest', params={'limit': limit})

    def get_rss_by_provider(self, provider: str) -> Dict:
        """
        Get articles from specific RSS provider

        Args:
            provider: Provider name (e.g., "MarketWatch", "CNBC", "Federal Reserve")

        Returns:
            {"success": bool, "provider": str, "count": int, "data": [...]}
        """
        return self._make_request('GET', f'/api/rss/provider/{provider}')

    def get_rss_stats(self) -> Dict:
        """
        Get RSS feed statistics

        Returns:
            {"success": bool, "totalArticles": int, "totalProviders": int, "providers": [...]}
        """
        return self._make_request('GET', '/api/rss/stats')

    # ==================== YouTube Transcript Data ====================

    def get_youtube_latest(self, limit: int = 100) -> Dict:
        """
        Get latest YouTube video transcripts with Ollama summaries

        Args:
            limit: Number of videos to return (default: 100)

        Returns:
            {"success": bool, "count": int, "data": [...]}

            Each video includes:
            - video_id, channel_name, channel_handle
            - title, url, published_date
            - summary (Ollama-generated, detailed analysis)
            - ollama_model, summary_generated_at
            - scraped_at
        """
        return self._make_request('GET', '/api/youtube/latest', params={'limit': limit})

    def get_youtube_by_channel(self, channel_handle: str) -> Dict:
        """
        Get transcripts from specific YouTube channel

        Args:
            channel_handle: Channel handle (e.g., "@RaoulPal", "@InvestAnswers")

        Returns:
            {"success": bool, "channel": str, "count": int, "data": [...]}
        """
        return self._make_request('GET', f'/api/youtube/channel/{channel_handle}')

    def get_youtube_stats(self) -> Dict:
        """
        Get YouTube transcript statistics

        Returns:
            {"success": bool, "totalTranscripts": int, "totalChannels": int,
             "successfulSummaries": int, "failedSummaries": int, "channels": [...]}
        """
        return self._make_request('GET', '/api/youtube/stats')

    # ==================== Scrape History ====================

    def get_scrape_history(self, limit: int = 10) -> Dict:
        """
        Get recent scrape metadata showing execution history

        Args:
            limit: Number of records to return (default: 10)

        Returns:
            {"success": bool, "count": int, "data": [...]}
        """
        return self._make_request('GET', '/api/history', params={'limit': limit})

    # ==================== Export & Backup ====================

    def export_json(self, include_metadata: bool = True) -> bytes:
        """
        Export all data as JSON file

        Args:
            include_metadata: Include system metadata (default: True)

        Returns:
            JSON file content as bytes
        """
        response = self.session.get(
            f"{self.base_url}/api/export/json",
            params={'metadata': str(include_metadata).lower()},
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.content

    def export_csv(self, table_name: str) -> bytes:
        """
        Export specific table as CSV

        Args:
            table_name: Table to export (etf_data, vix_data, max_pain_data, chat_messages, scrape_metadata)

        Returns:
            CSV file content as bytes
        """
        response = self.session.get(
            f"{self.base_url}/api/export/csv",
            params={'table': table_name},
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.content

    def create_backup(self) -> Dict:
        """
        Create timestamped database backup on server

        Returns:
            {"success": bool, "message": str, "backupPath": str, "timestamp": str}
        """
        return self._make_request('POST', '/api/backup')

    # ==================== Helper Methods ====================

    def is_data_fresh(self, max_age_hours: int = 1) -> bool:
        """
        Check if latest data is fresh (< max_age_hours old)

        Args:
            max_age_hours: Maximum age in hours (default: 1)

        Returns:
            True if data is fresh, False otherwise
        """
        try:
            status = self.get_status()
            if not status.get('success'):
                return False

            last_scrape = status.get('lastScrape', {})
            scrape_time_str = last_scrape.get('timestamp')

            if not scrape_time_str:
                return False

            # Parse timestamp
            scrape_time = datetime.fromisoformat(scrape_time_str.replace('Z', '+00:00'))
            age = datetime.now(scrape_time.tzinfo) - scrape_time

            return age < timedelta(hours=max_age_hours)

        except Exception as e:
            print(f"Error checking data freshness: {e}")
            return False

    def get_data_age_minutes(self) -> Optional[float]:
        """
        Get age of latest data in minutes

        Returns:
            Age in minutes, or None if unavailable
        """
        try:
            status = self.get_status()
            last_scrape = status.get('lastScrape', {})
            scrape_time_str = last_scrape.get('timestamp')

            if not scrape_time_str:
                return None

            scrape_time = datetime.fromisoformat(scrape_time_str.replace('Z', '+00:00'))
            age = datetime.now(scrape_time.tzinfo) - scrape_time

            return age.total_seconds() / 60

        except:
            return None

    def close(self):
        """Close HTTP session"""
        self.session.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# Convenience function for quick access
def get_client() -> MarketDataAPI:
    """Get configured API client instance"""
    return MarketDataAPI()


if __name__ == "__main__":
    # Test the API client
    print("Market Data API Client Test")
    print("=" * 60)

    with get_client() as api:
        # Health check
        print("\n1. Health Check")
        try:
            health = api.health_check()
            print(f"   [OK] Server healthy: {health}")
        except Exception as e:
            print(f"   [FAIL] Health check failed: {e}")
            exit(1)

        # System status
        print("\n2. System Status")
        try:
            status = api.get_status()
            print(f"   Database connected: {status['database']['connected']}")
            print(f"   ETF data rows: {status['tables']['etf_data']['rowCount']}")
            print(f"   VIX data rows: {status['tables']['vix_data']['rowCount']}")
            print(f"   Max pain rows: {status['tables']['max_pain_data']['rowCount']}")
        except Exception as e:
            print(f"   [FAIL] Status check failed: {e}")

        # Data freshness
        print("\n3. Data Freshness")
        try:
            age = api.get_data_age_minutes()
            fresh = api.is_data_fresh(max_age_hours=1)
            print(f"   Data age: {age:.1f} minutes")
            print(f"   Is fresh (<1 hour): {fresh}")
        except Exception as e:
            print(f"   [FAIL] Freshness check failed: {e}")

        # Get SPY data
        print("\n4. SPY Data")
        try:
            spy = api.get_spy_data()
            if spy['success']:
                data = spy['data']
                print(f"   Price: ${data.get('currentPrice', 'N/A')}")
                print(f"   IV: {data.get('impliedVolatility', 'N/A')}%")
                print(f"   Put/Call Ratio: {data.get('putCallOIRatio', 'N/A')}")
        except Exception as e:
            print(f"   [FAIL] SPY data failed: {e}")

        # Get VIX data
        print("\n5. VIX Data")
        try:
            vix = api.get_vix_data()
            if vix['success']:
                data = vix['data']
                print(f"   Current: {data.get('currentPrice', 'N/A')}")
                print(f"   Change: {data.get('change', 'N/A')} ({data.get('changePercent', 'N/A')}%)")
        except Exception as e:
            print(f"   [FAIL] VIX data failed: {e}")

        # Get max pain
        print("\n6. SPY Max Pain (Weekly)")
        try:
            maxpain = api.get_maxpain_weekly('SPY')
            if maxpain['success'] and maxpain['count'] > 0:
                nearest = maxpain['data'][0]
                print(f"   Nearest expiration: {nearest.get('expiration_date')}")
                print(f"   Max pain: ${nearest.get('max_pain_price', 'N/A')}")
                print(f"   Days until expiry: {nearest.get('days_until_expiry', 'N/A')}")
        except Exception as e:
            print(f"   [FAIL] Max pain failed: {e}")

        print("\n" + "=" * 60)
        print("API Client test complete!")
