#!/usr/bin/env python3
"""
Load ORB Restaurant Data into Database (Improved Version)
=======================================================

This script loads the scraped ORB restaurant data from the JSON file
into the database using the current schema with improved data validation
and error handling.

The script:
1. Reads the formatted_restaurants.json file
2. Validates and cleans the data before loading
3. Handles missing required fields with sensible defaults
4. Maps the data to our current database schema
5. Loads the restaurants into the database
6. Provides comprehensive statistics on the loaded data

Author: JewGo Development Team
Version: 2.0
"""

import json
import os
import sys
import re
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

def clean_phone_number(phone):
    """Clean and validate phone number."""
    if not phone:
        return None
    
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Check if it's a valid US phone number (10 or 11 digits)
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone  # Return original if can't format

def extract_zip_code(address):
    """Extract ZIP code from address if missing."""
    if not address:
        return None
    
    # Look for ZIP code pattern in address
    zip_match = re.search(r'\b\d{5}(?:-\d{4})?\b', address)
    if zip_match:
        return zip_match.group()
    return None

def extract_city_state(address):
    """Extract city and state from address if missing."""
    if not address:
        return None, None
    
    # Common Florida cities and their states
    florida_cities = {
        'Miami Beach': 'FL',
        'Miami': 'FL', 
        'Surfside': 'FL',
        'Hollywood': 'FL',
        'Boca Raton': 'FL',
        'Hallandale Beach': 'FL',
        'Aventura': 'FL',
        'North Miami Beach': 'FL',
        'Deerfield Beach': 'FL',
        'West Palm Beach': 'FL',
        'Fort Lauderdale': 'FL',
        'Pembroke Pines': 'FL',
        'Coral Springs': 'FL',
        'Plantation': 'FL',
        'Sunrise': 'FL',
        'Tamarac': 'FL',
        'Lauderhill': 'FL',
        'Margate': 'FL',
        'Coconut Creek': 'FL',
        'Pompano Beach': 'FL',
        'Boynton Beach': 'FL',
        'Delray Beach': 'FL',
        'Lake Worth': 'FL',
        'Wellington': 'FL',
        'Jupiter': 'FL',
        'Palm Beach Gardens': 'FL',
        'North Palm Beach': 'FL',
        'Palm Beach': 'FL',
        'Weston': 'FL',
        'Davie': 'FL',
        'Cooper City': 'FL',
        'Miramar': 'FL',
        'Hialeah': 'FL',
        'Hialeah Gardens': 'FL',
        'Miami Gardens': 'FL',
        'Opa-locka': 'FL',
        'North Miami': 'FL',
        'Miami Shores': 'FL',
        'Bal Harbour': 'FL',
        'Bay Harbor Islands': 'FL',
        'Key Biscayne': 'FL',
        'Coral Gables': 'FL',
        'South Miami': 'FL',
        'Kendall': 'FL',
        'Doral': 'FL',
        'Hialeah': 'FL',
    }
    
    # Try to find a city in the address
    for city, state in florida_cities.items():
        if city.lower() in address.lower():
            return city, state
    
    return None, None

def validate_and_clean_restaurant_data(restaurant_data):
    """Validate and clean restaurant data before loading."""
    cleaned_data = {}
    
    # Required fields with validation
    name = restaurant_data.get('name', '').strip()
    if not name:
        return None  # Skip restaurants without names
    cleaned_data['name'] = name
    
    # Address handling
    address = restaurant_data.get('address', '').strip()
    if not address:
        logger.warning(f"Missing address for restaurant: {name}")
        address = "Address not available"
    cleaned_data['address'] = address
    
    # City and state handling
    city = restaurant_data.get('city', '')
    if city:
        city = city.strip()
    state = restaurant_data.get('state', '')
    if state:
        state = state.strip()
    
    if not city or not state:
        extracted_city, extracted_state = extract_city_state(address)
        if not city and extracted_city:
            city = extracted_city
        if not state and extracted_state:
            state = extracted_state
    
    if not city:
        city = "Unknown City"
    if not state:
        state = "FL"  # Default to Florida
    
    cleaned_data['city'] = city
    cleaned_data['state'] = state
    
    # ZIP code handling
    zip_code = restaurant_data.get('zip_code', '')
    if zip_code:
        zip_code = zip_code.strip()
    if not zip_code:
        extracted_zip = extract_zip_code(address)
        if extracted_zip:
            zip_code = extracted_zip
        else:
            zip_code = "00000"  # Default ZIP code
    
    cleaned_data['zip_code'] = zip_code
    
    # Phone number handling
    phone_number = restaurant_data.get('phone_number', '')
    if phone_number:
        phone_number = phone_number.strip()
    if phone_number:
        phone_number = clean_phone_number(phone_number)
    else:
        phone_number = "(555) 000-0000"  # Default phone number
    
    cleaned_data['phone_number'] = phone_number
    
    # Optional fields
    website = restaurant_data.get('website', '')
    cleaned_data['website'] = website.strip() if website else None
    
    certifying_agency = restaurant_data.get('certifying_agency', 'KM')
    cleaned_data['certifying_agency'] = certifying_agency.strip() if certifying_agency else 'KM'
    
    kosher_category = restaurant_data.get('kosher_category', 'pareve')
    cleaned_data['kosher_category'] = kosher_category.strip() if kosher_category else 'pareve'
    
    listing_type = restaurant_data.get('listing_type', 'restaurant')
    cleaned_data['listing_type'] = listing_type.strip() if listing_type else 'restaurant'
    
    price_range = restaurant_data.get('price_range', '')
    cleaned_data['price_range'] = price_range.strip() if price_range else None
    
    hours_of_operation = restaurant_data.get('hours_open', '')
    cleaned_data['hours_of_operation'] = hours_of_operation.strip() if hours_of_operation else None
    
    # Coordinates
    cleaned_data['latitude'] = restaurant_data.get('latitude')
    cleaned_data['longitude'] = restaurant_data.get('longitude')
    
    # Additional fields
    cleaned_data['short_description'] = f"Kosher {cleaned_data['kosher_category']} certified by {cleaned_data['certifying_agency']}"
    cleaned_data['image_url'] = None
    cleaned_data['specials'] = '[]'
    cleaned_data['hours_parsed'] = False
    cleaned_data['timezone'] = 'America/New_York'
    
    # Set kosher supervision flags based on category
    if cleaned_data['kosher_category'] == 'dairy':
        cleaned_data['is_cholov_yisroel'] = True
        cleaned_data['is_pas_yisroel'] = None
    elif cleaned_data['kosher_category'] in ['meat', 'pareve']:
        cleaned_data['is_cholov_yisroel'] = None
        cleaned_data['is_pas_yisroel'] = False
    else:
        cleaned_data['is_cholov_yisroel'] = None
        cleaned_data['is_pas_yisroel'] = None
    
    return cleaned_data

def load_orb_restaurants_improved():
    """Load ORB restaurant data from JSON file into database with improved validation."""
    
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
        
        # Clear existing data
        session = db_manager.get_session()
        deleted_count = session.query(Restaurant).delete()
        session.commit()
        logger.info(f"Cleared {deleted_count} existing restaurants")
        
        # Load restaurants with validation
        success_count = 0
        error_count = 0
        skipped_count = 0
        validation_stats = {
            'missing_address': 0,
            'missing_phone': 0,
            'missing_city': 0,
            'missing_state': 0,
            'missing_zip': 0,
            'extracted_zip': 0,
            'extracted_city_state': 0
        }
        
        for i, restaurant_data in enumerate(restaurants, 1):
            try:
                # Validate and clean the data
                cleaned_data = validate_and_clean_restaurant_data(restaurant_data)
                
                if cleaned_data is None:
                    skipped_count += 1
                    continue
                
                # Track validation statistics
                original_data = restaurant_data
                if not original_data.get('address'):
                    validation_stats['missing_address'] += 1
                if not original_data.get('phone_number'):
                    validation_stats['missing_phone'] += 1
                if not original_data.get('city'):
                    validation_stats['missing_city'] += 1
                if not original_data.get('state'):
                    validation_stats['missing_state'] += 1
                if not original_data.get('zip_code'):
                    validation_stats['missing_zip'] += 1
                    if extract_zip_code(original_data.get('address', '')):
                        validation_stats['extracted_zip'] += 1
                if (not original_data.get('city') or not original_data.get('state')) and extract_city_state(original_data.get('address', ''))[0]:
                    validation_stats['extracted_city_state'] += 1
                
                # Add restaurant to database
                success = db_manager.add_restaurant(cleaned_data)
                if success:
                    success_count += 1
                    if success_count % 25 == 0:
                        logger.info(f"Loaded {success_count} restaurants...")
                else:
                    error_count += 1
                    logger.error(f"Failed to load restaurant: {cleaned_data.get('name', 'Unknown')}")
                    
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
        
        # Get certifying agency distribution
        agencies = session.query(
            Restaurant.certifying_agency,
            func.count(Restaurant.certifying_agency)
        ).group_by(Restaurant.certifying_agency).all()
        
        # Get city distribution (top 10)
        cities = session.query(
            Restaurant.city,
            func.count(Restaurant.city)
        ).group_by(Restaurant.city).order_by(func.count(Restaurant.city).desc()).limit(10).all()
        
        logger.info("=== LOADING COMPLETE ===")
        logger.info(f"Successfully loaded: {success_count} restaurants")
        logger.info(f"Errors: {error_count} restaurants")
        logger.info(f"Skipped: {skipped_count} restaurants")
        logger.info(f"Final database count: {final_count} restaurants")
        
        logger.info("Validation Statistics:")
        for stat, count in validation_stats.items():
            logger.info(f"  - {stat}: {count}")
        
        logger.info("Kosher Category Distribution:")
        for kosher_type, count in kosher_types:
            logger.info(f"  - {kosher_type}: {count} restaurants")
        
        logger.info("Certifying Agency Distribution:")
        for agency, count in agencies:
            logger.info(f"  - {agency}: {count} restaurants")
        
        logger.info("Top 10 Cities:")
        for city, count in cities:
            logger.info(f"  - {city}: {count} restaurants")
        
        session.close()
        db_manager.disconnect()
        
        return True
        
    except Exception as e:
        logger.error(f"Error loading ORB restaurants: {e}")
        return False

if __name__ == "__main__":
    success = load_orb_restaurants_improved()
    
    if success:
        print("✅ ORB restaurant data loaded successfully!")
    else:
        print("❌ Failed to load ORB restaurant data!")
        sys.exit(1) 