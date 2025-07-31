#!/usr/bin/env python3
"""
Fix Production Database Schema
=============================

This script adds missing columns to the production database to fix the
"column restaurants.rating does not exist" error.

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

def fix_production_schema():
    """Fix the production database schema by adding missing columns."""
    
    # Production database URL from the test file
    database_url = "postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    
    logger.info("Starting production database schema fix", database_host="ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech")
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        # Define the columns to add
        columns_to_add = [
            ("cuisine_type", "VARCHAR(100)"),
            ("hechsher_details", "VARCHAR(500)"),
            ("description", "TEXT"),
            ("latitude", "FLOAT"),
            ("longitude", "FLOAT"),
            ("rating", "FLOAT"),
            ("review_count", "INTEGER"),
            ("google_rating", "FLOAT"),
            ("google_review_count", "INTEGER"),
            ("google_reviews", "TEXT"),
            ("hours", "TEXT")
        ]
        
        with engine.begin() as conn:
            # Check if columns already exist and add them if they don't
            for column_name, column_type in columns_to_add:
                try:
                    # Check if column exists
                    result = conn.execute(text(f"""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = 'restaurants' 
                        AND column_name = '{column_name}'
                    """))
                    
                    if not result.fetchone():
                        # Column doesn't exist, add it
                        logger.info(f"Adding column {column_name} to restaurants table")
                        conn.execute(text(f"ALTER TABLE restaurants ADD COLUMN {column_name} {column_type}"))
                        logger.info(f"Successfully added column {column_name}")
                    else:
                        logger.info(f"Column {column_name} already exists, skipping")
                        
                except Exception as e:
                    logger.error(f"Error adding column {column_name}: {e}")
                    raise
        
        logger.info("Production database schema fix completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Production database schema fix failed: {e}")
        return False

if __name__ == "__main__":
    success = fix_production_schema()
    if success:
        print("✅ Production database schema fix completed successfully")
        sys.exit(0)
    else:
        print("❌ Production database schema fix failed")
        sys.exit(1) 