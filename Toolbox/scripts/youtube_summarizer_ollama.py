"""
YouTube Transcript Summarizer using Ollama
Reads YouTube transcripts and creates summaries using local Ollama model
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime

# Configuration
OLLAMA_URL = "http://192.168.10.52:11434/api/generate"
OLLAMA_MODEL = "gpt-oss:20b"
YOUTUBE_DIR = r"C:\Users\Iccanui\Desktop\Investing\Research\YouTube"
OUTPUT_DIR = r"C:\Users\Iccanui\Desktop\Investing\Research\.cache"
TODAY = datetime.now().strftime("%Y-%m-%d")

SUMMARIZATION_PROMPT = """You are analyzing a YouTube video transcript for investment research.

Extract and summarize:
1. Main thesis or market view
2. Key data points or levels mentioned
3. Bullish or bearish sentiment
4. Any specific trading ideas or predictions
5. Overall takeaway for traders/investors

Be concise but capture all important investment-relevant information.

Transcript:
{transcript}

Summary:"""


def find_today_transcripts():
    """Find all YouTube transcripts from today"""
    transcripts = []
    youtube_path = Path(YOUTUBE_DIR)

    for channel_dir in youtube_path.iterdir():
        if channel_dir.is_dir():
            for file in channel_dir.glob(f"{TODAY}_*.md"):
                transcripts.append({
                    'path': str(file),
                    'channel': channel_dir.name,
                    'filename': file.name
                })

    return transcripts


def read_transcript(file_path):
    """Read the full transcript from markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract just the transcript section (after "## Transcript")
    if "## Transcript" in content:
        transcript = content.split("## Transcript")[1].strip()
    else:
        transcript = content

    return transcript


def summarize_with_ollama(transcript, channel, filename):
    """Send transcript to Ollama for summarization"""

    prompt = SUMMARIZATION_PROMPT.format(transcript=transcript)

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    print(f"\n[VIDEO] Processing: {channel} - {filename}")
    print(f"   Transcript length: {len(transcript):,} characters")
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


def save_summary(channel, filename, summary):
    """Save summary to output file"""
    output_file = Path(OUTPUT_DIR) / f"{TODAY}_youtube_summary_{channel}.md"

    with open(output_file, 'a', encoding='utf-8') as f:
        f.write(f"\n## {filename}\n\n")
        f.write(f"**Channel:** {channel}\n\n")
        f.write(summary)
        f.write("\n\n---\n")

    print(f"   [SAVED] {output_file.name}")


def main():
    print("=" * 70)
    print("YouTube Transcript Summarizer (Ollama)")
    print("=" * 70)
    print(f"Date: {TODAY}")
    print(f"Ollama: {OLLAMA_URL}")
    print(f"Model: {OLLAMA_MODEL}")
    print("=" * 70)

    # Find transcripts
    transcripts = find_today_transcripts()

    if not transcripts:
        print(f"\n[ERROR] No YouTube transcripts found for {TODAY}")
        return

    print(f"\n[OK] Found {len(transcripts)} transcripts to process:")
    for t in transcripts:
        print(f"   - {t['channel']}: {t['filename']}")

    # Process each transcript
    print("\n" + "=" * 70)
    print("Processing transcripts...")
    print("=" * 70)

    success_count = 0

    for t in transcripts:
        try:
            # Read full transcript
            transcript = read_transcript(t['path'])

            # Summarize with Ollama
            summary = summarize_with_ollama(transcript, t['channel'], t['filename'])

            if summary:
                # Save summary
                save_summary(t['channel'], t['filename'], summary)
                success_count += 1

        except Exception as e:
            print(f"   [ERROR] Unexpected error: {e}")
            continue

    # Final report
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total transcripts: {len(transcripts)}")
    print(f"Successfully processed: {success_count}")
    print(f"Failed: {len(transcripts) - success_count}")
    print(f"\nOutput directory: {OUTPUT_DIR}")
    print("=" * 70)


if __name__ == "__main__":
    main()
