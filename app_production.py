#!/usr/bin/env python3
"""
Production-Ready Restaurant Database Web Application
Enhanced Flask-based web server with PostgreSQL support, security features, and monitoring.
"""

import os
import json
from datetime import datetime
import logging
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from database_manager_v2 import EnhancedDatabaseManager
from config import get_config
import structlog

# Import database initialization
try:
    from init_database import init_database
    INIT_DB_AVAILABLE = True
except ImportError:
    INIT_DB_AVAILABLE = False

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

def restaurant_to_dict(restaurant):
    """Convert a Restaurant SQLAlchemy object to a dictionary."""
    if not restaurant:
        return None
    
    try:
        # Map backend fields to frontend expected fields
        return {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'city': restaurant.city,
            'state': restaurant.state,
            'zip_code': restaurant.zip_code,
            'phone_number': restaurant.phone,  # Map phone to phone_number
            'website': restaurant.website,
            'certifying_agency': restaurant.hechsher_details or 'Unknown',  # Map hechsher_details to certifying_agency
            'kosher_category': restaurant.cuisine_type or 'restaurant',  # Map cuisine_type to kosher_category
            'listing_type': 'restaurant',  # Default value
            'status': 'active',  # Default value
            'hours_of_operation': restaurant.hours_of_operation,  # Map hours_of_operation to hours_of_operation
            'hours_open': restaurant.hours_of_operation,  # Also map to hours_open
            'short_description': restaurant.description,  # Map description to short_description
            'price_range': restaurant.price_range,
            'image_url': restaurant.image_url,
            'latitude': restaurant.latitude,
            'longitude': restaurant.longitude,
            'rating': restaurant.rating,
            'review_count': restaurant.review_count,
            'google_rating': restaurant.google_rating or restaurant.rating,  # Use Google rating if available, fallback to regular rating
            'google_review_count': restaurant.google_review_count or restaurant.review_count,  # Use Google count if available, fallback to regular count
            'google_reviews': restaurant.google_reviews,  # JSON string of Google reviews
            'specials': [],  # Default empty array for specials
            'created_at': restaurant.created_at.isoformat() if restaurant.created_at else None,
            'updated_at': restaurant.updated_at.isoformat() if restaurant.updated_at else None
        }
    except Exception as e:
        logger.error("Error converting restaurant to dict", error=str(e), restaurant_id=getattr(restaurant, 'id', 'unknown'))
        # Return a minimal dict with available data
        return {
            'id': getattr(restaurant, 'id', None),
            'name': getattr(restaurant, 'name', 'Unknown'),
            'error': 'Failed to serialize restaurant data'
        }

def create_app(config_name=None):
    """Application factory pattern for Flask app creation."""
    app = Flask(__name__)
    
    # Load configuration
    config = get_config()
    app.config.from_object(config)
    
    # Initialize database with restaurant data if available
    if INIT_DB_AVAILABLE:
        try:
            logger.info("Initializing database with restaurant data...")
            init_database()
            logger.info("Database initialization completed")
        except Exception as e:
            logger.error("Failed to initialize database", error=str(e))
    
    # Initialize CORS with production-ready settings
    CORS(app, 
         origins=app.config['CORS_ORIGINS'],
         methods=app.config['CORS_METHODS'],
         allow_headers=app.config['CORS_ALLOW_HEADERS'],
         supports_credentials=True,
         expose_headers=['Content-Type', 'Authorization'])
    
    # Initialize rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=app.config['RATELIMIT_DEFAULT'],
        storage_uri=app.config['RATELIMIT_STORAGE_URL']
    )
    
    # Initialize database manager
    def get_db_manager():
        """Get a fresh database manager instance for each request."""
        db_manager = EnhancedDatabaseManager()
        if not db_manager.connect():
            raise Exception("Failed to connect to database")
        return db_manager
    
    @app.before_request
    def before_request():
        """Ensure database connection before each request."""
        try:
            g.db_manager = get_db_manager()
            logger.info("Request started", 
                       method=request.method, 
                       path=request.path, 
                       remote_addr=request.remote_addr)
        except Exception as e:
            logger.error("Database connection error", error=str(e))
            return jsonify({'error': 'Database connection failed'}), 500
    
    @app.teardown_appcontext
    def teardown_db(exception):
        """Close database connection after each request."""
        if hasattr(g, 'db_manager') and g.db_manager:
            try:
                g.db_manager.disconnect()
            except Exception as e:
                logger.error("Error disconnecting database", error=str(e))
            g.db_manager = None
    
    @app.route('/', methods=['GET', 'OPTIONS'])
    @limiter.limit("100 per minute")
    def index():
        if request.method == 'OPTIONS':
            return '', 200
        """API server root with enhanced information."""
        return jsonify({
            'message': 'JewGo Restaurant API Server',
            'status': 'running',
            'version': app.config['API_VERSION'],
            'environment': os.environ.get('FLASK_ENV', 'development'),
            'database': 'PostgreSQL' if 'postgresql' in app.config['SQLALCHEMY_DATABASE_URI'] else 'SQLite',
            'endpoints': {
                'restaurants': '/api/restaurants',
                'statistics': '/api/statistics',
                'categories': '/api/categories',
                'states': '/api/states',
                'health': '/health'
            },
            'documentation': 'https://jewgo.com/api/docs',
            'timestamp': datetime.utcnow().isoformat()
        })
    
    @app.route('/api/restaurants', methods=['GET', 'OPTIONS'])
    @limiter.limit("200 per minute")
    def api_restaurants():
        if request.method == 'OPTIONS':
            return '', 200
        """Enhanced API endpoint for restaurant search with better error handling."""
        try:
            # Parse query parameters with validation
            query = request.args.get('query', '').strip()
            category = request.args.get('category', '').strip()
            state = request.args.get('state', '').strip()
            
            try:
                limit = min(int(request.args.get('limit', 50)), 100)  # Max 100 results
                offset = max(int(request.args.get('offset', 0)), 0)
            except ValueError:
                return jsonify({'error': 'Invalid limit or offset parameter'}), 400
            
            # Location-based filtering
            lat = request.args.get('lat')
            lng = request.args.get('lng')
            radius = request.args.get('radius', 50)
            
            if lat and lng:
                try:
                    lat = float(lat)
                    lng = float(lng)
                    radius = min(float(radius), 100)  # Max 100 mile radius
                    
                    # Validate coordinates
                    if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                        return jsonify({'error': 'Invalid coordinates'}), 400
                        
                    restaurants = g.db_manager.search_restaurants_near_location(
                        lat=lat, lng=lng, radius=radius,
                        query=query, category=category,
                        limit=limit, offset=offset
                    )
                except ValueError:
                    return jsonify({'error': 'Invalid location parameters'}), 400
            else:
                restaurants = g.db_manager.search_restaurants(
                    query=query, category=category, state=state,
                    limit=limit, offset=offset
                )
            
            # Add metadata to response
            response = {
                'success': True,
                'data': restaurants,
                'metadata': {
                    'total_results': len(restaurants),
                    'limit': limit,
                    'offset': offset,
                    'query': query,
                    'category': category,
                    'state': state,
                    'location_based': bool(lat and lng),
                    'timestamp': datetime.utcnow().isoformat()
                }
            }
            
            logger.info("Restaurant search completed", 
                       query=query, 
                       category=category, 
                       results_count=len(restaurants))
            
            return jsonify(response)
            
        except Exception as e:
            logger.error("Error in restaurant search", error=str(e))
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/restaurants/<business_id>', methods=['GET', 'OPTIONS'])
    @limiter.limit("100 per minute")
    def api_restaurant_detail(business_id):
        if request.method == 'OPTIONS':
            return '', 200
        """Get detailed information about a specific restaurant."""
        try:
            # Convert business_id to integer
            try:
                restaurant_id = int(business_id)
            except ValueError:
                return jsonify({'error': 'Invalid restaurant ID'}), 400
            
            restaurant = g.db_manager.get_restaurant(restaurant_id)
            
            if not restaurant:
                return jsonify({'error': 'Restaurant not found'}), 404
            
            # Convert restaurant object to dictionary for JSON serialization
            restaurant_data = restaurant_to_dict(restaurant)
            
            response = {
                'success': True,
                'restaurant': restaurant_data,
                'metadata': {
                    'business_id': business_id,
                    'timestamp': datetime.utcnow().isoformat()
                }
            }
            
            logger.info("Restaurant detail retrieved", business_id=business_id)
            return jsonify(response)
            
        except Exception as e:
            logger.error("Error getting restaurant detail", error=str(e), business_id=business_id)
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/statistics')
    @limiter.limit("50 per minute")
    def api_statistics():
        """Get comprehensive database statistics."""
        try:
            stats = g.db_manager.get_statistics()
            
            response = {
                'success': True,
                'data': stats,
                'metadata': {
                    'timestamp': datetime.utcnow().isoformat()
                }
            }
            
            logger.info("Statistics retrieved", total_restaurants=stats.get('total_restaurants', 0))
            return jsonify(response)
            
        except Exception as e:
            logger.error("Error getting statistics", error=str(e))
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/categories')
    @limiter.limit("100 per minute")
    def api_categories():
        """Get available restaurant categories."""
        try:
            categories = [
                {'id': 'restaurant', 'name': 'Restaurants', 'icon': '🍽️'},
                {'id': 'bakery', 'name': 'Bakeries', 'icon': '🥖'},
                {'id': 'grocery', 'name': 'Grocery Stores', 'icon': '🛒'},
                {'id': 'catering', 'name': 'Catering', 'icon': '🎉'},
                {'id': 'deli', 'name': 'Delis', 'icon': '🥪'},
                {'id': 'ice_cream', 'name': 'Ice Cream', 'icon': '🍦'},
                {'id': 'pizza', 'name': 'Pizza', 'icon': '🍕'},
                {'id': 'coffee', 'name': 'Coffee Shops', 'icon': '☕'}
            ]
            
            response = {
                'success': True,
                'data': categories,
                'metadata': {
                    'total_categories': len(categories),
                    'timestamp': datetime.utcnow().isoformat()
                }
            }
            
            return jsonify(response)
            
        except Exception as e:
            logger.error("Error getting categories", error=str(e))
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/states')
    @limiter.limit("100 per minute")
    def api_states():
        """Get available states with restaurant counts."""
        try:
            stats = g.db_manager.get_statistics()
            states_data = stats.get('states', {})
            
            # Convert to list format
            states = [
                {'code': state, 'name': state, 'count': count}
                for state, count in states_data.items()
            ]
            
            # Sort by count descending
            states.sort(key=lambda x: x['count'], reverse=True)
            
            response = {
                'success': True,
                'data': states,
                'metadata': {
                    'total_states': len(states),
                    'timestamp': datetime.utcnow().isoformat()
                }
            }
            
            return jsonify(response)
            
        except Exception as e:
            logger.error("Error getting states", error=str(e))
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/restaurants/<business_id>/hours', methods=['PUT', 'OPTIONS'])
    @limiter.limit("50 per minute")
    def api_update_restaurant_hours(business_id):
        """Update restaurant hours."""
        if request.method == 'OPTIONS':
            return '', 200
            
        try:
            # Get request data
            data = request.get_json()
            if not data or 'hours_open' not in data:
                return jsonify({'error': 'hours_open field is required'}), 400
            
            hours_open = data['hours_open']
            
            # Update restaurant hours in database
            success = g.db_manager.update_restaurant_hours(business_id, hours_open)
            
            if success:
                response = {
                    'success': True,
                    'message': f'Hours updated for restaurant {business_id}',
                    'data': {
                        'restaurant_id': business_id,
                        'hours_open': hours_open
                    },
                    'metadata': {
                        'timestamp': datetime.utcnow().isoformat()
                    }
                }
                return jsonify(response), 200
            else:
                return jsonify({'error': f'Restaurant {business_id} not found or update failed'}), 404
                
        except Exception as e:
            logger.error("Error updating restaurant hours", error=str(e), restaurant_id=business_id)
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/health')
    @limiter.limit("200 per minute")
    def health_check():
        """Enhanced health check endpoint."""
        try:
            # Test database connection
            db_healthy = g.db_manager is not None
            
            health_status = {
                'status': 'healthy' if db_healthy else 'unhealthy',
                'timestamp': datetime.utcnow().isoformat(),
                'version': app.config['API_VERSION'],
                'environment': os.environ.get('FLASK_ENV', 'development'),
                'database': {
                    'status': 'connected' if db_healthy else 'disconnected',
                    'type': 'PostgreSQL' if 'postgresql' in app.config['SQLALCHEMY_DATABASE_URI'] else 'SQLite'
                },
                'uptime': 'running',  # In production, add actual uptime calculation
                'memory_usage': 'normal'  # In production, add actual memory monitoring
            }
            
            status_code = 200 if db_healthy else 503
            return jsonify(health_status), status_code
            
        except Exception as e:
            logger.error("Health check failed", error=str(e))
            return jsonify({
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }), 503
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return jsonify({'error': 'Rate limit exceeded'}), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error("Internal server error", error=str(error))
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    # Production server configuration
    port = int(os.environ.get('PORT', 8081))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info("Starting JewGo API server", 
               port=port, 
               debug=debug, 
               environment=os.environ.get('FLASK_ENV', 'development'))
    
    # Use Gunicorn in production, Flask dev server in development
    if debug:
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        # For production, use: gunicorn app_production:app
        app.run(host='0.0.0.0', port=port, debug=False) 