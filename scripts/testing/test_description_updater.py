#!/usr/bin/env python3
"""
Test Google Places Description Updater
Demonstrates how the description updater works with sample restaurants.
"""

import os
import requests
from google_places_description_updater import GooglePlacesDescriptionUpdater

def test_description_generation():
    """Test description generation with a sample restaurant."""
    
    print("🧪 Testing Google Places Description Updater")
    print("=" * 50)
    
    # Get API key
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not api_key:
        print("❌ GOOGLE_PLACES_API_KEY not set")
        print("\nTo set your API key:")
        print("export GOOGLE_PLACES_API_KEY='your_api_key_here'")
        return
    
    print("✅ API Key found")
    
    # Create updater instance
    updater = GooglePlacesDescriptionUpdater(api_key)
    
    # Test with a sample restaurant
    test_restaurants = [
        {
            'name': '17 Restaurant and Sushi Bar',
            'address': '1751 Alton Rd, Miami Beach, FL'
        },
        {
            'name': 'Miami Kosher Pizza',
            'address': 'Miami, FL'
        }
    ]
    
    for restaurant in test_restaurants:
        print(f"\n🔍 Testing: {restaurant['name']}")
        print(f"   Address: {restaurant['address']}")
        
        # Search for the place
        place_id = updater.search_place(restaurant['name'], restaurant['address'])
        
        if place_id:
            print(f"   ✅ Found Place ID: {place_id}")
            
            # Get place details
            place_details = updater.get_place_details(place_id)
            
            if place_details:
                print("   ✅ Retrieved place details")
                
                # Generate description
                description = updater.generate_description(place_details, restaurant['name'])
                print(f"   📝 Generated Description: {description}")
                
            else:
                print("   ❌ Failed to get place details")
        else:
            print("   ❌ Place not found")
        
        print("-" * 40)

def main():
    """Main test function."""
    test_description_generation()
    
    print("\n" + "=" * 50)
    print("🎯 Next Steps:")
    print("1. Set your Google Places API key")
    print("2. Run: python google_places_description_updater.py")
    print("3. Choose option 3 to test with 5 restaurants")
    print("4. Check restaurant detail pages for updated descriptions!")

if __name__ == "__main__":
    main() 