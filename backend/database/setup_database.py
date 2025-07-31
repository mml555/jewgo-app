#!/usr/bin/env python3
"""
Database Setup Script for JewGo
Helps configure and test PostgreSQL database connections.
"""

import os
import sys
from dotenv import load_dotenv
from database_manager_v2 import EnhancedDatabaseManager, Base
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

def test_sqlite_connection():
    """Test SQLite connection (fallback)."""
    print("🔍 Testing SQLite connection...")
    try:
        db = EnhancedDatabaseManager("sqlite:///restaurants.db")
        if db.connect():
            print("✅ SQLite connection successful")
            return True
        else:
            print("❌ SQLite connection failed")
            return False
    except Exception as e:
        print(f"❌ SQLite error: {e}")
        return False

def test_postgresql_connection(database_url):
    """Test PostgreSQL connection."""
    print(f"🔍 Testing PostgreSQL connection...")
    try:
        db = EnhancedDatabaseManager(database_url)
        if db.connect():
            print("✅ PostgreSQL connection successful")
            return True
        else:
            print("❌ PostgreSQL connection failed")
            return False
    except Exception as e:
        print(f"❌ PostgreSQL error: {e}")
        return False

def create_tables(database_url):
    """Create database tables."""
    print("🔨 Creating database tables...")
    try:
        engine = create_engine(database_url)
        Base.metadata.create_all(engine)
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def migrate_data_from_sqlite():
    """Migrate data from existing SQLite database."""
    print("🔄 Migrating data from SQLite...")
    try:
        from database_manager import DatabaseManager as OldDB
        
        # Connect to old SQLite database
        old_db = OldDB()
        if not old_db.connect():
            print("❌ Could not connect to SQLite database")
            return False
        
        # Get database URL from environment
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL not set in environment")
            return False
        
        # Connect to new PostgreSQL database
        new_db = EnhancedDatabaseManager(database_url)
        if not new_db.connect():
            print("❌ Could not connect to PostgreSQL database")
            return False
        
        # Get all restaurants from SQLite
        restaurants = old_db.search_restaurants(limit=10000)
        print(f"📊 Found {len(restaurants)} restaurants to migrate")
        
        # Migrate each restaurant
        migrated_count = 0
        for restaurant in restaurants:
            if new_db.add_restaurant(restaurant):
                migrated_count += 1
            else:
                print(f"⚠️  Failed to migrate restaurant: {restaurant.get('name', 'Unknown')}")
        
        print(f"✅ Successfully migrated {migrated_count} restaurants")
        return True
        
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False

def show_database_info(database_url):
    """Show database information."""
    print("📊 Database Information:")
    print(f"   Type: {'PostgreSQL' if 'postgresql' in database_url else 'SQLite'}")
    print(f"   URL: {database_url}")
    
    try:
        db = EnhancedDatabaseManager(database_url)
        if db.connect():
            stats = db.get_statistics()
            print(f"   Total Restaurants: {stats.get('total_restaurants', 0)}")
            print(f"   Active Restaurants: {stats.get('active_restaurants', 0)}")
            print(f"   Categories: {len(stats.get('categories', {}))}")
            print(f"   States: {len(stats.get('states', {}))}")
            print(f"   Agencies: {len(stats.get('agencies', {}))}")
        else:
            print("   Status: Connection failed")
    except Exception as e:
        print(f"   Error: {e}")

def main():
    """Main setup function."""
    print("🚀 JewGo Database Setup")
    print("=" * 50)
    
    # Check environment variables
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("⚠️  DATABASE_URL not set in environment")
        print("📝 Please set your database URL:")
        print("   export DATABASE_URL='postgresql://username:password@host:port/database'")
        print("   or")
        print("   export DATABASE_URL='sqlite:///restaurants.db'")
        return
    
    # Test connection
    if 'postgresql' in database_url:
        if not test_postgresql_connection(database_url):
            print("\n❌ PostgreSQL connection failed. Please check:")
            print("   1. Database URL format")
            print("   2. Network connectivity")
            print("   3. Database credentials")
            return
    else:
        if not test_sqlite_connection():
            print("\n❌ SQLite connection failed")
            return
    
    # Create tables
    if not create_tables(database_url):
        print("\n❌ Failed to create database tables")
        return
    
    # Show database info
    print("\n" + "=" * 50)
    show_database_info(database_url)
    
    # Offer migration if using PostgreSQL
    if 'postgresql' in database_url:
        print("\n" + "=" * 50)
        migrate_choice = input("🔄 Would you like to migrate data from SQLite? (y/n): ").lower()
        if migrate_choice == 'y':
            migrate_data_from_sqlite()
    
    print("\n✅ Database setup complete!")
    print("\n📝 Next steps:")
    print("   1. Update your .env file with the DATABASE_URL")
    print("   2. Test your API endpoints")
    print("   3. Deploy to production")

if __name__ == "__main__":
    main() 