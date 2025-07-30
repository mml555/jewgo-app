#!/usr/bin/env python3
"""
Manual ORB Data Entry
Populates database with core restaurant information from ORB website.
Based on the ORB Dairy category data provided by the user.
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database_manager_v3 import DatabaseManager

def populate_orb_dairy_restaurants():
    """Populate database with ORB Dairy restaurants."""
    
    # ORB Dairy restaurants data from the user's screenshot
    dairy_restaurants = [
        {
            "name": "Grand Cafe Hollywood",
            "address": "2905 Stirling Rd, Fort Lauderdale, FL 33312",
            "phone": "954-986-6860",
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher",
            "extra_kosher_info": "Cholov Yisroel, Pas Yisroel"
        },
        {
            "name": "Yum Berry Cafe & Sushi Bar",
            "address": "4009 Oakwood Blvd, Hollywood, FL 33020",
            "phone": "954-922-7876",
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher",
            "extra_kosher_info": "Cholov Yisroel, Pas Yisroel"
        },
        {
            "name": "Mizrachi's Pizza in Hollywood",
            "address": "5650 Stirling Rd, Hollywood, FL 33021",
            "phone": "954-505-3190",
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher",
            "extra_kosher_info": "Pas Yisroel"
        },
        {
            "name": "Cafe 95 at JARC",
            "address": "21160 95th Ave South, Boca 33428",
            "phone": "561-558-2550",
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher",
            "extra_kosher_info": "Cholov Yisroel, Bishul Yisroel"
        },
        {
            "name": "Hollywood Deli",
            "address": "6100 Hollywood Blvd, Hollywood FL 33024",
            "phone": "954-986-7570",
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Jon's Place",
            "address": "22191 Powerline Rd, Boca Raton, FL 33434",
            "phone": "561-338-0008",
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Lox N Bagel (Bagel Factory Cafe)",
            "address": "21065 Powerline Road, Ste A-6, Boca Raton, FL 33487",
            "phone": None,
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Kosher Bagel Cove",
            "address": "668 W Hallandale Beach Blvd, Hallandale Beach, FL 33009",
            "phone": "754-999-8999",
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Cafe Noir",
            "address": "3000 Stirling Rd, Unit 112 Hollywood, FL 33021",
            "phone": "954-584-5171",
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Sobol Boca Raton",
            "address": "9224 Glades Rd, Boca Raton, FL 33434",
            "phone": None,
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Carmela's Boca",
            "address": "7300 W Camino Real, Boca Raton, FL 33433",
            "phone": "561-367-3412",
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Ariel's Delicious Pizza",
            "address": "3330 Griffin Rd, Fort Lauderdale, FL 33312",
            "phone": "754-888-9262",
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Sobol Boynton Beach",
            "address": "6691 W Boynton Beach Blvd, Boynton Beach, FL 33437",
            "phone": "516-779-1381",
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Lenny's Pizza (Boca)",
            "address": "9070 Kimberly Blvd, STE 26, Boca Raton, FL 33434",
            "phone": None,
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Mozart Cafe Sunny Isles Inc",
            "address": "18110 Collins Ave, Sunny Isles Beach, FL 33160",
            "phone": None,
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Zuka Miami",
            "address": "900 N Federal Highway, Hollywood, FL 33020",
            "phone": "954-880-4197",
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Grand Cafe Aventura",
            "address": "2491 NE 186th St, Miami, FL 33180",
            "phone": None,
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "La Vita é Bella",
            "address": "9485 Harding Ave, Surfside, FL 33154",
            "phone": "305-603-9248",
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "The Cafe Maison la Fleur & Dunwell Pizza",
            "address": "2906 NE 207th St, Aventura, FL 33180",
            "phone": None,
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Gifted Crust Pizza",
            "address": "9523 Harding Ave, Surfside, FL 33154",
            "phone": None,
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Joe's Pizza",
            "address": "3288 Stirling Rd, Hollywood, FL 33021",
            "phone": None,
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Bagel Boss Aventura (NMB)",
            "address": "18549 W Dixie Hwy, Aventura, FL 33180",
            "phone": None,
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Mizrachi's Pizza Kitchen in KC Boynton Beach",
            "address": "3775 Woolbright Rd, Boynton Beach, FL 33436",
            "phone": None,
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Yummy Pizza",
            "address": "730 W Hallandale Beach Blvd, Hallandale Beach, FL 33009",
            "phone": "754-465-5873",
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Rita's (in KC Market)",
            "address": "5650 Stirling Rd, Hollywood, FL 33021",
            "phone": None,
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Oasis Pizzeria & Bakery",
            "address": "5810 S University Dr #104, Davie, FL 33328",
            "phone": "954-681-6706",
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Hollywood Sara's Pizza",
            "address": "3944 N 46th Ave, Hollywood, FL 33021",
            "phone": None,
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Mizrachi's Pizza in KC Hallandale",
            "address": "1002 E Hallandale Beach Blvd, Hallandale Beach, FL 33009",
            "phone": None,
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "A La Carte",
            "address": "613 W Hallandale Beach Blvd #7, Hallandale Beach, FL 33009",
            "phone": None,
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Toast 770 (Inside Mobile Gas Station)",
            "address": "3991 Stirling Rd, Fort Lauderdale, FL 33312",
            "phone": "305-896-8668",
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Gifted Pizza (Food Truck)",
            "address": "96th St & The Beach, Surfside, FL 33155",
            "phone": None,
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Bagel Boss (Surfside)",
            "address": "9543 Harding Ave, Surfside, FL 33154",
            "phone": None,
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "Bagel Boss Boca Raton",
            "address": "22107 Powerline Rd, Boca Raton, FL, 33433",
            "phone": "754-264-8120",
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        },
        {
            "name": "BOUTIQUE CAFE",
            "address": "3558 N Ocean Blvd, Fort Lauderdale, FL 33308",
            "phone": "954-280-0500",
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher"
        }
    ]
    
    try:
        print("Starting ORB Dairy restaurants data entry...")
        
        db_manager = DatabaseManager()
        
        success_count = 0
        update_count = 0
        
        for restaurant in dairy_restaurants:
            try:
                # Check if restaurant already exists
                existing = db_manager.get_restaurant_by_name(restaurant['name'])
                
                if existing:
                    # Update existing restaurant with ORB data
                    success = db_manager.update_restaurant_orb_data(
                        existing['id'],
                        restaurant['address'],
                        restaurant['kosher_type'],
                        restaurant['certifying_agency'],
                        restaurant.get('extra_kosher_info')
                    )
                    if success:
                        update_count += 1
                        print(f"✅ Updated: {restaurant['name']}")
                    else:
                        print(f"❌ Failed to update: {restaurant['name']}")
                else:
                    # Create new restaurant
                    success = db_manager.add_restaurant_simple(
                        name=restaurant['name'],
                        address=restaurant['address'],
                        phone_number=restaurant['phone'],
                        kosher_type=restaurant['kosher_type'],
                        certifying_agency=restaurant['certifying_agency'],
                        extra_kosher_info=restaurant.get('extra_kosher_info'),
                        source='orb'
                    )
                    if success:
                        success_count += 1
                        print(f"✅ Added: {restaurant['name']}")
                    else:
                        print(f"❌ Failed to add: {restaurant['name']}")
                
            except Exception as e:
                print(f"❌ Error processing {restaurant['name']}: {e}")
        
        print(f"\n🎉 Data entry completed!")
        print(f"✅ Added: {success_count} new restaurants")
        print(f"✅ Updated: {update_count} existing restaurants")
        print(f"📊 Total processed: {len(dairy_restaurants)} restaurants")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during data entry: {e}")
        return False

def main():
    """Main function."""
    print("🍕 ORB Dairy Restaurants Data Entry")
    print("=" * 50)
    
    success = populate_orb_dairy_restaurants()
    
    if success:
        print("\n✅ All ORB Dairy restaurants have been added to the database!")
        print("🔍 You can now check the API to see the kosher type information.")
    else:
        print("\n❌ Data entry failed. Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    main() 