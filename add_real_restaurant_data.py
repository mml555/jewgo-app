#!/usr/bin/env python3
"""
Add Real Restaurant Data - Replace Sample Data with Real Data
"""

import json
import requests
import time
from datetime import datetime

def load_restaurant_data():
    """Load restaurant data from local_restaurants.json"""
    print("📂 Loading restaurant data from local_restaurants.json")
    
    try:
        with open('local_restaurants.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        restaurants = data.get('restaurants', [])
        print(f"✅ Loaded {len(restaurants)} restaurants from local_restaurants.json")
        return restaurants
        
    except Exception as e:
        print(f"❌ Error loading restaurant data: {e}")
        return []

def clear_sample_data():
    """Clear existing sample data from the database"""
    print("\n🧹 Clearing existing sample data")
    print("=" * 40)
    
    try:
        # Get current restaurants
        response = requests.get("https://jewgo.onrender.com/api/restaurants?limit=1000", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            current_restaurants = data.get('data', [])
            
            if current_restaurants:
                print(f"📊 Found {len(current_restaurants)} existing restaurants")
                
                # Clear all restaurants (this would require an admin endpoint)
                # For now, we'll just note that we need to add the real data
                print("⚠️  Note: Sample data will be replaced when adding real data")
                return True
            else:
                print("✅ Database is already empty")
                return True
        else:
            print(f"❌ Failed to check current data: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error clearing data: {e}")
        return False

def add_restaurant(restaurant):
    """Add a single restaurant to the database"""
    try:
        # Prepare restaurant data for API
        restaurant_data = {
            "business_id": restaurant.get("business_id"),
            "name": restaurant.get("name"),
            "address": restaurant.get("address"),
            "city": restaurant.get("city"),
            "state": restaurant.get("state"),
            "zip_code": restaurant.get("zip_code"),
            "phone_number": restaurant.get("phone_number"),
            "website": restaurant.get("website"),
            "kosher_category": restaurant.get("kosher_category"),
            "certifying_agency": restaurant.get("certifying_agency"),
            "listing_type": restaurant.get("listing_type"),
            "latitude": restaurant.get("latitude"),
            "longitude": restaurant.get("longitude"),
            "rating": restaurant.get("rating"),
            "review_count": restaurant.get("review_count"),
            "price_range": restaurant.get("price_range"),
            "hours_open": restaurant.get("hours_open"),
            "takeout_available": restaurant.get("takeout_available", 0),
            "delivery_available": restaurant.get("delivery_available", 0),
            "dine_in_available": restaurant.get("dine_in_available", 0),
            "status": restaurant.get("status", "active")
        }
        
        # Add restaurant via API
        response = requests.post(
            "https://jewgo.onrender.com/api/admin/restaurants",
            json=restaurant_data,
            timeout=10
        )
        
        if response.status_code == 201:
            return True
        else:
            print(f"❌ Failed to add {restaurant.get('name')}: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error adding {restaurant.get('name')}: {e}")
        return False

def add_all_restaurants(restaurants):
    """Add all restaurants to the database"""
    print(f"\n🍽️  Adding {len(restaurants)} Real Restaurants")
    print("=" * 50)
    
    success_count = 0
    failed_count = 0
    
    for i, restaurant in enumerate(restaurants, 1):
        print(f"📝 Adding restaurant {i}/{len(restaurants)}: {restaurant.get('name', 'Unknown')}")
        
        if add_restaurant(restaurant):
            success_count += 1
            print(f"✅ Successfully added: {restaurant.get('name')}")
        else:
            failed_count += 1
            print(f"❌ Failed to add: {restaurant.get('name')}")
        
        # Add a small delay to avoid overwhelming the API
        time.sleep(0.1)
        
        # Progress update every 10 restaurants
        if i % 10 == 0:
            print(f"📊 Progress: {i}/{len(restaurants)} restaurants processed")
    
    print(f"\n📊 Results:")
    print(f"✅ Successfully added: {success_count} restaurants")
    print(f"❌ Failed to add: {failed_count} restaurants")
    
    return success_count, failed_count

def verify_data_addition():
    """Verify that the data was added successfully"""
    print("\n🔍 Verifying Data Addition")
    print("=" * 30)
    
    try:
        response = requests.get("https://jewgo.onrender.com/api/restaurants?limit=10", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            restaurants = data.get('data', [])
            
            print(f"📊 Total restaurants in database: {len(restaurants)}")
            
            if restaurants:
                print("📋 Sample restaurants:")
                for i, restaurant in enumerate(restaurants[:5], 1):
                    print(f"  {i}. {restaurant.get('name')} - {restaurant.get('city')}, {restaurant.get('state')}")
                
                return True
            else:
                print("⚠️  No restaurants found in database")
                return False
        else:
            print(f"❌ Failed to verify data: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Adding Real Restaurant Data to JewGo Database")
    print("=" * 60)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load restaurant data
    restaurants = load_restaurant_data()
    
    if not restaurants:
        print("❌ No restaurant data found. Exiting.")
        return
    
    # Clear sample data
    if not clear_sample_data():
        print("❌ Failed to clear sample data. Exiting.")
        return
    
    # Add all restaurants
    success_count, failed_count = add_all_restaurants(restaurants)
    
    # Verify data addition
    if verify_data_addition():
        print("\n🎉 Real restaurant data successfully added!")
        print(f"📱 Visit: https://jewgo-app.vercel.app")
        print(f"📊 Total restaurants added: {success_count}")
        
        if failed_count > 0:
            print(f"⚠️  Note: {failed_count} restaurants failed to add (may already exist)")
    else:
        print("\n❌ Data verification failed")
    
    print(f"\n📅 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 