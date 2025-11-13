"""
API Sources Module: Handles all data fetching from Finnhub and Yahoo Finance
Primary: Finnhub API (60 calls/min rate limit)
Fallback: Yahoo Finance web scraping
"""

import requests
import json
import logging
from typing import Dict, Optional, List, Tuple
from datetime import datetime, timedelta
import pandas as pd
from bs4 import BeautifulSoup
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/api_sources.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class FinnhubAPI:
    """
    Finnhub API wrapper for market data fetching
    Free tier: 60 API calls per minute
    """

    def __init__(self, api_key: str):
        """
        Initialize Finnhub API client

        Args:
            api_key: Finnhub API key
        """
        self.api_key = api_key
        self.base_url = "https://finnhub.io/api/v1"
        self.call_count = 0
        self.call_reset_time = datetime.now()
        self.rate_limit = 60  # calls per minute
        self.warning_threshold = 55  # warn at 55 calls

    def _check_rate_limit(self) -> None:
        """Check and enforce rate limiting"""
        current_time = datetime.now()

        # Reset counter every minute
        if (current_time - self.call_reset_time).seconds >= 60:
            self.call_count = 0
            self.call_reset_time = current_time

        # Warn if approaching limit
        if self.call_count >= self.warning_threshold:
            logger.warning(f"API calls at {self.call_count}/{self.rate_limit} - approaching rate limit")

        # Enforce hard limit (queue if needed)
        if self.call_count >= self.rate_limit:
            wait_time = 60 - (current_time - self.call_reset_time).seconds
            logger.warning(f"Rate limit hit. Waiting {wait_time}s before next call")
            time.sleep(wait_time)
            self.call_count = 0
            self.call_reset_time = datetime.now()

    def _make_request(self, endpoint: str, params: Dict) -> Optional[Dict]:
        """
        Make API request with error handling

        Args:
            endpoint: API endpoint (without base URL)
            params: Query parameters

        Returns:
            Response JSON or None on error
        """
        self._check_rate_limit()
        self.call_count += 1

        url = f"{self.base_url}/{endpoint}"
        params['token'] = self.api_key

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Check for API errors
            if 'error' in data:
                logger.error(f"API Error: {data.get('error')}")
                return None

            logger.info(f"Successfully fetched {endpoint} for {params.get('symbol', 'unknown')}")
            return data

        except requests.exceptions.Timeout:
            logger.error(f"Timeout fetching {endpoint}")
            return None
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error fetching {endpoint}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return None

    def get_quote(self, ticker: str) -> Optional[Dict]:
        """
        Fetch current quote data for ticker

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dict with keys: price, change, changePercent, volume, bid, ask, timestamp
            or None on error
        """
        if not ticker or not isinstance(ticker, str):
            logger.error(f"Invalid ticker: {ticker}")
            return None

        data = self._make_request("quote", {"symbol": ticker})

        if data is None:
            return None

        try:
            quote = {
                'ticker': ticker,
                'price': data.get('c'),  # current price
                'change': data.get('d'),  # change
                'changePercent': data.get('dp'),  # change percent
                'high': data.get('h'),  # day high
                'low': data.get('l'),  # day low
                'open': data.get('o'),  # open price
                'volume': data.get('v'),  # volume
                'bid': data.get('bid'),  # bid price
                'ask': data.get('ask'),  # ask price
                'timestamp': datetime.now().isoformat()
            }
            return quote
        except Exception as e:
            logger.error(f"Error parsing quote data: {e}")
            return None

    def get_candles(self, ticker: str, days: int = 100, resolution: str = 'D') -> Optional[pd.DataFrame]:
        """
        Fetch OHLCV candle data (time series)

        Args:
            ticker: Stock ticker symbol
            days: Number of days of history
            resolution: 'D' for daily, '4' for 4-hour, '60' for 1-hour

        Returns:
            DataFrame with OHLCV data indexed by timestamp, or None on error
        """
        if not ticker:
            logger.error("Invalid ticker for candles")
            return None

        # Calculate from/to timestamps
        to_timestamp = int(datetime.now().timestamp())
        from_timestamp = int((datetime.now() - timedelta(days=days)).timestamp())

        data = self._make_request("stock/candle", {
            "symbol": ticker,
            "resolution": resolution,
            "from": from_timestamp,
            "to": to_timestamp
        })

        if data is None or 'c' not in data:
            logger.error(f"No candle data returned for {ticker}")
            return None

        try:
            # Build DataFrame from OHLCV arrays
            df = pd.DataFrame({
                'open': data.get('o', []),
                'high': data.get('h', []),
                'low': data.get('l', []),
                'close': data.get('c', []),
                'volume': data.get('v', []),
            })

            # Add timestamp index
            if 't' in data:
                df['timestamp'] = pd.to_datetime(data['t'], unit='s')
                df.set_index('timestamp', inplace=True)

            logger.info(f"Retrieved {len(df)} candles for {ticker}")
            return df
        except Exception as e:
            logger.error(f"Error building candles DataFrame: {e}")
            return None

    def get_vix(self) -> Optional[Dict]:
        """
        Fetch VIX (Volatility Index) data from Finnhub

        VIX measures market volatility/fear level
        Typical range: 10-80 (low volatility to panic)

        Returns:
            Dict with keys: price, change, changePercent, vol_regime, timestamp
            or None on error
        """
        data = self._make_request("quote", {"symbol": "VIX"})

        if data is None:
            logger.warning("VIX data not available from Finnhub, returning None")
            return None

        try:
            vix_value = data.get('c')  # current price
            vix_change = data.get('d')  # change amount
            vix_change_pct = data.get('dp')  # change percent

            # Classify volatility regime based on VIX level
            if vix_value is None:
                return None

            if vix_value < 15:
                vol_regime = 'low'
                vol_classification = 'Complacency'
            elif vix_value < 20:
                vol_regime = 'normal'
                vol_classification = 'Balanced'
            elif vix_value < 30:
                vol_regime = 'elevated'
                vol_classification = 'Elevated Risk'
            else:
                vol_regime = 'high'
                vol_classification = 'High Fear'

            # Handle None values for change/change_pct
            vix_change_safe = vix_change if vix_change is not None else 0
            vix_change_pct_safe = vix_change_pct if vix_change_pct is not None else 0

            vix_data = {
                'vix_current': round(vix_value, 2),
                'vix_change': round(vix_change_safe, 2),
                'vix_change_pct': round(vix_change_pct_safe, 2),
                'vol_regime': vol_regime,
                'vol_classification': vol_classification,
                'source': 'finnhub',
                'timestamp': datetime.now().isoformat()
            }

            logger.info(f"VIX: {vix_value:.2f} ({vix_change_pct_safe:+.2f}%), Regime: {vol_regime.upper()}")
            return vix_data

        except Exception as e:
            logger.error(f"Error parsing VIX data: {e}")
            return None

    def get_technical_indicators(self, ticker: str) -> Optional[Dict]:
        """
        Fetch technical analysis indicators from Finnhub

        Note: Finnhub doesn't provide comprehensive indicators via API
        This will return available data; additional indicators calculated locally

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dict with available technical data
        """
        quote = self.get_quote(ticker)
        candles = self.get_candles(ticker, days=100)

        if quote is None or candles is None or candles.empty:
            return None

        try:
            indicators = {
                'ticker': ticker,
                'price': quote['price'],
                'timestamp': datetime.now().isoformat(),
                'candles': len(candles)
            }

            return indicators
        except Exception as e:
            logger.error(f"Error calculating technical indicators: {e}")
            return None


class YahooFinanceScraper:
    """
    Yahoo Finance web scraper as fallback when Finnhub fails
    Uses BeautifulSoup to parse market data
    """

    def __init__(self):
        """Initialize scraper"""
        self.base_url = "https://finance.yahoo.com/quote"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def scrape_quote(self, ticker: str) -> Optional[Dict]:
        """
        Scrape current quote from Yahoo Finance

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dict with price data or None on error
        """
        if not ticker:
            logger.error("Invalid ticker for scraping")
            return None

        try:
            url = f"{self.base_url}/{ticker}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Yahoo Finance price is in a specific span
            price_span = soup.find('span', {'data-symbol': ticker})
            if price_span:
                price_text = price_span.get_text()
                try:
                    price = float(price_text.replace(',', ''))

                    quote = {
                        'ticker': ticker,
                        'price': price,
                        'source': 'yahoo_scrape',
                        'timestamp': datetime.now().isoformat()
                    }
                    logger.info(f"Scraped quote for {ticker}: ${price}")
                    return quote
                except ValueError:
                    logger.error(f"Could not parse price: {price_text}")
                    return None
            else:
                logger.warning(f"Could not find price element for {ticker}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error scraping {ticker}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error scraping: {e}")
            return None

    def scrape_candles(self, ticker: str, days: int = 100) -> Optional[pd.DataFrame]:
        """
        Scrape historical OHLCV data from Yahoo Finance

        Note: This is limited since Yahoo doesn't provide full history via simple scraping
        For production, consider using yfinance library as fallback

        Args:
            ticker: Stock ticker symbol
            days: Number of days of history

        Returns:
            DataFrame with OHLCV data or None on error
        """
        try:
            # Using yfinance as more reliable fallback for historical data
            import yfinance as yf

            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            data = yf.download(ticker, start=start_date, end=end_date, progress=False)

            if data.empty:
                logger.warning(f"No candle data from yfinance for {ticker}")
                return None

            logger.info(f"Retrieved {len(data)} candles for {ticker} from yfinance")
            return data

        except ImportError:
            logger.warning("yfinance not available, cannot scrape historical data")
            return None
        except Exception as e:
            logger.error(f"Error scraping candles: {e}")
            return None


class APISourceManager:
    """
    Manages API sources with fallback strategy
    Primary: Finnhub
    Fallback: Yahoo Finance scraper
    """

    def __init__(self, finnhub_key: str):
        """
        Initialize API manager

        Args:
            finnhub_key: Finnhub API key
        """
        self.finnhub = FinnhubAPI(finnhub_key)
        self.yahoo = YahooFinanceScraper()
        logger.info("API Source Manager initialized")

    def get_quote(self, ticker: str) -> Optional[Dict]:
        """
        Fetch quote with fallback strategy

        Args:
            ticker: Stock ticker symbol

        Returns:
            Quote data dict or None
        """
        # Try Finnhub first
        quote = self.finnhub.get_quote(ticker)
        if quote is not None:
            quote['source'] = 'finnhub'
            return quote

        logger.warning(f"Finnhub failed for {ticker}, trying Yahoo scraper")

        # Fallback to Yahoo
        quote = self.yahoo.scrape_quote(ticker)
        if quote is not None:
            return quote

        logger.error(f"All sources failed for {ticker}")
        return None

    def get_candles(self, ticker: str, days: int = 100) -> Optional[pd.DataFrame]:
        """
        Fetch candles with fallback strategy

        Args:
            ticker: Stock ticker symbol
            days: Number of days of history

        Returns:
            DataFrame with OHLCV data or None
        """
        # Try Finnhub first
        candles = self.finnhub.get_candles(ticker, days=days)
        if candles is not None and not candles.empty:
            logger.info(f"Candles from Finnhub for {ticker}")
            return candles

        logger.warning(f"Finnhub failed for candles {ticker}, trying Yahoo scraper")

        # Fallback to Yahoo
        candles = self.yahoo.scrape_candles(ticker, days=days)
        if candles is not None and not candles.empty:
            logger.info(f"Candles from Yahoo for {ticker}")
            return candles

        logger.error(f"All sources failed for candles {ticker}")
        return None

    def get_vix(self) -> Optional[Dict]:
        """
        Fetch VIX data from Finnhub API

        Returns:
            Dict with VIX data (current, change, vol_regime) or None
        """
        return self.finnhub.get_vix()

    def get_api_status(self) -> Dict:
        """
        Get current API usage status

        Returns:
            Dict with call count and rate limit info
        """
        return {
            'call_count': self.finnhub.call_count,
            'rate_limit': self.finnhub.rate_limit,
            'next_reset': self.finnhub.call_reset_time.isoformat(),
            'calls_remaining': self.finnhub.rate_limit - self.finnhub.call_count,
            'timestamp': datetime.now().isoformat()
        }
