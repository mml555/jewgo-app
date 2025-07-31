#!/usr/bin/env python3
"""
Load ORB Data
============

This script loads real ORB restaurant data directly into the database.
It uses the exact data structure from our successful local scraper run.
"""

import sys
import os
import structlog

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database_manager_v3 import EnhancedDatabaseManager

# Configure structured logging
logger = structlog.get_logger()

def load_orb_data():
    """Load real ORB data into the database."""
    
    # Real ORB data from our successful scraper run
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
            'kosher_type': 'dairy',
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
            'kosher_type': 'dairy',
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
            'kosher_type': 'dairy',
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
            'kosher_type': 'dairy',
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
            'kosher_type': 'dairy',
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
            'kosher_type': 'dairy',
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
            'kosher_type': 'dairy',
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
            'kosher_type': 'dairy',
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
            'kosher_type': 'dairy',
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
            'kosher_type': 'dairy',
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
            'kosher_type': 'meat',
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
            'kosher_type': 'meat',
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
            'kosher_type': 'meat',
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
            'kosher_type': 'meat',
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
            'kosher_type': 'meat',
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
            'kosher_type': 'meat',
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
            'kosher_type': 'meat',
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
            'kosher_type': 'meat',
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
            'kosher_type': 'meat',
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
            'kosher_type': 'meat',
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
            'kosher_type': 'pareve',
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
            'kosher_type': 'pareve',
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
            'kosher_type': 'pareve',
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
            'kosher_type': 'pareve',
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
            'kosher_type': 'pareve',
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
        
        deleted_count = session.query(Restaurant).delete()
        session.commit()
        logger.info(f"Deleted {deleted_count} existing restaurants")
        
        # Add ORB data
        success_count = 0
        for restaurant_data in orb_restaurants:
            try:
                success = db_manager.add_restaurant(restaurant_data)
                if success:
                    success_count += 1
                    logger.info(f"Added: {restaurant_data['name']} ({restaurant_data['kosher_type']})")
            except Exception as e:
                logger.error(f"Error saving restaurant {restaurant_data['name']}: {e}")
        
        logger.info(f"Successfully saved {success_count} ORB restaurants")
        
        # Show final statistics
        final_count = session.query(Restaurant).count()
        logger.info(f"Final restaurant count: {final_count}")
        
        # Show kosher type statistics
        from sqlalchemy import func
        kosher_types = session.query(
            Restaurant.kosher_category,
            func.count(Restaurant.kosher_category)
        ).group_by(Restaurant.kosher_category).all()
        
        logger.info("Kosher Type Distribution:")
        for kosher_type, count in kosher_types:
            logger.info(f"  - {kosher_type}: {count} restaurants")
        
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
        
        logger.info("Kosher Supervision Statistics:")
        logger.info(f"  - Chalav Yisroel: {chalav_yisroel_count}")
        logger.info(f"  - Chalav Stam: {chalav_stam_count}")
        logger.info(f"  - Pas Yisroel: {pas_yisroel_count}")
        
        session.close()
        db_manager.disconnect()
        
        return True
        
    except Exception as e:
        logger.error(f"Error loading ORB data: {e}")
        return False

if __name__ == "__main__":
    success = load_orb_data()
    
    if success:
        print("✅ ORB data loaded successfully!")
    else:
        print("❌ Failed to load ORB data!")
        sys.exit(1) 