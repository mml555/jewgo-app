#!/usr/bin/env python3
"""
Google Places Periodic Updater
==============================

This script runs periodic updates for Google Places data stored in the database.
It checks for places that need updating and fetches fresh data from the Google Places API.

Features:
- Batch processing to respect API rate limits
- Error handling and retry logic
- Statistics reporting
- Configurable update intervals
- Cleanup of old data

Usage:
    python scripts/maintenance/google_places_periodic_updater.py [--batch-size 10] [--cleanup-days 30]

Author: JewGo Development Team
Version: 1.0
Last Updated: 2024
"""

import os
import sys
import argparse
import time
from datetime import datetime
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent.parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from database.google_places_manager import GooglePlacesManager
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

def main():
    """Main function to run periodic Google Places updates."""
    parser = argparse.ArgumentParser(description='Run periodic Google Places updates')
    parser.add_argument('--batch-size', type=int, default=10, 
                       help='Number of places to update in each batch (default: 10)')
    parser.add_argument('--cleanup-days', type=int, default=30,
                       help='Clean up data older than this many days (default: 30)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be updated without making changes')
    parser.add_argument('--stats-only', action='store_true',
                       help='Only show statistics without running updates')
    
    args = parser.parse_args()
    
    # Check environment variables
    if not os.getenv('DATABASE_URL'):
        logger.error("DATABASE_URL environment variable is required")
        sys.exit(1)
    
    if not os.getenv('GOOGLE_PLACES_API_KEY'):
        logger.warning("GOOGLE_PLACES_API_KEY not set - updates will be limited")
    
    try:
        # Initialize the Google Places manager
        manager = GooglePlacesManager()
        
        # Get initial statistics
        stats = manager.get_statistics()
        logger.info("Google Places Data Statistics", **stats)
        
        if args.stats_only:
            print("\n📊 Google Places Data Statistics:")
            print(f"   Total Records: {stats.get('total_records', 0)}")
            print(f"   Active Records: {stats.get('active_records', 0)}")
            print(f"   Records Needing Update: {stats.get('records_needing_update', 0)}")
            print(f"   Records with Errors: {stats.get('error_records', 0)}")
            return
        
        # Get places that need updating
        places_needing_update = manager.get_places_needing_update(args.batch_size)
        
        if not places_needing_update:
            logger.info("No places need updating at this time")
            return
        
        logger.info(f"Found {len(places_needing_update)} places needing updates")
        
        if args.dry_run:
            print(f"\n🔍 DRY RUN - Would update {len(places_needing_update)} places:")
            for place in places_needing_update:
                print(f"   • {place.name} (ID: {place.google_place_id})")
                print(f"     Last updated: {place.last_updated}")
                print(f"     Error count: {place.error_count}")
            return
        
        # Run the updates
        print(f"\n🔄 Running periodic updates for {len(places_needing_update)} places...")
        start_time = time.time()
        
        update_stats = manager.run_periodic_updates(args.batch_size)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Report results
        print(f"\n✅ Update completed in {duration:.2f} seconds:")
        print(f"   Total Processed: {update_stats['total_processed']}")
        print(f"   Successful Updates: {update_stats['successful_updates']}")
        print(f"   Failed Updates: {update_stats['failed_updates']}")
        print(f"   Skipped Updates: {update_stats['skipped_updates']}")
        
        # Clean up old data
        if args.cleanup_days > 0:
            print(f"\n🧹 Cleaning up data older than {args.cleanup_days} days...")
            cleaned_count = manager.cleanup_old_data(args.cleanup_days)
            print(f"   Marked {cleaned_count} old records as inactive")
        
        # Get final statistics
        final_stats = manager.get_statistics()
        logger.info("Final statistics after updates", **final_stats)
        
        print(f"\n📊 Final Statistics:")
        print(f"   Total Records: {final_stats.get('total_records', 0)}")
        print(f"   Active Records: {final_stats.get('active_records', 0)}")
        print(f"   Records Needing Update: {final_stats.get('records_needing_update', 0)}")
        print(f"   Records with Errors: {final_stats.get('error_records', 0)}")
        
        # Disconnect from database
        manager.disconnect()
        
    except Exception as e:
        logger.error(f"Error running periodic updates: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 