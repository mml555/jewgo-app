#!/usr/bin/env python3
"""
Remove Duplicate Restaurants Script
==================================

This script removes duplicate restaurants from the database.
It keeps the oldest entry (lowest ID) for each restaurant name.

Author: JewGo Development Team
Version: 1.0
Last Updated: 2024
"""

import sys
import os
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database_manager_v3 import EnhancedDatabaseManager
from sqlalchemy import text
import structlog

# Configure structured logging
logger = structlog.get_logger()

def remove_duplicates():
    """Remove duplicate restaurants from the database."""
    try:
        # Initialize database manager
        db_manager = EnhancedDatabaseManager()
        db_manager.connect()
        
        logger.info("Starting duplicate removal process")
        
        # Get database session
        session = db_manager.get_session()
        
        # Find duplicates using SQL
        duplicate_query = text("""
            WITH duplicates AS (
                SELECT 
                    name,
                    MIN(id) as keep_id,
                    COUNT(*) as count
                FROM restaurants 
                GROUP BY name 
                HAVING COUNT(*) > 1
            )
            SELECT 
                d.name,
                d.keep_id,
                d.count,
                array_agg(r.id ORDER BY r.id) as all_ids
            FROM duplicates d
            JOIN restaurants r ON r.name = d.name
            GROUP BY d.name, d.keep_id, d.count
            ORDER BY d.name
        """)
        
        result = session.execute(duplicate_query)
        duplicates = result.fetchall()
        
        if not duplicates:
            logger.info("No duplicates found in database")
            return
        
        logger.info(f"Found {len(duplicates)} restaurants with duplicates")
        
        total_removed = 0
        
        for duplicate in duplicates:
            name = duplicate.name
            keep_id = duplicate.keep_id
            count = duplicate.count
            all_ids = duplicate.all_ids
            
            # Remove all except the oldest (lowest ID)
            ids_to_remove = [id for id in all_ids if id != keep_id]
            
            logger.info(f"Restaurant: {name}")
            logger.info(f"  - Keeping ID: {keep_id}")
            logger.info(f"  - Removing IDs: {ids_to_remove}")
            logger.info(f"  - Total duplicates: {count}")
            
            # Delete the duplicates
            delete_query = text("DELETE FROM restaurants WHERE id = ANY(:ids)")
            session.execute(delete_query, {"ids": ids_to_remove})
            
            total_removed += len(ids_to_remove)
        
        # Commit the changes
        session.commit()
        
        logger.info(f"Successfully removed {total_removed} duplicate restaurants")
        
        # Verify the results
        verify_query = text("SELECT COUNT(*) as total FROM restaurants")
        result = session.execute(verify_query)
        total_restaurants = result.fetchone().total
        
        logger.info(f"Total restaurants after cleanup: {total_restaurants}")
        
        # Check for any remaining duplicates
        remaining_duplicates_query = text("""
            SELECT name, COUNT(*) as count
            FROM restaurants 
            GROUP BY name 
            HAVING COUNT(*) > 1
            ORDER BY name
        """)
        
        result = session.execute(remaining_duplicates_query)
        remaining_duplicates = result.fetchall()
        
        if remaining_duplicates:
            logger.warning(f"Found {len(remaining_duplicates)} restaurants still with duplicates:")
            for dup in remaining_duplicates:
                logger.warning(f"  - {dup.name}: {dup.count} entries")
        else:
            logger.info("✅ No duplicates remaining in database")
        
    except Exception as e:
        logger.error(f"Error removing duplicates: {e}")
        if 'session' in locals():
            session.rollback()
        raise
    finally:
        if 'session' in locals():
            session.close()
        if 'db_manager' in locals():
            db_manager.disconnect()

def main():
    """Main function."""
    logger.info("Starting duplicate removal script")
    
    try:
        remove_duplicates()
        logger.info("Duplicate removal completed successfully")
    except Exception as e:
        logger.error(f"Duplicate removal failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 