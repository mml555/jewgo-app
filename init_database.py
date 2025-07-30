#!/usr/bin/env python3
"""
Database Initialization Script
This script populates the production database with restaurant data when the backend starts.
"""

import os
import json
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

def init_database():
    """Initialize the database with restaurant data if it's empty."""
    print("🚀 Starting database initialization...")
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("Error: DATABASE_URL environment variable not set")
        return False
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Check if database is empty
        cursor.execute("SELECT COUNT(*) FROM restaurants")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"✅ Database already has {count} restaurants. Skipping initialization.")
            conn.close()
            return True
        
        print("📝 Database is empty. Loading restaurant data...")
        
        # Load restaurant data from JSON file
        json_file = "restaurant_data_export_20250730_095036.json"
        if not os.path.exists(json_file):
            print(f"❌ Restaurant data file {json_file} not found")
            conn.close()
            return False
        
        with open(json_file, 'r') as f:
            restaurants_data = json.load(f)
        
        print(f"📊 Loading {len(restaurants_data)} restaurants...")
        
        # Insert restaurants
        for restaurant in restaurants_data:
            cursor.execute("""
                INSERT INTO restaurants (
                    name, address, city, state, zip_code, phone, website,
                    hechsher_details, cuisine_type, hours_of_operation, description,
                    price_range, image_url, latitude, longitude, rating, review_count,
                    google_rating, google_review_count, google_reviews, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                restaurant['name'],
                restaurant['address'],
                restaurant['city'],
                restaurant['state'],
                restaurant['zip_code'],
                restaurant['phone'],
                restaurant['website'],
                restaurant['hechsher_details'],
                restaurant['cuisine_type'],
                restaurant['hours_of_operation'],
                restaurant['description'],
                restaurant['price_range'],
                restaurant['image_url'],
                restaurant['latitude'],
                restaurant['longitude'],
                restaurant['rating'],
                restaurant['review_count'],
                restaurant['google_rating'],
                restaurant['google_review_count'],
                restaurant['google_reviews'],
                restaurant['created_at'],
                restaurant['updated_at']
            ))
        
        conn.commit()
        print(f"✅ Successfully loaded {len(restaurants_data)} restaurants into database")
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        if 'conn' in locals():
            conn.close()
        return False

if __name__ == "__main__":
    init_database() 