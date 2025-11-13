"""
Tests for fetch_market_data.py
================================

Unit tests for API integration script using mocked responses.
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from pathlib import Path
import sys
import os

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from fetch_market_data import MarketDataFetcher


class TestMarketDataFetcherInit:
    """Test MarketDataFetcher initialization"""

    def test_init_valid_date(self):
        """Test initialization with valid date"""
        fetcher = MarketDataFetcher('2025-10-10')
        assert fetcher.date_str == '2025-10-10'
        assert fetcher.date.year == 2025
        assert fetcher.date.month == 10
        assert fetcher.date.day == 10

    def test_init_creates_cache_dir(self):
        """Test cache directory is created"""
        fetcher = MarketDataFetcher('2025-10-10')
        assert fetcher.cache_dir.exists()
        assert fetcher.cache_dir.name == '.cache'


class TestFearGreedAPI:
    """Test Fear & Greed Index API integration"""

    @patch('requests.get')
    def test_fetch_fear_greed_success(self, mock_get):
        """Test successful Fear & Greed fetch"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': [
                {
                    'value': '75',
                    'value_classification': 'Greed'
                }
            ]
        }
        mock_get.return_value = mock_response

        fetcher = MarketDataFetcher('2025-10-10')
        result = fetcher.fetch_fear_greed()

        assert result is not None
        assert result['crypto'] == 75
        assert result['classification'] == 'Greed'
        assert 'timestamp' in result

    @patch('requests.get')
    def test_fetch_fear_greed_api_failure(self, mock_get):
        """Test Fear & Greed API failure handling"""
        mock_get.side_effect = Exception("API Down")

        fetcher = MarketDataFetcher('2025-10-10')
        result = fetcher.fetch_fear_greed()

        assert result is None

    @patch('requests.get')
    def test_fetch_fear_greed_extreme_values(self, mock_get):
        """Test Fear & Greed with extreme values"""
        # Test extreme fear
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': [{'value': '0', 'value_classification': 'Extreme Fear'}]
        }
        mock_get.return_value = mock_response

        fetcher = MarketDataFetcher('2025-10-10')
        result = fetcher.fetch_fear_greed()
        assert result['crypto'] == 0

        # Test extreme greed
        mock_response.json.return_value = {
            'data': [{'value': '100', 'value_classification': 'Extreme Greed'}]
        }
        result = fetcher.fetch_fear_greed()
        assert result['crypto'] == 100


class TestFREDAPI:
    """Test FRED Economic Data API"""

    @patch('requests.get')
    def test_fetch_economic_data_success(self, mock_get):
        """Test successful FRED data fetch"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'observations': [{'value': '3.8', 'date': '2025-09-01'}]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with patch.dict('os.environ', {'FRED_API_KEY': 'test_key'}):
            fetcher = MarketDataFetcher('2025-10-10')
            result = fetcher.fetch_economic_data()

            assert result is not None
            assert 'unemployment' in result
            assert 'cpi' in result
            assert 'fed_funds' in result
            assert 'gdp' in result

    def test_fetch_economic_data_no_api_key(self):
        """Test FRED with missing API key"""
        with patch.dict('os.environ', {}, clear=True):
            fetcher = MarketDataFetcher('2025-10-10')
            result = fetcher.fetch_economic_data()

            assert result is None

    @patch('requests.get')
    def test_fetch_economic_data_missing_value(self, mock_get):
        """Test FRED with missing data point"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'observations': [{'value': '.', 'date': '2025-09-01'}]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with patch.dict('os.environ', {'FRED_API_KEY': 'test_key'}):
            fetcher = MarketDataFetcher('2025-10-10')
            result = fetcher.fetch_economic_data()

            # Should handle missing data gracefully
            assert result is not None
            assert result['unemployment']['value'] is None


class TestCoinGeckoAPI:
    """Test CoinGecko Crypto Prices API"""

    @patch('requests.get')
    def test_fetch_crypto_prices_success(self, mock_get):
        """Test successful crypto price fetch"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'bitcoin': {
                'usd': 62000,
                'usd_24h_change': 2.5,
                'usd_market_cap': 1200000000000,
                'usd_24h_vol': 50000000000
            },
            'ethereum': {
                'usd': 3500,
                'usd_24h_change': -1.2,
                'usd_market_cap': 400000000000,
                'usd_24h_vol': 20000000000
            },
            'solana': {
                'usd': 150,
                'usd_24h_change': 5.8,
                'usd_market_cap': 50000000000,
                'usd_24h_vol': 5000000000
            }
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        fetcher = MarketDataFetcher('2025-10-10')
        result = fetcher.fetch_crypto_prices()

        assert result is not None
        assert 'bitcoin' in result
        assert 'ethereum' in result
        assert 'solana' in result
        assert result['bitcoin']['usd'] == 62000
        assert result['bitcoin']['usd_24h_change'] == 2.5

    @patch('requests.get')
    def test_fetch_crypto_prices_api_failure(self, mock_get):
        """Test crypto price fetch failure"""
        mock_get.side_effect = Exception("Network error")

        fetcher = MarketDataFetcher('2025-10-10')
        result = fetcher.fetch_crypto_prices()

        assert result is None


class TestYahooFinanceAPI:
    """Test Yahoo Finance Stock Indices"""

    @patch('yfinance.Ticker')
    def test_fetch_stock_indices_success(self, mock_ticker):
        """Test successful stock data fetch"""
        # Create mock historical data
        mock_hist = MagicMock()

        # Mock the Close and Volume series
        mock_close = MagicMock()
        mock_close.iloc = MagicMock()
        mock_close.iloc.__getitem__ = MagicMock(side_effect=lambda x: 450.0 if x == -1 else 445.0)

        mock_volume = MagicMock()
        mock_volume.iloc = MagicMock()
        mock_volume.iloc.__getitem__ = MagicMock(return_value=1000000)

        mock_hist.__getitem__ = MagicMock(side_effect=lambda x: mock_close if x == 'Close' else mock_volume)
        mock_hist.__len__ = MagicMock(return_value=5)

        mock_ticker_instance = Mock()
        mock_ticker_instance.history.return_value = mock_hist
        mock_ticker.return_value = mock_ticker_instance

        fetcher = MarketDataFetcher('2025-10-10')
        result = fetcher.fetch_stock_indices()

        assert result is not None
        assert len(result) > 0

    @patch('yfinance.Ticker')
    def test_fetch_stock_indices_insufficient_data(self, mock_ticker):
        """Test stock fetch with insufficient data"""
        mock_hist = MagicMock()
        mock_hist.__len__ = MagicMock(return_value=1)  # Only 1 data point

        mock_ticker_instance = Mock()
        mock_ticker_instance.history.return_value = mock_hist
        mock_ticker.return_value = mock_ticker_instance

        fetcher = MarketDataFetcher('2025-10-10')
        result = fetcher.fetch_stock_indices()

        # Should handle insufficient data gracefully
        assert result is not None


class TestFetchAll:
    """Test complete fetch_all orchestration"""

    @patch.object(MarketDataFetcher, 'fetch_fear_greed')
    @patch.object(MarketDataFetcher, 'fetch_economic_data')
    @patch.object(MarketDataFetcher, 'fetch_crypto_prices')
    @patch.object(MarketDataFetcher, 'fetch_stock_indices')
    def test_fetch_all_success(self, mock_stocks, mock_crypto, mock_econ, mock_fg):
        """Test fetch_all with all APIs successful"""
        mock_fg.return_value = {'crypto': 75, 'classification': 'Greed'}
        mock_econ.return_value = {'unemployment': {'value': 3.8, 'date': '2025-09-01'}}
        mock_crypto.return_value = {'bitcoin': {'usd': 62000}}
        mock_stocks.return_value = {'SPY': {'price': 450}}

        fetcher = MarketDataFetcher('2025-10-10')
        data = fetcher.fetch_all()

        assert data['date'] == '2025-10-10'
        assert 'timestamp' in data
        assert data['fear_greed']['crypto'] == 75
        assert data['economic']['unemployment']['value'] == 3.8
        assert data['crypto']['bitcoin']['usd'] == 62000
        assert data['stocks']['SPY']['price'] == 450

    @patch.object(MarketDataFetcher, 'fetch_fear_greed')
    @patch.object(MarketDataFetcher, 'fetch_economic_data')
    @patch.object(MarketDataFetcher, 'fetch_crypto_prices')
    @patch.object(MarketDataFetcher, 'fetch_stock_indices')
    def test_fetch_all_partial_failure(self, mock_stocks, mock_crypto, mock_econ, mock_fg):
        """Test fetch_all with some APIs failing"""
        mock_fg.return_value = {'crypto': 75}
        mock_econ.return_value = None  # Failed
        mock_crypto.return_value = {'bitcoin': {'usd': 62000}}
        mock_stocks.return_value = None  # Failed

        fetcher = MarketDataFetcher('2025-10-10')
        data = fetcher.fetch_all()

        # Should still complete with partial data
        assert data['fear_greed']['crypto'] == 75
        assert data['economic'] is None
        assert data['crypto']['bitcoin']['usd'] == 62000
        assert data['stocks'] is None


class TestSaveCache:
    """Test JSON cache saving"""

    def test_save_cache_creates_file(self):
        """Test cache file is created"""
        fetcher = MarketDataFetcher('2025-10-10')

        test_data = {
            'date': '2025-10-10',
            'timestamp': datetime.now().isoformat(),
            'fear_greed': {'crypto': 75},
            'crypto': {'bitcoin': {'usd': 62000}},
            'stocks': {},
            'economic': None
        }

        cache_file = fetcher.save_cache(test_data)

        assert cache_file.exists()
        assert cache_file.name == '2025-10-10_market_data.json'

        # Verify JSON is valid
        with open(cache_file) as f:
            loaded_data = json.load(f)

        assert loaded_data['date'] == '2025-10-10'
        assert loaded_data['fear_greed']['crypto'] == 75

    def test_save_cache_overwrites_existing(self):
        """Test cache overwrites existing file"""
        fetcher = MarketDataFetcher('2025-10-10')

        # First save
        data1 = {'date': '2025-10-10', 'fear_greed': {'crypto': 50}}
        fetcher.save_cache(data1)

        # Second save (overwrite)
        data2 = {'date': '2025-10-10', 'fear_greed': {'crypto': 80}}
        cache_file = fetcher.save_cache(data2)

        # Verify new data
        with open(cache_file) as f:
            loaded_data = json.load(f)

        assert loaded_data['fear_greed']['crypto'] == 80


class TestDataValidation:
    """Test data validation and schema"""

    def test_market_data_schema(self):
        """Test market data JSON matches expected schema"""
        from jsonschema import validate

        schema = {
            "type": "object",
            "required": ["date", "timestamp", "fear_greed", "economic", "crypto", "stocks"],
            "properties": {
                "date": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$"},
                "timestamp": {"type": "string"},
                "fear_greed": {
                    "anyOf": [
                        {"type": "null"},
                        {
                            "type": "object",
                            "properties": {
                                "crypto": {"type": "integer", "minimum": 0, "maximum": 100}
                            }
                        }
                    ]
                }
            }
        }

        # Test with valid data
        valid_data = {
            "date": "2025-10-10",
            "timestamp": datetime.now().isoformat(),
            "fear_greed": {"crypto": 75},
            "economic": None,
            "crypto": {},
            "stocks": {}
        }

        # Should not raise ValidationError
        validate(instance=valid_data, schema=schema)

    def test_fear_greed_range(self):
        """Test Fear & Greed is in valid range"""
        fetcher = MarketDataFetcher('2025-10-10')

        # Load actual cached data if exists
        cache_file = fetcher.cache_dir / f"{fetcher.date_str}_market_data.json"

        if cache_file.exists():
            with open(cache_file) as f:
                data = json.load(f)

            if data.get('fear_greed'):
                fg_value = data['fear_greed']['crypto']
                assert 0 <= fg_value <= 100, f"Fear & Greed {fg_value} out of range"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
