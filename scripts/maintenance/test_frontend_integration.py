#!/usr/bin/env python3
"""
Test Frontend Integration
========================

This script tests the frontend integration to verify that the API response
format fix is working correctly.

Author: JewGo Development Team
Version: 1.0
"""

import requests
import json

def test_frontend_integration():
    """Test the frontend integration with the backend API."""
    
    print("🔍 Testing Frontend Integration")
    print("=" * 40)
    
    # Test the backend API directly
    backend_url = "https://jewgo.onrender.com/api/restaurants?limit=5"
    print(f"Testing backend API: {backend_url}")
    
    try:
        response = requests.get(backend_url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend API response:")
            print(f"   Type: {type(data)}")
            print(f"   Keys: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
            
            if isinstance(data, dict) and 'restaurants' in data:
                restaurants = data['restaurants']
                print(f"   Restaurants count: {len(restaurants)}")
                print(f"   Total: {data.get('total', 'N/A')}")
                print(f"   Limit: {data.get('limit', 'N/A')}")
                print(f"   Offset: {data.get('offset', 'N/A')}")
                
                if restaurants:
                    print(f"   First restaurant: {restaurants[0].get('name', 'N/A')}")
            else:
                print(f"   ❌ Unexpected response format")
                
        else:
            print(f"❌ Backend API error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Backend API test failed: {e}")
    
    print()
    
    # Test the frontend API route
    frontend_url = "https://jewgo-app.vercel.app/api/restaurants?limit=5"
    print(f"Testing frontend API route: {frontend_url}")
    
    try:
        response = requests.get(frontend_url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Frontend API response:")
            print(f"   Type: {type(data)}")
            print(f"   Keys: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
            
            if isinstance(data, dict):
                if 'data' in data:
                    restaurants = data['data']
                    print(f"   Data count: {len(restaurants) if isinstance(restaurants, list) else 'N/A'}")
                elif 'restaurants' in data:
                    restaurants = data['restaurants']
                    print(f"   Restaurants count: {len(restaurants) if isinstance(restaurants, list) else 'N/A'}")
                else:
                    print(f"   ❌ No restaurants data found")
                    
                print(f"   Success: {data.get('success', 'N/A')}")
                print(f"   Total: {data.get('total', 'N/A')}")
                
        else:
            print(f"❌ Frontend API error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Frontend API test failed: {e}")
    
    print()
    
    # Test the main frontend page
    frontend_page_url = "https://jewgo-app.vercel.app"
    print(f"Testing frontend page: {frontend_page_url}")
    
    try:
        response = requests.get(frontend_page_url, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ Frontend page is accessible")
            print(f"   Content-Type: {response.headers.get('content-type', 'Unknown')}")
            print(f"   Content-Length: {len(response.text)}")
        else:
            print(f"❌ Frontend page error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Frontend page test failed: {e}")

def test_api_response_format():
    """Test the specific API response format that the frontend expects."""
    
    print("\n🔍 Testing API Response Format")
    print("=" * 40)
    
    backend_url = "https://jewgo.onrender.com/api/restaurants?limit=3"
    
    try:
        response = requests.get(backend_url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            print("Backend API Response Structure:")
            print(f"  - Type: {type(data)}")
            
            if isinstance(data, dict):
                print(f"  - Keys: {list(data.keys())}")
                
                if 'restaurants' in data:
                    restaurants = data['restaurants']
                    print(f"  - Restaurants: {len(restaurants)} items")
                    
                    if restaurants:
                        first_restaurant = restaurants[0]
                        print(f"  - First restaurant keys: {list(first_restaurant.keys())}")
                        
                        # Check for required fields
                        required_fields = ['id', 'name', 'address', 'city', 'state']
                        missing_fields = [field for field in required_fields if field not in first_restaurant]
                        
                        if missing_fields:
                            print(f"  - ⚠️  Missing fields: {missing_fields}")
                        else:
                            print(f"  - ✅ All required fields present")
                            
                        print(f"  - Sample data: {first_restaurant.get('name', 'N/A')} in {first_restaurant.get('state', 'N/A')}")
                else:
                    print(f"  - ❌ No 'restaurants' key found")
            else:
                print(f"  - ❌ Response is not a dictionary")
                
        else:
            print(f"❌ API error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_frontend_integration()
    test_api_response_format()
    print("\n🎉 Frontend integration testing completed!") 