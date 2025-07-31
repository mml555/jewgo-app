#!/usr/bin/env python3
"""
Simple Database Update Script
============================

A simplified version of the database update that works better on Render.
This script uses synchronous requests instead of async Playwright.

Author: JewGo Development Team
Version: 1.0
Last Updated: 2024
"""

import sys
import os
import requests
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database_manager_v3 import EnhancedDatabaseManager
import structlog

# Configure structured logging
logger = structlog.get_logger()

def update_database_simple():
    """Update database with a simple approach."""
    try:
        logger.info("Starting simple database update")
        
        # Initialize database manager
        db_manager = EnhancedDatabaseManager()
        
        if not db_manager.connect():
            logger.error("Failed to connect to database")
            return False
        
        session = db_manager.get_session()
        from database.database_manager_v3 import Restaurant
        
        # Step 1: Clear all existing restaurant data
        logger.info("Clearing all existing restaurant data...")
        deleted_count = session.query(Restaurant).delete()
        session.commit()
        logger.info(f"Deleted {deleted_count} existing restaurants")
        
        # Step 2: Add sample data with correct categorization
        # This is a simplified approach - in production, you'd want to use the scraper
        sample_restaurants = [
            {
                'name': 'Sample Dairy Restaurant 1',
                'address': '123 Dairy St, Miami, FL',
                'phone': '(305) 555-0101',
                'website': 'https://example.com',
                'kosher_type': 'dairy',
                'is_cholov_yisroel': True,
                'is_pas_yisroel': False,
                'certifying_agency': 'ORB',
                'short_description': 'Sample dairy restaurant'
            },
            {
                'name': 'Sample Meat Restaurant 1',
                'address': '456 Meat Ave, Miami, FL',
                'phone': '(305) 555-0202',
                'website': 'https://example.com',
                'kosher_type': 'meat',
                'is_cholov_yisroel': False,
                'is_pas_yisroel': False,
                'certifying_agency': 'ORB',
                'short_description': 'Sample meat restaurant'
            },
            {
                'name': 'Sample Pareve Restaurant 1',
                'address': '789 Pareve Blvd, Miami, FL',
                'phone': '(305) 555-0303',
                'website': 'https://example.com',
                'kosher_type': 'pareve',
                'is_cholov_yisroel': False,
                'is_pas_yisroel': True,
                'certifying_agency': 'ORB',
                'short_description': 'Sample pareve restaurant'
            }
        ]
        
        # Step 3: Save sample data to database
        logger.info(f"Saving {len(sample_restaurants)} sample restaurants...")
        
        success_count = 0
        for restaurant_data in sample_restaurants:
            try:
                success = db_manager.add_restaurant(restaurant_data)
                if success:
                    success_count += 1
                    logger.info(f"Added: {restaurant_data['name']} ({restaurant_data['kosher_type']})")
            except Exception as e:
                logger.error(f"Error saving restaurant {restaurant_data['name']}: {e}")
        
        logger.info(f"Successfully saved {success_count} restaurants")
        
        # Step 4: Verify the data
        final_count = session.query(Restaurant).count()
        logger.info(f"Final restaurant count: {final_count}")
        
        # Show final statistics
        kosher_types = session.query(
            Restaurant.kosher_type,
            db_manager.db.func.count(Restaurant.kosher_type)
        ).group_by(Restaurant.kosher_type).all()
        
        logger.info("Final Kosher Type Distribution:")
        for kosher_type, count in kosher_types:
            logger.info(f"  - {kosher_type}: {count} restaurants")
        
        # Show Chalav Yisroel statistics
        chalav_yisroel_count = session.query(Restaurant).filter(
            Restaurant.is_cholov_yisroel == True
        ).count()
        
        chalav_stam_count = session.query(Restaurant).filter(
            Restaurant.is_cholov_yisroel == False,
            Restaurant.kosher_type == 'dairy'
        ).count()
        
        pas_yisroel_count = session.query(Restaurant).filter(
            Restaurant.is_pas_yisroel == True
        ).count()
        
        logger.info("Final Kosher Supervision Statistics:")
        logger.info(f"  - Chalav Yisroel: {chalav_yisroel_count}")
        logger.info(f"  - Chalav Stam: {chalav_stam_count}")
        logger.info(f"  - Pas Yisroel: {pas_yisroel_count}")
        
        session.close()
        db_manager.disconnect()
        
        return True
        
    except Exception as e:
        logger.error(f"Error in simple database update: {e}")
        return False

if __name__ == "__main__":
    success = update_database_simple()
    
    if success:
        print("\n✅ Simple database update completed successfully!")
        print("The database now contains sample data with correct kosher categorization.")
    else:
        print("\n❌ Simple database update failed!")
        sys.exit(1) 