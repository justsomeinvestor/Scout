"""
Tests for calculate_signals.py
================================

Unit tests for signal calculation script.
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from pathlib import Path
import sys

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from calculate_signals import SignalCalculator


@pytest.fixture
def sample_market_data():
    """Sample market data for testing"""
    return {
        "date": "2025-10-10",
        "timestamp": "2025-10-10T12:00:00",
        "fear_greed": {"crypto": 75, "classification": "Greed"},
        "crypto": {
            "bitcoin": {"usd": 62000, "usd_24h_change": 5.0},
            "ethereum": {"usd": 3500, "usd_24h_change": 3.0},
            "solana": {"usd": 150, "usd_24h_change": 4.0}
        },
        "stocks": {
            "SPY": {"price": 450, "change_pct": 1.0},
            "QQQ": {"price": 380, "change_pct": 1.5},
            "^VIX": {"price": 15, "change_pct": -2.0}
        },
        "economic": None
    }


@pytest.fixture
def signal_calculator(tmp_path, sample_market_data):
    """Create signal calculator with test data"""
    # Create test cache directory
    cache_dir = tmp_path / "Research" / ".cache"
    cache_dir.mkdir(parents=True)

    # Save sample market data
    market_data_file = cache_dir / "2025-10-10_market_data.json"
    with open(market_data_file, 'w') as f:
        json.dump(sample_market_data, f)

    # Create calculator
    calculator = SignalCalculator('2025-10-10')
    calculator.cache_dir = cache_dir
    calculator.research_dir = tmp_path / "Research"

    return calculator


class TestSignalCalculatorInit:
    """Test SignalCalculator initialization"""

    def test_init_valid_date(self):
        """Test initialization with valid date"""
        calculator = SignalCalculator('2025-10-10')
        assert calculator.date_str == '2025-10-10'
        assert calculator.date.year == 2025
        assert calculator.date.month == 10

    def test_weights_sum_to_one(self):
        """Test component weights sum to 1.0"""
        calculator = SignalCalculator('2025-10-10')
        total_weight = sum(calculator.WEIGHTS.values())
        assert abs(total_weight - 1.0) < 0.001


class TestTrendScore:
    """Test trend score calculation"""

    def test_trend_score_positive_momentum(self, signal_calculator, sample_market_data):
        """Test trend score with positive momentum"""
        signal_calculator.market_data = sample_market_data
        score = signal_calculator.calculate_trend_score()

        assert 0 <= score <= 40
        assert score > 20  # Positive momentum should score above neutral

    def test_trend_score_negative_momentum(self, signal_calculator):
        """Test trend score with negative momentum"""
        signal_calculator.market_data = {
            "crypto": {
                "bitcoin": {"usd_24h_change": -5.0},
                "ethereum": {"usd_24h_change": -3.0},
                "solana": {"usd_24h_change": -4.0}
            }
        }

        score = signal_calculator.calculate_trend_score()
        assert score < 20  # Negative momentum should score below neutral

    def test_trend_score_no_data(self, signal_calculator):
        """Test trend score with no data"""
        signal_calculator.market_data = None
        score = signal_calculator.calculate_trend_score()

        assert score == 20.0  # Should return neutral (50% of max)


class TestBreadthScore:
    """Test breadth score calculation"""

    def test_breadth_score_all_positive(self, signal_calculator, sample_market_data):
        """Test breadth score with all assets positive"""
        signal_calculator.market_data = sample_market_data
        score = signal_calculator.calculate_breadth_score()

        assert 0 <= score <= 25
        assert score >= 20  # All positive should score high

    def test_breadth_score_mixed(self, signal_calculator):
        """Test breadth score with mixed sentiment"""
        signal_calculator.market_data = {
            "crypto": {
                "bitcoin": {"usd_24h_change": 5.0},
                "ethereum": {"usd_24h_change": -3.0}
            },
            "stocks": {
                "SPY": {"change_pct": 1.0},
                "QQQ": {"change_pct": -0.5}
            }
        }

        score = signal_calculator.calculate_breadth_score()
        assert 10 <= score <= 15  # Mixed should score in middle


class TestVolatilityScore:
    """Test volatility score calculation"""

    def test_volatility_score_low_vix(self, signal_calculator, sample_market_data):
        """Test volatility score with low VIX"""
        signal_calculator.market_data = sample_market_data
        signal_calculator.market_data['stocks']['^VIX']['price'] = 12

        score = signal_calculator.calculate_volatility_score()
        assert score == 20.0  # Low VIX = max score

    def test_volatility_score_high_vix(self, signal_calculator, sample_market_data):
        """Test volatility score with high VIX"""
        signal_calculator.market_data = sample_market_data
        signal_calculator.market_data['stocks']['^VIX']['price'] = 40

        score = signal_calculator.calculate_volatility_score()
        assert score == 0  # High VIX = min score

    def test_volatility_score_medium_vix(self, signal_calculator, sample_market_data):
        """Test volatility score with medium VIX"""
        signal_calculator.market_data = sample_market_data
        signal_calculator.market_data['stocks']['^VIX']['price'] = 20

        score = signal_calculator.calculate_volatility_score()
        assert 5 <= score <= 15  # Medium VIX = medium score


class TestTechnicalScore:
    """Test technical score calculation"""

    def test_technical_score_strong_momentum(self, signal_calculator, sample_market_data):
        """Test technical score with strong momentum"""
        signal_calculator.market_data = sample_market_data
        signal_calculator.market_data['crypto']['bitcoin']['usd_24h_change'] = 8.0

        score = signal_calculator.calculate_technical_score()
        assert score == 10.0  # Strong positive = max score

    def test_technical_score_weak_momentum(self, signal_calculator, sample_market_data):
        """Test technical score with weak momentum"""
        signal_calculator.market_data = sample_market_data
        signal_calculator.market_data['crypto']['bitcoin']['usd_24h_change'] = -6.0

        score = signal_calculator.calculate_technical_score()
        assert score == 0  # Strong negative = min score


class TestSeasonalityScore:
    """Test seasonality score calculation"""

    def test_seasonality_october(self):
        """Test seasonality for October (bullish)"""
        calculator = SignalCalculator('2025-10-15')
        score = calculator.calculate_seasonality_score()

        assert score == 5.0  # October is max bullish

    def test_seasonality_september(self):
        """Test seasonality for September (weakest)"""
        calculator = SignalCalculator('2025-09-15')
        score = calculator.calculate_seasonality_score()

        assert score < 2.0  # September is weakest

    def test_seasonality_range(self):
        """Test seasonality scores are in valid range"""
        for month in range(1, 13):
            date_str = f"2025-{month:02d}-15"
            calculator = SignalCalculator(date_str)
            score = calculator.calculate_seasonality_score()

            assert 0 <= score <= 5.0


class TestContrarianAdjustment:
    """Test contrarian adjustment logic"""

    def test_contrarian_extreme_greed(self, signal_calculator):
        """Test contrarian adjustment with extreme greed"""
        adjustment = signal_calculator.apply_contrarian_adjustment(20.0, 90)
        assert adjustment == -2.0  # Extreme greed reduces breadth

    def test_contrarian_extreme_fear(self, signal_calculator):
        """Test contrarian adjustment with extreme fear"""
        adjustment = signal_calculator.apply_contrarian_adjustment(20.0, 10)
        assert adjustment == 2.0  # Extreme fear increases breadth

    def test_contrarian_neutral(self, signal_calculator):
        """Test contrarian adjustment with neutral sentiment"""
        adjustment = signal_calculator.apply_contrarian_adjustment(20.0, 50)
        assert adjustment == 0.0  # Neutral = no adjustment


class TestXSentimentExtraction:
    """Test X sentiment extraction"""

    def test_extract_x_sentiment_found(self, signal_calculator):
        """Test extracting X sentiment from text"""
        signal_calculator.provider_summaries['x_crypto'] = "Sentiment is 85/100 very bullish"
        sentiment = signal_calculator.extract_x_sentiment('x_crypto')

        assert sentiment == 85

    def test_extract_x_sentiment_not_found(self, signal_calculator):
        """Test extracting X sentiment when pattern not found"""
        signal_calculator.provider_summaries['x_crypto'] = "No clear sentiment score"
        sentiment = signal_calculator.extract_x_sentiment('x_crypto')

        assert sentiment == 50  # Default to neutral

    def test_extract_x_sentiment_missing_summary(self, signal_calculator):
        """Test extracting X sentiment when summary missing"""
        sentiment = signal_calculator.extract_x_sentiment('nonexistent')
        assert sentiment == 50  # Default to neutral


class TestGetTier:
    """Test tier determination"""

    def test_get_tier_extreme(self, signal_calculator):
        """Test EXTREME tier"""
        assert signal_calculator.get_tier(90) == "EXTREME"
        assert signal_calculator.get_tier(85) == "EXTREME"

    def test_get_tier_strong(self, signal_calculator):
        """Test STRONG tier"""
        assert signal_calculator.get_tier(80) == "STRONG"
        assert signal_calculator.get_tier(70) == "STRONG"

    def test_get_tier_moderate(self, signal_calculator):
        """Test MODERATE tier"""
        assert signal_calculator.get_tier(65) == "MODERATE"
        assert signal_calculator.get_tier(55) == "MODERATE"

    def test_get_tier_weak(self, signal_calculator):
        """Test WEAK tier"""
        assert signal_calculator.get_tier(50) == "WEAK"
        assert signal_calculator.get_tier(20) == "WEAK"


class TestCalculateAll:
    """Test complete signal calculation"""

    def test_calculate_all_structure(self, signal_calculator, sample_market_data):
        """Test calculate_all returns correct structure"""
        signal_calculator.market_data = sample_market_data
        signals = signal_calculator.calculate_all()

        # Check required keys
        assert 'date' in signals
        assert 'composite' in signals
        assert 'tier' in signals
        assert 'breakdown' in signals
        assert 'x_sentiment' in signals
        assert 'ai_adjustments' in signals

        # Check breakdown components
        assert 'trend' in signals['breakdown']
        assert 'breadth' in signals['breakdown']
        assert 'volatility' in signals['breakdown']
        assert 'technical' in signals['breakdown']
        assert 'seasonality' in signals['breakdown']

    def test_calculate_all_composite_range(self, signal_calculator, sample_market_data):
        """Test composite score is in valid range"""
        signal_calculator.market_data = sample_market_data
        signals = signal_calculator.calculate_all()

        assert 0 <= signals['composite'] <= 100

    def test_calculate_all_tier_valid(self, signal_calculator, sample_market_data):
        """Test tier is valid"""
        signal_calculator.market_data = sample_market_data
        signals = signal_calculator.calculate_all()

        assert signals['tier'] in ['EXTREME', 'STRONG', 'MODERATE', 'WEAK']


class TestSaveSignals:
    """Test saving signals to JSON"""

    def test_save_signals_creates_file(self, signal_calculator, sample_market_data):
        """Test save_signals creates JSON file"""
        signal_calculator.market_data = sample_market_data
        signals = signal_calculator.calculate_all()

        output_file = signal_calculator.save_signals(signals)

        assert output_file.exists()
        assert output_file.name == "signals_2025-10-10.json"

    def test_save_signals_valid_json(self, signal_calculator, sample_market_data):
        """Test saved signals are valid JSON"""
        signal_calculator.market_data = sample_market_data
        signals = signal_calculator.calculate_all()
        output_file = signal_calculator.save_signals(signals)

        # Load and verify
        with open(output_file) as f:
            loaded_signals = json.load(f)

        assert loaded_signals['date'] == '2025-10-10'
        assert 'composite' in loaded_signals


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
