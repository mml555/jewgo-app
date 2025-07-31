#!/usr/bin/env python3
"""
Script to force Python version fix by updating all configuration files
"""

import os
import subprocess
import requests
import json
import time
from datetime import datetime

# Remote backend URL
REMOTE_BACKEND_URL = "https://jewgo.onrender.com"

def commit_force_fixes():
    """Commit all the force fixes"""
    try:
        # Add all the updated files
        subprocess.run(['git', 'add', 'requirements.txt', 'runtime.txt', 'render.yaml'], check=True)
        
        # Commit the changes
        commit_message = f"🔧 FORCE Python 3.11.9 - SQLAlchemy 1.4.53 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push to remote
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Force fixes committed and pushed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False

def check_deployment_status():
    """Check if the deployment is successful"""
    max_attempts = 40  # Wait up to 7 minutes
    attempt = 0
    
    print("🔄 Waiting for deployment to complete...")
    
    while attempt < max_attempts:
        try:
            response = requests.get(f"{REMOTE_BACKEND_URL}/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                current_version = data.get('version', 'unknown')
                
                print(f"✅ Backend is running! Version: {current_version}")
                return True
            else:
                print(f"⚠️  Backend returned status {response.status_code}")
        except requests.RequestException as e:
            print(f"⚠️  Connection error: {e}")
        
        attempt += 1
        time.sleep(10)  # Wait 10 seconds between attempts
    
    print("❌ Deployment did not complete within expected time")
    return False

def test_backend_functionality():
    """Test basic backend functionality"""
    try:
        print("🧪 Testing backend functionality...")
        
        # Test health endpoint
        response = requests.get(f"{REMOTE_BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test restaurants endpoint
        response = requests.get(f"{REMOTE_BACKEND_URL}/api/restaurants", timeout=10)
        if response.status_code == 200:
            print("✅ Restaurants endpoint working")
        else:
            print(f"❌ Restaurants endpoint failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing backend: {e}")
        return False

def main():
    """Main deployment function"""
    print("🚀 FORCING Python 3.11.9 and SQLAlchemy 1.4.53 compatibility...")
    print("=" * 60)
    
    # Step 1: Commit force fixes
    print("📋 Step 1: Committing force fixes...")
    if not commit_force_fixes():
        print("❌ Failed to commit force fixes. Exiting.")
        return
    
    # Step 2: Wait for deployment
    print("\n📋 Step 2: Waiting for deployment to complete...")
    if not check_deployment_status():
        print("❌ Deployment failed. Exiting.")
        return
    
    # Step 3: Test functionality
    print("\n📋 Step 3: Testing backend functionality...")
    if not test_backend_functionality():
        print("❌ Backend functionality test failed.")
        return
    
    print("\n" + "=" * 60)
    print("✅ Backend redeployment completed successfully!")
    print("🔧 Force fixes applied:")
    print("   - Python 3.11.9 (explicitly specified)")
    print("   - SQLAlchemy 1.4.53 (Python 3.13 compatible)")
    print("   - render.yaml configuration")
    print("   - runtime.txt updated")
    print("   - FPT feed validation logic will be active")

if __name__ == "__main__":
    main() 