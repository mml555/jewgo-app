#!/usr/bin/env python3
"""
Test API endpoints after database schema fix.
"""

import requests
import json
import time

def test_api_endpoints():
    """Test all API endpoints to ensure they work after schema fix."""
    base_url = "https://jewgo.onrender.com"
    
    print("🧪 Testing API endpoints after schema fix...")
    print("=" * 60)
    
    # Test health endpoint
    print("\n1️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Health endpoint working")
        else:
            print(f"   ❌ Health endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Health endpoint error: {e}")
    
    # Test root endpoint
    print("\n2️⃣ Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Root endpoint working - API Version: {data.get('version', 'unknown')}")
        else:
            print(f"   ❌ Root endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Root endpoint error: {e}")
    
    # Test restaurants endpoint
    print("\n3️⃣ Testing restaurants endpoint...")
    try:
        response = requests.get(f"{base_url}/api/restaurants?limit=5", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            restaurants = data.get('data', [])
            print(f"   ✅ Restaurants endpoint working - Found {len(restaurants)} restaurants")
            if restaurants:
                print(f"   📋 Sample restaurant: {restaurants[0].get('name', 'Unknown')}")
        else:
            print(f"   ❌ Restaurants endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Restaurants endpoint error: {e}")
    
    # Test statistics endpoint
    print("\n4️⃣ Testing statistics endpoint...")
    try:
        response = requests.get(f"{base_url}/api/statistics", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Statistics endpoint working")
            print(f"   📊 Total restaurants: {data.get('total_restaurants', 0)}")
            print(f"   📊 Kosher restaurants: {data.get('kosher_restaurants', 0)}")
        else:
            print(f"   ❌ Statistics endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Statistics endpoint error: {e}")
    
    # Test categories endpoint
    print("\n5️⃣ Testing categories endpoint...")
    try:
        response = requests.get(f"{base_url}/api/categories", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            categories = data.get('categories', [])
            print(f"   ✅ Categories endpoint working - Found {len(categories)} categories")
        else:
            print(f"   ❌ Categories endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Categories endpoint error: {e}")
    
    # Test states endpoint
    print("\n6️⃣ Testing states endpoint...")
    try:
        response = requests.get(f"{base_url}/api/states", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            states = data.get('states', [])
            print(f"   ✅ States endpoint working - Found {len(states)} states")
        else:
            print(f"   ❌ States endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ❌ States endpoint error: {e}")
    
    # Test restaurant search with filters
    print("\n7️⃣ Testing restaurant search with filters...")
    try:
        response = requests.get(f"{base_url}/api/restaurants?limit=3&category=Kosher", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            restaurants = data.get('data', [])
            print(f"   ✅ Search with filters working - Found {len(restaurants)} restaurants")
        else:
            print(f"   ❌ Search with filters failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Search with filters error: {e}")
    
    # Test individual restaurant endpoint
    print("\n8️⃣ Testing individual restaurant endpoint...")
    try:
        response = requests.get(f"{base_url}/api/restaurants/1", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            restaurant = data.get('data', {})
            print(f"   ✅ Individual restaurant endpoint working")
            print(f"   📋 Restaurant: {restaurant.get('name', 'Unknown')}")
        elif response.status_code == 404:
            print("   ⚠️  Restaurant not found (expected if no data)")
        else:
            print(f"   ❌ Individual restaurant endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Individual restaurant endpoint error: {e}")
    
    print("\n" + "=" * 60)
    print("🏁 API testing completed!")
    print("\n💡 If all endpoints show ✅, your database schema fix was successful!")
    print("💡 If you see ❌ errors, the schema fix may still be in progress or there are other issues.")

if __name__ == "__main__":
    test_api_endpoints() 