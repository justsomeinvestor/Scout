"""
Scout Data Collector
====================

Parallel data collection from all sources:
- API server (market data, YouTube transcripts, RSS articles)
- X/Twitter scraper (social sentiment - subprocess)

Migration Status:
- [DONE] RSS: Now using API (/api/rss/latest) - was subprocess
- [DONE] YouTube: Now using API (/api/youtube/latest) with Ollama summaries - was subprocess
- [TODO] X/Twitter: Still using local subprocess (no API endpoint yet)

Uses concurrent execution for speed.
"""

import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from config import config
from scripts.trading.api_client import get_client, APIClientError


class CollectionResult:
    """Container for collection results with metadata"""

    def __init__(self, source: str):
        self.source = source
        self.success = False
        self.data = None
        self.error = None
        self.duration = 0.0
        self.timestamp = datetime.now().isoformat()

    def __repr__(self):
        status = "[OK]" if self.success else "[ERROR]"
        return f"{status} {self.source}: {self.duration:.1f}s"


def collect_api_data() -> CollectionResult:
    """
    Collect market data from API server using /api/summary endpoint.

    Returns all market data in one call:
    - SPY, QQQ ETF data
    - VIX structure
    - Max Pain levels
    - Chat messages
    """
    result = CollectionResult("API Server")
    start_time = datetime.now()

    try:
        print(f"[{start_time.strftime('%H:%M:%S')}] Collecting API data...")

        with get_client() as api:
            # Health check first
            if not api.is_healthy():
                result.error = "API server offline"
                return result

            # Get all data in one call
            summary = api.get_summary()

            if not summary.get('success'):
                result.error = f"API returned error: {summary.get('error', 'Unknown')}"
                return result

            # Extract relevant data (API returns data nested under 'data' key)
            data = summary.get('data', {})
            counts = summary.get('counts', {})

            result.data = {
                'timestamp': summary.get('timestamp'),
                'etf_data': data.get('etf', []),
                'vix_data': data.get('vix', {}),
                'max_pain_data': data.get('maxPain', []),
                'chat_messages': data.get('chat', []),
                'counts': counts,
                'data_age_minutes': api.get_data_age_minutes()
            }

            result.success = True
            print(f"  [OK] API data collected ({counts.get('etf', 0)} ETFs, "
                  f"{counts.get('maxPain', 0)} max pain records)")

    except APIClientError as e:
        result.error = f"API client error: {e}"
        print(f"  [ERROR] API error: {e}")
    except Exception as e:
        result.error = f"Unexpected error: {e}"
        print(f"  [ERROR] Unexpected error: {e}")
        traceback.print_exc()
    finally:
        result.duration = (datetime.now() - start_time).total_seconds()

    return result


def collect_social_data() -> CollectionResult:
    """
    Collect X/Twitter data by running scraper.

    Returns posts from:
    - Technicals list
    - Crypto list
    - Macro list
    - Bookmarks
    """
    result = CollectionResult("X/Twitter")
    start_time = datetime.now()

    try:
        print(f"[{start_time.strftime('%H:%M:%S')}] Collecting X/Twitter data...")

        scraper_path = PROJECT_ROOT / "Scraper" / "x_scraper.py"

        if not scraper_path.exists():
            result.error = "X scraper not found"
            return result

        # Run scraper (this may take 1-2 minutes)
        process = subprocess.run(
            [sys.executable, str(scraper_path)],
            capture_output=True,
            text=True,
            timeout=180,  # 3 minute timeout
            cwd=str(PROJECT_ROOT)
        )

        if process.returncode != 0:
            result.error = f"Scraper failed: {process.stderr}"
            print(f"  [ERROR] X scraper error: {process.stderr[:200]}")
            return result

        # Parse scraped data (look for today's files)
        today = datetime.now().strftime("%Y%m%d")
        x_dir = config.paths.twitter_dir

        posts = []
        for list_dir in x_dir.iterdir():
            if not list_dir.is_dir() or list_dir.name.startswith('_'):
                continue

            # Find today's file
            post_file = list_dir / f"x_list_posts_{today}.json"
            if post_file.exists():
                with open(post_file, 'r', encoding='utf-8') as f:
                    list_posts = json.load(f)
                    posts.extend(list_posts.get('posts', []))

        result.data = {
            'posts': posts,
            'total_count': len(posts),
            'collection_date': today
        }
        result.success = True
        print(f"  [OK] X data collected ({len(posts)} posts)")

    except subprocess.TimeoutExpired:
        result.error = "Scraper timeout (>3 min)"
        print(f"  [ERROR] X scraper timeout")
    except Exception as e:
        result.error = f"Error: {e}"
        print(f"  [ERROR] X error: {e}")
        traceback.print_exc()
    finally:
        result.duration = (datetime.now() - start_time).total_seconds()

    return result


def collect_video_data() -> CollectionResult:
    """
    Collect YouTube transcript data from API server.

    Returns transcripts with Ollama summaries from investment channels.
    """
    result = CollectionResult("YouTube")
    start_time = datetime.now()

    try:
        print(f"[{start_time.strftime('%H:%M:%S')}] Collecting YouTube data from API...")

        with get_client() as api:
            # Health check first
            if not api.is_healthy():
                result.error = "API server offline"
                return result

            # Get YouTube data from API
            youtube_data = api.get_youtube_latest(limit=200)

            if not youtube_data.get('success'):
                result.error = f"API returned error: {youtube_data.get('error', 'Unknown')}"
                return result

            # Extract videos
            videos = youtube_data.get('data', [])

            # Filter to last 7 days (API returns all, we only want recent)
            cutoff = datetime.now() - timedelta(days=7)
            recent_videos = []
            for video in videos:
                scraped_at = video.get('scraped_at')
                if scraped_at:
                    # Parse ISO timestamp
                    video_time = datetime.fromisoformat(scraped_at.replace('Z', '+00:00'))
                    if video_time.replace(tzinfo=None) > cutoff:
                        recent_videos.append(video)

            # Count videos with summaries
            with_summaries = sum(1 for v in recent_videos if v.get('summary'))

            result.data = {
                'videos': recent_videos,
                'video_count': len(recent_videos),
                'total_available': len(videos),
                'with_summaries': with_summaries,
                'collection_date': datetime.now().strftime("%Y%m%d"),
                'channels': list(set(v.get('channel_name', 'Unknown') for v in recent_videos))
            }
            result.success = True
            print(f"  [OK] YouTube data collected ({len(recent_videos)} recent videos, {with_summaries} with Ollama summaries)")

    except APIClientError as e:
        result.error = f"API error: {e}"
        print(f"  [ERROR] YouTube API error: {e}")
    except Exception as e:
        result.error = f"Error: {e}"
        print(f"  [ERROR] YouTube error: {e}")
        traceback.print_exc()
    finally:
        result.duration = (datetime.now() - start_time).total_seconds()

    return result


def collect_news_data() -> CollectionResult:
    """
    Collect RSS news data from API server.

    Returns articles from:
    - MarketWatch
    - CNBC
    - Federal Reserve
    """
    result = CollectionResult("RSS News")
    start_time = datetime.now()

    try:
        print(f"[{start_time.strftime('%H:%M:%S')}] Collecting RSS data from API...")

        with get_client() as api:
            # Health check first
            if not api.is_healthy():
                result.error = "API server offline"
                return result

            # Get RSS data from API
            rss_data = api.get_rss_latest(limit=200)

            if not rss_data.get('success'):
                result.error = f"API returned error: {rss_data.get('error', 'Unknown')}"
                return result

            # Extract articles
            articles = rss_data.get('data', [])

            # Filter to last 24 hours (API returns all, we only want recent)
            cutoff = datetime.now() - timedelta(days=1)
            recent_articles = []
            for article in articles:
                scraped_at = article.get('scraped_at')
                if scraped_at:
                    # Parse ISO timestamp
                    article_time = datetime.fromisoformat(scraped_at.replace('Z', '+00:00'))
                    if article_time.replace(tzinfo=None) > cutoff:
                        recent_articles.append(article)

            result.data = {
                'articles': recent_articles,
                'article_count': len(recent_articles),
                'total_available': len(articles),
                'collection_date': datetime.now().strftime("%Y%m%d"),
                'providers': list(set(a.get('provider', 'Unknown') for a in recent_articles))
            }
            result.success = True
            print(f"  [OK] RSS data collected ({len(recent_articles)} recent articles from {len(result.data['providers'])} providers)")

    except APIClientError as e:
        result.error = f"API error: {e}"
        print(f"  [ERROR] RSS API error: {e}")
    except Exception as e:
        result.error = f"Error: {e}"
        print(f"  [ERROR] RSS error: {e}")
        traceback.print_exc()
    finally:
        result.duration = (datetime.now() - start_time).total_seconds()

    return result


def collect_all(parallel: bool = True) -> Dict[str, CollectionResult]:
    """
    Collect data from all sources.

    Args:
        parallel: Run scrapers in parallel (default: True)

    Returns:
        Dictionary of CollectionResult objects keyed by source name
    """
    print("\n" + "=" * 70)
    print("SCOUT DATA COLLECTION")
    print("=" * 70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Mode: {'Parallel' if parallel else 'Sequential'}")
    print()

    results = {}

    if parallel:
        # Run all collectors in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(collect_api_data): 'api',
                executor.submit(collect_social_data): 'social',
                executor.submit(collect_video_data): 'video',
                executor.submit(collect_news_data): 'news'
            }

            for future in as_completed(futures):
                result = future.result()
                results[result.source] = result
    else:
        # Run sequentially
        results['API Server'] = collect_api_data()
        results['X/Twitter'] = collect_social_data()
        results['YouTube'] = collect_video_data()
        results['RSS News'] = collect_news_data()

    # Summary
    print()
    print("=" * 70)
    print("COLLECTION SUMMARY")
    print("=" * 70)

    success_count = sum(1 for r in results.values() if r.success)
    total_duration = sum(r.duration for r in results.values())

    for source, result in results.items():
        print(f"{result}")

    print()
    print(f"Success Rate: {success_count}/{len(results)} sources")
    print(f"Total Duration: {total_duration:.1f}s")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    return results


if __name__ == "__main__":
    # Test collection
    results = collect_all(parallel=True)

    # Check results
    if all(r.success for r in results.values()):
        print("\nAll sources collected successfully!")
        sys.exit(0)
    else:
        print("\nWARNING: Some sources failed - check errors above")
        sys.exit(1)
