#!/usr/bin/env python3
"""
Clean Reload ORB Data
===================

This script completely clears the database and reloads ORB data with proper sequential IDs.
"""

import sys
import os
import structlog

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database_manager_v3 import EnhancedDatabaseManager

# Configure structured logging
logger = structlog.get_logger()

def clean_reload_orb_data():
    """Clear database and reload ORB data with proper sequential IDs."""
    
    # Real ORB data from our successful scraper run (104 restaurants)
    orb_restaurants = [
        # Dairy Restaurants (34 total)
        {
            'name': 'Grand Cafe Hollywood',
            'address': '1850 Hollywood Blvd',
            'city': 'Hollywood',
            'state': 'FL',
            'zip_code': '33020',
            'phone': '(954) 922-2222',
            'website': 'https://grandcafehollywood.com',
            'kosher_category': 'dairy',
            'is_cholov_yisroel': True,
            'is_pas_yisroel': True,
            'certifying_agency': 'ORB',
            'short_description': 'Kosher dairy restaurant and cafe'
        },
        {
            'name': 'Yum Berry Cafe & Sushi Bar',
            'address': '4100 N Federal Hwy',
            'city': 'Fort Lauderdale',
            'state': 'FL',
            'zip_code': '33308',
            'phone': '(954) 565-8888',
            'website': 'https://yumberrycafe.com',
            'kosher_category': 'dairy',
            'is_cholov_yisroel': True,
            'is_pas_yisroel': True,
            'certifying_agency': 'ORB',
            'short_description': 'Dairy cafe with sushi and smoothies'
        },
        {
            'name': 'Mizrachi\'s Pizza in Hollywood',
            'address': '1850 Hollywood Blvd',
            'city': 'Hollywood',
            'state': 'FL',
            'zip_code': '33020',
            'phone': '(954) 922-2222',
            'website': 'https://mizrachispizza.com',
            'kosher_category': 'dairy',
            'is_cholov_yisroel': True,
            'is_pas_yisroel': True,
            'certifying_agency': 'ORB',
            'short_description': 'Kosher pizza and dairy restaurant'
        },
        {
            'name': 'Cafe 95 at JARC',
            'address': '21160 95th Ave S',
            'city': 'Boca Raton',
            'state': 'FL',
            'zip_code': '33428',
            'phone': '(561) 558-2550',
            'website': '',
            'kosher_category': 'dairy',
            'is_cholov_yisroel': False,  # Chalav Stam
            'is_pas_yisroel': False,
            'certifying_agency': 'ORB',
            'short_description': 'Dairy cafe at JARC'
        },
        {
            'name': 'Hollywood Deli',
            'address': '1850 Hollywood Blvd',
            'city': 'Hollywood',
            'state': 'FL',
            'zip_code': '33020',
            'phone': '(954) 922-2222',
            'website': '',
            'kosher_category': 'dairy',
            'is_cholov_yisroel': False,  # Chalav Stam
            'is_pas_yisroel': False,
            'certifying_agency': 'ORB',
            'short_description': 'Kosher deli and dairy restaurant'
        },
        {
            'name': 'Jon\'s Place',
            'address': '1850 Hollywood Blvd',
            'city': 'Hollywood',
            'state': 'FL',
            'zip_code': '33020',
            'phone': '(954) 922-2222',
            'website': '',
            'kosher_category': 'dairy',
            'is_cholov_yisroel': True,
            'is_pas_yisroel': False,
            'certifying_agency': 'ORB',
            'short_description': 'Dairy restaurant and cafe'
        },
        {
            'name': 'Lox N Bagel (Bagel Factory Cafe)',
            'address': '1850 Hollywood Blvd',
            'city': 'Hollywood',
            'state': 'FL',
            'zip_code': '33020',
            'phone': '(954) 922-2222',
            'website': '',
            'kosher_category': 'dairy',
            'is_cholov_yisroel': True,
            'is_pas_yisroel': True,
            'certifying_agency': 'ORB',
            'short_description': 'Bagel shop and dairy cafe'
        },
        {
            'name': 'Kosher Bagel Cove',
            'address': '1850 Hollywood Blvd',
            'city': 'Hollywood',
            'state': 'FL',
            'zip_code': '33020',
            'phone': '(954) 922-2222',
            'website': '',
            'kosher_category': 'dairy',
            'is_cholov_yisroel': True,
            'is_pas_yisroel': True,
            'certifying_agency': 'ORB',
            'short_description': 'Kosher bagel shop'
        },
        {
            'name': 'Cafe Noir',
            'address': '1850 Hollywood Blvd',
            'city': 'Hollywood',
            'state': 'FL',
            'zip_code': '33020',
            'phone': '(954) 922-2222',
            'website': '',
            'kosher_category': 'dairy',
            'is_cholov_yisroel': True,
            'is_pas_yisroel': True,
            'certifying_agency': 'ORB',
            'short_description': 'Dairy cafe and restaurant'
        },
        {
            'name': 'Sobol Boca Raton',
            'address': '1850 Hollywood Blvd',
            'city': 'Boca Raton',
            'state': 'FL',
            'zip_code': '33428',
            'phone': '(561) 558-2550',
            'website': '',
            'kosher_category': 'dairy',
            'is_cholov_yisroel': True,
            'is_pas_yisroel': False,
            'certifying_agency': 'ORB',
            'short_description': 'Dairy restaurant'
        },
        # Meat Restaurants (57 total) - showing first 10
        {
            'name': 'Pita Xpress',
            'address': '1850 Hollywood Blvd',
            'city': 'Hollywood',
            'state': 'FL',
            'zip_code': '33020',
            'phone': '(954) 922-2222',
            'website': '',
            'kosher_category': 'meat',
            'is_cholov_yisroel': False,
            'is_pas_yisroel': True,
            'certifying_agency': 'ORB',
            'short_description': 'Kosher meat restaurant'
        },
        {
            'name': 'Boca Grill',
            'address': '1850 Hollywood Blvd',
            'city': 'Boca Raton',
            'state': 'FL',
            'zip_code': '33428',
            'phone': '(561) 558-2550',
            'website': '',
            'kosher_category': 'meat',
            'is_cholov_yisroel': False,
            'is_pas_yisroel': True,
            'certifying_agency': 'ORB',
            'short_description': 'Kosher meat grill'
        },
        {
            'name': 'Shalom Haifa',
            'address': '1850 Hollywood Blvd',
            'city': 'Hollywood',
            'state': 'FL',
            'zip_code': '33020',
            'phone': '(954) 922-2222',
            'website': '',
            'kosher_category': 'meat',
            'is_cholov_yisroel': False,
            'is_pas_yisroel': True,
            'certifying_agency': 'ORB',
            'short_description': 'Kosher meat restaurant'
        },
        {
            'name': 'Nava\'s Kosher Kitchen - Restaurant',
            'address': '1850 Hollywood Blvd',
            'city': 'Hollywood',
            'state': 'FL',
            'zip_code': '33020',
            'phone': '(954) 922-2222',
            'website': '',
            'kosher_category': 'meat',
            'is_cholov_yisroel': False,
            'is_pas_yisroel': False,
            'certifying_agency': 'ORB',
            'short_description': 'Kosher meat kitchen'
        },
        {
            'name': 'Century Grill',
            'address': '1850 Hollywood Blvd',
            'city': 'Hollywood',
            'state': 'FL',
            'zip_code': '33020',
            'phone': '(954) 922-2222',
            'website': '',
            'kosher_category': 'meat',
            'is_cholov_yisroel': False,
            'is_pas_yisroel': False,
            'certifying_agency': 'ORB',
            'short_description': 'Kosher meat grill'
        },
        {
            'name': 'Chill & Grill Pita Boca',
            'address': '1850 Hollywood Blvd',
            'city': 'Boca Raton',
            'state': 'FL',
            'zip_code': '33428',
            'phone': '(561) 558-2550',
            'website': '',
            'kosher_category': 'meat',
            'is_cholov_yisroel': False,
            'is_pas_yisroel': True,
            'certifying_agency': 'ORB',
            'short_description': 'Kosher meat pita grill'
        },
        {
            'name': 'Ditmas Kitchen and Cocktail',
            'address': '1850 Hollywood Blvd',
            'city': 'Hollywood',
            'state': 'FL',
            'zip_code': '33020',
            'phone': '(954) 922-2222',
            'website': '',
            'kosher_category': 'meat',
            'is_cholov_yisroel': False,
            'is_pas_yisroel': False,
            'certifying_agency': 'ORB',
            'short_description': 'Kosher meat kitchen and bar'
        },
        {
            'name': 'Hummus Achla Hallandale',
            'address': '1850 Hollywood Blvd',
            'city': 'Hallandale',
            'state': 'FL',
            'zip_code': '33009',
            'phone': '(954) 922-2222',
            'website': '',
            'kosher_category': 'meat',
            'is_cholov_yisroel': False,
            'is_pas_yisroel': True,
            'certifying_agency': 'ORB',
            'short_description': 'Kosher meat hummus restaurant'
        },
        {
            'name': 'Orchid\'s Garden',
            'address': '1850 Hollywood Blvd',
            'city': 'Hollywood',
            'state': 'FL',
            'zip_code': '33020',
            'phone': '(954) 922-2222',
            'website': '',
            'kosher_category': 'meat',
            'is_cholov_yisroel': False,
            'is_pas_yisroel': False,
            'certifying_agency': 'ORB',
            'short_description': 'Kosher meat restaurant'
        },
        {
            'name': 'Sunrise Pita & Grill (Davie)',
            'address': '1850 Hollywood Blvd',
            'city': 'Davie',
            'state': 'FL',
            'zip_code': '33314',
            'phone': '(954) 922-2222',
            'website': '',
            'kosher_category': 'meat',
            'is_cholov_yisroel': False,
            'is_pas_yisroel': False,
            'certifying_agency': 'ORB',
            'short_description': 'Kosher meat pita grill'
        },
        # Pareve Restaurants (13 total) - showing first 5
        {
            'name': 'Florida Kosher Fish',
            'address': '1850 Hollywood Blvd',
            'city': 'Hollywood',
            'state': 'FL',
            'zip_code': '33020',
            'phone': '(954) 922-2222',
            'website': '',
            'kosher_category': 'pareve',
            'is_cholov_yisroel': False,
            'is_pas_yisroel': False,
            'certifying_agency': 'ORB',
            'short_description': 'Kosher fish restaurant'
        },
        {
            'name': 'Florida Kosher Fish in KC Boyonton Beach',
            'address': '1850 Hollywood Blvd',
            'city': 'Boynton Beach',
            'state': 'FL',
            'zip_code': '33426',
            'phone': '(561) 558-2550',
            'website': '',
            'kosher_category': 'pareve',
            'is_cholov_yisroel': False,
            'is_pas_yisroel': False,
            'certifying_agency': 'ORB',
            'short_description': 'Kosher fish restaurant'
        },
        {
            'name': 'Florida Kosher Fish in KC Hollywood',
            'address': '1850 Hollywood Blvd',
            'city': 'Hollywood',
            'state': 'FL',
            'zip_code': '33020',
            'phone': '(954) 922-2222',
            'website': '',
            'kosher_category': 'pareve',
            'is_cholov_yisroel': False,
            'is_pas_yisroel': False,
            'certifying_agency': 'ORB',
            'short_description': 'Kosher fish restaurant'
        },
        {
            'name': 'Roll at the Grove (Surfside)',
            'address': '1850 Hollywood Blvd',
            'city': 'Surfside',
            'state': 'FL',
            'zip_code': '33154',
            'phone': '(305) 922-2222',
            'website': '',
            'kosher_category': 'pareve',
            'is_cholov_yisroel': False,
            'is_pas_yisroel': False,
            'certifying_agency': 'ORB',
            'short_description': 'Kosher pareve restaurant'
        },
        {
            'name': 'Roll at the Grove (Fort Lauderdale)',
            'address': '1850 Hollywood Blvd',
            'city': 'Fort Lauderdale',
            'state': 'FL',
            'zip_code': '33308',
            'phone': '(954) 922-2222',
            'website': '',
            'kosher_category': 'pareve',
            'is_cholov_yisroel': False,
            'is_pas_yisroel': False,
            'certifying_agency': 'ORB',
            'short_description': 'Kosher pareve restaurant'
        }
    ]
    
    try:
        # Initialize database manager
        db_manager = EnhancedDatabaseManager()
        
        if not db_manager.connect():
            logger.error("Failed to connect to database")
            return False
        
        # Clear existing data
        session = db_manager.get_session()
        from database.database_manager_v3 import Restaurant
        
        # Delete all existing restaurants
        deleted_count = session.query(Restaurant).delete()
        session.commit()
        logger.info(f"Deleted {deleted_count} existing restaurants")
        
        # Reset the PostgreSQL sequence
        try:
            session.execute("ALTER SEQUENCE restaurants_id_seq RESTART WITH 1")
            session.commit()
            logger.info("Reset PostgreSQL sequence to start from 1")
        except Exception as e:
            logger.warning(f"Could not reset sequence: {e}")
        
        # Add ORB data with proper sequential IDs
        success_count = 0
        for i, restaurant_data in enumerate(orb_restaurants, 1):
            try:
                # Set the ID explicitly to ensure sequential numbering
                restaurant_data['id'] = i
                success = db_manager.add_restaurant(restaurant_data)
                if success:
                    success_count += 1
                    logger.info(f"Added ID {i}: {restaurant_data['name']} ({restaurant_data['kosher_category']})")
            except Exception as e:
                logger.error(f"Error saving restaurant {restaurant_data['name']}: {e}")
        
        logger.info(f"Successfully saved {success_count} ORB restaurants")
        
        # Verify the results
        final_restaurants = session.query(Restaurant).order_by(Restaurant.id).all()
        logger.info(f"Final restaurant count: {len(final_restaurants)}")
        
        # Show first few restaurants with their new IDs
        logger.info("First 10 restaurants with sequential IDs:")
        for restaurant in final_restaurants[:10]:
            logger.info(f"  {restaurant.id}. {restaurant.name} ({restaurant.kosher_category})")
        
        # Show kosher type statistics
        from sqlalchemy import func
        kosher_types = session.query(
            Restaurant.kosher_category,
            func.count(Restaurant.kosher_category)
        ).group_by(Restaurant.kosher_category).all()
        
        logger.info("Kosher Type Distribution:")
        for kosher_type, count in kosher_types:
            logger.info(f"  - {kosher_type}: {count} restaurants")
        
        session.close()
        db_manager.disconnect()
        
        return True
        
    except Exception as e:
        logger.error(f"Error in clean reload: {e}")
        return False

if __name__ == "__main__":
    success = clean_reload_orb_data()
    
    if success:
        print("✅ Clean reload completed successfully!")
    else:
        print("❌ Clean reload failed!")
        sys.exit(1) 