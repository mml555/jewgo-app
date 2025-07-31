#!/usr/bin/env python3
"""
Clean Database for ORB Data
Remove all existing restaurant data and ensure we only have current ORB listings.
"""

import os
import sys
import logging
from datetime import datetime

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database_manager_v3 import EnhancedDatabaseManager as DatabaseManager, Restaurant

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clean_database():
    """Clean the database and prepare for fresh ORB data."""
    
    # Initialize database manager
    db_manager = DatabaseManager()
    
    try:
        # Connect to database
        if not db_manager.connect():
            logger.error("Failed to connect to database")
            return False
        
        logger.info("Connected to database successfully")
        
        # Get current restaurant count
        session = db_manager.get_session()
        current_count = session.query(Restaurant).count()
        logger.info(f"Current restaurant count: {current_count}")
        
        # Delete all existing restaurants
        logger.info("Deleting all existing restaurants...")
        session.query(Restaurant).delete()
        session.commit()
        
        # Verify deletion
        new_count = session.query(Restaurant).count()
        logger.info(f"After deletion, restaurant count: {new_count}")
        
        if new_count == 0:
            logger.info("✅ Database cleaned successfully - all restaurants removed")
            return True
        else:
            logger.error(f"❌ Failed to clean database - still have {new_count} restaurants")
            return False
            
    except Exception as e:
        logger.error(f"Error cleaning database: {e}")
        return False
    finally:
        if 'session' in locals():
            session.close()
        db_manager.disconnect()

def verify_orb_data_only():
    """Verify that we only have ORB data after running the scraper."""
    
    # Initialize database manager
    db_manager = DatabaseManager()
    
    try:
        # Connect to database
        if not db_manager.connect():
            logger.error("Failed to connect to database")
            return False
        
        logger.info("Connected to database successfully")
        
        # Get all restaurants
        session = db_manager.get_session()
        restaurants = session.query(Restaurant).all()
        
        logger.info(f"Total restaurants in database: {len(restaurants)}")
        
        # Check for non-ORB data
        non_orb_count = 0
        orb_count = 0
        
        for restaurant in restaurants:
            # Check if it has ORB-specific fields
            if (restaurant.kosher_cert_link and 'orbkosher.com' in restaurant.kosher_cert_link) or \
               (restaurant.short_description and 'ORB' in restaurant.short_description):
                orb_count += 1
            else:
                non_orb_count += 1
                logger.warning(f"Non-ORB restaurant found: {restaurant.name}")
        
        logger.info(f"ORB restaurants: {orb_count}")
        logger.info(f"Non-ORB restaurants: {non_orb_count}")
        
        if non_orb_count == 0:
            logger.info("✅ Database contains only ORB data")
            return True
        else:
            logger.warning(f"⚠️  Database contains {non_orb_count} non-ORB restaurants")
            return False
            
    except Exception as e:
        logger.error(f"Error verifying data: {e}")
        return False
    finally:
        if 'session' in locals():
            session.close()
        db_manager.disconnect()

def main():
    """Main function to clean database and verify ORB data."""
    
    logger.info("🧹 Starting database cleanup for ORB data...")
    
    # Step 1: Clean the database
    logger.info("Step 1: Cleaning database...")
    if not clean_database():
        logger.error("Failed to clean database")
        return False
    
    # Step 2: Run the ORB scraper to populate with fresh data
    logger.info("Step 2: Running ORB scraper to populate fresh data...")
    logger.info("Please run: python orb_scraper_v2.py")
    
    # Step 3: Verify the data
    logger.info("Step 3: Verifying ORB data...")
    if not verify_orb_data_only():
        logger.warning("Database verification shows non-ORB data")
    else:
        logger.info("✅ Database verification successful")
    
    logger.info("🎉 Database cleanup process completed!")
    logger.info("Next step: Run 'python orb_scraper_v2.py' to populate with fresh ORB data")

if __name__ == "__main__":
    main() 