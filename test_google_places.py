#!/usr/bin/env python3
"""
Test Google Places API Integration
Simple test script to verify Google Places API is working.
"""

import os
import requests
import json
from typing import Dict, Any

def test_google_places_api(api_key: str, restaurant_name: str, address: str):
    """Test Google Places API with a sample restaurant."""
    
    print(f"Testing Google Places API for: {restaurant_name}")
    print(f"Address: {address}")
    print("-" * 50)
    
    # Step 1: Search for the place
    print("1. Searching for place...")
    search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    search_params = {
        'query': f"{restaurant_name} {address}",
        'key': api_key,
        'type': 'restaurant'
    }
    
    try:
        response = requests.get(search_url, params=search_params)
        response.raise_for_status()
        search_data = response.json()
        
        print(f"Search Status: {search_data['status']}")
        
        if search_data['status'] == 'OK' and search_data['results']:
            place = search_data['results'][0]
            place_id = place['place_id']
            print(f"Found Place ID: {place_id}")
            print(f"Place Name: {place.get('name', 'N/A')}")
            print(f"Place Address: {place.get('formatted_address', 'N/A')}")
            
            # Step 2: Get place details
            print("\n2. Getting place details...")
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                'place_id': place_id,
                'fields': 'opening_hours,formatted_phone_number,website,rating,price_level,formatted_address',
                'key': api_key
            }
            
            response = requests.get(details_url, params=details_params)
            response.raise_for_status()
            details_data = response.json()
            
            print(f"Details Status: {details_data['status']}")
            
            if details_data['status'] == 'OK':
                result = details_data['result']
                
                # Display hours
                opening_hours = result.get('opening_hours', {})
                if opening_hours and 'weekday_text' in opening_hours:
                    print("\n📅 Opening Hours:")
                    for day_hours in opening_hours['weekday_text']:
                        print(f"  {day_hours}")
                else:
                    print("\n📅 Opening Hours: Not available")
                
                # Display other details
                print(f"\n📞 Phone: {result.get('formatted_phone_number', 'Not available')}")
                print(f"🌐 Website: {result.get('website', 'Not available')}")
                print(f"⭐ Rating: {result.get('rating', 'Not available')}")
                print(f"💰 Price Level: {result.get('price_level', 'Not available')}")
                
                return True
            else:
                print(f"Error getting details: {details_data.get('error_message', 'Unknown error')}")
                return False
        else:
            print(f"No places found. Status: {search_data.get('status')}")
            if 'error_message' in search_data:
                print(f"Error: {search_data['error_message']}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def main():
    """Main test function."""
    
    # Get API key
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not api_key:
        print("❌ GOOGLE_PLACES_API_KEY environment variable not set")
        print("\nTo set your API key:")
        print("export GOOGLE_PLACES_API_KEY='your_api_key_here'")
        return
    
    print("✅ Google Places API Key found")
    print("=" * 50)
    
    # Test with a sample restaurant
    test_restaurants = [
        {
            'name': 'Pizza Hut',
            'address': '123 Main St, Miami, FL 33101'
        },
        {
            'name': 'McDonald\'s',
            'address': '456 Oak Ave, Miami, FL 33102'
        }
    ]
    
    for restaurant in test_restaurants:
        success = test_google_places_api(
            api_key, 
            restaurant['name'], 
            restaurant['address']
        )
        
        if success:
            print(f"\n✅ Test PASSED for {restaurant['name']}")
        else:
            print(f"\n❌ Test FAILED for {restaurant['name']}")
        
        print("\n" + "=" * 50)

if __name__ == "__main__":
    main() 