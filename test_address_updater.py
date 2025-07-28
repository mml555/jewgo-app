#!/usr/bin/env python3
"""
Test script for Google Places Address Updater
Demonstrates how to use the updater to fix missing zip codes
"""

import os
import sys
from google_places_address_updater import GooglePlacesAddressUpdater

def test_single_restaurant():
    """Test updating a single restaurant (26 Sushi and wok)"""
    
    # Get API key from environment
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    
    if not api_key:
        print("❌ Please set GOOGLE_PLACES_API_KEY environment variable")
        print("   export GOOGLE_PLACES_API_KEY='your_api_key_here'")
        return
    
    # Initialize updater
    updater = GooglePlacesAddressUpdater(api_key)
    
    # Test data for "26 Sushi and wok"
    test_restaurant = {
        'name': '26 Sushi and wok',
        'address': '9487 Harding Ave',
        'city': 'Surfside',
        'state': 'FL',
        'zip_code': ''
    }
    
    print(f"🔍 Searching for: {test_restaurant['name']}")
    print(f"📍 Address: {test_restaurant['address']}, {test_restaurant['city']}, {test_restaurant['state']}")
    
    # Search for the place
    place_data = updater.search_place_by_address(
        test_restaurant['name'],
        test_restaurant['address'],
        test_restaurant['city'],
        test_restaurant['state']
    )
    
    if place_data:
        print("✅ Found restaurant in Google Places!")
        print(f"📍 Formatted Address: {place_data.get('formatted_address', 'N/A')}")
        
        # Extract address components
        address_components = updater.extract_address_components(place_data.get('address_components', []))
        
        print("📋 Address Components:")
        for key, value in address_components.items():
            print(f"   {key}: {value}")
        
        # Check if we found a zip code
        if 'zip_code' in address_components:
            print(f"🎯 Found zip code: {address_components['zip_code']}")
        else:
            print("❌ No zip code found")
            
        # Show other available data
        if place_data.get('rating'):
            print(f"⭐ Rating: {place_data['rating']}")
        if place_data.get('user_ratings_total'):
            print(f"📊 Reviews: {place_data['user_ratings_total']}")
        if place_data.get('website'):
            print(f"🌐 Website: {place_data['website']}")
            
    else:
        print("❌ Restaurant not found in Google Places")

def show_missing_zip_restaurants():
    """Show restaurants with missing zip codes"""
    
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not api_key:
        print("❌ Please set GOOGLE_PLACES_API_KEY environment variable")
        return
    
    updater = GooglePlacesAddressUpdater(api_key)
    restaurants = updater.get_restaurants_with_missing_zip()
    
    print(f"📊 Found {len(restaurants)} restaurants with missing zip codes:")
    print()
    
    for i, (restaurant_id, name, address, city, state, zip_code) in enumerate(restaurants[:10], 1):
        print(f"{i:2d}. {name}")
        print(f"    📍 {address}, {city}, {state}")
        print()

def main():
    """Main function"""
    print("🔧 Google Places Address Updater Test")
    print("=" * 40)
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == 'list':
        show_missing_zip_restaurants()
    else:
        test_single_restaurant()
    
    print()
    print("💡 To run the full updater:")
    print("   python google_places_address_updater.py")
    print()
    print("💡 To see all restaurants with missing zip codes:")
    print("   python test_address_updater.py list")

if __name__ == "__main__":
    main() 