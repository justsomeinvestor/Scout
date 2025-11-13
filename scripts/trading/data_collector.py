"""
Data Collector Module: Background daemon for continuous market data collection
- Runs independently every 5 minutes
- Fetches data from Finnhub API
- Calculates technical indicators
- Caches results for decision engine
- Logs all activity
"""

import threading
import time
import json
import logging
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from pathlib import Path
import os

from api_sources import APISourceManager, FinnhubAPI, YahooFinanceScraper
from cache_manager import CacheManager
from ticker_manager import TickerManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/data_collector.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DataCollector:
    """
    Background service that continuously collects and processes market data
    """

    def __init__(self, api_key: str, update_interval: int = 300):
        """
        Initialize data collector

        Args:
            api_key: Finnhub API key
            update_interval: Update interval in seconds (default: 300 = 5 minutes)
        """
        self.api_key = api_key
        self.update_interval = update_interval
        self.running = False
        self.thread = None
        self.last_run = None
        self.next_run = None
        self.error_count = 0
        self.success_count = 0

        # Initialize components
        self.api_manager = APISourceManager(api_key)
        self.cache = CacheManager()
        self.ticker_manager = TickerManager()

        # Status file
        self.status_file = 'data/collector_status.json'
        Path(os.path.dirname(self.status_file)).mkdir(parents=True, exist_ok=True)

        logger.info(f"Data collector initialized (interval: {update_interval}s)")

    def start(self) -> bool:
        """
        Begin background collection loop

        Returns:
            True if started successfully
        """
        if self.running:
            logger.warning("Collector already running")
            return False

        self.running = True
        self.thread = threading.Thread(target=self._collection_loop, daemon=True)
        self.thread.start()

        logger.info("Data collector started")
        self._update_status_file()
        return True

    def stop(self) -> bool:
        """
        Gracefully stop collection

        Returns:
            True if stopped successfully
        """
        if not self.running:
            logger.warning("Collector not running")
            return False

        self.running = False

        # Wait for thread to finish (max 10 seconds)
        if self.thread:
            self.thread.join(timeout=10)

        logger.info("Data collector stopped")
        self._update_status_file()
        return True

    def is_running(self) -> bool:
        """
        Check if service is active

        Returns:
            True if running
        """
        return self.running

    def _collection_loop(self) -> None:
        """
        Main collection loop: runs continuously every update_interval seconds
        """
        logger.info("Collection loop started")

        while self.running:
            try:
                self._fetch_and_process_all()
                self.success_count += 1
                self._update_status_file()

                # Calculate next run time
                self.next_run = datetime.now() + timedelta(seconds=self.update_interval)
                logger.info(f"Collection complete. Next run at {self.next_run.isoformat()}")

                # Sleep until next interval
                time.sleep(self.update_interval)

            except Exception as e:
                logger.error(f"Error in collection loop: {e}", exc_info=True)
                self.error_count += 1
                # Continue running on error, retry after short delay
                time.sleep(5)

        logger.info("Collection loop ended")

    def _fetch_and_process_all(self) -> None:
        """
        Fetch and process data for all tickers in watchlist
        """
        self.last_run = datetime.now()
        watchlist = self.ticker_manager.get_watchlist()

        logger.info(f"Processing {len(watchlist)} tickers")

        for ticker in watchlist:
            try:
                self._fetch_and_process(ticker)
            except Exception as e:
                logger.error(f"Error processing {ticker}: {e}")
                # Continue with next ticker

    def _fetch_and_process(self, ticker: str) -> Optional[Dict]:
        """
        Fetch and process single ticker:
        1. Fetch from API (price, candles)
        2. Calculate indicators (RSI, MACD, OBV, MAs)
        3. Detect support/resistance levels
        4. Cache result

        Args:
            ticker: Stock ticker symbol

        Returns:
            Processed data dict or None on error
        """
        logger.debug(f"Processing {ticker}")

        # Fetch quote
        quote = self.api_manager.get_quote(ticker)
        if quote is None:
            logger.error(f"Failed to fetch quote for {ticker}")
            return None

        # Fetch candles
        candles = self.api_manager.get_candles(ticker, days=100)
        if candles is None or candles.empty:
            logger.error(f"Failed to fetch candles for {ticker}")
            return None

        # Calculate indicators
        indicators = self._calculate_indicators(candles)
        if indicators is None:
            logger.warning(f"Failed to calculate indicators for {ticker}")
            indicators = {}

        # Detect support/resistance
        levels = self._detect_levels(candles)
        if levels is None:
            logger.warning(f"Failed to detect levels for {ticker}")
            levels = {}

        # Build result
        result = {
            'ticker': ticker,
            'timestamp': datetime.now().isoformat(),
            'quote': quote,
            'indicators': indicators,
            'levels': levels,
            'candle_count': len(candles)
        }

        # Cache result
        if self.cache.save(ticker, result):
            logger.info(f"Cached data for {ticker}")
        else:
            logger.error(f"Failed to cache data for {ticker}")

        return result

    def _calculate_indicators(self, candles: pd.DataFrame) -> Optional[Dict]:
        """
        Calculate technical indicators from OHLCV data

        Args:
            candles: DataFrame with OHLCV data

        Returns:
            Dict with indicator values
        """
        if candles is None or candles.empty or len(candles) < 14:
            return None

        try:
            close = candles['close'].values
            volume = candles['volume'].values

            indicators = {}

            # RSI (14-period)
            rsi = self._calculate_rsi(close, period=14)
            if rsi is not None:
                indicators['rsi'] = float(rsi[-1]) if len(rsi) > 0 else None
                indicators['rsi_period'] = 14

            # MACD (12/26/9)
            macd_result = self._calculate_macd(close, fast=12, slow=26, signal=9)
            if macd_result is not None:
                indicators['macd_line'] = float(macd_result['line'][-1]) if len(macd_result['line']) > 0 else None
                indicators['macd_signal'] = float(macd_result['signal'][-1]) if len(macd_result['signal']) > 0 else None
                indicators['macd_histogram'] = float(macd_result['histogram'][-1]) if len(macd_result['histogram']) > 0 else None

            # OBV (On-Balance Volume)
            obv = self._calculate_obv(close, volume)
            if obv is not None:
                indicators['obv'] = float(obv[-1]) if len(obv) > 0 else None

            # Moving Averages (EMA 20, 50, 200)
            ema20 = self._calculate_ema(close, period=20)
            if ema20 is not None:
                indicators['ema_20'] = float(ema20[-1]) if len(ema20) > 0 else None

            ema50 = self._calculate_ema(close, period=50)
            if ema50 is not None:
                indicators['ema_50'] = float(ema50[-1]) if len(ema50) > 0 else None

            ema200 = self._calculate_ema(close, period=200)
            if ema200 is not None:
                indicators['ema_200'] = float(ema200[-1]) if len(ema200) > 0 else None

            # Trend direction
            if ema20 is not None and ema50 is not None and ema200 is not None:
                current_price = close[-1]
                indicators['trend'] = 'UPTREND' if ema20[-1] > ema50[-1] > ema200[-1] else 'DOWNTREND'
                indicators['price'] = float(current_price)

            logger.debug(f"Calculated {len(indicators)} indicators")
            return indicators

        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            return None

    def _detect_levels(self, candles: pd.DataFrame) -> Optional[Dict]:
        """
        Detect support and resistance levels from price data

        Args:
            candles: DataFrame with OHLCV data

        Returns:
            Dict with support/resistance levels
        """
        if candles is None or candles.empty or len(candles) < 20:
            return None

        try:
            high = candles['high'].values
            low = candles['low'].values
            close = candles['close'].values

            levels = {}

            # Find recent peaks (resistance)
            resistance_indices = []
            for i in range(1, len(high) - 1):
                if high[i] > high[i-1] and high[i] > high[i+1]:
                    resistance_indices.append(i)

            if resistance_indices:
                # Get top 2 resistance levels
                top_resistances = sorted(
                    [(high[i], i) for i in resistance_indices[-10:]],
                    key=lambda x: x[0],
                    reverse=True
                )[:2]
                levels['resistance_1'] = float(top_resistances[0][0]) if top_resistances else None
                levels['resistance_2'] = float(top_resistances[1][0]) if len(top_resistances) > 1 else None

            # Find recent troughs (support)
            support_indices = []
            for i in range(1, len(low) - 1):
                if low[i] < low[i-1] and low[i] < low[i+1]:
                    support_indices.append(i)

            if support_indices:
                # Get bottom 2 support levels
                bottom_supports = sorted(
                    [(low[i], i) for i in support_indices[-10:]],
                    key=lambda x: x[0]
                )[:2]
                levels['support_1'] = float(bottom_supports[0][0]) if bottom_supports else None
                levels['support_2'] = float(bottom_supports[1][0]) if len(bottom_supports) > 1 else None

            # Current levels relative to support/resistance
            current_price = close[-1]
            levels['current_price'] = float(current_price)

            logger.debug(f"Detected support/resistance levels")
            return levels

        except Exception as e:
            logger.error(f"Error detecting levels: {e}")
            return None

    @staticmethod
    def _calculate_rsi(prices: np.ndarray, period: int = 14) -> Optional[np.ndarray]:
        """Calculate RSI indicator"""
        if len(prices) < period:
            return None

        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)

        avg_gain = np.convolve(gains, np.ones(period)/period, mode='valid')
        avg_loss = np.convolve(losses, np.ones(period)/period, mode='valid')

        rs = avg_gain / (avg_loss + 1e-10)
        rsi = 100 - (100 / (1 + rs))

        return rsi

    @staticmethod
    def _calculate_macd(prices: np.ndarray, fast: int = 12, slow: int = 26, signal: int = 9) -> Optional[Dict]:
        """Calculate MACD indicator"""
        if len(prices) < slow:
            return None

        ema_fast = np.convolve(prices, np.ones(fast)/fast, mode='valid')
        ema_slow = np.convolve(prices, np.ones(slow)/slow, mode='valid')

        # Align arrays
        min_len = min(len(ema_fast), len(ema_slow))
        macd_line = ema_fast[-min_len:] - ema_slow[-min_len:]

        signal_line = np.convolve(macd_line, np.ones(signal)/signal, mode='valid')
        histogram = macd_line[-len(signal_line):] - signal_line

        return {
            'line': macd_line,
            'signal': signal_line,
            'histogram': histogram
        }

    @staticmethod
    def _calculate_obv(prices: np.ndarray, volumes: np.ndarray) -> Optional[np.ndarray]:
        """Calculate OBV indicator"""
        if len(prices) != len(volumes):
            return None

        obv = np.zeros(len(prices))
        obv[0] = volumes[0]

        for i in range(1, len(prices)):
            if prices[i] > prices[i-1]:
                obv[i] = obv[i-1] + volumes[i]
            elif prices[i] < prices[i-1]:
                obv[i] = obv[i-1] - volumes[i]
            else:
                obv[i] = obv[i-1]

        return obv

    @staticmethod
    def _calculate_ema(prices: np.ndarray, period: int) -> Optional[np.ndarray]:
        """Calculate EMA (Exponential Moving Average)"""
        if len(prices) < period:
            return None

        multiplier = 2 / (period + 1)
        ema = np.zeros(len(prices))
        ema[0] = np.mean(prices[:period])

        for i in range(1, len(prices)):
            ema[i] = (prices[i] * multiplier) + (ema[i-1] * (1 - multiplier))

        return ema

    def _update_status_file(self) -> None:
        """Update status JSON file for frontend"""
        try:
            status = {
                'running': self.running,
                'last_run': self.last_run.isoformat() if self.last_run else None,
                'next_run': self.next_run.isoformat() if self.next_run else None,
                'update_interval': self.update_interval,
                'tickers_tracked': len(self.ticker_manager.get_watchlist()),
                'cache_entries': len(self.cache.get_tickers_in_cache()),
                'success_count': self.success_count,
                'error_count': self.error_count,
                'timestamp': datetime.now().isoformat(),
                'watchlist': self.ticker_manager.get_watchlist(),
                'api_status': self.api_manager.get_api_status()
            }

            with open(self.status_file, 'w') as f:
                json.dump(status, f, indent=2)

        except Exception as e:
            logger.error(f"Error updating status file: {e}")

    def get_status(self) -> Dict:
        """
        Get current collector status

        Returns:
            Dict with status info
        """
        cache_status = self.cache.get_cache_status()

        return {
            'running': self.running,
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'next_run': self.next_run.isoformat() if self.next_run else None,
            'update_interval': self.update_interval,
            'tickers_tracked': len(self.ticker_manager.get_watchlist()),
            'cache_entries': cache_status.get('entries', 0),
            'success_count': self.success_count,
            'error_count': self.error_count,
            'watchlist': self.ticker_manager.get_watchlist(),
            'timestamp': datetime.now().isoformat()
        }


# Global collector instance
_collector_instance = None


def get_collector(api_key: str = None) -> DataCollector:
    """
    Get or create global collector instance

    Args:
        api_key: Finnhub API key (required for first call)

    Returns:
        DataCollector instance
    """
    global _collector_instance

    if _collector_instance is None:
        if api_key is None:
            raise ValueError("API key required for first initialization")
        _collector_instance = DataCollector(api_key)

    return _collector_instance
