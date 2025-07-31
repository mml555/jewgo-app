#!/usr/bin/env python3
"""
JewGo Backend API Server
========================

Main Flask application for the JewGo backend API.
Handles restaurant data, kosher supervision information, and search functionality.

Author: JewGo Development Team
Version: 3.0
Last Updated: 2024
"""

import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import structlog

# Load environment variables
load_dotenv()

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

# Import database manager and Restaurant model
from database.database_manager_v3 import EnhancedDatabaseManager, Restaurant

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize database manager
db_manager = None

def init_database():
    """Initialize database connection."""
    global db_manager
    try:
        db_manager = EnhancedDatabaseManager()
        db_manager.connect()
        logger.info("Database connection established")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

# Initialize database on app startup
with app.app_context():
    init_database()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        if db_manager:
            # Test database connection
            from database.database_manager_v3 import Restaurant
            session = db_manager.get_session()
            total_restaurants = session.query(Restaurant).count()
            session.close()
            
            return jsonify({
                'status': 'healthy',
                'database': 'connected',
                'restaurants_count': total_restaurants,
                'version': '3.0'
            }), 200
        else:
            return jsonify({
                'status': 'unhealthy',
                'database': 'disconnected',
                'error': 'Database not initialized'
            }), 500
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    """Get all restaurants with optional filtering."""
    try:
        # Get query parameters
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        kosher_type = request.args.get('kosher_type')
        state = request.args.get('state')
        
        # Get restaurants from database
        restaurants = db_manager.get_all_places(
            limit=limit,
            offset=offset
        )
        
        # Apply filters
        if kosher_type:
            restaurants = [r for r in restaurants if r.get('kosher_type') == kosher_type]
        
        if state:
            restaurants = [r for r in restaurants if r.get('state') == state]
        
        logger.info(f"Retrieved {len(restaurants)} restaurants")
        
        return jsonify({
            'restaurants': restaurants,
            'total': len(restaurants),
            'limit': limit,
            'offset': offset
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting restaurants: {e}")
        return jsonify({
            'error': 'Failed to retrieve restaurants',
            'message': str(e)
        }), 500

@app.route('/api/restaurants/search', methods=['GET'])
def search_restaurants():
    """Search restaurants by name or location."""
    try:
        query = request.args.get('q', '')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        if not query:
            return jsonify({
                'error': 'Query parameter "q" is required'
            }), 400
        
        # Search restaurants
        results = db_manager.search_places(
            query=query,
            limit=limit,
            offset=offset
        )
        
        logger.info(f"Search for '{query}' returned {len(results)} results")
        
        return jsonify({
            'restaurants': results,
            'query': query,
            'total': len(results),
            'limit': limit,
            'offset': offset
        }), 200
        
    except Exception as e:
        logger.error(f"Error searching restaurants: {e}")
        return jsonify({
            'error': 'Failed to search restaurants',
            'message': str(e)
        }), 500

@app.route('/api/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    """Get a specific restaurant by ID."""
    try:
        restaurant = db_manager.get_place_by_id(restaurant_id)
        
        if not restaurant:
            return jsonify({
                'error': 'Restaurant not found'
            }), 404
        
        return jsonify(restaurant), 200
        
    except Exception as e:
        logger.error(f"Error getting restaurant {restaurant_id}: {e}")
        return jsonify({
            'error': 'Failed to retrieve restaurant',
            'message': str(e)
        }), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get database statistics."""
    try:
        stats = db_manager.get_statistics()
        return jsonify(stats), 200
        
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({
            'error': 'Failed to retrieve statistics',
            'message': str(e)
        }), 500

@app.route('/api/kosher-types', methods=['GET'])
def get_kosher_types():
    """Get available kosher types and counts."""
    try:
        session = db_manager.get_session()
        
        # Get kosher type distribution
        from database.database_manager_v3 import Restaurant
        from sqlalchemy import func
        
        kosher_types = session.query(
            Restaurant.kosher_type,
            func.count(Restaurant.kosher_type)
        ).group_by(Restaurant.kosher_type).all()
        
        # Get Chalav Yisroel/Stam counts
        chalav_yisroel_count = session.query(Restaurant).filter(
            Restaurant.is_cholov_yisroel == True
        ).count()
        
        chalav_stam_count = session.query(Restaurant).filter(
            Restaurant.is_cholov_yisroel == False,
            Restaurant.kosher_type == 'dairy'
        ).count()
        
        # Get Pas Yisroel count
        pas_yisroel_count = session.query(Restaurant).filter(
            Restaurant.is_pas_yisroel == True
        ).count()
        
        session.close()
        
        return jsonify({
            'kosher_types': dict(kosher_types),
            'chalav_yisroel': chalav_yisroel_count,
            'chalav_stam': chalav_stam_count,
            'pas_yisroel': pas_yisroel_count
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting kosher types: {e}")
        return jsonify({
            'error': 'Failed to retrieve kosher types',
            'message': str(e)
        }), 500

@app.route('/api/migrate', methods=['GET', 'POST'])
def run_migration():
    """Run database migration to add missing columns."""
    try:
        from sqlalchemy import text
        
        # Define the columns to add
        columns_to_add = [
            ("cuisine_type", "VARCHAR(100)"),
            ("hechsher_details", "VARCHAR(500)"),
            ("description", "TEXT"),
            ("latitude", "FLOAT"),
            ("longitude", "FLOAT"),
            ("rating", "FLOAT"),
            ("review_count", "INTEGER"),
            ("google_rating", "FLOAT"),
            ("google_review_count", "INTEGER"),
            ("google_reviews", "TEXT"),
            ("hours", "TEXT")
        ]
        
        engine = db_manager.engine
        added_columns = []
        
        with engine.connect() as conn:
            for column_name, column_type in columns_to_add:
                try:
                    # Check if column exists
                    result = conn.execute(text(f"""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = 'restaurants' 
                        AND column_name = '{column_name}'
                    """))
                    
                    if not result.fetchone():
                        # Column doesn't exist, add it
                        logger.info(f"Adding column {column_name} to restaurants table")
                        conn.execute(text(f"ALTER TABLE restaurants ADD COLUMN {column_name} {column_type}"))
                        conn.commit()
                        added_columns.append(column_name)
                        logger.info(f"Successfully added column {column_name}")
                    else:
                        logger.info(f"Column {column_name} already exists, skipping")
                        
                except Exception as e:
                    logger.error(f"Error adding column {column_name}: {e}")
                    return jsonify({
                        'error': f'Failed to add column {column_name}: {str(e)}'
                    }), 500
        
        return jsonify({
            'success': True,
            'message': 'Migration completed successfully',
            'added_columns': added_columns
        }), 200
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        return jsonify({
            'error': f'Migration failed: {str(e)}'
        }), 500

@app.route('/fix', methods=['GET'])
def fix_database():
    """Simple endpoint to fix database schema."""
    try:
        from sqlalchemy import text
        
        # Define the columns to add
        columns_to_add = [
            ("cuisine_type", "VARCHAR(100)"),
            ("hechsher_details", "VARCHAR(500)"),
            ("description", "TEXT"),
            ("latitude", "FLOAT"),
            ("longitude", "FLOAT"),
            ("rating", "FLOAT"),
            ("review_count", "INTEGER"),
            ("google_rating", "FLOAT"),
            ("google_review_count", "INTEGER"),
            ("google_reviews", "TEXT"),
            ("hours", "TEXT")
        ]
        
        engine = db_manager.engine
        added_columns = []
        
        for column_name, column_type in columns_to_add:
            try:
                with engine.connect() as conn:
                    # Check if column exists
                    result = conn.execute(text(f"""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = 'restaurants' 
                        AND column_name = '{column_name}'
                    """))
                    
                    if not result.fetchone():
                        # Column doesn't exist, add it
                        logger.info(f"Adding column {column_name} to restaurants table")
                        conn.execute(text(f"ALTER TABLE restaurants ADD COLUMN {column_name} {column_type}"))
                        conn.commit()
                        added_columns.append(column_name)
                        logger.info(f"Successfully added column {column_name}")
                    else:
                        logger.info(f"Column {column_name} already exists, skipping")
                        
            except Exception as e:
                logger.error(f"Error adding column {column_name}: {e}")
                return jsonify({
                    'error': f'Failed to add column {column_name}: {str(e)}'
                }), 500
        
        return jsonify({
            'success': True,
            'message': 'Database fix completed successfully',
            'added_columns': added_columns
        }), 200
        
    except Exception as e:
        logger.error(f"Database fix failed: {e}")
        return jsonify({
            'error': f'Database fix failed: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested endpoint does not exist'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    # Initialize database
    if init_database():
        logger.info("Starting JewGo Backend API Server")
        app.run(
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000)),
            debug=os.environ.get('ENVIRONMENT') != 'production'
        )
    else:
        logger.error("Failed to initialize database. Exiting.")
        exit(1) 