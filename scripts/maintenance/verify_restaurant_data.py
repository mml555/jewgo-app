#!/usr/bin/env python3
"""
Verify Restaurant Data
====================

This script verifies that restaurant data is being returned correctly
from the production API after the database schema fix.

Author: JewGo Development Team
Version: 1.0
"""

import requests
import json

def verify_restaurant_data():
    """Verify that restaurant data is being returned correctly."""
    
    base_url = "https://jewgo.onrender.com"
    url = base_url + "/api/restaurants?limit=3"
    
    print("🔍 Verifying Restaurant Data")
    print("=" * 30)
    print(f"URL: {url}")
    print()
    
    try:
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if isinstance(data, dict) and 'restaurants' in data:
                restaurants = data['restaurants']
                print(f"✅ Success: {len(restaurants)} restaurants returned")
                print()
                
                for i, restaurant in enumerate(restaurants, 1):
                    print(f"Restaurant {i}:")
                    print(f"  Name: {restaurant.get('name', 'N/A')}")
                    print(f"  Address: {restaurant.get('address', 'N/A')}")
                    print(f"  City: {restaurant.get('city', 'N/A')}")
                    print(f"  State: {restaurant.get('state', 'N/A')}")
                    print(f"  Rating: {restaurant.get('rating', 'N/A')}")
                    print(f"  Google Rating: {restaurant.get('google_rating', 'N/A')}")
                    print(f"  Kosher Type: {restaurant.get('kosher_category', 'N/A')}")
                    print(f"  Cuisine Type: {restaurant.get('cuisine_type', 'N/A')}")
                    print()
                    
            elif isinstance(data, list):
                print(f"✅ Success: {len(data)} restaurants returned (list format)")
                print()
                
                for i, restaurant in enumerate(data[:3], 1):
                    print(f"Restaurant {i}:")
                    print(f"  Name: {restaurant.get('name', 'N/A')}")
                    print(f"  Address: {restaurant.get('address', 'N/A')}")
                    print(f"  City: {restaurant.get('city', 'N/A')}")
                    print(f"  State: {restaurant.get('state', 'N/A')}")
                    print(f"  Rating: {restaurant.get('rating', 'N/A')}")
                    print(f"  Google Rating: {restaurant.get('google_rating', 'N/A')}")
                    print(f"  Kosher Type: {restaurant.get('kosher_category', 'N/A')}")
                    print(f"  Cuisine Type: {restaurant.get('cuisine_type', 'N/A')}")
                    print()
            else:
                print(f"❌ Unexpected response format: {type(data)}")
                print(f"Response: {json.dumps(data, indent=2)[:500]}...")
                
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        print(f"Response: {response.text[:200]}...")

if __name__ == "__main__":
    verify_restaurant_data()
    print("🎉 Restaurant data verification completed!") 