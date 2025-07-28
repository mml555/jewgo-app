#!/usr/bin/env python3
"""
Google Places API Demo
Demonstrates how the Google Places API integration works.
"""

import os
import requests
import json
from typing import Dict, Any

def demo_google_places_integration():
    """Demonstrate Google Places API integration."""
    
    print("🗺️ Google Places API Integration Demo")
    print("=" * 50)
    
    # Get API key
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not api_key:
        print("❌ GOOGLE_PLACES_API_KEY not set")
        print("\nTo set your API key:")
        print("export GOOGLE_PLACES_API_KEY='your_api_key_here'")
        print("\nThen run this script again.")
        return
    
    print("✅ API Key found")
    print("\n📋 Demo Restaurant:")
    print("   Name: 17 Restaurant and Sushi Bar")
    print("   Address: 1751 Alton Rd, Miami Beach, FL")
    print("\n" + "=" * 50)
    
    # Demo the process
    restaurant_name = "17 Restaurant and Sushi Bar"
    address = "1751 Alton Rd, Miami Beach, FL"
    
    print("\n🔍 Step 1: Searching for restaurant...")
    place_id = search_restaurant(api_key, restaurant_name, address)
    
    if place_id:
        print(f"✅ Found restaurant with Place ID: {place_id}")
        
        print("\n📅 Step 2: Fetching restaurant details...")
        details = get_restaurant_details(api_key, place_id)
        
        if details:
            display_restaurant_details(details)
        else:
            print("❌ Failed to get restaurant details")
    else:
        print("❌ Restaurant not found in Google Places")
    
    print("\n" + "=" * 50)
    print("🎯 Next Steps:")
    print("1. Set your Google Places API key")
    print("2. Run: python test_google_places.py")
    print("3. Run: python google_places_hours_updater.py")
    print("4. Check restaurant detail pages for hours!")

def search_restaurant(api_key: str, name: str, address: str) -> str:
    """Search for a restaurant and return its place_id."""
    
    try:
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': f"{name} {address}",
            'key': api_key,
            'type': 'restaurant'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data['status'] == 'OK' and data['results']:
            place = data['results'][0]
            print(f"   Found: {place.get('name', 'Unknown')}")
            print(f"   Address: {place.get('formatted_address', 'Unknown')}")
            return place['place_id']
        else:
            print(f"   Search failed: {data.get('status', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"   Error: {e}")
        return None

def get_restaurant_details(api_key: str, place_id: str) -> Dict[str, Any]:
    """Get detailed information about a restaurant."""
    
    try:
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'place_id': place_id,
            'fields': 'opening_hours,formatted_phone_number,website,rating,price_level,formatted_address',
            'key': api_key
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data['status'] == 'OK':
            return data['result']
        else:
            print(f"   Details failed: {data.get('status', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"   Error: {e}")
        return None

def display_restaurant_details(details: Dict[str, Any]):
    """Display restaurant details in a formatted way."""
    
    print("✅ Restaurant details retrieved successfully!")
    print("\n📊 Restaurant Information:")
    
    # Hours
    opening_hours = details.get('opening_hours', {})
    if opening_hours and 'weekday_text' in opening_hours:
        print("\n📅 Opening Hours:")
        for day_hours in opening_hours['weekday_text']:
            print(f"   {day_hours}")
    else:
        print("\n📅 Opening Hours: Not available")
    
    # Other details
    print(f"\n📞 Phone: {details.get('formatted_phone_number', 'Not available')}")
    print(f"🌐 Website: {details.get('website', 'Not available')}")
    print(f"⭐ Rating: {details.get('rating', 'Not available')}")
    print(f"💰 Price Level: {details.get('price_level', 'Not available')}")
    
    # Show how this would be stored in database
    hours_text = format_hours_for_database(opening_hours)
    print(f"\n💾 Database Storage Format:")
    print(f"   hours_of_operation: '{hours_text}'")

def format_hours_for_database(opening_hours: Dict[str, Any]) -> str:
    """Format hours for database storage."""
    
    if not opening_hours or 'weekday_text' not in opening_hours:
        return "Hours not available"
    
    return " | ".join(opening_hours['weekday_text'])

def main():
    """Main function."""
    demo_google_places_integration()

if __name__ == "__main__":
    main() 