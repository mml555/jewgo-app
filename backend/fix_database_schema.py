#!/usr/bin/env python3
"""
Database Schema Fix Script
=========================

This script adds missing columns to the restaurants table to fix the AttributeError.
Run this script on the deployed backend to fix the database schema.

Usage:
    python fix_database_schema.py
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

def fix_database_schema():
    """Add missing columns to the restaurants table."""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        logger.error("DATABASE_URL environment variable is required")
        return False
    
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
        
        with engine.connect() as conn:
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
                        conn.commit()
                        logger.info(f"Successfully added column {column_name}")
                    else:
                        logger.info(f"Column {column_name} already exists, skipping")
                        
                except Exception as e:
                    logger.error(f"Error adding column {column_name}: {e}")
                    conn.rollback()
                    return False
        
        logger.info("Database schema fix completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Database schema fix failed: {e}")
        return False

if __name__ == "__main__":
    success = fix_database_schema()
    if success:
        print("✅ Database schema fix completed successfully")
        sys.exit(0)
    else:
        print("❌ Database schema fix failed")
        sys.exit(1) 