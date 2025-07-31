#!/usr/bin/env python3
"""
Test Certifying Agency Direct
============================

This script tests the certifying_agency field directly in the database.

Author: JewGo Development Team
Version: 1.0
"""

import os
import sys
from sqlalchemy import create_engine, text

def test_certifying_agency_direct():
    """Test the certifying_agency field directly in the database."""
    
    # Production database URL
    database_url = "postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    
    print("🔍 Testing Certifying Agency Direct in Database")
    print("=" * 50)
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Check if the column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'restaurants' 
                AND column_name = 'certifying_agency'
            """))
            
            if result.fetchone():
                print("✅ certifying_agency column exists in database")
            else:
                print("❌ certifying_agency column does not exist in database")
                return
            
            # Check the data
            result = conn.execute(text("""
                SELECT certifying_agency, COUNT(*) as count
                FROM restaurants 
                GROUP BY certifying_agency
                ORDER BY count DESC
            """))
            
            agencies = result.fetchall()
            
            print("\n📊 Certifying Agency Distribution:")
            for agency, count in agencies:
                print(f"  {agency or 'NULL'}: {count} restaurants")
            
            # Check a few sample restaurants
            result = conn.execute(text("""
                SELECT name, certifying_agency, kosher_cert_link
                FROM restaurants 
                LIMIT 5
            """))
            
            print("\n📋 Sample Restaurants:")
            for name, agency, cert_link in result.fetchall():
                print(f"  {name}: {agency} (from: {cert_link[:50]}{'...' if len(cert_link) > 50 else ''})")
            
            # Check if there are any NULL values
            result = conn.execute(text("""
                SELECT COUNT(*) as null_count
                FROM restaurants 
                WHERE certifying_agency IS NULL OR certifying_agency = ''
            """))
            
            null_count = result.fetchone()[0]
            print(f"\n⚠️  Restaurants with NULL/empty certifying_agency: {null_count}")
            
            if null_count > 0:
                print("\n🔧 Updating NULL values to 'ORB'...")
                conn.execute(text("""
                    UPDATE restaurants 
                    SET certifying_agency = 'ORB' 
                    WHERE certifying_agency IS NULL OR certifying_agency = ''
                """))
                conn.commit()
                print("✅ Updated NULL values to 'ORB'")
                
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_certifying_agency_direct()
    print("\n🎉 Direct database test completed!") 