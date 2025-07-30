#!/usr/bin/env python3
"""
Check database schema to identify missing columns.
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
import json

def check_database_schema():
    """Check the actual database schema."""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL environment variable not found")
        return
    
    try:
        # Connect to database
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        print("🔍 Checking database schema...")
        
        # Get table information
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'restaurants'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        
        print(f"\n📋 Found {len(columns)} columns in restaurants table:")
        print("=" * 80)
        
        actual_columns = []
        for col in columns:
            print(f"  {col['column_name']:<25} {col['data_type']:<15} {'NULL' if col['is_nullable'] == 'YES' else 'NOT NULL'}")
            actual_columns.append(col['column_name'])
        
        print("\n" + "=" * 80)
        
        # Define expected columns from our SQLAlchemy model
        expected_columns = [
            'id', 'name', 'address', 'city', 'state', 'zip_code', 'phone', 'website',
            'cuisine_type', 'price_range', 'rating', 'review_count', 'latitude', 'longitude',
            'hours', 'description', 'image_url', 'is_kosher', 'is_glatt', 'is_cholov_yisroel',
            'is_pas_yisroel', 'is_bishul_yisroel', 'is_mehadrin', 'is_hechsher', 
            'hechsher_details', 'created_at', 'updated_at'
        ]
        
        # Find missing columns
        missing_columns = [col for col in expected_columns if col not in actual_columns]
        extra_columns = [col for col in actual_columns if col not in expected_columns]
        
        print(f"\n🔍 Analysis:")
        print(f"  Expected columns: {len(expected_columns)}")
        print(f"  Actual columns: {len(actual_columns)}")
        
        if missing_columns:
            print(f"\n❌ Missing columns ({len(missing_columns)}):")
            for col in missing_columns:
                print(f"  - {col}")
        
        if extra_columns:
            print(f"\n➕ Extra columns in DB ({len(extra_columns)}):")
            for col in extra_columns:
                print(f"  - {col}")
        
        if not missing_columns and not extra_columns:
            print("\n✅ Schema matches perfectly!")
        
        # Check if table has any data
        cursor.execute("SELECT COUNT(*) as count FROM restaurants")
        count_result = cursor.fetchone()
        row_count = count_result['count'] if count_result else 0
        
        print(f"\n📊 Table has {row_count} rows")
        
        # Show sample data structure
        if row_count > 0:
            cursor.execute("SELECT * FROM restaurants LIMIT 1")
            sample = cursor.fetchone()
            if sample:
                print(f"\n📝 Sample row structure:")
                for key, value in sample.items():
                    print(f"  {key}: {type(value).__name__} = {value}")
        
        cursor.close()
        conn.close()
        
        return {
            'actual_columns': actual_columns,
            'missing_columns': missing_columns,
            'extra_columns': extra_columns,
            'row_count': row_count
        }
        
    except Exception as e:
        print(f"❌ Error checking database schema: {e}")
        return None

if __name__ == "__main__":
    check_database_schema() 