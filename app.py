#!/usr/bin/env python3
"""
Restaurant Database Web Application
Flask-based web server for hosting the restaurant database with modern UI.
"""

from flask import Flask, request, jsonify, g
from flask_cors import CORS
from database_manager import DatabaseManager
import json
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app)  # Enable CORS for API endpoints

# Initialize database manager per request
def get_db_manager():
    """Get a fresh database manager instance for each request."""
    db_manager = DatabaseManager()
    if not db_manager.connect():
        raise Exception("Failed to connect to database")
    return db_manager

@app.before_request
def before_request():
    """Ensure database connection before each request."""
    try:
        # Store db manager in Flask's g object for this request
        g.db_manager = get_db_manager()
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return jsonify({'error': 'Database connection failed'}), 500

@app.teardown_appcontext
def teardown_db(exception):
    """Close database connection after each request."""
    if hasattr(g, 'db_manager') and g.db_manager:
        try:
            g.db_manager.disconnect()
        except Exception as e:
            logger.error(f"Error disconnecting database: {e}")
        g.db_manager = None

@app.route('/')
def index():
    """API server root - redirect to API documentation or return status."""
    return jsonify({
        'message': 'JewGo Restaurant API Server',
        'status': 'running',
        'version': '1.0.0',
        'endpoints': {
            'restaurants': '/api/restaurants',
            'statistics': '/api/statistics',
            'categories': '/api/categories',
            'states': '/api/states',
            'health': '/health'
        }
    })

@app.route('/api/restaurants')
def api_restaurants():
    """API endpoint for restaurant search."""
    try:
        query = request.args.get('query', '')
        category = request.args.get('category', '')
        state = request.args.get('state', '')
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        # Location-based filtering
        lat = request.args.get('lat')
        lng = request.args.get('lng')
        radius = float(request.args.get('radius', 50))  # Default 50 miles
        
        if lat and lng:
            # Use location-based search
            restaurants = g.db_manager.search_restaurants_near_location(
                lat=float(lat),
                lng=float(lng),
                radius=radius,
                query=query,
                category=category,
                limit=limit,
                offset=offset
            )
        else:
            # Use regular search
            restaurants = g.db_manager.search_restaurants(
                query=query,
                category=category,
                state=state,
                limit=limit,
                offset=offset
            )
        
        return jsonify({
            'success': True,
            'restaurants': restaurants,
            'count': len(restaurants)
        })
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/restaurants/<business_id>')
def api_restaurant_detail(business_id):
    """API endpoint for single restaurant details."""
    try:
        # Try to get restaurant by business_id first
        restaurant = g.db_manager.get_restaurant(business_id)
        
        # If not found, try to get by numeric id
        if not restaurant:
            try:
                numeric_id = int(business_id)
                # Get restaurant by numeric id
                restaurant = g.db_manager.get_restaurant_by_id(numeric_id)
            except (ValueError, TypeError):
                pass
        
        if restaurant:
            # Get reviews, tags, and specials
            reviews = g.db_manager.get_reviews(restaurant['id'])
            tags = g.db_manager.get_restaurant_tags(restaurant['id'])
            specials = g.db_manager.get_restaurant_specials(restaurant['id'], paid_only=True)
            
            restaurant['reviews'] = reviews
            restaurant['tags'] = tags
            restaurant['specials'] = specials
            
            return jsonify({
                'success': True,
                'restaurant': restaurant
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Restaurant not found'
            }), 404
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/statistics')
def api_statistics():
    """API endpoint for database statistics."""
    try:
        stats = g.db_manager.get_statistics()
        return jsonify({
            'success': True,
            'statistics': stats
        })
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/categories')
def api_categories():
    """API endpoint for available categories."""
    try:
        stats = g.db_manager.get_statistics()
        categories = stats.get('category_breakdown', {})
        return jsonify({
            'success': True,
            'categories': categories
        })
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/states')
def api_states():
    """API endpoint for available states."""
    try:
        stats = g.db_manager.get_statistics()
        states = stats.get('top_states', {})
        return jsonify({
            'success': True,
            'states': states
        })
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Removed template routes - using Next.js frontend instead
# @app.route('/restaurant/<business_id>')
# @app.route('/admin')

@app.route('/api/admin/restaurants', methods=['POST'])
def api_add_restaurant():
    """API endpoint for adding new restaurants."""
    try:
        data = request.get_json()
        
        required_fields = ['business_id', 'name', 'address']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        if g.db_manager.add_restaurant(data):
            return jsonify({'success': True, 'message': 'Restaurant added successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to add restaurant'}), 500
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/restaurants/<business_id>', methods=['PUT'])
def api_update_restaurant(business_id):
    """API endpoint for updating restaurants."""
    try:
        data = request.get_json()
        
        if g.db_manager.update_restaurant(business_id, data):
            return jsonify({'success': True, 'message': 'Restaurant updated successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to update restaurant'}), 500
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/restaurants/<business_id>/specials')
def api_restaurant_specials(business_id):
    """API endpoint for getting restaurant specials."""
    try:
        # Get restaurant first
        restaurant = g.db_manager.get_restaurant(business_id)
        if not restaurant:
            try:
                numeric_id = int(business_id)
                restaurant = g.db_manager.get_restaurant_by_id(numeric_id)
            except (ValueError, TypeError):
                pass
        
        if not restaurant:
            return jsonify({'success': False, 'error': 'Restaurant not found'}), 404
        
        # Get specials (paid only by default)
        paid_only = request.args.get('paid_only', 'true').lower() == 'true'
        specials = g.db_manager.get_restaurant_specials(restaurant['id'], paid_only=paid_only)
        
        return jsonify({
            'success': True,
            'specials': specials,
            'restaurant_id': restaurant['id']
        })
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/restaurants/<business_id>/specials', methods=['POST'])
def api_add_restaurant_special(business_id):
    """API endpoint for adding restaurant specials."""
    try:
        # Get restaurant first
        restaurant = g.db_manager.get_restaurant(business_id)
        if not restaurant:
            try:
                numeric_id = int(business_id)
                restaurant = g.db_manager.get_restaurant_by_id(numeric_id)
            except (ValueError, TypeError):
                pass
        
        if not restaurant:
            return jsonify({'success': False, 'error': 'Restaurant not found'}), 404
        
        data = request.get_json()
        data['restaurant_id'] = restaurant['id']
        
        if g.db_manager.add_restaurant_special(data):
            return jsonify({'success': True, 'message': 'Special added successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to add special'}), 500
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/specials/<int:special_id>/payment', methods=['PUT'])
def api_update_special_payment(special_id):
    """API endpoint for updating special payment status."""
    try:
        data = request.get_json()
        is_paid = data.get('is_paid', False)
        payment_status = data.get('payment_status', 'paid')
        
        if g.db_manager.update_special_payment_status(special_id, is_paid, payment_status):
            return jsonify({'success': True, 'message': 'Payment status updated successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to update payment status'}), 500
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/specials')
def api_get_all_specials():
    """API endpoint for getting all specials (admin only)."""
    try:
        # Get all specials (both paid and unpaid)
        all_specials = []
        
        # Get all restaurants and their specials
        restaurants = g.db_manager.search_restaurants(limit=1000)
        for restaurant in restaurants:
            specials = g.db_manager.get_restaurant_specials(restaurant['id'], paid_only=False)
            all_specials.extend(specials)
        
        return jsonify({
            'success': True,
            'specials': all_specials
        })
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export')
def api_export():
    """API endpoint for exporting data."""
    try:
        category = request.args.get('category', '')
        state = request.args.get('state', '')
        query = request.args.get('query', '')
        
        filters = {}
        if category:
            filters['category'] = category
        if state:
            filters['state'] = state
        if query:
            filters['query'] = query
        
        filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        if g.db_manager.export_to_json(filename, filters):
            return jsonify({
                'success': True,
                'filename': filename,
                'message': 'Export completed successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'Export failed'}), 500
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    try:
        # Test database connection
        stats = g.db_manager.get_statistics()
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'restaurants': stats.get('total_restaurants', 0)
        })
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    # Get configuration from environment
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8081))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting Restaurant Database Web Server")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🐛 Debug: {debug}")
    print(f"🌐 Access: http://{host}:{port}")
    
    app.run(host=host, port=port, debug=debug) 