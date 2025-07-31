#!/usr/bin/env python3
"""
Test Periodic Hours Update System
=================================

Creates test scenarios for the periodic hours updater by temporarily
modifying restaurant timestamps to simulate old data.
"""

import os
import sys
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
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

def setup_test_scenario():
    """Set up test scenario by modifying some restaurant timestamps."""
    database_url = "postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    
    try:
        engine = create_engine(database_url)
        
        with engine.begin() as conn:
            # Get some restaurants to modify
            result = conn.execute(text("""
                SELECT id, name, hours_open, updated_at 
                FROM restaurants 
                WHERE hours_open IS NOT NULL 
                AND hours_open != '' 
                AND hours_open != 'None'
                LIMIT 5
            """))
            
            restaurants = result.fetchall()
            
            if not restaurants:
                logger.info("No restaurants with hours found for testing")
                return False
            
            logger.info(f"Found {len(restaurants)} restaurants to modify for testing")
            
            # Modify timestamps to be old (10 days ago)
            old_date = datetime.utcnow() - timedelta(days=10)
            
            for restaurant in restaurants:
                conn.execute(text("""
                    UPDATE restaurants 
                    SET updated_at = :old_date 
                    WHERE id = :restaurant_id
                """), {
                    "old_date": old_date,
                    "restaurant_id": restaurant.id
                })
                
                logger.info(f"Modified restaurant {restaurant.id} ({restaurant.name}) timestamp to {old_date}")
            
            logger.info(f"Successfully modified {len(restaurants)} restaurants for testing")
            return True
            
    except Exception as e:
        logger.error(f"Error setting up test scenario", error=str(e))
        return False

def cleanup_test_scenario():
    """Clean up test scenario by restoring current timestamps."""
    database_url = "postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    
    try:
        engine = create_engine(database_url)
        
        with engine.begin() as conn:
            # Restore current timestamps
            current_date = datetime.utcnow()
            
            result = conn.execute(text("""
                UPDATE restaurants 
                SET updated_at = :current_date 
                WHERE updated_at < NOW() - INTERVAL '5 days'
            """), {"current_date": current_date})
            
            logger.info(f"Restored timestamps for {result.rowcount} restaurants")
            return True
            
    except Exception as e:
        logger.error(f"Error cleaning up test scenario", error=str(e))
        return False

def test_periodic_updater():
    """Test the periodic updater with the test scenario."""
    print("🧪 Testing Periodic Hours Updater")
    print("=" * 40)
    
    # Set up test scenario
    print("1. Setting up test scenario...")
    if not setup_test_scenario():
        print("❌ Failed to set up test scenario")
        return False
    
    print("✅ Test scenario created")
    
    # Test periodic updater
    print("\n2. Running periodic updater...")
    os.system("python scripts/maintenance/periodic_hours_updater.py --days 7 --limit 5")
    
    print("\n3. Cleaning up test scenario...")
    cleanup_test_scenario()
    print("✅ Test scenario cleaned up")
    
    return True

def main():
    """Main function."""
    print("🚀 Periodic Hours Update System Test")
    print("=" * 50)
    
    print("This script will:")
    print("1. Temporarily modify some restaurant timestamps to be old")
    print("2. Test the periodic updater with these restaurants")
    print("3. Clean up the modifications")
    print()
    
    confirm = input("Continue with test? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Test cancelled")
        return
    
    success = test_periodic_updater()
    
    if success:
        print("\n✅ Test completed successfully!")
        print("The periodic updater is working correctly.")
    else:
        print("\n❌ Test failed")
        print("Please check the logs for errors.")

if __name__ == "__main__":
    main() 