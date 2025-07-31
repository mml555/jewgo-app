#!/usr/bin/env python3
"""
Simple script to populate remote backend using individual restaurant additions
"""

import json
import requests
import time

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

def add_single_restaurant(restaurant):
    """Add a single restaurant to the remote backend"""
    try:
        response = requests.post(
            f"{REMOTE_BACKEND_URL}/api/admin/restaurants",
            json=restaurant,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('success', False)
        else:
            print(f"❌ Failed to add {restaurant.get('name', 'Unknown')}: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Error adding {restaurant.get('name', 'Unknown')}: {e}")
        return False

def main():
    print("🚀 Starting simple remote backend population...")
    print("=" * 50)
    
    # Load local data
    local_restaurants = load_local_data()
    if not local_restaurants:
        print("❌ No local restaurant data found!")
        return
    
    print(f"📊 Found {len(local_restaurants)} local restaurants")
    
    # Check remote data
    try:
        response = requests.get(f"{REMOTE_BACKEND_URL}/api/restaurants", timeout=10)
        if response.status_code == 200:
            data = response.json()
            remote_count = len(data.get('restaurants', []))
            print(f"📊 Remote backend has {remote_count} restaurants")
            
            if remote_count > 0:
                print("⚠️  Remote backend already has data!")
                response = input("   Continue anyway? (y/N): ")
                if response.lower() != 'y':
                    print("   Aborting...")
                    return
    except:
        print("⚠️  Could not check remote restaurant count")
    
    print("\n🔄 Starting population...")
    print("   This will add restaurants one by one.")
    print("   It may take a while for large datasets.")
    
    # Start with a small batch for testing
    test_batch = local_restaurants[:10]
    print(f"\n🧪 Testing with first {len(test_batch)} restaurants...")
    
    success_count = 0
    error_count = 0
    
    for i, restaurant in enumerate(test_batch):
        print(f"   Adding {i+1}/{len(test_batch)}: {restaurant.get('name', 'Unknown')}")
        
        if add_single_restaurant(restaurant):
            success_count += 1
            print(f"   ✅ Success")
        else:
            error_count += 1
            print(f"   ❌ Failed")
        
        # Small delay to avoid overwhelming the server
        time.sleep(0.5)
    
    print(f"\n📊 Test Results:")
    print(f"   ✅ Success: {success_count}")
    print(f"   ❌ Errors: {error_count}")
    
    if success_count > 0:
        print("\n🎉 Test successful! Ready to add all restaurants.")
        response = input("   Add all restaurants? (y/N): ")
        
        if response.lower() == 'y':
            print(f"\n🚀 Adding all {len(local_restaurants)} restaurants...")
            
            total_success = 0
            total_errors = 0
            
            for i, restaurant in enumerate(local_restaurants):
                if i % 10 == 0:
                    print(f"   Progress: {i}/{len(local_restaurants)}")
                
                if add_single_restaurant(restaurant):
                    total_success += 1
                else:
                    total_errors += 1
                
                time.sleep(0.5)
            
            print(f"\n🎉 Population completed!")
            print(f"   ✅ Total Success: {total_success}")
            print(f"   ❌ Total Errors: {total_errors}")
        else:
            print("   Skipping full population.")
    else:
        print("❌ Test failed. Cannot proceed with full population.")

if __name__ == "__main__":
    main() 