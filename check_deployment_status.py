#!/usr/bin/env python3
"""
Check deployment status after psycopg2 compatibility fix.
"""

import requests
import time
import sys
from datetime import datetime

def check_app_health():
    """Check if the application is responding correctly."""
    url = "https://jewgo.onrender.com"
    
    try:
        print(f"🔍 Checking application health at {url}")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Application is responding successfully!")
            print(f"📊 Status Code: {response.status_code}")
            print(f"⏱️  Response Time: {response.elapsed.total_seconds():.2f}s")
            return True
        else:
            print(f"⚠️  Application responded with status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to connect to application: {e}")
        return False

def check_api_endpoints():
    """Check if the API endpoints are working."""
    base_url = "https://jewgo.onrender.com"
    endpoints = [
        "/api/restaurants",
        "/api/restaurants/search",
        "/api/restaurants/stats"
    ]
    
    print("\n🔍 Checking API endpoints...")
    
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
    
    # Wait a bit for deployment to complete
    print("⏳ Waiting for deployment to complete...")
    time.sleep(30)
    
    # Check application health
    if check_app_health():
        print("\n🎉 Application is live and responding!")
        check_api_endpoints()
    else:
        print("\n❌ Application is not responding correctly")
        print("💡 This might indicate:")
        print("   - Deployment is still in progress")
        print("   - There's still an issue with the psycopg2 fix")
        print("   - Database connection issues")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Deployment status check completed!")

if __name__ == "__main__":
    main() 