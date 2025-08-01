#!/usr/bin/env python3
"""
Google Places System Deployment Script
=====================================

This script sets up the Google Places database system on the production server.
It runs the migration, populates initial data, and sets up monitoring.

Usage:
    python scripts/deployment/setup_google_places_system.py

Author: JewGo Development Team
Version: 1.0
Last Updated: 2024
"""

import os
import sys
import time
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent.parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from database.google_places_manager import GooglePlacesManager
from database.migrations.add_google_places_table import run_migration
from scripts.maintenance.populate_google_places_data import GooglePlacesPopulator
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

def setup_google_places_system():
    """Set up the complete Google Places system."""
    
    print("🚀 Setting up Google Places Database System...")
    print("=" * 50)
    
    # Step 1: Run Database Migration
    print("\n1️⃣ Running Database Migration...")
    try:
        success = run_migration()
        if success:
            print("✅ Database migration completed successfully")
        else:
            print("❌ Database migration failed")
            return False
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        return False
    
    # Step 2: Initialize Google Places Manager
    print("\n2️⃣ Initializing Google Places Manager...")
    try:
        manager = GooglePlacesManager()
        print("✅ Google Places Manager initialized")
    except Exception as e:
        print(f"❌ Error initializing manager: {e}")
        return False
    
    # Step 3: Get Initial Statistics
    print("\n3️⃣ Getting Initial Statistics...")
    try:
        stats = manager.get_statistics()
        print(f"📊 Initial Statistics:")
        print(f"   Total Records: {stats.get('total_records', 0)}")
        print(f"   Active Records: {stats.get('active_records', 0)}")
        print(f"   Records Needing Update: {stats.get('records_needing_update', 0)}")
        print(f"   Records with Errors: {stats.get('error_records', 0)}")
    except Exception as e:
        print(f"❌ Error getting statistics: {e}")
        return False
    
    # Step 4: Populate Initial Data
    print("\n4️⃣ Populating Initial Data...")
    try:
        populator = GooglePlacesPopulator()
        
        # Run with conservative settings for production
        stats = populator.populate_all_restaurants(batch_size=3, dry_run=False)
        
        print(f"📊 Population Statistics:")
        print(f"   Total Restaurants: {stats['total_restaurants']}")
        print(f"   Processed: {stats['processed']}")
        print(f"   Successful: {stats['successful']}")
        print(f"   Failed: {stats['failed']}")
        print(f"   Skipped (already exists): {stats['already_exists']}")
        
        populator.cleanup()
    except Exception as e:
        print(f"❌ Error populating data: {e}")
        return False
    
    # Step 5: Run Initial Periodic Updates
    print("\n5️⃣ Running Initial Periodic Updates...")
    try:
        update_stats = manager.run_periodic_updates(batch_size=5)
        
        print(f"📊 Update Statistics:")
        print(f"   Total Processed: {update_stats['total_processed']}")
        print(f"   Successful Updates: {update_stats['successful_updates']}")
        print(f"   Failed Updates: {update_stats['failed_updates']}")
        print(f"   Skipped Updates: {update_stats['skipped_updates']}")
    except Exception as e:
        print(f"❌ Error running updates: {e}")
        return False
    
    # Step 6: Final Statistics
    print("\n6️⃣ Final Statistics...")
    try:
        final_stats = manager.get_statistics()
        print(f"📊 Final Statistics:")
        print(f"   Total Records: {final_stats.get('total_records', 0)}")
        print(f"   Active Records: {final_stats.get('active_records', 0)}")
        print(f"   Records Needing Update: {final_stats.get('records_needing_update', 0)}")
        print(f"   Records with Errors: {final_stats.get('error_records', 0)}")
    except Exception as e:
        print(f"❌ Error getting final statistics: {e}")
        return False
    
    # Step 7: Cleanup
    print("\n7️⃣ Cleanup...")
    try:
        manager.disconnect()
        print("✅ Cleanup completed")
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Google Places System Setup Complete!")
    print("\n📋 Next Steps:")
    print("1. Set up cron job for periodic updates:")
    print("   0 */6 * * * cd /path/to/jewgo-app && python scripts/maintenance/google_places_periodic_updater.py --batch-size 10")
    print("2. Monitor performance with:")
    print("   python scripts/maintenance/google_places_periodic_updater.py --stats-only")
    print("3. Check logs for any issues")
    
    return True

def main():
    """Main function."""
    # Check environment variables
    if not os.getenv('DATABASE_URL'):
        print("❌ DATABASE_URL environment variable is required")
        sys.exit(1)
    
    if not os.getenv('GOOGLE_PLACES_API_KEY'):
        print("❌ GOOGLE_PLACES_API_KEY environment variable is required")
        sys.exit(1)
    
    # Run the setup
    success = setup_google_places_system()
    
    if success:
        print("\n✅ Setup completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 