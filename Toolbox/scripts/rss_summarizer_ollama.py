"""
RSS Article Summarizer using Ollama
Reads RSS article files and creates structured summaries using local Ollama model
"""

import os
import requests
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Configuration
OLLAMA_URL = "http://192.168.10.52:11434/api/generate"
OLLAMA_MODEL = "gpt-oss:20b"
RSS_DIR = r"C:\Users\Iccanui\Desktop\Investing\Research\RSS"
OUTPUT_DIR = r"C:\Users\Iccanui\Desktop\Investing\Research\.cache"
TODAY = datetime.now().strftime("%Y-%m-%d")

EXTRACTION_PROMPT = """Extract from this RSS article:
1. Headline (article title)
2. Key points (3-5 bullets, be specific)
3. Sentiment: Bullish/Bearish/Neutral/Mixed
4. Market impact: HIGH/MEDIUM/LOW
5. Tickers or levels mentioned (if any)

Keep it factual. No interpretation or analysis.

Article:
{article_content}

Summary:"""


def find_today_articles():
    """Find all RSS articles from today"""
    articles = []
    rss_path = Path(RSS_DIR)

    for provider_dir in rss_path.iterdir():
        if provider_dir.is_dir():
            for file in provider_dir.glob(f"{TODAY}_*.md"):
                articles.append({
                    'path': str(file),
                    'provider': provider_dir.name,
                    'filename': file.name
                })

    return articles


def read_article(file_path):
    """Read article content from markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract just the content section (after ## Content)
    if "## Content" in content:
        article_text = content.split("## Content")[1].strip()
    elif "## Summary" in content:
        article_text = content.split("## Summary")[1].strip()
    else:
        article_text = content

    return article_text


def summarize_with_ollama(article_content, provider, filename):
    """Send article to Ollama for summarization"""

    prompt = EXTRACTION_PROMPT.format(article_content=article_content)

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    print(f"\n[ARTICLE] Processing: {provider} - {filename[:60]}")
    print(f"   Content length: {len(article_content):,} characters")
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


def save_summary(provider, filename, summary, summaries_by_provider):
    """Accumulate summary for later batch save"""
    if provider not in summaries_by_provider:
        summaries_by_provider[provider] = []

    summaries_by_provider[provider].append({
        'filename': filename,
        'summary': summary
    })

    print(f"   [QUEUED] Will save to provider summary file")


def write_provider_summaries(summaries_by_provider):
    """Write all summaries grouped by provider"""
    for provider, summaries in summaries_by_provider.items():
        output_file = Path(OUTPUT_DIR) / f"{TODAY}_rss_summary_{provider}.md"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# RSS Summaries - {provider}\n\n")
            f.write(f"**Date:** {TODAY}\n")
            f.write(f"**Provider:** {provider}\n")
            f.write(f"**Articles Summarized:** {len(summaries)}\n\n")
            f.write("---\n\n")

            for item in summaries:
                f.write(f"## {item['filename']}\n\n")
                f.write(item['summary'])
                f.write("\n\n---\n\n")

        print(f"\n[SAVED] {output_file.name} ({len(summaries)} articles)")


def main():
    print("=" * 70)
    print("RSS Article Summarizer (Ollama)")
    print("=" * 70)
    print(f"Date: {TODAY}")
    print(f"Ollama: {OLLAMA_URL}")
    print(f"Model: {OLLAMA_MODEL}")
    print("=" * 70)

    # Find articles
    articles = find_today_articles()

    if not articles:
        print(f"\n[ERROR] No RSS articles found for {TODAY}")
        return

    print(f"\n[OK] Found {len(articles)} articles to process:")
    for a in articles:
        print(f"   - {a['provider']}: {a['filename'][:50]}")

    # Process each article
    print("\n" + "=" * 70)
    print("Processing articles...")
    print("=" * 70)

    success_count = 0
    summaries_by_provider = defaultdict(list)

    for a in articles:
        try:
            # Read article content
            article_content = read_article(a['path'])

            # Summarize with Ollama
            summary = summarize_with_ollama(article_content, a['provider'], a['filename'])

            if summary:
                # Queue summary for batch save
                save_summary(a['provider'], a['filename'], summary, summaries_by_provider)
                success_count += 1

        except Exception as e:
            print(f"   [ERROR] Unexpected error: {e}")
            continue

    # Write all summaries to files
    print("\n" + "=" * 70)
    print("Writing summary files...")
    print("=" * 70)

    if summaries_by_provider:
        write_provider_summaries(summaries_by_provider)

    # Final report
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total articles: {len(articles)}")
    print(f"Successfully processed: {success_count}")
    print(f"Failed: {len(articles) - success_count}")
    print(f"\nOutput directory: {OUTPUT_DIR}")
    print("=" * 70)


if __name__ == "__main__":
    main()
