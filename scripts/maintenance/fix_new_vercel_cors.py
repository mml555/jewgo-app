#!/usr/bin/env python3
"""
Script to fix CORS for new Vercel domain
"""

import os
import subprocess
import requests
import json
import time
from datetime import datetime

# Remote backend URL
REMOTE_BACKEND_URL = "https://jewgo.onrender.com"
NEW_VERCEL_DOMAIN = "https://jewgo-j953cxrfi-mml555s-projects.vercel.app"

def commit_cors_fix():
    """Commit the CORS configuration fix for new Vercel domain"""
    try:
        # Add the updated config file
        subprocess.run(['git', 'add', 'config.py'], check=True)
        
        # Commit the changes
        commit_message = f"🔧 Fix CORS for new Vercel domain - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push to remote
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ CORS fix for new Vercel domain committed and pushed successfully!")
        print(f"📝 Commit: {commit_message}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing changes: {e}")
        return False

def test_cors_fix():
    """Test if the CORS fix is working for the new domain"""
    print("\n🔄 Testing CORS fix for new Vercel domain...")
    print("⏳ Waiting for backend to redeploy...")
    
    # Wait a bit for the deployment to complete
    time.sleep(30)
    
    try:
        # Test the CORS headers by making a request from the new domain
        headers = {
            'Origin': NEW_VERCEL_DOMAIN,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(f"{REMOTE_BACKEND_URL}/api/restaurants?limit=5", headers=headers, timeout=10)
        
        if response.status_code == 200:
            cors_headers = response.headers
            print("✅ CORS request from new Vercel domain successful!")
            print(f"📋 Access-Control-Allow-Origin: {cors_headers.get('Access-Control-Allow-Origin', 'Not set')}")
            print(f"📋 Access-Control-Allow-Methods: {cors_headers.get('Access-Control-Allow-Methods', 'Not set')}")
            print(f"📋 Access-Control-Allow-Headers: {cors_headers.get('Access-Control-Allow-Headers', 'Not set')}")
            
            if NEW_VERCEL_DOMAIN in cors_headers.get('Access-Control-Allow-Origin', ''):
                print("✅ New Vercel domain is now allowed!")
                return True
            else:
                print("⚠️  New Vercel domain not found in CORS headers")
                return False
        else:
            print(f"❌ CORS request failed with status: {response.status_code}")
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

def provide_guidance():
    """Provide guidance on the CORS fix"""
    print("\n🔧 CORS Configuration Updated:")
    print("   • Added new Vercel domain to allowed origins")
    print("   • Updated both development and production configs")
    print("   • Backend will redeploy automatically")
    
    print(f"\n🌐 New Vercel Domain: {NEW_VERCEL_DOMAIN}")
    print("   • This appears to be a new deployment URL")
    print("   • CORS now configured for this domain")
    print("   • API access should work properly")
    
    print("\n🎯 Next Steps:")
    print("   1. Wait for backend redeployment to complete")
    print("   2. Test the frontend at the new Vercel URL")
    print("   3. Verify restaurant data loads correctly")
    print("   4. Check browser console for any remaining errors")

def main():
    """Main function to fix CORS for new Vercel domain"""
    print("🚀 Fixing CORS for New Vercel Domain")
    print("=" * 50)
    
    # Check current backend status
    if not check_backend_status():
        print("❌ Backend is not responding. Please check deployment status.")
        return
    
    # Commit the CORS fix
    if commit_cors_fix():
        print(f"\n✅ CORS configuration updated for: {NEW_VERCEL_DOMAIN}")
        print("   • Added new Vercel domain to allowed origins")
        print("   • Updated both development and production configs")
        print("   • Backend will redeploy automatically")
        
        # Test the fix
        if test_cors_fix():
            print("\n🎉 CORS issue for new Vercel domain resolved!")
            print("✅ Frontend should now be able to access the backend API")
            print(f"🌐 Test the frontend at: {NEW_VERCEL_DOMAIN}")
        else:
            print("\n⚠️  CORS fix may still be deploying...")
            print("⏳ Please wait a few minutes and test again")
        
        provide_guidance()
    else:
        print("❌ Failed to commit CORS fix")

if __name__ == "__main__":
    main() 