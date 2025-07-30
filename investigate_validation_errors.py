#!/usr/bin/env python3
"""
Investigate Validation Errors - Find specific causes of 500 responses
"""

import json
import requests
import time

def test_backend_health():
    """Test if backend is responding"""
    print("🔍 Testing Backend Health")
    print("=" * 30)
    
    try:
        response = requests.get("https://jewgo.onrender.com/health", timeout=30)
        print(f"Health endpoint status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Backend is responding")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health check error: {e}")
        return False

def test_single_restaurant_import(restaurant_data):
    """Test importing a single restaurant and get detailed error information"""
    print(f"\n🧪 Testing restaurant: {restaurant_data.get('name', 'Unknown')}")
    
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
                print(f"   Error JSON: {json.dumps(error_data, indent=2)}")
                
                # Look for specific validation errors
                if 'error' in error_data:
                    print(f"   Error message: {error_data['error']}")
                if 'message' in error_data:
                    print(f"   Message: {error_data['message']}")
                if 'details' in error_data:
                    print(f"   Details: {error_data['details']}")
                    
            except json.JSONDecodeError:
                print(f"   Raw response: {response.text[:500]}")
            
            return False
            
    except Exception as e:
        print(f"❌ Request error: {e}")
        return False

def load_sample_restaurants():
    """Load a few sample restaurants for testing"""
    print("\n📂 Loading sample restaurants for testing")
    
    try:
        with open('local_restaurants.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        restaurants = data.get('restaurants', [])
        print(f"✅ Loaded {len(restaurants)} restaurants")
        
        # Return first 5 restaurants for testing
        return restaurants[:5]
        
    except Exception as e:
        print(f"❌ Error loading restaurants: {e}")
        return []

def create_test_restaurant():
    """Create a minimal test restaurant to check basic validation"""
    print("\n🧪 Creating minimal test restaurant")
    
    test_restaurant = {
        'business_id': 'test_001',
        'name': 'Test Restaurant',
        'website_link': '',
        'phone_number': '',
        'address': '123 Test St',
        'city': 'Test City',
        'state': 'FL',
        'zip_code': '12345',
        'certificate_link': '',
        'image_url': '',
        'certifying_agency': 'ORB',
        'kosher_category': 'unknown',
        'listing_type': 'restaurant',
        'status': 'active',
        'rating': None,
        'price_range': '',
        'hours_of_operation': '',
        'short_description': '',
        'notes': '',
        'latitude': None,
        'longitude': None,
        'data_source': 'manual',
        'external_id': ''
    }
    
    return test_restaurant

def test_api_endpoints():
    """Test all API endpoints to see which ones are working"""
    print("\n🔍 Testing API Endpoints")
    print("=" * 30)
    
    endpoints = [
        "/health",
        "/api/restaurants",
        "/api/categories", 
        "/api/states",
        "/api/statistics"
    ]
    
    for endpoint in endpoints:
        try:
            url = f"https://jewgo.onrender.com{endpoint}"
            response = requests.get(url, timeout=30)
            print(f"{endpoint}: {response.status_code}")
            
            if response.status_code != 200:
                try:
                    error_data = response.json()
                    print(f"  Error: {error_data}")
                except:
                    print(f"  Raw: {response.text[:100]}")
                    
        except Exception as e:
            print(f"{endpoint}: Error - {e}")

def investigate_specific_restaurant():
    """Investigate a specific restaurant that was failing"""
    print("\n🔍 Investigating specific failing restaurant")
    
    # This is one of the restaurants that was failing
    failing_restaurant = {
        'business_id': 'test_fail_001',
        'name': 'A La Carte',
        'website_link': '',
        'phone_number': '',
        'address': '',
        'city': 'Unknown',
        'state': 'FL',
        'zip_code': '',
        'certificate_link': '',
        'image_url': '',
        'certifying_agency': 'ORB',
        'kosher_category': 'unknown',
        'listing_type': 'restaurant',
        'status': 'active',
        'rating': None,
        'price_range': '',
        'hours_of_operation': '',
        'short_description': '',
        'notes': '',
        'latitude': None,
        'longitude': None,
        'data_source': 'manual',
        'external_id': ''
    }
    
    return test_single_restaurant_import(failing_restaurant)

def main():
    """Main investigation function"""
    print("🔍 Investigating Validation Errors Causing 500 Responses")
    print("=" * 60)
    
    # 1. Test backend health
    if not test_backend_health():
        print("\n❌ Backend is not responding. Waiting 30 seconds and retrying...")
        time.sleep(30)
        if not test_backend_health():
            print("❌ Backend still not responding. The issue may be temporary.")
            return
    
    # 2. Test API endpoints
    test_api_endpoints()
    
    # 3. Test minimal restaurant
    print("\n" + "="*50)
    test_restaurant = create_test_restaurant()
    test_single_restaurant_import(test_restaurant)
    
    # 4. Test specific failing restaurant
    print("\n" + "="*50)
    investigate_specific_restaurant()
    
    # 5. Test a few sample restaurants from the data
    print("\n" + "="*50)
    sample_restaurants = load_sample_restaurants()
    
    for i, restaurant in enumerate(sample_restaurants):
        print(f"\n--- Testing Sample Restaurant {i+1} ---")
        
        # Format the restaurant data
        formatted_restaurant = {
            'business_id': restaurant.get('business_id', f'sample_{i+1}'),
            'name': restaurant.get('name', f'Sample Restaurant {i+1}'),
            'website_link': restaurant.get('website_link') or restaurant.get('website', ''),
            'phone_number': restaurant.get('phone_number', ''),
            'address': restaurant.get('address', ''),
            'city': restaurant.get('city', '') or 'Unknown',
            'state': restaurant.get('state', '') or 'FL',
            'zip_code': restaurant.get('zip_code', ''),
            'certificate_link': restaurant.get('certificate_link', ''),
            'image_url': restaurant.get('image_url', ''),
            'certifying_agency': 'ORB',
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
        
        # Fix kosher_category if invalid
        kosher_category = formatted_restaurant['kosher_category']
        valid_categories = ['meat', 'dairy', 'pareve', 'fish', 'unknown']
        if kosher_category not in valid_categories:
            formatted_restaurant['kosher_category'] = 'unknown'
        
        # Clean numeric fields
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
        
        test_single_restaurant_import(formatted_restaurant)
        
        # Small delay between tests
        time.sleep(2)
    
    print("\n" + "="*60)
    print("🔍 Investigation Complete")
    print("Check the error messages above to identify specific validation issues.")

if __name__ == "__main__":
    main() 