#!/usr/bin/env python3
"""
Export Restaurant Data Script
This script exports restaurant data from the local database to a JSON file.
"""

import os
import psycopg2
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def export_restaurant_data():
    """Export restaurant data from local database to JSON file."""
    print("🚀 Starting Restaurant Data Export...")
    print("=" * 50)
    
    # Connect to local database
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("Error: DATABASE_URL environment variable not set")
        return
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Get all restaurants
        cursor.execute("""
            SELECT id, name, address, city, state, zip_code, phone, website, 
                   hechsher_details, cuisine_type, hours_of_operation, description, price_range, 
                   image_url, latitude, longitude, rating, review_count, 
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
                'hours_of_operation': row[10],
                'description': row[11],
                'price_range': row[12],
                'image_url': row[13],
                'latitude': row[14],
                'longitude': row[15],
                'rating': row[16],
                'review_count': row[17],
                'created_at': row[18].isoformat() if row[18] else None,
                'updated_at': row[19].isoformat() if row[19] else None
            }
            restaurants.append(restaurant)
        
        conn.close()
        
        print(f"📊 Found {len(restaurants)} restaurants")
        
        # Create export data
        export_data = {
            'export_date': datetime.now().isoformat(),
            'total_restaurants': len(restaurants),
            'restaurants': restaurants
        }
        
        # Save to JSON file
        filename = f"restaurant_data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Data exported to {filename}")
        print(f"📊 Total restaurants: {len(restaurants)}")
        
        # Show sample data
        if restaurants:
            print("\n📋 Sample restaurant data:")
            sample = restaurants[0]
            print(f"   Name: {sample['name']}")
            print(f"   Address: {sample['address']}")
            print(f"   Hours: {sample['hours_of_operation']}")
            print(f"   Category: {sample['cuisine_type']}")
        
        return filename
        
    except Exception as e:
        print(f"❌ Error exporting data: {e}")
        return None

if __name__ == "__main__":
    export_restaurant_data() 