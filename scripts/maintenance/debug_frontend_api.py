#!/usr/bin/env python3
"""
Debug Frontend API
================

This script debugs the frontend API route response in detail.

Author: JewGo Development Team
Version: 1.0
"""

import requests
import json

def debug_frontend_api():
    """Debug the frontend API route response."""
    
    frontend_url = "https://jewgo-app.vercel.app/api/restaurants?limit=3"
    
    print("🔍 Debugging Frontend API Route")
    print("=" * 40)
    print(f"URL: {frontend_url}")
    print()
    
    try:
        response = requests.get(frontend_url, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'Unknown')}")
        print()
        
        if response.status_code == 200:
            data = response.json()
            
            print("Frontend API Response Structure:")
            print(f"  - Type: {type(data)}")
            print(f"  - Keys: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
            print()
            
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        print(f"  - Key '{key}': List with {len(value)} items")
                        if value:
                            print(f"    First item type: {type(value[0])}")
                            if isinstance(value[0], dict):
                                print(f"    First item keys: {list(value[0].keys())}")
                                print(f"    Sample: {value[0].get('name', 'N/A')}")
                    else:
                        print(f"  - Key '{key}': {type(value)} = {value}")
            
            print()
            print("📄 Full Response (first 1000 chars):")
            print(json.dumps(data, indent=2)[:1000])
            if len(json.dumps(data, indent=2)) > 1000:
                print("... (truncated)")
                
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        print(f"Response: {response.text[:200]}...")

if __name__ == "__main__":
    debug_frontend_api()
    print("\n🎉 Frontend API debugging completed!") 