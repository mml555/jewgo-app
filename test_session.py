#!/usr/bin/env python3
"""
Test session creation and database operations.
"""

import os
from database_manager_v2 import EnhancedDatabaseManager

def test_session():
    """Test session creation and basic operations."""
    
    # Set up database URL
    os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
    
    # Create database manager
    db = EnhancedDatabaseManager()
    
    print("1. Testing connection...")
    success = db.connect()
    print(f"Connection result: {success}")
    
    print("2. Checking SessionLocal...")
    print(f"SessionLocal exists: {db.SessionLocal is not None}")
    print(f"SessionLocal type: {type(db.SessionLocal)}")
    
    print("3. Testing get_session...")
    try:
        session = db.get_session()
        print(f"Session created successfully: {session}")
        print(f"Session type: {type(session)}")
        session.close()
    except Exception as e:
        print(f"Error getting session: {e}")
    
    print("4. Testing add_restaurant...")
    test_data = {
        'name': 'Test Restaurant',
        'address': '123 Test St',
        'city': 'Test City',
        'state': 'FL',
        'zip_code': '12345',
        'phone': '555-123-4567',
        'website': 'http://test.com',
        'cuisine_type': 'Test',
        'description': 'Test restaurant',
        'is_kosher': True,
        'is_hechsher': True,
        'hechsher_details': 'Test Hechsher'
    }
    
    try:
        result = db.add_restaurant(test_data)
        print(f"Add restaurant result: {result}")
    except Exception as e:
        print(f"Error adding restaurant: {e}")
    
    print("5. Testing get_restaurants...")
    try:
        restaurants = db.get_restaurants(limit=5)
        print(f"Found {len(restaurants)} restaurants")
    except Exception as e:
        print(f"Error getting restaurants: {e}")

if __name__ == "__main__":
    test_session() 