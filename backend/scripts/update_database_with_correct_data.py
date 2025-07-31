#!/usr/bin/env python3
"""
Update Database with Correct ORB Data
=====================================

This script clears all old restaurant data and populates the database
with the correct ORB data that properly differentiates between meat and dairy.

Author: JewGo Development Team
Version: 1.0
Last Updated: 2024
"""

import sys
import os
import asyncio
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database_manager_v3 import EnhancedDatabaseManager
from scrapers.orb_scraper_v2 import ORBScraperV2
import structlog

# Configure structured logging
logger = structlog.get_logger()

async def update_database():
    """Clear old data and populate with correct ORB data."""
    try:
        logger.info("Starting database update with correct ORB data")
        
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
        
        # Step 2: Run the updated ORB scraper
        logger.info("Running updated ORB scraper...")
        scraper = ORBScraperV2()
        
        if not await scraper.setup_playwright():
            logger.error("Failed to setup Playwright")
            return False
        
        # Scrape all categories
        businesses = await scraper.scrape_all_categories()
        
        if businesses:
            # Step 3: Save new data to database
            logger.info(f"Saving {len(businesses)} businesses to database...")
            saved_count = scraper.save_businesses_to_database(businesses)
            
            logger.info(f"Successfully saved {saved_count} businesses")
            
            # Step 4: Verify the data
            final_count = session.query(Restaurant).count()
            logger.info(f"Final restaurant count: {final_count}")
            
            # Show final statistics
            kosher_types = session.query(
                Restaurant.kosher_type,
                db_manager.db.func.count(Restaurant.kosher_type)
            ).group_by(Restaurant.kosher_type).all()
            
            logger.info("Final Kosher Type Distribution:")
            for kosher_type, count in kosher_types.items():
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
            
        else:
            logger.error("No businesses were scraped")
            return False
        
        session.close()
        db_manager.disconnect()
        await scraper.cleanup()
        
        return True
        
    except Exception as e:
        logger.error(f"Error updating database: {e}")
        return False

async def main():
    """Main entry point."""
    success = await update_database()
    
    if success:
        print("\n✅ Database update completed successfully!")
        print("The database now contains the correct ORB data with proper meat/dairy categorization.")
    else:
        print("\n❌ Database update failed!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 