#!/usr/bin/env python3
"""
Migration script to add missing columns to the restaurants table.
This fixes the AttributeError: 'Restaurant' object has no attribute 'hechsher_details'
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

def run_migration():
    """Run the migration to add missing columns."""
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
        
        logger.info("Migration completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1) 