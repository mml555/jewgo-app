#!/usr/bin/env python3
"""
Test script for updated JewGo API with kosher_places integration
"""

import requests
import json
from datetime import datetime

def test_api_endpoints():
    """Test the updated API endpoints."""
    base_url = "http://localhost:5000"  # Adjust if your API runs on different port
    
    print("🧪 Testing Updated JewGo API with Kosher Places Integration")
    print("=" * 60)
    
    # Test 1: Get all places (both legacy and ORB)
    print("\n1. Testing /api/restaurants (all sources)")
    try:
        response = requests.get(f"{base_url}/api/restaurants?limit=10")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {len(data.get('data', []))} places")
            print(f"   Response keys: {list(data.keys())}")
            
            # Show sample places
            places = data.get('data', [])
            if places:
                print(f"   Sample places:")
                for i, place in enumerate(places[:3]):
                    source = place.get('source', 'unknown')
                    print(f"   {i+1}. {place.get('name', 'Unknown')} ({source})")
        else:
            print(f"❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Get only legacy restaurants
    print("\n2. Testing /api/restaurants (legacy only)")
    try:
        response = requests.get(f"{base_url}/api/restaurants?source=legacy&limit=5")
        if response.status_code == 200:
            data = response.json()
            places = data.get('data', [])
            print(f"✅ Success! Found {len(places)} legacy places")
            if places:
                print(f"   All sources: {[p.get('source') for p in places]}")
        else:
            print(f"❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Get only ORB kosher places
    print("\n3. Testing /api/restaurants (ORB only)")
    try:
        response = requests.get(f"{base_url}/api/restaurants?source=orb&limit=5")
        if response.status_code == 200:
            data = response.json()
            places = data.get('data', [])
            print(f"✅ Success! Found {len(places)} ORB places")
            if places:
                print(f"   All sources: {[p.get('source') for p in places]}")
        else:
            print(f"❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Search by category
    print("\n4. Testing /api/restaurants (search by category)")
    try:
        response = requests.get(f"{base_url}/api/restaurants?category=cafe&limit=5")
        if response.status_code == 200:
            data = response.json()
            places = data.get('data', [])
            print(f"✅ Success! Found {len(places)} places with 'cafe' category")
            if places:
                print(f"   Categories: {[p.get('kosher_category') for p in places]}")
        else:
            print(f"❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Get statistics
    print("\n5. Testing /api/statistics")
    try:
        response = requests.get(f"{base_url}/api/statistics")
        if response.status_code == 200:
            data = response.json()
            stats = data.get('data', {})
            print(f"✅ Success! Statistics:")
            print(f"   Total restaurants: {stats.get('total_restaurants', 0)}")
            print(f"   Total kosher restaurants: {stats.get('total_kosher_restaurants', 0)}")
            print(f"   Categories: {len(stats.get('categories', []))}")
        else:
            print(f"❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 6: Get categories
    print("\n6. Testing /api/categories")
    try:
        response = requests.get(f"{base_url}/api/categories")
        if response.status_code == 200:
            data = response.json()
            categories = data.get('data', [])
            print(f"✅ Success! Found {len(categories)} categories")
            print(f"   Sample categories: {[c.get('name') for c in categories[:5]]}")
        else:
            print(f"❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 7: Get restaurant detail
    print("\n7. Testing /api/restaurants/1")
    try:
        response = requests.get(f"{base_url}/api/restaurants/1")
        if response.status_code == 200:
            data = response.json()
            place = data.get('place', {})
            print(f"✅ Success! Found place: {place.get('name', 'Unknown')}")
            print(f"   Certifying agency: {place.get('certifying_agency', 'Unknown')}")
        elif response.status_code == 404:
            print("⚠️  No restaurant with ID 1 found (this is normal)")
        else:
            print(f"❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 API Testing Complete!")

if __name__ == "__main__":
    test_api_endpoints() 