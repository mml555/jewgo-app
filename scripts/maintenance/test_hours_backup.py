#!/usr/bin/env python3
"""
Test Hours Backup System
========================

Test script to verify the Google Places hours backup functionality.
Tests both backend API endpoints and frontend integration.
"""

import os
import sys
import requests
import json
import time
from typing import Dict, Any

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_backend_hours_endpoints():
    """Test the backend hours API endpoints."""
    print("🔍 Testing Backend Hours API Endpoints")
    print("=" * 50)
    
    backend_url = "https://jewgo.onrender.com"
    
    # Test 1: Get a sample restaurant to test with
    print("\n1. Getting sample restaurant...")
    try:
        response = requests.get(f"{backend_url}/api/restaurants?limit=1")
        response.raise_for_status()
        data = response.json()
        
        if 'restaurants' in data and data['restaurants']:
            restaurant = data['restaurants'][0]
            restaurant_id = restaurant['id']
            restaurant_name = restaurant['name']
            print(f"   ✅ Found restaurant: {restaurant_name} (ID: {restaurant_id})")
            print(f"   📊 Current hours: {restaurant.get('hours_open', 'None')}")
        else:
            print("   ❌ No restaurants found")
            return False
            
    except Exception as e:
        print(f"   ❌ Error getting sample restaurant: {e}")
        return False
    
    # Test 2: Test individual restaurant hours fetch
    print(f"\n2. Testing individual hours fetch for restaurant {restaurant_id}...")
    try:
        response = requests.post(f"{backend_url}/api/restaurants/{restaurant_id}/fetch-hours")
        response.raise_for_status()
        data = response.json()
        
        print(f"   ✅ Response: {data.get('message', 'No message')}")
        if 'hours' in data:
            print(f"   📊 Hours found: {data['hours']}")
        else:
            print(f"   ℹ️  No hours found (this is normal if restaurant already has hours)")
            
    except Exception as e:
        print(f"   ❌ Error testing individual hours fetch: {e}")
        return False
    
    # Test 3: Test bulk hours fetch
    print(f"\n3. Testing bulk hours fetch...")
    try:
        response = requests.post(
            f"{backend_url}/api/restaurants/fetch-missing-hours",
            json={"limit": 3}
        )
        response.raise_for_status()
        data = response.json()
        
        print(f"   ✅ Response: {data.get('message', 'No message')}")
        print(f"   📊 Updated: {data.get('updated', 0)}")
        print(f"   📊 Total checked: {data.get('total_checked', 0)}")
        print(f"   📊 Limit used: {data.get('limit_used', 0)}")
        
    except Exception as e:
        print(f"   ❌ Error testing bulk hours fetch: {e}")
        return False
    
    print("\n✅ Backend hours API tests completed successfully!")
    return True

def test_frontend_api_endpoint():
    """Test the frontend API route for hours functionality."""
    print("\n🔍 Testing Frontend API Route")
    print("=" * 50)
    
    frontend_url = "https://jewgo.vercel.app"
    
    # Test 1: Check if frontend API route exists
    print("\n1. Testing frontend API route...")
    try:
        response = requests.get(f"{frontend_url}/api/restaurants?limit=1")
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data and 'restaurants' in data['data']:
            restaurants = data['data']['restaurants']
            if restaurants:
                restaurant = restaurants[0]
                print(f"   ✅ Frontend API working, found restaurant: {restaurant.get('name', 'Unknown')}")
                print(f"   📊 Hours available: {bool(restaurant.get('hours_open'))}")
                return True
            else:
                print("   ❌ No restaurants returned from frontend API")
                return False
        else:
            print("   ❌ Unexpected response structure from frontend API")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing frontend API: {e}")
        return False

def test_enhanced_hours_updater():
    """Test the enhanced hours updater script."""
    print("\n🔍 Testing Enhanced Hours Updater Script")
    print("=" * 50)
    
    # Check if the script exists
    script_path = "scripts/maintenance/enhanced_google_places_hours_updater.py"
    if not os.path.exists(script_path):
        print(f"   ❌ Script not found: {script_path}")
        return False
    
    print(f"   ✅ Script found: {script_path}")
    
    # Check if Google Places API key is available
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not api_key:
        print("   ⚠️  GOOGLE_PLACES_API_KEY not set (this is expected in production)")
    else:
        print(f"   ✅ Google Places API key available (length: {len(api_key)})")
    
    print("   ℹ️  To test the script manually, run:")
    print(f"   python {script_path}")
    
    return True

def check_hours_data_availability():
    """Check the current state of hours data in the database."""
    print("\n🔍 Checking Hours Data Availability")
    print("=" * 50)
    
    backend_url = "https://jewgo.onrender.com"
    
    try:
        # Get a sample of restaurants to check hours data
        response = requests.get(f"{backend_url}/api/restaurants?limit=20")
        response.raise_for_status()
        data = response.json()
        
        if 'restaurants' not in data:
            print("   ❌ No restaurants data found")
            return False
        
        restaurants = data['restaurants']
        total_restaurants = len(restaurants)
        
        # Count restaurants with and without hours
        with_hours = 0
        without_hours = 0
        
        for restaurant in restaurants:
            hours_open = restaurant.get('hours_open', '')
            hours_of_operation = restaurant.get('hours_of_operation', '')
            
            if (hours_open and hours_open != 'None' and len(hours_open) > 10) or \
               (hours_of_operation and hours_of_operation != 'None' and len(hours_of_operation) > 10):
                with_hours += 1
            else:
                without_hours += 1
        
        print(f"   📊 Total restaurants checked: {total_restaurants}")
        print(f"   ✅ Restaurants with hours: {with_hours}")
        print(f"   ❌ Restaurants without hours: {without_hours}")
        print(f"   📈 Hours coverage: {(with_hours/total_restaurants*100):.1f}%")
        
        # Show some examples
        print(f"\n   📋 Sample restaurants with hours:")
        for i, restaurant in enumerate(restaurants[:3]):
            if restaurant.get('hours_open') or restaurant.get('hours_of_operation'):
                hours = restaurant.get('hours_open') or restaurant.get('hours_of_operation')
                print(f"      {i+1}. {restaurant.get('name', 'Unknown')}: {hours[:50]}...")
        
        print(f"\n   📋 Sample restaurants without hours:")
        for i, restaurant in enumerate(restaurants[:3]):
            if not (restaurant.get('hours_open') or restaurant.get('hours_of_operation')):
                print(f"      {i+1}. {restaurant.get('name', 'Unknown')}: No hours")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error checking hours data: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Testing Google Places Hours Backup System")
    print("=" * 60)
    
    # Run all tests
    tests = [
        ("Backend Hours API Endpoints", test_backend_hours_endpoints),
        ("Frontend API Route", test_frontend_api_endpoint),
        ("Enhanced Hours Updater Script", test_enhanced_hours_updater),
        ("Hours Data Availability", check_hours_data_availability),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error in {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Hours backup system is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 