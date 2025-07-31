#!/usr/bin/env python3
"""
Debug API Response
================

This script debugs the exact API response format to understand why
the frontend is showing 0 restaurants.

Author: JewGo Development Team
Version: 1.0
"""

import requests
import json

def debug_api_response():
    """Debug the API response format."""
    
    base_url = "https://jewgo.onrender.com"
    url = base_url + "/api/restaurants"
    
    print("🔍 Debugging API Response Format")
    print("=" * 40)
    print(f"URL: {url}")
    print()
    
    try:
        response = requests.get(url, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'Unknown')}")
        print(f"Content-Length: {len(response.text)}")
        print()
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ JSON Response Structure:")
                print(f"Type: {type(data)}")
                print(f"Keys: {list(data.keys()) if isinstance(data, dict) else 'N/A (not a dict)'}")
                print()
                
                if isinstance(data, dict):
                    for key, value in data.items():
                        if isinstance(value, list):
                            print(f"Key '{key}': List with {len(value)} items")
                            if value:
                                print(f"  First item type: {type(value[0])}")
                                print(f"  First item keys: {list(value[0].keys()) if isinstance(value[0], dict) else 'N/A'}")
                        else:
                            print(f"Key '{key}': {type(value)} = {value}")
                elif isinstance(data, list):
                    print(f"Response is a list with {len(data)} items")
                    if data:
                        print(f"First item type: {type(data[0])}")
                        print(f"First item keys: {list(data[0].keys()) if isinstance(data[0], dict) else 'N/A'}")
                
                print()
                print("📄 Full Response (first 1000 chars):")
                print(json.dumps(data, indent=2)[:1000])
                if len(json.dumps(data, indent=2)) > 1000:
                    print("... (truncated)")
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
                print(f"Raw response: {response.text[:500]}...")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

def test_frontend_endpoint():
    """Test the endpoint that the frontend is likely calling."""
    
    base_url = "https://jewgo.onrender.com"
    url = base_url + "/api/restaurants?limit=20&offset=0"
    
    print("\n🔍 Testing Frontend Endpoint")
    print("=" * 40)
    print(f"URL: {url}")
    print()
    
    try:
        response = requests.get(url, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response type: {type(data)}")
            
            if isinstance(data, dict):
                restaurants = data.get('restaurants', [])
                print(f"Restaurants key found: {len(restaurants)} items")
            elif isinstance(data, list):
                restaurants = data
                print(f"Direct list response: {len(restaurants)} items")
            else:
                print(f"Unexpected response type: {type(data)}")
                restaurants = []
            
            print(f"Total restaurants returned: {len(restaurants)}")
            
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    debug_api_response()
    test_frontend_endpoint()
    print("\n🎉 API response debugging completed!") 