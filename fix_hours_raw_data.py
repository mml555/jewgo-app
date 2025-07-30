#!/usr/bin/env python3
"""
Fix Hours Raw Data Script
This script fixes the hours_of_operation data to store raw hours instead of processed status.
"""

import os
import psycopg2
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def extract_raw_hours(processed_hours):
    """Extract raw hours from processed hours string."""
    if not processed_hours:
        return None
    
    # Remove the status prefix (🔴 Closed •, 🟢 Open Now •, etc.)
    # Pattern: emoji + status + bullet point + space
    raw_hours = re.sub(r'^[🔴🟢⚪]+\s*(?:Closed|Open|Open Now|Unknown)\s*•\s*', '', processed_hours)
    
    return raw_hours.strip() if raw_hours.strip() else None

def fix_hours_raw_data():
    """Fix hours data to store raw hours instead of processed status."""
    print("🔧 Fixing hours data to store raw format...")
    print("=" * 50)
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("Error: DATABASE_URL environment variable not set")
        return
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Get restaurants with processed hours data
        cursor.execute("""
            SELECT id, name, hours_of_operation 
            FROM restaurants 
            WHERE hours_of_operation IS NOT NULL 
            AND (hours_of_operation LIKE '%🔴%' OR hours_of_operation LIKE '%🟢%' OR hours_of_operation LIKE '%⚪%')
        """)
        
        restaurants = cursor.fetchall()
        print(f"📊 Found {len(restaurants)} restaurants with processed hours data")
        
        if not restaurants:
            print("✅ No restaurants need fixing")
            conn.close()
            return
        
        # Show sample before/after
        print("\n📋 Sample data before fixing:")
        sample = restaurants[0]
        print(f"   Name: {sample[1]}")
        print(f"   Current: {sample[2]}")
        raw_hours = extract_raw_hours(sample[2])
        print(f"   Will become: {raw_hours}")
        
        # Confirm with user
        response = input("\n❓ Proceed with fixing hours data? (y/N): ")
        if response.lower() != 'y':
            print("❌ Operation cancelled")
            conn.close()
            return
        
        # Update hours data
        updated_count = 0
        for restaurant in restaurants:
            restaurant_id, name, processed_hours = restaurant
            raw_hours = extract_raw_hours(processed_hours)
            
            if raw_hours:
                cursor.execute("""
                    UPDATE restaurants 
                    SET hours_of_operation = %s 
                    WHERE id = %s
                """, (raw_hours, restaurant_id))
                updated_count += 1
        
        conn.commit()
        print(f"✅ Successfully updated {updated_count} restaurants")
        
        # Show sample after fixing
        cursor.execute("""
            SELECT id, name, hours_of_operation 
            FROM restaurants 
            WHERE id = %s
        """, (sample[0],))
        
        updated_sample = cursor.fetchone()
        print(f"\n📋 Sample data after fixing:")
        print(f"   Name: {updated_sample[1]}")
        print(f"   Hours: {updated_sample[2]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error fixing hours data: {e}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    fix_hours_raw_data() 