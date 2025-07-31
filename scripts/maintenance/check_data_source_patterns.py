#!/usr/bin/env python3
"""
Check Data Source Patterns
=========================

This script checks for patterns in the data that might explain why some restaurants 
have websites and others don't.

Author: JewGo Development Team
Version: 1.0
"""

import os
import sys
from sqlalchemy import create_engine, text

def check_data_source_patterns():
    """Check for patterns in the data that might explain website availability."""
    
    # Production database URL
    database_url = "postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    
    print("🔍 Analyzing Data Source Patterns")
    print("=" * 40)
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Check if there are different data sources or import batches
            print("📊 Data Import Analysis:")
            
            # Check creation dates to see if there are different batches
            result = conn.execute(text("""
                SELECT 
                    DATE(created_at) as import_date,
                    COUNT(*) as count,
                    COUNT(CASE WHEN website IS NOT NULL AND website != '' THEN 1 END) as with_website,
                    COUNT(CASE WHEN website IS NULL OR website = '' THEN 1 END) as without_website
                FROM restaurants 
                GROUP BY DATE(created_at)
                ORDER BY import_date
            """))
            
            print("  Import dates and website availability:")
            for import_date, count, with_website, without_website in result.fetchall():
                print(f"    {import_date}: {count} restaurants, {with_website} with website ({with_website/count*100:.1f}%)")
            
            # Check if there are patterns in the kosher_cert_link field
            print(f"\n🔗 Kosher Cert Link Patterns:")
            result = conn.execute(text("""
                SELECT 
                    CASE 
                        WHEN kosher_cert_link IS NULL OR kosher_cert_link = '' THEN 'No cert link'
                        WHEN kosher_cert_link LIKE '%orbkosher.com%' THEN 'ORB cert link'
                        ELSE 'Other cert link'
                    END as cert_link_type,
                    COUNT(*) as total,
                    COUNT(CASE WHEN website IS NOT NULL AND website != '' THEN 1 END) as with_website,
                    COUNT(CASE WHEN website IS NULL OR website = '' THEN 1 END) as without_website
                FROM restaurants 
                GROUP BY 
                    CASE 
                        WHEN kosher_cert_link IS NULL OR kosher_cert_link = '' THEN 'No cert link'
                        WHEN kosher_cert_link LIKE '%orbkosher.com%' THEN 'ORB cert link'
                        ELSE 'Other cert link'
                    END
                ORDER BY total DESC
            """))
            
            for cert_link_type, total, with_website, without_website in result.fetchall():
                print(f"  {cert_link_type}: {total} total, {with_website} with website ({with_website/total*100:.1f}%)")
            
            # Check if there are patterns in the detail_url field
            print(f"\n🔗 Detail URL Patterns:")
            result = conn.execute(text("""
                SELECT 
                    CASE 
                        WHEN detail_url IS NULL OR detail_url = '' THEN 'No detail URL'
                        WHEN detail_url LIKE '%orbkosher.com%' THEN 'ORB detail URL'
                        ELSE 'Other detail URL'
                    END as detail_url_type,
                    COUNT(*) as total,
                    COUNT(CASE WHEN website IS NOT NULL AND website != '' THEN 1 END) as with_website,
                    COUNT(CASE WHEN website IS NULL OR website = '' THEN 1 END) as without_website
                FROM restaurants 
                GROUP BY 
                    CASE 
                        WHEN detail_url IS NULL OR detail_url = '' THEN 'No detail URL'
                        WHEN detail_url LIKE '%orbkosher.com%' THEN 'ORB detail URL'
                        ELSE 'Other detail URL'
                    END
                ORDER BY total DESC
            """))
            
            for detail_url_type, total, with_website, without_website in result.fetchall():
                print(f"  {detail_url_type}: {total} total, {with_website} with website ({with_website/total*100:.1f}%)")
            
            # Check if there are patterns in restaurant names (might indicate different data sources)
            print(f"\n🔗 Restaurant Name Patterns:")
            
            # Check for restaurants with similar names but different website availability
            result = conn.execute(text("""
                SELECT 
                    name,
                    website,
                    kosher_cert_link,
                    detail_url
                FROM restaurants 
                WHERE name LIKE '%Bagel Boss%'
                ORDER BY name
            """))
            
            print("  Bagel Boss restaurants (example of similar names):")
            for name, website, cert_link, detail_url in result.fetchall():
                print(f"    {name}: {website or 'No website'} | {cert_link[:50] if cert_link else 'No cert'}...")
            
            # Check for restaurants that might be from different sources
            print(f"\n🔗 Potential Data Source Indicators:")
            
            # Check if restaurants with websites have more complete data
            result = conn.execute(text("""
                SELECT 
                    'With Website' as group_type,
                    COUNT(*) as total,
                    COUNT(CASE WHEN phone IS NOT NULL AND phone != '' THEN 1 END) as with_phone,
                    COUNT(CASE WHEN address IS NOT NULL AND address != '' THEN 1 END) as with_address,
                    COUNT(CASE WHEN kosher_cert_link IS NOT NULL AND kosher_cert_link != '' THEN 1 END) as with_cert_link
                FROM restaurants 
                WHERE website IS NOT NULL AND website != ''
                
                UNION ALL
                
                SELECT 
                    'Without Website' as group_type,
                    COUNT(*) as total,
                    COUNT(CASE WHEN phone IS NOT NULL AND phone != '' THEN 1 END) as with_phone,
                    COUNT(CASE WHEN address IS NOT NULL AND address != '' THEN 1 END) as with_address,
                    COUNT(CASE WHEN kosher_cert_link IS NOT NULL AND kosher_cert_link != '' THEN 1 END) as with_cert_link
                FROM restaurants 
                WHERE website IS NULL OR website = ''
            """))
            
            for group_type, total, with_phone, with_address, with_cert_link in result.fetchall():
                print(f"  {group_type}: {total} total")
                print(f"    - With phone: {with_phone} ({with_phone/total*100:.1f}%)")
                print(f"    - With address: {with_address} ({with_address/total*100:.1f}%)")
                print(f"    - With cert link: {with_cert_link} ({with_cert_link/total*100:.1f}%)")
                
    except Exception as e:
        print(f"❌ Analysis failed: {e}")

if __name__ == "__main__":
    check_data_source_patterns()
    print("\n🎉 Data source pattern analysis completed!") 