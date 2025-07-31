#!/usr/bin/env python3
"""
Add Certifying Agency Column
===========================

This script adds the missing certifying_agency column to the restaurants table
and populates it with data extracted from the kosher_cert_link field.

Author: JewGo Development Team
Version: 1.0
"""

import os
import sys
from sqlalchemy import create_engine, text
import structlog

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

def extract_agency_from_link(cert_link):
    """Extract certifying agency from certificate link."""
    if not cert_link:
        return "Unknown"
    
    # Common patterns in kosher certification links
    if 'orbkosher.com' in cert_link:
        return "ORB"
    elif 'oukosher.org' in cert_link:
        return "OU"
    elif 'crcweb.org' in cert_link:
        return "CRC"
    elif 'star-k.org' in cert_link:
        return "Star-K"
    elif 'ok.org' in cert_link:
        return "OK"
    elif 'kof-k.org' in cert_link:
        return "Kof-K"
    elif 'chabad.org' in cert_link:
        return "Chabad"
    elif 'diamondk.org' in cert_link:
        return "Diamond K"
    elif 'kmkosher.com' in cert_link:
        return "KM"
    elif 'kdmkosher.com' in cert_link:
        return "KDM"
    else:
        # Try to extract from the filename
        filename = cert_link.split('/')[-1] if '/' in cert_link else cert_link
        if filename and '.' in filename:
            # Remove file extension and try to extract agency
            name_without_ext = filename.split('.')[0]
            # Look for common agency patterns
            if any(agency in name_without_ext.upper() for agency in ['ORB', 'OU', 'CRC', 'STAR', 'OK', 'KOF', 'DIAMOND', 'KM', 'KDM']):
                return name_without_ext
        return "Unknown"

def add_certifying_agency_column():
    """Add the certifying_agency column and populate it with data."""
    
    # Production database URL
    database_url = "postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    
    logger.info("Starting certifying_agency column addition", database_host="ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech")
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        with engine.begin() as conn:
            # Step 1: Add the certifying_agency column if it doesn't exist
            try:
                # Check if column exists
                result = conn.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'restaurants' 
                    AND column_name = 'certifying_agency'
                """))
                
                if not result.fetchone():
                    # Column doesn't exist, add it
                    logger.info("Adding certifying_agency column to restaurants table")
                    conn.execute(text("ALTER TABLE restaurants ADD COLUMN certifying_agency VARCHAR(100)"))
                    logger.info("Successfully added certifying_agency column")
                else:
                    logger.info("certifying_agency column already exists")
                    
            except Exception as e:
                logger.error(f"Error adding certifying_agency column: {e}")
                raise
            
            # Step 2: Get all restaurants with kosher_cert_link
            result = conn.execute(text("""
                SELECT id, kosher_cert_link, name 
                FROM restaurants 
                WHERE kosher_cert_link IS NOT NULL AND kosher_cert_link != ''
            """))
            
            restaurants_with_links = result.fetchall()
            logger.info(f"Found {len(restaurants_with_links)} restaurants with kosher_cert_link")
            
            # Step 3: Update each restaurant with extracted certifying agency
            updated_count = 0
            for restaurant in restaurants_with_links:
                restaurant_id, cert_link, name = restaurant
                
                # Extract agency from the link
                agency = extract_agency_from_link(cert_link)
                
                # Update the restaurant
                conn.execute(text("""
                    UPDATE restaurants 
                    SET certifying_agency = :agency 
                    WHERE id = :restaurant_id
                """), {"agency": agency, "restaurant_id": restaurant_id})
                
                logger.info(f"Updated restaurant {name} (ID: {restaurant_id}) with agency: {agency}")
                updated_count += 1
            
            # Step 4: Set default agency for restaurants without cert links
            result = conn.execute(text("""
                SELECT id, name 
                FROM restaurants 
                WHERE kosher_cert_link IS NULL OR kosher_cert_link = ''
            """))
            
            restaurants_without_links = result.fetchall()
            logger.info(f"Found {len(restaurants_without_links)} restaurants without kosher_cert_link")
            
            for restaurant in restaurants_without_links:
                restaurant_id, name = restaurant
                
                # Set default agency based on the short_description or other clues
                conn.execute(text("""
                    UPDATE restaurants 
                    SET certifying_agency = 'ORB' 
                    WHERE id = :restaurant_id AND (certifying_agency IS NULL OR certifying_agency = '')
                """), {"restaurant_id": restaurant_id})
                
                logger.info(f"Set default agency 'ORB' for restaurant {name} (ID: {restaurant_id})")
                updated_count += 1
            
            logger.info(f"Total restaurants updated: {updated_count}")
        
        logger.info("Certifying agency column addition and population completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Certifying agency column addition failed: {e}")
        return False

def verify_certifying_agency_data():
    """Verify that the certifying_agency data was added correctly."""
    
    database_url = "postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Check the data
            result = conn.execute(text("""
                SELECT certifying_agency, COUNT(*) as count
                FROM restaurants 
                GROUP BY certifying_agency
                ORDER BY count DESC
            """))
            
            agencies = result.fetchall()
            
            print("\n🔍 Certifying Agency Data Verification")
            print("=" * 40)
            print("Agency distribution:")
            for agency, count in agencies:
                print(f"  {agency or 'NULL'}: {count} restaurants")
            
            # Check a few sample restaurants
            result = conn.execute(text("""
                SELECT name, certifying_agency, kosher_cert_link
                FROM restaurants 
                LIMIT 5
            """))
            
            print("\nSample restaurants:")
            for name, agency, cert_link in result.fetchall():
                print(f"  {name}: {agency} (from: {cert_link[:50]}{'...' if len(cert_link) > 50 else ''})")
                
    except Exception as e:
        print(f"❌ Verification failed: {e}")

if __name__ == "__main__":
    success = add_certifying_agency_column()
    if success:
        print("✅ Certifying agency column addition completed successfully")
        verify_certifying_agency_data()
        sys.exit(0)
    else:
        print("❌ Certifying agency column addition failed")
        sys.exit(1) 