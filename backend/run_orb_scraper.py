#!/usr/bin/env python3
"""
Standalone ORB Scraper Runner
============================

This script runs the ORB scraper and saves the data to the database.
It can be called from the Flask endpoint or run independently.
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

async def run_orb_scraper():
    """Run the ORB scraper and return success status."""
    try:
        logger.info("Starting ORB scraper...")
        
        scraper = ORBScraperV2()
        success = await scraper.run()
        
        if success:
            logger.info("ORB scraper completed successfully")
            return True
        else:
            logger.error("ORB scraper failed")
            return False
            
    except Exception as e:
        logger.error(f"Error running ORB scraper: {e}")
        return False

def main():
    """Main entry point."""
    success = asyncio.run(run_orb_scraper())
    
    if success:
        print("✅ ORB scraper completed successfully")
        sys.exit(0)
    else:
        print("❌ ORB scraper failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 