#!/usr/bin/env python3
"""
Database Migration: Add Google Places Table
===========================================

This migration creates the google_places_data table to store Google Places information
for restaurants, reducing API calls and improving performance.

Author: JewGo Development Team
Version: 1.0
Last Updated: 2024
"""

import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from database.google_places_manager import Base
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import structlog

# Configure structured logging
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
    """Run the migration to create the Google Places table."""
    try:
        # Get database URL
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            logger.error("DATABASE_URL environment variable is required")
            return False
        
        # Create engine
        engine = create_engine(database_url)
        
        # Create the table
        logger.info("Creating google_places_data table...")
        Base.metadata.create_all(bind=engine, tables=[Base.metadata.tables['google_places_data']])
        
        logger.info("✅ Successfully created google_places_data table")
        
        # Verify the table was created
        with engine.connect() as connection:
            result = connection.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'google_places_data')")
            table_exists = result.scalar()
            
            if table_exists:
                logger.info("✅ Table verification successful")
                
                # Show table structure
                result = connection.execute("""
                    SELECT column_name, data_type, is_nullable 
                    FROM information_schema.columns 
                    WHERE table_name = 'google_places_data' 
                    ORDER BY ordinal_position
                """)
                
                columns = result.fetchall()
                logger.info("Table structure:")
                for column in columns:
                    logger.info(f"  - {column[0]}: {column[1]} ({'NULL' if column[2] == 'YES' else 'NOT NULL'})")
            else:
                logger.error("❌ Table verification failed")
                return False
        
        return True
        
    except SQLAlchemyError as e:
        logger.error(f"Database error during migration: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during migration: {e}")
        return False

def rollback_migration():
    """Rollback the migration by dropping the table."""
    try:
        # Get database URL
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            logger.error("DATABASE_URL environment variable is required")
            return False
        
        # Create engine
        engine = create_engine(database_url)
        
        # Drop the table
        logger.info("Dropping google_places_data table...")
        with engine.connect() as connection:
            connection.execute("DROP TABLE IF EXISTS google_places_data")
            connection.commit()
        
        logger.info("✅ Successfully dropped google_places_data table")
        return True
        
    except SQLAlchemyError as e:
        logger.error(f"Database error during rollback: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during rollback: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Google Places table migration')
    parser.add_argument('--rollback', action='store_true', help='Rollback the migration')
    
    args = parser.parse_args()
    
    if args.rollback:
        print("🔄 Rolling back Google Places table migration...")
        success = rollback_migration()
        if success:
            print("✅ Rollback completed successfully")
        else:
            print("❌ Rollback failed")
            sys.exit(1)
    else:
        print("🔄 Running Google Places table migration...")
        success = run_migration()
        if success:
            print("✅ Migration completed successfully")
        else:
            print("❌ Migration failed")
            sys.exit(1) 