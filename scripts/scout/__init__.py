"""
Scout - Unified Reconnaissance System
======================================

Market intelligence collection, processing, and dashboard updates.

Architecture:
- collector.py: Parallel data collection (API + scrapers)
- transformer.py: Data transformation & signal calculation
- builder.py: Dashboard JSON generation & validation

Version: 1.0.0
"""

__version__ = "1.0.0"

from .collector import collect_all
from .transformer import transform_all
from .builder import build_dashboard

__all__ = ['collect_all', 'transform_all', 'build_dashboard']
