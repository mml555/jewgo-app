#!/usr/bin/env python3
"""
Test Google Places API with Real Restaurant Data
Tests the API with actual restaurants from the database.
"""

import os
import requests
import json
from database_manager import DatabaseManager

def test_with_real_restaurant():
    """Test Google Places API with a real restaurant from the database."""
    
    # Get API key
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not api_key:
        print("❌ GOOGLE_PLACES_API_KEY environment variable not set")
        print("\nTo set your API key:")
        print("export GOOGLE_PLACES_API_KEY='your_api_key_here'")
        return
    
    # Connect to database
    db_manager = DatabaseManager()
    if not db_manager.connect():
        print("❌ Failed to connect to database")
        return
    
    try:
        # Get a few restaurants from the database
        restaurants = db_manager.search_restaurants(limit=5)
        
        if not restaurants:
            print("❌ No restaurants found in database")
            return
        
        print(f"✅ Found {len(restaurants)} restaurants in database")
        print("=" * 60)
        
        for i, restaurant in enumerate(restaurants, 1):
            print(f"\n{i}. Testing: {restaurant['name']}")
            print(f"   Address: {restaurant['address']}")
            
            # Test Google Places API
            success = test_restaurant_with_places_api(api_key, restaurant)
            
            if success:
                print(f"   ✅ SUCCESS - Hours found")
            else:
                print(f"   ❌ FAILED - No hours found")
            
            print("-" * 40)
    
    finally:
        db_manager.disconnect()

def test_restaurant_with_places_api(api_key: str, restaurant: dict) -> bool:
    """Test Google Places API for a specific restaurant."""
    
    restaurant_name = restaurant.get('name', '')
    address = restaurant.get('address', '')
    
    if not restaurant_name or not address:
        return False
    
    try:
        # Step 1: Search for the place
        search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        search_params = {
            'query': f"{restaurant_name} {address}",
            'key': api_key,
            'type': 'restaurant'
        }
        
        response = requests.get(search_url, params=search_params)
        response.raise_for_status()
        search_data = response.json()
        
        if search_data['status'] != 'OK' or not search_data['results']:
            return False
        
        place = search_data['results'][0]
        place_id = place['place_id']
        
        # Step 2: Get place details
        details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        details_params = {
            'place_id': place_id,
            'fields': 'opening_hours',
            'key': api_key
        }
        
        response = requests.get(details_url, params=details_params)
        response.raise_for_status()
        details_data = response.json()
        
        if details_data['status'] == 'OK':
            result = details_data['result']
            opening_hours = result.get('opening_hours', {})
            
            if opening_hours and 'weekday_text' in opening_hours:
                print(f"   📅 Hours found:")
                for day_hours in opening_hours['weekday_text']:
                    print(f"      {day_hours}")
                return True
        
        return False
        
    except Exception as e:
        print(f"   Error: {e}")
        return False

def main():
    """Main function."""
    print("🧪 Testing Google Places API with Real Restaurant Data")
    print("=" * 60)
    
    test_with_real_restaurant()

if __name__ == "__main__":
    main() 