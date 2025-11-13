"""
Simple X/Twitter Data Collection

Runs the existing X scraper and reports results.
Data saved to: Research/X/{Technicals, Crypto, Macro, Bookmarks}/
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime
import json

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
SCRAPER_DIR = PROJECT_ROOT / "Scraper"
X_SCRAPER = SCRAPER_DIR / "x_scraper.py"
RESEARCH_X = PROJECT_ROOT / "Research" / "X"

def main():
    print("=" * 70)
    print("X/TWITTER DATA COLLECTION")
    print("=" * 70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Check if scraper exists
    if not X_SCRAPER.exists():
        print(f"[ERROR] X scraper not found: {X_SCRAPER}")
        sys.exit(1)

    print(f"Running X scraper...")
    print(f"  Script: {X_SCRAPER}")
    print(f"  Output: {RESEARCH_X}/")
    print()

    # Run scraper
    try:
        # Change to Scraper directory (scraper uses relative paths)
        result = subprocess.run(
            [sys.executable, "x_scraper.py"],
            cwd=str(SCRAPER_DIR),
            capture_output=False,  # Show output in real-time
            text=True
        )

        if result.returncode != 0:
            print()
            print(f"[ERROR] Scraper exited with code {result.returncode}")
            sys.exit(1)

    except KeyboardInterrupt:
        print()
        print("[CANCELLED] User interrupted")
        sys.exit(1)

    except Exception as e:
        print()
        print(f"[ERROR] Failed to run scraper: {e}")
        sys.exit(1)

    # Report results
    print()
    print("=" * 70)
    print("COLLECTION COMPLETE")
    print("=" * 70)

    categories = ["Technicals", "Crypto", "Macro", "Bookmarks"]
    total_posts = 0

    for category in categories:
        category_dir = RESEARCH_X / category
        if not category_dir.exists():
            print(f"  {category}: No data directory")
            continue

        # Look for JSON files
        json_files = list(category_dir.glob("*.json"))
        if not json_files:
            print(f"  {category}: No JSON files")
            continue

        # Count posts in most recent file
        latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                count = len(data) if isinstance(data, list) else 0
                total_posts += count
                print(f"  {category}: {count} posts ({latest_file.name})")
        except:
            print(f"  {category}: Error reading {latest_file.name}")

    print()
    print(f"Total posts collected: {total_posts}")
    print(f"Data location: {RESEARCH_X}/")
    print("=" * 70)

if __name__ == "__main__":
    main()
