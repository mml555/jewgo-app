#!/usr/bin/env python3
"""
Script to format restaurant data for database import
"""

import json

def format_restaurant_for_db(restaurant):
    """Format a restaurant object for database import"""
    return {
        'business_id': restaurant.get('business_id', ''),
        'name': restaurant.get('name', ''),
        'address': restaurant.get('address', ''),
        'city': restaurant.get('city', ''),
        'state': restaurant.get('state', ''),
        'zip_code': restaurant.get('zip_code', ''),
        'phone_number': restaurant.get('phone_number', ''),
        'website': restaurant.get('website', ''),
        'kosher_category': restaurant.get('kosher_category', ''),
        'certifying_agency': restaurant.get('certifying_agency', ''),
        'listing_type': restaurant.get('listing_type', 'restaurant'),
        'latitude': restaurant.get('latitude'),
        'longitude': restaurant.get('longitude'),
        'rating': restaurant.get('rating', 0.0),
        'review_count': restaurant.get('review_count', 0),
        'price_range': restaurant.get('price_range', ''),
        'hours_open': restaurant.get('hours_open', ''),
        'takeout_available': restaurant.get('takeout_available', 0),
        'delivery_available': restaurant.get('delivery_available', 0),
        'dine_in_available': restaurant.get('dine_in_available', 0),
        'status': restaurant.get('status', 'active')
    }

def main():
    print("🔧 Formatting restaurant data for database import...")
    
    # Load original data
    try:
        with open('local_restaurants.json', 'r') as f:
            data = json.load(f)
            restaurants = data.get('restaurants', [])
    except FileNotFoundError:
        print("❌ local_restaurants.json not found!")
        return
    except json.JSONDecodeError:
        print("❌ Invalid JSON in local_restaurants.json!")
        return
    
    print(f"📊 Found {len(restaurants)} restaurants")
    
    # Format restaurants for database
    formatted_restaurants = []
    for restaurant in restaurants:
        formatted = format_restaurant_for_db(restaurant)
        formatted_restaurants.append(formatted)
    
    # Create new file with formatted data
    formatted_data = {
        'restaurants': formatted_restaurants
    }
    
    with open('formatted_restaurants.json', 'w') as f:
        json.dump(formatted_data, f, indent=2)
    
    print(f"✅ Formatted {len(formatted_restaurants)} restaurants")
    print("📝 Saved to: formatted_restaurants.json")
    
    # Show sample of formatted data
    if formatted_restaurants:
        print("\n📋 Sample formatted restaurant:")
        sample = formatted_restaurants[0]
        for key, value in sample.items():
            print(f"   {key}: {value}")

if __name__ == "__main__":
    main() 