# Scraper Systems Documentation
**Purpose:** Technical documentation for server migration evaluation
**Date:** 2025-11-08
**Target Server:** 192.168.10.56:3000

---

## Executive Summary

This document provides comprehensive technical documentation for the three scraper systems currently running locally. The goal is to evaluate migrating these scrapers to the API server to reduce local execution time and token usage.

### Migration Difficulty Assessment

| Scraper | Complexity | Server-Ready | Migration Difficulty |
|---------|-----------|--------------|---------------------|
| RSS Scraper | Low | ✅ Yes | **EASY** - HTTP only, no dependencies |
| YouTube Scraper | Medium | ✅ Yes | **EASY** - API-based, minimal deps |
| X/Twitter Scraper | High | ⚠️ Partial | **HARD** - Browser required, auth needed |

### Quick Recommendation

**Migrate Immediately:**
- ✅ RSS Scraper (trivial migration)
- ✅ YouTube Scraper (easy migration)

**Requires Planning:**
- ⚠️ X/Twitter Scraper (complex, needs browser + auth strategy)

---

## 1. RSS Scraper

### Executive Summary

**File:** `Scraper/rss_scraper.py`
**Lines:** ~400 lines
**Migration Difficulty:** ⭐ EASY (1/5)
**Server-Ready:** ✅ YES

Pure HTTP-based scraper with no browser requirements. Perfect candidate for immediate server migration.

---

### Technical Architecture

**Language:** Python 3.x

**Dependencies:**
```python
import feedparser      # RSS/Atom feed parsing
import requests       # HTTP requests
import json          # Data serialization
import time          # Rate limiting
from pathlib import Path
from datetime import datetime
```

**External Libraries:**
- `feedparser` - RSS/Atom feed parser (pip install feedparser)
- `requests` - HTTP library (standard)

**Browser Requirements:** None
**Authentication:** None
**Platform Dependencies:** None (cross-platform)

---

### How It Works

**1. Configuration Loading**

Reads from `Scraper/rss_feeds.json`:
```json
{
  "feeds": [
    {
      "name": "MarketWatch - Top Stories",
      "url": "https://www.marketwatch.com/rss/topstories",
      "provider": "MarketWatch",
      "enabled": true
    },
    {
      "name": "CNBC - Top News",
      "url": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
      "provider": "CNBC",
      "enabled": true
    },
    {
      "name": "Federal Reserve - Press Releases",
      "url": "https://www.federalreserve.gov/feeds/press_all.xml",
      "provider": "FederalReserve",
      "enabled": true
    }
  ]
}
```

**2. Scraping Process**

For each enabled feed:
1. Send HTTP GET request to RSS URL
2. Parse XML/RSS with feedparser
3. Extract article metadata (title, link, published date, summary)
4. Check against processed articles log (skip duplicates)
5. Save each article as individual JSON file
6. Update processed articles tracking file
7. Wait 2 seconds before next feed (rate limiting)

**3. Rate Limiting**
- 2-second delay between feeds
- No concurrent requests
- Polite scraping (respects server load)

**4. Duplicate Prevention**
- Maintains `_processed_articles.json` per provider
- Tracks article links (URLs) to avoid re-scraping
- Only processes new articles

---

### Output Format

**Directory Structure:**
```
Research/RSS/
├── MarketWatch/
│   ├── article_123456.json
│   ├── article_123457.json
│   └── _processed_articles.json
├── CNBC/
│   ├── article_789012.json
│   └── _processed_articles.json
├── FederalReserve/
│   ├── article_345678.json
│   └── _processed_articles.json
└── _archives/
    └── YYYY-MM/
        └── [archived articles]
```

**Article JSON Format:**
```json
{
  "title": "Fed Holds Rates Steady Amid Economic Uncertainty",
  "link": "https://www.marketwatch.com/story/...",
  "published": "2025-11-08T10:30:00Z",
  "summary": "The Federal Reserve announced...",
  "provider": "MarketWatch",
  "feed_name": "MarketWatch - Top Stories",
  "scraped_at": "2025-11-08T14:25:00Z"
}
```

**Processed Articles Tracking:**
```json
{
  "provider": "MarketWatch",
  "feed_name": "MarketWatch - Top Stories",
  "last_updated": "2025-11-08T14:25:00Z",
  "articles": [
    {
      "link": "https://www.marketwatch.com/story/...",
      "title": "Article Title",
      "processed_at": "2025-11-08T14:25:00Z"
    }
  ]
}
```

---

### Configuration

**Config File:** `Scraper/rss_feeds.json`

**Configurable Parameters:**
- Feed URLs
- Feed names
- Provider names
- Enabled/disabled status per feed

**Environment Variables:** None required

**Hardcoded Values:**
```python
MAX_ARTICLES_PER_FEED = 20  # Could be parameterized
REQUEST_DELAY = 2  # seconds - could be configurable
```

---

### Current Limitations

**Execution Time:** ~5-10 seconds total
- 3 feeds × 2 seconds delay = 6 seconds
- Actual scraping: 2-4 seconds
- **Fast!**

**Resource Usage:**
- Memory: <50 MB
- CPU: Minimal (I/O bound)
- Network: Lightweight (RSS feeds are small)

**Failure Points:**
- Network connectivity issues
- RSS feed URL changes (broken links)
- Malformed RSS/XML
- File system permissions

**Platform Dependencies:** None (cross-platform)

---

### Server Migration Analysis

**Headless Capability:** ✅ Already headless (no browser)

**Dependencies Needed on Server:**
```bash
pip install feedparser requests
```

**Platform Issues:** ✅ None - pure Python, cross-platform

**Migration Checklist:**
- [ ] Install feedparser on server
- [ ] Copy rss_feeds.json config
- [ ] Create Research/RSS/ directory structure
- [ ] Ensure write permissions
- [ ] Test RSS URL accessibility from server

**API Alternative Design:**

Instead of writing files locally, scraper could:
1. Scrape RSS feeds
2. POST articles to API endpoint: `/api/rss/articles`
3. Server stores in database
4. Client fetches via: `GET /api/rss/latest`

**Example API Endpoint:**
```python
@app.post('/api/rss/articles')
def receive_rss_articles(articles: List[Article]):
    # Store in database
    # Return success/failure
    pass

@app.get('/api/rss/latest')
def get_latest_rss(provider: str = None, days: int = 1):
    # Return articles from last N days
    # Filter by provider if specified
    pass
```

**Advantages of Server Migration:**
- No local file I/O
- Centralized storage
- Multiple clients can access same data
- No duplicate scraping
- Scheduled execution on server

**Migration Effort:** 2-3 hours
- 30 min: Setup environment on server
- 60 min: Modify scraper to use API instead of files
- 30 min: Test & validate

---

## 2. YouTube Scraper

### Executive Summary

**File:** `Scraper/youtube_scraper.py`
**Lines:** ~500 lines
**Migration Difficulty:** ⭐⭐ EASY (2/5)
**Server-Ready:** ✅ YES (with minor modifications)

API-based scraper using YouTube Transcript API. No browser required, but needs API access and has rate limiting considerations.

---

### Technical Architecture

**Language:** Python 3.x

**Dependencies:**
```python
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp  # YouTube video info
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
```

**External Libraries:**
- `youtube-transcript-api` - Transcript fetching
- `yt-dlp` - Video metadata (replaces deprecated youtube-dl)

**Installation:**
```bash
pip install youtube-transcript-api yt-dlp
```

**Browser Requirements:** None
**Authentication:** None (uses public YouTube API)
**Platform Dependencies:** None

---

### How It Works

**1. Configuration Loading**

Reads from `Scraper/channels.txt`:
```
# Investment & Finance Channels
@42Macro
@ARKInvest
@BenjaminCowen
@MeetKevin
@RealVision
@TheCompoundNews
# ... 20+ total channels
```

**2. Channel Processing**

For each channel:
1. Use yt-dlp to get channel info and recent videos
2. Extract video IDs (limit: 3 most recent videos per channel)
3. Check against `_processed_videos.json` (skip if already scraped)
4. For each new video:
   - Fetch transcript using YouTubeTranscriptApi
   - Save transcript to text file
   - Mark as processed

**3. Transcript Fetching**

```python
transcript = YouTubeTranscriptApi.get_transcript(video_id)
# Returns: [
#   {'text': 'Hello everyone', 'start': 0.0, 'duration': 2.5},
#   {'text': 'Today we discuss...', 'start': 2.5, 'duration': 3.0},
#   ...
# ]
```

**4. Rate Limiting & Retry Logic**

- 3 attempts per video with exponential backoff
- 5-second delay between videos
- 45-second timeout per transcript fetch
- Handles quota exceeded errors gracefully

**5. Error Handling**

Catches and logs:
- `TranscriptsDisabled` - Video has no transcripts
- `NoTranscriptFound` - No English transcript available
- `VideoUnavailable` - Video deleted/private
- `TooManyRequests` - API quota exceeded
- `Timeout` - Transcript fetch took too long

---

### Output Format

**Directory Structure:**
```
Research/YouTube/
├── 42Macro/
│   ├── VIDEO_ID_1_transcript.txt
│   ├── VIDEO_ID_2_transcript.txt
│   └── _processed_videos.json
├── ARKInvest/
│   ├── VIDEO_ID_3_transcript.txt
│   └── _processed_videos.json
└── BenjaminCowen/
    ├── VIDEO_ID_4_transcript.txt
    └── _processed_videos.json
```

**Transcript File Format** (`VIDEO_ID_transcript.txt`):
```
Video Title: Market Update - November 8, 2025
Channel: @42Macro
Video ID: ABC123XYZ
Published: 2025-11-08
URL: https://youtube.com/watch?v=ABC123XYZ

--- TRANSCRIPT ---

[00:00:00] Hello everyone, welcome back to the channel.

[00:00:15] Today we're going to discuss the recent market movements
and what they mean for investors.

[00:01:30] The Federal Reserve's latest announcement...

...
```

**Processed Videos Tracking:**
```json
{
  "channel": "@42Macro",
  "last_updated": "2025-11-08T14:30:00Z",
  "videos": [
    {
      "video_id": "ABC123XYZ",
      "title": "Market Update - November 8, 2025",
      "published": "2025-11-08T10:00:00Z",
      "processed_at": "2025-11-08T14:30:00Z",
      "transcript_available": true
    }
  ]
}
```

---

### Configuration

**Config File:** `Scraper/channels.txt`

**Configurable Parameters:**
```python
MAX_VIDEOS_PER_CHANNEL = 3  # Could be parameterized
TRANSCRIPT_TIMEOUT = 45  # seconds
RETRY_ATTEMPTS = 3
VIDEO_DELAY = 5  # seconds between videos
```

**Environment Variables:** None required

**yt-dlp Options:**
```python
ydl_opts = {
    'quiet': True,
    'extract_flat': True,
    'playlist_items': '1-3',  # Only get 3 most recent
}
```

---

### Current Limitations

**Execution Time:** 5-10 minutes
- 20 channels × 3 videos = 60 videos max
- ~5 seconds per video (with delays)
- Actual transcripts vary (some fast, some slow)

**Resource Usage:**
- Memory: ~100 MB (yt-dlp can be heavy)
- CPU: Minimal (I/O bound)
- Network: Moderate (video metadata + transcripts)

**Failure Points:**
- YouTube API quota limits (429 errors)
- Videos with transcripts disabled
- Private/deleted videos
- Network timeouts
- Channel name changes

**Rate Limiting:**
- YouTube has undocumented rate limits
- Too many requests → temporary ban (1-2 hours)
- Current implementation has conservative delays

**Platform Dependencies:**
- yt-dlp sometimes needs ffmpeg (but not for metadata only)
- Cross-platform compatible

---

### Server Migration Analysis

**Headless Capability:** ✅ Yes - no browser needed

**Dependencies Needed on Server:**
```bash
pip install youtube-transcript-api yt-dlp
```

**Platform Issues:** ✅ None - pure Python

**Migration Checklist:**
- [ ] Install youtube-transcript-api and yt-dlp
- [ ] Copy channels.txt config
- [ ] Create Research/YouTube/ directory structure
- [ ] Test API quota from server IP
- [ ] Consider rotating API keys if needed

**API Alternative Design:**

Server-based scraper could:
1. Scrape YouTube transcripts on schedule
2. Store in database with metadata
3. Expose via API:

```python
@app.get('/api/youtube/transcripts')
def get_transcripts(
    channel: str = None,
    days: int = 7,
    limit: int = 10
):
    # Return recent transcripts
    # Filter by channel, date range
    pass

@app.get('/api/youtube/transcript/{video_id}')
def get_transcript(video_id: str):
    # Return specific transcript
    pass
```

**Response Format:**
```json
{
  "success": true,
  "count": 5,
  "data": [
    {
      "video_id": "ABC123",
      "title": "Market Update",
      "channel": "@42Macro",
      "published": "2025-11-08T10:00:00Z",
      "transcript": "Full transcript text...",
      "scraped_at": "2025-11-08T14:30:00Z"
    }
  ]
}
```

**Advantages of Server Migration:**
- Centralized transcript storage
- No local file management
- Scheduled updates
- API access for multiple clients
- Better rate limit management

**Migration Effort:** 3-4 hours
- 30 min: Setup environment
- 90 min: Create API endpoints
- 60 min: Modify scraper to use database
- 30 min: Test & validate

**Considerations:**
- YouTube's rate limits apply per IP
- Server IP may have different quota than local
- Consider caching to reduce API calls
- Monitor quota usage

---

## 3. X/Twitter Scraper

### Executive Summary

**File:** `Scraper/x_scraper.py`
**Lines:** ~1,100 lines
**Migration Difficulty:** ⭐⭐⭐⭐⭐ HARD (5/5)
**Server-Ready:** ⚠️ Partial (complex migration)

Browser-based scraper using Selenium with Chrome. Requires authenticated session and has Windows-specific code. Most complex of the three scrapers.

---

### Technical Architecture

**Language:** Python 3.x

**Dependencies:**
```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import psutil  # Windows process management
from pathlib import Path
from datetime import datetime, timedelta
```

**External Libraries:**
- `selenium` - Browser automation
- `psutil` - Process management (Windows)
- Chrome WebDriver (chromedriver.exe)

**Browser Requirements:** ✅ **CRITICAL**
- Google Chrome installed
- ChromeDriver matching Chrome version
- Chrome user profile with X/Twitter login

**Authentication:** ✅ **REQUIRED**
- Uses existing Chrome profile with logged-in session
- Profile path: `C:\Users\Iccanui\AppData\Local\Google\Chrome\User Data`
- No username/password in code (session-based)

**Platform Dependencies:** ⚠️ **Windows-specific**
- Chrome profile path is Windows-specific
- psutil process management may differ on Linux
- Chrome installation location

---

### How It Works

**1. Chrome Profile Setup**

Uses existing Chrome profile to maintain login session:
```python
chrome_options = Options()
chrome_options.add_argument(
    "--user-data-dir=C:\\Users\\Iccanui\\AppData\\Local\\Google\\Chrome\\User Data"
)
chrome_options.add_argument("--profile-directory=Default")
```

**Why this matters:**
- X/Twitter blocks automated logins
- Using existing session bypasses login
- Maintains cookies and authentication tokens
- No need to handle 2FA, captchas, etc.

**2. List Scraping Process**

Scrapes 4 sources:
1. Technicals List (https://x.com/i/lists/1479448773449314306)
2. Crypto List (https://x.com/i/lists/1430346349375938572)
3. Macro List (https://x.com/i/lists/1366729121678589959)
4. Bookmarks (https://x.com/i/bookmarks)

**For each list:**
1. Navigate to list URL
2. Wait for page load (dynamic content)
3. Scroll to load posts (lazy loading)
4. Extract post elements from DOM
5. Parse post data (author, text, timestamp, engagement)
6. Filter by time window (last 24 hours)
7. Save to JSON file

**3. DOM Extraction**

X/Twitter uses dynamic class names, so scraper uses data attributes:
```python
# Find all posts
posts = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')

for post in posts:
    # Extract author
    author = post.find_element(By.CSS_SELECTOR, '[data-testid="User-Name"]')

    # Extract text
    text = post.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')

    # Extract timestamp
    time_elem = post.find_element(By.TAG_NAME, 'time')

    # Extract engagement
    likes = post.find_element(By.CSS_SELECTOR, '[data-testid="like"]')
    retweets = post.find_element(By.CSS_SELECTOR, '[data-testid="retweet"]')
```

**4. Incremental Scraping**

Only scrapes new posts since last run:
```python
SCRAPE_CUTOFF_HOURS = 24  # Only get last 24 hours

# Check post timestamp
if post_timestamp > (now - timedelta(hours=24)):
    # Save post
    pass
else:
    # Stop scrolling (older posts)
    break
```

**5. Scrolling & Lazy Loading**

X/Twitter uses infinite scroll:
```python
while posts_found < MAX_POSTS:
    # Scroll down
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for new content
    time.sleep(2)

    # Check for new posts
    new_posts = driver.find_elements(...)
```

**6. Chrome Process Cleanup**

Windows-specific process management:
```python
def kill_chrome_processes():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'chrome' in proc.info['name'].lower():
            proc.kill()
```

Ensures no zombie Chrome processes.

---

### Output Format

**Directory Structure:**
```
Research/X/
├── Technicals/
│   ├── x_list_posts_20251108.json
│   └── _archives/
│       └── 2025-11/
│           └── x_list_posts_20251101.json
├── Crypto/
│   ├── x_list_posts_20251108.json
│   └── _archives/
├── Macro/
│   ├── x_list_posts_20251108.json
│   └── _archives/
└── Bookmarks/
    ├── x_list_posts_20251108.json
    └── _archives/
```

**Post JSON Format:**
```json
{
  "list_name": "Technicals",
  "list_url": "https://x.com/i/lists/1479448773449314306",
  "scraped_at": "2025-11-08T14:45:00Z",
  "scrape_cutoff": "2025-11-07T14:45:00Z",
  "total_posts": 47,
  "posts": [
    {
      "author": "@TechnicalAnalyst",
      "handle": "TechnicalAnalyst",
      "text": "SPY breaking above key resistance at 585...",
      "timestamp": "2025-11-08T10:30:00Z",
      "post_url": "https://x.com/TechnicalAnalyst/status/123456789",
      "engagement": {
        "likes": 245,
        "retweets": 32,
        "replies": 18
      },
      "has_media": true,
      "has_link": false
    }
  ]
}
```

---

### Configuration

**Config:** Hardcoded list URLs in script

**Lists:**
```python
LISTS = {
    "Technicals": "https://x.com/i/lists/1479448773449314306",
    "Crypto": "https://x.com/i/lists/1430346349375938572",
    "Macro": "https://x.com/i/lists/1366729121678589959",
    "Bookmarks": "https://x.com/i/bookmarks"
}
```

**Configurable Parameters:**
```python
SCRAPE_CUTOFF_HOURS = 24  # Time window
MAX_SCROLL_ATTEMPTS = 20  # Scroll limit
SCROLL_DELAY = 2  # seconds between scrolls
PAGE_LOAD_TIMEOUT = 30  # seconds
```

**Chrome Profile Path:**
```python
CHROME_PROFILE = "C:\\Users\\Iccanui\\AppData\\Local\\Google\\Chrome\\User Data"
```

**Environment Variables:** None

---

### Current Limitations

**Execution Time:** 2-5 minutes
- 4 lists/sources
- Scrolling is slow (lazy loading)
- Network-dependent
- DOM parsing overhead

**Resource Usage:**
- Memory: ~500 MB - 1 GB (Chrome is heavy)
- CPU: Moderate (Chrome rendering)
- Network: Heavy (loading images, media)

**Failure Points:**
- Chrome crashes
- X/Twitter layout changes (breaks selectors)
- Session expires (needs re-login)
- Rate limiting (too many requests)
- Network timeouts
- Chrome process zombies

**Platform Dependencies:**
- Windows-specific Chrome profile path
- psutil process management
- Chrome installation location
- ChromeDriver version matching

**Session Management:**
- Relies on persistent Chrome session
- Session can expire
- No automatic re-authentication
- Manual login required if session lost

---

### Server Migration Analysis

**Headless Capability:** ⚠️ Partial
- Chrome can run headless (`--headless=new`)
- But X/Twitter detects headless mode
- May block or show different content
- Authentication harder in headless

**Dependencies Needed on Server:**
```bash
# Ubuntu/Linux
apt-get install -y chromium-browser chromium-chromedriver
pip install selenium psutil

# Or Docker
FROM selenium/standalone-chrome:latest
```

**Platform Issues:** ⚠️ Significant

1. **Chrome Profile Path**
   - Windows: `C:\Users\...\AppData\Local\Google\Chrome\User Data`
   - Linux: `/home/user/.config/google-chrome/`
   - Need to recreate authenticated session on server

2. **Process Management**
   - psutil works differently on Linux
   - Different process names
   - Different kill mechanisms

3. **ChromeDriver**
   - Must match Chrome version on server
   - Version management required

**Authentication Challenge:** ⚠️ **MAJOR BLOCKER**

How to maintain X/Twitter login on server:

**Option 1: Transfer Chrome Profile**
- Copy entire Chrome profile to server
- Risks: Session expires, security concerns
- Maintenance: Need to re-login manually on server

**Option 2: Cookie Transfer**
- Extract auth cookies from local Chrome
- Inject into server Chrome session
- Risks: Cookies expire, X may detect
- Maintenance: Regular cookie refresh

**Option 3: API Alternative**
- Use X/Twitter API v2 (requires paid plan)
- No scraping needed
- Costs: $100-$5,000/month depending on tier
- Benefits: Official, reliable, no scraping issues

**Option 4: Hybrid Approach**
- Keep X scraper local (where login exists)
- Upload scraped posts to server API
- Server stores and serves data
- Benefits: Works now, no auth issues

**Migration Checklist:**
- [ ] Setup Chrome on server (headless or VNC)
- [ ] Create authenticated X session on server
- [ ] Test session persistence
- [ ] Modify file paths for Linux
- [ ] Update psutil process management
- [ ] Handle ChromeDriver version updates
- [ ] Implement session monitoring
- [ ] Create fallback for expired sessions

---

### Server Migration Recommendation

**RECOMMENDED: Hybrid Approach**

**Architecture:**
```
Local Machine:
├── Run x_scraper.py (uses local Chrome profile)
├── Scrape posts to JSON
└── POST to server: /api/x/posts

Server (192.168.10.56:3000):
├── Receive posts via API
├── Store in database
├── Expose via: GET /api/x/latest
└── Serve to dashboard
```

**Benefits:**
- ✅ No authentication issues (uses local login)
- ✅ No Chrome setup on server
- ✅ Simpler migration
- ✅ Works immediately
- ✅ Can still run scrapers in parallel

**API Design:**
```python
@app.post('/api/x/posts')
def receive_x_posts(list_name: str, posts: List[Post]):
    # Store posts in database
    # Tag with list_name, timestamp
    # Return success
    pass

@app.get('/api/x/latest')
def get_latest_x_posts(
    list_name: str = None,
    hours: int = 24,
    limit: int = 100
):
    # Return recent posts
    # Filter by list, time range
    # Sort by timestamp desc
    pass
```

**Migration Effort:** 2-3 hours
- 60 min: Create API endpoints on server
- 30 min: Modify scraper to POST results
- 30 min: Test & validate
- 30 min: Update Scout collector to use API

**Alternative: Full Server Migration**

**Effort:** 8-12 hours
- 2 hours: Setup Chrome on server
- 3 hours: Create authenticated session
- 2 hours: Modify code for Linux
- 2 hours: Test & debug
- 2 hours: Session management & monitoring

**Risks:**
- Session persistence issues
- X/Twitter detection of automation
- Complex debugging (server vs local)
- Ongoing maintenance burden

---

## Server Migration Strategy

### Immediate Wins (Week 1)

**1. RSS Scraper → Server** ⚡ Priority 1
- **Effort:** 2-3 hours
- **Complexity:** Low
- **Benefits:** Immediate, centralized news data

**Steps:**
1. Install feedparser on server
2. Create `/api/rss/` endpoints
3. Migrate scraper to run on server
4. Test & validate

**2. YouTube Scraper → Server** ⚡ Priority 2
- **Effort:** 3-4 hours
- **Complexity:** Low-Medium
- **Benefits:** Centralized transcripts, quota management

**Steps:**
1. Install youtube-transcript-api on server
2. Create `/api/youtube/` endpoints
3. Migrate scraper to run on server
4. Monitor API quotas

### Medium-Term (Week 2-3)

**3. X/Twitter → Hybrid Approach** ⚡ Priority 3
- **Effort:** 2-3 hours
- **Complexity:** Medium
- **Benefits:** Works immediately, no auth issues

**Steps:**
1. Create `/api/x/` endpoints on server
2. Modify x_scraper.py to POST results
3. Keep scraper running locally
4. Update Scout to fetch from API

### Long-Term (Month 2+)

**4. Full X/Twitter Server Migration** (Optional)
- **Effort:** 8-12 hours
- **Complexity:** High
- **Benefits:** Fully centralized, scheduled execution
- **Risks:** Authentication, maintenance

**Consider only if:**
- Hybrid approach proves insufficient
- Need scheduled X scraping on server
- Have time for complex setup
- Willing to manage Chrome on server

---

## API Endpoint Design

### Unified Data API

All scrapers would feed into unified API:

```
GET  /api/data/summary              # All latest data
GET  /api/rss/latest                # RSS articles
GET  /api/youtube/transcripts       # YouTube videos
GET  /api/x/posts                   # X/Twitter posts

POST /api/rss/ingest                # Upload RSS articles
POST /api/youtube/ingest            # Upload transcripts
POST /api/x/ingest                  # Upload X posts
```

### Integration with Existing `/api/summary`

Extend current summary endpoint:
```json
{
  "success": true,
  "timestamp": "2025-11-08T15:00:00Z",
  "etf_data": { ... },
  "vix_data": { ... },
  "max_pain_data": { ... },
  "chat_messages": { ... },

  // NEW: Scraped data
  "rss_articles": {
    "count": 25,
    "data": [ ... ]
  },
  "youtube_videos": {
    "count": 15,
    "data": [ ... ]
  },
  "x_posts": {
    "count": 120,
    "data": [ ... ]
  }
}
```

This would make Scout's collector even simpler:
```python
# Single API call gets EVERYTHING
summary = api.get_summary()

# Already has:
# - Market data (ETF, VIX, Max Pain)
# - RSS articles
# - YouTube transcripts
# - X/Twitter posts
```

---

## Summary & Recommendations

### Migration Priority

1. **RSS Scraper** → Migrate immediately ✅
   - Trivial migration
   - No dependencies
   - Immediate benefit

2. **YouTube Scraper** → Migrate next ✅
   - Easy migration
   - Minor dependencies
   - Good benefit

3. **X/Twitter Scraper** → Hybrid approach ⚠️
   - Keep local, POST results to server
   - Avoid authentication complexity
   - Works immediately

### Expected Impact

**Before Migration:**
- Scout runs 3 scrapers locally (2-5 minutes)
- Heavy local resource usage
- File I/O overhead
- Duplicate scraping if multiple clients

**After Migration:**
- Scout calls single `/api/summary` endpoint (<5 seconds)
- Server handles all scraping
- Centralized data storage
- Single source of truth
- Scheduled updates

**Time Savings:**
- Current: 2-5 minutes scraping + processing
- After: <5 seconds API call
- **Improvement: 95%+ faster**

**Token Savings:**
- No local scraper execution logs
- No file reading overhead
- Direct data from API
- **Estimated: 50%+ reduction in tokens**

---

## Next Steps

### For Server Team

1. **Review this documentation**
2. **Start with RSS scraper** (easiest)
3. **Create `/api/rss/` endpoints**
4. **Test with sample data**
5. **Move to YouTube scraper**
6. **Discuss X/Twitter strategy** (hybrid vs full migration)

### For Client Team (Scout)

1. **Wait for `/api/rss/` and `/api/youtube/` endpoints**
2. **Test API connectivity**
3. **Update Scout collector.py** to use new endpoints
4. **Remove local scraper calls** (once API verified)
5. **Test end-to-end**

### Timeline Estimate

- **RSS Migration:** Week 1 (2-3 hours)
- **YouTube Migration:** Week 1-2 (3-4 hours)
- **X Hybrid Approach:** Week 2 (2-3 hours)
- **Scout Integration:** Week 2-3 (2-3 hours)

**Total:** 10-15 hours of work over 2-3 weeks

---

## Questions for Server Team

1. **Database:** What database is the server using? (SQLite, PostgreSQL, etc.)
2. **Storage:** File storage vs database for transcripts/articles?
3. **Scheduling:** Cron jobs available on server?
4. **API Framework:** FastAPI, Flask, Express, other?
5. **Authentication:** Any API authentication needed? (for POST endpoints)
6. **Rate Limits:** Any concerns about YouTube API quotas from server IP?
7. **X/Twitter:** Preference on hybrid vs full server migration?

---

**Document Created:** 2025-11-08
**Last Updated:** 2025-11-08
**Version:** 1.0
**Status:** Ready for server team review
