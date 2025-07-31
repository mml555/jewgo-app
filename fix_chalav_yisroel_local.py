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
        "count": len(restaurants),
        "restaurants": restaurants
    }
    
    # Create backup
    backup_filename = f"local_restaurants_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open('local_restaurants.json', 'r') as f:
            with open(backup_filename, 'w') as backup_f:
                backup_f.write(f.read())
        print(f"✅ Created backup: {backup_filename}")
    except Exception as e:
        print(f"⚠️  Could not create backup: {e}")
    
    # Save updated data
    try:
        with open('local_restaurants.json', 'w') as f:
            json.dump(data, f, indent=2)
        print("✅ Updated local_restaurants.json")
        return True
    except Exception as e:
        print(f"❌ Failed to save data: {e}")
        return False

def fix_kosher_status():
    """Fix Chalav Yisroel and Pas Yisroel status for restaurants."""
    restaurants = load_local_data()
    
    if not restaurants:
        print("❌ No restaurants found!")
        return False
    
    # Define restaurants that should have Cholov Stam (regular milk) - all other dairy should be Cholov Yisroel
    cholov_stam_restaurants = [
        "Cafe 95 at JARC",
        "Hollywood Deli", 
        "Sobol Boynton Beach"
    ]
    
    # Define restaurants that should have Pas Yisroel (supervised bread)
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
        "Vish Hummus Hollywood",
        "JZ Steakhouse",
        "The Cave Kosher Bar & Grill",
        "Capas Burger",
        "Kosher Chobee",
        "Plantation Pita & Grill",
        "Lenny's Pizza (Boca)",
        "Bissli Grill",
        "Mozart Cafe Sunny Isles Inc",
        "PALA Mediterranean Kitchen",
        "Hummus Vegas & Grill (Hollywood)",
        "Zuka Miami",
        "Grand Cafe Aventura",
        "Dabush",
        "Traditions South LLC",
        "La Vita é Bella",
        "G7 Hospitality",
        "The Cafe Maison la Fleur & Dunwell Pizza",
        "Bagel Boss (JCC)",
        "Lasso Kosher Grill",
        "Sushi Addicts",
        "Gifted Crust Pizza",
        "Yumm Sushi",
        "Ariel's Bamboo Kitchen",
        "Bambu Pan Asian Kitchen (Boca)",
        "Smash House Burgers Miami",
        "Pita Plus Hollywood",
        "Joe's Pizza",
        "Glatt Miami",
        "Grill Place",
        "The W Kosher Steakhouse",
        "Panini / Panino Kosher Hollywood",
        "Subaba Subs",
        "Bagel Boss Aventura (NMB)",
        "Smash House Burgers Boca",
        "Shipudim",
        "Mizrachi's Pizza Kitchen in KC Boynton Beach",
        "Yummy Pizza",
        "Pita Lee",
        "Rita's (in KC Market)",
        "BREADS & CO",
        "Oasis Pizzeria & Bakery",
        "Bagel Boss (Miami Beach)",
        "Hollywood Sara's Pizza",
        "Knights Table Diner",
        "Mizrachi's Pizza in KC Hallandale",
        "A La Carte",
        "Street Bar Surfside",
        "Gifted Pizza (Food Truck)",
        "Sakura Poke and Omakase LLC",
        "Panini / Panino Kosher Surfside",
        "Avi's Grill, Inc.",
        "Urban Fine Street Food",
        "Bambu Hollywood - Shanghai 18",
        "Chayhana Samarkand",
        "Puya Urban Cantina LLC",
        "Bagel Boss (Surfside)",
        "Bagel Boss Boca Raton",
        "Ben Yehuda Grill",
        "BOUTIQUE CAFE"
    ]
    
    updated_chalav = 0
    updated_pas = 0
    dairy_count = 0
    meat_pareve_count = 0
    
    print("🥛 Updating Chalav Yisroel/Chalav Stam status for dairy restaurants...")
    print("🍞 Updating Pas Yisroel status for meat/pareve restaurants...")
    
    for restaurant in restaurants:
        restaurant_name = restaurant.get('name', '')
        kosher_category = restaurant.get('kosher_category', '')
        
        # Handle dairy restaurants (Chalav Yisroel vs Chalav Stam)
        if kosher_category == 'dairy':
            dairy_count += 1
            
            # Check if it should be Cholov Stam
            if restaurant_name in cholov_stam_restaurants:
                if restaurant.get('is_cholov_yisroel'):
                    restaurant['is_cholov_yisroel'] = False
                    print(f"✅ {restaurant_name}: Set to Chalav Stam")
                    updated_chalav += 1
                else:
                    print(f"ℹ️  {restaurant_name}: Already Chalav Stam")
            
            # All other dairy restaurants should be Cholov Yisroel
            else:
                if not restaurant.get('is_cholov_yisroel'):
                    restaurant['is_cholov_yisroel'] = True
                    print(f"✅ {restaurant_name}: Set to Chalav Yisroel")
                    updated_chalav += 1
                else:
                    print(f"ℹ️  {restaurant_name}: Already Chalav Yisroel")
        
        # Handle meat and pareve restaurants (Pas Yisroel)
        elif kosher_category in ['meat', 'pareve']:
            meat_pareve_count += 1
            
            # Check if it should have Pas Yisroel
            if restaurant_name in pas_yisroel_restaurants:
                if not restaurant.get('is_pas_yisroel'):
                    restaurant['is_pas_yisroel'] = True
                    print(f"✅ {restaurant_name}: Set to Pas Yisroel")
                    updated_pas += 1
                else:
                    print(f"ℹ️  {restaurant_name}: Already Pas Yisroel")
            
            # All other meat/pareve restaurants should NOT have Pas Yisroel
            else:
                if restaurant.get('is_pas_yisroel'):
                    restaurant['is_pas_yisroel'] = False
                    print(f"✅ {restaurant_name}: Set to regular Pas")
                    updated_pas += 1
                else:
                    print(f"ℹ️  {restaurant_name}: Already regular Pas")
    
    print(f"\n📊 Summary:")
    print(f"   - Total dairy restaurants: {dairy_count}")
    print(f"   - Total meat/pareve restaurants: {meat_pareve_count}")
    print(f"   - Updated Chalav status: {updated_chalav}")
    print(f"   - Updated Pas status: {updated_pas}")
    
    # Show final status
    print(f"\n📋 Final Chalav Yisroel Status:")
    dairy_restaurants = [r for r in restaurants if r.get('kosher_category') == 'dairy']
    for restaurant in sorted(dairy_restaurants, key=lambda x: x.get('name', '')):
        name = restaurant.get('name', '')
        status = "Chalav Yisroel" if restaurant.get('is_cholov_yisroel') else "Chalav Stam"
        print(f"   - {name}: {status}")
    
    print(f"\n📋 Final Pas Yisroel Status:")
    meat_pareve_restaurants = [r for r in restaurants if r.get('kosher_category') in ['meat', 'pareve']]
    for restaurant in sorted(meat_pareve_restaurants, key=lambda x: x.get('name', '')):
        name = restaurant.get('name', '')
        status = "Pas Yisroel" if restaurant.get('is_pas_yisroel') else "Regular Pas"
        print(f"   - {name}: {status}")
    
    return save_local_data(restaurants)

if __name__ == "__main__":
    print("🥛🍞 Fix Chalav Yisroel and Pas Yisroel Status in Local Data")
    print("=" * 60)
    
    if fix_kosher_status():
        print("\n🎉 Successfully updated Chalav Yisroel and Pas Yisroel status!")
    else:
        print("\n❌ Failed to update kosher status.") 