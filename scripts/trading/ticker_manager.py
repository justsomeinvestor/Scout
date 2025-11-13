"""
Ticker Manager Module: Manages user watchlist and protected tickers
Data file: data/watchlist.json
Protected tickers: SPY, QQQ (always tracked, cannot be removed)
"""

import json
import logging
from typing import List, Optional
from datetime import datetime
from pathlib import Path
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/ticker_manager.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TickerManager:
    """
    Manages watchlist of stock tickers
    Protected tickers (SPY, QQQ) are always tracked and cannot be removed
    """

    def __init__(self, watchlist_file: str = 'data/watchlist.json'):
        """
        Initialize ticker manager

        Args:
            watchlist_file: Path to watchlist JSON file
        """
        self.watchlist_file = watchlist_file
        self.protected_tickers = ['SPY', 'QQQ']
        self.watchlist = []

        # Create directory if needed
        Path(os.path.dirname(watchlist_file)).mkdir(parents=True, exist_ok=True)

        # Load existing watchlist or create new one
        if not self.load():
            self._create_default_watchlist()

        logger.info(f"Ticker manager initialized with {len(self.watchlist)} tickers")

    def _create_default_watchlist(self) -> None:
        """Create default watchlist with protected tickers"""
        self.watchlist = self.protected_tickers.copy()
        self.save()
        logger.info("Created default watchlist")

    def load(self) -> bool:
        """
        Load watchlist from JSON file

        Returns:
            True if loaded successfully, False otherwise
        """
        if not os.path.exists(self.watchlist_file):
            logger.warning(f"Watchlist file not found: {self.watchlist_file}")
            return False

        try:
            with open(self.watchlist_file, 'r') as f:
                data = json.load(f)

            self.watchlist = data.get('watchlist', [])

            # Ensure protected tickers are in list
            for ticker in self.protected_tickers:
                if ticker not in self.watchlist:
                    self.watchlist.append(ticker)

            logger.info(f"Loaded watchlist with {len(self.watchlist)} tickers")
            return True

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error loading watchlist: {e}")
            return False
        except IOError as e:
            logger.error(f"IO error loading watchlist: {e}")
            return False
        except Exception as e:
            logger.error(f"Error loading watchlist: {e}")
            return False

    def save(self) -> bool:
        """
        Persist watchlist to JSON file

        Returns:
            True if successful
        """
        # Ensure protected tickers are always in watchlist
        for ticker in self.protected_tickers:
            if ticker not in self.watchlist:
                self.watchlist.append(ticker)

        # Remove duplicates and sort
        self.watchlist = sorted(list(set(self.watchlist)))

        try:
            data = {
                'watchlist': self.watchlist,
                'protected': self.protected_tickers,
                'last_updated': datetime.now().isoformat()
            }

            with open(self.watchlist_file, 'w') as f:
                json.dump(data, f, indent=2)

            logger.info(f"Saved watchlist with {len(self.watchlist)} tickers")
            return True

        except IOError as e:
            logger.error(f"IO error saving watchlist: {e}")
            return False
        except Exception as e:
            logger.error(f"Error saving watchlist: {e}")
            return False

    def add_ticker(self, ticker: str) -> bool:
        """
        Add ticker to watchlist

        Args:
            ticker: Stock ticker symbol

        Returns:
            True if added, False if already exists or invalid
        """
        # Validate ticker
        if not self.validate_ticker(ticker):
            logger.warning(f"Invalid ticker format: {ticker}")
            return False

        ticker = ticker.upper()

        # Check if already in list
        if self.is_tracked(ticker):
            logger.warning(f"Ticker already tracked: {ticker}")
            return False

        # Add to list
        self.watchlist.append(ticker)
        success = self.save()

        if success:
            logger.info(f"Added ticker to watchlist: {ticker}")
        else:
            # Remove if save failed
            self.watchlist.remove(ticker)

        return success

    def remove_ticker(self, ticker: str) -> bool:
        """
        Remove ticker from watchlist

        Args:
            ticker: Stock ticker symbol

        Returns:
            True if removed, False if protected or not found
        """
        ticker = ticker.upper()

        # Check if protected
        if ticker in self.protected_tickers:
            logger.warning(f"Cannot remove protected ticker: {ticker}")
            return False

        # Check if exists
        if ticker not in self.watchlist:
            logger.warning(f"Ticker not in watchlist: {ticker}")
            return False

        # Remove
        self.watchlist.remove(ticker)
        success = self.save()

        if success:
            logger.info(f"Removed ticker from watchlist: {ticker}")
        else:
            # Add back if save failed
            self.watchlist.append(ticker)

        return success

    def is_tracked(self, ticker: str) -> bool:
        """
        Check if ticker is in watchlist

        Args:
            ticker: Stock ticker symbol

        Returns:
            True if tracked
        """
        return ticker.upper() in self.watchlist

    def get_watchlist(self) -> List[str]:
        """
        Get current watchlist

        Returns:
            List of tracked tickers (sorted)
        """
        return sorted(self.watchlist)

    def validate_ticker(self, ticker: str) -> bool:
        """
        Validate ticker format

        Criteria:
        - Alphanumeric only (no spaces, special chars)
        - 1-5 characters long
        - Not a duplicate of protected ticker

        Args:
            ticker: Ticker to validate

        Returns:
            True if valid format
        """
        if not ticker or not isinstance(ticker, str):
            return False

        ticker = ticker.upper()

        # Check length
        if len(ticker) < 1 or len(ticker) > 5:
            logger.debug(f"Ticker length invalid: {ticker} (must be 1-5 chars)")
            return False

        # Check alphanumeric only
        if not ticker.isalnum():
            logger.debug(f"Ticker contains non-alphanumeric: {ticker}")
            return False

        # Could check against known exchanges here
        # For now, just basic validation
        return True

    def get_protected_tickers(self) -> List[str]:
        """
        Get list of protected (non-removable) tickers

        Returns:
            List of protected ticker symbols
        """
        return self.protected_tickers.copy()

    def get_custom_tickers(self) -> List[str]:
        """
        Get list of user-added (non-protected) tickers

        Returns:
            List of custom ticker symbols
        """
        custom = [t for t in self.watchlist if t not in self.protected_tickers]
        return sorted(custom)

    def get_status(self) -> dict:
        """
        Get manager status and statistics

        Returns:
            Dict with watchlist info
        """
        return {
            'total_tracked': len(self.watchlist),
            'protected_count': len(self.protected_tickers),
            'custom_count': len(self.get_custom_tickers()),
            'watchlist': self.get_watchlist(),
            'protected': self.get_protected_tickers(),
            'custom': self.get_custom_tickers(),
            'timestamp': datetime.now().isoformat()
        }
