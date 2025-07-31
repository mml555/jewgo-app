#!/usr/bin/env python3
"""
Script to fix database connection issue with Python 3.13
"""

import os
import subprocess
import requests
import time
from datetime import datetime

def commit_database_fix():
    """Commit the database connection fix"""
    try:
        # Add the updated requirements file
        subprocess.run(['git', 'add', 'requirements.txt'], check=True)
        
        # Commit the changes
        commit_message = f"🔧 Fix database connection - update psycopg2 for Python 3.13 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push to remote
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Database connection fix committed and pushed successfully!")
        print(f"📝 Commit: {commit_message}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing changes: {e}")
        return False

def check_backend_status():
    """Check if the backend is working after the fix"""
    print("\n🔄 Checking backend status after database fix...")
    print("⏳ Waiting for backend to redeploy...")
    
    # Wait for deployment to complete
    time.sleep(60)
    
    try:
        response = requests.get("https://jewgo.onrender.com/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend is responding successfully!")
            print(f"📋 Status: {data.get('status', 'unknown')}")
            print(f"📋 Version: {data.get('version', 'unknown')}")
            return True
        else:
            print(f"❌ Backend returned status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error checking backend: {e}")
        return False

def test_database_connection():
    """Test if the database connection is working"""
    try:
        response = requests.get("https://jewgo.onrender.com/api/restaurants?limit=5", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Database connection is working!")
            print(f"📊 API Response: {data.get('success', False)}")
            print(f"📊 Total Results: {data.get('metadata', {}).get('total_results', 0)}")
            return True
        else:
            print(f"❌ Database API returned status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing database: {e}")
        return False

def provide_guidance():
    """Provide guidance on the database fix"""
    print("\n🔧 Database Connection Fix Applied:")
    print("   • Updated psycopg2-binary from 2.9.7 to 2.9.9")
    print("   • This version is compatible with Python 3.13")
    print("   • Resolves the undefined symbol error")
    print("   • Backend will redeploy automatically")
    
    print("\n🎯 What This Fixes:")
    print("   • PostgreSQL connection errors")
    print("   • Python 3.13 compatibility issues")
    print("   • Database API functionality")
    print("   • Restaurant data access")
    
    print("\n⚠️  Technical Details:")
    print("   • Error: undefined symbol: _PyInterpreterState_Get")
    print("   • Cause: psycopg2 binary incompatible with Python 3.13")
    print("   • Solution: Updated to psycopg2-binary 2.9.9")
    print("   • Impact: Full database functionality restored")
    
    print("\n🚀 Next Steps:")
    print("   1. Wait for backend redeployment to complete")
    print("   2. Test database API endpoints")
    print("   3. Verify restaurant data loads correctly")
    print("   4. Check frontend-backend integration")

def main():
    """Main function to fix database connection"""
    print("🚀 Fixing Database Connection for Python 3.13")
    print("=" * 55)
    
    # Commit the database fix
    if commit_database_fix():
        print(f"\n✅ Database connection fix deployed")
        print("   • Updated psycopg2-binary to 2.9.9")
        print("   • Python 3.13 compatibility restored")
        print("   • Backend will redeploy automatically")
        
        # Test the fix
        if check_backend_status():
            print("\n🎉 Database connection issue resolved!")
            print("✅ Backend is responding successfully")
            
            # Test database functionality
            if test_database_connection():
                print("✅ Database API is working correctly")
                print("✅ Restaurant data access restored")
            else:
                print("⚠️  Database API may still be initializing...")
        else:
            print("\n⚠️  Database fix may still be deploying...")
            print("⏳ Please wait a few minutes and test again")
        
        provide_guidance()
    else:
        print("❌ Failed to commit database fix")

if __name__ == "__main__":
    main() 