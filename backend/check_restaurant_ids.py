#!/usr/bin/env python3
"""
Check Restaurant IDs Script
==========================

This script checks the database to see which restaurant IDs exist and identifies any gaps.
This helps debug 404 errors for specific restaurant IDs.

Author: JewGo Development Team
Version: 1.0
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from database.database_manager_v3 import EnhancedDatabaseManager, Restaurant
    from sqlalchemy import func
except ImportError as e:
    print(f"Error importing database modules: {e}")
    print("Make sure you're running this script from the backend directory")
    sys.exit(1)

def check_restaurant_ids():
    """Check restaurant IDs in the database."""
    try:
        # Initialize database manager
        db_manager = EnhancedDatabaseManager()
        db_manager.connect()
        
        # Get database session
        session = db_manager.get_session()
        
        # Get all restaurant IDs
        restaurant_ids = session.query(Restaurant.id).order_by(Restaurant.id).all()
        
        if not restaurant_ids:
            print("No restaurants found in the database!")
            return
        
        # Convert to list of integers
        ids = [r[0] for r in restaurant_ids]
        
        print(f"Found {len(ids)} restaurants in the database")
        print(f"ID range: {min(ids)} to {max(ids)}")
        
        # Check for gaps
        gaps = []
        for i in range(min(ids), max(ids) + 1):
            if i not in ids:
                gaps.append(i)
        
        if gaps:
            print(f"\nFound {len(gaps)} gaps in restaurant IDs:")
            print(f"Missing IDs: {gaps}")
        else:
            print("\nNo gaps found in restaurant IDs")
        
        # Show some sample restaurants
        print(f"\nSample restaurants:")
        sample_restaurants = session.query(Restaurant.id, Restaurant.name).limit(10).all()
        for restaurant_id, name in sample_restaurants:
            print(f"  ID {restaurant_id}: {name}")
        
        # Check if ID 1262 exists specifically
        restaurant_1262 = session.query(Restaurant).filter(Restaurant.id == 1262).first()
        if restaurant_1262:
            print(f"\nRestaurant ID 1262 exists: {restaurant_1262.name}")
        else:
            print(f"\nRestaurant ID 1262 does NOT exist")
            print(f"Closest IDs:")
            # Find closest IDs
            lower_id = session.query(Restaurant.id).filter(Restaurant.id < 1262).order_by(Restaurant.id.desc()).first()
            higher_id = session.query(Restaurant.id).filter(Restaurant.id > 1262).order_by(Restaurant.id.asc()).first()
            
            if lower_id:
                print(f"  Lower: ID {lower_id[0]}")
            if higher_id:
                print(f"  Higher: ID {higher_id[0]}")
        
        session.close()
        
    except Exception as e:
        print(f"Error checking restaurant IDs: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Checking restaurant IDs in the database...")
    check_restaurant_ids() 