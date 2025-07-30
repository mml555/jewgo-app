#!/usr/bin/env python3
"""
Populate Production Database Script
This script connects to the production database and populates it with restaurant data.
"""

import os
import psycopg2
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def connect_to_production_db():
    """Connect to the production database."""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("Error: DATABASE_URL environment variable not set")
        return None
    
    try:
        conn = psycopg2.connect(database_url)
        return conn
    except Exception as e:
        print(f"Error connecting to production database: {e}")
        return None

def get_local_restaurants():
    """Get restaurant data from local database."""
    local_db_url = os.environ.get('DATABASE_URL')
    if not local_db_url:
        print("Error: DATABASE_URL environment variable not set")
        return []
    
    try:
        conn = psycopg2.connect(local_db_url)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, address, city, state, zip_code, phone, website, 
                   hechsher_details, cuisine_type, hours, description, price_range, 
                   image_url, latitude, longitude, rating, review_count, 
                   google_rating, google_review_count, google_reviews, 
                   created_at, updated_at
            FROM restaurants 
            ORDER BY id
        """)
        
        restaurants = []
        for row in cursor.fetchall():
            restaurant = {
                'id': row[0],
                'name': row[1],
                'address': row[2],
                'city': row[3],
                'state': row[4],
                'zip_code': row[5],
                'phone': row[6],
                'website': row[7],
                'hechsher_details': row[8],
                'cuisine_type': row[9],
                'hours': row[10],
                'description': row[11],
                'price_range': row[12],
                'image_url': row[13],
                'latitude': row[14],
                'longitude': row[15],
                'rating': row[16],
                'review_count': row[17],
                'google_rating': row[18],
                'google_review_count': row[19],
                'google_reviews': row[20],
                'created_at': row[21],
                'updated_at': row[22]
            }
            restaurants.append(restaurant)
        
        conn.close()
        return restaurants
        
    except Exception as e:
        print(f"Error getting local restaurants: {e}")
        return []

def populate_production_database():
    """Populate the production database with restaurant data."""
    print("🚀 Starting Production Database Population...")
    print("=" * 50)
    
    # Connect to production database
    prod_conn = connect_to_production_db()
    if not prod_conn:
        print("❌ Failed to connect to production database")
        return
    
    # Get local restaurant data
    print("📊 Fetching local restaurant data...")
    local_restaurants = get_local_restaurants()
    
    if not local_restaurants:
        print("❌ No local restaurant data found")
        return
    
    print(f"📊 Found {len(local_restaurants)} local restaurants")
    
    # Check production database
    prod_cursor = prod_conn.cursor()
    prod_cursor.execute("SELECT COUNT(*) FROM restaurants")
    prod_count = prod_cursor.fetchone()[0]
    print(f"📊 Production database has {prod_count} restaurants")
    
    if prod_count > 0:
        print("⚠️  Production database already has data!")
        response = input("Do you want to continue and add more restaurants? (y/n): ")
        if response.lower() != 'y':
            print("❌ Operation cancelled")
            return
    
    # Insert restaurants
    print("\n🔄 Inserting restaurants into production database...")
    
    success_count = 0
    error_count = 0
    
    for i, restaurant in enumerate(local_restaurants, 1):
        try:
            # Prepare the insert query
            query = """
                INSERT INTO restaurants (
                    id, name, address, city, state, zip_code, phone, website,
                    hechsher_details, cuisine_type, hours, description, price_range,
                    image_url, latitude, longitude, rating, review_count,
                    google_rating, google_review_count, google_reviews,
                    created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                ) ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    address = EXCLUDED.address,
                    city = EXCLUDED.city,
                    state = EXCLUDED.state,
                    zip_code = EXCLUDED.zip_code,
                    phone = EXCLUDED.phone,
                    website = EXCLUDED.website,
                    hechsher_details = EXCLUDED.hechsher_details,
                    cuisine_type = EXCLUDED.cuisine_type,
                    hours = EXCLUDED.hours,
                    description = EXCLUDED.description,
                    price_range = EXCLUDED.price_range,
                    image_url = EXCLUDED.image_url,
                    latitude = EXCLUDED.latitude,
                    longitude = EXCLUDED.longitude,
                    rating = EXCLUDED.rating,
                    review_count = EXCLUDED.review_count,
                    google_rating = EXCLUDED.google_rating,
                    google_review_count = EXCLUDED.google_review_count,
                    google_reviews = EXCLUDED.google_reviews,
                    updated_at = EXCLUDED.updated_at
            """
            
            values = (
                restaurant['id'], restaurant['name'], restaurant['address'],
                restaurant['city'], restaurant['state'], restaurant['zip_code'],
                restaurant['phone'], restaurant['website'], restaurant['hechsher_details'],
                restaurant['cuisine_type'], restaurant['hours'], restaurant['description'],
                restaurant['price_range'], restaurant['image_url'], restaurant['latitude'],
                restaurant['longitude'], restaurant['rating'], restaurant['review_count'],
                restaurant['google_rating'], restaurant['google_review_count'],
                restaurant['google_reviews'], restaurant['created_at'], restaurant['updated_at']
            )
            
            prod_cursor.execute(query, values)
            success_count += 1
            
            if i % 10 == 0:
                print(f"   ✅ Processed {i}/{len(local_restaurants)} restaurants")
                
        except Exception as e:
            error_count += 1
            print(f"   ❌ Error inserting {restaurant['name']}: {e}")
    
    # Commit changes
    prod_conn.commit()
    prod_conn.close()
    
    print("\n📊 Population Results:")
    print(f"   ✅ Successfully inserted: {success_count}")
    print(f"   ❌ Errors: {error_count}")
    print(f"   📊 Total processed: {len(local_restaurants)}")
    
    if success_count > 0:
        print("\n🎉 Production database populated successfully!")
        print("🌐 The website should now show restaurant data.")
    else:
        print("\n❌ Failed to populate production database")

if __name__ == "__main__":
    populate_production_database() 