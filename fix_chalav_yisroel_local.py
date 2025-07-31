#!/usr/bin/env python3
"""
Fix Chalav Yisroel and Pas Yisroel Status in Local Data
Update the local restaurants JSON with correct Chalav Yisroel/Chalav Stam and Pas Yisroel information.
"""

import json
import os
from datetime import datetime

def load_local_data():
    """Load restaurant data from local JSON file."""
    try:
        with open('local_restaurants.json', 'r') as f:
            data = json.load(f)
            return data.get('restaurants', [])
    except FileNotFoundError:
        print("❌ local_restaurants.json not found!")
        return []
    except json.JSONDecodeError:
        print("❌ Invalid JSON in local_restaurants.json!")
        return []

def save_local_data(restaurants):
    """Save restaurant data to local JSON file."""
    data = {
        "last_updated": datetime.now().isoformat(),
        "restaurants": restaurants
    }
    with open('local_restaurants.json', 'w') as f:
        json.dump(data, f, indent=2)

def fix_chalav_yisroel_status(restaurants):
    """Fix Chalav Yisroel status for dairy restaurants."""
    
    # Chalav Stam restaurants (only these 3 should be Chalav Stam)
    chalav_stam_restaurants = [
        "Cafe 95 at JARC",
        "Hollywood Deli", 
        "Sobol Boynton Beach"
    ]
    
    updated_count = 0
    dairy_count = 0
    
    for restaurant in restaurants:
        if restaurant.get('kosher_category') == 'dairy':
            dairy_count += 1
            restaurant_name = restaurant.get('name', '')
            
            # Check if this restaurant should be Chalav Stam
            if restaurant_name in chalav_stam_restaurants:
                if not restaurant.get('is_cholov_yisroel', True):  # If not already set to false
                    restaurant['is_cholov_yisroel'] = False
                    updated_count += 1
                    print(f"✅ Set {restaurant_name} to Chalav Stam")
            else:
                # All other dairy restaurants should be Chalav Yisroel
                if not restaurant.get('is_cholov_yisroel', False):  # If not already set to true
                    restaurant['is_cholov_yisroel'] = True
                    updated_count += 1
                    print(f"✅ Set {restaurant_name} to Chalav Yisroel")
    
    return updated_count, dairy_count

def fix_pas_yisroel_status(restaurants):
    """Fix Pas Yisroel status for meat/pareve restaurants."""
    
    # Only these specific restaurants should be Pas Yisroel
    pas_yisroel_restaurants = [
        "Grand Cafe Hollywood",
        "Yum Berry Cafe & Sushi Bar", 
        "Pita Xpress",
        "Mizrachi's Pizza in Hollywood",
        "Boca Grill",
        "Shalom Haifa",
        "Chill & Grill Pita Boca",
        "Hummus Achla Hallandale",
        "Jon's Place",
        "Levy's Shawarma",
        "Holy Smokes BBQ and Grill (Food Truck)",
        "Friendship Cafe & Catering",
        "Tagine by Alma Grill",
        "Lox N Bagel (Bagel Factory Cafe)",
        "Kosher Bagel Cove",
        "Cafe Noir",
        "Grill Xpress",
        "PX Grill Mediterranean Cuisine",
        "Carmela's Boca",
        "Ariel's Delicious Pizza",
        "Oak and Ember",
        "Rave Pizza & Sushi",
        "Burnt Smokehouse and Bar",
        "Vish Hummus Hollywood"
    ]
    
    updated_count = 0
    meat_pareve_count = 0
    
    for restaurant in restaurants:
        if restaurant.get('kosher_category') in ['meat', 'pareve']:
            meat_pareve_count += 1
            restaurant_name = restaurant.get('name', '')
            
            # Check if this restaurant should be Pas Yisroel
            if restaurant_name in pas_yisroel_restaurants:
                if not restaurant.get('is_pas_yisroel', False):  # If not already set to true
                    restaurant['is_pas_yisroel'] = True
                    updated_count += 1
                    print(f"✅ Set {restaurant_name} to Pas Yisroel")
            else:
                # All other meat/pareve restaurants should NOT be Pas Yisroel
                if restaurant.get('is_pas_yisroel', False):  # If currently set to true
                    restaurant['is_pas_yisroel'] = False
                    updated_count += 1
                    print(f"✅ Set {restaurant_name} to Regular Pas (not Pas Yisroel)")
    
    return updated_count, meat_pareve_count

def main():
    print("🔄 Loading restaurant data...")
    restaurants = load_local_data()
    
    if not restaurants:
        print("❌ No restaurant data found!")
        return
    
    print(f"📊 Found {len(restaurants)} restaurants")
    
    # Fix Chalav Yisroel status
    print("\n🥛 Fixing Chalav Yisroel status...")
    chalav_updated, dairy_count = fix_chalav_yisroel_status(restaurants)
    
    # Fix Pas Yisroel status  
    print("\n🍞 Fixing Pas Yisroel status...")
    pas_updated, meat_pareve_count = fix_pas_yisroel_status(restaurants)
    
    # Save updated data
    print("\n💾 Saving updated data...")
    save_local_data(restaurants)
    
    # Summary
    print("\n" + "="*50)
    print("📋 UPDATE SUMMARY")
    print("="*50)
    print(f"🥛 Dairy restaurants processed: {dairy_count}")
    print(f"🥛 Chalav Yisroel updates: {chalav_updated}")
    print(f"🍞 Meat/Pareve restaurants processed: {meat_pareve_count}")
    print(f"🍞 Pas Yisroel updates: {pas_updated}")
    print(f"📊 Total restaurants updated: {chalav_updated + pas_updated}")
    print("="*50)
    
    # Count final statuses
    chalav_yisroel_count = sum(1 for r in restaurants if r.get('kosher_category') == 'dairy' and r.get('is_cholov_yisroel', False))
    chalav_stam_count = sum(1 for r in restaurants if r.get('kosher_category') == 'dairy' and not r.get('is_cholov_yisroel', True))
    pas_yisroel_count = sum(1 for r in restaurants if r.get('is_pas_yisroel', False))
    
    print(f"\n📈 FINAL COUNTS:")
    print(f"🥛 Chalav Yisroel: {chalav_yisroel_count}")
    print(f"🥛 Chalav Stam: {chalav_stam_count}")
    print(f"🍞 Pas Yisroel: {pas_yisroel_count}")
    print(f"🍞 Regular Pas (not Pas Yisroel): {meat_pareve_count - pas_yisroel_count}")

if __name__ == "__main__":
    main() 