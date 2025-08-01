#!/usr/bin/env python3
"""
Load ORB Restaurant Data into Database
=====================================

This script loads the scraped ORB restaurant data from the JSON file
into the database using the current schema.

The script:
1. Reads the formatted_restaurants.json file
2. Maps the data to our current database schema
3. Loads the restaurants into the database
4. Provides statistics on the loaded data

Author: JewGo Development Team
Version: 1.0
"""

import json
import os
import sys
from datetime import datetime
import structlog

# Configure logging
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
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database.database_manager_v3 import EnhancedDatabaseManager, Restaurant

def load_orb_restaurants():
    """Load ORB restaurant data from JSON file into database."""
    
    # Path to the JSON file
    json_file_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'data', 'exports', 'formatted_restaurants.json'
    )
    
    if not os.path.exists(json_file_path):
        logger.error(f"JSON file not found: {json_file_path}")
        return False
    
    try:
        # Load JSON data
        logger.info(f"Loading restaurant data from: {json_file_path}")
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        restaurants = data.get('restaurants', [])
        logger.info(f"Found {len(restaurants)} restaurants in JSON file")
        
        # Initialize database manager
        db_manager = EnhancedDatabaseManager()
        if not db_manager.connect():
            logger.error("Failed to connect to database")
            return False
        
        # Clear existing data (optional - comment out if you want to keep existing data)
        session = db_manager.get_session()
        deleted_count = session.query(Restaurant).delete()
        session.commit()
        logger.info(f"Cleared {deleted_count} existing restaurants")
        
        # Load restaurants
        success_count = 0
        error_count = 0
        
        for i, restaurant_data in enumerate(restaurants, 1):
            try:
                # Map JSON data to database schema
                mapped_data = {
                    'name': restaurant_data.get('name', ''),
                    'address': restaurant_data.get('address', ''),
                    'city': restaurant_data.get('city', ''),
                    'state': restaurant_data.get('state', ''),
                    'zip_code': restaurant_data.get('zip_code', ''),
                    'phone_number': restaurant_data.get('phone_number', ''),
                    'website': restaurant_data.get('website', ''),
                    'certifying_agency': restaurant_data.get('certifying_agency', 'KM'),
                    'kosher_category': restaurant_data.get('kosher_category', 'pareve'),
                    'listing_type': restaurant_data.get('listing_type', 'restaurant'),
                    'price_range': restaurant_data.get('price_range', ''),
                    'hours_of_operation': restaurant_data.get('hours_open', ''),
                    'latitude': restaurant_data.get('latitude'),
                    'longitude': restaurant_data.get('longitude'),
                    'short_description': f"Kosher {restaurant_data.get('kosher_category', 'restaurant')} certified by {restaurant_data.get('certifying_agency', 'KM')}",
                    'image_url': None,  # Will be populated later if needed
                    'specials': '[]',  # Empty JSON array as string
                    'hours_parsed': False,
                    'timezone': 'America/New_York',  # Default timezone for Florida
                    'is_cholov_yisroel': None,  # Will be determined based on kosher_category
                    'is_pas_yisroel': None,  # Will be determined based on kosher_category
                }
                
                # Set kosher supervision flags based on category
                if mapped_data['kosher_category'] == 'dairy':
                    mapped_data['is_cholov_yisroel'] = True  # Default to Chalav Yisroel
                elif mapped_data['kosher_category'] in ['meat', 'pareve']:
                    mapped_data['is_pas_yisroel'] = False  # Default to not Pas Yisroel
                
                # Add restaurant to database
                success = db_manager.add_restaurant(mapped_data)
                if success:
                    success_count += 1
                    if success_count % 50 == 0:
                        logger.info(f"Loaded {success_count} restaurants...")
                else:
                    error_count += 1
                    logger.error(f"Failed to load restaurant: {restaurant_data.get('name', 'Unknown')}")
                    
            except Exception as e:
                error_count += 1
                logger.error(f"Error loading restaurant {restaurant_data.get('name', 'Unknown')}: {e}")
                continue
        
        # Show final statistics
        final_count = session.query(Restaurant).count()
        
        # Get kosher category distribution
        from sqlalchemy import func
        kosher_types = session.query(
            Restaurant.kosher_category,
            func.count(Restaurant.kosher_category)
        ).group_by(Restaurant.kosher_category).all()
        
        logger.info("=== LOADING COMPLETE ===")
        logger.info(f"Successfully loaded: {success_count} restaurants")
        logger.info(f"Errors: {error_count} restaurants")
        logger.info(f"Final database count: {final_count} restaurants")
        
        logger.info("Kosher Category Distribution:")
        for kosher_type, count in kosher_types:
            logger.info(f"  - {kosher_type}: {count} restaurants")
        
        # Get certifying agency distribution
        agencies = session.query(
            Restaurant.certifying_agency,
            func.count(Restaurant.certifying_agency)
        ).group_by(Restaurant.certifying_agency).all()
        
        logger.info("Certifying Agency Distribution:")
        for agency, count in agencies:
            logger.info(f"  - {agency}: {count} restaurants")
        
        session.close()
        db_manager.disconnect()
        
        return True
        
    except Exception as e:
        logger.error(f"Error loading ORB restaurants: {e}")
        return False

if __name__ == "__main__":
    success = load_orb_restaurants()
    
    if success:
        print("✅ ORB restaurant data loaded successfully!")
    else:
        print("❌ Failed to load ORB restaurant data!")
        sys.exit(1) 