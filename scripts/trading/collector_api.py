"""
Collector API: Flask endpoints for controlling the data collector from Command Center
Provides REST API endpoints for:
- Starting/stopping the collector
- Adding/removing tickers
- Getting collector status
"""

import json
import logging
from typing import Dict, Tuple
from flask import Blueprint, request, jsonify

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Blueprint for collector API
collector_bp = Blueprint('collector', __name__, url_prefix='/api/collector')

# Global collector instance (will be set by main app)
collector_instance = None


def set_collector(collector):
    """Set the global collector instance"""
    global collector_instance
    collector_instance = collector


@collector_bp.route('/start', methods=['POST'])
def start_collector() -> Tuple[Dict, int]:
    """Start the background data collector service"""
    if not collector_instance:
        return {'success': False, 'message': 'Collector not initialized'}, 500

    if collector_instance.is_running():
        return {'success': False, 'message': 'Collector already running'}, 400

    try:
        success = collector_instance.start()
        if success:
            return {
                'success': True,
                'message': 'Collector started',
                'status': collector_instance.get_status()
            }, 200
        else:
            return {'success': False, 'message': 'Failed to start collector'}, 500
    except Exception as e:
        logger.error(f"Error starting collector: {e}")
        return {'success': False, 'message': str(e)}, 500


@collector_bp.route('/stop', methods=['POST'])
def stop_collector() -> Tuple[Dict, int]:
    """Stop the background data collector service"""
    if not collector_instance:
        return {'success': False, 'message': 'Collector not initialized'}, 500

    if not collector_instance.is_running():
        return {'success': False, 'message': 'Collector not running'}, 400

    try:
        success = collector_instance.stop()
        if success:
            return {
                'success': True,
                'message': 'Collector stopped',
                'status': collector_instance.get_status()
            }, 200
        else:
            return {'success': False, 'message': 'Failed to stop collector'}, 500
    except Exception as e:
        logger.error(f"Error stopping collector: {e}")
        return {'success': False, 'message': str(e)}, 500


@collector_bp.route('/status', methods=['GET'])
def get_status() -> Tuple[Dict, int]:
    """Get current collector status"""
    if not collector_instance:
        return {'success': False, 'message': 'Collector not initialized'}, 500

    try:
        status = collector_instance.get_status()
        return {
            'success': True,
            **status
        }, 200
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return {'success': False, 'message': str(e)}, 500


@collector_bp.route('/ticker/add', methods=['POST'])
def add_ticker() -> Tuple[Dict, int]:
    """Add ticker to watchlist"""
    if not collector_instance:
        return {'success': False, 'message': 'Collector not initialized'}, 500

    try:
        data = request.get_json()
        ticker = data.get('ticker', '').upper()

        if not ticker:
            return {'success': False, 'message': 'Ticker required'}, 400

        # Add ticker
        success = collector_instance.ticker_manager.add_ticker(ticker)

        if success:
            return {
                'success': True,
                'message': f'Added {ticker} to watchlist',
                'watchlist': collector_instance.ticker_manager.get_watchlist()
            }, 200
        else:
            return {
                'success': False,
                'message': f'Failed to add {ticker} (may already exist or be invalid)'
            }, 400

    except Exception as e:
        logger.error(f"Error adding ticker: {e}")
        return {'success': False, 'message': str(e)}, 500


@collector_bp.route('/ticker/remove', methods=['POST'])
def remove_ticker() -> Tuple[Dict, int]:
    """Remove ticker from watchlist"""
    if not collector_instance:
        return {'success': False, 'message': 'Collector not initialized'}, 500

    try:
        data = request.get_json()
        ticker = data.get('ticker', '').upper()

        if not ticker:
            return {'success': False, 'message': 'Ticker required'}, 400

        # Check if protected
        if ticker in collector_instance.ticker_manager.get_protected_tickers():
            return {
                'success': False,
                'message': f'{ticker} is protected and cannot be removed'
            }, 400

        # Remove ticker
        success = collector_instance.ticker_manager.remove_ticker(ticker)

        if success:
            return {
                'success': True,
                'message': f'Removed {ticker} from watchlist',
                'watchlist': collector_instance.ticker_manager.get_watchlist()
            }, 200
        else:
            return {
                'success': False,
                'message': f'Failed to remove {ticker} (may not exist)'
            }, 400

    except Exception as e:
        logger.error(f"Error removing ticker: {e}")
        return {'success': False, 'message': str(e)}, 500


@collector_bp.route('/status/json', methods=['GET'])
def status_json_file() -> Tuple[Dict, int]:
    """Get collector status from JSON file (for debugging)"""
    try:
        with open('data/collector_status.json', 'r') as f:
            status = json.load(f)
        return {
            'success': True,
            'data': status
        }, 200
    except FileNotFoundError:
        return {
            'success': False,
            'message': 'Status file not found (collector may not have run yet)'
        }, 404
    except Exception as e:
        logger.error(f"Error reading status file: {e}")
        return {'success': False, 'message': str(e)}, 500
