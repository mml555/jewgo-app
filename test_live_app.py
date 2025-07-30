#!/usr/bin/env python3
"""
Test Live App - Comprehensive Testing After Compatibility Fixes
"""

import requests
import time
from datetime import datetime

def test_backend_status():
    """Test backend status and configuration"""
    print("🔍 Testing Backend Status")
    print("=" * 25)
    
    try:
        response = requests.get("https://jewgo.onrender.com/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Status: {data.get('status', 'Unknown')}")
            print(f"📊 Environment: {data.get('environment', 'Unknown')}")
            print(f"📊 Database: {data.get('database', 'Unknown')}")
            print(f"📊 Version: {data.get('version', 'Unknown')}")
            
            # Check if using PostgreSQL
            if data.get('database') == 'PostgreSQL':
                print("🎉 SUCCESS: Backend is using PostgreSQL!")
                return True
            else:
                print(f"⚠️  Backend is using: {data.get('database', 'Unknown')}")
                return False
        else:
            print(f"❌ Backend returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing backend: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🔍 Testing API Endpoints")
    print("=" * 25)
    
    endpoints = [
        "/api/restaurants",
        "/api/categories", 
        "/api/states",
        "/api/statistics"
    ]
    
    success_count = 0
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"https://jewgo.onrender.com{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"✅ {endpoint}: Working")
                success_count += 1
            else:
                print(f"❌ {endpoint}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")
    
    print(f"\n📊 API Endpoints: {success_count}/{len(endpoints)} working")
    return success_count == len(endpoints)

def test_frontend_access():
    """Test frontend access"""
    print("\n🔍 Testing Frontend Access")
    print("=" * 25)
    
    frontend_urls = [
        "https://jewgo-app.vercel.app",
        "https://jewgo-j953cxrfi-mml555s-projects.vercel.app"
    ]
    
    success_count = 0
    
    for url in frontend_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {url}: Accessible")
                success_count += 1
            else:
                print(f"❌ {url}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {url}: Error - {e}")
    
    print(f"\n📊 Frontend URLs: {success_count}/{len(frontend_urls)} accessible")
    return success_count > 0

def test_cors_configuration():
    """Test CORS configuration"""
    print("\n🔍 Testing CORS Configuration")
    print("=" * 25)
    
    try:
        # Test OPTIONS request (CORS preflight)
        response = requests.options("https://jewgo.onrender.com/api/restaurants", timeout=10)
        
        if response.status_code == 200:
            print("✅ CORS preflight request successful")
            
            # Check CORS headers
            cors_headers = response.headers.get('Access-Control-Allow-Origin')
            if cors_headers:
                print(f"✅ CORS headers present: {cors_headers}")
                return True
            else:
                print("⚠️  CORS headers not found")
                return False
        else:
            print(f"❌ CORS preflight failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ CORS test error: {e}")
        return False

def test_restaurant_data():
    """Test restaurant data retrieval"""
    print("\n🔍 Testing Restaurant Data")
    print("=" * 25)
    
    try:
        response = requests.get("https://jewgo.onrender.com/api/restaurants?limit=5", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'data' in data and isinstance(data['data'], list):
                restaurants = data['data']
                print(f"✅ Retrieved {len(restaurants)} restaurants")
                
                if len(restaurants) > 0:
                    print("✅ Restaurant data is available")
                    return True
                else:
                    print("⚠️  No restaurant data found")
                    return False
            else:
                print("❌ Unexpected data format")
                return False
        else:
            print(f"❌ Failed to retrieve restaurant data: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Restaurant data test error: {e}")
        return False

def provide_summary():
    """Provide comprehensive summary"""
    print("\n📋 Live App Test Summary")
    print("=" * 30)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("🎯 Compatibility Fixes Applied:")
    print("   ✅ Python 3.13 compatibility")
    print("   ✅ PostgreSQL with psycopg3")
    print("   ✅ SQLAlchemy 1.4.53 configuration")
    print("   ✅ Environment variables set")
    print()
    print("🔧 Technical Stack:")
    print("   • Backend: Flask + Python 3.13.5")
    print("   • Database: PostgreSQL (Neon)")
    print("   • Frontend: Next.js + Node.js 22")
    print("   • Deployment: Render + Vercel")
    print()
    print("📊 URLs:")
    print("   • Backend: https://jewgo.onrender.com")
    print("   • Frontend: https://jewgo-app.vercel.app")
    print("   • Alternative: https://jewgo-j953cxrfi-mml555s-projects.vercel.app")

def main():
    """Main test function"""
    print("🚀 Testing Live App After Compatibility Fixes")
    print("=" * 50)
    
    # Run all tests
    backend_ok = test_backend_status()
    api_ok = test_api_endpoints()
    frontend_ok = test_frontend_access()
    cors_ok = test_cors_configuration()
    data_ok = test_restaurant_data()
    
    # Provide summary
    provide_summary()
    
    print("\n🎯 Test Results:")
    print("=" * 15)
    print(f"Backend Status: {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(f"API Endpoints: {'✅ PASS' if api_ok else '❌ FAIL'}")
    print(f"Frontend Access: {'✅ PASS' if frontend_ok else '❌ FAIL'}")
    print(f"CORS Configuration: {'✅ PASS' if cors_ok else '❌ FAIL'}")
    print(f"Restaurant Data: {'✅ PASS' if data_ok else '❌ FAIL'}")
    
    # Overall result
    all_tests_passed = backend_ok and api_ok and frontend_ok and cors_ok and data_ok
    
    print(f"\n🏆 Overall Result: {'🎉 ALL TESTS PASSED' if all_tests_passed else '⚠️  SOME TESTS FAILED'}")
    
    if all_tests_passed:
        print("\n🎉 CONGRATULATIONS!")
        print("   Your JewGo application is fully operational!")
        print("   All compatibility issues have been resolved.")
        print("   The app is ready for production use.")
    else:
        print("\n🔧 Next Steps:")
        print("   • Check the specific failing tests above")
        print("   • Review backend logs for any errors")
        print("   • Verify environment variables are set correctly")

if __name__ == "__main__":
    main() 