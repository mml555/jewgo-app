#!/usr/bin/env python3
"""
Neon PostgreSQL Setup Script for JewGo
Quick setup for Neon Tech PostgreSQL database.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

def setup_neon_database():
    """Setup Neon PostgreSQL database."""
    print("🚀 Setting up Neon PostgreSQL for JewGo")
    print("=" * 50)
    
    # Check if DATABASE_URL is set
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url or 'neon.tech' not in database_url or 'username:password' in database_url:
        print("❌ Neon PostgreSQL URL not configured!")
        print(f"\n📝 Current DATABASE_URL: {database_url}")
        print("\n🔧 Please update your env.local file:")
        print("1. Go to https://neon.tech")
        print("2. Copy your connection string from 'Connection Details'")
        print("3. Replace the DATABASE_URL in env.local file")
        print("\nExample of what your DATABASE_URL should look like:")
        print("DATABASE_URL=postgresql://your_actual_username:your_actual_password@your_host.neon.tech:5432/your_database_name")
        print("\n⚠️  Make sure to replace the placeholder with your actual Neon credentials!")
        return False
    
    print(f"✅ Found Neon database URL: {database_url}")
    
    # Test connection
    print("\n🔍 Testing Neon PostgreSQL connection...")
    try:
        from database_manager_v2 import EnhancedDatabaseManager
        
        db = EnhancedDatabaseManager(database_url)
        if db.connect():
            print("✅ Neon PostgreSQL connection successful!")
            
            # Create tables
            print("\n🔨 Creating database tables...")
            from database_manager_v2 import Base
            from sqlalchemy import create_engine
            
            engine = create_engine(database_url)
            Base.metadata.create_all(engine)
            print("✅ Database tables created successfully!")
            
            # Show database info
            print("\n📊 Database Information:")
            stats = db.get_statistics()
            print(f"   Total Restaurants: {stats.get('total_restaurants', 0)}")
            print(f"   Active Restaurants: {stats.get('active_restaurants', 0)}")
            print(f"   Categories: {len(stats.get('categories', {}))}")
            print(f"   States: {len(stats.get('states', {}))}")
            print(f"   Agencies: {len(stats.get('agencies', {}))}")
            
            # Offer migration
            if stats.get('total_restaurants', 0) == 0:
                print("\n🔄 Database is empty. Would you like to migrate data from SQLite?")
                migrate_choice = input("Migrate data from SQLite? (y/n): ").lower()
                
                if migrate_choice == 'y':
                    migrate_from_sqlite(database_url)
            
            return True
        else:
            print("❌ Failed to connect to Neon PostgreSQL")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your DATABASE_URL format")
        print("2. Verify your Neon project is active")
        print("3. Check network connectivity")
        return False

def migrate_from_sqlite(database_url):
    """Migrate data from SQLite to Neon PostgreSQL."""
    print("\n🔄 Migrating data from SQLite to Neon PostgreSQL...")
    
    try:
        from database_manager import DatabaseManager as OldDB
        from database_manager_v2 import EnhancedDatabaseManager as NewDB
        
        # Connect to old SQLite database
        old_db = OldDB()
        if not old_db.connect():
            print("❌ Could not connect to SQLite database")
            return False
        
        # Connect to new Neon PostgreSQL database
        new_db = EnhancedDatabaseManager(database_url)
        if not new_db.connect():
            print("❌ Could not connect to Neon PostgreSQL database")
            return False
        
        # Get all restaurants from SQLite
        restaurants = old_db.search_restaurants(limit=10000)
        print(f"📊 Found {len(restaurants)} restaurants to migrate")
        
        # Migrate each restaurant
        migrated_count = 0
        for i, restaurant in enumerate(restaurants, 1):
            if new_db.add_restaurant(restaurant):
                migrated_count += 1
                if i % 50 == 0:  # Progress indicator
                    print(f"   Migrated {i}/{len(restaurants)} restaurants...")
            else:
                print(f"⚠️  Failed to migrate restaurant: {restaurant.get('name', 'Unknown')}")
        
        print(f"\n✅ Successfully migrated {migrated_count} restaurants to Neon PostgreSQL!")
        
        # Show final statistics
        stats = new_db.get_statistics()
        print(f"\n📊 Final Database Statistics:")
        print(f"   Total Restaurants: {stats.get('total_restaurants', 0)}")
        print(f"   Active Restaurants: {stats.get('active_restaurants', 0)}")
        print(f"   Categories: {len(stats.get('categories', {}))}")
        print(f"   States: {len(stats.get('states', {}))}")
        print(f"   Agencies: {len(stats.get('agencies', {}))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False

def test_api():
    """Test the API with Neon database."""
    print("\n🧪 Testing API with Neon database...")
    
    try:
        # Start the production Flask app
        import subprocess
        import time
        
        print("Starting Flask app...")
        process = subprocess.Popen([
            sys.executable, "app_production.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(3)
        
        # Test endpoints
        import requests
        
        try:
            response = requests.get("http://localhost:8081/", timeout=5)
            if response.status_code == 200:
                print("✅ API root endpoint working")
            else:
                print(f"⚠️  API root endpoint returned {response.status_code}")
        except:
            print("⚠️  Could not test API root endpoint")
        
        try:
            response = requests.get("http://localhost:8081/health", timeout=5)
            if response.status_code == 200:
                print("✅ Health check endpoint working")
            else:
                print(f"⚠️  Health check returned {response.status_code}")
        except:
            print("⚠️  Could not test health check endpoint")
        
        try:
            response = requests.get("http://localhost:8081/api/restaurants", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Restaurants endpoint working ({len(data.get('data', []))} restaurants)")
            else:
                print(f"⚠️  Restaurants endpoint returned {response.status_code}")
        except:
            print("⚠️  Could not test restaurants endpoint")
        
        # Stop the server
        process.terminate()
        
    except Exception as e:
        print(f"❌ API test error: {e}")

def main():
    """Main setup function."""
    if setup_neon_database():
        print("\n🎉 Neon PostgreSQL setup complete!")
        print("\n📝 Next steps:")
        print("1. Your database is ready for production")
        print("2. Test your API: python app_production.py")
        print("3. Deploy to Render/Railway/Fly.io")
        print("4. Update frontend API URL for production")
        
        # Offer to test API
        test_choice = input("\n🧪 Would you like to test the API? (y/n): ").lower()
        if test_choice == 'y':
            test_api()
    else:
        print("\n❌ Setup failed. Please check your configuration.")

if __name__ == "__main__":
    main() 