# 🚀 Workflow Automation: APIs, Scripts, and AI

**Created:** 2025-10-10
**Status:** Approved - Ready for Implementation
**Target:** Practical AI Autonomy for Master Plan Updates
**Estimated Implementation:** 4 weeks

---

## 📋 Executive Summary

**Problem:** The current master plan workflow relies heavily on web searches and manual data extraction, leading to:
- High token consumption (~150K per run)
- Unreliable data from web scraping
- Time-intensive AI operations (30-45 minutes)
- Difficulty achieving full AI autonomy

**Solution:** Modernize with APIs + Scripts + AI hybrid approach:
1. **API Integration** - Replace web searches with reliable API data sources
2. **Scripts for Calculations** - Automate pure math and string operations
3. **AI for Judgment** - Preserve AI review for all important decisions

**Core Principle:**
> **"Scripts for repeatable tasks, AI for dynamic judgment"**
>
> Only automate deterministic operations. AI must review all data and can adjust based on qualitative factors.

**Benefits:**
- ✅ **Reliable Data** - APIs provide structured, consistent data vs. web scraping
- ✅ **Token Efficiency** - 32% reduction (150K → 102K tokens)
- ✅ **Time Savings** - 10-15 minutes faster per run
- ✅ **AI Preserved** - AI still reviews all calculations and makes final decisions
- ✅ **Maintainable** - Clear separation between automation and intelligence

**Token Savings Breakdown:**
- **Before:** ~150K tokens (web searches, data extraction, calculations)
- **After:** ~102K tokens (API integration, AI reviews structured data)
- **Savings:** 48K tokens (32% reduction)

**Cost Analysis:**
- **Tier 1 (Free):** Fear & Greed Index, FRED, CoinGecko, Yahoo Finance - $0/month
- **Tier 2 (Paid):** CoinGlass ($50/mo), Glassnode ($30/mo) - Optional for premium data
- **Total:** Free tier viable, ~$80/month for complete premium setup

---

## 🎯 The Four Scripts Architecture

### 1. **fetch_market_data.py** - API Data Collection

**Purpose:** Replace web searches with reliable API calls

**What It Does:**
- Fetches Fear & Greed Index (CNN API)
- Fetches economic indicators (FRED API)
- Fetches crypto prices and metrics (CoinGecko API)
- Fetches stock indices (Yahoo Finance API)
- Optionally: CoinGlass funding rates, Glassnode on-chain metrics
- Saves structured JSON files for script consumption

**AI Role:** None (pure data fetching)

**Token Impact:** Eliminates 40K tokens from web searches

**Output Files:**
```
Research/.cache/YYYY-MM-DD_fear_greed.json
Research/.cache/YYYY-MM-DD_economic_data.json
Research/.cache/YYYY-MM-DD_crypto_prices.json
Research/.cache/YYYY-MM-DD_stock_indices.json
```

---

### 2. **calculate_signals.py** - Signal Score Calculation

**Purpose:** Calculate signal components from structured data

**What It Does:**
```
Composite Score = (Trend × 0.40) + (Breadth × 0.25) + (Volatility × 0.20) +
                  (Technical × 0.10) + (Seasonality × 0.05)
```

**Calculations (Script performs):**
- Trend Score: EMA crossovers, momentum indicators
- Breadth Score: Advance/decline ratios, market participation
- Volatility Score: VIX levels, historical volatility
- Technical Score: RSI, MACD from structured data
- Seasonality Score: Month-based historical patterns
- X Sentiment Contrarian Adjustment: Apply to breadth

**AI Role (Hybrid Approach):**
1. **Script calculates** - Math operations produce initial scores
2. **AI reviews** - Sees calculations + context (summaries, news, X sentiment)
3. **AI can adjust** - Override scores based on qualitative factors
4. **AI explains** - Documents reasoning for any adjustments

**Token Impact:** Saves 15K tokens (script does math, AI reviews vs. AI does everything)

**Output:**
```json
{
  "date": "2025-10-10",
  "composite": 81,
  "tier": "STRONG",
  "breakdown": {
    "trend": {"score": 32, "weight": 0.40, "notes": "Strong uptrend all timeframes"},
    "breadth": {"score": 20, "weight": 0.25, "adjustment": -2, "notes": "Improving breadth"},
    "volatility": {"score": 16, "weight": 0.20, "notes": "VIX at 17, compressed"},
    "technical": {"score": 8, "weight": 0.10, "notes": "RSI overbought but MACD bullish"},
    "seasonality": {"score": 4, "weight": 0.05, "notes": "October bullish seasonality"}
  },
  "ai_adjustments": [
    {"component": "breadth", "original": 22, "adjusted": 20, "reason": "X sentiment extremely bullish, contrarian reduction"}
  ]
}
```

---

### 3. **update_master_plan.py** - Pure Automation

**Purpose:** Deterministic master plan date and structure updates

**What It Does:**
- Updates pageTitle: "October 9, 2025" → "October 10, 2025"
- Updates dateBadge: Same date transformation
- Updates all tab `updatedAt` timestamps to current date
- Updates EAGLE EYE header date
- Updates footer dates (Last Updated, Next Review)
- Adds sentimentHistory entry from signals JSON
- Updates HTML dashboard title

**AI Role:** None (pure string replacement and date arithmetic)

**Token Impact:** Saves 10K tokens (previously AI read entire file to find dates)

**Inputs:**
- Target date (2025-10-10)
- Signals JSON (for sentiment score)

**Operations:**
- Regex replacements for all date occurrences
- JSON front matter updates
- Timestamp calculations

---

### 4. **verify_consistency.py** - Automated Validation

**Purpose:** Verify all dates and scores are consistent

**What It Does:**
- Scans master-plan.md for all date references
- Verifies pageTitle matches dateBadge
- Checks all tab updatedAt timestamps match target date
- Validates signal score consistency across file
- Checks EAGLE EYE header date
- Verifies footer dates
- Checks HTML dashboard title matches
- Validates sentimentHistory latest entry

**AI Role:** Minimal (reports findings, AI interprets results)

**Token Impact:** Saves 5K tokens (script performs checks, AI only reviews report)

**Output:**
```
✅ All dates consistent: 2025-10-10
✅ All updatedAt timestamps current
✅ Signal score consistent: 81/100 (STRONG)
✅ HTML dashboard matches
⚠️  WARNING: Found historical date in sentimentHistory (expected)
```

---

## 🔌 API Integration Strategy

### Tier 1: Free APIs (Core Data)

#### 1. **Fear & Greed Index**
- **Source:** CNN Business / Alternative.me (Crypto)
- **Endpoint:** `https://api.alternative.me/fng/`
- **Data:** Fear & Greed score (0-100), historical trends
- **Rate Limit:** Unlimited
- **Cost:** Free

#### 2. **FRED Economic Data**
- **Source:** Federal Reserve Economic Data
- **Endpoint:** `https://api.stlouisfed.org/fred/`
- **Data:** Unemployment, inflation, interest rates, GDP
- **Rate Limit:** 120 requests/minute
- **Cost:** Free (requires API key)

#### 3. **CoinGecko Crypto Prices**
- **Source:** CoinGecko
- **Endpoint:** `https://api.coingecko.com/api/v3/`
- **Data:** BTC, ETH, SOL prices, market cap, volume
- **Rate Limit:** 10-50 calls/minute (free tier)
- **Cost:** Free

#### 4. **Yahoo Finance**
- **Source:** yfinance Python library
- **Method:** `yf.download(['SPY', 'QQQ', 'GLD'])`
- **Data:** Stock indices, historical prices, volume
- **Rate Limit:** Reasonable use
- **Cost:** Free

### Tier 2: Paid APIs (Premium Data - Optional)

#### 5. **CoinGlass (Crypto Derivatives)**
- **Source:** CoinGlass
- **Endpoint:** `https://open-api.coinglass.com/`
- **Data:** Funding rates, liquidations, open interest
- **Cost:** ~$50/month (basic plan)
- **Value:** Critical for crypto sentiment

#### 6. **Glassnode (On-Chain Analytics)**
- **Source:** Glassnode
- **Endpoint:** `https://api.glassnode.com/v1/`
- **Data:** On-chain metrics, whale movements, exchange flows
- **Cost:** ~$30/month (starter plan)
- **Value:** Deep on-chain insights

### API Integration Code Structure

```python
# fetch_market_data.py

import requests
from datetime import datetime
import json
from pathlib import Path

class MarketDataFetcher:
    def __init__(self, date_str):
        self.date = datetime.strptime(date_str, "%Y-%m-%d")
        self.cache_dir = Path("Research/.cache")
        self.cache_dir.mkdir(exist_ok=True)

    def fetch_all(self):
        """Fetch all market data from APIs"""
        print(f"📡 Fetching market data for {self.date.strftime('%Y-%m-%d')}")

        data = {
            'fear_greed': self.fetch_fear_greed(),
            'economic': self.fetch_economic_data(),
            'crypto': self.fetch_crypto_prices(),
            'stocks': self.fetch_stock_indices()
        }

        # Optional: Premium data
        if self.has_coinglass_api():
            data['derivatives'] = self.fetch_derivatives_data()

        if self.has_glassnode_api():
            data['onchain'] = self.fetch_onchain_data()

        # Save to cache
        self.save_cache(data)

        return data

    def fetch_fear_greed(self):
        """Fetch Fear & Greed Index"""
        try:
            # Crypto Fear & Greed
            crypto_resp = requests.get("https://api.alternative.me/fng/")
            crypto_fg = crypto_resp.json()['data'][0]['value']

            # Stock Fear & Greed (CNN - may require scraping or alternative)
            # For now, use crypto as proxy or implement later

            return {
                'crypto': int(crypto_fg),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"⚠️  Failed to fetch Fear & Greed: {e}")
            return None

    def fetch_economic_data(self):
        """Fetch economic indicators from FRED"""
        try:
            api_key = os.getenv('FRED_API_KEY')
            base_url = "https://api.stlouisfed.org/fred/series/observations"

            indicators = {
                'unemployment': 'UNRATE',
                'cpi': 'CPIAUCSL',
                'fed_funds': 'DFF'
            }

            data = {}
            for name, series_id in indicators.items():
                params = {
                    'series_id': series_id,
                    'api_key': api_key,
                    'file_type': 'json',
                    'sort_order': 'desc',
                    'limit': 1
                }
                resp = requests.get(base_url, params=params)
                data[name] = resp.json()['observations'][0]['value']

            return data
        except Exception as e:
            print(f"⚠️  Failed to fetch economic data: {e}")
            return None

    def fetch_crypto_prices(self):
        """Fetch crypto prices from CoinGecko"""
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                'ids': 'bitcoin,ethereum,solana',
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_market_cap': 'true'
            }
            resp = requests.get(url, params=params)
            return resp.json()
        except Exception as e:
            print(f"⚠️  Failed to fetch crypto prices: {e}")
            return None

    def fetch_stock_indices(self):
        """Fetch stock indices from Yahoo Finance"""
        try:
            import yfinance as yf

            tickers = ['SPY', 'QQQ', 'GLD', '^VIX']
            data = {}

            for ticker in tickers:
                stock = yf.Ticker(ticker)
                hist = stock.history(period='5d')
                current = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2]
                change_pct = ((current - prev) / prev) * 100

                data[ticker] = {
                    'price': float(current),
                    'change_pct': float(change_pct),
                    'volume': float(hist['Volume'].iloc[-1])
                }

            return data
        except Exception as e:
            print(f"⚠️  Failed to fetch stock indices: {e}")
            return None

    def save_cache(self, data):
        """Save all fetched data to cache"""
        cache_file = self.cache_dir / f"{self.date.strftime('%Y-%m-%d')}_market_data.json"
        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"💾 Data cached: {cache_file}")

# Usage
if __name__ == "__main__":
    import sys
    date_str = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y-%m-%d")
    fetcher = MarketDataFetcher(date_str)
    data = fetcher.fetch_all()
    print("✅ Market data fetch complete")
```

---

## 🔄 Complete Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    STEP 1: DATA COLLECTION                      │
│                         (API Integration)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🤖 SCRIPT: fetch_market_data.py                               │
│                                                                 │
│     ┌─────────────────┐                                        │
│     │   API Calls     │                                        │
│     ├─────────────────┤                                        │
│     │ Fear & Greed    │ ──→ JSON                              │
│     │ FRED Economic   │ ──→ JSON                              │
│     │ CoinGecko       │ ──→ JSON                              │
│     │ Yahoo Finance   │ ──→ JSON                              │
│     │ [CoinGlass]     │ ──→ JSON (optional)                   │
│     │ [Glassnode]     │ ──→ JSON (optional)                   │
│     └─────────────────┘                                        │
│                                                                 │
│  OUTPUT: Research/.cache/YYYY-MM-DD_market_data.json          │
│                                                                 │
│  Time: 30-60 seconds                                           │
│  Tokens: 0 (no AI)                                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                 STEP 2: SIGNAL CALCULATION                      │
│                    (Script + AI Hybrid)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🤖 SCRIPT: calculate_signals.py                               │
│                                                                 │
│     1. Load market_data.json                                   │
│     2. Load provider summaries (YouTube, RSS, X)               │
│     3. Calculate components:                                    │
│        - Trend Score (40%)                                     │
│        - Breadth Score (25%)                                   │
│        - Volatility Score (20%)                                │
│        - Technical Score (10%)                                 │
│        - Seasonality Score (5%)                                │
│     4. Apply X sentiment contrarian adjustment                 │
│     5. Calculate composite score                               │
│     6. Determine tier (EXTREME/STRONG/MODERATE/WEAK)          │
│                                                                 │
│  OUTPUT: signals_YYYY-MM-DD.json (initial calculations)       │
│                                                                 │
│  ────────────────────────────────────────────────────────      │
│                                                                 │
│  🧠 AI REVIEW: Claude reads signals + summaries + market data  │
│                                                                 │
│     - Reviews all calculations                                 │
│     - Considers qualitative factors:                           │
│       * Breaking news not in summaries                         │
│       * Market regime changes                                  │
│       * Unusual X sentiment patterns                           │
│       * Geopolitical events                                    │
│     - Can adjust scores with explanation                       │
│     - Documents reasoning                                      │
│                                                                 │
│  OUTPUT: signals_YYYY-MM-DD.json (AI-reviewed, final)         │
│                                                                 │
│  Time: 2-3 minutes                                             │
│  Tokens: ~15K (AI reviews structured data vs. doing all math)  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                 STEP 3: MASTER PLAN UPDATE                      │
│                    (Pure Automation)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🤖 SCRIPT: update_master_plan.py                              │
│                                                                 │
│     1. Load signals_YYYY-MM-DD.json                           │
│     2. Update dates:                                           │
│        - pageTitle: "October 10, 2025"                        │
│        - dateBadge: "October 10, 2025"                        │
│        - All tab updatedAt timestamps                          │
│        - EAGLE EYE header                                      │
│        - Footer dates                                          │
│     3. Update signal data (from JSON)                          │
│     4. Update X sentiment (from trending_words.json)           │
│     5. Update sentimentHistory (add new entry)                 │
│     6. Update HTML dashboard title                             │
│     7. Update .processing_log.json                             │
│                                                                 │
│  OUTPUT: Updated master-plan.md + supporting files             │
│                                                                 │
│  Time: 10-20 seconds                                           │
│  Tokens: 0 (no AI)                                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  STEP 4: VERIFICATION                           │
│                    (Automated Checks)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🤖 SCRIPT: verify_consistency.py                              │
│                                                                 │
│     1. Scan master-plan.md for dates                           │
│     2. Verify all match target date                            │
│     3. Check signal score consistency                          │
│     4. Validate timestamp updates                              │
│     5. Check HTML dashboard                                    │
│     6. Generate verification report                            │
│                                                                 │
│  ────────────────────────────────────────────────────────────  │
│                                                                 │
│  🧠 AI: Reviews verification report                            │
│     - Confirms all checks passed                               │
│     - Investigates any warnings                                │
│     - Final quality check                                      │
│                                                                 │
│  OUTPUT: Verification report                                   │
│                                                                 │
│  Time: 5-10 seconds                                            │
│  Tokens: ~2K (AI reviews report only)                          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    ✅ WORKFLOW COMPLETE
```

---

## 📊 Token Usage Breakdown

### Before (Current Workflow)

| Step | Operation | Tokens | Notes |
|------|-----------|--------|-------|
| 1 | Read provider summaries | 20K | YouTube, RSS, X summaries |
| 2 | Web search for technicals | 40K | Multiple searches, data extraction |
| 3 | Calculate signals | 30K | AI reads summaries, does math |
| 4 | Update master plan dates | 20K | AI reads file, finds all dates |
| 5 | Verify consistency | 15K | AI reads file, checks dates |
| 6 | Update supporting files | 10K | HTML, processing log |
| 7 | Generate documentation | 15K | Processing notes |
| **TOTAL** | | **150K** | |

### After (API + Scripts + AI)

| Step | Operation | Tokens | Notes |
|------|-----------|--------|-------|
| 1 | Fetch market data (API) | 0 | Script only, no AI |
| 2 | Calculate signals (Script) | 0 | Math operations |
| 2b | AI reviews signals | 15K | Reviews JSON + summaries, can adjust |
| 3 | Update master plan (Script) | 0 | Pure string replacement |
| 4 | Verify consistency (Script) | 0 | Automated checks |
| 4b | AI reviews verification | 2K | Reviews report only |
| 5 | Read provider summaries | 20K | Same as before (still needed) |
| 6 | Market overview synthesis | 40K | AI still synthesizes (preserved) |
| 7 | X trends processing | 5K | Already scripted |
| 8 | Final quality check | 20K | AI final review |
| **TOTAL** | | **102K** | **32% reduction** |

**Savings:** 48K tokens per run

**Time Savings:**
- Before: 30-45 minutes
- After: 20-30 minutes
- Savings: 10-15 minutes per run

---

## 🛠️ Implementation Phases

### **Phase 1: API Integration (Week 1)**

**Goal:** Replace web searches with API data

**Tasks:**
- [ ] Set up API keys (FRED, CoinGecko)
- [ ] Implement `fetch_market_data.py`
  - [ ] Fear & Greed Index integration
  - [ ] FRED economic data
  - [ ] CoinGecko crypto prices
  - [ ] Yahoo Finance stock indices
- [ ] Create JSON cache structure
- [ ] Test API reliability and rate limits
- [ ] Error handling and fallbacks

**Deliverable:** `fetch_market_data.py` fully functional

---

### **Phase 2: Signal Calculation (Week 2)**

**Goal:** Automate signal math, preserve AI review

**Tasks:**
- [ ] Implement `calculate_signals.py`
  - [ ] Trend score calculation
  - [ ] Breadth score calculation
  - [ ] Volatility score calculation
  - [ ] Technical score calculation
  - [ ] Seasonality score calculation
  - [ ] X sentiment contrarian adjustment
  - [ ] Composite score and tier determination
- [ ] Implement AI review workflow
  - [ ] Load calculated signals
  - [ ] Load provider summaries for context
  - [ ] AI reviews and can adjust
  - [ ] Save final signals JSON
- [ ] Test calculation accuracy vs. manual

**Deliverable:** `calculate_signals.py` with AI review integration

---

### **Phase 3: Master Plan Automation (Week 3)**

**Goal:** Automate deterministic updates

**Tasks:**
- [ ] Implement `update_master_plan.py`
  - [ ] Date updates (pageTitle, dateBadge, headers, footer)
  - [ ] Tab timestamp updates
  - [ ] Signal data updates from JSON
  - [ ] X sentiment updates
  - [ ] sentimentHistory updates
  - [ ] HTML dashboard updates
  - [ ] Processing log updates
- [ ] Implement `verify_consistency.py`
  - [ ] Date consistency checks
  - [ ] Signal score consistency
  - [ ] Timestamp validation
  - [ ] HTML dashboard verification
- [ ] Test on historical dates

**Deliverable:** `update_master_plan.py` and `verify_consistency.py` fully functional

---

### **Phase 4: Integration & Testing (Week 4)**

**Goal:** End-to-end testing and documentation

**Tasks:**
- [ ] Create master orchestrator script
  - [ ] Runs all 4 scripts in sequence
  - [ ] Error handling between stages
  - [ ] Progress reporting
- [ ] End-to-end testing
  - [ ] Test multiple dates
  - [ ] Test error scenarios
  - [ ] Test API failures (fallbacks)
- [ ] Update workflow documentation
  - [ ] Update `How to use_MP.txt`
  - [ ] Add API setup guide
  - [ ] Add troubleshooting guide
- [ ] Performance optimization
  - [ ] Parallel API calls
  - [ ] Caching strategies
  - [ ] Token optimization

**Deliverable:** Complete automated workflow, fully documented

---

## 📝 Key Principles Preserved

### 1. **AI Reviews All Important Decisions**

The hybrid approach ensures AI sees everything critical:

- ✅ Signal calculations (AI reviews, can adjust)
- ✅ Provider summaries (AI still reads and synthesizes)
- ✅ Market overview (AI generates from all data)
- ✅ Consistency verification (AI reviews report)
- ✅ Final quality check (AI confirms everything)

**What AI Does NOT See (By Design):**
- Date string replacements (pure automation)
- JSON file updates (deterministic)
- API data fetching (no interpretation needed until review)

### 2. **Scripts Only for Deterministic Tasks**

Scripts handle **only** operations with one correct answer:

- ✅ Math calculations (trend score = 32/40)
- ✅ Date arithmetic (October 9 + 1 day = October 10)
- ✅ String replacements ("October 9" → "October 10")
- ✅ JSON parsing and updates
- ✅ Regex pattern matching
- ✅ File I/O operations

**NOT Scripted (Requires Judgment):**
- Interpreting market news
- Synthesizing provider insights
- Deciding if X sentiment is meaningful
- Adjusting scores for qualitative factors
- Writing market commentary

### 3. **Data Flow Transparency**

Every step produces visible, reviewable outputs:

1. **API Fetch** → `market_data.json` (AI can inspect raw data)
2. **Signal Calc** → `signals.json` (AI reviews calculations)
3. **AI Review** → `signals.json` (AI adds adjustments with reasoning)
4. **Master Plan Update** → `master-plan.md` (visible changes)
5. **Verification** → Report (AI confirms)

Nothing happens in a "black box" - AI can trace every decision.

---

## 🎯 Success Criteria

### Automation Goals

- ✅ **Reliability:** API data sources 99%+ uptime
- ✅ **Accuracy:** Signal calculations match manual calculations 100%
- ✅ **Consistency:** All dates/scores updated correctly 100% of time
- ✅ **Transparency:** AI can explain every automated step
- ✅ **Maintainability:** Scripts are readable, well-documented

### AI Preservation Goals

- ✅ **Signal Review:** AI reviews 100% of signal calculations
- ✅ **Synthesis:** AI still generates market overview
- ✅ **Judgment:** AI can override any automated decision
- ✅ **Quality:** AI performs final quality check
- ✅ **Documentation:** AI documents any adjustments made

### Performance Goals

- ✅ **Token Reduction:** 30%+ reduction (48K tokens saved)
- ✅ **Time Savings:** 10-15 minutes faster per run
- ✅ **Cost:** Free tier viable, <$100/month for premium
- ✅ **Autonomy:** 90%+ of routine tasks automated
- ✅ **Flexibility:** AI can still handle edge cases

---

## 🔍 Comparison: Old vs. New Approach

### Old Two-Stage Refactoring (Previous Proposal)

**Issues:**
- ❌ Complex two-stage architecture (prep + update)
- ❌ 6-week implementation timeline
- ❌ Removed AI from seeing important data
- ❌ Over-engineered for the problem
- ❌ Lost sight of core principle

### New API + Scripts + AI (Approved)

**Benefits:**
- ✅ Linear workflow maintained (existing structure)
- ✅ 4-week implementation timeline
- ✅ AI reviews all calculations (hybrid approach)
- ✅ Practical, focused automation
- ✅ Aligns with "scripts for repeatable, AI for dynamic" principle

### The Key Insight

The breakthrough was realizing:

> **"The workflow is already linear. We don't need to restructure it.
> We just need to replace web searches with APIs and automate the math."**

This led to the 4-script approach:
1. **fetch_market_data.py** - APIs replace web searches
2. **calculate_signals.py** - Script calculates, AI reviews
3. **update_master_plan.py** - Pure automation for dates
4. **verify_consistency.py** - Automated checks

Simple. Practical. Preserves AI judgment.

---

## 📚 API Resources and Documentation

### Free Tier APIs (Tier 1)

1. **Fear & Greed Index (Crypto)**
   - URL: https://api.alternative.me/fng/
   - Docs: https://alternative.me/crypto/fear-and-greed-index/
   - Rate Limit: None
   - Data Format: JSON

2. **FRED Economic Data**
   - URL: https://fred.stlouisfed.org/docs/api/
   - API Key: Free registration required
   - Rate Limit: 120 requests/minute
   - Data: Unemployment, CPI, Fed Funds Rate, GDP

3. **CoinGecko**
   - URL: https://www.coingecko.com/en/api
   - Free Tier: 10-50 calls/minute
   - Data: Crypto prices, market cap, volume, 24h change
   - Docs: https://www.coingecko.com/en/api/documentation

4. **Yahoo Finance (yfinance)**
   - Docs: https://github.com/ranaroussi/yfinance
   - Installation: `pip install yfinance`
   - Data: Stock indices (SPY, QQQ, GLD), VIX
   - Rate Limit: Reasonable use policy

### Paid Tier APIs (Tier 2 - Optional)

5. **CoinGlass**
   - URL: https://www.coinglass.com/api
   - Cost: $50/month (basic plan)
   - Data: Funding rates, liquidations, open interest
   - Value: Critical for crypto derivatives sentiment

6. **Glassnode**
   - URL: https://docs.glassnode.com/api
   - Cost: $30/month (starter plan)
   - Data: On-chain metrics, whale activity, exchange flows
   - Value: Deep on-chain insights for BTC/ETH

---

## ✅ Next Steps

### Immediate Actions (This Week)

1. **Set up API accounts** ✓
   - Register for FRED API key
   - Verify CoinGecko free tier access
   - Test yfinance installation

2. **Create Phase 1 skeleton**
   - `scripts/fetch_market_data.py` (basic structure)
   - Test one API (start with CoinGecko)
   - Verify JSON cache creation

3. **Document current state**
   - List all web searches in current workflow
   - Map each to API replacement
   - Prioritize by token impact

### Week 1 Deliverable

- `fetch_market_data.py` functional for all Tier 1 APIs
- JSON cache structure established
- Basic error handling implemented

### Long-term Vision

This API + Scripts + AI architecture becomes the foundation for:
- **Full AI autonomy** for routine updates (no human needed)
- **Real-time data** from reliable APIs vs. web scraping
- **Scalable workflow** that can run multiple times per day
- **Transparent decisions** where AI can explain every step
- **Maintainable system** with clear separation of concerns

---

## 📖 References

- **Current Workflow:** `master-plan/How to use_MP.txt`
- **Research Guide:** `Research/How to use_Research.txt`
- **Technicals Guide:** `Research/Technicals/How to use_Technicals.txt`
- **Signals Guide:** `Trading/signal-system/How to use_Signals.txt`
- **X Trends Script:** `Research/X/Trends/process_trends.py`

---

**Status:** ✅ Approved - Ready for Implementation
**Implementation Start:** Week of 2025-10-10
**Expected Completion:** November 7, 2025 (4 weeks)
**Estimated ROI:**
- 32% token reduction (48K tokens saved per run)
- 10-15 minutes time savings per run
- $0-80/month cost (free tier viable)
- 90%+ automation while preserving AI judgment

---

*Practical automation plan created October 10, 2025 during master plan workflow analysis*
*Core Principle: "Scripts for repeatable, AI for dynamic"*
