#!/usr/bin/env python3
"""
Check Website Data
=================

This script analyzes the website field data to understand why some restaurants 
have websites and others don't.

Author: JewGo Development Team
Version: 1.0
"""

import os
import sys
from sqlalchemy import create_engine, text

def check_website_data():
    """Check the website field data in the database."""
    
    # Production database URL
    database_url = "postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    
    print("🔍 Analyzing Website Data")
    print("=" * 40)
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Get total count
            result = conn.execute(text("SELECT COUNT(*) FROM restaurants"))
            total_count = result.fetchone()[0]
            
            # Count restaurants with websites
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM restaurants 
                WHERE website IS NOT NULL AND website != ''
            """))
            with_website_count = result.fetchone()[0]
            
            # Count restaurants without websites
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM restaurants 
                WHERE website IS NULL OR website = ''
            """))
            without_website_count = result.fetchone()[0]
            
            print(f"📊 Website Data Summary:")
            print(f"  Total restaurants: {total_count}")
            print(f"  With website: {with_website_count} ({with_website_count/total_count*100:.1f}%)")
            print(f"  Without website: {without_website_count} ({without_website_count/total_count*100:.1f}%)")
            
            # Check website field patterns
            print(f"\n🔍 Website Field Analysis:")
            
            # Check for different types of website data
            result = conn.execute(text("""
                SELECT 
                    CASE 
                        WHEN website IS NULL THEN 'NULL'
                        WHEN website = '' THEN 'Empty string'
                        WHEN website LIKE 'http%' THEN 'Valid URL'
                        WHEN website LIKE 'www.%' THEN 'WWW without protocol'
                        ELSE 'Other format'
                    END as website_type,
                    COUNT(*) as count
                FROM restaurants 
                GROUP BY 
                    CASE 
                        WHEN website IS NULL THEN 'NULL'
                        WHEN website = '' THEN 'Empty string'
                        WHEN website LIKE 'http%' THEN 'Valid URL'
                        WHEN website LIKE 'www.%' THEN 'WWW without protocol'
                        ELSE 'Other format'
                    END
                ORDER BY count DESC
            """))
            
            website_types = result.fetchall()
            print(f"  Website field types:")
            for website_type, count in website_types:
                print(f"    {website_type}: {count} restaurants")
            
            # Sample restaurants with websites
            print(f"\n📋 Sample Restaurants WITH Websites:")
            result = conn.execute(text("""
                SELECT name, website, kosher_cert_link
                FROM restaurants 
                WHERE website IS NOT NULL AND website != ''
                LIMIT 10
            """))
            
            for name, website, cert_link in result.fetchall():
                print(f"  {name}: {website}")
            
            # Sample restaurants without websites
            print(f"\n📋 Sample Restaurants WITHOUT Websites:")
            result = conn.execute(text("""
                SELECT name, website, kosher_cert_link
                FROM restaurants 
                WHERE website IS NULL OR website = ''
                LIMIT 10
            """))
            
            for name, website, cert_link in result.fetchall():
                print(f"  {name}: {website or 'NULL'}")
            
            # Check if there's a correlation with certifying agency
            print(f"\n🔗 Website vs Certifying Agency Correlation:")
            result = conn.execute(text("""
                SELECT 
                    certifying_agency,
                    COUNT(*) as total,
                    COUNT(CASE WHEN website IS NOT NULL AND website != '' THEN 1 END) as with_website,
                    COUNT(CASE WHEN website IS NULL OR website = '' THEN 1 END) as without_website
                FROM restaurants 
                GROUP BY certifying_agency
                ORDER BY total DESC
            """))
            
            for agency, total, with_website, without_website in result.fetchall():
                print(f"  {agency or 'NULL'}: {total} total, {with_website} with website ({with_website/total*100:.1f}%), {without_website} without")
            
            # Check if there's a correlation with kosher_category
            print(f"\n🔗 Website vs Kosher Type Correlation:")
            result = conn.execute(text("""
                SELECT 
                    kosher_category,
                    COUNT(*) as total,
                    COUNT(CASE WHEN website IS NOT NULL AND website != '' THEN 1 END) as with_website,
                    COUNT(CASE WHEN website IS NULL OR website = '' THEN 1 END) as without_website
                FROM restaurants 
                GROUP BY kosher_category
                ORDER BY total DESC
            """))
            
            for kosher_category, total, with_website, without_website in result.fetchall():
                print(f"  {kosher_category or 'NULL'}: {total} total, {with_website} with website ({with_website/total*100:.1f}%), {without_website} without")
                
    except Exception as e:
        print(f"❌ Analysis failed: {e}")

if __name__ == "__main__":
    check_website_data()
    print("\n🎉 Website data analysis completed!") 