#!/usr/bin/env python3
"""
Simple Kosher Type Update Script
Manually update specific restaurants with correct kosher types.
"""

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def get_database_url():
    """Get database URL from environment."""
    return os.environ.get('DATABASE_URL')

def update_kosher_types():
    """Update specific restaurants with correct kosher types."""
    database_url = get_database_url()
    
    if not database_url:
        print("❌ No database URL found. Please check environment variables.")
        return False
    
    try:
        # Connect to database
        conn = psycopg2.connect(database_url)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("✅ Connected to database")
        
        # Define specific updates based on ORB website data
        updates = [
            # Dairy restaurants (confirmed from ORB)
            ("Gifted Pizza (Food Truck)", "dairy"),      # ORB Dairy category
            ("Grand Cafe Hollywood", "dairy"),           # ORB Dairy category
            ("A La Carte", "dairy"),                     # ORB Dairy category
            ("Yum Berry Cafe & Sushi Bar", "dairy"),     # ORB Dairy category
            ("Mizrachi's Pizza in Hollywood", "dairy"),  # ORB Dairy category
            ("Cafe 95 at JARC", "dairy"),               # ORB Dairy category
            ("Toast 770", "dairy"),                      # ORB Dairy category
            
            # Meat restaurants (based on names)
            ("Oak and Ember", "meat"),                   # Grill/BBQ is meat
            ("Grill Xpress", "meat"),                    # Grill is meat
            
            # Test/Unknown restaurants
            ("Test Restaurant", "pareve"),               # Test restaurant, default to pareve
        ]
        
        updated_count = 0
        for name, kosher_type in updates:
            cursor.execute("""
                UPDATE restaurants 
                SET kosher_type = %s 
                WHERE name = %s
            """, (kosher_type, name))
            
            if cursor.rowcount > 0:
                print(f"✅ {name}: {kosher_type}")
                updated_count += 1
            else:
                print(f"⚠️  {name}: Not found")
        
        print(f"\n🎉 Successfully updated {updated_count} restaurants")
        
        # Show the results
        cursor.execute("""
            SELECT name, kosher_type 
            FROM restaurants 
            WHERE kosher_type IS NOT NULL 
            ORDER BY name
        """)
        
        results = cursor.fetchall()
        print("\n📋 Updated Kosher Types:")
        for name, kosher_type in results:
            print(f"  - {name}: {kosher_type}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to update kosher types: {str(e)}")
        return False

if __name__ == "__main__":
    print("🍽️  Update Kosher Types")
    print("=" * 50)
    
    if update_kosher_types():
        print("\n🎉 All done! Kosher types have been updated.")
    else:
        print("\n❌ Failed to update kosher types.") 