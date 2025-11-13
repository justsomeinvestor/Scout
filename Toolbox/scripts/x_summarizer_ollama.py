"""
X/Twitter Post Summarizer using Ollama
Reads X posts and creates summaries using local Ollama model
"""

import json
import requests
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Configuration
OLLAMA_URL = "http://192.168.10.52:11434/api/generate"
OLLAMA_MODEL = "gpt-oss:20b"
PROJECT_ROOT = Path(__file__).parent.parent.parent
X_DIR = PROJECT_ROOT / "Research" / "X"
OUTPUT_DIR = PROJECT_ROOT / "Research" / ".cache"
TODAY = datetime.now().strftime("%Y-%m-%d")

# Categories to process
CATEGORIES = ["Technicals", "Crypto", "Macro", "Bookmarks"]

SUMMARIZATION_PROMPT = """You are analyzing X/Twitter posts from a curated investment research list.

Extract and summarize from these {post_count} posts:

1. **Overall Sentiment:** Bullish/Bearish/Mixed (with %)
2. **Top Trending Tickers:** List top 5-10 most mentioned tickers with context
3. **Key Narratives:** 3-5 dominant themes or discussions
4. **Notable Calls:** Any specific price predictions, technical levels, or trade ideas
5. **Institutional/Whale Activity:** Mentions of large players or accumulation
6. **Risk Warnings:** Any caution flags or bearish warnings
7. **High-Engagement Posts:** Summarize top 3-5 posts by engagement (likes + retweets)

Keep it concise but capture all trading-relevant information. Focus on actionable insights.

Posts:
{posts_json}

Summary:"""


def find_latest_x_files():
    """Find the most recent X post JSON files for each category"""
    files = {}

    for category in CATEGORIES:
        category_dir = X_DIR / category
        if not category_dir.exists():
            print(f"   [WARN] Category directory not found: {category}")
            continue

        # Look for timestamped JSON files (exclude _last_run metadata file)
        json_files = [
            f for f in category_dir.glob("x_list_posts_*.json")
            if "last_run" not in f.name
        ]

        if not json_files:
            print(f"   [WARN] No post files in: {category}")
            continue

        # Get most recent file
        latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
        files[category] = latest_file

    return files


def load_posts(file_path):
    """Load posts from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        posts = json.load(f)

    if not isinstance(posts, list):
        return []

    return posts


def prepare_posts_for_prompt(posts, max_posts=100):
    """Prepare posts for Ollama prompt, limiting to most relevant posts"""

    # If too many posts, select most engaged ones
    if len(posts) > max_posts:
        # Sort by engagement (likes + retweets)
        sorted_posts = sorted(
            posts,
            key=lambda p: p.get('like_count', 0) + p.get('retweet_count', 0),
            reverse=True
        )
        posts = sorted_posts[:max_posts]

    # Format posts as readable text
    formatted_posts = []
    for i, post in enumerate(posts, 1):
        text = post.get('text', '')
        author = post.get('author', 'Unknown')
        likes = post.get('like_count', 0)
        retweets = post.get('retweet_count', 0)

        formatted = f"[{i}] @{author} (❤️ {likes} | 🔄 {retweets})\n{text}\n"
        formatted_posts.append(formatted)

    return "\n".join(formatted_posts)


def summarize_with_ollama(posts, category):
    """Send posts to Ollama for summarization"""

    post_count = len(posts)
    posts_text = prepare_posts_for_prompt(posts)

    prompt = SUMMARIZATION_PROMPT.format(
        post_count=post_count,
        posts_json=posts_text
    )

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    print(f"\n[CATEGORY] Processing: {category}")
    print(f"   Total posts: {post_count}")
    print(f"   Posts in prompt: {len(posts) if len(posts) <= 100 else 100} (top by engagement)")
    print(f"   Sending to Ollama...")

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=300)
        response.raise_for_status()

        result = response.json()
        summary = result.get('response', '').strip()

        print(f"   [OK] Summary generated ({len(summary)} characters)")
        return summary

    except requests.exceptions.RequestException as e:
        print(f"   [ERROR] {e}")
        return None


def save_summary(category, summary, total_posts):
    """Save summary to output file"""
    output_file = OUTPUT_DIR / f"{TODAY}_x_summary_{category}.md"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# X/Twitter Summary - {category}\n")
        f.write(f"**Date:** {TODAY}\n")
        f.write(f"**Total Posts:** {total_posts}\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        f.write(summary)
        f.write("\n")

    print(f"   [SAVED] {output_file.name}")


def main():
    print("=" * 70)
    print("X/Twitter Post Summarizer (Ollama)")
    print("=" * 70)
    print(f"Date: {TODAY}")
    print(f"Ollama: {OLLAMA_URL}")
    print(f"Model: {OLLAMA_MODEL}")
    print("=" * 70)

    # Find latest X files
    print(f"\nSearching for X post files in: {X_DIR}")
    files = find_latest_x_files()

    if not files:
        print(f"\n[ERROR] No X post files found")
        return

    print(f"\n[OK] Found {len(files)} categories to process:")
    for category, file_path in files.items():
        print(f"   - {category}: {file_path.name}")

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Process each category
    print("\n" + "=" * 70)
    print("Processing categories...")
    print("=" * 70)

    success_count = 0
    total_posts_processed = 0

    for category, file_path in files.items():
        try:
            # Load posts
            posts = load_posts(file_path)

            if not posts:
                print(f"\n[CATEGORY] {category}")
                print(f"   [WARN] No posts found in file")
                continue

            total_posts_processed += len(posts)

            # Summarize with Ollama
            summary = summarize_with_ollama(posts, category)

            if summary:
                # Save summary
                save_summary(category, summary, len(posts))
                success_count += 1

        except Exception as e:
            print(f"\n[CATEGORY] {category}")
            print(f"   [ERROR] Unexpected error: {e}")
            continue

    # Final report
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total categories: {len(files)}")
    print(f"Successfully processed: {success_count}")
    print(f"Failed: {len(files) - success_count}")
    print(f"Total posts analyzed: {total_posts_processed}")
    print(f"\nOutput directory: {OUTPUT_DIR}")
    print(f"Output files:")
    for category in files.keys():
        output_file = OUTPUT_DIR / f"{TODAY}_x_summary_{category}.md"
        if output_file.exists():
            print(f"   - {output_file.name}")
    print("=" * 70)


if __name__ == "__main__":
    main()
