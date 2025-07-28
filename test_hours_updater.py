#!/usr/bin/env python3
"""
Test script for Google Hours Updater
Tests API connectivity and shows sample results
"""

import os
import requests
from google_places_hours_updater import GoogleHoursUpdater

def test_api_keys():
    """Test if API keys are working"""
    print("🔑 Testing API Keys")
    print("=" * 30)
    
    # Test Google Places API
    places_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if places_key:
        print("✅ GOOGLE_PLACES_API_KEY found")
        
        # Test with a simple search
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': 'McDonald\'s Miami',
            'key': places_key,
            'type': 'restaurant'
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'OK':
                    print("✅ Google Places API working")
                    print(f"   Found: {data['results'][0]['name']}")
                else:
                    print(f"❌ Google Places API error: {data['status']}")
            else:
                print(f"❌ Google Places API HTTP error: {response.status_code}")
        except Exception as e:
            print(f"❌ Google Places API test failed: {e}")
    else:
        print("❌ GOOGLE_PLACES_API_KEY not found")
    
    # Test Google Knowledge Graph API
    kg_key = os.getenv('GOOGLE_KNOWLEDGE_GRAPH_API_KEY')
    if kg_key:
        print("✅ GOOGLE_KNOWLEDGE_GRAPH_API_KEY found")
        
        # Test with a simple search
        url = "https://kgsearch.googleapis.com/v1/entities:search"
        params = {
            'query': 'McDonald\'s',
            'key': kg_key,
            'types': 'Restaurant',
            'limit': 1
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get('itemListElement'):
                    print("✅ Google Knowledge Graph API working")
                    print(f"   Found: {data['itemListElement'][0]['result']['name']}")
                else:
                    print("❌ Google Knowledge Graph API: No results")
            else:
                print(f"❌ Google Knowledge Graph API HTTP error: {response.status_code}")
        except Exception as e:
            print(f"❌ Google Knowledge Graph API test failed: {e}")
    else:
        print("❌ GOOGLE_KNOWLEDGE_GRAPH_API_KEY not found")

def test_sample_restaurants():
    """Test with a few sample restaurants"""
    print("\n🍽️ Testing Sample Restaurants")
    print("=" * 30)
    
    updater = GoogleHoursUpdater()
    
    # Get a few restaurants without hours
    restaurants = updater.get_restaurants_without_hours()
    
    if not restaurants:
        print("✅ All restaurants already have hours data!")
        return
    
    print(f"📊 Found {len(restaurants)} restaurants without hours")
    
    # Test with first 3 restaurants
    test_restaurants = restaurants[:3]
    
    for i, restaurant in enumerate(test_restaurants, 1):
        print(f"\n[{i}/{len(test_restaurants)}] Testing: {restaurant['name']}")
        print(f"   Address: {restaurant.get('address', 'N/A')}")
        print(f"   Location: {restaurant.get('city', '')}, {restaurant.get('state', '')}")
        
        # Test Google Places search
        search_query = restaurant['name']
        location = f"{restaurant.get('city', '')} {restaurant.get('state', '')}".strip()
        
        place_result = updater.search_google_places(search_query, location)
        
        if place_result:
            print(f"   ✅ Found on Google Places: {place_result['name']}")
            print(f"   📍 Place ID: {place_result['place_id']}")
            
            # Get details
            place_details = updater.get_place_details(place_result['place_id'])
            
            if place_details and 'opening_hours' in place_details:
                hours_open = updater.format_hours_from_places_api(place_details['opening_hours'])
                print(f"   🕐 Hours: {hours_open}")
            else:
                print("   ❌ No hours found")
        else:
            print("   ❌ Not found on Google Places")
        
        # Test Knowledge Graph
        kg_result = updater.search_google_knowledge_graph(search_query)
        if kg_result:
            print(f"   📊 Found on Knowledge Graph: {kg_result.get('name', 'Unknown')}")
        else:
            print("   ❌ Not found on Knowledge Graph")

def show_restaurants_without_hours():
    """Show list of restaurants without hours"""
    print("\n📋 Restaurants Without Hours")
    print("=" * 30)
    
    updater = GoogleHoursUpdater()
    restaurants = updater.get_restaurants_without_hours()
    
    if not restaurants:
        print("✅ All restaurants have hours data!")
        return
    
    print(f"📊 Total: {len(restaurants)} restaurants")
    print("\nFirst 10 restaurants without hours:")
    
    for i, restaurant in enumerate(restaurants[:10], 1):
        print(f"{i:2d}. {restaurant['name']}")
        print(f"    {restaurant.get('address', 'No address')}")
        print(f"    {restaurant.get('city', '')}, {restaurant.get('state', '')}")
        print()

if __name__ == "__main__":
    print("🧪 Google Hours Updater Test")
    print("=" * 50)
    
    # Test API keys
    test_api_keys()
    
    # Show restaurants without hours
    show_restaurants_without_hours()
    
    # Test with sample restaurants
    test_sample_restaurants()
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")
    print("\nTo run the full updater:")
    print("python google_places_hours_updater.py") 