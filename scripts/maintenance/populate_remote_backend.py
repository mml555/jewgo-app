#!/usr/bin/env python3
"""
Script to populate the remote backend with restaurant data
Supports both POST endpoint and fallback database direct access
"""

import json
import requests
import time
import sqlite3
import os
from datetime import datetime

# Remote backend URL
REMOTE_BACKEND_URL = "https://jewgo.onrender.com"

def load_local_data():
    """Load restaurant data from local JSON file"""
    try:
        with open('local_restaurants.json', 'r') as f:
            data = json.load(f)
            return data.get('restaurants', [])
    except FileNotFoundError:
        print("❌ local_restaurants.json not found!")
        return []
    except json.JSONDecodeError:
        print("❌ Invalid JSON in local_restaurants.json!")
        return []

def check_remote_backend():
    """Check if remote backend is accessible"""
    try:
        response = requests.get(f"{REMOTE_BACKEND_URL}/", timeout=10)
        if response.status_code == 200:
            print("✅ Remote backend is accessible")
            data = response.json()
            if 'endpoints' in data and 'admin' in data['endpoints']:
                print("✅ Bulk import endpoint available")
                return True
            else:
                print("⚠️  Bulk import endpoint not available")
                return False
        else:
            print(f"❌ Remote backend returned status {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ Cannot connect to remote backend: {e}")
        return False

def get_remote_restaurants():
    """Get current restaurants from remote backend"""
    try:
        response = requests.get(f"{REMOTE_BACKEND_URL}/api/restaurants", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('restaurants', [])
        else:
            print(f"❌ Failed to get remote restaurants: {response.status_code}")
            return []
    except requests.RequestException as e:
        print(f"❌ Error getting remote restaurants: {e}")
        return []

def populate_via_api(restaurants):
    """Populate remote backend using the bulk import API endpoint"""
    print(f"🚀 Attempting to populate via API endpoint...")
    
    try:
        # Prepare the data
        payload = {
            'restaurants': restaurants
        }
        
        # Make the request
        response = requests.post(
            f"{REMOTE_BACKEND_URL}/api/admin/restaurants/bulk",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ API Population Successful!")
                print(f"   📊 Success: {result.get('success_count', 0)}")
                print(f"   ❌ Errors: {result.get('error_count', 0)}")
                if result.get('errors'):
                    print(f"   📝 First few errors:")
                    for error in result['errors'][:3]:
                        print(f"      - {error}")
                return True
            else:
                print(f"❌ API Population Failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ API request failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ API request error: {e}")
        return False

def get_local_database_path():
    """Find the local SQLite database file"""
    possible_paths = [
        'restaurants.db',
        'database.db',
        'jewgo.db',
        'data/restaurants.db',
        'app/restaurants.db'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # Try to find any .db file
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.db'):
                return os.path.join(root, file)
    
    return None

def populate_via_database_direct(restaurants):
    """Fallback: Populate remote database directly (requires database access)"""
    print(f"🔄 Attempting direct database access...")
    
    # This is a fallback method that would require:
    # 1. Database credentials for the remote database
    # 2. Direct database connection (PostgreSQL, MySQL, etc.)
    # 3. Proper database schema knowledge
    
    print("⚠️  Direct database access requires:")
    print("   1. Remote database credentials")
    print("   2. Database connection details")
    print("   3. Proper database schema")
    print("   4. Network access to the database")
    
    # For now, we'll just show what would be needed
    print("\n📋 To implement direct database access:")
    print("   - Get database URL from remote backend")
    print("   - Use psycopg2 for PostgreSQL or similar")
    print("   - Insert restaurants directly into database")
    
    return False

def main():
    print("🚀 Starting remote backend population...")
    print("=" * 50)
    
    # Check remote backend
    if not check_remote_backend():
        print("\n❌ Cannot proceed - remote backend not accessible")
        return
    
    # Load local data
    local_restaurants = load_local_data()
    if not local_restaurants:
        print("❌ No local restaurant data found!")
        return
    
    print(f"📊 Found {len(local_restaurants)} local restaurants")
    
    # Check remote data
    remote_restaurants = get_remote_restaurants()
    print(f"📊 Remote backend has {len(remote_restaurants)} restaurants")
    
    if len(remote_restaurants) > 0:
        print("⚠️  Remote backend already has data!")
        response = input("   Do you want to continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("   Aborting...")
            return
    
    print("\n" + "=" * 50)
    print("🔄 Starting population process...")
    
    # Method 1: Try API endpoint first
    print("\n📡 Method 1: API Endpoint")
    if populate_via_api(local_restaurants):
        print("✅ Population completed successfully via API!")
        return
    
    # Method 2: Fallback to direct database access
    print("\n🗄️  Method 2: Direct Database Access")
    if populate_via_database_direct(local_restaurants):
        print("✅ Population completed successfully via direct database access!")
        return
    
    print("\n❌ All population methods failed!")
    print("\n📋 Manual Steps Required:")
    print("1. Access the remote backend's database directly")
    print("2. Import the restaurant data manually")
    print("3. Or contact the backend administrator")
    print(f"4. Or use the local data file: {os.path.abspath('local_restaurants.json')}")

if __name__ == "__main__":
    main() 