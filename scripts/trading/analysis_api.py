#!/usr/bin/env python3
"""
Analysis API: Flask endpoints for serving real-time decision engine analysis to Command Center
Exposes the TickerAnalyzer to the web interface via REST API endpoints

Features:
- /api/analyze/<ticker> - Analyze a single ticker
- /api/batch - Analyze multiple tickers at once
- /api/market-context - Get current market context (SPY, QQQ, VIX)
- Real data from cache/API, fallback to simulated data
- Returns complete decision engine output (probability, signal, levels, reasoning, etc.)
"""

import json
import os
import logging
from flask import Blueprint, request, jsonify, current_app
from typing import Dict, Tuple
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the decision engine
try:
    from analyze_ticker_v2 import TickerAnalyzer
    from cache_manager import CacheManager
    HAS_ANALYZER = True
except ImportError as e:
    HAS_ANALYZER = False
    print(f"Warning: Could not import analyzer: {e}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Blueprint for analysis API
analysis_bp = Blueprint('analysis', __name__, url_prefix='/api')

# Global analyzer instance
analyzer_instance = None
cache_instance = None


def init_analyzer(api_key: str = None):
    """Initialize the global analyzer instance with API key"""
    global analyzer_instance, cache_instance
    if HAS_ANALYZER:
        analyzer_instance = TickerAnalyzer(api_key=api_key)
        cache_instance = CacheManager()
        logger.info("Analysis engine initialized")
    else:
        logger.warning("Analyzer not available - analysis endpoints will use cache only")


@analysis_bp.route('/analyze/<ticker>', methods=['GET'])
def analyze_ticker(ticker: str) -> Tuple[Dict, int]:
    """
    Analyze a single ticker with full decision engine

    Returns: Complete analysis including probability, signal, levels, reasoning
    """
    ticker = ticker.upper().strip()

    if not ticker or len(ticker) > 5:
        return {'success': False, 'message': 'Invalid ticker symbol'}, 400

    try:
        if not HAS_ANALYZER:
            return {
                'success': False,
                'message': 'Analysis engine not initialized',
                'available_tickers': ['SPY', 'QQQ', 'NVDA', 'TSLA'] if cache_instance else []
            }, 503

        # Run the analyzer (verbose=False for API to avoid console output)
        analysis = analyzer_instance.analyze(ticker, verbose=False)

        return {
            'success': True,
            'data': analysis
        }, 200

    except Exception as e:
        logger.error(f"Error analyzing {ticker}: {e}")
        return {
            'success': False,
            'message': f'Failed to analyze {ticker}: {str(e)}'
        }, 500


@analysis_bp.route('/analyze/batch', methods=['POST'])
def analyze_batch() -> Tuple[Dict, int]:
    """
    Analyze multiple tickers at once

    Request body:
    {
        "tickers": ["SPY", "NVDA", "TSLA"]
    }
    """
    try:
        data = request.get_json()
        tickers = data.get('tickers', [])

        if not tickers or not isinstance(tickers, list):
            return {'success': False, 'message': 'tickers array required'}, 400

        if len(tickers) > 20:
            return {'success': False, 'message': 'Maximum 20 tickers per batch'}, 400

        if not HAS_ANALYZER:
            return {
                'success': False,
                'message': 'Analysis engine not initialized'
            }, 503

        results = {}
        for ticker in tickers:
            try:
                analysis = analyzer_instance.analyze(ticker, verbose=False)
                results[ticker] = {
                    'success': True,
                    'data': analysis
                }
            except Exception as e:
                results[ticker] = {
                    'success': False,
                    'message': str(e)
                }

        return {
            'success': True,
            'results': results,
            'count': len(tickers)
        }, 200

    except Exception as e:
        logger.error(f"Error in batch analysis: {e}")
        return {
            'success': False,
            'message': f'Batch analysis failed: {str(e)}'
        }, 500


@analysis_bp.route('/market-context', methods=['GET'])
def get_market_context() -> Tuple[Dict, int]:
    """
    Get current market context (SPY, QQQ, VIX, etc.)

    Returns: Market indices and context data
    """
    try:
        if not HAS_ANALYZER or not analyzer_instance:
            return {
                'success': False,
                'message': 'Context engine not available'
            }, 503

        # Gather context through analyzer
        context = analyzer_instance._gather_context("TEMP")

        # Build market context response
        market_context = {
            'spy': context.get('spy_price', 'N/A'),
            'qqq': context.get('qqq_price', 'N/A'),
            'vix': context.get('vix', 'N/A'),
            'market_trend': context.get('market_trend', 'NEUTRAL'),
            'market_strength': context.get('market_strength', 'NEUTRAL'),
            'data_source': analyzer_instance.data_source,
            'timestamp': context.get('date', 'N/A')
        }

        return {
            'success': True,
            'data': market_context
        }, 200

    except Exception as e:
        logger.error(f"Error getting market context: {e}")
        return {
            'success': False,
            'message': f'Failed to get market context: {str(e)}'
        }, 500


@analysis_bp.route('/status', methods=['GET'])
def analysis_status() -> Tuple[Dict, int]:
    """Get status of analysis engine"""
    try:
        if not HAS_ANALYZER:
            return {
                'success': False,
                'status': 'NOT_INITIALIZED',
                'message': 'Analyzer module not available'
            }, 503

        if not analyzer_instance:
            return {
                'success': False,
                'status': 'NOT_READY',
                'message': 'Analyzer not initialized'
            }, 503

        return {
            'success': True,
            'status': 'READY',
            'data_source': analyzer_instance.data_source,
            'has_cache': cache_instance is not None,
            'message': 'Analysis engine is ready'
        }, 200

    except Exception as e:
        logger.error(f"Error checking status: {e}")
        return {
            'success': False,
            'status': 'ERROR',
            'message': str(e)
        }, 500
