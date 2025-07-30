#!/usr/bin/env python3
"""
Fix Remaining Restaurants - Handle 500 errors with aggressive data cleaning
"""

import json
import requests
import time
import re
from datetime import datetime

def get_failing_restaurants():
    """Get list of restaurants that failed to import"""
    # These are the restaurants that failed with 500 errors from the previous run
    failing_names = [
        "A La Carte", "Appetite Foods", "Ariel's Delicious Pizza", "BOUTIQUE CAFE", 
        "Bagel Boss (Surfside)", "Bagel Boss Aventura (NMB)", "Bissli Grill", 
        "Boca Grill", "Brendy's", "Brendy's - Yogurt & Ice Cream", "Cafe Noir", 
        "Carmela's Boca", "Carnicery", "Carvel (Boca East #3351)", "Carvel (Boca West #2183)", 
        "Carvel (NMB #1657)", "Century Grill", "Cuisine Art @ The Altair", "Dabush", 
        "Danzinger Kosher Catering", "Ditmas Kitchen and Cocktail", "Dunkin Donuts - Hollywood", 
        "Flavors Catering", "Forty One", "Friendship Cafe & Catering", "G7 Hospitality", 
        "Gifted Crust Pizza", "Gifted Pizza (Food Truck)", "Glatt Miami", "Glyk Gelato", 
        "Gold Kosher Catering (Dairy)", "Grand Cafe Aventura", "Grand Cafe Hollywood", 
        "Grill Place", "Grill Xpress", "Hollywood Sara's Pizza", "Hummus Vegas & Grill (Hollywood)", 
        "JZ Steakhouse", "Joe's Pizza", "Juicylicious Bar LLC", "Katai Sushi Express", 
        "King David Catering (Dairy)", "Kosher Bagel Cove", "Kosher Chobee", "Kosher Gourmet By Jacob", 
        "Kosher Ice Cream Parlor", "Kosher Palate", "Kosher from Z Heart", "Krispy Kreme #4259", 
        "Krispy Kreme #4273", "Krispy Kreme #4325", "Krispy Kreme #4339", "Krispy Kreme #4341", 
        "Krispy Kreme #4392", "Krispy Kreme #4457", "Lenny's Pizza (Boca)", "Lox N Bagel (Bagel Factory Cafe)", 
        "Meat Bar Butcher", "Menchie's Frozen Yogurt", "Miami Alkaline Water", "Miami Beach Chocolates - Surfside", 
        "Miami Fresh Fish Market", "Miami Kosher Bakery", "Miami Kosher Butcher", "Miami Kosher Catering", 
        "Miami Kosher Deli", "Miami Kosher Pizza", "Miami N Ice Events", "Miami N' Ice LLC", 
        "Mizrachi's Pizza Kitchen in KC Boynton Beach", "Mizrachi's Pizza in Hollywood", 
        "Mizrachi's Pizza in KC Hallandale", "Mozart Cafe Sunny Isles Inc", "Nava's Kosher Kitchen - Restaurant", 
        "Neya", "Nothing Bundt Cakes - ONLY this location", "Nothing Bundt Cakes - ONLY this location.", 
        "OVO at The Altair", "Oak and Ember", "Oakberry Surfside - THIS LOCATION ONLY", 
        "Oasis Pizzeria & Bakery", "Oki Miami", "Orchid's Garden", "Ostrow Brasserie", 
        "PALA Mediterranean Kitchen", "PX Grill Mediterranean Cuisine", "Panini / Panino Kosher Hollywood", 
        "Panini / Panino Kosher Surfside", "Pita Hut-Miami", "Pita Hut-North Miami Beach", 
        "Pita Lee", "Pita Loca", "Pita Plus Hollywood", "Pizza Biza", "Plantation Pita & Grill", 
        "Pure Green Aventura", "Pure Green Florida Garden Shops Corp", "Puya Urban Cantina LLC", 
        "Rave Pizza & Sushi", "Sage Dining Services at David Posnack Jewish Day School (JCC)", 
        "Sakura Poke and Omakase LLC", "Salt And Pepper", "Shalom Haifa", "Shipudim", 
        "Smash House Burgers Boca", "Smash House Burgers Miami", "Sobol Boca Raton", 
        "Street Bar Surfside", "Subaba Subs", "Sunrise Pita & Grill (Davie)", "Sushi Addicts", 
        "Sushi House", "Tagine by Alma Grill", "Temptings, LLC", "Test Kosher Restaurant", 
        "The Cafe Maison la Fleur & Dunwell Pizza", "The Cave Kosher Bar & Grill", 
        "The Coffee Ark Cart, Cafe and Catering", "The Ice Cream Club", "The Sweet Tooth", 
        "The W Kosher Steakhouse", "Thin Slim Foods", "Toast 770 (Inside Mobile Gas Station)", 
        "Toasted", "Totally Bananas", "Traditions South LLC", "TreeHouse Sweets"
    ]
    return set(failing_names)

def clean_text_field(text, max_length=255):
    """Clean text field to prevent validation issues"""
    if not text:
        return ""
    
    # Convert to string
    text = str(text)
    
    # Remove any non-printable characters except newlines and tabs
    text = re.sub(r'[^\x20-\x7E\n\t]', '', text)
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Trim
    text = text.strip()
    
    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length-3] + "..."
    
    return text

def clean_phone_number(phone):
    """Clean phone number field"""
    if not phone:
        return ""
    
    phone = str(phone)
    
    # Remove all non-digit characters except + and -
    phone = re.sub(r'[^\d+\-\(\)\s]', '', phone)
    
    # Remove excessive whitespace
    phone = re.sub(r'\s+', ' ', phone)
    
    # Trim
    phone = phone.strip()
    
    # Limit length
    if len(phone) > 50:
        phone = phone[:50]
    
    return phone

def clean_website_url(url):
    """Clean website URL field"""
    if not url:
        return ""
    
    url = str(url)
    
    # Remove any non-printable characters
    url = re.sub(r'[^\x20-\x7E]', '', url)
    
    # Ensure it starts with http:// or https://
    if url and not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Limit length
    if len(url) > 500:
        url = url[:500]
    
    return url

def load_and_aggressively_clean_restaurant_data():
    """Load and aggressively clean restaurant data"""
    print("📂 Loading and aggressively cleaning restaurant data")
    
    try:
        with open('local_restaurants.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        restaurants = data.get('restaurants', [])
        failing_names = get_failing_restaurants()
        
        # Get existing restaurants to skip them
        try:
            response = requests.get("https://jewgo.onrender.com/api/restaurants?limit=1000", timeout=30)
            if response.status_code == 200:
                data = response.json()
                existing = data.get('data', [])
                existing_ids = {restaurant.get('business_id') for restaurant in existing}
                print(f"📊 Found {len(existing)} existing restaurants")
            else:
                existing_ids = set()
        except:
            existing_ids = set()
        
        # Filter to only failing restaurants
        failing_restaurants = []
        
        for restaurant in restaurants:
            business_id = restaurant.get('business_id', '')
            name = restaurant.get('name', '')
            
            # Skip if already exists
            if business_id in existing_ids:
                continue
            
            # Only process failing restaurants
            if name in failing_names:
                failing_restaurants.append(restaurant)
        
        print(f"📊 Found {len(failing_restaurants)} failing restaurants to retry")
        
        # Format and aggressively clean the data
        formatted_restaurants = []
        
        for restaurant in failing_restaurants:
            business_id = restaurant.get('business_id', '')
            
            # Generate business_id if missing
            if not business_id:
                business_id = f"auto_{len(formatted_restaurants) + 1}"
            
            # Aggressively clean all text fields
            formatted_restaurant = {
                'business_id': clean_text_field(business_id, 255),
                'name': clean_text_field(restaurant.get('name', ''), 255),
                'website_link': clean_website_url(restaurant.get('website_link') or restaurant.get('website', '')),
                'phone_number': clean_phone_number(restaurant.get('phone_number', '')),
                'address': clean_text_field(restaurant.get('address', ''), 500),
                'city': clean_text_field(restaurant.get('city', ''), 100),
                'state': clean_text_field(restaurant.get('state', ''), 50),
                'zip_code': clean_text_field(restaurant.get('zip_code', ''), 20),
                'certificate_link': clean_website_url(restaurant.get('certificate_link', '')),
                'image_url': clean_website_url(restaurant.get('image_url', '')),
                'certifying_agency': 'ORB',  # Default to ORB for all
                'kosher_category': 'unknown',  # Default to unknown
                'listing_type': 'restaurant',
                'status': 'active',
                'rating': None,  # Set to None to avoid validation issues
                'price_range': clean_text_field(restaurant.get('price_range', ''), 50),
                'hours_of_operation': clean_text_field(restaurant.get('hours_of_operation', ''), 500),
                'short_description': clean_text_field(restaurant.get('short_description', ''), 1000),
                'notes': clean_text_field(restaurant.get('notes', ''), 1000),
                'latitude': None,  # Set to None to avoid validation issues
                'longitude': None,  # Set to None to avoid validation issues
                'data_source': 'manual',
                'external_id': clean_text_field(restaurant.get('external_id', ''), 255)
            }
            
            # Ensure required fields have minimum values
            if not formatted_restaurant['name']:
                formatted_restaurant['name'] = f"Restaurant {formatted_restaurant['business_id']}"
            
            if not formatted_restaurant['city']:
                formatted_restaurant['city'] = 'Unknown'
            
            if not formatted_restaurant['state']:
                formatted_restaurant['state'] = 'FL'
            
            formatted_restaurants.append(formatted_restaurant)
        
        print(f"✅ Prepared {len(formatted_restaurants)} cleaned restaurants for retry")
        return formatted_restaurants
        
    except Exception as e:
        print(f"❌ Error loading restaurant data: {e}")
        return []

def retry_failed_restaurants(restaurants, batch_size=3):
    """Retry failed restaurants with smaller batches and longer delays"""
    print(f"🔄 Retrying {len(restaurants)} failed restaurants in batches of {batch_size}")
    
    total_restaurants = len(restaurants)
    successful_imports = 0
    failed_imports = 0
    
    for i in range(0, total_restaurants, batch_size):
        batch = restaurants[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total_restaurants + batch_size - 1) // batch_size
        
        print(f"\n📦 Processing batch {batch_num}/{total_batches} ({len(batch)} restaurants)")
        
        batch_success = 0
        batch_failures = 0
        
        for j, restaurant in enumerate(batch):
            restaurant_num = i + j + 1
            
            try:
                # Add restaurant via API
                response = requests.post(
                    "https://jewgo.onrender.com/api/admin/restaurants",
                    json=restaurant,
                    timeout=30
                )
                
                if response.status_code == 200:
                    print(f"✅ [{restaurant_num}/{total_restaurants}] Added: {restaurant['name']}")
                    successful_imports += 1
                    batch_success += 1
                elif response.status_code == 409:
                    print(f"⏭️  [{restaurant_num}/{total_restaurants}] Already exists: {restaurant['name']}")
                    successful_imports += 1
                    batch_success += 1
                else:
                    print(f"❌ [{restaurant_num}/{total_restaurants}] Failed ({response.status_code}): {restaurant['name']}")
                    batch_failures += 1
                    failed_imports += 1
                    
            except Exception as e:
                print(f"❌ [{restaurant_num}/{total_restaurants}] Error: {restaurant['name']} - {e}")
                batch_failures += 1
                failed_imports += 1
            
            # Longer delay between requests for retry
            time.sleep(3)
        
        # Print batch summary
        print(f"📊 Batch {batch_num} summary: {batch_success} success, {batch_failures} failures")
        
        # Longer delay between batches for retry
        if batch_num < total_batches:
            print("⏳ Waiting 10 seconds before next batch...")
            time.sleep(10)
    
    return {
        'successful': successful_imports,
        'failed': failed_imports,
        'total': total_restaurants
    }

def main():
    """Main function to retry failed restaurants"""
    print("🔄 Retrying Failed Restaurants with Aggressive Data Cleaning")
    print("=" * 60)
    
    # Load and clean restaurant data
    restaurants = load_and_aggressively_clean_restaurant_data()
    
    if not restaurants:
        print("✅ No failed restaurants to retry - all done!")
        return
    
    # Retry failed restaurants
    results = retry_failed_restaurants(restaurants, batch_size=3)
    
    # Print summary
    print("\n📊 Retry Summary")
    print("=" * 30)
    print(f"✅ Successfully imported: {results['successful']}")
    print(f"❌ Still failed: {results['failed']}")
    print(f"📋 Total retried: {results['total']}")
    
    # Final verification
    try:
        response = requests.get("https://jewgo.onrender.com/api/restaurants?limit=1000", timeout=30)
        if response.status_code == 200:
            data = response.json()
            restaurants = data.get('data', [])
            print(f"\n🎉 Final restaurant count: {len(restaurants)}")
            
            if len(restaurants) >= 200:
                print("🎊 SUCCESS! We now have 200+ restaurants in the database!")
                print("🌐 The application is ready with the full dataset.")
            else:
                print(f"📊 Progress: {len(restaurants)}/200+ restaurants imported")
        else:
            print(f"❌ Could not verify final count: {response.status_code}")
    except Exception as e:
        print(f"❌ Error verifying final count: {e}")

if __name__ == "__main__":
    main() 