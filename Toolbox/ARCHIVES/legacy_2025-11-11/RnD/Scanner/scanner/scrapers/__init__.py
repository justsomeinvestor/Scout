"""
Scanner web scrapers package.

IMPORTANT: RnD Project
This code is in Research & Development (RnD/Scanner/).
Do not move to production until proven reliable (see README.md).
"""

from .utils import (
    sanitize_filename,
    record_scraper_status,
    rate_limit_delay,
    scrape_with_retry,
    clean_html_text
)

__all__ = [
    'sanitize_filename',
    'record_scraper_status',
    'rate_limit_delay',
    'scrape_with_retry',
    'clean_html_text'
]
