#!/usr/bin/env python3
"""
Test database connection and table creation
"""

import os
import sys
from database_manager_v2 import EnhancedDatabaseManager

def test_local_database():
    """Test the local database connection"""
    print("🧪 Testing local database connection...")
    
    # Test with SQLite
    db_manager = EnhancedDatabaseManager('sqlite:///test_restaurants.db')
    
    if db_manager.connect():
        print("✅ Local database connected successfully")
        
        # Test adding a restaurant
        test_data = {
            "business_id": "test_local_001",
            "name": "Local Test Restaurant",
            "address": "123 Local St",
            "city": "Local City",
            "state": "FL"
        }
        
        if db_manager.add_restaurant(test_data):
            print("✅ Local database: Restaurant added successfully")
            
            # Test retrieving the restaurant
            restaurant = db_manager.get_restaurant("test_local_001")
            if restaurant:
                print(f"✅ Local database: Restaurant retrieved: {restaurant.get('name')}")
            else:
                print("❌ Local database: Failed to retrieve restaurant")
        else:
            print("❌ Local database: Failed to add restaurant")
        
        db_manager.disconnect()
    else:
        print("❌ Local database: Failed to connect")

def test_postgresql_connection():
    """Test PostgreSQL connection if DATABASE_URL is available"""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("⚠️  No DATABASE_URL found in environment variables")
        return
    
    print(f"🧪 Testing PostgreSQL connection...")
    print(f"Database URL: {database_url[:20]}...")  # Show first 20 chars for security
    
    db_manager = EnhancedDatabaseManager(database_url)
    
    if db_manager.connect():
        print("✅ PostgreSQL database connected successfully")
        
        # Test adding a restaurant
        test_data = {
            "business_id": "test_pg_001",
            "name": "PostgreSQL Test Restaurant",
            "address": "123 PG St",
            "city": "PG City",
            "state": "FL"
        }
        
        if db_manager.add_restaurant(test_data):
            print("✅ PostgreSQL database: Restaurant added successfully")
            
            # Test retrieving the restaurant
            restaurant = db_manager.get_restaurant("test_pg_001")
            if restaurant:
                print(f"✅ PostgreSQL database: Restaurant retrieved: {restaurant.get('name')}")
            else:
                print("❌ PostgreSQL database: Failed to retrieve restaurant")
        else:
            print("❌ PostgreSQL database: Failed to add restaurant")
        
        db_manager.disconnect()
    else:
        print("❌ PostgreSQL database: Failed to connect")

def main():
    print("🔍 Database Connection Test")
    print("=" * 40)
    
    # Test local database
    test_local_database()
    
    print("\n" + "=" * 40)
    
    # Test PostgreSQL if available
    test_postgresql_connection()
    
    print("\n📋 Summary:")
    print("• If local database works but PostgreSQL fails: Database configuration issue")
    print("• If both fail: Code issue")
    print("• If both work: Remote backend configuration issue")

if __name__ == "__main__":
    main() 