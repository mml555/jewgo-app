#!/usr/bin/env python3
"""
Test Google Places Image Updater
Demonstrates how the image updater works with sample restaurants.
"""

import os
import requests
from google_places_image_updater import GooglePlacesImageUpdater

def test_image_generation():
    """Test image generation with a sample restaurant."""
    
    print("🖼️ Testing Google Places Image Updater")
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
    updater = GooglePlacesImageUpdater(api_key)
    
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
                
                # Get photos
                photos = place_details.get('photos', [])
                if photos:
                    print(f"   📸 Found {len(photos)} photos")
                    
                    # Select best photo
                    photo_reference = updater.select_best_photo(photos)
                    if photo_reference:
                        # Generate photo URL
                        image_url = updater.get_photo_url(photo_reference)
                        print(f"   🖼️ Generated Image URL: {image_url}")
                        
                        # Test if image is accessible
                        try:
                            response = requests.head(image_url)
                            if response.status_code == 200:
                                print("   ✅ Image URL is accessible")
                            else:
                                print(f"   ⚠️ Image URL returned status: {response.status_code}")
                        except Exception as e:
                            print(f"   ❌ Error testing image URL: {e}")
                    else:
                        print("   ❌ No suitable photo found")
                else:
                    print("   ❌ No photos found")
                
            else:
                print("   ❌ Failed to get place details")
        else:
            print("   ❌ Place not found")
        
        print("-" * 40)

def main():
    """Main test function."""
    test_image_generation()
    
    print("\n" + "=" * 50)
    print("🎯 Next Steps:")
    print("1. Set your Google Places API key")
    print("2. Run: python google_places_image_updater.py")
    print("3. Choose option 3 to test with 5 restaurants")
    print("4. Check restaurant detail pages for updated images!")

if __name__ == "__main__":
    main() 