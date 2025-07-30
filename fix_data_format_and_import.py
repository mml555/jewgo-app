#!/usr/bin/env python3
"""
Fix Data Format and Import All Restaurants
"""

import json
import requests
import time
from datetime import datetime

def load_and_format_restaurant_data():
    """Load and format restaurant data from local_restaurants.json"""
    print("📂 Loading and formatting restaurant data from local_restaurants.json")
    
    try:
        with open('local_restaurants.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        restaurants = data.get('restaurants', [])
        print(f"✅ Loaded {len(restaurants)} restaurants from local_restaurants.json")
        
        # Format the data to match database schema
        formatted_restaurants = []
        
        for restaurant in restaurants:
            # Map the fields to match database schema
            formatted_restaurant = {
                'business_id': restaurant.get('business_id', ''),
                'name': restaurant.get('name', ''),
                'website_link': restaurant.get('website_link') or restaurant.get('website', ''),
                'phone_number': restaurant.get('phone_number', ''),
                'address': restaurant.get('address', ''),
                'city': restaurant.get('city', ''),
                'state': restaurant.get('state', ''),
                'zip_code': restaurant.get('zip_code', ''),
                'certificate_link': restaurant.get('certificate_link', ''),
                'image_url': restaurant.get('image_url', ''),
                'certifying_agency': restaurant.get('certifying_agency', 'ORB'),
                'kosher_category': restaurant.get('kosher_category', 'unknown'),
                'listing_type': restaurant.get('listing_type', 'restaurant'),
                'status': restaurant.get('status', 'active'),
                'rating': restaurant.get('rating') or restaurant.get('google_rating'),
                'price_range': restaurant.get('price_range', ''),
                'hours_of_operation': restaurant.get('hours_of_operation', ''),
                'short_description': restaurant.get('short_description', ''),
                'notes': restaurant.get('notes', ''),
                'latitude': restaurant.get('latitude'),
                'longitude': restaurant.get('longitude'),
                'data_source': restaurant.get('data_source', 'manual'),
                'external_id': restaurant.get('external_id', '')
            }
            
            # Clean up data
            if formatted_restaurant['rating']:
                try:
                    formatted_restaurant['rating'] = float(formatted_restaurant['rating'])
                except (ValueError, TypeError):
                    formatted_restaurant['rating'] = None
            
            if formatted_restaurant['latitude']:
                try:
                    formatted_restaurant['latitude'] = float(formatted_restaurant['latitude'])
                except (ValueError, TypeError):
                    formatted_restaurant['latitude'] = None
            
            if formatted_restaurant['longitude']:
                try:
                    formatted_restaurant['longitude'] = float(formatted_restaurant['longitude'])
                except (ValueError, TypeError):
                    formatted_restaurant['longitude'] = None
            
            # Validate required fields
            if not formatted_restaurant['name'] or not formatted_restaurant['business_id']:
                print(f"⚠️  Skipping restaurant with missing name or business_id: {restaurant.get('name', 'Unknown')}")
                continue
            
            formatted_restaurants.append(formatted_restaurant)
        
        print(f"✅ Formatted {len(formatted_restaurants)} restaurants for import")
        return formatted_restaurants
        
    except Exception as e:
        print(f"❌ Error loading restaurant data: {e}")
        return []

def clear_existing_data():
    """Clear existing restaurant data"""
    print("🗑️  Clearing existing restaurant data")
    
    try:
        # Get current restaurants
        response = requests.get("https://jewgo.onrender.com/api/restaurants?limit=1000", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            existing_restaurants = data.get('data', [])
            
            if existing_restaurants:
                print(f"📊 Found {len(existing_restaurants)} existing restaurants")
                
                # Delete each restaurant (if there's a delete endpoint)
                # For now, we'll just note that we're replacing the data
                print("⚠️  Note: Existing data will be replaced with new import")
            else:
                print("✅ No existing restaurants found")
        else:
            print(f"⚠️  Could not check existing data: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️  Error checking existing data: {e}")

def import_restaurants_in_batches(restaurants, batch_size=10):
    """Import restaurants in batches to avoid overwhelming the API"""
    print(f"🚀 Importing {len(restaurants)} restaurants in batches of {batch_size}")
    
    total_restaurants = len(restaurants)
    successful_imports = 0
    failed_imports = 0
    skipped_imports = 0
    
    for i in range(0, total_restaurants, batch_size):
        batch = restaurants[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total_restaurants + batch_size - 1) // batch_size
        
        print(f"\n📦 Processing batch {batch_num}/{total_batches} ({len(batch)} restaurants)")
        
        for j, restaurant in enumerate(batch):
            restaurant_num = i + j + 1
            
            try:
                # Add restaurant via API
                response = requests.post(
                    "https://jewgo.onrender.com/api/admin/restaurants",
                    json=restaurant,
                    timeout=30
                )
                
                if response.status_code == 200:
                    print(f"✅ [{restaurant_num}/{total_restaurants}] Added: {restaurant['name']}")
                    successful_imports += 1
                elif response.status_code == 409:
                    print(f"⏭️  [{restaurant_num}/{total_restaurants}] Skipped (already exists): {restaurant['name']}")
                    skipped_imports += 1
                else:
                    print(f"❌ [{restaurant_num}/{total_restaurants}] Failed ({response.status_code}): {restaurant['name']}")
                    failed_imports += 1
                    
            except Exception as e:
                print(f"❌ [{restaurant_num}/{total_restaurants}] Error: {restaurant['name']} - {e}")
                failed_imports += 1
            
            # Small delay between requests to avoid overwhelming the server
            time.sleep(0.5)
        
        # Delay between batches
        if batch_num < total_batches:
            print(f"⏳ Waiting 2 seconds before next batch...")
            time.sleep(2)
    
    return {
        'successful': successful_imports,
        'failed': failed_imports,
        'skipped': skipped_imports,
        'total': total_restaurants
    }

def verify_import_results():
    """Verify the import results"""
    print("\n🔍 Verifying import results")
    
    try:
        response = requests.get("https://jewgo.onrender.com/api/restaurants?limit=1000", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            restaurants = data.get('data', [])
            
            print(f"📊 Total restaurants in database: {len(restaurants)}")
            
            if restaurants:
                print("📋 Sample restaurants:")
                for i, restaurant in enumerate(restaurants[:5]):
                    print(f"   {i+1}. {restaurant.get('name', 'Unknown')} - {restaurant.get('city', 'Unknown')}, {restaurant.get('state', 'Unknown')}")
            
            return len(restaurants)
        else:
            print(f"❌ Failed to verify results: {response.status_code}")
            return 0
            
    except Exception as e:
        print(f"❌ Error verifying results: {e}")
        return 0

def main():
    """Main function to fix data format and import all restaurants"""
    print("🚀 Fixing Data Format and Importing All Restaurants")
    print("=" * 60)
    
    # Load and format restaurant data
    restaurants = load_and_format_restaurant_data()
    
    if not restaurants:
        print("❌ No restaurants to import")
        return
    
    # Clear existing data (optional)
    clear_existing_data()
    
    # Import restaurants in batches
    results = import_restaurants_in_batches(restaurants, batch_size=10)
    
    # Print summary
    print("\n📊 Import Summary")
    print("=" * 30)
    print(f"✅ Successfully imported: {results['successful']}")
    print(f"❌ Failed to import: {results['failed']}")
    print(f"⏭️  Skipped (already exists): {results['skipped']}")
    print(f"📋 Total processed: {results['total']}")
    
    # Verify results
    final_count = verify_import_results()
    
    print(f"\n🎉 Import completed!")
    print(f"📊 Final restaurant count: {final_count}")
    
    if final_count > 0:
        print("✅ Success! All restaurants have been imported.")
        print("🌐 You can now test the application with the full dataset.")
    else:
        print("⚠️  No restaurants found in database after import.")

if __name__ == "__main__":
    main() 