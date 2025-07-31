#!/usr/bin/env python3
"""
Test script for ORB Kosher scraper
Tests the scraper functionality before running the full scrape.
"""

import os
import json
from orb_kosher_scraper import ORBKosherScraper

def test_scraper():
    """Test the scraper with a small sample."""
    try:
        scraper = ORBKosherScraper()
        
        print("Testing ORB Kosher scraper...")
        print("=" * 50)
        
        # Test scraping just the first few restaurants
        url = "https://www.orbkosher.com/category/restaurants/"
        
        print(f"Scraping from: {url}")
        
        # Get a small sample (first 3 restaurants)
        restaurants = scraper.scrape_orb_category(url, "Restaurant")
        
        if restaurants:
            print(f"\nSuccessfully scraped {len(restaurants)} restaurants")
            print("\nSample data:")
            print("-" * 30)
            
            for i, restaurant in enumerate(restaurants[:3], 1):
                print(f"\n{i}. {restaurant['name']}")
                print(f"   Address: {restaurant['address']}")
                print(f"   Phone: {restaurant['phone']}")
                print(f"   City: {restaurant['city']}")
                print(f"   State: {restaurant['state']}")
                print(f"   Kosher Type: {restaurant['cuisine_type']}")
                print(f"   Description: {restaurant['description'][:100]}...")
            
            # Save sample to JSON
            sample_filename = "orb_sample_restaurants.json"
            scraper.save_to_json(restaurants[:5], sample_filename)
            print(f"\nSample data saved to: {sample_filename}")
            
            # Test database insertion (just one restaurant)
            print("\nTesting database insertion...")
            test_restaurant = restaurants[0]
            success = scraper.db_manager.add_restaurant(test_restaurant)
            
            if success:
                print(f"✓ Successfully inserted test restaurant: {test_restaurant['name']}")
            else:
                print(f"✗ Failed to insert test restaurant: {test_restaurant['name']}")
        
        else:
            print("No restaurants found during test scrape")
        
    except Exception as e:
        print(f"Error during test: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        if 'scraper' in locals():
            scraper.close()

if __name__ == "__main__":
    test_scraper() 