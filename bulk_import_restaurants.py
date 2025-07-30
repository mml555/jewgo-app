#!/usr/bin/env python3
"""
Bulk Import Restaurants - Use bulk import endpoint to add all restaurants at once
"""

import json
import requests
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

def prepare_restaurants_for_bulk_import(restaurants):
    """Prepare restaurant data for bulk import"""
    print("🔧 Preparing restaurants for bulk import")
    
    bulk_data = []
    
    for restaurant in restaurants:
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
        
        bulk_data.append(restaurant_data)
    
    print(f"✅ Prepared {len(bulk_data)} restaurants for bulk import")
    return bulk_data

def bulk_import_restaurants(restaurants_data):
    """Import all restaurants using bulk import endpoint"""
    print(f"\n🚀 Bulk Importing {len(restaurants_data)} Restaurants")
    print("=" * 50)
    
    try:
        # Use bulk import endpoint
        response = requests.post(
            "https://jewgo.onrender.com/api/admin/restaurants/bulk",
            json={"restaurants": restaurants_data},
            timeout=60  # Longer timeout for bulk operation
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Bulk import successful!")
            print(f"📊 Added: {result.get('added', 0)} restaurants")
            print(f"📊 Updated: {result.get('updated', 0)} restaurants")
            print(f"📊 Failed: {result.get('failed', 0)} restaurants")
            return True
        else:
            print(f"❌ Bulk import failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during bulk import: {e}")
        return False

def verify_bulk_import():
    """Verify that the bulk import was successful"""
    print("\n🔍 Verifying Bulk Import")
    print("=" * 30)
    
    try:
        response = requests.get("https://jewgo.onrender.com/api/restaurants?limit=20", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            restaurants = data.get('data', [])
            
            print(f"📊 Total restaurants in database: {len(restaurants)}")
            
            if restaurants:
                print("📋 Sample restaurants:")
                for i, restaurant in enumerate(restaurants[:10], 1):
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
    print("🚀 Bulk Importing Real Restaurant Data to JewGo Database")
    print("=" * 60)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load restaurant data
    restaurants = load_restaurant_data()
    
    if not restaurants:
        print("❌ No restaurant data found. Exiting.")
        return
    
    # Prepare restaurants for bulk import
    bulk_data = prepare_restaurants_for_bulk_import(restaurants)
    
    if not bulk_data:
        print("❌ Failed to prepare restaurant data. Exiting.")
        return
    
    # Perform bulk import
    if bulk_import_restaurants(bulk_data):
        print("\n🎉 Bulk import completed!")
        
        # Verify the import
        if verify_bulk_import():
            print("\n✅ Bulk import verification successful!")
            print(f"📱 Visit: https://jewgo-app.vercel.app")
        else:
            print("\n⚠️  Bulk import verification failed")
    else:
        print("\n❌ Bulk import failed")
    
    print(f"\n📅 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 