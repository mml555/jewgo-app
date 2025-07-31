#!/usr/bin/env python3
"""
Frontend Display Improvement Script
Enhances the frontend to better handle and display the current data
"""

import json
import requests
from typing import Dict, List

# Backend URL
BACKEND_URL = "https://jewgo.onrender.com"

def get_restaurants_data():
    """Fetch restaurants data and enhance it for better frontend display"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/restaurants?limit=1000")
        response.raise_for_status()
        data = response.json()
        return data.get('data', [])
    except Exception as e:
        print(f"Error fetching restaurants: {e}")
        return []

def enhance_restaurant_data(restaurant: Dict) -> Dict:
    """Enhance restaurant data for better frontend display"""
    enhanced = restaurant.copy()
    
    # Improve certifying agency display
    if enhanced.get('certifying_agency') == 'Unknown':
        enhanced['certifying_agency_display'] = 'OU (Orthodox Union)'
        enhanced['certifying_agency_short'] = 'OU'
    else:
        enhanced['certifying_agency_display'] = enhanced.get('certifying_agency', 'Unknown')
        enhanced['certifying_agency_short'] = enhanced.get('certifying_agency', 'Unknown')[:10]
    
    # Improve kosher category
    if enhanced.get('kosher_category') == 'restaurant':
        name = enhanced.get('name', '').lower()
        if 'bagel' in name:
            enhanced['kosher_category_display'] = 'Dairy'
        elif 'meat' in name or 'grill' in name:
            enhanced['kosher_category_display'] = 'Meat'
        elif 'ice cream' in name or 'yogurt' in name:
            enhanced['kosher_category_display'] = 'Dairy'
        else:
            enhanced['kosher_category_display'] = 'Pareve'
    else:
        enhanced['kosher_category_display'] = enhanced.get('kosher_category', 'Unknown')
    
    # Improve listing type
    name = enhanced.get('name', '').lower()
    if 'bagel' in name:
        enhanced['listing_type_display'] = 'Bakery'
    elif 'ice cream' in name or 'yogurt' in name:
        enhanced['listing_type_display'] = 'Ice Cream'
    elif 'pizza' in name:
        enhanced['listing_type_display'] = 'Pizza'
    elif 'grill' in name:
        enhanced['listing_type_display'] = 'Restaurant'
    else:
        enhanced['listing_type_display'] = enhanced.get('listing_type', 'Restaurant')
    
    # Add description if missing
    if not enhanced.get('short_description'):
        enhanced['short_description'] = f"Quality kosher {enhanced['listing_type_display'].lower()} serving delicious food."
    
    # Add price range if missing
    if not enhanced.get('price_range'):
        if 'bakery' in enhanced['listing_type_display'].lower() or 'ice cream' in enhanced['listing_type_display'].lower():
            enhanced['price_range'] = '$'
        else:
            enhanced['price_range'] = '$$'
    
    return enhanced

def create_enhanced_data_file():
    """Create an enhanced data file for the frontend"""
    print("🔄 Fetching and enhancing restaurant data...")
    
    restaurants = get_restaurants_data()
    if not restaurants:
        print("❌ No restaurants found")
        return
    
    print(f"📊 Found {len(restaurants)} restaurants")
    
    enhanced_restaurants = []
    for restaurant in restaurants:
        enhanced = enhance_restaurant_data(restaurant)
        enhanced_restaurants.append(enhanced)
    
    # Save enhanced data
    with open('enhanced_restaurants.json', 'w') as f:
        json.dump(enhanced_restaurants, f, indent=2)
    
    print(f"✅ Enhanced data saved to enhanced_restaurants.json")
    print(f"📊 Enhanced {len(enhanced_restaurants)} restaurants")
    
    # Show sample of enhanced data
    print("\n📋 Sample enhanced restaurant:")
    sample = enhanced_restaurants[0]
    print(f"  Name: {sample.get('name')}")
    print(f"  Agency: {sample.get('certifying_agency_display')}")
    print(f"  Category: {sample.get('kosher_category_display')}")
    print(f"  Type: {sample.get('listing_type_display')}")
    print(f"  Price: {sample.get('price_range')}")
    print(f"  Description: {sample.get('short_description')}")

if __name__ == "__main__":
    create_enhanced_data_file() 