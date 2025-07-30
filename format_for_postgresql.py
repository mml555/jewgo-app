#!/usr/bin/env python3
"""
Format restaurant data for PostgreSQL backend schema
"""

import json

def format_for_postgresql(restaurant):
    """Format a restaurant object for PostgreSQL backend"""
    return {
        'business_id': restaurant.get('business_id', ''),
        'name': restaurant.get('name', ''),
        'website_link': restaurant.get('website', ''),  # Map website to website_link
        'phone_number': restaurant.get('phone_number', ''),
        'address': restaurant.get('address', ''),
        'city': restaurant.get('city', ''),
        'state': restaurant.get('state', ''),
        'zip_code': restaurant.get('zip_code', ''),
        'certificate_link': restaurant.get('certificate_link', ''),
        'image_url': restaurant.get('image_url', ''),
        'certifying_agency': restaurant.get('certifying_agency', 'KM'),
        'kosher_category': restaurant.get('kosher_category', 'unknown'),
        'listing_type': restaurant.get('listing_type', 'restaurant'),
        'status': restaurant.get('status', 'active'),
        'rating': restaurant.get('rating'),
        'price_range': restaurant.get('price_range', ''),
        'hours_of_operation': restaurant.get('hours_open', ''),  # Map hours_open to hours_of_operation
        'short_description': restaurant.get('short_description', ''),
        'notes': restaurant.get('notes', ''),
        'latitude': restaurant.get('latitude'),
        'longitude': restaurant.get('longitude'),
        'data_source': restaurant.get('data_source', 'manual'),
        'external_id': restaurant.get('external_id', '')
    }

def main():
    print("🔄 Formatting restaurant data for PostgreSQL backend...")
    
    # Load the formatted data
    try:
        with open('formatted_restaurants.json', 'r') as f:
            data = json.load(f)
        restaurants = data.get('restaurants', [])
    except Exception as e:
        print(f"❌ Error loading formatted_restaurants.json: {e}")
        return
    
    print(f"📊 Found {len(restaurants)} restaurants to format")
    
    # Format for PostgreSQL
    postgresql_restaurants = []
    for restaurant in restaurants:
        formatted = format_for_postgresql(restaurant)
        postgresql_restaurants.append(formatted)
    
    # Save to new file
    output_data = {'restaurants': postgresql_restaurants}
    
    try:
        with open('postgresql_restaurants.json', 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"✅ Saved {len(postgresql_restaurants)} restaurants to postgresql_restaurants.json")
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return
    
    # Show sample of formatted data
    if postgresql_restaurants:
        print("\n📋 Sample formatted restaurant:")
        sample = postgresql_restaurants[0]
        for key, value in sample.items():
            if value is not None and value != '':
                print(f"  {key}: {value}")

if __name__ == "__main__":
    main() 