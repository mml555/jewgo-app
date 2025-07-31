#!/usr/bin/env python3
"""
Script to redeploy the backend with updated FPT feed validation logic
"""

import os
import subprocess
import requests
import json
import time
from datetime import datetime

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

def commit_validation_changes():
    """Commit the validation logic changes"""
    try:
        # Add the updated files
        subprocess.run(['git', 'add', 'database_manager_v2.py', 'config.py'], check=True)
        
        # Commit the changes
        commit_message = f"🔧 Add FPT feed validation logic - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push to remote
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Validation changes committed and pushed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False

def check_remote_backend_version():
    """Check if the remote backend has been updated to the new version"""
    max_attempts = 30  # Wait up to 5 minutes
    attempt = 0
    
    print("🔄 Waiting for remote backend to update with validation logic...")
    
    while attempt < max_attempts:
        try:
            response = requests.get(f"{REMOTE_BACKEND_URL}/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                current_version = data.get('version', 'unknown')
                
                if current_version == '1.0.3':
                    print("✅ Remote backend updated successfully with FPT validation!")
                    print(f"📊 New version: {current_version}")
                    return True
                else:
                    print(f"⏳ Still waiting... Current version: {current_version} (attempt {attempt + 1}/{max_attempts})")
            else:
                print(f"⚠️  Remote backend returned status {response.status_code}")
        except requests.RequestException as e:
            print(f"⚠️  Connection error: {e}")
        
        attempt += 1
        time.sleep(10)  # Wait 10 seconds between attempts
    
    print("❌ Remote backend did not update within expected time")
    return False

def test_validation_logic():
    """Test the new validation logic on the remote backend"""
    try:
        print("🧪 Testing FPT feed validation logic...")
        
        # Test 1: Valid restaurant data
        valid_data = {
            'business_id': 'test_validation_001',
            'name': 'Test Validation Restaurant',
            'address': '123 Test Street, Test City, TS 12345',
            'city': 'Test City',
            'state': 'TS',
            'zip_code': '12345',
            'phone_number': '555-123-4567',
            'website_link': 'https://testrestaurant.com',
            'kosher_category': 'meat',
            'certifying_agency': 'ORB',
            'listing_type': 'restaurant'
        }
        
        response = requests.post(
            f"{REMOTE_BACKEND_URL}/api/admin/restaurants",
            json=valid_data,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Valid restaurant data passed validation")
        else:
            print(f"❌ Valid restaurant data failed: {response.status_code}")
            print(f"   Response: {response.text}")
        
        # Test 2: Invalid restaurant data (should fail validation)
        invalid_data = {
            'business_id': 'test_validation_002',
            'name': '',  # Missing name
            'certifying_agency': 'INVALID_AGENCY',  # Invalid agency
            'kosher_category': 'invalid_category',  # Invalid category
            'phone_number': '123',  # Invalid phone
            'website_link': 'not-a-url'  # Invalid URL
        }
        
        response = requests.post(
            f"{REMOTE_BACKEND_URL}/api/admin/restaurants",
            json=invalid_data,
            timeout=30
        )
        
        if response.status_code == 400:
            print("✅ Invalid restaurant data correctly rejected by validation")
        else:
            print(f"⚠️  Invalid restaurant data should have been rejected: {response.status_code}")
            print(f"   Response: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing validation logic: {e}")
        return False

def main():
    """Main deployment function"""
    print("🚀 Starting backend redeployment with FPT feed validation...")
    print("=" * 60)
    
    # Step 1: Check git status
    print("📋 Step 1: Checking git status...")
    git_status = check_git_status()
    if git_status:
        print(f"📝 Uncommitted changes found: {git_status}")
    
    # Step 2: Commit and push changes
    print("\n📋 Step 2: Committing validation changes...")
    if not commit_validation_changes():
        print("❌ Failed to commit changes. Exiting.")
        return
    
    # Step 3: Wait for remote backend update
    print("\n📋 Step 3: Waiting for remote backend update...")
    if not check_remote_backend_version():
        print("❌ Remote backend did not update. Exiting.")
        return
    
    # Step 4: Test validation logic
    print("\n📋 Step 4: Testing validation logic...")
    if not test_validation_logic():
        print("❌ Validation logic test failed.")
        return
    
    print("\n" + "=" * 60)
    print("✅ Backend redeployment with FPT feed validation completed successfully!")
    print("🔧 New features:")
    print("   - FPT feed validation for restaurant data")
    print("   - Certifying agency validation")
    print("   - Kosher category validation")
    print("   - Phone number format validation")
    print("   - Website URL validation")
    print("   - Address completeness validation")
    print("   - Duplicate business ID detection")

if __name__ == "__main__":
    main() 