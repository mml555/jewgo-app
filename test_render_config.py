#!/usr/bin/env python3
"""
Test Render Configuration After Environment Variables Are Set
"""

import requests
import time
from datetime import datetime

def test_backend_database():
    """Test if backend is now using PostgreSQL"""
    print("🔍 Testing Backend Database Configuration")
    print("=" * 45)
    
    try:
        response = requests.get("https://jewgo.onrender.com/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Status: {data.get('status', 'Unknown')}")
            print(f"📊 Environment: {data.get('environment', 'Unknown')}")
            print(f"📊 Database: {data.get('database', 'Unknown')}")
            print(f"📊 Version: {data.get('version', 'Unknown')}")
            
            if data.get('database') == 'PostgreSQL':
                print("\n🎉 SUCCESS: Backend is now using PostgreSQL!")
                return True
            else:
                print(f"\n⚠️  Backend is still using: {data.get('database', 'Unknown')}")
                print("   This means the environment variables may not be set correctly")
                return False
        else:
            print(f"❌ Backend returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing backend: {e}")
        return False

def wait_for_deployment():
    """Wait for Render deployment to complete"""
    print("⏳ Waiting for Render deployment to complete...")
    print("   This may take 2-3 minutes...")
    
    for i in range(30):  # Wait up to 5 minutes
        try:
            response = requests.get("https://jewgo.onrender.com/", timeout=5)
            if response.status_code == 200:
                print("✅ Backend is responding!")
                return True
        except:
            pass
        
        print(f"   Attempt {i+1}/30: Waiting for deployment...")
        time.sleep(10)
    
    print("❌ Backend did not come online within timeout")
    return False

def provide_troubleshooting():
    """Provide troubleshooting steps"""
    print("\n🔧 Troubleshooting Steps")
    print("=" * 25)
    
    print("If the backend is still using SQLite:")
    print()
    print("1. 🔍 Check Environment Variables:")
    print("   • Go to Render dashboard > jewgo-backend > Environment")
    print("   • Verify DATABASE_URL is exactly:")
    print("     postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
    print()
    print("2. 🔄 Force Redeploy:")
    print("   • In Render dashboard, click 'Manual Deploy'")
    print("   • Select 'Deploy latest commit'")
    print()
    print("3. 📋 Check Backend Logs:")
    print("   • In Render dashboard, go to 'Logs' tab")
    print("   • Look for PostgreSQL connection messages")
    print()
    print("4. 🧪 Test Connection:")
    print("   • The render_connection_test.py script is deployed")
    print("   • You can run it to test the PostgreSQL connection")

def main():
    """Main function"""
    print("🚀 Testing Render Database Configuration")
    print("=" * 45)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("📋 Instructions:")
    print("1. Add the DATABASE_URL to Render environment variables")
    print("2. Wait for deployment to complete")
    print("3. Run this script to test the configuration")
    print()
    
    # Wait for deployment
    if wait_for_deployment():
        # Test the database configuration
        success = test_backend_database()
        
        if success:
            print("\n🎉 CONGRATULATIONS!")
            print("   Your PostgreSQL database is now working!")
            print("   The backend is successfully connected to Neon PostgreSQL")
        else:
            print("\n⚠️  Configuration Issue Detected")
            provide_troubleshooting()
    else:
        print("\n❌ Backend Deployment Issue")
        print("   Please check if the environment variables were added correctly")
        print("   and wait for the deployment to complete")

if __name__ == "__main__":
    main() 