#!/usr/bin/env python3
"""
Comprehensive API endpoint test script for JewGo backend.
Tests all endpoints to ensure they're working correctly.
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://jewgo.onrender.com"

def test_endpoint(endpoint, method="GET", data=None, params=None):
    """Test a single endpoint and return the result."""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        return {
            'endpoint': endpoint,
            'method': method,
            'status_code': response.status_code,
            'success': response.status_code < 400,
            'response_time': response.elapsed.total_seconds(),
            'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text[:200]
        }
    except Exception as e:
        return {
            'endpoint': endpoint,
            'method': method,
            'status_code': None,
            'success': False,
            'error': str(e),
            'data': None
        }

def main():
    """Run comprehensive API tests."""
    print("🚀 JewGo API Endpoint Test Suite")
    print("=" * 50)
    print(f"Testing against: {BASE_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    # Define test endpoints
    endpoints = [
        # Basic endpoints
        {'endpoint': '/', 'method': 'GET', 'description': 'API Root'},
        {'endpoint': '/health', 'method': 'GET', 'description': 'Health Check'},
        
        # Data endpoints
        {'endpoint': '/api/restaurants', 'method': 'GET', 'description': 'Restaurants List'},
        {'endpoint': '/api/restaurants', 'method': 'GET', 'params': {'limit': 5}, 'description': 'Restaurants with Limit'},
        {'endpoint': '/api/restaurants', 'method': 'GET', 'params': {'category': 'Bakery'}, 'description': 'Restaurants by Category'},
        {'endpoint': '/api/restaurants', 'method': 'GET', 'params': {'query': 'pizza'}, 'description': 'Restaurants Search'},
        
        # Statistics and metadata
        {'endpoint': '/api/statistics', 'method': 'GET', 'description': 'Database Statistics'},
        {'endpoint': '/api/categories', 'method': 'GET', 'description': 'Categories List'},
        {'endpoint': '/api/states', 'method': 'GET', 'description': 'States List'},
        
        # Admin endpoints (read-only tests)
        {'endpoint': '/api/admin/restaurants', 'method': 'GET', 'description': 'Admin Restaurants (should fail)'},
    ]
    
    results = []
    passed = 0
    failed = 0
    
    for test in endpoints:
        print(f"🔍 Testing: {test['description']}")
        print(f"   Endpoint: {test['method']} {test['endpoint']}")
        
        result = test_endpoint(
            test['endpoint'], 
            method=test['method'],
            params=test.get('params')
        )
        
        results.append(result)
        
        if result['success']:
            print(f"   ✅ PASS - Status: {result['status_code']} - Time: {result['response_time']:.2f}s")
            passed += 1
        else:
            print(f"   ❌ FAIL - Status: {result['status_code']} - Error: {result.get('error', 'Unknown')}")
            failed += 1
        
        print()
    
    # Summary
    print("=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    print()
    
    # Detailed results
    print("📋 DETAILED RESULTS")
    print("=" * 50)
    for result in results:
        status_icon = "✅" if result['success'] else "❌"
        print(f"{status_icon} {result['method']} {result['endpoint']}")
        print(f"   Status: {result['status_code']}")
        if result.get('response_time'):
            print(f"   Time: {result['response_time']:.2f}s")
        if result.get('error'):
            print(f"   Error: {result['error']}")
        print()
    
    # Recommendations
    print("💡 RECOMMENDATIONS")
    print("=" * 50)
    if failed == 0:
        print("🎉 All endpoints are working perfectly!")
        print("   The API is ready for production use.")
    else:
        print("⚠️  Some endpoints need attention:")
        for result in results:
            if not result['success']:
                print(f"   - {result['method']} {result['endpoint']}: {result.get('error', 'Unknown error')}")
    
    print()
    print("🏁 Test completed!")

if __name__ == "__main__":
    main() 