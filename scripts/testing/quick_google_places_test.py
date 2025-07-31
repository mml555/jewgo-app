#!/usr/bin/env python3
"""
Quick Google Places API Test
===========================

A simple test script to quickly verify Google Places API functionality
with sample restaurant data. This script doesn't require database connection
and can be run immediately to test the API key and basic functionality.

Author: JewGo Development Team
Version: 1.0
"""

import os
import requests
import json
import time
from typing import Dict, Any

def test_google_places_api(api_key: str, restaurant_name: str, address: str):
    """Test Google Places API with a sample restaurant."""
    
    print(f"🏪 Testing: {restaurant_name}")
    print(f"📍 Address: {address}")
    print("-" * 50)
    
    # Step 1: Search for the place
    print("1. 🔍 Searching for place...")
    search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    search_params = {
        'query': f"{restaurant_name} {address}",
        'key': api_key,
        'type': 'restaurant'
    }
    
    try:
        response = requests.get(search_url, params=search_params, timeout=10)
        response.raise_for_status()
        search_data = response.json()
        
        print(f"   Status: {search_data['status']}")
        
        if search_data['status'] == 'OK' and search_data['results']:
            place = search_data['results'][0]
            place_id = place['place_id']
            print(f"   ✅ Found Place ID: {place_id}")
            print(f"   📍 Google Name: {place.get('name', 'N/A')}")
            print(f"   🏠 Google Address: {place.get('formatted_address', 'N/A')}")
            print(f"   📞 Phone: {place.get('formatted_phone_number', 'N/A')}")
            print(f"   ⭐ Rating: {place.get('rating', 'N/A')}")
            print(f"   💰 Price Level: {place.get('price_level', 'N/A')}")
            
            # Step 2: Get detailed place information
            print("\n2. 📋 Getting detailed information...")
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                'place_id': place_id,
                'fields': 'opening_hours,website,formatted_phone_number,rating,price_level,formatted_address,url',
                'key': api_key
            }
            
            response = requests.get(details_url, params=details_params, timeout=10)
            response.raise_for_status()
            details_data = response.json()
            
            print(f"   Status: {details_data['status']}")
            
            if details_data['status'] == 'OK':
                result = details_data['result']
                
                # Display hours
                opening_hours = result.get('opening_hours', {})
                if opening_hours and 'weekday_text' in opening_hours:
                    print("\n   🕒 Opening Hours:")
                    for day_hours in opening_hours['weekday_text']:
                        print(f"      {day_hours}")
                    
                    # Test hours formatting
                    formatted_hours = format_hours_from_places_api(opening_hours)
                    print(f"\n   📝 Formatted Hours: {formatted_hours}")
                else:
                    print("\n   🕒 Opening Hours: Not available")
                
                # Display other details
                print(f"\n   🌐 Website: {result.get('website', 'Not available')}")
                print(f"   📞 Phone: {result.get('formatted_phone_number', 'Not available')}")
                print(f"   ⭐ Rating: {result.get('rating', 'Not available')}")
                print(f"   💰 Price Level: {result.get('price_level', 'Not available')}")
                print(f"   🔗 Google Maps URL: {result.get('url', 'Not available')}")
                
                return True
            else:
                print(f"   ❌ Error getting details: {details_data.get('error_message', 'Unknown error')}")
                return False
        else:
            print(f"   ❌ No places found. Status: {search_data.get('status')}")
            if 'error_message' in search_data:
                print(f"   Error: {search_data['error_message']}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def format_hours_from_places_api(opening_hours: dict) -> str:
    """Format opening hours from Google Places API format."""
    if not opening_hours or 'weekday_text' not in opening_hours:
        return ""
        
    weekday_text = opening_hours['weekday_text']
    
    day_mapping = {
        'Monday': 'Mon',
        'Tuesday': 'Tue', 
        'Wednesday': 'Wed',
        'Thursday': 'Thu',
        'Friday': 'Fri',
        'Saturday': 'Sat',
        'Sunday': 'Sun'
    }
    
    formatted_hours = []
    for day_text in weekday_text:
        if ': ' in day_text:
            day, hours = day_text.split(': ', 1)
            short_day = day_mapping.get(day, day[:3])
            formatted_hours.append(f"{short_day} {hours}")
    
    return ', '.join(formatted_hours)

def test_api_key_validity(api_key: str):
    """Test if the API key is valid with a simple request."""
    print("🔑 Testing API Key Validity...")
    
    # Simple test with a known place ID (McDonald's in NYC)
    test_url = "https://maps.googleapis.com/maps/api/place/details/json"
    test_params = {
        'place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY4',
        'fields': 'name',
        'key': api_key
    }
    
    try:
        response = requests.get(test_url, params=test_params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] == 'OK':
            print("   ✅ API Key is valid")
            return True
        elif data['status'] == 'REQUEST_DENIED':
            print("   ❌ API Key is invalid or restricted")
            print(f"   Error: {data.get('error_message', 'Unknown error')}")
            return False
        else:
            print(f"   ⚠️  API Key test returned status: {data['status']}")
            return True
            
    except Exception as e:
        print(f"   ❌ API Key test failed: {e}")
        return False

def main():
    """Main test function."""
    
    print("🔍 Google Places API Quick Test")
    print("=" * 50)
    
    # Get API key
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not api_key:
        print("❌ GOOGLE_PLACES_API_KEY environment variable not set")
        print("\nTo set your API key:")
        print("export GOOGLE_PLACES_API_KEY='your_api_key_here'")
        return
    
    print("✅ Google Places API Key found")
    
    # Test API key validity first
    if not test_api_key_validity(api_key):
        print("\n❌ API Key validation failed. Please check your key and try again.")
        return
    
    print("\n" + "=" * 50)
    
    # Test with sample restaurants
    test_restaurants = [
        {
            'name': 'McDonald\'s',
            'address': '123 Main St, Miami, FL 33101'
        },
        {
            'name': 'Pizza Hut',
            'address': '456 Oak Ave, Miami, FL 33102'
        },
        {
            'name': 'Subway',
            'address': '789 Pine St, Miami, FL 33103'
        },
        {
            'name': 'Starbucks',
            'address': '321 Elm St, Miami, FL 33104'
        },
        {
            'name': 'Burger King',
            'address': '654 Maple Ave, Miami, FL 33105'
        }
    ]
    
    successful_tests = 0
    total_tests = len(test_restaurants)
    
    for i, restaurant in enumerate(test_restaurants, 1):
        print(f"\n📊 Test {i}/{total_tests}")
        
        success = test_google_places_api(
            api_key, 
            restaurant['name'], 
            restaurant['address']
        )
        
        if success:
            successful_tests += 1
            print(f"   ✅ Test PASSED for {restaurant['name']}")
        else:
            print(f"   ❌ Test FAILED for {restaurant['name']}")
        
        # Rate limiting - wait between requests
        if i < total_tests:
            print("   ⏳ Waiting 2 seconds before next test...")
            time.sleep(2)
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    print(f"✅ Successful Tests: {successful_tests}/{total_tests}")
    print(f"❌ Failed Tests: {total_tests - successful_tests}/{total_tests}")
    print(f"📈 Success Rate: {(successful_tests/total_tests)*100:.1f}%")
    
    if successful_tests == total_tests:
        print("\n🎉 All tests passed! Google Places API is working correctly.")
    elif successful_tests > 0:
        print(f"\n⚠️  {successful_tests} out of {total_tests} tests passed. API is partially working.")
    else:
        print("\n❌ All tests failed. Please check your API key and configuration.")

if __name__ == "__main__":
    main() 