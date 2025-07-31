#!/usr/bin/env python3
"""
Update Cholov Yisroel Information
Update ORB dairy restaurants with Cholov Yisroel information.
"""

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def get_database_url():
    """Get database URL from environment."""
    return os.environ.get('DATABASE_URL')

def update_cholov_yisroel():
    """Update ORB dairy restaurants with Cholov Yisroel information."""
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
        
        # Define ORB dairy restaurants that should have Cholov Yisroel
        cholov_yisroel_restaurants = [
            "Grand Cafe Hollywood",
            "Yum Berry Cafe & Sushi Bar", 
            "Cafe 95 at JARC",
            "Grand Cafe Aventura",
            "La Vita é Bella",
            "The Cafe Maison la Fleur & Dunwell Pizza",
            "Mozart Cafe Sunny Isles Inc",
            "Zuka Miami"
        ]
        
        # Define restaurants that use Cholov Stam (regular milk)
        cholov_stam_restaurants = [
            "Mizrachi's Pizza in Hollywood",
            "A La Carte",
            "Toast 770 (Inside Mobile Gas Station)",
            "Gifted Pizza (Food Truck)",
            "Bagel Boss (Surfside)",
            "Bagel Boss Boca Raton",
            "BOUTIQUE CAFE",
            "Joe's Pizza",
            "Yummy Pizza",
            "Rita's (in KC Market)",
            "Hollywood Sara's Pizza",
            "Mizrachi's Pizza in KC Hallandale"
        ]
        
        updated_count = 0
        
        # Update Cholov Yisroel restaurants
        print("\n🥛 Updating Cholov Yisroel restaurants...")
        for name in cholov_yisroel_restaurants:
            cursor.execute("""
                UPDATE restaurants 
                SET is_cholov_yisroel = TRUE 
                WHERE name = %s AND source = 'orb'
            """, (name,))
            
            if cursor.rowcount > 0:
                print(f"✅ {name}: Cholov Yisroel = TRUE")
                updated_count += 1
            else:
                print(f"⚠️  {name}: Not found or not ORB source")
        
        # Update Cholov Stam restaurants
        print("\n🥛 Updating Cholov Stam restaurants...")
        for name in cholov_stam_restaurants:
            cursor.execute("""
                UPDATE restaurants 
                SET is_cholov_yisroel = FALSE 
                WHERE name = %s AND source = 'orb'
            """, (name,))
            
            if cursor.rowcount > 0:
                print(f"✅ {name}: Cholov Yisroel = FALSE (Cholov Stam)")
                updated_count += 1
            else:
                print(f"⚠️  {name}: Not found or not ORB source")
        
        print(f"\n🎉 Successfully updated {updated_count} restaurants")
        
        # Show the results
        cursor.execute("""
            SELECT name, is_cholov_yisroel, source
            FROM restaurants 
            WHERE source = 'orb' AND is_cholov_yisroel IS NOT NULL
            ORDER BY name
        """)
        
        results = cursor.fetchall()
        print("\n📋 Cholov Yisroel Status:")
        for name, is_cholov_yisroel, source in results:
            status = "Cholov Yisroel" if is_cholov_yisroel else "Cholov Stam"
            print(f"  - {name}: {status}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to update Cholov Yisroel: {str(e)}")
        return False

if __name__ == "__main__":
    print("🥛 Update Cholov Yisroel Information")
    print("=" * 50)
    
    if update_cholov_yisroel():
        print("\n🎉 All done! Cholov Yisroel information has been updated.")
    else:
        print("\n❌ Failed to update Cholov Yisroel information.") 