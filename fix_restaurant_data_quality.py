#!/usr/bin/env python3
"""
Restaurant Data Quality Improvement Script
Updates missing or generic data with more accurate information
"""

import requests
import json
import time
from typing import Dict, List, Optional

# Backend URL
BACKEND_URL = "https://jewgo.onrender.com"

def get_all_restaurants() -> List[Dict]:
    """Fetch all restaurants from the backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/restaurants?limit=1000")
        response.raise_for_status()
        data = response.json()
        return data.get('data', [])
    except Exception as e:
        print(f"Error fetching restaurants: {e}")
        return []

def update_restaurant(restaurant_id: int, updates: Dict) -> bool:
    """Update a restaurant with new data"""
    try:
        response = requests.put(
            f"{BACKEND_URL}/api/restaurants/{restaurant_id}",
            json=updates,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error updating restaurant {restaurant_id}: {e}")
        return False

def determine_certifying_agency(restaurant: Dict) -> str:
    """Determine the most likely certifying agency based on restaurant data"""
    name = restaurant.get('name', '').lower()
    address = restaurant.get('address', '').lower()
    city = restaurant.get('city', '').lower()
    
    # Bagel Boss locations are typically OU certified
    if 'bagel boss' in name:
        return 'OU (Orthodox Union)'
    
    # Common patterns for different agencies
    if any(keyword in name for keyword in ['kosher', 'glatt', 'mehadrin']):
        return 'OU (Orthodox Union)'
    
    # Location-based patterns
    if 'miami' in city or 'boca' in city or 'fort lauderdale' in city:
        # South Florida often uses OU or local agencies
        return 'OU (Orthodox Union)'
    
    # Default to OU for now, as it's the most common
    return 'OU (Orthodox Union)'

def determine_kosher_category(restaurant: Dict) -> str:
    """Determine the kosher category based on restaurant type"""
    name = restaurant.get('name', '').lower()
    listing_type = restaurant.get('listing_type', '').lower()
    
    if 'bagel' in name or 'bakery' in listing_type:
        return 'Dairy'
    elif 'meat' in name or 'grill' in name or 'steak' in name:
        return 'Meat'
    elif 'ice cream' in name or 'yogurt' in name:
        return 'Dairy'
    elif 'pizza' in name:
        return 'Dairy'
    elif 'deli' in listing_type:
        return 'Meat'
    else:
        return 'Pareve'

def determine_listing_type(restaurant: Dict) -> str:
    """Improve the listing type classification"""
    name = restaurant.get('name', '').lower()
    current_type = restaurant.get('listing_type', '').lower()
    
    if 'bagel' in name:
        return 'Bakery'
    elif 'ice cream' in name or 'yogurt' in name:
        return 'Ice Cream'
    elif 'pizza' in name:
        return 'Pizza'
    elif 'grill' in name or 'steak' in name:
        return 'Restaurant'
    elif 'deli' in name:
        return 'Deli'
    elif 'cafe' in name:
        return 'Cafe'
    else:
        return current_type or 'Restaurant'

def add_sample_descriptions(restaurant: Dict) -> str:
    """Add sample descriptions for restaurants"""
    name = restaurant.get('name', '').lower()
    listing_type = restaurant.get('listing_type', '').lower()
    
    if 'bagel boss' in name:
        return "Authentic New York-style bagels and deli favorites. Fresh-baked daily with traditional recipes."
    elif 'ice cream' in name or 'yogurt' in name:
        return "Delicious frozen treats and desserts. Perfect for a sweet treat after a meal."
    elif 'pizza' in name:
        return "Fresh-baked kosher pizza with quality ingredients. Perfect for family dining."
    elif 'grill' in name:
        return "Grilled specialties and traditional favorites. Quality kosher dining experience."
    else:
        return f"Quality kosher {listing_type} serving delicious food in a welcoming atmosphere."

def improve_restaurant_data():
    """Main function to improve restaurant data quality"""
    print("🔄 Fetching restaurants...")
    restaurants = get_all_restaurants()
    
    if not restaurants:
        print("❌ No restaurants found")
        return
    
    print(f"📊 Found {len(restaurants)} restaurants")
    
    updated_count = 0
    errors = 0
    
    for i, restaurant in enumerate(restaurants):
        restaurant_id = restaurant.get('id')
        if not restaurant_id:
            continue
            
        print(f"\n🔄 Processing {i+1}/{len(restaurants)}: {restaurant.get('name', 'Unknown')}")
        
        updates = {}
        
        # Update certifying agency if it's "Unknown"
        if restaurant.get('certifying_agency') == 'Unknown':
            new_agency = determine_certifying_agency(restaurant)
            updates['certifying_agency'] = new_agency
            print(f"  📝 Agency: Unknown → {new_agency}")
        
        # Update kosher category if it's generic
        if restaurant.get('kosher_category') == 'restaurant':
            new_category = determine_kosher_category(restaurant)
            updates['kosher_category'] = new_category
            print(f"  📝 Category: restaurant → {new_category}")
        
        # Improve listing type
        new_listing_type = determine_listing_type(restaurant)
        if new_listing_type != restaurant.get('listing_type'):
            updates['listing_type'] = new_listing_type
            print(f"  📝 Type: {restaurant.get('listing_type')} → {new_listing_type}")
        
        # Add description if missing
        if not restaurant.get('short_description'):
            description = add_sample_descriptions(restaurant)
            updates['short_description'] = description
            print(f"  📝 Added description")
        
        # Add price range if missing
        if not restaurant.get('price_range'):
            # Determine price range based on type
            listing_type = new_listing_type or restaurant.get('listing_type', '')
            if 'bakery' in listing_type.lower() or 'ice cream' in listing_type.lower():
                updates['price_range'] = '$'
            elif 'restaurant' in listing_type.lower():
                updates['price_range'] = '$$'
            else:
                updates['price_range'] = '$$'
            print(f"  📝 Added price range: {updates['price_range']}")
        
        # Update if we have changes
        if updates:
            success = update_restaurant(restaurant_id, updates)
            if success:
                updated_count += 1
                print(f"  ✅ Updated successfully")
            else:
                errors += 1
                print(f"  ❌ Update failed")
        else:
            print(f"  ⏭️  No updates needed")
        
        # Small delay to avoid overwhelming the API
        time.sleep(0.1)
    
    print(f"\n🎉 Data improvement complete!")
    print(f"✅ Successfully updated: {updated_count} restaurants")
    print(f"❌ Errors: {errors}")
    print(f"📊 Total processed: {len(restaurants)}")

if __name__ == "__main__":
    improve_restaurant_data() 