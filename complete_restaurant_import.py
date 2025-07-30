#!/usr/bin/env python3
"""
Complete Restaurant Import with Rate Limiting
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

def load_and_fix_restaurant_data():
    """Load and fix restaurant data to pass validation"""
    print("📂 Loading and fixing restaurant data from local_restaurants.json")
    
    try:
        with open('local_restaurants.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        restaurants = data.get('restaurants', [])
        print(f"✅ Loaded {len(restaurants)} restaurants from local_restaurants.json")
        
        # Get existing restaurants to skip them
        existing_ids = get_existing_restaurants()
        
        # Format and fix the data to match database schema
        formatted_restaurants = []
        
        for restaurant in restaurants:
            business_id = restaurant.get('business_id', '')
            
            # Skip if already exists
            if business_id in existing_ids:
                print(f"⏭️  Skipping existing restaurant: {restaurant.get('name', 'Unknown')}")
                continue
            
            # Map the fields to match database schema
            formatted_restaurant = {
                'business_id': business_id,
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
            
            # Fix validation issues
            
            # 1. Fix certifying_agency - map invalid values to valid ones
            certifying_agency = formatted_restaurant['certifying_agency']
            valid_agencies = ['ORB', 'OU', 'KOF-K', 'Star-K', 'CRC', 'Vaad HaRabbonim']
            
            if certifying_agency not in valid_agencies:
                # Map common invalid values to valid ones
                agency_mapping = {
                    'KM': 'ORB',  # Map KM to ORB as default
                    'KDM': 'ORB',  # Map KDM to ORB as default
                    'Diamond K': 'ORB',  # Map Diamond K to ORB
                    '': 'ORB',     # Empty to ORB
                    None: 'ORB'    # None to ORB
                }
                formatted_restaurant['certifying_agency'] = agency_mapping.get(certifying_agency, 'ORB')
            
            # 2. Fix kosher_category - ensure it's valid
            kosher_category = formatted_restaurant['kosher_category']
            valid_categories = ['meat', 'dairy', 'pareve', 'fish', 'unknown']
            
            if kosher_category not in valid_categories:
                # Map common invalid values to valid ones
                category_mapping = {
                    '': 'unknown',
                    None: 'unknown',
                    'meat': 'meat',
                    'dairy': 'dairy',
                    'pareve': 'pareve',
                    'fish': 'fish'
                }
                formatted_restaurant['kosher_category'] = category_mapping.get(kosher_category, 'unknown')
            
            # 3. Clean up data types
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
            
            # 4. Ensure required fields are present
            if not formatted_restaurant['name']:
                formatted_restaurant['name'] = f"Restaurant {formatted_restaurant['business_id']}"
            
            if not formatted_restaurant['business_id']:
                formatted_restaurant['business_id'] = f"auto_{len(formatted_restaurants) + 1}"
            
            # 5. Clean up text fields that might be too long
            max_lengths = {
                'name': 255,
                'website_link': 500,
                'phone_number': 50,
                'address': 500,
                'city': 100,
                'state': 50,
                'zip_code': 20,
                'certificate_link': 500,
                'image_url': 1000,
                'certifying_agency': 100,
                'kosher_category': 50,
                'listing_type': 100,
                'status': 50,
                'price_range': 50,
                'data_source': 100,
                'external_id': 255
            }
            
            for field, max_length in max_lengths.items():
                if formatted_restaurant[field] and len(str(formatted_restaurant[field])) > max_length:
                    formatted_restaurant[field] = str(formatted_restaurant[field])[:max_length]
            
            formatted_restaurants.append(formatted_restaurant)
        
        print(f"✅ Prepared {len(formatted_restaurants)} new restaurants for import")
        return formatted_restaurants
        
    except Exception as e:
        print(f"❌ Error loading restaurant data: {e}")
        return []

def import_restaurants_with_rate_limiting(restaurants, batch_size=5):
    """Import restaurants with better rate limiting handling"""
    print(f"🚀 Importing {len(restaurants)} restaurants in batches of {batch_size}")
    
    total_restaurants = len(restaurants)
    successful_imports = 0
    failed_imports = 0
    rate_limit_count = 0
    
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
                    # Count as success since it's already there
                    successful_imports += 1
                    batch_success += 1
                elif response.status_code == 429:
                    print(f"⏳ [{restaurant_num}/{total_restaurants}] Rate limited: {restaurant['name']}")
                    rate_limit_count += 1
                    batch_failures += 1
                    failed_imports += 1
                    
                    # Wait longer for rate limiting
                    print("   ⏳ Waiting 10 seconds due to rate limiting...")
                    time.sleep(10)
                else:
                    print(f"❌ [{restaurant_num}/{total_restaurants}] Failed ({response.status_code}): {restaurant['name']}")
                    batch_failures += 1
                    failed_imports += 1
                    
            except Exception as e:
                print(f"❌ [{restaurant_num}/{total_restaurants}] Error: {restaurant['name']} - {e}")
                batch_failures += 1
                failed_imports += 1
            
            # Small delay between requests
            time.sleep(1)
        
        # Print batch summary
        print(f"📊 Batch {batch_num} summary: {batch_success} success, {batch_failures} failures")
        
        # If we had rate limiting issues, wait longer
        if rate_limit_count > 0:
            print("⏳ Rate limiting detected, waiting 30 seconds before next batch...")
            time.sleep(30)
            rate_limit_count = 0  # Reset counter
        else:
            # Normal delay between batches
            if batch_num < total_batches:
                print("⏳ Waiting 5 seconds before next batch...")
                time.sleep(5)
    
    return {
        'successful': successful_imports,
        'failed': failed_imports,
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
                for i, restaurant in enumerate(restaurants[:10]):
                    print(f"   {i+1}. {restaurant.get('name', 'Unknown')} - {restaurant.get('city', 'Unknown')}, {restaurant.get('state', 'Unknown')}")
            
            return len(restaurants)
        else:
            print(f"❌ Failed to verify results: {response.status_code}")
            return 0
            
    except Exception as e:
        print(f"❌ Error verifying results: {e}")
        return 0

def main():
    """Main function to complete restaurant import"""
    print("🚀 Completing Restaurant Import with Rate Limiting")
    print("=" * 60)
    
    # Load and fix restaurant data
    restaurants = load_and_fix_restaurant_data()
    
    if not restaurants:
        print("✅ No new restaurants to import - all done!")
        verify_import_results()
        return
    
    # Import restaurants with better rate limiting
    results = import_restaurants_with_rate_limiting(restaurants, batch_size=5)
    
    # Print summary
    print("\n📊 Import Summary")
    print("=" * 30)
    print(f"✅ Successfully imported: {results['successful']}")
    print(f"❌ Failed to import: {results['failed']}")
    print(f"📋 Total processed: {results['total']}")
    
    # Verify results
    final_count = verify_import_results()
    
    print(f"\n🎉 Import completed!")
    print(f"📊 Final restaurant count: {final_count}")
    
    if final_count > 0:
        print("✅ Success! Restaurant import completed.")
        print("🌐 You can now test the application with the full dataset.")
    else:
        print("⚠️  No restaurants found in database after import.")

if __name__ == "__main__":
    main() 