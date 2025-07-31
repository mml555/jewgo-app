#!/usr/bin/env python3
"""
Check Current Database Schema
============================

This script checks the current schema of the restaurants table
to understand what columns exist before running migrations.
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_schema():
    """Check the current schema of the restaurants table."""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL environment variable is required")
        return False
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Get all columns in the restaurants table
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'restaurants'
                ORDER BY ordinal_position
            """))
            
            columns = result.fetchall()
            
            print("📊 Current restaurants table schema:")
            print("=" * 80)
            print(f"{'Column Name':<25} {'Data Type':<15} {'Nullable':<10} {'Default'}")
            print("-" * 80)
            
            for column in columns:
                column_name, data_type, is_nullable, column_default = column
                default_str = str(column_default) if column_default else 'None'
                print(f"{column_name:<25} {data_type:<15} {is_nullable:<10} {default_str}")
            
            print(f"\n📈 Total columns: {len(columns)}")
            
            # Check for specific columns we're looking for
            column_names = [col[0] for col in columns]
            
            print("\n🔍 Checking for specific columns:")
            print(f"  - kosher_category: {'✅' if 'kosher_category' in column_names else '❌'}")
            print(f"  - listing_type: {'✅' if 'listing_type' in column_names else '❌'}")
            print(f"  - phone_number: {'✅' if 'phone_number' in column_names else '❌'}")
            print(f"  - hours_of_operation: {'✅' if 'hours_of_operation' in column_names else '❌'}")
            print(f"  - kosher_type: {'✅' if 'kosher_type' in column_names else '❌'}")
            print(f"  - phone: {'✅' if 'phone' in column_names else '❌'}")
            print(f"  - category: {'✅' if 'category' in column_names else '❌'}")
            print(f"  - hours_open: {'✅' if 'hours_open' in column_names else '❌'}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error checking schema: {e}")
        return False

if __name__ == "__main__":
    success = check_schema()
    sys.exit(0 if success else 1) 