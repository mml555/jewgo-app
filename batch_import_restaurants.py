#!/usr/bin/env python3
"""
Batch Import Restaurants - Import restaurants in smaller batches
"""

import json
import requests
import time
from datetime import datetime

def load_formatted_restaurant_data():
    """Load restaurant data from formatted_restaurants.json"""
    print("📂 Loading restaurant data from formatted_restaurants.json")
    
    try:
        with open('formatted_restaurants.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        restaurants = data.get('restaurants', [])
        print(f"✅ Loaded {len(restaurants)} restaurants from formatted_restaurants.json")
        return restaurants
        
    except Exception as e:
        print(f"❌ Error loading restaurant data: {e}")
        return []

def import_restaurant_batch(restaurants, batch_size=10):
    """Import restaurants in batches"""
    print(f"\n🚀 Importing {len(restaurants)} Restaurants in Batches of {batch_size}")
    print("=" * 60)
    
    total_success = 0
    total_failed = 0
    
    # Split restaurants into batches
    for i in range(0, len(restaurants), batch_size):
        batch = restaurants[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (len(restaurants) + batch_size - 1) // batch_size
        
        print(f"\n📦 Processing Batch {batch_num}/{total_batches} ({len(batch)} restaurants)")
        
        batch_success = 0
        batch_failed = 0
        
        for restaurant in batch:
            try:
                # Prepare restaurant data
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
                    batch_success += 1
                    print(f"  ✅ {restaurant.get('name')}")
                else:
                    batch_failed += 1
                    print(f"  ❌ {restaurant.get('name')} - Status: {response.status_code}")
                
                # Small delay between requests
                time.sleep(0.2)
                
            except Exception as e:
                batch_failed += 1
                print(f"  ❌ {restaurant.get('name')} - Error: {e}")
        
        total_success += batch_success
        total_failed += batch_failed
        
        print(f"  📊 Batch {batch_num} Results: {batch_success} success, {batch_failed} failed")
        
        # Wait between batches
        if batch_num < total_batches:
            print("  ⏳ Waiting 2 seconds before next batch...")
            time.sleep(2)
    
    print(f"\n📊 Total Results:")
    print(f"✅ Successfully added: {total_success} restaurants")
    print(f"❌ Failed to add: {total_failed} restaurants")
    
    return total_success, total_failed

def verify_import():
    """Verify the import was successful"""
    print("\n🔍 Verifying Import")
    print("=" * 30)
    
    try:
        response = requests.get("https://jewgo.onrender.com/api/restaurants?limit=50", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            restaurants = data.get('data', [])
            total_results = data.get('metadata', {}).get('total_results', 0)
            
            print(f"📊 Total restaurants in database: {total_results}")
            print(f"📋 Sample restaurants:")
            
            for i, restaurant in enumerate(restaurants[:10], 1):
                print(f"  {i}. {restaurant.get('name')} - {restaurant.get('city')}, {restaurant.get('state')}")
            
            return True
        else:
            print(f"❌ Failed to verify data: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Batch Importing Real Restaurant Data to JewGo Database")
    print("=" * 60)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load restaurant data
    restaurants = load_formatted_restaurant_data()
    
    if not restaurants:
        print("❌ No restaurant data found. Exiting.")
        return
    
    # Import restaurants in batches
    success_count, failed_count = import_restaurant_batch(restaurants, batch_size=10)
    
    # Verify the import
    if verify_import():
        print("\n✅ Import verification successful!")
        print(f"📱 Visit: https://jewgo-app.vercel.app")
        print(f"📊 Total restaurants added: {success_count}")
        
        if failed_count > 0:
            print(f"⚠️  Note: {failed_count} restaurants failed to add")
    else:
        print("\n⚠️  Import verification failed")
    
    print(f"\n📅 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 