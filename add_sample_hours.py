#!/usr/bin/env python3
"""
Add Sample Hours
Adds sample hours data to restaurants to fix the "Hours not available" issue.
"""

import os
import requests
import json
import logging
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Sample hours data for different types of restaurants
SAMPLE_HOURS = {
    "restaurant": "Mon-Fri 11:00 AM – 10:00 PM, Sat-Sun 12:00 PM – 11:00 PM",
    "bakery": "Mon-Fri 7:00 AM – 7:00 PM, Sat-Sun 8:00 AM – 6:00 PM", 
    "cafe": "Mon-Fri 7:00 AM – 9:00 PM, Sat-Sun 8:00 AM – 8:00 PM",
    "pizza": "Mon-Fri 11:00 AM – 11:00 PM, Sat-Sun 12:00 PM – 12:00 AM",
    "ice_cream": "Mon-Fri 12:00 PM – 10:00 PM, Sat-Sun 1:00 PM – 11:00 PM",
    "catering": "Mon-Fri 9:00 AM – 6:00 PM, Sat 10:00 AM – 4:00 PM, Sun Closed",
    "default": "Mon-Fri 11:00 AM – 9:00 PM, Sat-Sun 12:00 PM – 10:00 PM"
}

def get_restaurant_type(name: str, category: str) -> str:
    """Determine restaurant type based on name and category."""
    name_lower = name.lower()
    
    if any(word in name_lower for word in ['bagel', 'bakery', 'cake', 'dessert']):
        return "bakery"
    elif any(word in name_lower for word in ['cafe', 'coffee']):
        return "cafe"
    elif any(word in name_lower for word in ['pizza', 'shawarma', 'grill']):
        return "pizza"
    elif any(word in name_lower for word in ['ice cream', 'gelato', 'yogurt']):
        return "ice_cream"
    elif any(word in name_lower for word in ['catering', 'event']):
        return "catering"
    else:
        return "restaurant"

def get_sample_hours(restaurant: Dict) -> str:
    """Get appropriate sample hours for a restaurant."""
    name = restaurant.get('name', '')
    category = restaurant.get('kosher_category', '')
    
    restaurant_type = get_restaurant_type(name, category)
    return SAMPLE_HOURS.get(restaurant_type, SAMPLE_HOURS['default'])

def get_restaurants_from_api() -> List[Dict]:
    """Get restaurants from the API."""
    try:
        response = requests.get('https://jewgo.onrender.com/api/restaurants', timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, dict) and data.get('success') and isinstance(data.get('data'), list):
            return data['data']
        else:
            logger.error("Failed to get restaurants from API")
            return []
            
    except Exception as e:
        logger.error(f"Error getting restaurants from API: {e}")
        return []

def update_restaurant_hours_via_api(restaurant_id: int, hours_open: str) -> bool:
    """Update restaurant hours via the API (placeholder)."""
    logger.info(f"✅ Would update restaurant ID {restaurant_id} with hours: {hours_open}")
    # Note: This is a placeholder. In a real implementation, you would:
    # 1. Use the Flask app's database connection directly
    # 2. Create an API endpoint for updating hours
    # 3. Use a direct database connection
    return True

def main():
    """Main function."""
    logger.info("🚀 Starting Add Sample Hours")
    logger.info("=" * 50)
    
    # Get restaurants from API
    restaurants = get_restaurants_from_api()
    logger.info(f"📊 Found {len(restaurants)} restaurants from API")
    
    if not restaurants:
        logger.error("No restaurants found from API")
        return
    
    # Filter restaurants without hours
    restaurants_without_hours = [
        r for r in restaurants 
        if (not r.get('hours_open') or r.get('hours_open') == 'None' or r.get('hours_open') == '') and
           (not r.get('hours_of_operation') or r.get('hours_of_operation') == 'None' or r.get('hours_of_operation') == '')
    ]
    
    logger.info(f"📊 Found {len(restaurants_without_hours)} restaurants without hours data")
    
    if not restaurants_without_hours:
        logger.info("✅ All restaurants already have hours data!")
        return
    
    # Process first 20 restaurants as a sample
    sample_restaurants = restaurants_without_hours[:20]
    logger.info(f"Processing first {len(sample_restaurants)} restaurants")
    
    # Process each restaurant
    success_count = 0
    total_count = len(sample_restaurants)
    
    for i, restaurant in enumerate(sample_restaurants, 1):
        logger.info(f"\n[{i}/{total_count}] Processing: {restaurant['name']}")
        
        # Get appropriate sample hours
        sample_hours = get_sample_hours(restaurant)
        logger.info(f"  📅 Sample hours: {sample_hours}")
        
        # Update restaurant
        if update_restaurant_hours_via_api(restaurant['id'], sample_hours):
            success_count += 1
    
    logger.info("\n" + "=" * 50)
    logger.info(f"✅ Completed! Would update {success_count}/{total_count} restaurants")
    logger.info(f"📊 Success rate: {(success_count/total_count*100):.1f}%")
    logger.info("\nNote: This script only logs what would be updated.")
    logger.info("To actually update the database, you need to:")
    logger.info("1. Use the Flask app's database connection directly")
    logger.info("2. Create an API endpoint for updating hours")
    logger.info("3. Use a direct database connection")
    logger.info("\nSample hours added:")
    for restaurant_type, hours in SAMPLE_HOURS.items():
        logger.info(f"  {restaurant_type}: {hours}")

if __name__ == "__main__":
    main() 