#!/usr/bin/env python3
"""
Script to populate remote backend using individual restaurant POST requests
"""

import requests
import json
import time

REMOTE_BACKEND_URL = "https://jewgo.onrender.com"

def load_local_data():
    """Load the formatted restaurant data"""
    try:
        with open('formatted_restaurants.json', 'r') as f:
            data = json.load(f)
        return data.get('restaurants', [])
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return []

def add_single_restaurant(restaurant):
    """Add a single restaurant to the remote backend"""
    try:
        response = requests.post(
            f"{REMOTE_BACKEND_URL}/api/admin/restaurants",
            json=restaurant,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ Added: {restaurant.get('name', 'Unknown')}")
                return True
            else:
                print(f"❌ Failed to add {restaurant.get('name', 'Unknown')}: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP {response.status_code} for {restaurant.get('name', 'Unknown')}: {response.text}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Network error for {restaurant.get('name', 'Unknown')}: {e}")
        return False

def main():
    print("🚀 Populating Remote Backend with Individual Requests")
    print("=" * 60)
    
    # Load data
    restaurants = load_local_data()
    if not restaurants:
        print("❌ No restaurant data found")
        return
    
    print(f"📊 Found {len(restaurants)} restaurants to add")
    
    # Test with first restaurant
    print("\n🧪 Testing with first restaurant...")
    test_restaurant = restaurants[0]
    print(f"Testing: {test_restaurant.get('name', 'Unknown')}")
    print(f"Business ID: {test_restaurant.get('business_id', 'Unknown')}")
    
    if add_single_restaurant(test_restaurant):
        print("✅ Test successful! Proceeding with all restaurants...")
        
        # Add all restaurants
        success_count = 0
        for i, restaurant in enumerate(restaurants[1:], 1):  # Skip first one since we already added it
            if add_single_restaurant(restaurant):
                success_count += 1
            
            # Add delay to avoid overwhelming the server
            time.sleep(0.5)
            
            # Progress update every 10 restaurants
            if i % 10 == 0:
                print(f"📈 Progress: {i}/{len(restaurants)-1} completed")
        
        print(f"\n🎉 Population complete!")
        print(f"✅ Successfully added: {success_count + 1} restaurants")  # +1 for the test restaurant
        print(f"❌ Failed: {len(restaurants) - success_count - 1} restaurants")
        
    else:
        print("❌ Test failed. Stopping to avoid wasting time.")
        print("💡 Check the error message above to understand the issue.")

if __name__ == "__main__":
    main() 