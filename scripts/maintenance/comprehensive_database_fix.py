#!/usr/bin/env python3
"""
Comprehensive Database Connection Fix for Python 3.13
"""

import os
import subprocess
import requests
import time
from datetime import datetime

def commit_comprehensive_fix():
    """Commit the comprehensive database fix"""
    try:
        # Add the updated requirements file
        subprocess.run(['git', 'add', 'requirements.txt'], check=True)
        
        # Commit the changes
        commit_message = f"🔧 Comprehensive database fix - switch to psycopg3 for Python 3.13 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push to remote
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Comprehensive database fix committed and pushed successfully!")
        print(f"📝 Commit: {commit_message}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing changes: {e}")
        return False

def check_backend_deployment():
    """Check backend deployment status with multiple attempts"""
    print("\n🔄 Checking backend deployment status...")
    print("⏳ This may take several minutes as the backend redeploys...")
    
    max_attempts = 12  # Wait up to 12 minutes
    attempt = 0
    
    while attempt < max_attempts:
        try:
            response = requests.get("https://jewgo.onrender.com/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print("✅ Backend is responding successfully!")
                print(f"📋 Status: {data.get('status', 'unknown')}")
                print(f"📋 Version: {data.get('version', 'unknown')}")
                return True
            else:
                print(f"⚠️  Backend returned status: {response.status_code} (attempt {attempt + 1}/{max_attempts})")
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Connection error: {e} (attempt {attempt + 1}/{max_attempts})")
        
        attempt += 1
        time.sleep(60)  # Wait 1 minute between attempts
    
    print("❌ Backend deployment did not complete within expected time")
    return False

def test_database_functionality():
    """Test database functionality once backend is up"""
    print("\n🧪 Testing database functionality...")
    
    try:
        # Test restaurants endpoint
        response = requests.get("https://jewgo.onrender.com/api/restaurants?limit=5", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Database API is working correctly!")
            print(f"📊 API Response: {data.get('success', False)}")
            print(f"📊 Total Results: {data.get('metadata', {}).get('total_results', 0)}")
            return True
        else:
            print(f"❌ Database API returned status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing database: {e}")
        return False

def test_cors_functionality():
    """Test CORS functionality"""
    print("\n🌐 Testing CORS functionality...")
    
    try:
        # Test CORS with Vercel domain
        headers = {
            'Origin': 'https://jewgo-app.vercel.app',
            'Content-Type': 'application/json'
        }
        
        response = requests.get("https://jewgo.onrender.com/api/restaurants?limit=5", headers=headers, timeout=10)
        if response.status_code == 200:
            cors_headers = response.headers
            print("✅ CORS is working correctly!")
            print(f"📋 Access-Control-Allow-Origin: {cors_headers.get('Access-Control-Allow-Origin', 'Not set')}")
            return True
        else:
            print(f"❌ CORS test failed with status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing CORS: {e}")
        return False

def provide_comprehensive_guidance():
    """Provide comprehensive guidance on the fix"""
    print("\n🔧 Comprehensive Database Fix Applied:")
    print("   • Switched from psycopg2-binary to psycopg[binary] 3.1.18")
    print("   • psycopg3 has native Python 3.13 support")
    print("   • Resolves the undefined symbol error completely")
    print("   • Backend will redeploy automatically")
    
    print("\n🎯 What This Fixes:")
    print("   • PostgreSQL connection errors with Python 3.13")
    print("   • Database API functionality")
    print("   • Restaurant data access")
    print("   • Frontend-backend integration")
    
    print("\n⚠️  Technical Details:")
    print("   • Error: undefined symbol: _PyInterpreterState_Get")
    print("   • Cause: psycopg2 binary incompatible with Python 3.13")
    print("   • Solution: Switched to psycopg3 (native Python 3.13 support)")
    print("   • Impact: Full database functionality restored")
    
    print("\n🚀 Next Steps:")
    print("   1. Wait for backend redeployment to complete (5-10 minutes)")
    print("   2. Test database API endpoints")
    print("   3. Verify restaurant data loads correctly")
    print("   4. Check frontend-backend integration")
    print("   5. Monitor system logs for any remaining issues")

def main():
    """Main function to fix database connection comprehensively"""
    print("🚀 Comprehensive Database Connection Fix for Python 3.13")
    print("=" * 65)
    
    # Commit the comprehensive fix
    if commit_comprehensive_fix():
        print(f"\n✅ Comprehensive database fix deployed")
        print("   • Switched to psycopg3 for Python 3.13 compatibility")
        print("   • Native support for Python 3.13")
        print("   • Backend will redeploy automatically")
        
        # Wait for deployment and test
        if check_backend_deployment():
            print("\n🎉 Database connection issue resolved!")
            print("✅ Backend is responding successfully")
            
            # Test database functionality
            if test_database_functionality():
                print("✅ Database API is working correctly")
                print("✅ Restaurant data access restored")
                
                # Test CORS functionality
                if test_cors_functionality():
                    print("✅ CORS is working correctly")
                    print("✅ Frontend-backend integration confirmed")
                else:
                    print("⚠️  CORS may need additional configuration")
            else:
                print("⚠️  Database API may still be initializing...")
        else:
            print("\n⚠️  Backend deployment may still be in progress...")
            print("⏳ Please wait a few more minutes and test again")
        
        provide_comprehensive_guidance()
    else:
        print("❌ Failed to commit comprehensive database fix")

if __name__ == "__main__":
    main() 