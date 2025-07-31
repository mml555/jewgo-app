#!/usr/bin/env python3
"""
Test Production API
==================

This script tests the production API to verify that the database schema fix
resolved the "column restaurants.rating does not exist" error.

Author: JewGo Development Team
Version: 1.0
"""

import requests
import json
import sys

def test_production_api():
    """Test the production API endpoints."""
    
    base_url = "https://jewgo.onrender.com"
    
    print("🔍 Testing Production API")
    print("=" * 30)
    print(f"Base URL: {base_url}")
    print()
    
    # Test endpoints
    endpoints = [
        "/api/restaurants",
        "/api/restaurants?limit=10",
        "/api/restaurants?limit=5&offset=0"
    ]
    
    for endpoint in endpoints:
        url = base_url + endpoint
        print(f"Testing: {endpoint}")
        
        try:
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"✅ Success: {len(data)} restaurants returned")
                    if data:
                        print(f"   First restaurant: {data[0].get('name', 'Unknown')}")
                else:
                    print(f"✅ Success: API responded with data")
                    print(f"   Response type: {type(data)}")
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        
        print()

def test_health_endpoint():
    """Test the health check endpoint."""
    
    base_url = "https://jewgo.onrender.com"
    url = base_url + "/health"
    
    print("🏥 Testing Health Endpoint")
    print("=" * 30)
    print(f"URL: {url}")
    print()
    
    try:
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            print("✅ Health check passed")
            try:
                data = response.json()
                print(f"   Status: {data.get('status', 'Unknown')}")
                print(f"   Timestamp: {data.get('timestamp', 'Unknown')}")
            except:
                print(f"   Response: {response.text}")
        else:
            print(f"❌ Health check failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check request failed: {e}")

if __name__ == "__main__":
    test_health_endpoint()
    print()
    test_production_api()
    
    print("🎉 Production API testing completed!") 