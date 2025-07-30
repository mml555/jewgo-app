#!/usr/bin/env python3
"""
Script to fix CORS headers issue for frontend-backend integration
"""

import os
import subprocess
import requests
import json
import time
from datetime import datetime

# Remote backend URL
REMOTE_BACKEND_URL = "https://jewgo.onrender.com"

def commit_cors_fix():
    """Commit the CORS headers fix"""
    try:
        # Add the updated app.py file
        subprocess.run(['git', 'add', 'app.py'], check=True)
        
        # Commit the changes
        commit_message = f"🔧 Fix CORS headers for all responses - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push to remote
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ CORS headers fix committed and pushed successfully!")
        print(f"📝 Commit: {commit_message}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing changes: {e}")
        return False

def test_cors_headers():
    """Test if the CORS headers are working correctly"""
    print("\n🔄 Testing CORS headers...")
    print("⏳ Waiting for backend to redeploy...")
    
    # Wait for deployment
    time.sleep(60)
    
    try:
        # Test GET request with Origin header
        headers = {
            'Origin': 'https://jewgo-app.vercel.app'
        }
        
        response = requests.get(f"{REMOTE_BACKEND_URL}/api/restaurants", headers=headers, timeout=10)
        
        if response.status_code == 200:
            cors_headers = response.headers
            print("✅ GET request successful!")
            print(f"📋 Access-Control-Allow-Origin: {cors_headers.get('Access-Control-Allow-Origin', 'Not set')}")
            print(f"📋 Access-Control-Allow-Methods: {cors_headers.get('Access-Control-Allow-Methods', 'Not set')}")
            print(f"📋 Access-Control-Allow-Headers: {cors_headers.get('Access-Control-Allow-Headers', 'Not set')}")
            print(f"📋 Access-Control-Allow-Credentials: {cors_headers.get('Access-Control-Allow-Credentials', 'Not set')}")
            
            if cors_headers.get('Access-Control-Allow-Origin') == 'https://jewgo-app.vercel.app':
                print("✅ CORS headers are correctly set!")
                return True
            else:
                print("⚠️  CORS headers not set correctly")
                return False
        else:
            print(f"❌ GET request failed with status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing CORS headers: {e}")
        return False

def test_restaurant_detail():
    """Test restaurant detail endpoint specifically"""
    print("\n🔄 Testing restaurant detail endpoint...")
    
    try:
        headers = {
            'Origin': 'https://jewgo-app.vercel.app'
        }
        
        response = requests.get(f"{REMOTE_BACKEND_URL}/api/restaurants/15", headers=headers, timeout=10)
        
        if response.status_code == 200:
            cors_headers = response.headers
            print("✅ Restaurant detail request successful!")
            print(f"📋 Access-Control-Allow-Origin: {cors_headers.get('Access-Control-Allow-Origin', 'Not set')}")
            
            if cors_headers.get('Access-Control-Allow-Origin') == 'https://jewgo-app.vercel.app':
                print("✅ Restaurant detail CORS headers are correct!")
                return True
            else:
                print("⚠️  Restaurant detail CORS headers not set correctly")
                return False
        else:
            print(f"❌ Restaurant detail request failed with status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing restaurant detail: {e}")
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

def main():
    """Main function to fix CORS headers issue"""
    print("🚀 Fixing CORS Headers Issue")
    print("=" * 50)
    
    # Check current backend status
    if not check_backend_status():
        print("❌ Backend is not responding. Please check deployment status.")
        return
    
    # Commit the CORS fix
    if commit_cors_fix():
        print(f"\n✅ CORS headers fix committed successfully")
        
        # Test the fix
        if test_cors_headers():
            print("\n🎉 CORS headers issue resolved!")
            
            # Test restaurant detail endpoint
            if test_restaurant_detail():
                print("\n🎉 All CORS issues resolved!")
            else:
                print("\n⚠️  Restaurant detail endpoint may still have issues")
        else:
            print("\n⚠️  CORS headers fix may still be deploying...")
            print("   Please wait a few minutes and test again.")
    else:
        print("❌ Failed to commit CORS headers fix")

if __name__ == "__main__":
    main() 