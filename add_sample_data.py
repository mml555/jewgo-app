#!/usr/bin/env python3
"""
Add Sample Restaurant Data for Testing
"""

import requests
import json
from datetime import datetime

# Sample restaurant data
SAMPLE_RESTAURANTS = [
    {
        "business_id": "sample_001",
        "name": "Kosher Deli & Grill",
        "website_link": "https://example.com/kosher-deli",
        "phone_number": "(555) 123-4567",
        "address": "123 Main Street",
        "city": "Miami",
        "state": "FL",
        "zip_code": "33101",
        "certificate_link": "https://example.com/cert1",
        "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=400",
        "certifying_agency": "ORB",
        "kosher_category": "meat",
        "listing_type": "restaurant",
        "status": "active",
        "rating": 4.5,
        "price_range": "$$",
        "hours_of_operation": "Mon-Fri: 11AM-9PM, Sat: 12PM-10PM, Sun: Closed",
        "short_description": "Authentic kosher deli serving traditional Jewish cuisine with a modern twist.",
        "notes": "Glatt kosher certified by ORB",
        "latitude": 25.7617,
        "longitude": -80.1918,
        "data_source": "manual"
    },
    {
        "business_id": "sample_002",
        "name": "Shalom Pizza & Pasta",
        "website_link": "https://example.com/shalom-pizza",
        "phone_number": "(555) 234-5678",
        "address": "456 Ocean Drive",
        "city": "Miami Beach",
        "state": "FL",
        "zip_code": "33139",
        "certificate_link": "https://example.com/cert2",
        "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400",
        "certifying_agency": "ORB",
        "kosher_category": "dairy",
        "listing_type": "restaurant",
        "status": "active",
        "rating": 4.2,
        "price_range": "$",
        "hours_of_operation": "Daily: 11AM-11PM",
        "short_description": "Kosher pizza and pasta restaurant with authentic Italian flavors.",
        "notes": "Dairy restaurant - no meat products",
        "latitude": 25.7907,
        "longitude": -80.1300,
        "data_source": "manual"
    },
    {
        "business_id": "sample_003",
        "name": "Mazel Tov Bakery",
        "website_link": "https://example.com/mazel-tov-bakery",
        "phone_number": "(555) 345-6789",
        "address": "789 Biscayne Blvd",
        "city": "Miami",
        "state": "FL",
        "zip_code": "33132",
        "certificate_link": "https://example.com/cert3",
        "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400",
        "certifying_agency": "ORB",
        "kosher_category": "dairy",
        "listing_type": "bakery",
        "status": "active",
        "rating": 4.8,
        "price_range": "$",
        "hours_of_operation": "Mon-Sat: 6AM-8PM, Sun: 7AM-6PM",
        "short_description": "Traditional Jewish bakery specializing in challah, rugelach, and other kosher pastries.",
        "notes": "Parve and dairy options available",
        "latitude": 25.7749,
        "longitude": -80.1977,
        "data_source": "manual"
    },
    {
        "business_id": "sample_004",
        "name": "Beth Israel Synagogue",
        "website_link": "https://example.com/beth-israel",
        "phone_number": "(555) 456-7890",
        "address": "321 Temple Street",
        "city": "Miami",
        "state": "FL",
        "zip_code": "33133",
        "certificate_link": "https://example.com/cert4",
        "image_url": "https://images.unsplash.com/photo-1542810634-71277d95dcbb?w=400",
        "certifying_agency": "ORB",
        "kosher_category": "synagogue",
        "listing_type": "synagogue",
        "status": "active",
        "rating": 4.6,
        "price_range": "Free",
        "hours_of_operation": "Daily: Services at 7AM, 6PM",
        "short_description": "Conservative synagogue serving the Miami Jewish community with daily services and educational programs.",
        "notes": "Welcoming community for all levels of observance",
        "latitude": 25.7617,
        "longitude": -80.1918,
        "data_source": "manual"
    },
    {
        "business_id": "sample_005",
        "name": "Kosher Market & Deli",
        "website_link": "https://example.com/kosher-market",
        "phone_number": "(555) 567-8901",
        "address": "654 Market Avenue",
        "city": "Miami",
        "state": "FL",
        "zip_code": "33134",
        "certificate_link": "https://example.com/cert5",
        "image_url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400",
        "certifying_agency": "ORB",
        "kosher_category": "grocery",
        "listing_type": "grocery",
        "status": "active",
        "rating": 4.3,
        "price_range": "$$",
        "hours_of_operation": "Mon-Fri: 8AM-9PM, Sat: 9AM-8PM, Sun: 9AM-7PM",
        "short_description": "Full-service kosher grocery store with fresh produce, meats, and prepared foods.",
        "notes": "Glatt kosher meats and poultry available",
        "latitude": 25.7749,
        "longitude": -80.1977,
        "data_source": "manual"
    }
]

def add_sample_restaurants():
    """Add sample restaurant data to the database"""
    backend_url = "https://jewgo.onrender.com"
    
    print("🍽️  Adding Sample Restaurant Data")
    print("=" * 40)
    
    success_count = 0
    error_count = 0
    
    for i, restaurant in enumerate(SAMPLE_RESTAURANTS, 1):
        try:
            print(f"\n📝 Adding restaurant {i}/{len(SAMPLE_RESTAURANTS)}: {restaurant['name']}")
            
            response = requests.post(
                f"{backend_url}/api/admin/restaurants",
                json=restaurant,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ Successfully added: {restaurant['name']}")
                    success_count += 1
                else:
                    print(f"❌ Failed to add: {restaurant['name']} - {data.get('message', 'Unknown error')}")
                    error_count += 1
            else:
                print(f"❌ HTTP Error {response.status_code}: {restaurant['name']}")
                error_count += 1
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request Error: {restaurant['name']} - {e}")
            error_count += 1
        except Exception as e:
            print(f"❌ Unexpected Error: {restaurant['name']} - {e}")
            error_count += 1
    
    print(f"\n📊 Results:")
    print(f"✅ Successfully added: {success_count} restaurants")
    print(f"❌ Failed to add: {error_count} restaurants")
    
    return success_count > 0

def verify_data_added():
    """Verify that the data was added successfully"""
    print("\n🔍 Verifying Data Addition")
    print("=" * 30)
    
    try:
        response = requests.get("https://jewgo.onrender.com/api/restaurants?limit=10", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            total_results = data.get('metadata', {}).get('total_results', 0)
            restaurants = data.get('restaurants', [])
            
            print(f"📊 Total restaurants in database: {total_results}")
            print(f"📋 Restaurants returned: {len(restaurants)}")
            
            if restaurants:
                print("\n🍽️  Sample restaurants in database:")
                for i, restaurant in enumerate(restaurants[:3], 1):
                    print(f"  {i}. {restaurant.get('name', 'Unknown')} - {restaurant.get('city', 'Unknown')}, {restaurant.get('state', 'Unknown')}")
            
            return total_results > 0
        else:
            print(f"❌ Error verifying data: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
        return False

def main():
    """Main function to add sample data"""
    print("🚀 Adding Sample Restaurant Data for Testing")
    print("=" * 50)
    
    # Add sample restaurants
    if add_sample_restaurants():
        print("\n✅ Sample data addition completed")
        
        # Verify the data was added
        if verify_data_added():
            print("\n🎉 Sample restaurant data successfully added!")
            print("🌐 You can now test the application with real data")
            print("📱 Visit: https://jewgo-app.vercel.app")
        else:
            print("\n⚠️  Data verification failed - please check manually")
    else:
        print("\n❌ Failed to add sample data")

if __name__ == "__main__":
    main() 