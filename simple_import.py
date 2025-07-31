#!/usr/bin/env python3
"""
Simple import script for ORB Kosher restaurant data.
"""

import os
import json
import sys
from datetime import datetime
from database_manager_v2 import EnhancedDatabaseManager

def import_orb_data(json_file: str):
    """Import ORB restaurant data from JSON file into database."""
    
    # Check if JSON file exists
    if not os.path.exists(json_file):
        print(f"Error: JSON file '{json_file}' not found.")
        return False
    
    # Initialize database manager
    db_manager = None
    try:
        db_manager = EnhancedDatabaseManager()
        db_manager.connect()
        print("Connected to database successfully.")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return False
    
    try:
        # Load JSON data
        with open(json_file, 'r', encoding='utf-8') as f:
            restaurants = json.load(f)
        
        print(f"Loaded {len(restaurants)} restaurants from {json_file}")
        
        # Import restaurants
        imported_count = 0
        skipped_count = 0
        error_count = 0
        
        for i, restaurant in enumerate(restaurants, 1):
            try:
                # Check if restaurant already exists
                existing = db_manager.search_restaurants(
                    query=restaurant['name'],
                    limit=1
                )
                
                if existing:
                    print(f"[{i}/{len(restaurants)}] Skipped (exists): {restaurant['name']}")
                    skipped_count += 1
                    continue
                
                # Prepare restaurant data for database
                db_restaurant = {
                    'name': restaurant['name'],
                    'address': restaurant['address'],
                    'city': restaurant['city'],
                    'state': restaurant['state'],
                    'zip_code': restaurant['zip_code'],
                    'phone': restaurant['phone'],
                    'website': restaurant['website'],
                    'cuisine_type': restaurant['cuisine_type'],
                    'description': restaurant['description'],
                    'image_url': restaurant['image_url'],
                    'hechsher_details': restaurant['hechsher_details'],
                    'is_kosher': restaurant['is_kosher'],
                    'is_glatt': restaurant['is_glatt'],
                    'is_cholov_yisroel': restaurant['is_cholov_yisroel'],
                    'is_pas_yisroel': restaurant['is_pas_yisroel'],
                    'is_bishul_yisroel': restaurant['is_bishul_yisroel'],
                    'is_mehadrin': restaurant['is_mehadrin'],
                    'is_hechsher': restaurant['is_hechsher'],
                    'rating': restaurant['rating'],
                    'review_count': restaurant['review_count'],
                    'price_range': restaurant['price_range'],
                    'hours': restaurant['hours'],
                    'created_at': datetime.fromisoformat(restaurant['created_at'].replace('Z', '+00:00')),
                    'updated_at': datetime.fromisoformat(restaurant['updated_at'].replace('Z', '+00:00'))
                }
                
                # Add restaurant to database
                success = db_manager.add_restaurant(db_restaurant)
                
                if success:
                    print(f"[{i}/{len(restaurants)}] Imported: {restaurant['name']}")
                    imported_count += 1
                else:
                    print(f"[{i}/{len(restaurants)}] Failed to import: {restaurant['name']}")
                    error_count += 1
                
            except Exception as e:
                print(f"[{i}/{len(restaurants)}] Error importing {restaurant.get('name', 'Unknown')}: {e}")
                error_count += 1
                continue
        
        # Print summary
        print("\n" + "="*50)
        print("IMPORT SUMMARY")
        print("="*50)
        print(f"Total restaurants in file: {len(restaurants)}")
        print(f"Successfully imported: {imported_count}")
        print(f"Skipped (already exists): {skipped_count}")
        print(f"Errors: {error_count}")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"Error during import: {e}")
        return False
    
    finally:
        if db_manager:
            db_manager.close()

def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python simple_import.py <json_file>")
        print("Example: python simple_import.py orb_restaurants_20250730_182452.json")
        return
    
    json_file = sys.argv[1]
    
    print("ORB Kosher Restaurant Data Import (Simple)")
    print("="*40)
    print(f"Importing from: {json_file}")
    print()
    
    success = import_orb_data(json_file)
    
    if success:
        print("\nImport completed successfully!")
    else:
        print("\nImport failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 