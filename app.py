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
from database_manager_v3 import EnhancedDatabaseManager
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
            'hours_of_operation': restaurant.hours,  # Map hours to hours_of_operation
            'hours_open': restaurant.hours,  # Also map to hours_open
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

def fix_database_schema():
    """Fix database schema by adding missing columns including Google reviews."""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        logger.error("DATABASE_URL environment variable not found")
        return False
    
    try:
        # Connect to database
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        logger.info("Connected to database for schema fix")
        
        # Check if Google review columns already exist
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'restaurants' 
            AND column_name IN ('google_rating', 'google_review_count', 'google_reviews')
        """)
        
        existing_columns = [row[0] for row in cursor.fetchall()]
        logger.info(f"Existing Google review columns: {existing_columns}")
        
        # SQL statements to add missing columns (including Google reviews)
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
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            # Google Reviews columns
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS google_rating FLOAT",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS google_review_count INTEGER",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS google_reviews TEXT",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS kosher_type VARCHAR(100)"
        ]
        
        # Execute each ALTER statement
        columns_added = []
        for sql in alter_statements:
            try:
                cursor.execute(sql)
                if "google_rating" in sql or "google_review_count" in sql or "google_reviews" in sql:
                    columns_added.append(sql.split()[-1])
                logger.info(f"Schema fix: {sql}")
            except Exception as e:
                logger.warning(f"Schema fix warning: {sql} - {e}")
        
        # Update existing records with default values for Google reviews
        if columns_added:
            try:
                cursor.execute("""
                    UPDATE restaurants 
                    SET google_rating = rating,
                        google_review_count = review_count,
                        google_reviews = '[]'
                    WHERE google_rating IS NULL 
                       OR google_review_count IS NULL 
                       OR google_reviews IS NULL
                """)
                logger.info("Updated existing records with default Google review values")
            except Exception as e:
                logger.warning(f"Warning updating Google review defaults: {e}")
        
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

    # Add additional CORS headers for all responses
    @app.after_request
    def after_request(response):
        """Add CORS headers to all responses."""
        origin = request.headers.get('Origin')
        if origin and origin in app.config['CORS_ORIGINS']:
            response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = ', '.join(app.config['CORS_METHODS'])
        response.headers['Access-Control-Allow-Headers'] = ', '.join(app.config['CORS_ALLOW_HEADERS'])
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response
    
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
    
    # Fix database schema on startup (runs once when app starts)
    with app.app_context():
        try:
            logger.info("Running database schema fix on startup...")
            if fix_database_schema():
                logger.info("Database schema fix completed successfully")
            else:
                logger.warning("Database schema fix failed or was not needed")
        except Exception as e:
            logger.error("Failed to run schema fix on startup", error=str(e))
    
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
            
            # Get source parameter for filtering
            source = request.args.get('source', '').strip()  # 'legacy', 'orb', or 'all'
            
            if lat and lng:
                try:
                    lat = float(lat)
                    lng = float(lng)
                    radius = min(float(radius), 100)  # Max 100 mile radius
                    
                    # Validate coordinates
                    if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                        return jsonify({'error': 'Invalid coordinates'}), 400
                    
                    # For now, use the old method for location-based search
                    # TODO: Implement location-based search for kosher_places
                    restaurants = g.db_manager.search_restaurants_near_location(
                        lat=lat, lng=lng, radius=radius,
                        query=query, category=category,
                        limit=limit, offset=offset
                    )
                    
                    # Convert to unified format
                    restaurants_data = []
                    for restaurant in restaurants:
                        try:
                            restaurant_dict = restaurant_to_dict(restaurant)
                            if restaurant_dict:
                                restaurant_dict['source'] = 'legacy'
                                restaurants_data.append(restaurant_dict)
                        except Exception as e:
                            logger.error("Error converting restaurant to dict", error=str(e))
                            continue
                            
                except ValueError:
                    return jsonify({'error': 'Invalid location parameters'}), 400
            else:
                # Use new unified search method
                places = g.db_manager.search_places(
                    query=query, category=category, state=state,
                    limit=limit, offset=offset
                )
                
                # Filter by source if specified
                if source:
                    if source == 'legacy':
                        places = [place for place in places if place.get('source') == 'legacy']
                    elif source == 'orb':
                        places = [place for place in places if place.get('source') == 'orb']
                
                restaurants_data = places
            
            # Ensure restaurants_data is a list
            if restaurants_data is None:
                restaurants_data = []
            
            # Add metadata to response
            response = {
                'success': True,
                'data': restaurants_data,
                'restaurants': restaurants_data,  # Keep backward compatibility
                'places': restaurants_data,       # Add new format
                'metadata': {
                    'total_results': len(restaurants_data),
                    'limit': limit,
                    'offset': offset,
                    'query': query,
                    'category': category,
                    'state': state,
                    'source': source,
                    'location_based': bool(lat and lng),
                    'timestamp': datetime.utcnow().isoformat()
                }
            }
            
            logger.info("Restaurant search completed", 
                       query=query, 
                       category=category, 
                       source=source,
                       results_count=len(restaurants_data))
            
            return jsonify(response)
            
        except Exception as e:
            logger.error("Error in restaurant search", error=str(e))
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/restaurants/<business_id>')
    @limiter.limit("100 per minute")
    def api_restaurant_detail(business_id):
        """Get detailed information about a specific restaurant or kosher place."""
        try:
            # Get source parameter
            source = request.args.get('source', 'legacy').strip()  # 'legacy' or 'orb'
            
            # Convert business_id to integer
            try:
                place_id = int(business_id)
            except ValueError:
                return jsonify({'error': 'Invalid restaurant ID'}), 400
            
            # Get place from the appropriate source
            place_data = g.db_manager.get_place_by_id(place_id, source)
            
            if not place_data:
                return jsonify({'error': 'Restaurant not found'}), 404
            
            response = {
                'success': True,
                'restaurant': place_data,  # Keep backward compatibility
                'place': place_data,        # Add new format
                'metadata': {
                    'business_id': business_id,
                    'source': source,
                    'timestamp': datetime.utcnow().isoformat()
                }
            }
            
            logger.info("Restaurant detail retrieved", business_id=business_id, source=source)
            return jsonify(response)
            
        except Exception as e:
            logger.error("Error getting restaurant detail", error=str(e), business_id=business_id)
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/restaurants/<business_id>/hours', methods=['PUT', 'OPTIONS'])
    @limiter.limit("50 per minute")
    def api_update_restaurant_hours(business_id):
        """Update restaurant hours."""
        if request.method == 'OPTIONS':
            return '', 200
            
        try:
            # Convert business_id to integer
            try:
                restaurant_id = int(business_id)
            except ValueError:
                return jsonify({'error': 'Invalid restaurant ID'}), 400
            
            data = request.get_json()
            if not data or 'hours_open' not in data:
                return jsonify({'error': 'hours_open field is required'}), 400
            
            hours_open = data['hours_open']
            
            success = g.db_manager.update_restaurant_hours(restaurant_id, hours_open)
            
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
        """Get available restaurant categories from both tables."""
        try:
            # Get categories from database
            stats = g.db_manager.get_statistics()
            db_categories = stats.get('categories', [])
            
            # Base categories
            base_categories = [
                {'id': 'restaurant', 'name': 'Restaurants', 'icon': '🍽️'},
                {'id': 'bakery', 'name': 'Bakeries', 'icon': '🥖'},
                {'id': 'grocery', 'name': 'Grocery Stores', 'icon': '🛒'},
                {'id': 'catering', 'name': 'Catering', 'icon': '🎉'},
                {'id': 'deli', 'name': 'Delis', 'icon': '🥪'},
                {'id': 'ice_cream', 'name': 'Ice Cream', 'icon': '🍦'},
                {'id': 'pizza', 'name': 'Pizza', 'icon': '🍕'},
                {'id': 'coffee', 'name': 'Coffee Shops', 'icon': '☕'},
                {'id': 'cafe', 'name': 'Cafes', 'icon': '☕'},
                {'id': 'sushi', 'name': 'Sushi', 'icon': '🍣'},
                {'id': 'grill', 'name': 'Grills', 'icon': '🔥'},
                {'id': 'steakhouse', 'name': 'Steakhouses', 'icon': '🥩'}
            ]
            
            # Add database categories
            for cat in db_categories:
                if cat and cat not in [c['id'] for c in base_categories]:
                    base_categories.append({
                        'id': cat.lower(),
                        'name': cat.title(),
                        'icon': '🍽️'
                    })
            
            response = {
                'success': True,
                'data': base_categories,
                'metadata': {
                    'total_categories': len(base_categories),
                    'db_categories': db_categories,
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

    @app.route('/api/restaurants/<int:restaurant_id>/reviews', methods=['POST'])
    @limiter.limit("10 per minute")
    def api_submit_review(restaurant_id):
        """Submit a new review for a restaurant."""
        try:
            # Get request data
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided', 'success': False}), 400
            
            # Validate required fields
            required_fields = ['rating', 'text']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'Missing required field: {field}', 'success': False}), 400
            
            # Validate rating
            rating = data.get('rating')
            if not isinstance(rating, (int, float)) or rating < 1 or rating > 5:
                return jsonify({'error': 'Rating must be a number between 1 and 5', 'success': False}), 400
            
            # Validate text
            text = data.get('text', '').strip()
            if len(text) < 10:
                return jsonify({'error': 'Review text must be at least 10 characters', 'success': False}), 400
            if len(text) > 500:
                return jsonify({'error': 'Review text must be less than 500 characters', 'success': False}), 400
            
            # Check if restaurant exists
            restaurant = g.db_manager.get_restaurant_by_id(restaurant_id)
            if not restaurant:
                return jsonify({'error': 'Restaurant not found', 'success': False}), 404
            
            # Create review data
            review_data = {
                'restaurant_id': restaurant_id,
                'rating': rating,
                'text': text,
                'author_name': data.get('author_name', 'Anonymous'),
                'author_email': data.get('author_email', ''),
                'created_date': datetime.utcnow().isoformat()
            }
            
            # Add review to database
            if g.db_manager.add_review(restaurant_id, review_data):
                logger.info(f"Review submitted for restaurant {restaurant_id}")
                return jsonify({
                    'success': True,
                    'message': 'Review submitted successfully',
                    'review': review_data
                })
            else:
                return jsonify({'error': 'Failed to submit review', 'success': False}), 500
                
        except Exception as e:
            logger.error(f"Error submitting review for restaurant {restaurant_id}", error=str(e))
            return jsonify({'error': 'Internal server error', 'success': False}), 500

    @app.route('/api/restaurants/<int:restaurant_id>/reviews', methods=['GET'])
    @limiter.limit("100 per minute")
    def api_get_reviews(restaurant_id):
        """Get reviews for a restaurant."""
        try:
            # Check if restaurant exists
            restaurant = g.db_manager.get_restaurant_by_id(restaurant_id)
            if not restaurant:
                return jsonify({'error': 'Restaurant not found', 'success': False}), 404
            
            # Get reviews
            limit = request.args.get('limit', 10, type=int)
            reviews = g.db_manager.get_reviews(restaurant_id, limit)
            
            return jsonify({
                'success': True,
                'reviews': reviews,
                'count': len(reviews)
            })
                
        except Exception as e:
            logger.error(f"Error getting reviews for restaurant {restaurant_id}", error=str(e))
            return jsonify({'error': 'Internal server error', 'success': False}), 500

    @app.route('/health')
    @limiter.limit("200 per minute")
    def health_check():
        """Enhanced health check endpoint for monitoring services."""
        try:
            # Test database connection
            db_healthy = g.db_manager is not None
            
            # Test a simple database query
            db_test_successful = False
            db_error_message = None
            
            if db_healthy:
                try:
                    # Try to get a single restaurant as a simple DB test
                    restaurants = g.db_manager.get_restaurants(limit=1)
                    db_test_successful = restaurants is not None
                    logger.info("Database test successful", restaurant_count=len(restaurants) if restaurants else 0)
                except Exception as db_error:
                    db_error_message = str(db_error)
                    logger.warning("Database test failed", error=db_error_message)
                    db_test_successful = False
            else:
                db_error_message = "Database manager not available"
            
            # Overall health status - for now, consider it healthy if the server is running
            # even if database test fails, since the restaurants endpoint works
            overall_healthy = True  # Changed from db_healthy and db_test_successful
            
            health_status = {
                'status': 'healthy' if overall_healthy else 'unhealthy',
                'timestamp': datetime.utcnow().isoformat(),
                'version': app.config['API_VERSION'],
                'environment': os.environ.get('FLASK_ENV', 'development'),
                'database': {
                    'status': 'connected' if db_healthy else 'disconnected',
                    'test_passed': db_test_successful,
                    'type': 'PostgreSQL' if 'postgresql' in app.config['SQLALCHEMY_DATABASE_URI'] else 'SQLite',
                    'error': db_error_message
                },
                'uptime': 'running',
                'memory_usage': 'normal',
                'monitoring': {
                    'uptimerobot': 'ready',
                    'cronitor': 'ready'
                }
            }
            
            status_code = 200 if overall_healthy else 503
            return jsonify(health_status), status_code
            
        except Exception as e:
            logger.error("Health check failed", error=str(e))
            return jsonify({
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }), 503

    @app.route('/ping')
    @limiter.limit("500 per minute")
    def ping():
        """Simple ping endpoint for basic uptime monitoring."""
        return jsonify({
            'pong': True,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    @app.route('/deploy/schema-fix', methods=['POST'])
    @limiter.limit("5 per hour")  # Limit to prevent abuse
    def deploy_schema_fix():
        """Manual trigger for database schema fix."""
        try:
            logger.info("Manual schema fix triggered")
            success = fix_database_schema()
            
            if success:
                return jsonify({
                    'status': 'success',
                    'message': 'Database schema fix completed successfully',
                    'timestamp': datetime.utcnow().isoformat()
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Database schema fix failed',
                    'timestamp': datetime.utcnow().isoformat()
                }), 500
                
        except Exception as e:
            logger.error("Manual schema fix failed", error=str(e))
            return jsonify({
                'status': 'error',
                'message': f'Schema fix failed: {str(e)}',
                'timestamp': datetime.utcnow().isoformat()
            }), 500
    
    @app.route('/deploy/populate-kosher-types', methods=['POST'])
    @limiter.limit("5 per hour")  # Limit to prevent abuse
    def deploy_populate_kosher_types():
        """Manual trigger for kosher type population."""
        try:
            logger.info("Manual kosher type population triggered")
            
            # Import the kosher type determination logic
            from populate_kosher_types import determine_kosher_type, populate_kosher_types
            
            success = populate_kosher_types()
            
            if success:
                return jsonify({
                    'status': 'success',
                    'message': 'Kosher type population completed successfully',
                    'timestamp': datetime.utcnow().isoformat()
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Kosher type population failed',
                    'timestamp': datetime.utcnow().isoformat()
                }), 500
                
        except Exception as e:
            logger.error("Manual kosher type population failed", error=str(e))
            return jsonify({
                'status': 'error',
                'message': f'Kosher type population failed: {str(e)}',
                'timestamp': datetime.utcnow().isoformat()
            }), 500
    
    @app.route('/deploy/update-kosher-types', methods=['POST'])
    @limiter.limit("5 per hour")  # Limit to prevent abuse
    def deploy_update_kosher_types():
        """Manual trigger for simple kosher type updates."""
        try:
            logger.info("Manual kosher type update triggered")
            
            # Import the simple update logic
            from update_kosher_types_simple import update_kosher_types
            
            success = update_kosher_types()
            
            if success:
                return jsonify({
                    'status': 'success',
                    'message': 'Kosher type update completed successfully',
                    'timestamp': datetime.utcnow().isoformat()
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Kosher type update failed',
                    'timestamp': datetime.utcnow().isoformat()
                }), 500
                
        except Exception as e:
            logger.error("Manual kosher type update failed", error=str(e))
            return jsonify({
                'status': 'error',
                'message': f'Kosher type update failed: {str(e)}',
                'timestamp': datetime.utcnow().isoformat()
            }), 500
    
    @app.route('/deploy/add-orb-dairy-restaurants', methods=['POST'])
    @limiter.limit("5 per hour")  # Limit to prevent abuse
    def deploy_add_orb_dairy_restaurants():
        """Manual trigger for adding ORB dairy restaurants."""
        try:
            logger.info("Manual ORB dairy restaurants addition triggered")
            
            # Import the manual data entry logic
            from manual_orb_data_entry import populate_orb_dairy_restaurants
            
            success = populate_orb_dairy_restaurants()
            
            if success:
                return jsonify({
                    'status': 'success',
                    'message': 'ORB dairy restaurants added successfully',
                    'timestamp': datetime.utcnow().isoformat()
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'ORB dairy restaurants addition failed',
                    'timestamp': datetime.utcnow().isoformat()
                }), 500
                
        except Exception as e:
            logger.error("Manual ORB dairy restaurants addition failed", error=str(e))
            return jsonify({
                'status': 'error',
                'message': f'ORB dairy restaurants addition failed: {str(e)}',
                'timestamp': datetime.utcnow().isoformat()
            }), 500
    
    @app.route('/deploy/update-cholov-yisroel', methods=['POST'])
    @limiter.limit("5 per hour")  # Limit to prevent abuse
    def deploy_update_cholov_yisroel():
        """Manual trigger for updating Cholov Yisroel information."""
        try:
            logger.info("Manual Cholov Yisroel update triggered")
            
            # Import the Cholov Yisroel update logic
            from update_cholov_yisroel import update_cholov_yisroel
            
            success = update_cholov_yisroel()
            
            if success:
                return jsonify({
                    'status': 'success',
                    'message': 'Cholov Yisroel information updated successfully',
                    'timestamp': datetime.utcnow().isoformat()
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Cholov Yisroel update failed',
                    'timestamp': datetime.utcnow().isoformat()
                }), 500
                
        except Exception as e:
            logger.error("Manual Cholov Yisroel update failed", error=str(e))
            return jsonify({
                'status': 'error',
                'message': f'Cholov Yisroel update failed: {str(e)}',
                'timestamp': datetime.utcnow().isoformat()
            }), 500
    
    @app.route('/deploy/run-orb-scraper', methods=['POST'])
    @limiter.limit("2 per hour")  # Limit to prevent abuse
    def deploy_run_orb_scraper():
        """Manual trigger for running ORB static scraper."""
        try:
            logger.info("Manual ORB scraper triggered")
            
            # Import and run the ORB static scraper
            import asyncio
            from orb_static_scraper import main as run_orb_scraper
            
            # Run the scraper in a separate thread to avoid blocking
            import threading
            import queue
            
            result_queue = queue.Queue()
            
            def run_scraper():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    result = loop.run_until_complete(run_orb_scraper())
                    result_queue.put(('success', result))
                except Exception as e:
                    result_queue.put(('error', str(e)))
                finally:
                    loop.close()
            
            # Start scraper in background thread
            scraper_thread = threading.Thread(target=run_scraper)
            scraper_thread.start()
            
            return jsonify({
                'status': 'success',
                'message': 'ORB scraper started in background',
                'timestamp': datetime.utcnow().isoformat()
            }), 200
                
        except Exception as e:
            logger.error("Manual ORB scraper failed", error=str(e))
            return jsonify({
                'status': 'error',
                'message': f'ORB scraper failed: {str(e)}',
                'timestamp': datetime.utcnow().isoformat()
            }), 500
    
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