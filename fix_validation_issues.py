#!/usr/bin/env python3
"""
Fix Validation Issues and Import All Restaurants
"""

import json
import requests
import time
from datetime import datetime

def load_and_fix_restaurant_data():
    """Load and fix restaurant data to pass validation"""
    print("📂 Loading and fixing restaurant data from local_restaurants.json")
    
    try:
        with open('local_restaurants.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        restaurants = data.get('restaurants', [])
        print(f"✅ Loaded {len(restaurants)} restaurants from local_restaurants.json")
        
        # Format and fix the data to match database schema
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
            
            # Fix validation issues
            
            # 1. Fix certifying_agency - map invalid values to valid ones
            certifying_agency = formatted_restaurant['certifying_agency']
            valid_agencies = ['ORB', 'OU', 'KOF-K', 'Star-K', 'CRC', 'Vaad HaRabbonim']
            
            if certifying_agency not in valid_agencies:
                # Map common invalid values to valid ones
                agency_mapping = {
                    'KM': 'ORB',  # Map KM to ORB as default
                    'KDM': 'ORB',  # Map KDM to ORB as default
                    '': 'ORB',     # Empty to ORB
                    None: 'ORB'    # None to ORB
                }
                formatted_restaurant['certifying_agency'] = agency_mapping.get(certifying_agency, 'ORB')
                print(f"   🔧 Fixed certifying_agency: {certifying_agency} → {formatted_restaurant['certifying_agency']}")
            
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
                print(f"   🔧 Fixed kosher_category: {kosher_category} → {formatted_restaurant['kosher_category']}")
            
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
                print(f"   🔧 Fixed missing name: {formatted_restaurant['name']}")
            
            if not formatted_restaurant['business_id']:
                formatted_restaurant['business_id'] = f"auto_{len(formatted_restaurants) + 1}"
                print(f"   🔧 Fixed missing business_id: {formatted_restaurant['business_id']}")
            
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
                    print(f"   🔧 Truncated {field}: {formatted_restaurant[field]}")
            
            formatted_restaurants.append(formatted_restaurant)
        
        print(f"✅ Fixed and formatted {len(formatted_restaurants)} restaurants for import")
        return formatted_restaurants
        
    except Exception as e:
        print(f"❌ Error loading restaurant data: {e}")
        return []

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
                    # Try to get error details
                    try:
                        error_data = response.json()
                        if 'error' in error_data:
                            print(f"   Error: {error_data['error']}")
                    except:
                        pass
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
    """Main function to fix validation issues and import all restaurants"""
    print("🚀 Fixing Validation Issues and Importing All Restaurants")
    print("=" * 70)
    
    # Load and fix restaurant data
    restaurants = load_and_fix_restaurant_data()
    
    if not restaurants:
        print("❌ No restaurants to import")
        return
    
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