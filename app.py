#!/usr/bin/env python3
"""
JewGo Restaurant API
A Flask-based REST API for kosher restaurant discovery with FPT feed validation.
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
import psycopg2

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
    
    return {
        'id': restaurant.id,
        'name': restaurant.name,
        'address': restaurant.address,
        'city': restaurant.city,
        'state': restaurant.state,
        'zip_code': restaurant.zip_code,
        'phone': restaurant.phone,
        'website': restaurant.website,
        'cuisine_type': restaurant.cuisine_type,
        'price_range': restaurant.price_range,
        'rating': restaurant.rating,
        'review_count': restaurant.review_count,
        'latitude': restaurant.latitude,
        'longitude': restaurant.longitude,
        'hours': restaurant.hours,
        'description': restaurant.description,
        'image_url': restaurant.image_url,
        'is_kosher': restaurant.is_kosher,
        'is_glatt': restaurant.is_glatt,
        'is_cholov_yisroel': restaurant.is_cholov_yisroel,
        'is_pas_yisroel': restaurant.is_pas_yisroel,
        'is_bishul_yisroel': restaurant.is_bishul_yisroel,
        'is_mehadrin': restaurant.is_mehadrin,
        'is_hechsher': restaurant.is_hechsher,
        'hechsher_details': restaurant.hechsher_details,
        'created_at': restaurant.created_at.isoformat() if restaurant.created_at else None,
        'updated_at': restaurant.updated_at.isoformat() if restaurant.updated_at else None
    }

def fix_database_schema():
    """Fix database schema by adding missing columns."""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        logger.error("DATABASE_URL environment variable not found")
        return False
    
    try:
        # Connect to database
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        logger.info("Connected to database for schema fix")
        
        # SQL statements to add missing columns
        alter_statements = [
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS phone VARCHAR(50)",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS website VARCHAR(500)",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS cuisine_type VARCHAR(100)",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS price_range VARCHAR(20)",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS review_count INTEGER",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS hours TEXT",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS description TEXT",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS image_url VARCHAR(500)",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS is_kosher BOOLEAN DEFAULT FALSE",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS is_glatt BOOLEAN DEFAULT FALSE",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS is_cholov_yisroel BOOLEAN DEFAULT FALSE",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS is_pas_yisroel BOOLEAN DEFAULT FALSE",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS is_bishul_yisroel BOOLEAN DEFAULT FALSE",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS is_mehadrin BOOLEAN DEFAULT FALSE",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS is_hechsher BOOLEAN DEFAULT FALSE",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS hechsher_details VARCHAR(500)",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        ]
        
        # Execute each ALTER statement
        for sql in alter_statements:
            try:
                cursor.execute(sql)
                logger.info(f"Schema fix: {sql}")
            except Exception as e:
                logger.warning(f"Schema fix warning: {sql} - {e}")
        
        # Commit changes
        conn.commit()
        logger.info("Database schema fix completed successfully")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        logger.error("Error fixing database schema", error=str(e))
        return False

def create_app(config_name=None):
    """Application factory pattern for Flask app creation."""
    app = Flask(__name__)
    
    # Load configuration
    config = get_config()
    app.config.from_object(config)
    
    # Initialize CORS with production-ready settings
    CORS(app, 
         origins=app.config['CORS_ORIGINS'],
         methods=app.config['CORS_METHODS'],
         allow_headers=app.config['CORS_ALLOW_HEADERS'],
         supports_credentials=True)
    
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
    
    # Fix database schema on startup
    try:
        logger.info("Running database schema fix on startup...")
        fix_database_schema()
        logger.info("Database schema fix completed on startup")
    except Exception as e:
        logger.error("Failed to fix database schema on startup", error=str(e))
    
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
    
    # Run schema fix on app startup
    with app.app_context():
        try:
            logger.info("Running database schema fix on startup...")
            fix_database_schema()
            logger.info("Database schema fix completed successfully")
        except Exception as e:
            logger.error("Failed to run schema fix on startup", error=str(e))
    
    @app.teardown_appcontext
    def teardown_db(exception):
        """Close database connection after each request."""
        if hasattr(g, 'db_manager') and g.db_manager:
            try:
                g.db_manager.disconnect()
            except Exception as e:
                logger.error("Error disconnecting database", error=str(e))
            g.db_manager = None
    
    @app.route('/')
    @limiter.limit("100 per minute")
    def index():
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
                'health': '/health',
                'admin': {
                    'add_restaurant': '/api/admin/restaurants',
                    'bulk_import': '/api/admin/restaurants/bulk',
                    'update_restaurant': '/api/admin/restaurants/<business_id>',
                    'add_special': '/api/admin/restaurants/<business_id>/specials',
                    'get_specials': '/api/admin/specials'
                }
            },
            'documentation': 'https://jewgo.com/api/docs',
            'timestamp': datetime.utcnow().isoformat()
        })
    
    @app.route('/api/restaurants')
    @limiter.limit("200 per minute")
    def api_restaurants():
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
            
            # Convert Restaurant objects to dictionaries for JSON serialization
            restaurants_data = [restaurant_to_dict(restaurant) for restaurant in restaurants]
            
            # Add metadata to response
            response = {
                'success': True,
                'data': restaurants_data,
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
    
    @app.route('/api/restaurants/<business_id>')
    @limiter.limit("100 per minute")
    def api_restaurant_detail(business_id):
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
                'data': restaurant_data,
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
    
    # Admin endpoints for restaurant management
    @app.route('/api/admin/restaurants', methods=['POST'])
    @limiter.limit("50 per minute")
    def admin_add_restaurant():
        """Add a new restaurant via admin API."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided', 'success': False}), 400
            
            # Validate required fields
            required_fields = ['business_id', 'name']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'error': f'Missing required field: {field}', 'success': False}), 400
            
            # Add restaurant
            success = g.db_manager.add_restaurant(data)
            if success:
                return jsonify({'success': True, 'message': 'Restaurant added successfully'})
            else:
                return jsonify({'error': 'Failed to add restaurant', 'success': False}), 500
                
        except Exception as e:
            logger.error("Error adding restaurant", error=str(e))
            return jsonify({'error': 'Internal server error', 'success': False}), 500

    @app.route('/api/admin/restaurants/bulk', methods=['POST'])
    @limiter.limit("10 per minute")
    def admin_bulk_import():
        """Bulk import restaurants via admin API."""
        try:
            data = request.get_json()
            if not data or 'restaurants' not in data:
                return jsonify({'error': 'No restaurants data provided', 'success': False}), 400
            
            restaurants = data['restaurants']
            if not isinstance(restaurants, list):
                return jsonify({'error': 'Restaurants must be a list', 'success': False}), 400
            
            success_count = 0
            error_count = 0
            errors = []
            
            for i, restaurant in enumerate(restaurants):
                try:
                    if g.db_manager.add_restaurant(restaurant):
                        success_count += 1
                    else:
                        error_count += 1
                        errors.append(f"Restaurant {i}: Failed to add to database")
                except Exception as e:
                    error_count += 1
                    errors.append(f"Restaurant {i}: {str(e)}")
                
                # Limit error messages to first 10
                if len(errors) >= 10:
                    break
            
            return jsonify({
                'success': True,
                'message': f'Bulk import completed: {success_count} successful, {error_count} failed',
                'success_count': success_count,
                'error_count': error_count,
                'errors': errors
            })
            
        except Exception as e:
            logger.error("Error in bulk import", error=str(e))
            return jsonify({'error': 'Internal server error', 'success': False}), 500

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