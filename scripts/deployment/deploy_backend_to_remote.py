#!/usr/bin/env python3
"""
Script to deploy the updated backend code to the remote server
"""

import os
import subprocess
import requests
import json
from datetime import datetime
import time

# Remote backend URL
REMOTE_BACKEND_URL = "https://jewgo.onrender.com"

def check_git_status():
    """Check if we have uncommitted changes"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print("❌ Git not available or not a git repository")
        return None

def commit_and_push_changes():
    """Commit and push the backend changes"""
    try:
        # Add the updated app.py
        subprocess.run(['git', 'add', 'app.py'], check=True)
        
        # Commit the changes
        commit_message = f"🔧 Add bulk import endpoint - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push to remote
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Changes committed and pushed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False

def check_remote_backend_update():
    """Check if the remote backend has been updated"""
    max_attempts = 30  # Wait up to 5 minutes
    attempt = 0
    
    print("🔄 Waiting for remote backend to update...")
    
    while attempt < max_attempts:
        try:
            response = requests.get(f"{REMOTE_BACKEND_URL}/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'endpoints' in data and 'admin' in data['endpoints']:
                    print("✅ Remote backend updated successfully!")
                    return True
                else:
                    print(f"⏳ Still waiting... (attempt {attempt + 1}/{max_attempts})")
            else:
                print(f"⚠️  Remote backend returned status {response.status_code}")
        except requests.RequestException as e:
            print(f"⚠️  Connection error: {e}")
        
        attempt += 1
        time.sleep(10)  # Wait 10 seconds between attempts
    
    print("❌ Remote backend did not update within expected time")
    return False

def test_remote_bulk_import():
    """Test the bulk import endpoint on the remote backend"""
    try:
        test_data = {
            'restaurants': [
                {
                    'business_id': 'test_remote_123',
                    'name': 'Test Remote Restaurant',
                    'address': '456 Remote Test St',
                    'city': 'Test City',
                    'state': 'TS',
                    'zip_code': '12345',
                    'phone_number': '555-123-4567',
                    'website': 'https://test.com',
                    'kosher_category': 'meat',
                    'certifying_agency': 'TEST',
                    'listing_type': 'restaurant'
                }
            ]
        }
        
        response = requests.post(
            f"{REMOTE_BACKEND_URL}/api/admin/restaurants/bulk",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Remote bulk import endpoint working!")
                return True
            else:
                print(f"❌ Remote bulk import failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Remote bulk import request failed: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Remote bulk import test error: {e}")
        return False

def main():
    print("🚀 Starting backend deployment to remote...")
    print("=" * 50)
    
    # Check git status
    print("📋 Checking git status...")
    uncommitted = check_git_status()
    if uncommitted:
        print("📝 Found uncommitted changes:")
        print(uncommitted)
        response = input("   Commit and push these changes? (y/N): ")
        if response.lower() == 'y':
            if not commit_and_push_changes():
                print("❌ Failed to commit and push changes")
                return
        else:
            print("❌ Aborting - changes not committed")
            return
    else:
        print("✅ No uncommitted changes found")
    
    # Wait for remote backend to update
    if not check_remote_backend_update():
        print("❌ Remote backend update failed")
        return
    
    # Test the remote bulk import endpoint
    print("\n🧪 Testing remote bulk import endpoint...")
    if not test_remote_bulk_import():
        print("❌ Remote bulk import test failed")
        return
    
    print("\n🎉 Backend deployment successful!")
    print("✅ Remote backend now has bulk import capability")
    print("✅ Ready to populate with restaurant data")

if __name__ == "__main__":
    main() 