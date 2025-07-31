#!/usr/bin/env python3
"""
Load Complete ORB Data
=====================

This script runs the ORB scraper and saves all 104 restaurants to the database.
"""

import asyncio
import sys
import os
import structlog

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.orb_scraper_v2 import ORBScraperV2

# Configure structured logging
logger = structlog.get_logger()

async def load_complete_orb_data():
    """Run the ORB scraper and save all data to database."""
    try:
        logger.info("Starting complete ORB data loading...")
        
        scraper = ORBScraperV2()
        success = await scraper.run()
        
        if success:
            logger.info("Complete ORB data loading successful")
            return True
        else:
            logger.error("Complete ORB data loading failed")
            return False
            
    except Exception as e:
        logger.error(f"Error loading complete ORB data: {e}")
        return False

def main():
    """Main entry point."""
    success = asyncio.run(load_complete_orb_data())
    
    if success:
        print("✅ Complete ORB data loaded successfully!")
    else:
        print("❌ Failed to load complete ORB data!")
        sys.exit(1)

if __name__ == "__main__":
    main() 