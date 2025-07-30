#!/usr/bin/env python3
"""
Test monitoring endpoints for JewGo API
"""

import requests
import json
import time
from datetime import datetime

def test_endpoint(url, name, expected_status=200, timeout=30):
    """Test a single endpoint."""
    try:
        start_time = time.time()
        response = requests.get(url, timeout=timeout)
        response_time = (time.time() - start_time) * 1000
        
        status = "✅" if response.status_code == expected_status else "❌"
        
        print(f"{status} {name}")
        print(f"   URL: {url}")
        print(f"   Status: {response.status_code} (expected: {expected_status})")
        print(f"   Response Time: {response_time:.2f}ms")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if name == "Health Check":
                    db_status = data.get('database', {}).get('status', 'unknown')
                    print(f"   Database: {db_status}")
                elif name == "Ping":
                    pong = data.get('pong', False)
                    print(f"   Pong: {pong}")
                elif name == "Restaurants API":
                    success = data.get('success', False)
                    print(f"   Success: {success}")
            except json.JSONDecodeError:
                print(f"   Response: {response.text[:100]}...")
        
        print()
        return response.status_code == expected_status
        
    except requests.exceptions.Timeout:
        print(f"❌ {name} - Timeout after {timeout}s")
        print(f"   URL: {url}")
        print()
        return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {name} - Connection Error")
        print(f"   URL: {url}")
        print()
        return False
    except Exception as e:
        print(f"❌ {name} - Error: {e}")
        print(f"   URL: {url}")
        print()
        return False

def main():
    """Test all monitoring endpoints."""
    print("🧪 Testing JewGo API Monitoring Endpoints")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Get API URL from environment or use default
    import os
    api_url = os.environ.get('API_URL', 'https://jewgo.onrender.com')
    frontend_url = os.environ.get('FRONTEND_URL', 'https://jewgo.com')
    
    endpoints = [
        {
            "url": f"{api_url}/health",
            "name": "Health Check",
            "expected": 200
        },
        {
            "url": f"{api_url}/ping",
            "name": "Ping",
            "expected": 200
        },
        {
            "url": f"{api_url}/api/restaurants?limit=1",
            "name": "Restaurants API",
            "expected": 200
        },
        {
            "url": frontend_url,
            "name": "Frontend",
            "expected": 200
        }
    ]
    
    results = []
    for endpoint in endpoints:
        success = test_endpoint(
            endpoint["url"],
            endpoint["name"],
            endpoint["expected"]
        )
        results.append(success)
    
    # Summary
    print("📊 Summary")
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All endpoints are healthy!")
    else:
        print("⚠️  Some endpoints are failing. Check the details above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 