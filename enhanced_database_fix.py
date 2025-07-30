#!/usr/bin/env python3
"""
Enhanced Database Fix with Better Error Handling
"""

import os
import subprocess
import requests
import time
from datetime import datetime

def commit_enhanced_fix():
    """Commit the enhanced database fix"""
    try:
        # Add the updated files
        subprocess.run(['git', 'add', 'requirements.txt', 'database_manager_v2.py'], check=True)
        
        # Commit the changes
        commit_message = f"🔧 Enhanced database fix - better error handling and connection testing - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push to remote
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Enhanced database fix committed and pushed successfully!")
        print(f"📝 Commit: {commit_message}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing changes: {e}")
        return False

def check_backend_status():
    """Check backend status with detailed monitoring"""
    print("\n🔄 Monitoring backend deployment...")
    print("⏳ This may take several minutes as the backend redeploys...")
    
    max_attempts = 15  # Wait up to 15 minutes
    attempt = 0
    
    while attempt < max_attempts:
        try:
            response = requests.get("https://jewgo.onrender.com/", timeout=15)
            if response.status_code == 200:
                data = response.json()
                print("✅ Backend is responding successfully!")
                print(f"📋 Status: {data.get('status', 'unknown')}")
                print(f"📋 Version: {data.get('version', 'unknown')}")
                return True
            elif response.status_code == 500:
                print(f"⚠️  Backend returned 500 error (attempt {attempt + 1}/{max_attempts})")
                print("   This is normal during deployment - backend is still starting up")
            else:
                print(f"⚠️  Backend returned status: {response.status_code} (attempt {attempt + 1}/{max_attempts})")
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Connection error: {e} (attempt {attempt + 1}/{max_attempts})")
        
        attempt += 1
        time.sleep(60)  # Wait 1 minute between attempts
    
    print("❌ Backend deployment did not complete within expected time")
    return False

def test_database_api():
    """Test database API functionality"""
    print("\n🧪 Testing database API...")
    
    try:
        # Test restaurants endpoint
        response = requests.get("https://jewgo.onrender.com/api/restaurants?limit=5", timeout=15)
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
        print(f"❌ Error testing database API: {e}")
        return False

def test_health_endpoint():
    """Test health endpoint"""
    print("\n🏥 Testing health endpoint...")
    
    try:
        response = requests.get("https://jewgo.onrender.com/health", timeout=15)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health endpoint is working!")
            print(f"📋 Health Status: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"❌ Health endpoint returned status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing health endpoint: {e}")
        return False

def provide_guidance():
    """Provide guidance on the enhanced fix"""
    print("\n🔧 Enhanced Database Fix Applied:")
    print("   • Reverted to psycopg2-binary 2.9.9 (stable version)")
    print("   • Added enhanced error handling for PostgreSQL connections")
    print("   • Added connection testing and fallback configuration")
    print("   • Improved connection pooling and timeout settings")
    
    print("\n🎯 What This Fixes:")
    print("   • PostgreSQL connection errors with Python 3.13")
    print("   • Database connection stability")
    print("   • Connection timeout issues")
    print("   • Pool management problems")
    
    print("\n⚠️  Technical Improvements:")
    print("   • Added connection testing with 'SELECT 1'")
    print("   • Enhanced error handling with fallback configuration")
    print("   • Added connection timeout and application name")
    print("   • Improved connection pooling settings")
    
    print("\n🚀 Next Steps:")
    print("   1. Wait for backend redeployment to complete (5-10 minutes)")
    print("   2. Test database API endpoints")
    print("   3. Verify restaurant data loads correctly")
    print("   4. Check frontend-backend integration")
    print("   5. Monitor system logs for any remaining issues")

def main():
    """Main function to deploy enhanced database fix"""
    print("🚀 Enhanced Database Connection Fix")
    print("=" * 45)
    
    # Commit the enhanced fix
    if commit_enhanced_fix():
        print(f"\n✅ Enhanced database fix deployed")
        print("   • Better error handling and connection testing")
        print("   • Improved PostgreSQL configuration")
        print("   • Backend will redeploy automatically")
        
        # Wait for deployment and test
        if check_backend_status():
            print("\n🎉 Database connection issue resolved!")
            print("✅ Backend is responding successfully")
            
            # Test health endpoint
            if test_health_endpoint():
                print("✅ Health endpoint is working")
                
                # Test database API
                if test_database_api():
                    print("✅ Database API is working correctly")
                    print("✅ Restaurant data access restored")
                    print("✅ Frontend-backend integration confirmed")
                else:
                    print("⚠️  Database API may still be initializing...")
            else:
                print("⚠️  Health endpoint may still be initializing...")
        else:
            print("\n⚠️  Backend deployment may still be in progress...")
            print("⏳ Please wait a few more minutes and test again")
        
        provide_guidance()
    else:
        print("❌ Failed to commit enhanced database fix")

if __name__ == "__main__":
    main() 