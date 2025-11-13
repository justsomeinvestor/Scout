# 🧪 Testing & Validation Plan

**Project:** Workflow Automation - API + Scripts + AI
**Purpose:** Comprehensive testing strategy to ensure quality and reliability
**Status:** Planning Phase

---

## 🎯 Testing Philosophy

**Core Principles:**
1. **Test Early, Test Often** - Write tests alongside code
2. **Modular Testing** - Each module tested independently
3. **Integration Testing** - Validate module interactions
4. **Real-World Scenarios** - Test with actual market data
5. **Error Resilience** - Test failure modes and recovery

---

## 📋 Test Coverage Requirements

### Minimum Coverage Targets

| Component | Unit Tests | Integration Tests | E2E Tests | Target Coverage |
|-----------|-----------|-------------------|-----------|-----------------|
| fetch_market_data.py | ✅ Required | ✅ Required | ✅ Required | 85%+ |
| calculate_signals.py | ✅ Required | ✅ Required | ✅ Required | 90%+ |
| update_master_plan.py | ✅ Required | ✅ Required | ✅ Required | 95%+ |
| verify_consistency.py | ✅ Required | ⚪ Optional | ✅ Required | 90%+ |
| run_workflow.py | ⚪ Optional | ✅ Required | ✅ Required | 80%+ |

**Overall Project Target:** 85%+ code coverage

---

## 🔬 Phase 1: API Integration Testing

### Unit Tests

**File:** `tests/test_fetch_market_data.py`

```python
import pytest
from unittest.mock import patch, Mock
from scripts.fetch_market_data import MarketDataFetcher

class TestFearGreedAPI:
    """Test Fear & Greed Index API integration"""

    @patch('requests.get')
    def test_fetch_fear_greed_success(self, mock_get):
        """Test successful Fear & Greed fetch"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': [{'value': '75', 'value_classification': 'Greed'}]
        }
        mock_get.return_value = mock_response

        fetcher = MarketDataFetcher('2025-10-10')
        result = fetcher.fetch_fear_greed()

        assert result['crypto'] == 75
        assert 'timestamp' in result

    @patch('requests.get')
    def test_fetch_fear_greed_api_failure(self, mock_get):
        """Test Fear & Greed API failure handling"""
        mock_get.side_effect = requests.exceptions.RequestException("API Down")

        fetcher = MarketDataFetcher('2025-10-10')
        result = fetcher.fetch_fear_greed()

        assert result is None  # Should return None on failure

class TestFREDAPI:
    """Test FRED Economic Data API"""

    @patch('requests.get')
    def test_fetch_economic_data_success(self, mock_get):
        """Test successful FRED data fetch"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'observations': [{'value': '3.8'}]
        }
        mock_get.return_value = mock_response

        fetcher = MarketDataFetcher('2025-10-10')
        result = fetcher.fetch_economic_data()

        assert 'unemployment' in result
        assert 'cpi' in result
        assert 'fed_funds' in result

    @patch('requests.get')
    def test_fred_rate_limit_handling(self, mock_get):
        """Test FRED rate limit (120/min) handling"""
        mock_response = Mock()
        mock_response.status_code = 429  # Rate limit
        mock_get.return_value = mock_response

        fetcher = MarketDataFetcher('2025-10-10')
        # Should implement exponential backoff
        # Test that it retries after delay

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
                'usd_market_cap': 1200000000000
            }
        }
        mock_get.return_value = mock_response

        fetcher = MarketDataFetcher('2025-10-10')
        result = fetcher.fetch_crypto_prices()

        assert 'bitcoin' in result
        assert result['bitcoin']['usd'] == 62000

class TestYahooFinanceAPI:
    """Test Yahoo Finance Stock Indices"""

    @patch('yfinance.Ticker')
    def test_fetch_stock_indices_success(self, mock_ticker):
        """Test successful stock data fetch"""
        mock_hist = Mock()
        mock_hist.__getitem__ = Mock(side_effect=lambda x: {
            'Close': Mock(iloc=[-1: 450.0, -2: 445.0]),
            'Volume': Mock(iloc=[-1: 1000000])
        }[x])

        mock_ticker.return_value.history.return_value = mock_hist

        fetcher = MarketDataFetcher('2025-10-10')
        result = fetcher.fetch_stock_indices()

        assert 'SPY' in result
        assert 'price' in result['SPY']
        assert 'change_pct' in result['SPY']
```

### Integration Tests

**File:** `tests/integration/test_api_integration.py`

```python
import pytest
from scripts.fetch_market_data import MarketDataFetcher
import json
from pathlib import Path

class TestAPIIntegration:
    """Integration tests for API data fetching"""

    @pytest.mark.integration
    def test_fetch_all_apis(self):
        """Test fetching from all APIs in sequence"""
        fetcher = MarketDataFetcher('2025-10-10')
        data = fetcher.fetch_all()

        # Verify all data sources present
        assert 'fear_greed' in data
        assert 'economic' in data
        assert 'crypto' in data
        assert 'stocks' in data

        # Verify data structure
        assert isinstance(data['fear_greed']['crypto'], int)
        assert 0 <= data['fear_greed']['crypto'] <= 100

    @pytest.mark.integration
    def test_json_cache_creation(self):
        """Test JSON cache file is created correctly"""
        fetcher = MarketDataFetcher('2025-10-10')
        data = fetcher.fetch_all()

        cache_file = Path('Research/.cache/2025-10-10_market_data.json')
        assert cache_file.exists()

        # Verify JSON is valid
        with open(cache_file) as f:
            cached_data = json.load(f)

        assert cached_data == data

    @pytest.mark.integration
    @pytest.mark.slow
    def test_api_rate_limits_respected(self):
        """Test that rate limits are respected"""
        # Run multiple fetches rapidly
        # Verify no 429 errors
        # Verify delays are implemented
```

### End-to-End Tests

**File:** `tests/e2e/test_phase1_e2e.py`

```python
import pytest
import subprocess
from pathlib import Path
import json

class TestPhase1E2E:
    """End-to-end tests for Phase 1"""

    @pytest.mark.e2e
    def test_cli_execution(self):
        """Test running fetch_market_data.py from CLI"""
        result = subprocess.run(
            ['python', 'scripts/fetch_market_data.py', '2025-10-10'],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert 'Market data fetch complete' in result.stdout

    @pytest.mark.e2e
    def test_output_file_created(self):
        """Test output JSON file is created"""
        subprocess.run(
            ['python', 'scripts/fetch_market_data.py', '2025-10-10'],
            check=True
        )

        output_file = Path('Research/.cache/2025-10-10_market_data.json')
        assert output_file.exists()

        # Validate JSON schema
        with open(output_file) as f:
            data = json.load(f)

        required_keys = ['fear_greed', 'economic', 'crypto', 'stocks']
        for key in required_keys:
            assert key in data
```

### Validation Tests

**File:** `tests/validation/test_api_data_schema.py`

```python
import pytest
import json
from jsonschema import validate, ValidationError

# JSON Schema for market_data.json
MARKET_DATA_SCHEMA = {
    "type": "object",
    "required": ["date", "timestamp", "fear_greed", "economic", "crypto", "stocks"],
    "properties": {
        "date": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$"},
        "timestamp": {"type": "string"},
        "fear_greed": {
            "type": "object",
            "required": ["crypto"],
            "properties": {
                "crypto": {"type": "integer", "minimum": 0, "maximum": 100}
            }
        },
        "economic": {
            "type": "object",
            "required": ["unemployment", "cpi", "fed_funds"]
        },
        "crypto": {"type": "object"},
        "stocks": {"type": "object"}
    }
}

class TestMarketDataSchema:
    """Validate market_data.json schema"""

    def test_schema_validation(self):
        """Test market data matches schema"""
        with open('Research/.cache/2025-10-10_market_data.json') as f:
            data = json.load(f)

        # Should not raise ValidationError
        validate(instance=data, schema=MARKET_DATA_SCHEMA)

    def test_fear_greed_range(self):
        """Test Fear & Greed is in valid range"""
        with open('Research/.cache/2025-10-10_market_data.json') as f:
            data = json.load(f)

        fg_value = data['fear_greed']['crypto']
        assert 0 <= fg_value <= 100
```

---

## 📈 Phase 2: Signal Calculation Testing

### Unit Tests

**File:** `tests/test_calculate_signals.py`

```python
import pytest
from scripts.calculate_signals import (
    calculate_trend_score,
    calculate_breadth_score,
    calculate_volatility_score,
    calculate_technical_score,
    calculate_seasonality_score,
    apply_contrarian_adjustment
)

class TestTrendScore:
    """Test trend score calculation"""

    def test_trend_score_range(self):
        """Test trend score is within 0-40 range"""
        score = calculate_trend_score(sample_market_data())
        assert 0 <= score <= 40

    def test_strong_uptrend(self):
        """Test strong uptrend produces high score"""
        data = {
            'ema_12': 100,
            'ema_26': 95,
            'momentum': 'strong'
        }
        score = calculate_trend_score(data)
        assert score >= 30  # Should be high for strong trend

    def test_downtrend(self):
        """Test downtrend produces low score"""
        data = {
            'ema_12': 95,
            'ema_26': 100,
            'momentum': 'weak'
        }
        score = calculate_trend_score(data)
        assert score <= 15  # Should be low for downtrend

class TestBreadthScore:
    """Test breadth score calculation"""

    def test_breadth_score_range(self):
        """Test breadth score is within 0-25 range"""
        score = calculate_breadth_score(sample_market_data())
        assert 0 <= score <= 25

    def test_high_participation(self):
        """Test high market participation produces high score"""
        data = {
            'advance_decline_ratio': 2.5,
            'new_highs': 150,
            'new_lows': 20
        }
        score = calculate_breadth_score(data)
        assert score >= 18

class TestVolatilityScore:
    """Test volatility score calculation"""

    def test_volatility_score_range(self):
        """Test volatility score is within 0-20 range"""
        score = calculate_volatility_score(sample_market_data())
        assert 0 <= score <= 20

    def test_low_vix_high_score(self):
        """Test low VIX produces high score"""
        data = {'VIX': 12}
        score = calculate_volatility_score(data)
        assert score >= 16  # Low vol = high score

    def test_high_vix_low_score(self):
        """Test high VIX produces low score"""
        data = {'VIX': 35}
        score = calculate_volatility_score(data)
        assert score <= 8  # High vol = low score

class TestContrarian Adjustment:
    """Test X sentiment contrarian adjustment"""

    def test_extreme_bullish_reduces_breadth(self):
        """Test extreme X bullishness reduces breadth"""
        breadth = 22
        x_sentiment = 90  # Extreme bullish

        adjusted = apply_contrarian_adjustment(breadth, x_sentiment)
        assert adjusted < breadth  # Should reduce

    def test_extreme_bearish_increases_breadth(self):
        """Test extreme X bearishness increases breadth"""
        breadth = 15
        x_sentiment = 15  # Extreme bearish

        adjusted = apply_contrarian_adjustment(breadth, x_sentiment)
        assert adjusted > breadth  # Should increase

    def test_neutral_no_change(self):
        """Test neutral X sentiment doesn't adjust breadth"""
        breadth = 20
        x_sentiment = 50  # Neutral

        adjusted = apply_contrarian_adjustment(breadth, x_sentiment)
        assert adjusted == breadth  # No change

class TestCompositeScore:
    """Test composite score calculation"""

    def test_composite_calculation(self):
        """Test composite score formula"""
        components = {
            'trend': 32,
            'breadth': 20,
            'volatility': 16,
            'technical': 8,
            'seasonality': 4
        }

        composite = (
            components['trend'] * 0.40 +
            components['breadth'] * 0.25 +
            components['volatility'] * 0.20 +
            components['technical'] * 0.10 +
            components['seasonality'] * 0.05
        )

        assert composite == 80  # 12.8 + 5 + 3.2 + 0.8 + 0.2

    def test_tier_assignment(self):
        """Test tier is assigned correctly"""
        assert get_tier(88) == "EXTREME"
        assert get_tier(75) == "STRONG"
        assert get_tier(60) == "MODERATE"
        assert get_tier(45) == "WEAK"
```

### Integration Tests

**File:** `tests/integration/test_signal_integration.py`

```python
import pytest
from scripts.calculate_signals import SignalCalculator
import json

class TestSignalIntegration:
    """Integration tests for signal calculation"""

    @pytest.mark.integration
    def test_full_signal_calculation(self):
        """Test full signal calculation pipeline"""
        calculator = SignalCalculator('2025-10-10')
        signals = calculator.calculate_all()

        # Verify all components calculated
        assert 'trend' in signals['breakdown']
        assert 'breadth' in signals['breakdown']
        assert 'volatility' in signals['breakdown']
        assert 'technical' in signals['breakdown']
        assert 'seasonality' in signals['breakdown']

        # Verify composite score
        assert 0 <= signals['composite'] <= 100
        assert signals['tier'] in ['EXTREME', 'STRONG', 'MODERATE', 'WEAK']

    @pytest.mark.integration
    def test_loads_market_data(self):
        """Test signal calculator loads market data correctly"""
        calculator = SignalCalculator('2025-10-10')
        calculator.load_data()

        assert calculator.market_data is not None
        assert 'crypto' in calculator.market_data
        assert 'stocks' in calculator.market_data

    @pytest.mark.integration
    def test_saves_signals_json(self):
        """Test signals saved to JSON correctly"""
        calculator = SignalCalculator('2025-10-10')
        signals = calculator.calculate_all()
        calculator.save_signals(signals)

        output_file = Path('Research/.cache/signals_2025-10-10.json')
        assert output_file.exists()

        with open(output_file) as f:
            saved_signals = json.load(f)

        assert saved_signals == signals
```

### Validation Tests

**File:** `tests/validation/test_signals_schema.py`

```python
import pytest
import json
from jsonschema import validate

SIGNALS_SCHEMA = {
    "type": "object",
    "required": ["date", "composite", "tier", "breakdown"],
    "properties": {
        "date": {"type": "string"},
        "composite": {"type": "number", "minimum": 0, "maximum": 100},
        "tier": {"enum": ["EXTREME", "STRONG", "MODERATE", "WEAK"]},
        "breakdown": {
            "type": "object",
            "required": ["trend", "breadth", "volatility", "technical", "seasonality"],
            "properties": {
                "trend": {
                    "type": "object",
                    "required": ["score", "weight", "notes"],
                    "properties": {
                        "score": {"type": "number", "minimum": 0, "maximum": 40},
                        "weight": {"const": 0.40}
                    }
                }
            }
        },
        "ai_adjustments": {"type": "array"}
    }
}

class TestSignalsSchema:
    """Validate signals.json schema"""

    def test_signals_schema_validation(self):
        """Test signals JSON matches schema"""
        with open('Research/.cache/signals_2025-10-10.json') as f:
            signals = json.load(f)

        validate(instance=signals, schema=SIGNALS_SCHEMA)

    def test_weights_sum_to_one(self):
        """Test component weights sum to 1.0"""
        with open('Research/.cache/signals_2025-10-10.json') as f:
            signals = json.load(f)

        total_weight = sum(
            component['weight']
            for component in signals['breakdown'].values()
        )

        assert abs(total_weight - 1.0) < 0.001  # Allow for floating point
```

---

## 🔄 Phase 3: Master Plan Update Testing

### Unit Tests

**File:** `tests/test_update_master_plan.py`

```python
import pytest
from scripts.update_master_plan import MasterPlanUpdater
import re

class TestDateUpdates:
    """Test date update functions"""

    def test_update_page_title(self):
        """Test pageTitle date update"""
        content = '"pageTitle": "Investment Research Dashboard - October 9, 2025"'
        updater = MasterPlanUpdater('2025-10-10')

        updated = updater.update_page_title(content)
        assert 'October 10, 2025' in updated
        assert 'October 9, 2025' not in updated

    def test_update_date_badge(self):
        """Test dateBadge update"""
        content = '"dateBadge": "October 9, 2025"'
        updater = MasterPlanUpdater('2025-10-10')

        updated = updater.update_date_badge(content)
        assert '"dateBadge": "October 10, 2025"' in updated

    def test_update_eagle_eye_header(self):
        """Test EAGLE EYE header update"""
        content = '## 🎯 EAGLE EYE MACRO OVERVIEW (October 9, 2025)'
        updater = MasterPlanUpdater('2025-10-10')

        updated = updater.update_eagle_eye(content)
        assert 'October 10, 2025' in updated

class TestTimestampUpdates:
    """Test timestamp update functions"""

    def test_update_tab_timestamps(self):
        """Test all tab updatedAt timestamps"""
        content = '''
        {"id": "macro", "updatedAt": "2025-10-09T08:00:00Z"}
        {"id": "crypto", "updatedAt": "2025-10-09T08:00:00Z"}
        '''
        updater = MasterPlanUpdater('2025-10-10')

        updated = updater.update_tab_timestamps(content)
        assert '2025-10-10T' in updated
        assert '2025-10-09T' not in updated

    def test_preserves_tab_structure(self):
        """Test tab structure is preserved"""
        content = '{"id": "macro", "name": "Macro", "updatedAt": "2025-10-09T08:00:00Z"}'
        updater = MasterPlanUpdater('2025-10-10')

        updated = updater.update_tab_timestamps(content)
        assert '"id": "macro"' in updated
        assert '"name": "Macro"' in updated

class TestSignalDataUpdates:
    """Test signal data update functions"""

    def test_update_signal_data(self):
        """Test signalData section update"""
        signals = {
            "composite": 81,
            "tier": "STRONG",
            "breakdown": {...}
        }

        updater = MasterPlanUpdater('2025-10-10')
        content = updater.load_master_plan()

        updated = updater.update_signal_data(content, signals)
        assert '"composite": 81' in updated
        assert '"tier": "STRONG"' in updated

    def test_update_sentiment_history(self):
        """Test sentimentHistory array update"""
        signals = {"composite": 81, "tier": "STRONG"}

        updater = MasterPlanUpdater('2025-10-10')
        content = '"sentimentHistory": [{"date": "2025-10-09", "score": 80, "label": "STRONG"}]'

        updated = updater.update_sentiment_history(content, signals)
        assert '2025-10-10' in updated
        assert '2025-10-09' in updated  # Should preserve history

class TestHTMLDashboard:
    """Test HTML dashboard updates"""

    def test_update_html_title(self):
        """Test HTML title update"""
        html = '<title>Investment Research Dashboard - October 9, 2025</title>'
        updater = MasterPlanUpdater('2025-10-10')

        updated = updater.update_html_dashboard(html)
        assert 'October 10, 2025' in updated
        assert '<title>' in updated and '</title>' in updated
```

### Integration Tests

**File:** `tests/integration/test_master_plan_integration.py`

```python
import pytest
from scripts.update_master_plan import MasterPlanUpdater
from pathlib import Path
import shutil

class TestMasterPlanIntegration:
    """Integration tests for master plan updates"""

    @pytest.fixture
    def test_master_plan(self):
        """Create test copy of master plan"""
        source = Path('master-plan/master-plan.md')
        test_copy = Path('tests/fixtures/test-master-plan.md')
        shutil.copy(source, test_copy)
        yield test_copy
        test_copy.unlink()  # Cleanup

    @pytest.mark.integration
    def test_full_master_plan_update(self, test_master_plan):
        """Test full master plan update"""
        updater = MasterPlanUpdater('2025-10-10')
        updater.master_plan_path = test_master_plan

        # Load signals
        signals = load_test_signals()

        # Update
        updater.update_all(signals)

        # Verify
        content = test_master_plan.read_text()
        assert 'October 10, 2025' in content
        assert '2025-10-10' in content

    @pytest.mark.integration
    def test_preserves_content_structure(self, test_master_plan):
        """Test update preserves master plan structure"""
        original = test_master_plan.read_text()

        updater = MasterPlanUpdater('2025-10-10')
        updater.master_plan_path = test_master_plan
        updater.update_all(load_test_signals())

        updated = test_master_plan.read_text()

        # Should have same number of sections
        assert original.count('##') == updated.count('##')
        assert original.count('###') == updated.count('###')
```

### Consistency Verification Tests

**File:** `tests/test_verify_consistency.py`

```python
import pytest
from scripts.verify_consistency import ConsistencyVerifier

class TestConsistencyChecks:
    """Test consistency verification"""

    def test_finds_date_inconsistencies(self):
        """Test detection of inconsistent dates"""
        content = '''
        "pageTitle": "October 10, 2025"
        "dateBadge": "October 9, 2025"
        '''

        verifier = ConsistencyVerifier('2025-10-10')
        issues = verifier.check_dates(content)

        assert len(issues) > 0
        assert 'dateBadge' in str(issues)

    def test_validates_signal_consistency(self):
        """Test signal score consistency check"""
        content = '''
        "composite": 81
        ...
        "composite": 80
        '''

        verifier = ConsistencyVerifier('2025-10-10')
        issues = verifier.check_signal_consistency(content)

        assert len(issues) > 0

    def test_allows_historical_dates(self):
        """Test allows historical dates in sentimentHistory"""
        content = '''
        "sentimentHistory": [
            {"date": "2025-10-09", "score": 80},
            {"date": "2025-10-10", "score": 81}
        ]
        '''

        verifier = ConsistencyVerifier('2025-10-10')
        issues = verifier.check_dates(content)

        # Should not flag historical dates as errors
        historical_issues = [i for i in issues if '2025-10-09' in str(i)]
        assert len(historical_issues) == 0
```

---

## ✅ Phase 4: End-to-End Testing

### Workflow Tests

**File:** `tests/e2e/test_complete_workflow.py`

```python
import pytest
import subprocess
from pathlib import Path
import json

class TestCompleteWorkflow:
    """End-to-end workflow tests"""

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_full_workflow_execution(self):
        """Test complete workflow from start to finish"""
        date = '2025-10-10'

        # Run complete workflow
        result = subprocess.run(
            ['python', 'scripts/run_workflow.py', date],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        assert result.returncode == 0

        # Verify all outputs exist
        assert Path(f'Research/.cache/{date}_market_data.json').exists()
        assert Path(f'Research/.cache/signals_{date}.json').exists()
        assert Path('master-plan/master-plan.md').exists()

    @pytest.mark.e2e
    def test_workflow_with_historical_date(self):
        """Test workflow on historical date"""
        result = subprocess.run(
            ['python', 'scripts/run_workflow.py', '2025-10-09'],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0

    @pytest.mark.e2e
    def test_workflow_error_handling(self):
        """Test workflow handles errors gracefully"""
        # Test with invalid date
        result = subprocess.run(
            ['python', 'scripts/run_workflow.py', 'invalid-date'],
            capture_output=True,
            text=True
        )

        assert result.returncode != 0
        assert 'error' in result.stderr.lower()
```

### Performance Tests

**File:** `tests/performance/test_performance.py`

```python
import pytest
import time
from scripts.run_workflow import WorkflowOrchestrator

class TestPerformance:
    """Performance and benchmark tests"""

    @pytest.mark.performance
    def test_workflow_execution_time(self):
        """Test workflow completes within time target"""
        orchestrator = WorkflowOrchestrator('2025-10-10')

        start_time = time.time()
        orchestrator.run_all()
        end_time = time.time()

        execution_time = end_time - start_time

        # Target: 20-30 minutes (1200-1800 seconds)
        assert execution_time < 1800, f"Workflow took {execution_time}s (>30 min)"

    @pytest.mark.performance
    def test_token_usage(self):
        """Test token usage meets reduction target"""
        # Mock AI calls and count tokens
        # Verify < 102K tokens used
        pass

    @pytest.mark.performance
    def test_api_call_count(self):
        """Test number of API calls is optimized"""
        orchestrator = WorkflowOrchestrator('2025-10-10')

        with patch('requests.get') as mock_get:
            orchestrator.run_all()

            # Should make reasonable number of API calls
            assert mock_get.call_count < 50
```

---

## 🚨 Error Scenario Testing

### API Failure Tests

**File:** `tests/error_scenarios/test_api_failures.py`

```python
import pytest
from unittest.mock import patch
from scripts.fetch_market_data import MarketDataFetcher

class TestAPIFailures:
    """Test handling of API failures"""

    @patch('requests.get')
    def test_fear_greed_timeout(self, mock_get):
        """Test Fear & Greed API timeout handling"""
        mock_get.side_effect = requests.exceptions.Timeout()

        fetcher = MarketDataFetcher('2025-10-10')
        result = fetcher.fetch_fear_greed()

        # Should return None or cached data
        assert result is None or 'crypto' in result

    @patch('requests.get')
    def test_fred_authentication_error(self, mock_get):
        """Test FRED API authentication error"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        fetcher = MarketDataFetcher('2025-10-10')
        result = fetcher.fetch_economic_data()

        # Should log error and return None
        assert result is None

    def test_missing_api_key(self):
        """Test behavior when API key missing"""
        # Temporarily remove API key from env
        with patch.dict('os.environ', {}, clear=True):
            fetcher = MarketDataFetcher('2025-10-10')

            with pytest.raises(ValueError, match="API key"):
                fetcher.fetch_economic_data()
```

### Data Validation Failures

**File:** `tests/error_scenarios/test_data_validation.py`

```python
import pytest
from scripts.calculate_signals import SignalCalculator

class TestDataValidation:
    """Test handling of invalid data"""

    def test_missing_market_data_file(self):
        """Test behavior when market data file missing"""
        calculator = SignalCalculator('2025-01-01')  # Date with no data

        with pytest.raises(FileNotFoundError):
            calculator.load_data()

    def test_malformed_json(self):
        """Test handling of malformed JSON"""
        # Create malformed JSON file
        bad_json = Path('Research/.cache/2025-10-10_market_data.json')
        bad_json.write_text('{"incomplete": }')

        calculator = SignalCalculator('2025-10-10')

        with pytest.raises(json.JSONDecodeError):
            calculator.load_data()

    def test_missing_required_fields(self):
        """Test handling when required fields missing"""
        incomplete_data = {"crypto": {}}  # Missing other fields

        calculator = SignalCalculator('2025-10-10')
        calculator.market_data = incomplete_data

        with pytest.raises(KeyError):
            calculator.calculate_all()
```

---

## 📊 Test Execution Plan

### Pre-Commit Tests (Fast)

Run before every commit:
```bash
pytest tests/ -m "not slow and not integration and not e2e" --maxfail=1
```

Estimated time: < 1 minute

### Pre-Phase Completion Tests

Run before marking phase complete:
```bash
pytest tests/ -m "not e2e" --cov=scripts --cov-report=html
```

Estimated time: 5-10 minutes

### Full Test Suite

Run before final deployment:
```bash
pytest tests/ --cov=scripts --cov-report=html --cov-report=term
```

Estimated time: 15-30 minutes

### Performance Benchmarks

Run weekly during development:
```bash
pytest tests/performance/ -v --benchmark-only
```

---

## 📋 Test Data Requirements

### Fixtures Needed

**File:** `tests/fixtures/sample_data.py`

```python
def sample_market_data():
    """Sample market data for testing"""
    return {
        "date": "2025-10-10",
        "fear_greed": {"crypto": 75},
        "economic": {
            "unemployment": 3.8,
            "cpi": 3.2,
            "fed_funds": 5.25
        },
        "crypto": {
            "bitcoin": {"usd": 62000, "usd_24h_change": 2.5}
        },
        "stocks": {
            "SPY": {"price": 450, "change_pct": 0.5},
            "^VIX": {"price": 15, "change_pct": -2.0}
        }
    }

def sample_signals():
    """Sample signals data for testing"""
    return {
        "date": "2025-10-10",
        "composite": 81,
        "tier": "STRONG",
        "breakdown": {
            "trend": {"score": 32, "weight": 0.40, "notes": "Strong uptrend"},
            "breadth": {"score": 20, "weight": 0.25, "notes": "Improving"},
            "volatility": {"score": 16, "weight": 0.20, "notes": "VIX 15"},
            "technical": {"score": 8, "weight": 0.10, "notes": "Overbought"},
            "seasonality": {"score": 4, "weight": 0.05, "notes": "October bullish"}
        }
    }
```

---

## ✅ Test Completion Criteria

### Phase 1 Testing Complete When:
- [ ] All unit tests passing
- [ ] All API integrations tested
- [ ] Error scenarios covered
- [ ] JSON schema validated
- [ ] 85%+ code coverage

### Phase 2 Testing Complete When:
- [ ] All calculation tests passing
- [ ] Formula validation complete
- [ ] AI review workflow tested
- [ ] Signal schema validated
- [ ] 90%+ code coverage

### Phase 3 Testing Complete When:
- [ ] All update tests passing
- [ ] Consistency verification working
- [ ] Test master plan validated
- [ ] No date inconsistencies
- [ ] 95%+ code coverage

### Phase 4 Testing Complete When:
- [ ] E2E tests passing
- [ ] Performance targets met
- [ ] Error scenarios handled
- [ ] Full workflow validated
- [ ] 85%+ overall coverage

---

**Last Updated:** 2025-10-10
**Status:** Ready for implementation alongside development

---

*Comprehensive testing ensures quality, reliability, and confidence in the automated workflow.*
