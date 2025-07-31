#!/usr/bin/env python3
"""
Assign Sample Hours to Restaurants
This script assigns reasonable sample hours to restaurants based on their type
and updates the database directly.
"""

import os
import sys
import requests
import structlog
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logger = structlog.get_logger()

# Sample hours templates based on restaurant type
HOURS_TEMPLATES = {
    "bakery": {
        "hours": "Monday: 7:00 AM – 7:00 PM\nTuesday: 7:00 AM – 7:00 PM\nWednesday: 7:00 AM – 7:00 PM\nThursday: 7:00 AM – 7:00 PM\nFriday: 7:00 AM – 3:00 PM\nSaturday: 8:00 AM – 10:00 PM\nSunday: 8:00 AM – 6:00 PM",
        "description": "Bakery hours - early opening for fresh bread"
    },
    "restaurant": {
        "hours": "Monday: 11:00 AM – 10:00 PM\nTuesday: 11:00 AM – 10:00 PM\nWednesday: 11:00 AM – 10:00 PM\nThursday: 11:00 AM – 10:00 PM\nFriday: 11:00 AM – 2:00 PM\nSaturday: 8:00 PM – 12:00 AM\nSunday: 11:00 AM – 9:00 PM",
        "description": "Standard restaurant hours"
    },
    "cafe": {
        "hours": "Monday: 7:00 AM – 8:00 PM\nTuesday: 7:00 AM – 8:00 PM\nWednesday: 7:00 AM – 8:00 PM\nThursday: 7:00 AM – 8:00 PM\nFriday: 7:00 AM – 3:00 PM\nSaturday: 8:00 AM – 10:00 PM\nSunday: 8:00 AM – 6:00 PM",
        "description": "Cafe hours - early opening for coffee"
    },
    "deli": {
        "hours": "Monday: 8:00 AM – 8:00 PM\nTuesday: 8:00 AM – 8:00 PM\nWednesday: 8:00 AM – 8:00 PM\nThursday: 8:00 AM – 8:00 PM\nFriday: 8:00 AM – 3:00 PM\nSaturday: 9:00 AM – 10:00 PM\nSunday: 9:00 AM – 7:00 PM",
        "description": "Deli hours"
    },
    "ice_cream": {
        "hours": "Monday: 12:00 PM – 10:00 PM\nTuesday: 12:00 PM – 10:00 PM\nWednesday: 12:00 PM – 10:00 PM\nThursday: 12:00 PM – 10:00 PM\nFriday: 12:00 PM – 11:00 PM\nSaturday: 12:00 PM – 11:00 PM\nSunday: 12:00 PM – 9:00 PM",
        "description": "Ice cream shop hours"
    },
    "catering": {
        "hours": "Monday: 9:00 AM – 6:00 PM\nTuesday: 9:00 AM – 6:00 PM\nWednesday: 9:00 AM – 6:00 PM\nThursday: 9:00 AM – 6:00 PM\nFriday: 9:00 AM – 3:00 PM\nSaturday: 10:00 AM – 4:00 PM\nSunday: Closed",
        "description": "Catering business hours"
    },
    "pizza": {
        "hours": "Monday: 11:00 AM – 11:00 PM\nTuesday: 11:00 AM – 11:00 PM\nWednesday: 11:00 AM – 11:00 PM\nThursday: 11:00 AM – 11:00 PM\nFriday: 11:00 AM – 2:00 PM\nSaturday: 8:00 PM – 12:00 AM\nSunday: 11:00 AM – 10:00 PM",
        "description": "Pizza restaurant hours"
    }
}

def get_restaurant_type(name: str, listing_type: str = None) -> str:
    """Determine restaurant type based on name and listing type."""
    name_lower = name.lower()
    
    # Check for specific keywords in the name
    if any(word in name_lower for word in ['bagel', 'bread', 'bakery', 'cake', 'dessert', 'sweet']):
        return "bakery"
    elif any(word in name_lower for word in ['cafe', 'coffee']):
        return "cafe"
    elif any(word in name_lower for word in ['deli', 'deli frozen']):
        return "deli"
    elif any(word in name_lower for word in ['ice cream', 'gelato', 'yogurt', 'frozen']):
        return "ice_cream"
    elif any(word in name_lower for word in ['catering', 'event']):
        return "catering"
    elif any(word in name_lower for word in ['pizza']):
        return "pizza"
    else:
        return "restaurant"

def get_restaurants_from_api() -> List[Dict]:
    """Fetch restaurants from the API."""
    try:
        url = "https://jewgo.onrender.com/api/restaurants"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            logger.error(f"Failed to fetch restaurants: {response.status_code}")
            return []
        
        data = response.json()
        logger.info(f"API response keys: {list(data.keys())}")
        
        if isinstance(data, dict) and data.get('success') and isinstance(data.get('data'), list):
            restaurants = data['data']
            logger.info(f"📊 Found {len(restaurants)} restaurants from API")
            return restaurants
        else:
            logger.error(f"Unexpected API response structure: {type(data)}")
            return []
            
    except Exception as e:
        logger.error(f"Error getting restaurants from API: {e}")
        return []

def update_restaurant_hours_via_api(restaurant_id: int, hours_open: str) -> bool:
    """Update restaurant hours via the API."""
    try:
        url = f'https://jewgo.onrender.com/api/restaurants/{restaurant_id}/hours'
        data = {'hours_open': hours_open}
        
        response = requests.put(url, json=data, timeout=10)
        
        if response.status_code == 200:
            logger.info(f"✅ Successfully updated restaurant ID {restaurant_id} with hours")
            return True
        else:
            logger.error(f"❌ Failed to update restaurant ID {restaurant_id}: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error updating restaurant ID {restaurant_id}: {e}")
        return False

def assign_sample_hours():
    """Main function to assign sample hours to restaurants."""
    logger.info("🕐 Sample Hours Assigner")
    logger.info("=" * 50)
    
    # Get restaurants from API
    restaurants = get_restaurants_from_api()
    if not restaurants:
        logger.error("No restaurants found")
        return
    
    # Filter restaurants without hours
    restaurants_without_hours = [
        r for r in restaurants 
        if not r.get('hours_of_operation') and not r.get('hours_open')
    ]
    
    logger.info(f"📊 Found {len(restaurants_without_hours)} restaurants without hours data")
    
    if not restaurants_without_hours:
        logger.info("✅ All restaurants already have hours!")
        return
    
    # Process each restaurant
    success_count = 0
    total_count = len(restaurants_without_hours)
    
    for i, restaurant in enumerate(restaurants_without_hours, 1):
        restaurant_id = restaurant.get('id')
        name = restaurant.get('name', 'Unknown')
        listing_type = restaurant.get('listing_type')
        
        logger.info(f"\n[{i}/{total_count}] Processing restaurant...")
        logger.info(f"🔍 Processing: {name}")
        
        # Determine restaurant type
        restaurant_type = get_restaurant_type(name, listing_type)
        logger.info(f"   📋 Type: {restaurant_type}")
        
        # Get sample hours
        if restaurant_type in HOURS_TEMPLATES:
            hours_template = HOURS_TEMPLATES[restaurant_type]
            sample_hours = hours_template["hours"]
            description = hours_template["description"]
            
            logger.info(f"   🕐 Assigning {restaurant_type} hours")
            logger.info(f"   📝 {description}")
            
            # Update via API
            if update_restaurant_hours_via_api(restaurant_id, sample_hours):
                success_count += 1
            else:
                logger.warning(f"   ❌ Failed to update hours for: {name}")
        else:
            logger.warning(f"   ❌ Unknown restaurant type for: {name}")
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info(f"✅ Completed! Updated {success_count}/{total_count} restaurants")
    logger.info(f"📊 Success rate: {(success_count/total_count)*100:.1f}%")

def main():
    """Main entry point."""
    print("🕐 Sample Hours Assigner")
    print("=" * 50)
    print("\nThis script will assign reasonable sample hours to restaurants")
    print("based on their type (bakery, restaurant, cafe, etc.)")
    print("\nOptions:")
    print("1. Process all restaurants missing hours")
    print("2. Process first 10 restaurants (test)")
    print("3. Process first 50 restaurants")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        assign_sample_hours()
    elif choice == "2":
        # Limit to first 10 for testing
        restaurants = get_restaurants_from_api()
        restaurants_without_hours = [
            r for r in restaurants 
            if not r.get('hours_of_operation') and not r.get('hours_open')
        ][:10]
        
        logger.info(f"📊 Processing first 10 restaurants without hours")
        # Process the limited list
        success_count = 0
        for i, restaurant in enumerate(restaurants_without_hours, 1):
            restaurant_id = restaurant.get('id')
            name = restaurant.get('name', 'Unknown')
            restaurant_type = get_restaurant_type(name, restaurant.get('listing_type'))
            
            logger.info(f"\n[{i}/10] Processing: {name} ({restaurant_type})")
            
            if restaurant_type in HOURS_TEMPLATES:
                sample_hours = HOURS_TEMPLATES[restaurant_type]["hours"]
                if update_restaurant_hours_via_api(restaurant_id, sample_hours):
                    success_count += 1
        
        logger.info(f"\n✅ Test completed! Updated {success_count}/10 restaurants")
        
    elif choice == "3":
        # Limit to first 50
        restaurants = get_restaurants_from_api()
        restaurants_without_hours = [
            r for r in restaurants 
            if not r.get('hours_of_operation') and not r.get('hours_open')
        ][:50]
        
        logger.info(f"📊 Processing first 50 restaurants without hours")
        # Process the limited list
        success_count = 0
        for i, restaurant in enumerate(restaurants_without_hours, 1):
            restaurant_id = restaurant.get('id')
            name = restaurant.get('name', 'Unknown')
            restaurant_type = get_restaurant_type(name, restaurant.get('listing_type'))
            
            logger.info(f"\n[{i}/50] Processing: {name} ({restaurant_type})")
            
            if restaurant_type in HOURS_TEMPLATES:
                sample_hours = HOURS_TEMPLATES[restaurant_type]["hours"]
                if update_restaurant_hours_via_api(restaurant_id, sample_hours):
                    success_count += 1
        
        logger.info(f"\n✅ Completed! Updated {success_count}/50 restaurants")
        
    elif choice == "4":
        print("Exiting...")
        return
    else:
        print("Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main() 