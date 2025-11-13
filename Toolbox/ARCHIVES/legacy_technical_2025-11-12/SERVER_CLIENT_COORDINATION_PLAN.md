# Server-Client Coordination Plan
**Investment Research Dashboard - Complete API Migration**

**Date:** 2025-11-08
**Version:** 1.0
**Purpose:** Coordinate API development between server team and client team

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Responsibility Breakdown](#responsibility-breakdown)
3. [API Endpoint Specifications](#api-endpoint-specifications)
4. [Data Formats](#data-formats)
5. [Ollama Processing Guidelines](#ollama-processing-guidelines)
6. [Implementation Timeline](#implementation-timeline)
7. [Testing Strategy](#testing-strategy)
8. [Migration Path](#migration-path)

---

## Architecture Overview

### Current State (Phase 1 Complete)

```
┌─────────────────────────────────────────────┐
│  API Server (192.168.10.56:3000)            │
│  ✅ ETF Data (SPY, QQQ, VIX)                │
│  ✅ Max Pain Options                         │
│  ✅ Chat Data                                │
└─────────────────────────────────────────────┘
                    ↓ HTTP
┌─────────────────────────────────────────────┐
│  Client Machine (Windows)                    │
│  ├── API Client (technical data)            │
│  ├── Local Scrapers (YouTube, RSS, Twitter) │
│  └── Claude AI (synthesis + dashboard)      │
└─────────────────────────────────────────────┘
```

### Target State (Phase 2 - This Plan)

```
┌───────────────────────────────────────────────────────┐
│  API Server (192.168.10.56:3000)                      │
│                                                        │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 1. Scrapers (Playwright)                        │ │
│  │    ├── YouTube (19 channels)                    │ │
│  │    ├── RSS (MarketWatch, CNBC, Fed)            │ │
│  │    └── Twitter (3 lists + bookmarks)           │ │
│  └─────────────────────────────────────────────────┘ │
│                    ↓                                   │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 2. Ollama Processing (192.168.10.52:11434)     │ │
│  │    ├── Summarize YouTube transcripts           │ │
│  │    ├── Summarize RSS articles                  │ │
│  │    └── Sentiment analysis on tweets            │ │
│  └─────────────────────────────────────────────────┘ │
│                    ↓                                   │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 3. Database Storage (SQLite)                    │ │
│  │    ├── Raw scraped data                         │ │
│  │    ├── Ollama summaries                         │ │
│  │    └── Metadata (timestamps, sources)          │ │
│  └─────────────────────────────────────────────────┘ │
│                    ↓                                   │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 4. REST API Endpoints                           │ │
│  │    ├── /api/research/youtube                    │ │
│  │    ├── /api/research/rss                        │ │
│  │    ├── /api/research/twitter                    │ │
│  │    └── /api/signals/latest                      │ │
│  └─────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────┘
                    ↓ HTTP (Ollama-summarized data)
┌───────────────────────────────────────────────────────┐
│  Client Machine (Windows)                              │
│                                                        │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 1. API Client                                    │ │
│  │    └── Fetch pre-summarized data                │ │
│  └─────────────────────────────────────────────────┘ │
│                    ↓                                   │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 2. Claude AI (High-Level Synthesis)             │ │
│  │    ├── Provider overviews (e.g., "MarketWatch") │ │
│  │    ├── Category overviews (e.g., "Crypto")      │ │
│  │    ├── Cross-cutting themes                     │ │
│  │    └── Strategic insights                       │ │
│  └─────────────────────────────────────────────────┘ │
│                    ↓                                   │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 3. Dashboard Updates                             │ │
│  │    └── Update dashboard.json thoughtfully       │ │
│  └─────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────┘
```

### Cost Optimization Strategy

| Task | Who Does It | Cost | Rationale |
|------|-------------|------|-----------|
| **Scraping** | Server (Playwright) | Low | Automated, no AI needed |
| **Individual Summaries** | Server (Ollama) | **FREE** | Ollama is local, unlimited |
| **Provider Overviews** | Client (Claude) | Moderate | Requires synthesis across items |
| **Category Overviews** | Client (Claude) | Moderate | Cross-cutting analysis |
| **Strategic Insights** | Client (Claude) | Moderate | High-value human-like reasoning |
| **Dashboard Updates** | Client (Claude) | Low | Simple JSON updates |

**Total Token Savings:** ~90% reduction in Claude API costs

---

## Responsibility Breakdown

### Server Team Responsibilities

#### Scraping (Automated, Scheduled)

1. **YouTube Transcripts**
   - Scrape 19 channels every 6 hours
   - Extract: title, URL, published date, full transcript
   - Store raw data in database

2. **RSS Feeds**
   - Scrape 3 providers × multiple categories every 30 minutes
   - Extract: title, URL, published date, full article text
   - Store raw data in database

3. **Twitter/X Posts**
   - Scrape 3 lists (Technicals, Crypto, Macro) every 30 minutes
   - Scrape bookmarks every hour
   - Extract: username, text, engagement metrics, timestamp
   - Store raw data in database

#### Ollama Processing (Individual Item Summarization)

1. **YouTube Summaries**
   - For each video: send transcript to Ollama
   - Prompt: "Summarize investment thesis, key data, sentiment"
   - Return: 150-300 word summary
   - Store summary in database

2. **RSS Summaries**
   - For each article: send full text to Ollama
   - Prompt: "Summarize main story, market impact, key quotes"
   - Return: 100-200 word summary
   - Store summary in database

3. **Twitter Sentiment**
   - For each post: send text to Ollama
   - Prompt: "Analyze sentiment (bullish/bearish/neutral) and extract topics"
   - Return: sentiment label + confidence + topic tags
   - Store in database

#### Database Management

- Store raw + processed data
- Index for fast queries
- Expire old data (keep last 7 days)
- Track scrape metadata (success/failure, duration)

#### API Endpoints

- Serve pre-summarized data via REST API
- Handle filtering (by date, provider, category)
- Return JSON responses
- CORS enabled for client access

### Client Team Responsibilities

#### API Consumption

1. **Fetch Pre-Summarized Data**
   - Call API endpoints during RECON
   - Retrieve Ollama summaries for all sources
   - Organize by provider/category
   - Duration: ~30-60 seconds

#### High-Level Synthesis (Claude AI)

1. **Provider Overviews**
   - Example: "MarketWatch Overview"
   - Synthesize 20-30 article summaries into cohesive narrative
   - Identify common themes across MarketWatch content
   - Extract key market narratives

2. **Category Overviews**
   - Example: "Crypto Sentiment Overview"
   - Synthesize across providers (YouTube + Twitter + RSS)
   - Cross-cutting analysis (not just one source)
   - Identify consensus vs divergence

3. **Strategic Insights**
   - Market implications
   - Trading opportunities
   - Risk assessment
   - Actionable recommendations

#### Dashboard Updates

- Update `dashboard.json` with synthesized insights
- Maintain thoughtful, concise formatting
- Include attribution and confidence levels

---

## API Endpoint Specifications

### 1. YouTube Research Data

#### **GET /api/research/youtube**

**Purpose:** Return Ollama-summarized YouTube videos from tracked channels

**Query Parameters:**
- `hours` (optional, default: 24) - Get videos from last N hours
- `channel` (optional) - Filter by specific channel name
- `limit` (optional, default: 100) - Max videos to return

**Response Format:**
```json
{
  "success": true,
  "timestamp": "2025-11-08T10:00:00.000Z",
  "count": 42,
  "channels": [
    {
      "channel_name": "Meet Kevin",
      "channel_subscriber_count": 1800000,
      "videos": [
        {
          "video_id": "DQVQ_lvVtoo",
          "video_title": "Fed to RAPIDLY CUT Rates to ZERO | MAJOR PANIC",
          "video_url": "https://youtube.com/watch?v=DQVQ_lvVtoo",
          "published_date": "2025-11-08T08:00:00.000Z",
          "duration_seconds": 1847,
          "view_count": 127000,

          "transcript_summary_ollama": "Kevin discusses Federal Reserve's potential for rapid rate cuts to zero, analyzing historical precedents from 2008 and 2020. Key points: 1) Fed may cut 50-75bps at next meeting if unemployment rises above 4.5%. 2) Market pricing in 3-4 cuts by Q2 2025. 3) Risk of recession if cuts come too late. Sentiment: Bearish on short-term growth, bullish on bonds. Recommends: reduce equity exposure, increase cash/bonds, avoid tech concentration.",

          "full_transcript": "Hey everyone, it's Meet Kevin here...",

          "ollama_metadata": {
            "model": "gpt-oss:20b",
            "processing_time_ms": 3420,
            "summary_length_words": 89,
            "sentiment_detected": "bearish"
          },

          "scraped_at": "2025-11-08T09:00:00.000Z"
        }
      ]
    },
    {
      "channel_name": "Graham Stephan",
      "videos": [...]
    }
  ]
}
```

**Ollama Processing:**
- Server sends full transcript to Ollama
- Ollama returns structured summary (thesis, data, sentiment)
- Server stores summary + metadata in database
- API serves pre-processed summaries

**Client Usage:**
```python
api = MarketDataAPI()
youtube_data = api.get_youtube_research(hours=24)

# Claude synthesizes channel-level overviews
# Example: "Meet Kevin focused on Fed policy this week..."
```

---

### 2. RSS Research Data

#### **GET /api/research/rss**

**Purpose:** Return Ollama-summarized RSS articles from tracked providers

**Query Parameters:**
- `hours` (optional, default: 24) - Get articles from last N hours
- `provider` (optional) - Filter by provider (MarketWatch, CNBC, FederalReserve)
- `category` (optional) - Filter by category
- `limit` (optional, default: 200) - Max articles to return

**Response Format:**
```json
{
  "success": true,
  "timestamp": "2025-11-08T10:00:00.000Z",
  "count": 127,
  "providers": [
    {
      "provider_name": "MarketWatch",
      "categories": [
        {
          "category_name": "Top Stories",
          "articles": [
            {
              "article_id": "mw_20251108_001",
              "article_title": "Banks like Chase, Capital One offering help to affected customers",
              "article_url": "https://marketwatch.com/story/banks-help-2025",
              "published_date": "2025-11-08T07:30:00.000Z",
              "author": "Rachel Smith",

              "article_summary_ollama": "Major banks including JPMorgan Chase and Capital One are offering payment deferrals and fee waivers to customers affected by recent government shutdown. Programs include: 1) 90-day mortgage payment deferrals, 2) Credit card late fee waivers, 3) Early access to direct deposits. Impact: Estimated 2M federal workers affected. Banks cite customer retention and regulatory goodwill as motivations. Market reaction: Bank stocks flat, viewed as cost of doing business.",

              "full_text": "Major banks are stepping up to help...",

              "ollama_metadata": {
                "model": "gpt-oss:20b",
                "processing_time_ms": 2100,
                "summary_length_words": 74,
                "topics_extracted": ["banking", "government shutdown", "customer service"]
              },

              "scraped_at": "2025-11-08T08:00:00.000Z"
            }
          ]
        },
        {
          "category_name": "Economy",
          "articles": [...]
        }
      ]
    },
    {
      "provider_name": "CNBC",
      "categories": [...]
    }
  ]
}
```

**Ollama Processing:**
- Server sends full article text to Ollama
- Ollama returns structured summary (story, impact, quotes)
- Server categorizes by provider + category
- API serves organized summaries

**Client Usage:**
```python
api = MarketDataAPI()
rss_data = api.get_rss_research(hours=24)

# Claude synthesizes provider-level overviews
# Example: "MarketWatch coverage emphasized banking sector responses..."
```

---

### 3. Twitter/X Research Data

#### **GET /api/research/twitter**

**Purpose:** Return X/Twitter posts with Ollama sentiment analysis

**Query Parameters:**
- `hours` (optional, default: 24) - Get posts from last N hours
- `list` (optional) - Filter by list (Technicals, Crypto, Macro)
- `include_bookmarks` (optional, default: false) - Include bookmarked posts
- `limit` (optional, default: 300) - Max posts to return

**Response Format:**
```json
{
  "success": true,
  "timestamp": "2025-11-08T10:00:00.000Z",
  "count": 243,
  "lists": [
    {
      "list_name": "Technicals",
      "post_count": 87,
      "posts": [
        {
          "post_id": "1234567890",
          "username": "trader_joe",
          "display_name": "Joe Trader",
          "post_text": "SPY breaking resistance at 450. Next target 465 if we hold above 448 on the daily. Volume confirming the move. Bullish setup into Q4.",
          "posted_at": "2025-11-08T08:15:00.000Z",
          "post_url": "https://twitter.com/trader_joe/status/1234567890",

          "engagement": {
            "likes": 127,
            "retweets": 34,
            "replies": 12,
            "views": 8430
          },

          "has_media": true,
          "media_urls": ["https://pbs.twimg.com/media/chart.jpg"],

          "ollama_sentiment_analysis": {
            "sentiment": "bullish",
            "confidence": 0.87,
            "topics": ["SPY", "resistance", "breakout", "Q4"],
            "key_levels_mentioned": ["450", "465", "448"],
            "rationale": "Post discusses price breakout with technical confirmation (volume). Bullish directional bias with specific targets and risk levels. High conviction based on multiple confirming factors."
          },

          "ollama_metadata": {
            "model": "gpt-oss:20b",
            "processing_time_ms": 1200
          },

          "scraped_at": "2025-11-08T09:00:00.000Z"
        }
      ]
    },
    {
      "list_name": "Crypto",
      "posts": [...]
    },
    {
      "list_name": "Macro",
      "posts": [...]
    }
  ],
  "bookmarks": [
    {
      "post_id": "9876543210",
      "username": "macro_analyst",
      "post_text": "Fed minutes suggest 75% probability of 25bp cut in December...",
      "ollama_sentiment_analysis": {...},
      "bookmarked_at": "2025-11-08T07:45:00.000Z"
    }
  ]
}
```

**Ollama Processing:**
- Server sends each post text to Ollama
- Ollama returns: sentiment, confidence, topics, key levels
- Server stores analysis with original post
- API serves posts with embedded analysis

**Client Usage:**
```python
api = MarketDataAPI()
twitter_data = api.get_twitter_research(hours=24, list="Crypto")

# Claude synthesizes category-level sentiment
# Example: "Crypto Twitter sentiment shifted bearish as BTC failed 112k..."
```

---

### 4. Signal Calculation Data

#### **GET /api/signals/latest**

**Purpose:** Return calculated technical signals and composite score

**Query Parameters:**
- None (always returns latest calculation)

**Response Format:**
```json
{
  "success": true,
  "timestamp": "2025-11-08T10:00:00.000Z",
  "calculation_date": "2025-11-08",

  "composite_signal": {
    "score": 54.1,
    "tier": "MODERATE",
    "stance": "Consolidation Phase / Selective Positioning",
    "last_updated": "2025-11-08T09:00:00.000Z"
  },

  "components": {
    "trend": {
      "weight": 30,
      "score": 16.8,
      "max_score": 30,
      "rationale": "SPX 6,840 neutral momentum (RSI 61), bullish bias, stuck in 6,703-6,977 range. No directional conviction.",
      "indicators": {
        "spy_price": 6840,
        "spy_rsi": 61,
        "spy_trend": "neutral",
        "support_levels": [6703, 6498],
        "resistance_levels": [6977, 7182]
      }
    },
    "breadth": {
      "weight": 25,
      "score": 13.3,
      "max_score": 25,
      "rationale": "AD ratio 1.33 (neutral), NYSE 3,056 adv / 2,303 dec suggests mild advance. Lacks thrust.",
      "indicators": {
        "ad_ratio": 1.33,
        "advancers": 3056,
        "decliners": 2303,
        "up_volume_pct": 52
      }
    },
    "volatility": {
      "weight": 20,
      "score": 12.0,
      "max_score": 20,
      "rationale": "SPY IV 64% / QQQ IV 68% elevated but stabilizing. Not panic (>80), not risk-on (<40).",
      "indicators": {
        "spy_iv": 64,
        "qqq_iv": 68,
        "vix_current": 18.5,
        "vix_regime": "normal"
      }
    },
    "sentiment": {
      "weight": 15,
      "score": 7.5,
      "max_score": 15,
      "rationale": "Buffett caution (-1.5 pts), retail Greed +0.5 pts = net negative bias. Professional money preparing for downside.",
      "indicators": {
        "fear_greed_index": 62,
        "put_call_ratio": 0.92,
        "smart_money_flow": "defensive"
      }
    },
    "technical": {
      "weight": 10,
      "score": 4.5,
      "max_score": 10,
      "rationale": "Max pain levels (SPY 683 / QQQ 629) suggest range-bound theta decay. Options market pricing consolidation.",
      "indicators": {
        "spy_max_pain": 683,
        "qqq_max_pain": 629,
        "spy_current": 450.23,
        "qqq_current": 380.15
      }
    }
  },

  "market_interpretation": {
    "summary": "Consolidation, not conviction. Spinning-top pattern + elevated IV + Buffett defensiveness = market waiting for catalyst.",
    "bias": "Selective long bias",
    "hedging_recommendation": "Put spreads (SPY 665/660) offer attractive risk/reward",
    "next_catalyst": "Q4 earnings + Fed policy clarity (likely December)"
  }
}
```

**Server Calculation:**
- Server runs `calculate_signals.py` logic
- Weights: Trend 30%, Breadth 25%, Volatility 20%, Sentiment 15%, Technical 10%
- Returns full breakdown + rationale
- Updates every market close

**Client Usage:**
```python
api = MarketDataAPI()
signals = api.get_signals_latest()

# Claude uses signals for dashboard updates
# Claude can override or adjust based on synthesis
```

---

## Data Formats

### YouTube Video Summary (Ollama Output)

**Input to Ollama:**
```
Full video transcript (5,000-20,000 words)
```

**Ollama Prompt:**
```
You are a financial analyst summarizing YouTube videos for traders and investors.

Analyze this video transcript and provide a concise summary (150-300 words) covering:
1. Main investment thesis or market view
2. Key data points, numbers, or statistics mentioned
3. Specific recommendations or actionable insights
4. Overall sentiment (bullish/bearish/neutral) with brief justification

Transcript:
{full_transcript}

Provide your response in this exact format:
SUMMARY: [your summary here]
SENTIMENT: [bullish/bearish/neutral]
```

**Expected Output:**
```
SUMMARY: Kevin discusses Federal Reserve's potential for rapid rate cuts to zero, analyzing historical precedents from 2008 and 2020. Key points: 1) Fed may cut 50-75bps at next meeting if unemployment rises above 4.5%. 2) Market pricing in 3-4 cuts by Q2 2025. 3) Risk of recession if cuts come too late. Recommends: reduce equity exposure, increase cash/bonds, avoid tech concentration.

SENTIMENT: bearish
```

---

### RSS Article Summary (Ollama Output)

**Input to Ollama:**
```
Full article text (500-3,000 words)
```

**Ollama Prompt:**
```
You are a financial analyst summarizing news articles for traders and investors.

Analyze this article and provide a concise summary (100-200 words) covering:
1. Main story or development
2. Market impact or implications for investors
3. Key quotes or important data points
4. Relevance to different asset classes (stocks/bonds/commodities)

Article:
{full_text}

Provide your response in this exact format:
SUMMARY: [your summary here]
TOPICS: [comma-separated list of relevant topics]
```

**Expected Output:**
```
SUMMARY: Major banks including JPMorgan Chase and Capital One are offering payment deferrals and fee waivers to customers affected by government shutdown. Programs include 90-day mortgage deferrals, credit card late fee waivers, and early direct deposit access. Estimated 2M federal workers affected. Banks cite customer retention and regulatory goodwill as motivations. Market reaction muted, viewed as cost of doing business. Minimal impact on bank earnings expected.

TOPICS: banking, government shutdown, customer service, credit cards, mortgages
```

---

### Twitter Sentiment Analysis (Ollama Output)

**Input to Ollama:**
```
Single tweet text (1-280 characters)
```

**Ollama Prompt:**
```
You are a financial sentiment analyst analyzing trading-related tweets.

Analyze this tweet and determine:
1. Sentiment (bullish/bearish/neutral)
2. Confidence level (0.0 to 1.0)
3. Key topics mentioned (stock tickers, sectors, themes)
4. Any price levels or targets mentioned
5. Brief rationale for sentiment classification

Tweet:
{post_text}

Provide your response in this exact JSON format:
{
  "sentiment": "bullish|bearish|neutral",
  "confidence": 0.87,
  "topics": ["SPY", "resistance", "breakout"],
  "levels": ["450", "465", "448"],
  "rationale": "Post discusses price breakout with technical confirmation..."
}
```

**Expected Output:**
```json
{
  "sentiment": "bullish",
  "confidence": 0.87,
  "topics": ["SPY", "resistance", "breakout", "Q4"],
  "levels": ["450", "465", "448"],
  "rationale": "Post discusses price breakout with technical confirmation (volume). Bullish directional bias with specific targets and risk levels. High conviction based on multiple confirming factors."
}
```

---

## Ollama Processing Guidelines

### Performance Targets

| Task | Input Size | Processing Time | Output Size |
|------|-----------|-----------------|-------------|
| YouTube Summary | 5,000-20,000 words | 3-5 seconds | 150-300 words |
| RSS Summary | 500-3,000 words | 1-2 seconds | 100-200 words |
| Twitter Sentiment | 1-280 characters | 0.5-1 second | JSON (50-150 chars) |

### Batch Processing

- Process in batches of 10-20 items
- Use async requests to Ollama
- Retry failed requests (max 3 attempts)
- Store failures for manual review

### Quality Control

**Validation Checks:**
- Summary length within limits
- Sentiment is one of: bullish/bearish/neutral
- Topics array not empty
- Rationale provided

**Fallback Behavior:**
- If Ollama fails: store raw content, mark as "pending_summary"
- Client can request re-processing
- Manual summaries as last resort

### Caching Strategy

- Cache Ollama summaries by content hash
- Don't re-summarize identical content
- Expire cache after 30 days
- Reduces Ollama load by ~40-50%

---

## Implementation Timeline

### Phase 1: YouTube API (Week 1-2)

**Server Tasks:**
1. Build YouTube scraper (Playwright)
2. Integrate Ollama summarization
3. Create `/api/research/youtube` endpoint
4. Database schema + storage
5. PM2 cron job (every 6 hours)

**Client Tasks:**
1. Add `get_youtube_research()` to API client
2. Create data transformer for YouTube format
3. Update RECON to fetch from API
4. Test with Claude synthesis workflow

**Success Criteria:**
- 19 channels scraped successfully
- Ollama summaries generated for all videos
- API returns data in <1 second
- Claude can synthesize channel overviews

---

### Phase 2: RSS API (Week 2-3)

**Server Tasks:**
1. Build RSS scraper (existing logic + Playwright for full articles)
2. Integrate Ollama summarization
3. Create `/api/research/rss` endpoint
4. Database schema + storage
5. PM2 cron job (every 30 minutes)

**Client Tasks:**
1. Add `get_rss_research()` to API client
2. Create data transformer for RSS format
3. Update RECON to fetch from API
4. Test with Claude synthesis workflow

**Success Criteria:**
- 3 providers × categories scraped successfully
- Ollama summaries for all articles
- API returns data in <1 second
- Claude can synthesize provider overviews

---

### Phase 3: Twitter API (Week 3-4)

**Server Tasks:**
1. Build Twitter scraper (Playwright)
2. Handle authentication (session cookies)
3. Integrate Ollama sentiment analysis
4. Create `/api/research/twitter` endpoint
5. Database schema + storage
6. PM2 cron job (every 30 minutes)

**Client Tasks:**
1. Add `get_twitter_research()` to API client
2. Create data transformer for Twitter format
3. Update RECON to fetch from API
4. Test with Claude synthesis workflow

**Success Criteria:**
- 3 lists + bookmarks scraped successfully
- Ollama sentiment for all posts
- API returns data in <1 second
- Claude can synthesize category sentiment

---

### Phase 4: Signal Calculation (Week 4-5)

**Server Tasks:**
1. Port `calculate_signals.py` logic to server
2. Calculate components: trend, breadth, volatility, sentiment, technical
3. Create `/api/signals/latest` endpoint
4. Store signal history
5. PM2 cron job (every market close)

**Client Tasks:**
1. Add `get_signals_latest()` to API client
2. Use signals in dashboard updates
3. Optional: Allow Claude to override/adjust

**Success Criteria:**
- Signal calculation matches current logic
- API returns full breakdown
- Dashboard displays signal correctly

---

### Phase 5: Client Integration & Cleanup (Week 5-6)

**Client Tasks:**
1. Remove all local scrapers (archive as backup)
2. Update RECON to be pure API fetch
3. Update documentation
4. End-to-end testing
5. Performance validation

**Success Criteria:**
- RECON takes <60 seconds (API fetch only)
- PREP synthesis unchanged (Claude quality)
- Total morning workflow <30 minutes
- 90% token cost reduction achieved

---

## Testing Strategy

### Server-Side Testing

**Unit Tests:**
```python
def test_youtube_scraper():
    # Test scraping single channel
    # Verify transcript extraction
    # Validate data format

def test_ollama_youtube_summary():
    # Test Ollama integration
    # Verify summary format
    # Check length constraints

def test_api_youtube_endpoint():
    # Test endpoint response
    # Verify filtering works
    # Check performance (<1s)
```

**Integration Tests:**
```python
def test_end_to_end_youtube():
    # Scrape → Ollama → Database → API
    # Verify full pipeline
    # Check data consistency
```

**Performance Tests:**
- Scraper completes in reasonable time
- Ollama processing <5s per item
- API responds in <1s
- Database queries optimized

---

### Client-Side Testing

**API Client Tests:**
```python
def test_api_youtube_fetch():
    api = MarketDataAPI()
    result = api.get_youtube_research(hours=24)
    assert result['success'] == True
    assert len(result['channels']) > 0

def test_data_transformer():
    raw_api_data = {...}
    transformed = transform_youtube_data(raw_api_data)
    assert 'channel_overviews' in transformed
```

**Integration Tests:**
```python
def test_recon_workflow():
    # Run full RECON with API
    # Verify data fetched correctly
    # Check file outputs

def test_prep_synthesis():
    # Load API data
    # Run Claude synthesis
    # Verify overviews generated
```

---

### Acceptance Testing

**Criteria:**
- ✅ All API endpoints return data successfully
- ✅ Ollama summaries are accurate and concise
- ✅ Client can synthesize overviews from summaries
- ✅ RECON duration <60 seconds
- ✅ PREP quality unchanged (Claude synthesis)
- ✅ Dashboard updates correctly
- ✅ 90% token cost reduction achieved

**Test Scenarios:**
1. Normal operation (everything works)
2. API server down (client handles gracefully)
3. Ollama slow/unavailable (fallback to raw data)
4. Partial data (some sources fail)
5. Stale data (scraper hasn't run)

---

## Migration Path

### Current State (Before Phase 2)

**RECON:**
```bash
# Local scrapers run on this machine
python scripts/automation/run_recon.py

# Takes 2-5 minutes:
# - API fetch (technical data): 10 sec
# - Local YouTube scraper: 5-10 min
# - Local RSS scraper: 2-3 min
# - Local Twitter scraper: 3-5 min
```

**Data Storage:**
- `Research/YouTube/{Channel}/*.md` (raw transcripts)
- `Research/RSS/{Provider}/*.md` (raw articles)
- `Research/X/{List}/*.json` (raw posts)

**PREP:**
- Claude reads raw files
- Claude runs Ollama locally for summaries
- Claude synthesizes overviews
- Claude updates dashboard

---

### Transition State (During Phase 2 Development)

**Hybrid Approach:**
- Use API for completed endpoints
- Keep local scrapers for pending endpoints
- Both systems write to Research/ directory

**Example:**
```python
# In run_recon.py

# Phase 1: Use API (already done)
spy_data = api.get_spy_data()

# Phase 2: Use API when available
if api_has_youtube:
    youtube_data = api.get_youtube_research()
else:
    # Fall back to local scraper
    run_local_youtube_scraper()
```

---

### Final State (After Phase 2 Complete)

**RECON:**
```bash
# Pure API fetch
python scripts/automation/run_recon.py

# Takes <60 seconds:
# - API fetch (all data): 30-60 sec
```

**Data Storage:**
- `Research/.cache/{date}_youtube_summaries.json` (Ollama summaries)
- `Research/.cache/{date}_rss_summaries.json` (Ollama summaries)
- `Research/.cache/{date}_twitter_sentiment.json` (Ollama analysis)
- Optional: Cache raw data for debugging

**PREP:**
- Claude reads Ollama summaries from cache
- Claude synthesizes provider/category overviews
- Claude updates dashboard
- **No local Ollama processing needed**

---

## Rollback Procedures

### If API Development Delayed

**Option 1:** Continue using local scrapers
```bash
# Old workflow still works
python scripts/automation/run_all_scrapers.py
```

**Option 2:** Hybrid mode
```bash
# Use API for what's available, local for rest
python scripts/automation/run_recon.py --hybrid
```

### If API Has Issues

**Client-side fallback:**
```python
# Automatic in new code
try:
    data = api.get_youtube_research()
except APIClientError:
    # Fall back to local scraper
    data = run_local_youtube_scraper()
```

### If Ollama Processing Fails

**Server-side fallback:**
- Store raw content without summary
- Mark as "pending_summary"
- Client can still access raw data
- Manual summary as last resort

---

## Success Metrics

### Performance

| Metric | Before | Target | Validation |
|--------|--------|--------|------------|
| RECON Duration | 10-15 min | <60 sec | Timer logs |
| PREP Duration | 30-45 min | 30-45 min | Unchanged |
| Total Morning Workflow | 45-60 min | 30-45 min | End-to-end test |
| API Response Time | N/A | <1 sec | Load testing |

### Cost

| Metric | Before | Target | Validation |
|--------|--------|--------|------------|
| Claude Tokens (Daily) | ~500k-1M | ~50k-100k | Token tracking |
| Claude Cost (Daily) | ~$15-30 | ~$1.50-3.00 | Cost analysis |
| Token Reduction | 0% | 90% | Comparison |

### Quality

| Metric | Target | Validation |
|--------|--------|------------|
| Ollama Summary Accuracy | >90% match human judgment | Manual review of 100 samples |
| Claude Synthesis Quality | Unchanged from current | User assessment |
| Data Completeness | >95% successful scrapes | Scrape metadata tracking |
| API Uptime | >99% | Monitoring logs |

---

## Coordination Checklist

### Server Team Deliverables

- [ ] YouTube scraper (Playwright)
- [ ] RSS scraper (Playwright for full articles)
- [ ] Twitter scraper (Playwright)
- [ ] Ollama integration (YouTube, RSS, Twitter)
- [ ] Database schema (3 new tables)
- [ ] `/api/research/youtube` endpoint
- [ ] `/api/research/rss` endpoint
- [ ] `/api/research/twitter` endpoint
- [ ] `/api/signals/latest` endpoint
- [ ] PM2 cron jobs (scheduled scraping)
- [ ] API documentation
- [ ] Unit tests
- [ ] Performance optimization

### Client Team Deliverables

- [ ] Update `api_client.py` (4 new methods)
- [ ] Create data transformers (3 new transformers)
- [ ] Update `run_recon.py` (pure API mode)
- [ ] Remove local scrapers (archive)
- [ ] Update PREP documentation
- [ ] Integration tests
- [ ] End-to-end validation
- [ ] Performance benchmarking

### Joint Deliverables

- [ ] API contract testing (server + client)
- [ ] Integration testing (end-to-end)
- [ ] Performance validation
- [ ] Cost analysis
- [ ] User acceptance testing
- [ ] Documentation updates
- [ ] Migration guide

---

## Questions for Server Team

1. **Ollama Server:**
   - Confirm Ollama server accessible at 192.168.10.52:11434
   - Model `gpt-oss:20b` available?
   - Any rate limits or performance constraints?

2. **Scraping:**
   - Playwright preferred, or other framework?
   - Authentication handling for Twitter (session cookies)?
   - Rate limiting strategy?

3. **Database:**
   - SQLite sufficient, or need PostgreSQL?
   - Data retention policy (7 days? 30 days?)
   - Backup strategy?

4. **Scheduling:**
   - PM2 cron jobs acceptable?
   - Scrape frequencies: YouTube (6h), RSS (30m), Twitter (30m)?
   - Error notification strategy?

5. **Timeline:**
   - 4-6 week timeline realistic?
   - Prefer sequential phases or parallel development?
   - Testing approach (continuous or end-to-end)?

---

## Next Steps

### Immediate (This Week)

1. **Server Team:** Review this document, provide feedback
2. **Client Team:** Stand by for API specs confirmation
3. **Joint:** Schedule kickoff meeting to align on timeline

### Short-Term (Next 2 Weeks)

1. **Server Team:** Start Phase 1 (YouTube API)
2. **Client Team:** Prepare client-side integration code
3. **Joint:** Weekly sync on progress

### Medium-Term (Weeks 3-6)

1. **Server Team:** Complete Phases 2-4 (RSS, Twitter, Signals)
2. **Client Team:** Integrate endpoints as they become available
3. **Joint:** Integration testing and validation

### Long-Term (Week 6+)

1. **Joint:** Final testing and performance validation
2. **Joint:** Migration to production
3. **Joint:** Monitoring and optimization

---

**Status:** ✅ **COORDINATION PLAN COMPLETE**

**Ready for:** Server team review and kickoff

**Contact:** Share this document with server AI/team for alignment

---

*Document Version: 1.0*
*Created: 2025-11-08*
*Authors: Client Team (Claude AI)*
*Purpose: Server-Client Coordination for Phase 2 API Migration*
