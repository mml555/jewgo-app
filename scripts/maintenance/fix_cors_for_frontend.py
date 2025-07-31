#!/usr/bin/env python3
"""
Script to fix CORS issue for frontend deployment
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
    """Commit the CORS configuration fix"""
    try:
        # Add the updated config file
        subprocess.run(['git', 'add', 'config.py'], check=True)
        
        # Commit the changes
        commit_message = f"🔧 Fix CORS for Vercel frontend - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push to remote
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ CORS fix committed and pushed successfully!")
        print(f"📝 Commit: {commit_message}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing changes: {e}")
        return False

def test_cors_fix():
    """Test if the CORS fix is working"""
    print("\n🔄 Testing CORS fix...")
    print("⏳ Waiting for backend to redeploy...")
    
    # Wait a bit for the deployment to complete
    time.sleep(30)
    
    try:
        # Test the CORS headers by making a request
        headers = {
            'Origin': 'https://jewgo-app.vercel.app',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        
        response = requests.options(f"{REMOTE_BACKEND_URL}/api/restaurants", headers=headers, timeout=10)
        
        if response.status_code == 200:
            cors_headers = response.headers
            print("✅ CORS preflight request successful!")
            print(f"📋 Access-Control-Allow-Origin: {cors_headers.get('Access-Control-Allow-Origin', 'Not set')}")
            print(f"📋 Access-Control-Allow-Methods: {cors_headers.get('Access-Control-Allow-Methods', 'Not set')}")
            print(f"📋 Access-Control-Allow-Headers: {cors_headers.get('Access-Control-Allow-Headers', 'Not set')}")
            
            if 'https://jewgo-app.vercel.app' in cors_headers.get('Access-Control-Allow-Origin', ''):
                print("✅ Vercel domain is now allowed!")
                return True
            else:
                print("⚠️  Vercel domain not found in CORS headers")
                return False
        else:
            print(f"❌ CORS preflight failed with status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing CORS: {e}")
        return False

def check_backend_status():
    """Check if the backend is still running"""
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
    """Main function to fix CORS issue"""
    print("🚀 Fixing CORS Issue for Frontend")
    print("=" * 50)
    
    # Check current backend status
    if not check_backend_status():
        print("❌ Backend is not responding. Please check deployment status.")
        return
    
    # Commit the CORS fix
    if commit_cors_fix():
        print("\n✅ CORS configuration updated:")
        print("   • Added https://jewgo-app.vercel.app to allowed origins")
        print("   • Updated both development and production configs")
        print("   • Backend will redeploy automatically")
        
        # Test the fix
        if test_cors_fix():
            print("\n🎉 CORS issue resolved!")
            print("✅ Frontend should now be able to access the backend API")
            print("🌐 Test the frontend at: https://jewgo-app.vercel.app")
        else:
            print("\n⚠️  CORS fix may still be deploying...")
            print("⏳ Please wait a few minutes and test again")
    else:
        print("❌ Failed to commit CORS fix")

if __name__ == "__main__":
    main() 