#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scout - Market Intelligence System
===================================

Single entry point for complete market research workflow.

Usage:
    python scout.py

Workflow:
    1. Cleanup - Remove stale cache files (30 sec)
    2. Collect - Gather data from all sources (10-15 min)
        - X/Twitter (local scraper)
        - YouTube (API server: 192.168.10.56:3000)
        - RSS (API server: 192.168.10.56:3000)
        - Market data (API server: 192.168.10.56:3000)
    3. Process - AI analysis with checkpoints (40 min)
    4. Output - Generate dash.md and dash.html
    5. Done - Open dashboard in browser

Total time: <60 minutes
"""

import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import traceback

# Ensure proper encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from config import config


class Scout:
    """Main orchestrator for Scout intelligence system"""

    def __init__(self):
        self.root = Path(__file__).parent
        self.project_root = PROJECT_ROOT
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.date_display = datetime.now().strftime("%B %d, %Y")
        self.results = {}

    def run(self):
        """Execute complete workflow"""
        print("\n" + "=" * 70)
        print("🔍 SCOUT MARKET INTELLIGENCE SYSTEM")
        print("=" * 70)
        print(f"Date: {self.date_display}")
        print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 70 + "\n")

        try:
            # Phase 1: Cleanup
            self.cleanup()

            # Phase 2: Collect Data
            self.collect()

            # Phase 3: Process Data (AI Analysis)
            print("\n" + "=" * 70)
            print("[3/5] AI PROCESSING")
            print("=" * 70)
            print("\n⚠️  MANUAL STEP REQUIRED:")
            print("The AI processing phase requires manual execution through Claude.")
            print("\nData has been collected and is ready for analysis in:")
            print(f"  - Research/X/")
            print(f"  - Research/.cache/{self.date}_technical_data.json")
            print(f"  - API server data (YouTube/RSS via API)")
            print("\nNext steps:")
            print("  1. Review collected data")
            print("  2. Run Step 3 analysis (see Toolbox/MasterFlow/05_STEP_3_PROCESS_DATA.md)")
            print("  3. Generate dash.md output")
            print("\nScout collector phase complete!")
            print("=" * 70 + "\n")

            # Report
            self.report()

        except KeyboardInterrupt:
            print("\n\n[INTERRUPTED] Scout workflow stopped by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n\n[ERROR] Scout workflow failed: {e}")
            traceback.print_exc()
            sys.exit(1)

    def cleanup(self):
        """Phase 1: Remove stale cache files"""
        print("=" * 70)
        print("[1/5] CLEANUP")
        print("=" * 70)
        print("Removing stale cache files...")

        try:
            cleanup_script = self.project_root / "Toolbox" / "scripts" / "cleanup" / "scout_cleanup.py"

            if not cleanup_script.exists():
                print("[WARN] Cleanup script not found, skipping...")
                self.results['cleanup'] = 'skipped'
                return

            result = subprocess.run(
                [sys.executable, str(cleanup_script)],
                capture_output=True,
                text=True,
                cwd=str(self.project_root)
            )

            if result.returncode == 0:
                # Extract summary from output
                for line in result.stdout.split('\n'):
                    if 'paths_removed=' in line or 'total_reclaimed=' in line:
                        print(f"  {line.strip()}")
                print("[OK] Cleanup complete")
                self.results['cleanup'] = 'success'
            else:
                print(f"[WARN] Cleanup returned code {result.returncode}")
                self.results['cleanup'] = 'warning'

        except Exception as e:
            print(f"[ERROR] Cleanup failed: {e}")
            self.results['cleanup'] = 'failed'

        print()

    def collect(self):
        """Phase 2: Collect data from all sources"""
        print("=" * 70)
        print("[2/5] DATA COLLECTION")
        print("=" * 70)
        print("\nData sources:")
        print("  [1/4] X/Twitter - Local scraper (2-3 min)")
        print("  [2/4] YouTube - API server")
        print("  [3/4] RSS News - API server")
        print("  [4/4] Market Data - API server")
        print()

        collection_results = {}

        # 1. X/Twitter (local scraper)
        x_result = self.collect_x_twitter()
        collection_results['x_twitter'] = x_result

        # 2. API Data (all at once)
        api_result = self.collect_api_data()
        collection_results['api_data'] = api_result

        # Summary
        print("\n" + "=" * 70)
        print("COLLECTION SUMMARY")
        print("=" * 70)
        success_count = sum(1 for r in collection_results.values() if r == 'success')
        print(f"Success: {success_count}/{len(collection_results)} sources")

        for source, status in collection_results.items():
            icon = "✅" if status == 'success' else "⚠️"
            print(f"  {icon} {source.replace('_', ' ').title()}: {status}")

        self.verify_collection()

        if success_count >= 2:
            self.results['collect'] = 'success'
        elif success_count >= 1:
            self.results['collect'] = 'partial'
        else:
            self.results['collect'] = 'failed'

        print()

    def collect_x_twitter(self) -> str:
        """Collect X/Twitter data using local scraper"""
        print("\n[1/4] X/Twitter Collection")
        print("-" * 70)

        try:
            x_scraper = self.project_root / "Scraper" / "x_scraper.py"

            if not x_scraper.exists():
                print("[SKIP] X scraper not found")
                return 'skipped'

            print("Running X scraper (optimized - should take 3-5 minutes)...")
            print("  (Scraping 4 lists: Technicals, Crypto, Macro, Bookmarks)")
            print("=" * 70)

            # Use Popen for real-time output streaming
            process = subprocess.Popen(
                [sys.executable, str(x_scraper)],
                cwd=str(self.project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,  # Line buffered for real-time output
                universal_newlines=True
            )

            # Stream output in real-time
            try:
                for line in iter(process.stdout.readline, ''):
                    if line:
                        print(line.rstrip())

                process.wait(timeout=600)  # 10 minute timeout

                # Check return code after process completes
                if process.returncode == 0:
                    # Count collected posts
                    x_dir = self.project_root / "Research" / "X"
                    post_files = list(x_dir.rglob(f"*{self.date.replace('-', '')}*.json"))
                    print("=" * 70)
                    print(f"[OK] X scraper complete - {len(post_files)} files collected")
                    return 'success'
                else:
                    print("=" * 70)
                    print(f"[WARN] X scraper returned code {process.returncode}")
                    return 'partial'

            except subprocess.TimeoutExpired:
                process.kill()
                print("=" * 70)
                print("[ERROR] X scraper timeout (>10 minutes)")
                return 'timeout'

        except subprocess.TimeoutExpired:
            print("[ERROR] X scraper timeout (>10 minutes)")
            return 'timeout'
        except Exception as e:
            print(f"[ERROR] X scraper failed: {e}")
            return 'failed'

    def collect_api_data(self) -> str:
        """Collect data from API server"""
        print("\n[2-4/4] API Server Collection")
        print("-" * 70)

        try:
            # Import API client
            from scripts.trading.api_client import get_client, APIClientError

            with get_client() as api:
                # Health check
                if not api.is_healthy():
                    print("[ERROR] API server offline")
                    return 'failed'

                print("[OK] API server online")

                # Get all data
                sources_collected = []

                # Market data
                try:
                    summary = api.get_summary()
                    if summary.get('success'):
                        counts = summary.get('counts', {})
                        print(f"  ✅ Market data: {counts.get('etf', 0)} ETFs, {counts.get('maxPain', 0)} max pain records")
                        sources_collected.append('market_data')
                except Exception as e:
                    print(f"  ⚠️  Market data: {e}")

                # YouTube
                try:
                    youtube = api.get_youtube_latest(limit=50)
                    if youtube.get('success'):
                        video_count = len(youtube.get('data', []))
                        print(f"  ✅ YouTube: {video_count} videos")
                        sources_collected.append('youtube')
                except Exception as e:
                    print(f"  ⚠️  YouTube: {e}")

                # RSS
                try:
                    rss = api.get_rss_latest(limit=50)
                    if rss.get('success'):
                        article_count = len(rss.get('data', []))
                        print(f"  ✅ RSS News: {article_count} articles")
                        sources_collected.append('rss')
                except Exception as e:
                    print(f"  ⚠️  RSS: {e}")

                print(f"\n[OK] API collection complete - {len(sources_collected)}/3 sources")

                if len(sources_collected) >= 2:
                    return 'success'
                elif len(sources_collected) >= 1:
                    return 'partial'
                else:
                    return 'failed'

        except Exception as e:
            print(f"[ERROR] API collection failed: {e}")
            traceback.print_exc()
            return 'failed'

    def verify_collection(self):
        """Verify collected data files exist"""
        print("\nVerifying collected data...")

        checks = {
            'X/Twitter': self.project_root / "Research" / "X",
            'Technical Data': self.project_root / "Research" / ".cache" / f"{self.date}_technical_data.json",
        }

        for source, path in checks.items():
            if path.exists():
                if path.is_dir():
                    # Count files in directory
                    files = list(path.rglob(f"*{self.date.replace('-', '')}*"))
                    print(f"  ✅ {source}: {len(files)} files")
                else:
                    print(f"  ✅ {source}: Found")
            else:
                print(f"  ⚠️  {source}: Not found")

    def report(self):
        """Report workflow completion"""
        print("\n" + "=" * 70)
        print("📊 SCOUT WORKFLOW REPORT")
        print("=" * 70)

        for phase, status in self.results.items():
            status_icon = "✅" if status in ['success', 'completed'] else "⚠️"
            print(f"{status_icon} {phase.title()}: {status}")

        print("\n" + "=" * 70)
        print("NEXT STEPS:")
        print("=" * 70)
        print("\n1. Review collected data in Research/ directories")
        print("2. Process data using AI analysis (Step 3)")
        print("   See: Toolbox/MasterFlow/05_STEP_3_PROCESS_DATA.md")
        print("3. Generate dash.md and dash.html")
        print("4. Open dashboard in browser")
        print("\n" + "=" * 70 + "\n")


def main():
    """Entry point"""
    scout = Scout()
    scout.run()


if __name__ == "__main__":
    main()
