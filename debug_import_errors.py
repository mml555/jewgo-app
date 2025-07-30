#!/usr/bin/env python3
"""
Debug Import Errors - Identify specific validation issues
"""

import json
import requests
import time

def test_single_restaurant_import(restaurant_data):
    """Test importing a single restaurant and get detailed error information"""
    try:
        response = requests.post(
            "https://jewgo.onrender.com/api/admin/restaurants",
            json=restaurant_data,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Success!")
            return True
        else:
            print(f"❌ Error Response:")
            try:
                error_data = response.json()
                print(f"   Error: {error_data}")
            except:
                print(f"   Raw Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def load_and_test_sample_restaurants():
    """Load restaurant data and test a few samples to identify issues"""
    print("🔍 Debugging Import Errors")
    print("=" * 40)
    
    try:
        with open('local_restaurants.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        restaurants = data.get('restaurants', [])
        print(f"📂 Loaded {len(restaurants)} restaurants")
        
        # Test first few restaurants to identify patterns
        test_count = 5
        
        for i in range(min(test_count, len(restaurants))):
            restaurant = restaurants[i]
            
            print(f"\n🧪 Testing Restaurant {i+1}: {restaurant.get('name', 'Unknown')}")
            print("-" * 50)
            
            # Format the restaurant data
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
            
            # Print the formatted data being sent
            print("📤 Sending data:")
            for key, value in formatted_restaurant.items():
                if value is not None and value != '':
                    print(f"   {key}: {value}")
            
            # Test the import
            success = test_single_restaurant_import(formatted_restaurant)
            
            if not success:
                print("🔍 This restaurant failed - checking for common issues...")
                
                # Check for common validation issues
                if not formatted_restaurant['name']:
                    print("   ❌ Missing name")
                if not formatted_restaurant['business_id']:
                    print("   ❌ Missing business_id")
                if formatted_restaurant['certifying_agency'] not in ['ORB', 'OU', 'KOF-K', 'Star-K', 'CRC', 'Vaad HaRabbonim']:
                    print(f"   ❌ Invalid certifying_agency: {formatted_restaurant['certifying_agency']}")
                if formatted_restaurant['kosher_category'] not in ['meat', 'dairy', 'pareve', 'fish', 'unknown']:
                    print(f"   ❌ Invalid kosher_category: {formatted_restaurant['kosher_category']}")
            
            time.sleep(2)  # Delay between tests
            
    except Exception as e:
        print(f"❌ Error loading data: {e}")

def test_minimal_restaurant():
    """Test with a minimal restaurant to see if basic validation works"""
    print("\n🧪 Testing Minimal Restaurant")
    print("=" * 40)
    
    minimal_restaurant = {
        'business_id': 'test_001',
        'name': 'Test Restaurant',
        'certifying_agency': 'ORB',
        'kosher_category': 'unknown',
        'listing_type': 'restaurant',
        'status': 'active',
        'data_source': 'manual'
    }
    
    print("📤 Sending minimal data:")
    for key, value in minimal_restaurant.items():
        print(f"   {key}: {value}")
    
    success = test_single_restaurant_import(minimal_restaurant)
    
    if success:
        print("✅ Minimal restaurant works - the issue is with specific data fields")
    else:
        print("❌ Even minimal restaurant fails - there's a fundamental API issue")

def main():
    """Main debugging function"""
    print("🚀 Debugging Restaurant Import Errors")
    print("=" * 50)
    
    # Test minimal restaurant first
    test_minimal_restaurant()
    
    # Test sample restaurants
    load_and_test_sample_restaurants()
    
    print("\n📋 Summary:")
    print("   • Check the error messages above for specific validation issues")
    print("   • Common issues: invalid certifying_agency, kosher_category, or missing required fields")
    print("   • The API may have additional validation rules not visible in the database schema")

if __name__ == "__main__":
    main() 