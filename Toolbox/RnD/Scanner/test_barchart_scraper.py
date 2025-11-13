#!/usr/bin/env python3
"""
Quick test runner for Barchart scraper
Run from RnD/Scanner/ directory
"""

import sys
from pathlib import Path

# Add scanner package to path
sys.path.insert(0, str(Path(__file__).parent))

# Import and run tests
from scanner.scrapers.test_barchart import run_all_tests

if __name__ == '__main__':
    sys.exit(run_all_tests())
