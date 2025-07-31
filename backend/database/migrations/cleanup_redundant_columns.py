#!/usr/bin/env python3
"""
Migration script to remove redundant columns from restaurants table.
This migration removes columns that are duplicates or no longer needed.

Columns to remove:
- hechsher_details (duplicate of certifying_agency)
- is_hechsher (redundant, can infer from certifying_agency)
- is_mehadrin (not needed, can be handled in JSON if required)
- is_kosher (all restaurants are kosher by definition)
- is_glatt (not needed, can be handled in JSON if required)
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import structlog
from datetime import datetime

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
    """Run the migration to remove redundant columns."""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        logger.error("DATABASE_URL environment variable is required")
        return False
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Start transaction
            trans = conn.begin()
            
            try:
                logger.info("Starting cleanup of redundant columns")
                
                # Columns to remove
                columns_to_remove = [
                    'hechsher_details',
                    'is_hechsher', 
                    'is_mehadrin',
                    'is_kosher',
                    'is_glatt'
                ]
                
                for column_name in columns_to_remove:
                    try:
                        # Check if column exists
                        result = conn.execute(text(f"""
                            SELECT column_name 
                            FROM information_schema.columns 
                            WHERE table_name = 'restaurants' 
                            AND column_name = '{column_name}'
                        """))
                        
                        if result.fetchone():
                            logger.info(f"Removing column {column_name} from restaurants table")
                            conn.execute(text(f"ALTER TABLE restaurants DROP COLUMN {column_name}"))
                            logger.info(f"Successfully removed column {column_name}")
                        else:
                            logger.info(f"Column {column_name} does not exist, skipping")
                            
                    except Exception as e:
                        logger.error(f"Error removing column {column_name}: {e}")
                        raise
                
                # Commit transaction
                trans.commit()
                logger.info("Successfully completed cleanup of redundant columns")
                
                return True
                
            except Exception as e:
                # Rollback transaction on error
                trans.rollback()
                logger.error(f"Error during migration: {e}")
                raise
                
    except Exception as e:
        logger.error(f"Failed to run migration: {e}")
        return False

def verify_migration():
    """Verify that the migration was successful."""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        logger.error("DATABASE_URL environment variable is required")
        return False
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Check that columns were removed
            columns_to_remove = [
                'hechsher_details',
                'is_hechsher', 
                'is_mehadrin',
                'is_kosher',
                'is_glatt'
            ]
            
            for column_name in columns_to_remove:
                result = conn.execute(text(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'restaurants' 
                    AND column_name = '{column_name}'
                """))
                
                if result.fetchone():
                    logger.error(f"Column {column_name} still exists after migration!")
                    return False
                else:
                    logger.info(f"✅ Column {column_name} successfully removed")
            
            # Get total column count
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.columns 
                WHERE table_name = 'restaurants'
            """))
            
            column_count = result.fetchone()[0]
            logger.info(f"✅ Total columns in restaurants table: {column_count}")
            
            return True
            
    except Exception as e:
        logger.error(f"Error verifying migration: {e}")
        return False

if __name__ == "__main__":
    logger.info("Starting redundant columns cleanup migration")
    
    if run_migration():
        logger.info("Migration completed successfully")
        
        if verify_migration():
            logger.info("✅ Migration verification passed")
        else:
            logger.error("❌ Migration verification failed")
    else:
        logger.error("❌ Migration failed")
        sys.exit(1) 