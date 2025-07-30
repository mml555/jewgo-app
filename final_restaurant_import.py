#!/usr/bin/env python3
"""
Final Restaurant Import - Conservative approach
"""

import json
import requests
import time
from datetime import datetime

def get_existing_restaurants():
    """Get list of existing restaurants to avoid duplicates"""
    try:
        response = requests.get("https://jewgo.onrender.com/api/restaurants?limit=1000", timeout=30)
        if response.status_code == 200:
            data = response.json()
            existing = data.get('data', [])
            existing_ids = {restaurant.get('business_id') for restaurant in existing}
            print(f"📊 Found {len(existing)} existing restaurants")
            return existing_ids
        else:
            print(f"⚠️  Could not check existing restaurants: {response.status_code}")
            return set()
    except Exception as e:
        print(f"⚠️  Error checking existing restaurants: {e}")
        return set()

def load_and_minimally_fix_restaurant_data():
    """Load and minimally fix restaurant data"""
    print("📂 Loading and minimally fixing restaurant data")
    
    try:
        with open('local_restaurants.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        restaurants = data.get('restaurants', [])
        print(f"✅ Loaded {len(restaurants)} restaurants from local_restaurants.json")
        
        # Get existing restaurants to skip them
        existing_ids = get_existing_restaurants()
        
        # Format and minimally fix the data
        formatted_restaurants = []
        
        for restaurant in restaurants:
            business_id = restaurant.get('business_id', '')
            
            # Skip if already exists
            if business_id in existing_ids:
                continue
            
            # Map the fields to match database schema with minimal changes
            formatted_restaurant = {
                'business_id': business_id or f"auto_{len(formatted_restaurants) + 1}",
                'name': restaurant.get('name', '') or f"Restaurant {business_id}",
                'website_link': restaurant.get('website_link') or restaurant.get('website', ''),
                'phone_number': restaurant.get('phone_number', ''),
                'address': restaurant.get('address', ''),
                'city': restaurant.get('city', '') or 'Unknown',
                'state': restaurant.get('state', '') or 'FL',
                'zip_code': restaurant.get('zip_code', ''),
                'certificate_link': restaurant.get('certificate_link', ''),
                'image_url': restaurant.get('image_url', ''),
                'certifying_agency': 'ORB',  # Default to ORB for all
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
            
            # Only fix the essential validation issues
            
            # 1. Fix kosher_category if invalid
            kosher_category = formatted_restaurant['kosher_category']
            valid_categories = ['meat', 'dairy', 'pareve', 'fish', 'unknown']
            if kosher_category not in valid_categories:
                formatted_restaurant['kosher_category'] = 'unknown'
            
            # 2. Clean up data types for numeric fields
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
            
            # 3. Ensure text fields are strings and not too long
            for field in ['name', 'website_link', 'phone_number', 'address', 'city', 'state', 'zip_code', 'certificate_link', 'image_url', 'price_range', 'hours_of_operation', 'short_description', 'notes', 'data_source', 'external_id']:
                if formatted_restaurant[field] is not None:
                    formatted_restaurant[field] = str(formatted_restaurant[field])
                    # Truncate if too long (basic truncation)
                    if len(formatted_restaurant[field]) > 1000:
                        formatted_restaurant[field] = formatted_restaurant[field][:997] + "..."
                else:
                    formatted_restaurant[field] = ""
            
            formatted_restaurants.append(formatted_restaurant)
        
        print(f"✅ Prepared {len(formatted_restaurants)} restaurants for import")
        return formatted_restaurants
        
    except Exception as e:
        print(f"❌ Error loading restaurant data: {e}")
        return []

def import_restaurants_conservatively(restaurants, batch_size=5):
    """Import restaurants with conservative approach"""
    print(f"🚀 Importing {len(restaurants)} restaurants in batches of {batch_size}")
    
    total_restaurants = len(restaurants)
    successful_imports = 0
    failed_imports = 0
    
    for i in range(0, total_restaurants, batch_size):
        batch = restaurants[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total_restaurants + batch_size - 1) // batch_size
        
        print(f"\n📦 Processing batch {batch_num}/{total_batches} ({len(batch)} restaurants)")
        
        batch_success = 0
        batch_failures = 0
        
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
                    batch_success += 1
                elif response.status_code == 409:
                    print(f"⏭️  [{restaurant_num}/{total_restaurants}] Already exists: {restaurant['name']}")
                    successful_imports += 1
                    batch_success += 1
                elif response.status_code == 429:
                    print(f"⏳ [{restaurant_num}/{total_restaurants}] Rate limited: {restaurant['name']}")
                    batch_failures += 1
                    failed_imports += 1
                    print("   ⏳ Waiting 15 seconds due to rate limiting...")
                    time.sleep(15)
                else:
                    print(f"❌ [{restaurant_num}/{total_restaurants}] Failed ({response.status_code}): {restaurant['name']}")
                    batch_failures += 1
                    failed_imports += 1
                    
            except Exception as e:
                print(f"❌ [{restaurant_num}/{total_restaurants}] Error: {restaurant['name']} - {e}")
                batch_failures += 1
                failed_imports += 1
            
            # Small delay between requests
            time.sleep(2)
        
        # Print batch summary
        print(f"📊 Batch {batch_num} summary: {batch_success} success, {batch_failures} failures")
        
        # Delay between batches
        if batch_num < total_batches:
            print("⏳ Waiting 8 seconds before next batch...")
            time.sleep(8)
    
    return {
        'successful': successful_imports,
        'failed': failed_imports,
        'total': total_restaurants
    }

def main():
    """Main function to complete restaurant import"""
    print("🚀 Final Restaurant Import - Conservative Approach")
    print("=" * 60)
    
    # Load and minimally fix restaurant data
    restaurants = load_and_minimally_fix_restaurant_data()
    
    if not restaurants:
        print("✅ No new restaurants to import - all done!")
        return
    
    # Import restaurants conservatively
    results = import_restaurants_conservatively(restaurants, batch_size=5)
    
    # Print summary
    print("\n📊 Import Summary")
    print("=" * 30)
    print(f"✅ Successfully imported: {results['successful']}")
    print(f"❌ Failed to import: {results['failed']}")
    print(f"📋 Total processed: {results['total']}")
    
    # Final verification
    try:
        response = requests.get("https://jewgo.onrender.com/api/restaurants?limit=1000", timeout=30)
        if response.status_code == 200:
            data = response.json()
            restaurants = data.get('data', [])
            print(f"\n🎉 Final restaurant count: {len(restaurants)}")
            
            if len(restaurants) >= 200:
                print("🎊 SUCCESS! We now have 200+ restaurants in the database!")
                print("🌐 The application is ready with the full dataset.")
            else:
                print(f"📊 Progress: {len(restaurants)}/200+ restaurants imported")
        else:
            print(f"❌ Could not verify final count: {response.status_code}")
    except Exception as e:
        print(f"❌ Error verifying final count: {e}")

if __name__ == "__main__":
    main() 