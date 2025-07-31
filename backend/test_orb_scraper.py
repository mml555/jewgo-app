#!/usr/bin/env python3
"""
Test ORB Scraper
===============

Simple test script to debug ORB scraper issues.
"""

import asyncio
import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.orb_scraper_v2 import ORBScraperV2

async def test_scraper():
    """Test the ORB scraper."""
    print("Testing ORB Scraper...")
    
    try:
        scraper = ORBScraperV2()
        print("Scraper initialized successfully")
        
        # Test Playwright setup
        print("Testing Playwright setup...")
        success = await scraper.setup_playwright()
        if success:
            print("✅ Playwright setup successful")
        else:
            print("❌ Playwright setup failed")
            return False
        
        # Test scraping
        print("Testing scraping...")
        businesses = await scraper.scrape_all_categories()
        print(f"Scraped {len(businesses)} businesses")
        
        if businesses:
            print("Sample businesses:")
            for i, business in enumerate(businesses[:3]):
                print(f"  {i+1}. {business['name']} - {business.get('kosher_category', 'unknown')}")
        
        # Cleanup
        await scraper.cleanup()
        print("✅ Test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_scraper())
    sys.exit(0 if success else 1) 