#!/usr/bin/env python3
"""
Add Google Reviews columns to existing PostgreSQL database
"""

import os
import psycopg2
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def add_google_reviews_columns():
    """Add Google reviews columns to the restaurants table."""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        logger.error("DATABASE_URL environment variable not found")
        return False
    
    try:
        # Connect to database
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        logger.info("Connected to database for adding Google reviews columns")
        
        # SQL statements to add Google reviews columns
        alter_statements = [
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS google_rating REAL",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS google_review_count INTEGER",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS google_reviews TEXT"
        ]
        
        # Execute each ALTER statement
        for sql in alter_statements:
            try:
                cursor.execute(sql)
                logger.info(f"Added column: {sql}")
            except Exception as e:
                logger.warning(f"Column already exists or error: {sql} - {e}")
        
        # Commit changes
        conn.commit()
        logger.info("Google reviews columns added successfully")
        
        # Verify the columns exist
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'restaurants' 
            AND column_name IN ('google_rating', 'google_review_count', 'google_reviews')
            ORDER BY column_name
        """)
        
        columns = cursor.fetchall()
        logger.info(f"Verified columns: {columns}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        logger.error("Error adding Google reviews columns", error=str(e))
        return False

if __name__ == "__main__":
    success = add_google_reviews_columns()
    if success:
        print("✅ Google reviews columns added successfully")
    else:
        print("❌ Failed to add Google reviews columns") 