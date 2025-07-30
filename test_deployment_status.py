#!/usr/bin/env python3
"""
Test deployment status and diagnose issues.
"""

import requests
import time
from datetime import datetime

def test_app_health():
    """Test if the application is responding."""
    url = "https://jewgo.onrender.com"
    
    try:
        print(f"🔍 Testing application at {url}")
        response = requests.get(url, timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"⏱️  Response Time: {response.elapsed.total_seconds():.2f}s")
        
        if response.status_code == 200:
            print("✅ Application is responding successfully!")
            return True
        else:
            print(f"⚠️  Application responded with status code: {response.status_code}")
            print(f"📄 Response content: {response.text[:200]}...")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to connect to application: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints."""
    base_url = "https://jewgo.onrender.com"
    endpoints = [
        "/api/restaurants",
        "/api/restaurants/search",
        "/api/restaurants/stats"
    ]
    
    print("\n🔍 Testing API endpoints...")
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {endpoint} - OK")
            else:
                print(f"⚠️  {endpoint} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint} - Error: {e}")

def main():
    print(f"🚀 Deployment Status Check - {datetime.now()}")
    print("=" * 50)
    
    # Test application health
    if test_app_health():
        print("\n🎉 Application is live and responding!")
        test_api_endpoints()
    else:
        print("\n❌ Application is not responding correctly")
        print("💡 Possible issues:")
        print("   - Deployment is still in progress")
        print("   - Python 3.11.8 compatibility issue")
        print("   - Database connection issue")
        print("   - SQLAlchemy configuration problem")
    
    print("\n" + "=" * 50)
    print("✅ Status check completed!")

if __name__ == "__main__":
    main() 