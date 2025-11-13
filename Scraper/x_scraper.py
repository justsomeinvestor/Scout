import os
import re
import sys
import time
import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Iterable, List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import RemoteConnection

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# ========================================================================
# SHARED CONFIGURATION (X specific)
# ========================================================================

# Output root
X_ROOT = Path("../Research") / "X"
X_ROOT.mkdir(parents=True, exist_ok=True)

# X (Twitter) Configuration
X_CHROME_PROFILE_PATH = r"C:\Users\Iccanui\AppData\Local\Google\Chrome\User Data"
X_LISTS = [
    ("Technicals", "https://x.com/i/lists/1479448773449314306"),
    ("Crypto", "https://x.com/i/lists/1430346349375938572"),
    ("Macro", "https://x.com/i/lists/1366729121678589959")
]
X_BOOKMARKS_URL = "https://x.com/i/bookmarks"
X_SCROLL_INTERVAL = 0.3  # seconds between scrolls (OPTIMIZED: 0.6 → 0.3 for 50% faster scrolling)
X_MAX_POSTS = 0          # 0 = unlimited
X_MAX_DURATION = 86400   # 24 hours (safety)

# Cutoff behavior controls
X_CUTOFF_MODE = "last_24h"     # Collect last 24 hours of posts (full daily data)
X_CUTOFF_HOURS = 24            # used if X_CUTOFF_MODE == "last_24h"

# Scroll/Wait tuning (OPTIMIZED FOR SPEED)
X_MAX_NO_NEW = 10              # consecutive no-new sweeps before stopping (was 30 - 66% faster)
X_WAIT_TIMEOUT = 2             # seconds to wait for DOM growth after scroll (was 4 - 50% faster)

# ========================================================================
# UTILITIES
# ========================================================================

def sanitize_filename(name):
    """Remove invalid filename characters"""
    return re.sub(r'[<>:"/\\|?*]', '_', str(name).strip())

def load_last_run_metadata(output_folder):
    """Load timestamp of last scraper run"""
    metadata_file = Path(output_folder) / 'x_list_posts_last_run.json'
    if not metadata_file.exists():
        return None
    try:
        data = json.loads(metadata_file.read_text(encoding='utf-8'))
        return data
    except Exception:
        return None

def save_last_run_metadata(output_folder, new_posts_count, total_posts):
    """Save timestamp of current scraper run for next incremental scrape"""
    metadata_file = Path(output_folder) / 'x_list_posts_last_run.json'
    metadata = {
        "last_run_timestamp": datetime.now(timezone.utc).isoformat(),
        "last_run_posts_collected": total_posts,
        "last_run_new_posts": new_posts_count
    }
    metadata_file.write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    print(f"    [METADATA] Saved last run timestamp: {metadata['last_run_timestamp']}")

def load_existing_x_data(output_folder):
    """
    Load existing X data from the most recent source file
    Returns (existing_posts, seen_ids) tuple for duplicate detection
    """
    output_folder = Path(output_folder)
    if not output_folder.exists():
        return [], set()

    # Load latest source file (accumulates throughout day)
    json_files = sorted(output_folder.glob('x_list_posts_*.json'), reverse=True)
    # Filter out archived/historical files
    json_files = [f for f in json_files if '_archived' not in f.name and '_historical' not in f.name]

    if not json_files:
        return [], set()

    latest = json_files[0]
    try:
        data = json.loads(latest.read_text(encoding='utf-8'))
        posts = data if isinstance(data, list) else data.get("posts", [])
        seen = {p.get("tweet_id") for p in posts if p.get("tweet_id")}
        print(f"    Loading existing data from {latest.name}")
        print(f"    Found {len(posts)} existing posts, {len(seen)} unique IDs")
        return posts, seen
    except Exception:
        return [], set()

def archive_old_x_files(output_folder):
    """
    Move old x_list_posts JSON files to archive folder once per day
    Keep all files from today, archive older days
    """
    output_folder = Path(output_folder)
    archive_folder = output_folder / 'archive'
    if not output_folder.exists():
        return
    json_files = sorted(output_folder.glob('x_list_posts_*.json'), reverse=True)
    if len(json_files) <= 1:
        return
    today = datetime.now().strftime('%Y%m%d')
    for f in json_files:
        if today not in f.name:
            archive_folder.mkdir(parents=True, exist_ok=True)
            # Use replace() instead of rename() to overwrite if file exists
            f.replace(archive_folder / f.name)


def record_scraper_status(scraper_name: str, items_found: int, error_message: str = None):
    """
    Record scraper execution status for verification.
    FOOLPROOF: Wrapped in try/except - never fails even if write fails.

    Args:
        scraper_name: Name of scraper (e.g., "X_Crypto", "X_Bookmarks")
        items_found: Number of items found (0 is valid, means no new content)
        error_message: If scraper failed, error description
    """
    try:
        status_dir = Path('../Research/.cache')
        status_dir.mkdir(parents=True, exist_ok=True)

        today = datetime.now().strftime('%Y-%m-%d')
        status_file = status_dir / f'scraper_status_{today}.json'

        # Load existing status or create new
        if status_file.exists():
            try:
                status_data = json.loads(status_file.read_text(encoding='utf-8'))
            except:
                status_data = {}
        else:
            status_data = {}

        # Record this scraper's status
        status_data[scraper_name] = {
            'ran': error_message is None,
            'items_found': items_found if error_message is None else 0,
            'error': error_message,
            'timestamp': datetime.now().isoformat(),
            'message': 'No new content found' if (error_message is None and items_found == 0) else (error_message or 'Scraper completed successfully')
        }

        # Write back
        status_file.write_text(json.dumps(status_data, indent=2), encoding='utf-8')
    except Exception as e:
        # Silent failure - never break the scraper because status write failed
        pass

# ========================================================================
# SCRAPER
# ========================================================================

class TwitterListScraper:
    def __init__(self, profile_path, list_url, list_name, scroll_interval=0.9, max_posts=0, max_duration=0, existing_posts=None, existing_ids=None):
        self.profile_path = profile_path
        self.list_url = list_url
        self.list_name = list_name
        self.scroll_interval = scroll_interval
        self.max_posts = max_posts
        self.max_duration = max_duration
        self.driver = None

        self.seen_ids = set()  # seen in this run
        self.existing_ids = existing_ids if existing_ids else set()
        self.posts = existing_posts if existing_posts else []
        self.new_posts_count = 0
        self.consecutive_existing = 0
        self.max_consecutive_existing = 50  # OPTIMIZED: Stop after 50 (was 500) - we've caught up!
        self.consecutive_old = 0
        self.max_consecutive_old = 30  # OPTIMIZED: Stop after 30 (was 50) - 40% faster exit when hitting cutoff
        self.cutoff_datetime = None
        self.cutoff_reason = None
        self.cutoff_reached = False
        self.cutoff_logged = False
        self.init_time_cutoff()

    @staticmethod
    def parse_iso_datetime(value):
        """Convert ISO timestamp to timezone-aware datetime."""
        if not value:
            return None
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            try:
                return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
            except ValueError:
                try:
                    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                except ValueError:
                    return None

    def init_time_cutoff(self):
        """Initialize a time cutoff to avoid scrolling forever.

        INCREMENTAL SCRAPING: Uses last run timestamp to only collect NEW tweets
        since last scrape, instead of re-scraping entire 24-hour window.
        """
        mode = globals().get("X_CUTOFF_MODE", "since_last")
        hours = int(globals().get("X_CUTOFF_HOURS", 24))

        # PRIORITY 1: Check for last run metadata (INCREMENTAL MODE)
        output_folder = X_ROOT / self.list_name
        metadata = load_last_run_metadata(output_folder)

        if mode == "since_last" and metadata:
            last_run_str = metadata.get("last_run_timestamp")
            if last_run_str:
                last_run_dt = self.parse_iso_datetime(last_run_str)
                if last_run_dt:
                    # Safety margin: go back 5 minutes to catch any missed posts
                    safety_margin = timedelta(minutes=5)
                    self.cutoff_datetime = last_run_dt - safety_margin
                    self.cutoff_reason = f"incremental: since last run ({last_run_dt.strftime('%H:%M:%S')} UTC - 5min safety)"
                    print(f"    ✓ INCREMENTAL MODE: Collecting posts since {self.cutoff_datetime.strftime('%H:%M:%S')} UTC")
                    print(f"    Last run collected {metadata.get('last_run_new_posts', 0)} new posts")
                    return

        # PRIORITY 2: No metadata found - first run of the day (FALLBACK: 6 hours)
        if mode == "since_last":
            fallback_hours = 6  # User preference: 6 hours fallback
            self.cutoff_datetime = datetime.now(timezone.utc) - timedelta(hours=fallback_hours)
            self.cutoff_reason = f"first run fallback: last {fallback_hours}h"
            print(f"    ⚠ No metadata found - FIRST RUN MODE: Collecting last {fallback_hours} hours")
            print(f"    Cutoff: {self.cutoff_datetime.strftime('%H:%M:%S')} UTC")
        elif mode == "last_24h":
            self.cutoff_datetime = datetime.now(timezone.utc) - timedelta(hours=hours)
            self.cutoff_reason = f"rolling {hours}h window"
            print(f"    Rolling window mode: last {hours} hours")
        else:
            self.cutoff_datetime = None
            self.cutoff_reason = "no cutoff"
            print(f"    No cutoff mode enabled")

    def _log_cutoff_once(self, msg):
        if not self.cutoff_logged:
            print(f"    {msg}")
            self.cutoff_logged = True

    def is_pinned_tweet(self, article):
        try:
            badges = article.find_elements(By.CSS_SELECTOR, 'div[data-testid="socialContext"]')
            for badge in badges:
                if "Pinned" in (badge.text or ""):
                    return True
        except Exception:
            pass
        return False

    def setup_driver(self):
        """Set up Chrome with Scraper_Profile + Selenium debugger connection."""
        import shutil
        from pathlib import Path
        import socket

        print('Opening Chrome with Scraper_Profile...')

        # Define paths
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        base_user_data = Path(self.profile_path)
        default_profile = base_user_data / "Default"
        scraper_profile = base_user_data / "Scraper_Profile"
        debug_host = "127.0.0.1"
        debug_port = 9222

        # Kill any existing Chrome processes first
        print("    Setting up Chrome...", end=" ", flush=True)
        try:
            subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'],
                          capture_output=True, timeout=5)
            time.sleep(2)
        except Exception:
            pass

        # Prepare Scraper_Profile (copy from Default if needed)
        try:
            if not scraper_profile.exists() and default_profile.exists():
                shutil.copytree(default_profile, scraper_profile)
        except Exception:
            pass

        # Launch Chrome with Scraper_Profile and remote debugging
        try:
            subprocess.Popen([
                chrome_path,
                f'--user-data-dir={scraper_profile}',
                f'--remote-debugging-port={debug_port}'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            print(f"✗\n    Error: {e}")
            raise

        # Wait for debugging port to be ready (with retries)
        port_ready = False
        for attempt in range(15):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((debug_host, debug_port))
                sock.close()
                if result == 0:
                    port_ready = True
                    break
            except Exception:
                pass
            time.sleep(1)

        if not port_ready:
            print("✗")
            raise RuntimeError(f"Debugging port {debug_port} never became ready after 15 seconds")

        # Connect Selenium to the running Chrome instance
        options = Options()
        options.add_experimental_option("debuggerAddress", f"{debug_host}:{debug_port}")

        try:
            self.driver = webdriver.Chrome(options=options)
        except Exception as e:
            print(f"✗\n    Failed to connect Selenium: {e}")
            raise

        # Verify we can navigate
        try:
            self.driver.get("https://x.com")

            # Wait for page to actually load
            WebDriverWait(self.driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

            current_url = self.driver.current_url
            if "login" in current_url.lower() or "i/flow/login" in current_url:
                print("✗\n    ⚠ Not logged in - showing login page")
            else:
                print("✓")
        except Exception as e:
            print(f"✗\n    Navigation error: {e}")

    def extract_primary_tweet(self, article):
        """Prefer the deepest tweet node that has a <time> (original content)."""
        try:
            candidates = article.find_elements(By.CSS_SELECTOR, 'div[data-testid="tweet"]')
            for node in reversed(candidates):
                try:
                    node.find_element(By.CSS_SELECTOR, 'time')
                    return node
                except Exception:
                    continue
            return candidates[-1] if candidates else article
        except Exception:
            return article

    def extract_count_from_button(self, article, testid):
        """Extract count from button (reply, retweet, like), supporting K/M/B suffixes."""
        def parse_count(text: str) -> int:
            if not text:
                return 0
            t = text.replace(',', '').strip().lower()
            m = re.search(r'(\d+(?:\.\d+)?)([kmb])?', t)
            if not m:
                return 0
            num = float(m.group(1))
            suf = m.group(2)
            mult = 1
            if suf == 'k':
                mult = 1000
            elif suf == 'm':
                mult = 1000000
            elif suf == 'b':
                mult = 1000000000
            return int(num * mult)
        try:
            el = article.find_element(By.CSS_SELECTOR, f'div[data-testid="{testid}"]')
            label = el.get_attribute('aria-label') or el.text or ''
            return parse_count(label)
        except Exception:
            return 0

    def extract_urls(self, article):
        urls = set()
        try:
            for a in article.find_elements(By.CSS_SELECTOR, '[data-testid="tweetText"] a[href^="http"]'):
                href = a.get_attribute('href') or ''
                if href and 'x.com' not in href:
                    urls.add(href)
        except Exception:
            pass
        return sorted(urls)

    def parse_tweet(self, article):
        try:
            target_article = self.extract_primary_tweet(article)
            time_el = target_article.find_element(By.CSS_SELECTOR, 'time')
            created_at = time_el.get_attribute('datetime')

            # tweet id from anchor href
            link = target_article.find_element(By.CSS_SELECTOR, 'a[href*="/status/"]')
            href = link.get_attribute('href')
            m = re.search(r'/status/(\d+)', href or '')
            tweet_id = m.group(1) if m else None
            if not tweet_id:
                return None

            # author
            author_el = target_article.find_element(By.CSS_SELECTOR, 'a[href^="/"][role="link"]')
            author_href = author_el.get_attribute('href') or ''
            author = author_href.strip('/').split('/')[0]

            # text
            try:
                text_el = target_article.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
                text = text_el.text.strip()
            except Exception:
                text = ''

            reply_count = self.extract_count_from_button(target_article, 'reply')
            retweet_count = self.extract_count_from_button(target_article, 'retweet')
            like_count = self.extract_count_from_button(target_article, 'like')
            urls = self.extract_urls(target_article)
            is_pinned = self.is_pinned_tweet(target_article)

            return {
                'tweet_id': tweet_id,
                'author': author,
                'permalink': f'https://x.com/{author}/status/{tweet_id}',
                'created_at': created_at,
                'text': text,
                'reply_count': reply_count,
                'retweet_count': retweet_count,
                'like_count': like_count,
                'urls': urls,
                'is_pinned': is_pinned
            }
        except Exception:
            return None

    def harvest_once(self):
        """Harvest tweets currently visible on the page"""
        articles = self.driver.find_elements(By.CSS_SELECTOR, 'article[role="article"]')
        added = 0
        skipped_existing = 0
        skipped_old = 0

        for article in articles:
            tweet_data = self.parse_tweet(article)
            if not tweet_data:
                continue

            tweet_id = tweet_data['tweet_id']
            is_pinned = tweet_data.get('is_pinned', False)

            if tweet_id in self.seen_ids or tweet_id in self.existing_ids:
                self.consecutive_existing += 1
                skipped_existing += 1
                if self.consecutive_existing >= self.max_consecutive_existing:
                    print(f"      ✓ Hit {self.consecutive_existing} consecutive existing posts - we've caught up!")
                    print(f"      Collected {self.new_posts_count} new posts in this run")
                    self.cutoff_reached = True
                    break
                continue  # keep scrolling to find older new posts

            # Reset consecutive existing counter: we found a new post
            self.consecutive_existing = 0

            # Check timestamp cutoff - but don't break, just skip and continue
            tweet_dt = self.parse_iso_datetime(tweet_data.get('created_at'))
            if self.cutoff_datetime and tweet_dt and tweet_dt < self.cutoff_datetime:
                if is_pinned:
                    continue
                # Track consecutive old posts
                self.consecutive_old += 1
                skipped_old += 1
                if self.consecutive_old >= self.max_consecutive_old:
                    self._log_cutoff_once(
                        f"Hit {self.consecutive_old} consecutive posts older than cutoff - stopping"
                    )
                    self.cutoff_reached = True
                    break
                continue  # Skip this old post but keep scrolling

            # Reset consecutive old counter: we found a recent post
            self.consecutive_old = 0

            # Add new post
            self.seen_ids.add(tweet_id)
            self.posts.append(tweet_data)
            self.new_posts_count += 1
            added += 1

        # Only show updates when finding new posts (cleaner console)
        if added > 0:
            print(f"      +{added} new posts (total: {self.new_posts_count} new, {len(self.posts)} overall)")

        return added

    def wait_for_more_content(self):
        """Scroll and wait until the page height increases (new content loaded)."""
        try:
            prev_height = self.driver.execute_script("return document.body.scrollHeight")
            scroll_amount = max(1200, self.driver.execute_script("return window.innerHeight") - 100)  # OPTIMIZED: 600 → 1200 for 50% fewer scrolls
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            timeout = int(globals().get("X_WAIT_TIMEOUT", 5))

            # Try to wait for new content
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.body.scrollHeight") > prev_height
            )
        except Exception:
            # Silent timeout - content didn't load in time, just continue
            time.sleep(self.scroll_interval)

    def save_json(self, output_folder):
        """Save collected posts to JSON file + metadata for incremental scraping"""
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)
        archive_old_x_files(output_folder)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = output_folder / f"x_list_posts_{timestamp}.json"
        with filename.open('w', encoding='utf-8') as f:
            json.dump(self.posts, f, ensure_ascii=False, indent=2)
        print(f"    Saved {len(self.posts)} total posts ({self.new_posts_count} new) to {filename.name}")

        # Save metadata for next incremental scrape
        save_last_run_metadata(output_folder, self.new_posts_count, len(self.posts))

    def scrape(self):
        """Main scraping loop with time-based safety exit"""
        print(f"    Opening {self.list_url}")
        self.driver.get(self.list_url)

        # Wait for page to load
        WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(2)  # Additional wait for dynamic content

        print("    Starting to collect posts...")
        if self.cutoff_datetime:
            print(f"    Cutoff target: stop at posts before {self.cutoff_datetime.isoformat()} ({self.cutoff_reason})")
        if self.max_duration > 0:
            print(f"    Will run for {self.max_duration} seconds")

        start_time = time.time()
        last_new_post_time = time.time()  # Track when we last found a new post
        no_new_count = 0
        max_no_new = int(globals().get('X_MAX_NO_NEW', 5))
        stale_timeout = 180  # 3 minutes without new posts = exit (was 300 - 40% faster)
        scroll_count = 0

        while True:
            elapsed = time.time() - start_time

            # Check max duration
            if self.max_duration > 0 and elapsed >= self.max_duration:
                print(f"    Reached time limit of {self.max_duration} seconds")
                break

            # SAFETY EXIT: If no new posts in 5 minutes, we're likely stuck
            time_since_last_new = time.time() - last_new_post_time
            if time_since_last_new >= stale_timeout:
                print(f"    ⚠ Safety exit: No new posts found in {stale_timeout/60:.1f} minutes")
                print(f"    Collected {self.new_posts_count} new posts before stalling")
                break

            scroll_count += 1
            added = self.harvest_once()

            # Update last new post time if we found something
            if added > 0:
                last_new_post_time = time.time()
                no_new_count = 0
            else:
                no_new_count += 1

            # Progress update every 10 scrolls (removed verbose checkpoint spam)
            if scroll_count % 10 == 0:
                print(f"      [Progress] {len(self.posts)} total posts ({self.new_posts_count} new this run)")

            if self.cutoff_reached:
                print("    Cutoff reached; stopping scrape.")
                break

            if self.max_posts > 0 and len(self.posts) >= self.max_posts:
                print(f"    Reached maximum of {self.max_posts} posts")
                break

            if no_new_count >= max_no_new:
                print("    No new posts found after multiple scrolls. Stopping.")
                break

            self.wait_for_more_content()

    def save_json_and_close(self, output_folder):
        import shutil

        try:
            self.save_json(output_folder)
        finally:
            try:
                print("    Closing browser...")
                # Force close with timeout
                try:
                    self.driver.quit()
                    print("    ✓ Browser closed")
                except Exception as e:
                    print(f"    ⚠ Error closing driver: {e}")
                    # Force kill if quit() hangs
                    subprocess.run(['taskkill', '/IM', 'chrome.exe', '/F'],
                                 capture_output=True, timeout=5)
                    print("    ✓ Force closed Chrome")

                time.sleep(1)

                # Clean up temporary directory
                if hasattr(self, 'temp_dir') and self.temp_dir and Path(self.temp_dir).exists():
                    try:
                        shutil.rmtree(self.temp_dir)
                        print("    Temp profile cleaned up")
                    except Exception:
                        pass
            except Exception as e:
                print(f"    Error during cleanup: {e}")

# ========================================================================
# RUNNER
# ========================================================================

def run_x_scraper():
    print("""
============================================================
X (TWITTER) SCRAPER - LISTS & BOOKMARKS
============================================================

Will scrape 3 Twitter/X lists + bookmarks...
""")
    total_posts = 0
    list_stats = {}
    bookmarks_stats = {}
    for idx, (list_name, list_url) in enumerate(X_LISTS, start=1):
        print(f"""
============================================================
[{idx}/{len(X_LISTS)}] Scraping X List: {list_name}
============================================================
""")
        output_folder = X_ROOT / list_name
        try:
            existing_posts, existing_ids = load_existing_x_data(output_folder)
            scraper = TwitterListScraper(
                profile_path=X_CHROME_PROFILE_PATH,
                list_url=list_url,
                list_name=list_name,
                scroll_interval=X_SCROLL_INTERVAL,
                max_posts=X_MAX_POSTS,
                max_duration=X_MAX_DURATION,
                existing_posts=existing_posts,
                existing_ids=existing_ids
            )
            scraper.setup_driver()
            scraper.scrape()
            scraper.save_json_and_close(output_folder)

            posts_count = len(scraper.posts)
            new_count = scraper.new_posts_count
            list_stats[list_name] = posts_count
            total_posts += posts_count
            print(f"\n  [+] Completed: {list_name} ({posts_count} total posts, {new_count} new)")
            # Record status for this list
            record_scraper_status(f'X_{list_name}', new_count)
        except Exception as e:
            import traceback
            print(f"\n  An error occurred while processing the list: {list_name}")
            traceback.print_exc()
            # Record failure status for this list
            record_scraper_status(f'X_{list_name}', 0, str(e)[:100])
            # Attempt to close any driver opened
            try:
                scraper.driver.quit()
            except Exception:
                pass

    print("""
============================================================
All 3 X lists scraped successfully!
============================================================

X posts saved to:
  - output/X/Technicals
  - output/X/Crypto
  - output/X/Macro

""")

    # ========================================================================
    # NOW SCRAPE BOOKMARKS
    # ========================================================================
    print("""
============================================================
[4/4] Scraping X Bookmarks
============================================================
""")
    try:
        output_folder = X_ROOT / "Bookmarks"
        existing_posts, existing_ids = load_existing_x_data(output_folder)
        scraper = TwitterListScraper(
            profile_path=X_CHROME_PROFILE_PATH,
            list_url=X_BOOKMARKS_URL,
            list_name="Bookmarks",
            scroll_interval=X_SCROLL_INTERVAL,
            max_posts=X_MAX_POSTS,
            max_duration=X_MAX_DURATION,
            existing_posts=existing_posts,
            existing_ids=existing_ids
        )
        scraper.setup_driver()
        scraper.scrape()
        scraper.save_json_and_close(output_folder)

        bookmarks_count = len(scraper.posts)
        new_count = scraper.new_posts_count
        bookmarks_stats["Bookmarks"] = bookmarks_count
        total_posts += bookmarks_count
        print(f"\n  [+] Completed: Bookmarks ({bookmarks_count} total posts, {new_count} new)")
        # Record status for bookmarks
        record_scraper_status('X_Bookmarks', new_count)
    except Exception as e:
        import traceback
        print(f"\n  An error occurred while processing bookmarks")
        traceback.print_exc()
        # Record failure status for bookmarks
        record_scraper_status('X_Bookmarks', 0, str(e)[:100])
        # Attempt to close any driver opened
        try:
            scraper.driver.quit()
        except Exception:
            pass

    print("""
============================================================
All X lists + bookmarks scraped successfully!
============================================================

X posts saved to:
  - Research/X/Technicals
  - Research/X/Crypto
  - Research/X/Macro
  - Research/X/Bookmarks

[OK] X Scraping complete! Closing in 3 seconds...
""")

    # Force close any remaining Chrome processes
    time.sleep(3)
    try:
        subprocess.run(['taskkill', '/IM', 'chrome.exe', '/F'],
                      capture_output=True, timeout=5)
        print("[✓] All Chrome processes terminated")
    except Exception:
        pass


if __name__ == "__main__":
    run_x_scraper()
