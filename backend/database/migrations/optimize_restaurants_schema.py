#!/usr/bin/env python3
"""
Migration script to optimize the restaurants table schema.
This migration implements the new optimized schema design.

Changes:
1. Add new required fields
2. Remove deprecated fields
3. Update field constraints
4. Add proper indexes
5. Update data types where needed
"""

import os
import sys
from sqlalchemy import create_engine, text, MetaData, Table, Column, String, Boolean, DateTime, Float, Integer, Text
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
    """Run the migration to optimize the restaurants table schema."""
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
                logger.info("Starting restaurants table schema optimization")
                
                # 1. Add new required fields
                new_columns = [
                    ("current_time_local", "TIMESTAMP"),
                    ("hours_parsed", "BOOLEAN DEFAULT FALSE"),
                    ("timezone", "VARCHAR(50)"),
                    ("phone_number", "VARCHAR(50)"),  # Rename from 'phone'
                    ("listing_type", "VARCHAR(100)"),  # Rename from 'category'
                    ("hours_of_operation", "TEXT"),  # Rename from 'hours_open'
                    ("specials", "TEXT"),  # New field for admin-managed specials
                ]
                
                for column_name, column_type in new_columns:
                    try:
                        # Check if column exists
                        result = conn.execute(text(f"""
                            SELECT column_name 
                            FROM information_schema.columns 
                            WHERE table_name = 'restaurants' 
                            AND column_name = '{column_name}'
                        """))
                        
                        if not result.fetchone():
                            logger.info(f"Adding column {column_name} to restaurants table")
                            conn.execute(text(f"ALTER TABLE restaurants ADD COLUMN {column_name} {column_type}"))
                            logger.info(f"Successfully added column {column_name}")
                        else:
                            logger.info(f"Column {column_name} already exists, skipping")
                            
                    except Exception as e:
                        logger.error(f"Error adding column {column_name}: {e}")
                        raise
                
                # 2. Update existing columns to be NOT NULL where required
                required_columns = [
                    "name", "address", "city", "state", "zip_code", 
                    "phone_number", "certifying_agency", "kosher_category", "listing_type"
                ]
                
                for column_name in required_columns:
                    try:
                        # Check if column can be made NOT NULL (no NULL values)
                        result = conn.execute(text(f"""
                            SELECT COUNT(*) 
                            FROM restaurants 
                            WHERE {column_name} IS NULL
                        """))
                        null_count = result.fetchone()[0]
                        
                        if null_count == 0:
                            logger.info(f"Making column {column_name} NOT NULL")
                            conn.execute(text(f"ALTER TABLE restaurants ALTER COLUMN {column_name} SET NOT NULL"))
                            logger.info(f"Successfully made {column_name} NOT NULL")
                        else:
                            logger.warning(f"Column {column_name} has {null_count} NULL values, skipping NOT NULL constraint")
                            
                    except Exception as e:
                        logger.error(f"Error updating column {column_name}: {e}")
                        # Continue with other columns
                
                # 3. Set default values for certifying_agency
                logger.info("Setting default value for certifying_agency")
                conn.execute(text("""
                    UPDATE restaurants 
                    SET certifying_agency = 'ORB' 
                    WHERE certifying_agency IS NULL OR certifying_agency = ''
                """))
                
                # 4. Migrate data from old column names to new ones
                logger.info("Migrating data from old column names to new ones")
                
                # Migrate phone to phone_number
                conn.execute(text("""
                    UPDATE restaurants 
                    SET phone_number = phone 
                    WHERE phone_number IS NULL AND phone IS NOT NULL
                """))
                
                # Migrate category to listing_type
                conn.execute(text("""
                    UPDATE restaurants 
                    SET listing_type = category 
                    WHERE listing_type IS NULL AND category IS NOT NULL
                """))
                
                # Migrate hours_open to hours_of_operation
                conn.execute(text("""
                    UPDATE restaurants 
                    SET hours_of_operation = hours_open 
                    WHERE hours_of_operation IS NULL AND hours_open IS NOT NULL
                """))
                
                # Migrate kosher_type to kosher_category
                conn.execute(text("""
                    UPDATE restaurants 
                    SET kosher_category = kosher_type 
                    WHERE kosher_category IS NULL AND kosher_type IS NOT NULL
                """))
                
                # 5. Remove deprecated columns
                deprecated_columns = [
                    "detail_url", "email", "kosher_cert_link", "next_open_time", 
                    "is_open", "status_reason", "phone", "category", "hours_open", 
                    "kosher_type", "cuisine_type", "hours"
                ]
                
                for column_name in deprecated_columns:
                    try:
                        # Check if column exists
                        result = conn.execute(text(f"""
                            SELECT column_name 
                            FROM information_schema.columns 
                            WHERE table_name = 'restaurants' 
                            AND column_name = '{column_name}'
                        """))
                        
                        if result.fetchone():
                            logger.info(f"Removing deprecated column {column_name}")
                            conn.execute(text(f"ALTER TABLE restaurants DROP COLUMN {column_name}"))
                            logger.info(f"Successfully removed column {column_name}")
                        else:
                            logger.info(f"Column {column_name} doesn't exist, skipping removal")
                            
                    except Exception as e:
                        logger.error(f"Error removing column {column_name}: {e}")
                        # Continue with other columns
                
                # 6. Add indexes for better performance
                indexes = [
                    ("idx_restaurants_kosher_category", "kosher_category"),
                    ("idx_restaurants_certifying_agency", "certifying_agency"),
                    ("idx_restaurants_state", "state"),
                    ("idx_restaurants_city", "city"),
                    ("idx_restaurants_created_at", "created_at"),
                    ("idx_restaurants_location", "latitude, longitude"),
                ]
                
                for index_name, columns in indexes:
                    try:
                        # Check if index exists
                        result = conn.execute(text(f"""
                            SELECT indexname 
                            FROM pg_indexes 
                            WHERE tablename = 'restaurants' 
                            AND indexname = '{index_name}'
                        """))
                        
                        if not result.fetchone():
                            logger.info(f"Creating index {index_name}")
                            conn.execute(text(f"CREATE INDEX {index_name} ON restaurants ({columns})"))
                            logger.info(f"Successfully created index {index_name}")
                        else:
                            logger.info(f"Index {index_name} already exists, skipping")
                            
                    except Exception as e:
                        logger.error(f"Error creating index {index_name}: {e}")
                        # Continue with other indexes
                
                # 7. Update current_time_local for all existing records
                logger.info("Updating current_time_local for existing records")
                conn.execute(text("""
                    UPDATE restaurants 
                    SET current_time_local = created_at 
                    WHERE current_time_local IS NULL
                """))
                
                # Commit transaction
                trans.commit()
                logger.info("Schema optimization completed successfully")
                return True
                
            except Exception as e:
                trans.rollback()
                logger.error(f"Migration failed: {e}")
                return False
                
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        return False

def verify_migration():
    """Verify that the migration was successful."""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        logger.error("DATABASE_URL environment variable is required")
        return False
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Check required columns exist
            required_columns = [
                "name", "address", "city", "state", "zip_code", 
                "phone_number", "certifying_agency", "kosher_category", "listing_type"
            ]
            
            for column_name in required_columns:
                result = conn.execute(text(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'restaurants' 
                    AND column_name = '{column_name}'
                    AND is_nullable = 'NO'
                """))
                
                if not result.fetchone():
                    logger.error(f"Required column {column_name} is missing or nullable")
                    return False
            
            # Check deprecated columns are removed
            deprecated_columns = ["detail_url", "email", "kosher_cert_link"]
            
            for column_name in deprecated_columns:
                result = conn.execute(text(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'restaurants' 
                    AND column_name = '{column_name}'
                """))
                
                if result.fetchone():
                    logger.error(f"Deprecated column {column_name} still exists")
                    return False
            
            # Check data integrity
            result = conn.execute(text("SELECT COUNT(*) FROM restaurants"))
            total_count = result.fetchone()[0]
            logger.info(f"Total restaurants: {total_count}")
            
            result = conn.execute(text("SELECT COUNT(*) FROM restaurants WHERE certifying_agency = 'ORB'"))
            orb_count = result.fetchone()[0]
            logger.info(f"ORB restaurants: {orb_count}")
            
            logger.info("Migration verification completed successfully")
            return True
            
    except Exception as e:
        logger.error(f"Verification failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting restaurants table schema optimization...")
    
    success = run_migration()
    if success:
        print("✅ Migration completed successfully")
        
        print("🔍 Verifying migration...")
        if verify_migration():
            print("✅ Migration verification passed")
            sys.exit(0)
        else:
            print("❌ Migration verification failed")
            sys.exit(1)
    else:
        print("❌ Migration failed")
        sys.exit(1) 