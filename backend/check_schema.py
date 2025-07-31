#!/usr/bin/env python3
"""
Script to check the current database schema and identify column issues.
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_schema():
    """Check the current database schema."""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("DATABASE_URL environment variable is required")
        return False
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Check if restaurants table exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'restaurants'
                )
            """))
            
            if not result.fetchone()[0]:
                print("❌ Restaurants table does not exist!")
                return False
            
            print("✅ Restaurants table exists")
            
            # Get all columns in the restaurants table
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'restaurants' 
                AND table_schema = 'public'
                ORDER BY ordinal_position
            """))
            
            columns = result.fetchall()
            print(f"\n📋 Current columns in restaurants table ({len(columns)} total):")
            print("-" * 80)
            
            for col in columns:
                nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                default = f" DEFAULT {col[3]}" if col[3] else ""
                print(f"  {col[0]:<25} {col[1]:<15} {nullable}{default}")
            
            # Check for kosher_type vs kosher_category
            kosher_columns = [col for col in columns if 'kosher' in col[0].lower()]
            print(f"\n🔍 Kosher-related columns: {[col[0] for col in kosher_columns]}")
            
            if not kosher_columns:
                print("❌ No kosher-related columns found!")
            elif len(kosher_columns) > 1:
                print("⚠️  Multiple kosher columns found - this might be the issue!")
            else:
                print(f"✅ Single kosher column: {kosher_columns[0][0]}")
            
            # Check table row count
            result = conn.execute(text("SELECT COUNT(*) FROM restaurants"))
            count = result.fetchone()[0]
            print(f"\n📊 Total restaurants in database: {count}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error checking schema: {e}")
        return False

if __name__ == "__main__":
    check_schema() 