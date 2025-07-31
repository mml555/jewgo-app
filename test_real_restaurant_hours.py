#!/usr/bin/env python3
"""
Test script for real restaurant hours updates using Google Places API
"""

import os
import requests
import json
from datetime import datetime

# Set your Google Places API key here
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key

def test_google_places_api():
    """Test Google Places API connection"""
    print("🔍 Testing Google Places API Connection")
    print("=" * 50)
    
    # Test with a well-known restaurant (McDonald's in NYC)
    test_place_id = "ChIJN1t_tDeuEmsRUsoyG83frY4"
    
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': test_place_id,
        'fields': 'name,opening_hours,utc_offset_minutes',
        'key': GOOGLE_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        print(f"📊 API Response Status: {data.get('status')}")
        
        if data.get('status') == 'OK':
            result = data.get('result', {})
            print(f"✅ Restaurant: {result.get('name')}")
            
            opening_hours = result.get('opening_hours', {})
            if opening_hours:
                print(f"🕐 Open Now: {opening_hours.get('open_now')}")
                print(f"📅 Weekday Text:")
                for day in opening_hours.get('weekday_text', [])[:3]:  # Show first 3 days
                    print(f"   {day}")
                print(f"   ...")
            else:
                print("❌ No opening hours available")
                
            print(f"🌍 UTC Offset: {result.get('utc_offset_minutes')} minutes")
            return True
        else:
            print(f"❌ API Error: {data.get('status')}")
            print(f"📝 Error Message: {data.get('error_message', 'No error message')}")
            return False
            
    except Exception as e:
        print(f"❌ Request Error: {e}")
        return False

def search_kosher_restaurants():
    """Search for kosher restaurants in Miami"""
    print("\n🍽️  Searching for Kosher Restaurants in Miami")
    print("=" * 50)
    
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': 'kosher restaurant miami',
        'key': GOOGLE_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get('status') == 'OK':
            restaurants = data.get('results', [])
            print(f"📊 Found {len(restaurants)} restaurants")
            
            for i, restaurant in enumerate(restaurants[:5], 1):  # Show first 5
                print(f"\n{i}. {restaurant.get('name')}")
                print(f"   📍 {restaurant.get('formatted_address')}")
                print(f"   🆔 Place ID: {restaurant.get('place_id')}")
                print(f"   ⭐ Rating: {restaurant.get('rating', 'N/A')}")
                
                # Check if it's open
                if restaurant.get('opening_hours', {}).get('open_now'):
                    print(f"   🟢 Currently Open")
                else:
                    print(f"   🔴 Currently Closed")
                    
            return restaurants
        else:
            print(f"❌ Search Error: {data.get('status')}")
            return []
            
    except Exception as e:
        print(f"❌ Search Error: {e}")
        return []

def get_restaurant_hours(place_id):
    """Get detailed hours for a specific restaurant"""
    print(f"\n🕐 Getting Hours for Restaurant")
    print("=" * 50)
    
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'fields': 'name,opening_hours,utc_offset_minutes',
        'key': GOOGLE_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get('status') == 'OK':
            result = data.get('result', {})
            restaurant_name = result.get('name')
            opening_hours = result.get('opening_hours', {})
            
            print(f"🍽️  Restaurant: {restaurant_name}")
            print(f"🕐 Open Now: {opening_hours.get('open_now')}")
            print(f"📅 Weekly Schedule:")
            
            for day in opening_hours.get('weekday_text', []):
                print(f"   {day}")
                
            periods = opening_hours.get('periods', [])
            print(f"\n📊 Structured Hours Data:")
            print(json.dumps(periods[:2], indent=2))  # Show first 2 periods
            print("   ...")
            
            return {
                'name': restaurant_name,
                'weekday_text': opening_hours.get('weekday_text', []),
                'periods': periods,
                'utc_offset_minutes': result.get('utc_offset_minutes')
            }
        else:
            print(f"❌ Error getting hours: {data.get('status')}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_backend_hours_update(restaurant_id, place_id):
    """Test the backend hours update endpoint"""
    print(f"\n🔄 Testing Backend Hours Update")
    print("=" * 50)
    
    url = "https://jewgo.onrender.com/api/admin/update-hours"
    data = {
        'id': restaurant_id,
        'placeId': place_id
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result.get('message')}")
            print(f"🆔 Restaurant ID: {result.get('restaurant_id')}")
            print(f"🕐 Hours Updated: {result.get('hours_updated')}")
            print(f"🌍 Timezone: {result.get('timezone')}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request Error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Real Restaurant Hours Integration")
    print("=" * 60)
    
    # Check if API key is set
    if GOOGLE_API_KEY == "YOUR_API_KEY_HERE":
        print("❌ Please set your Google Places API key in the script")
        print("📝 Edit the GOOGLE_API_KEY variable at the top of this file")
        return
    
    # Test 1: API Connection
    if not test_google_places_api():
        print("❌ Google Places API test failed. Check your API key.")
        return
    
    # Test 2: Search for restaurants
    restaurants = search_kosher_restaurants()
    if not restaurants:
        print("❌ No restaurants found. Check your search query.")
        return
    
    # Test 3: Get hours for first restaurant
    first_restaurant = restaurants[0]
    place_id = first_restaurant.get('place_id')
    restaurant_name = first_restaurant.get('name')
    
    print(f"\n🎯 Testing with: {restaurant_name}")
    hours_data = get_restaurant_hours(place_id)
    
    if hours_data:
        print(f"\n✅ Successfully retrieved hours data for {restaurant_name}")
        print(f"📊 Data ready for backend update")
        
        # Test 4: Update backend (using one of our test restaurants)
        print(f"\n🔄 Testing Backend Update...")
        test_backend_hours_update(833, place_id)  # Use our test restaurant ID 833
        
    else:
        print(f"❌ Failed to get hours data for {restaurant_name}")

if __name__ == "__main__":
    main() 