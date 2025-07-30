#!/usr/bin/env python3
"""
Script to help redeploy the Render backend
"""

import requests
import json
import os
from datetime import datetime

# Render API configuration
RENDER_API_URL = "https://api.render.com/v1"
RENDER_SERVICE_ID = os.environ.get('RENDER_SERVICE_ID')  # You'll need to set this
RENDER_API_KEY = os.environ.get('RENDER_API_KEY')  # You'll need to set this

def check_remote_backend():
    """Check current remote backend status"""
    try:
        response = requests.get("https://jewgo.onrender.com/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Remote backend is accessible")
            print(f"📊 Current endpoints: {list(data.get('endpoints', {}).keys())}")
            
            if 'admin' in data.get('endpoints', {}):
                print("✅ Admin endpoints are available!")
                return True
            else:
                print("❌ Admin endpoints are missing - needs redeploy")
                return False
        else:
            print(f"❌ Remote backend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to remote backend: {e}")
        return False

def trigger_render_redeploy():
    """Trigger a redeploy on Render (requires API credentials)"""
    if not RENDER_SERVICE_ID or not RENDER_API_KEY:
        print("❌ Render API credentials not configured")
        print("📋 To configure:")
        print("   1. Get your Render API key from: https://dashboard.render.com/account/api-keys")
        print("   2. Get your service ID from the Render dashboard")
        print("   3. Set environment variables:")
        print("      export RENDER_API_KEY='your_api_key'")
        print("      export RENDER_SERVICE_ID='your_service_id'")
        return False
    
    try:
        headers = {
            'Authorization': f'Bearer {RENDER_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        # Trigger deploy
        deploy_url = f"{RENDER_API_URL}/services/{RENDER_SERVICE_ID}/deploys"
        response = requests.post(deploy_url, headers=headers, json={})
        
        if response.status_code == 201:
            print("✅ Redeploy triggered successfully!")
            return True
        else:
            print(f"❌ Failed to trigger redeploy: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error triggering redeploy: {e}")
        return False

def wait_for_deployment():
    """Wait for deployment to complete"""
    print("🔄 Waiting for deployment to complete...")
    max_attempts = 30
    attempt = 0
    
    while attempt < max_attempts:
        try:
            response = requests.get("https://jewgo.onrender.com/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'admin' in data.get('endpoints', {}):
                    print("✅ Deployment completed successfully!")
                    print("✅ Admin endpoints are now available!")
                    return True
                else:
                    print(f"⏳ Still waiting... (attempt {attempt + 1}/{max_attempts})")
            else:
                print(f"⚠️  Backend returned status {response.status_code}")
        except Exception as e:
            print(f"⚠️  Connection error: {e}")
        
        attempt += 1
        import time
        time.sleep(20)  # Wait 20 seconds between attempts
    
    print("❌ Deployment did not complete within expected time")
    return False

def main():
    print("🚀 Render Backend Redeploy Helper")
    print("=" * 50)
    
    # Check current status
    print("📋 Checking current remote backend status...")
    if check_remote_backend():
        print("✅ Remote backend is already up to date!")
        return
    
    print("\n🔄 Remote backend needs to be updated")
    print("📋 Options to fix this:")
    print("\n1️⃣  MANUAL REDEPLOY (Recommended):")
    print("   • Go to: https://dashboard.render.com/")
    print("   • Find your backend service")
    print("   • Click 'Manual Deploy' → 'Deploy latest commit'")
    print("   • Wait for deployment to complete")
    
    print("\n2️⃣  API REDEPLOY (Requires setup):")
    response = input("   Try API redeploy? (y/N): ")
    if response.lower() == 'y':
        if trigger_render_redeploy():
            wait_for_deployment()
        else:
            print("❌ API redeploy failed - use manual method")
    
    print("\n3️⃣  VERIFY AFTER REDEPLOY:")
    print("   After redeploy completes, run:")
    print("   curl -s https://jewgo.onrender.com/ | python -m json.tool")
    print("   Look for 'admin' in the endpoints list")

if __name__ == "__main__":
    main() 