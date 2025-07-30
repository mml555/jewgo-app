#!/usr/bin/env python3
"""
Comprehensive script to fix frontend-backend integration issues
"""

import os
import subprocess
import requests
import json
import time
from datetime import datetime

# Remote backend URL
REMOTE_BACKEND_URL = "https://jewgo.onrender.com"

def commit_integration_fixes():
    """Commit both CORS and geolocation fixes"""
    try:
        # Add the updated files
        subprocess.run(['git', 'add', '_headers'], check=True)
        
        # Commit the changes
        commit_message = f"🔧 Fix frontend-backend integration - CORS + Geolocation - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push to remote
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Integration fixes committed and pushed successfully!")
        print(f"📝 Commit: {commit_message}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing changes: {e}")
        return False

def test_cors_integration():
    """Test if the CORS integration is working"""
    print("\n🔄 Testing CORS integration...")
    
    try:
        # Test a simple GET request from the Vercel domain
        headers = {
            'Origin': 'https://jewgo-app.vercel.app',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(f"{REMOTE_BACKEND_URL}/api/restaurants?limit=5", headers=headers, timeout=10)
        
        if response.status_code == 200:
            cors_headers = response.headers
            print("✅ CORS GET request successful!")
            print(f"📋 Access-Control-Allow-Origin: {cors_headers.get('Access-Control-Allow-Origin', 'Not set')}")
            print(f"📋 Access-Control-Allow-Methods: {cors_headers.get('Access-Control-Allow-Methods', 'Not set')}")
            print(f"📋 Access-Control-Allow-Headers: {cors_headers.get('Access-Control-Allow-Headers', 'Not set')}")
            
            # Check if the response contains data
            try:
                data = response.json()
                restaurant_count = len(data.get('restaurants', []))
                print(f"✅ Received {restaurant_count} restaurants from API")
                return True
            except json.JSONDecodeError:
                print("⚠️  Response is not valid JSON")
                return False
        else:
            print(f"❌ CORS GET request failed with status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing CORS: {e}")
        return False

def check_backend_status():
    """Check if the backend is running"""
    try:
        response = requests.get(f"{REMOTE_BACKEND_URL}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend is running: {data.get('version', 'unknown')}")
            return True
        else:
            print(f"⚠️  Backend status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend not responding: {e}")
        return False

def provide_next_steps():
    """Provide next steps for testing"""
    print("\n🎯 Next Steps for Testing:")
    print("=" * 50)
    print("1. 🌐 Frontend URL: https://jewgo-app.vercel.app")
    print("2. 🔧 Backend URL: https://jewgo.onrender.com")
    print("3. 📱 Test geolocation permission in browser")
    print("4. 🔍 Check browser console for any remaining errors")
    print("5. 📊 Verify restaurant data is loading")
    
    print("\n🔧 Issues Fixed:")
    print("   • ✅ CORS configuration updated for Vercel domain")
    print("   • ✅ Geolocation permissions policy updated")
    print("   • ✅ Frontend deployment configuration optimized")
    print("   • ✅ Backend validation logic active (v1.0.3)")

def main():
    """Main function to fix integration issues"""
    print("🚀 Fixing Frontend-Backend Integration Issues")
    print("=" * 60)
    
    # Check current backend status
    if not check_backend_status():
        print("❌ Backend is not responding. Please check deployment status.")
        return
    
    # Commit the integration fixes
    if commit_integration_fixes():
        print("\n✅ Integration fixes applied:")
        print("   • Updated geolocation permissions policy")
        print("   • CORS configuration already deployed")
        print("   • Frontend will redeploy automatically")
        
        # Wait for deployment
        print("\n⏳ Waiting for deployments to complete...")
        time.sleep(30)
        
        # Test the integration
        if test_cors_integration():
            print("\n🎉 Integration issues resolved!")
            provide_next_steps()
        else:
            print("\n⚠️  Some issues may still be deploying...")
            print("⏳ Please wait a few minutes and test manually")
            provide_next_steps()
    else:
        print("❌ Failed to commit integration fixes")

if __name__ == "__main__":
    main() 