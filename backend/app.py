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
import json
from datetime import datetime

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

# Import Google Places functionality
import requests
import time

# Initialize Flask app
app = Flask(__name__)

# Load configuration
from config.config import get_config
app.config.from_object(get_config())

# Initialize CORS with configuration
CORS(app, origins=app.config.get('CORS_ORIGINS', ['*']))

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

@app.route('/', methods=['GET'])
def root():
    """Root endpoint - redirect to health check or return API info."""
    return jsonify({
        'message': 'JewGo Backend API',
        'version': '3.0',
        'status': 'running',
        'endpoints': {
            'health': '/health',
            'restaurants': '/api/restaurants',
            'search': '/api/restaurants/search',
            'statistics': '/api/statistics'
        }
    }), 200

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
        # Support both kosher_type and kosher_category parameters for frontend compatibility
        kosher_category = request.args.get('kosher_category')
        state = request.args.get('state')
        
        # Get restaurants from database
        restaurants = db_manager.get_all_places(
            limit=limit,
            offset=offset
        )
        
        # Apply filters
        if kosher_category:
            restaurants = [r for r in restaurants if r.get('kosher_category') == kosher_category]
        
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
            Restaurant.kosher_category,
            func.count(Restaurant.kosher_category)
        ).group_by(Restaurant.kosher_category).all()
        
        # Get Chalav Yisroel/Stam counts
        chalav_yisroel_count = session.query(Restaurant).filter(
            Restaurant.is_cholov_yisroel == True
        ).count()
        
        chalav_stam_count = session.query(Restaurant).filter(
            Restaurant.is_cholov_yisroel == False,
            Restaurant.kosher_category == 'dairy'
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

@app.route('/api/remove-duplicates', methods=['POST'])
def remove_duplicates():
    """Remove duplicate restaurants from the database."""
    try:
        session = db_manager.get_session()
        
        # Find duplicates using SQL
        from sqlalchemy import text
        
        duplicate_query = text("""
            WITH duplicates AS (
                SELECT 
                    name,
                    MIN(id) as keep_id,
                    COUNT(*) as count
                FROM restaurants 
                GROUP BY name 
                HAVING COUNT(*) > 1
            )
            SELECT 
                d.name,
                d.keep_id,
                d.count,
                array_agg(r.id ORDER BY r.id) as all_ids
            FROM duplicates d
            JOIN restaurants r ON r.name = d.name
            GROUP BY d.name, d.keep_id, d.count
            ORDER BY d.name
        """)
        
        result = session.execute(duplicate_query)
        duplicates = result.fetchall()
        
        if not duplicates:
            return jsonify({
                'message': 'No duplicates found in database',
                'removed_count': 0
            }), 200
        
        total_removed = 0
        removed_details = []
        
        for duplicate in duplicates:
            name = duplicate.name
            keep_id = duplicate.keep_id
            count = duplicate.count
            all_ids = duplicate.all_ids
            
            # Remove all except the oldest (lowest ID)
            ids_to_remove = [id for id in all_ids if id != keep_id]
            
            # Delete the duplicates
            delete_query = text("DELETE FROM restaurants WHERE id = ANY(:ids)")
            session.execute(delete_query, {"ids": ids_to_remove})
            
            total_removed += len(ids_to_remove)
            
            removed_details.append({
                'name': name,
                'kept_id': keep_id,
                'removed_ids': ids_to_remove,
                'total_duplicates': count
            })
        
        # Commit the changes
        session.commit()
        
        # Get updated count
        verify_query = text("SELECT COUNT(*) as total FROM restaurants")
        result = session.execute(verify_query)
        total_restaurants = result.fetchone().total
        
        session.close()
        
        return jsonify({
            'message': f'Successfully removed {total_removed} duplicate restaurants',
            'removed_count': total_removed,
            'total_restaurants_after': total_restaurants,
            'removed_details': removed_details
        }), 200
        
    except Exception as e:
        logger.error(f"Error removing duplicates: {e}")
        if 'session' in locals():
            session.rollback()
            session.close()
        return jsonify({
            'error': 'Failed to remove duplicates',
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

def search_google_places(restaurant_name: str, address: str) -> str:
    """
    Search Google Places API for a restaurant's website.
    Returns the website URL if found, empty string otherwise.
    """
    try:
        api_key = os.environ.get('GOOGLE_PLACES_API_KEY')
        if not api_key:
            logger.warning("GOOGLE_PLACES_API_KEY not set")
            return ""
        
        # Build search query
        query = f"{restaurant_name} {address}"
        
        # Search for the place
        search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        search_params = {
            'query': query,
            'key': api_key,
            'type': 'restaurant'
        }
        
        logger.info(f"Searching Google Places for: {query}")
        response = requests.get(search_url, params=search_params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data['status'] == 'OK' and data['results']:
            place_id = data['results'][0]['place_id']
            
            # Get place details
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                'place_id': place_id,
                'fields': 'website',
                'key': api_key
            }
            
            logger.info(f"Getting place details for place_id: {place_id}")
            details_response = requests.get(details_url, params=details_params, timeout=10)
            details_response.raise_for_status()
            
            details_data = details_response.json()
            
            if details_data['status'] == 'OK' and 'result' in details_data:
                website = details_data['result'].get('website', '')
                if website:
                    logger.info(f"Found website for {restaurant_name}: {website}")
                    return website
            
            logger.warning(f"No website found for {restaurant_name}")
            return ""
        else:
            logger.warning(f"No place found for: {query}")
            return ""
            
    except Exception as e:
        logger.error(f"Error searching Google Places for {restaurant_name}: {e}")
        return ""

@app.route('/api/restaurants/<int:restaurant_id>/fetch-website', methods=['POST'])
def fetch_restaurant_website(restaurant_id):
    """Fetch website information for a specific restaurant using Google Places API."""
    try:
        # Get the restaurant from database
        session = db_manager.get_session()
        restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        
        if not restaurant:
            return jsonify({'error': 'Restaurant not found'}), 404
        
        # If restaurant already has a website, return it
        if restaurant.website:
            return jsonify({
                'success': True,
                'website': restaurant.website,
                'message': 'Restaurant already has a website'
            })
        
        # Try to get website from Google Places API if we have coordinates
        if restaurant.latitude and restaurant.longitude:
            try:
                # Import Google Places helper functions
                from utils.google_places_helper import search_google_places_website
                
                # Search for website using restaurant name and address
                website_url = search_google_places_website(restaurant.name, restaurant.address or "")
                
                if website_url:
                    # Update the restaurant with the found website
                    restaurant.website = website_url
                    session.commit()
                    
                    return jsonify({
                        'success': True,
                        'website': website_url,
                        'message': 'Website found via Google Places API'
                    })
                else:
                    return jsonify({
                        'success': False,
                        'message': 'No website found for this restaurant'
                    })
                    
            except Exception as e:
                logger.error(f"Error fetching website from Google Places: {e}")
                return jsonify({
                    'success': False,
                    'message': 'Failed to fetch website from Google Places API'
                })
        else:
            return jsonify({
                'success': False,
                'message': 'Restaurant coordinates not available for website lookup'
            })
            
    except Exception as e:
        logger.error(f"Error in fetch_restaurant_website: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        if 'session' in locals():
            session.close()

@app.route('/api/restaurants/fetch-missing-websites', methods=['POST'])
def fetch_missing_websites():
    """
    Fetch website links for all restaurants that don't have them.
    This is a bulk operation that can take some time.
    """
    try:
        if not db_manager:
            return jsonify({'error': 'Database not connected'}), 500
        
        # Get limit from request (default 10 to avoid long-running requests)
        limit = request.json.get('limit', 10) if request.is_json else 10
        
        session = db_manager.get_session()
        
        # Get restaurants without websites
        restaurants_without_websites = session.query(Restaurant).filter(
            (Restaurant.website.is_(None)) | 
            (Restaurant.website == '') | 
            (Restaurant.website == ' ')
        ).limit(limit).all()
        
        if not restaurants_without_websites:
            return jsonify({
                'message': 'No restaurants found without websites',
                'updated': 0,
                'total_checked': 0
            }), 200
        
        updated_count = 0
        total_checked = len(restaurants_without_websites)
        
        for restaurant in restaurants_without_websites:
            try:
                # Search for website using Google Places API
                website_url = search_google_places(restaurant.name, restaurant.address or "")
                
                if website_url:
                    # Update the restaurant with the found website
                    restaurant.website = website_url
                    updated_count += 1
                    logger.info(f"Updated restaurant {restaurant.id} with website: {website_url}")
                
                # Add delay to respect API rate limits
                time.sleep(0.2)  # 200ms delay between requests
                
            except Exception as e:
                logger.error(f"Error processing restaurant {restaurant.id}: {e}")
                continue
        
        # Commit all changes
        session.commit()
        
        logger.info(f"Bulk website update completed", updated=updated_count, total=total_checked)
        
        return jsonify({
            'message': 'Bulk website update completed',
            'updated': updated_count,
            'total_checked': total_checked,
            'limit_used': limit
        }), 200
        
    except Exception as e:
        logger.error(f"Error in bulk website update: {e}")
        return jsonify({'error': f'Error in bulk website update: {str(e)}'}), 500

def search_google_places_hours(restaurant_name: str, address: str) -> str:
    """
    Search Google Places API for a restaurant's opening hours.
    Returns the formatted hours string if found, empty string otherwise.
    """
    try:
        api_key = os.environ.get('GOOGLE_PLACES_API_KEY')
        if not api_key:
            logger.warning("GOOGLE_PLACES_API_KEY not set")
            return ""
        
        # Build search query
        query = f"{restaurant_name} {address}"
        
        # Search for the place
        search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        search_params = {
            'query': query,
            'key': api_key,
            'type': 'restaurant'
        }
        
        logger.info(f"Searching Google Places for hours: {query}")
        response = requests.get(search_url, params=search_params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data['status'] == 'OK' and data['results']:
            place_id = data['results'][0]['place_id']
            
            # Get place details
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                'place_id': place_id,
                'fields': 'opening_hours',
                'key': api_key
            }
            
            logger.info(f"Getting place details for hours, place_id: {place_id}")
            details_response = requests.get(details_url, params=details_params, timeout=10)
            details_response.raise_for_status()
            
            details_data = details_response.json()
            
            if details_data['status'] == 'OK' and 'result' in details_data:
                opening_hours = details_data['result'].get('opening_hours')
                if opening_hours and 'weekday_text' in opening_hours:
                    hours_formatted = format_hours_from_places_api(opening_hours)
                    if hours_formatted:
                        logger.info(f"Found hours for {restaurant_name}: {hours_formatted}")
                        return hours_formatted
            
            logger.warning(f"No hours found for {restaurant_name}")
            return ""
        else:
            logger.warning(f"No place found for hours: {query}")
            return ""
            
    except Exception as e:
        logger.error(f"Error searching Google Places for hours {restaurant_name}: {e}")
        return ""

def format_hours_from_places_api(opening_hours: dict) -> str:
    """
    Format opening hours from Google Places API format to our database format.
    """
    if not opening_hours or 'weekday_text' not in opening_hours:
        return ""
        
    # Google Places API provides weekday_text as a list of formatted strings
    # e.g., ["Monday: 11:00 AM – 10:00 PM", "Tuesday: 11:00 AM – 10:00 PM", ...]
    weekday_text = opening_hours['weekday_text']
    
    # Convert to our format: "Mon 11:00 AM – 10:00 PM, Tue 11:00 AM – 10:00 PM, ..."
    day_mapping = {
        'Monday': 'Mon',
        'Tuesday': 'Tue', 
        'Wednesday': 'Wed',
        'Thursday': 'Thu',
        'Friday': 'Fri',
        'Saturday': 'Sat',
        'Sunday': 'Sun'
    }
    
    formatted_hours = []
    for day_text in weekday_text:
        # Parse "Monday: 11:00 AM – 10:00 PM"
        if ': ' in day_text:
            day, hours = day_text.split(': ', 1)
            short_day = day_mapping.get(day, day[:3])
            formatted_hours.append(f"{short_day} {hours}")
    
    return ', '.join(formatted_hours)

@app.route('/api/restaurants/<int:restaurant_id>/fetch-hours', methods=['POST'])
def fetch_restaurant_hours(restaurant_id):
    """
    Fetch opening hours for a specific restaurant using Google Places API.
    This is a backup system when the restaurant doesn't have hours data.
    """
    try:
        if not db_manager:
            return jsonify({'error': 'Database not connected'}), 500
        
        # Get restaurant details
        session = db_manager.get_session()
        restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        
        if not restaurant:
            return jsonify({'error': 'Restaurant not found'}), 404
        
        # Check if restaurant already has hours
        if restaurant.hours_open and len(restaurant.hours_open) > 10:
            return jsonify({
                'message': 'Restaurant already has hours data',
                'hours': restaurant.hours_open
            }), 200
        
        # Search for hours using Google Places API
        hours_data = search_google_places_hours(restaurant.name, restaurant.address or "")
        
        if hours_data:
            # Update the restaurant with the found hours
            restaurant.hours_open = hours_data
            session.commit()
            
            logger.info(f"Updated restaurant {restaurant_id} with hours: {hours_data}")
            
            return jsonify({
                'message': 'Hours found and updated',
                'hours': hours_data,
                'restaurant_id': restaurant_id,
                'restaurant_name': restaurant.name
            }), 200
        else:
            return jsonify({
                'message': 'No hours found for this restaurant',
                'restaurant_id': restaurant_id,
                'restaurant_name': restaurant.name
            }), 404
            
    except Exception as e:
        logger.error(f"Error fetching hours for restaurant {restaurant_id}: {e}")
        return jsonify({'error': f'Error fetching hours: {str(e)}'}), 500

@app.route('/api/restaurants/fetch-missing-hours', methods=['POST'])
def fetch_missing_hours():
    """
    Fetch opening hours for all restaurants that don't have them.
    This is a bulk operation that can take some time.
    """
    try:
        if not db_manager:
            return jsonify({'error': 'Database not connected'}), 500
        
        # Get limit from request (default 10 to avoid long-running requests)
        limit = request.json.get('limit', 10) if request.is_json else 10
        
        session = db_manager.get_session()
        
        # Get restaurants without hours
        restaurants_without_hours = session.query(Restaurant).filter(
            (Restaurant.hours_open.is_(None)) | 
            (Restaurant.hours_open == '') | 
            (Restaurant.hours_open == ' ') |
            (Restaurant.hours_open == 'None')
        ).limit(limit).all()
        
        if not restaurants_without_hours:
            return jsonify({
                'message': 'No restaurants found without hours',
                'updated': 0,
                'total_checked': 0
            }), 200
        
        updated_count = 0
        total_checked = len(restaurants_without_hours)
        
        for restaurant in restaurants_without_hours:
            try:
                # Search for hours using Google Places API
                hours_data = search_google_places_hours(restaurant.name, restaurant.address or "")
                
                if hours_data:
                    # Update the restaurant with the found hours
                    restaurant.hours_open = hours_data
                    updated_count += 1
                    logger.info(f"Updated restaurant {restaurant.id} with hours: {hours_data}")
                
                # Add delay to respect API rate limits
                time.sleep(0.2)  # 200ms delay between requests
                
            except Exception as e:
                logger.error(f"Error processing restaurant {restaurant.id}: {e}")
                continue
        
        # Commit all changes
        session.commit()
        
        logger.info(f"Bulk hours update completed", updated=updated_count, total=total_checked)
        
        return jsonify({
            'message': 'Bulk hours update completed',
            'updated': updated_count,
            'total_checked': total_checked,
            'limit_used': limit
        }), 200
        
    except Exception as e:
        logger.error(f"Error in bulk hours update: {e}")
        return jsonify({'error': f'Error in bulk hours update: {str(e)}'        }), 500

@app.route('/api/update-database', methods=['POST'])
def update_database():
    """Update database with real ORB data."""
    try:
        import asyncio
        from scrapers.orb_scraper_v2 import ORBScraperV2
        
        session = db_manager.get_session()
        from database.database_manager_v3 import Restaurant
        
        # Step 1: Clear all existing restaurant data
        logger.info("Clearing all existing restaurant data...")
        deleted_count = session.query(Restaurant).delete()
        session.commit()
        logger.info(f"Deleted {deleted_count} existing restaurants")
        
        # Step 2: Load ORB data directly
        logger.info("Loading ORB data into database...")
        
        try:
            # Import and run the clean reload ORB data function
            from clean_reload_orb_data import clean_reload_orb_data
            businesses = clean_reload_orb_data()
            
            if businesses:
                logger.info("Clean reload ORB data completed successfully")
            else:
                logger.error("Clean reload ORB data failed")
                
        except Exception as e:
            logger.error(f"Error in clean reload ORB data: {e}")
            businesses = False
        
        if businesses:  # businesses is now a boolean indicating success
            logger.info("ORB scraper completed successfully")
            
            # Step 3: Verify the data (scraper already saved to database)
            final_count = session.query(Restaurant).count()
            logger.info(f"Final restaurant count: {final_count}")
            
            # Show final statistics
            from sqlalchemy import func
            kosher_types = session.query(
                Restaurant.kosher_category,
                func.count(Restaurant.kosher_category)
            ).group_by(Restaurant.kosher_category).all()
            
            # Show Chalav Yisroel statistics
            chalav_yisroel_count = session.query(Restaurant).filter(
                Restaurant.is_cholov_yisroel == True
            ).count()
            
            chalav_stam_count = session.query(Restaurant).filter(
                Restaurant.is_cholov_yisroel == False,
                Restaurant.kosher_category == 'dairy'
            ).count()
            
            pas_yisroel_count = session.query(Restaurant).filter(
                Restaurant.is_pas_yisroel == True
            ).count()
            
            return jsonify({
                'message': f'Successfully updated database with ORB restaurants',
                'deleted_count': deleted_count,
                'saved_count': final_count,
                'final_count': final_count,
                'kosher_types': dict(kosher_types),
                'chalav_yisroel': chalav_yisroel_count,
                'chalav_stam': chalav_stam_count,
                'pas_yisroel': pas_yisroel_count
            }), 200
        else:
            logger.error("ORB scraper failed")
            return jsonify({
                'error': 'ORB scraper failed',
                'message': 'Failed to scrape ORB data - check logs for details'
            }), 500
        
    except Exception as e:
        logger.error(f"Error updating database: {e}")
        return jsonify({
            'error': 'Failed to update database',
            'message': str(e)
        }), 500

@app.route('/api/admin/update-hours', methods=['POST'])
def update_restaurant_hours():
    """Update restaurant hours using Google Places API."""
    try:
        data = request.get_json()
        restaurant_id = data.get('id')
        place_id = data.get('placeId')
        
        if not restaurant_id or not place_id:
            return jsonify({'error': 'Missing restaurant ID or place ID'}), 400
        
        # Get the restaurant from database
        db = EnhancedDatabaseManager()
        if not db.connect():
            return jsonify({'error': 'Database connection failed'}), 500
        
        session = db.get_session()
        restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        
        if not restaurant:
            return jsonify({'error': 'Restaurant not found'}), 404
        
        # Fetch hours from Google Places API
        google_api_key = os.environ.get('GOOGLE_API_KEY')
        if not google_api_key:
            return jsonify({'error': 'Google Places API key not configured'}), 500
        
        # Make request to Google Places API
        url = f"https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'place_id': place_id,
            'fields': 'opening_hours,utc_offset_minutes',
            'key': google_api_key
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get('status') != 'OK':
            return jsonify({'error': f'Google Places API error: {data.get("status")}'}), 400
        
        result = data.get('result', {})
        opening_hours = result.get('opening_hours', {})
        
        # Extract hours data
        periods = opening_hours.get('periods', [])
        weekday_text = opening_hours.get('weekday_text', [])
        utc_offset = result.get('utc_offset_minutes', 0)
        
        # Convert UTC offset to timezone
        timezone = offset_to_timezone(utc_offset)
        
        # Update restaurant hours
        restaurant.hours_of_operation = '\n'.join(weekday_text)
        restaurant.hours_json = json.dumps(periods)
        restaurant.hours_last_updated = datetime.utcnow()
        restaurant.timezone = timezone
        restaurant.hours_parsed = True
        
        session.commit()
        session.close()
        
        return jsonify({
            'success': True,
            'message': 'Hours updated successfully',
            'restaurant_id': restaurant_id,
            'hours_updated': True,
            'timezone': timezone
        })
        
    except Exception as e:
        logger.error(f"Error updating restaurant hours: {e}")
        return jsonify({'error': str(e)}), 500

def offset_to_timezone(offset_minutes):
    """Convert UTC offset to timezone name."""
    # Simple mapping for common US timezones
    offset_hours = offset_minutes / 60
    if offset_hours == -5:
        return 'America/New_York'
    elif offset_hours == -6:
        return 'America/Chicago'
    elif offset_hours == -7:
        return 'America/Denver'
    elif offset_hours == -8:
        return 'America/Los_Angeles'
    else:
        return 'UTC'

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
        
        # Determine if we're in production
        is_production = os.environ.get('ENVIRONMENT') == 'production' or os.environ.get('RENDER') == 'true'
        
        app.run(
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000)),
            debug=not is_production
        )
    else:
        logger.error("Failed to initialize database. Exiting.")
        exit(1) # Force redeploy - Thu Jul 31 19:36:41 AST 2025
