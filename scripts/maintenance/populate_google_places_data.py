#!/usr/bin/env python3
"""
Populate Google Places Data
===========================

This script populates Google Places data for existing restaurants in the database.
It searches for each restaurant on Google Places and stores the data for future use.

Features:
- Batch processing to respect API rate limits
- Error handling and retry logic
- Progress tracking
- Statistics reporting
- Configurable search parameters

Usage:
    python scripts/maintenance/populate_google_places_data.py [--batch-size 5] [--dry-run]

Author: JewGo Development Team
Version: 1.0
Last Updated: 2024
"""

import os
import sys
import argparse
import time
import requests
from datetime import datetime
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent.parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from database.google_places_manager import GooglePlacesManager
from database.database_manager_v3 import EnhancedDatabaseManager
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

class GooglePlacesPopulator:
    """Handles populating Google Places data for restaurants."""
    
    def __init__(self):
        """Initialize the populator."""
        self.api_key = os.getenv('GOOGLE_PLACES_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_PLACES_API_KEY environment variable is required")
        
        self.places_manager = GooglePlacesManager()
        self.db_manager = EnhancedDatabaseManager()
        
    def search_restaurant_on_google_places(self, restaurant_name: str, address: str) -> dict:
        """
        Search for a restaurant on Google Places API.
        
        Args:
            restaurant_name: Name of the restaurant
            address: Address of the restaurant
            
        Returns:
            dict: Google Places search results or None if not found
        """
        try:
            # Build search query
            query = f"{restaurant_name} {address}"
            
            # Search for the place
            search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            search_params = {
                'query': query,
                'key': self.api_key,
                'type': 'restaurant'
            }
            
            logger.info(f"Searching Google Places for: {query}")
            response = requests.get(search_url, params=search_params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                place_id = data['results'][0]['place_id']
                
                # Get detailed place information
                details_url = "https://maps.googleapis.com/maps/api/place/details/json"
                details_params = {
                    'place_id': place_id,
                    'fields': 'name,formatted_address,formatted_phone_number,website,rating,user_ratings_total,price_level,geometry,opening_hours,utc_offset,photos,types,reviews',
                    'key': self.api_key
                }
                
                logger.info(f"Getting place details for place_id: {place_id}")
                details_response = requests.get(details_url, params=details_params, timeout=10)
                details_response.raise_for_status()
                
                details_data = details_response.json()
                
                if details_data['status'] == 'OK':
                    # Add place_id to the result
                    details_data['result']['place_id'] = place_id
                    return details_data
                
            logger.warning(f"No place found for: {query}")
            return None
            
        except Exception as e:
            logger.error(f"Error searching Google Places for {restaurant_name}: {e}")
            return None
    
    def populate_restaurant_data(self, restaurant: dict) -> bool:
        """
        Populate Google Places data for a single restaurant.
        
        Args:
            restaurant: Restaurant data from the database
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            restaurant_id = restaurant['id']
            name = restaurant['name']
            address = restaurant['address']
            city = restaurant['city']
            state = restaurant['state']
            
            # Build full address
            full_address = f"{address}, {city}, {state}"
            
            # Check if data already exists
            existing_data = self.places_manager.get_place_data(restaurant_id)
            if existing_data:
                logger.info(f"Google Places data already exists for restaurant {name} (ID: {restaurant_id})")
                return True
            
            # Search for the restaurant on Google Places
            place_data = self.search_restaurant_on_google_places(name, full_address)
            
            if place_data:
                # Store the data
                success = self.places_manager.store_place_data(restaurant_id, place_data)
                if success:
                    logger.info(f"Successfully populated Google Places data for {name} (ID: {restaurant_id})")
                    return True
                else:
                    logger.error(f"Failed to store Google Places data for {name} (ID: {restaurant_id})")
                    return False
            else:
                logger.warning(f"No Google Places data found for {name} (ID: {restaurant_id})")
                return False
                
        except Exception as e:
            logger.error(f"Error populating data for restaurant {restaurant.get('name', 'Unknown')}: {e}")
            return False
    
    def populate_all_restaurants(self, batch_size: int = 5, dry_run: bool = False) -> dict:
        """
        Populate Google Places data for all restaurants.
        
        Args:
            batch_size: Number of restaurants to process in each batch
            dry_run: If True, only show what would be done without making changes
            
        Returns:
            dict: Statistics about the operation
        """
        stats = {
            'total_restaurants': 0,
            'processed': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'already_exists': 0
        }
        
        try:
            # Get all restaurants from the database
            restaurants = self.db_manager.get_restaurants(limit=1000)
            stats['total_restaurants'] = len(restaurants)
            
            logger.info(f"Found {len(restaurants)} restaurants to process")
            
            if dry_run:
                print(f"\n🔍 DRY RUN - Would process {len(restaurants)} restaurants:")
                for restaurant in restaurants[:10]:  # Show first 10
                    print(f"   • {restaurant['name']} - {restaurant['address']}, {restaurant['city']}, {restaurant['state']}")
                if len(restaurants) > 10:
                    print(f"   ... and {len(restaurants) - 10} more")
                return stats
            
            # Process restaurants in batches
            for i in range(0, len(restaurants), batch_size):
                batch = restaurants[i:i + batch_size]
                logger.info(f"Processing batch {i//batch_size + 1}/{(len(restaurants) + batch_size - 1)//batch_size}")
                
                for restaurant in batch:
                    stats['processed'] += 1
                    
                    # Check if data already exists
                    existing_data = self.places_manager.get_place_data(restaurant['id'])
                    if existing_data:
                        stats['already_exists'] += 1
                        logger.info(f"Skipping {restaurant['name']} - data already exists")
                        continue
                    
                    # Populate data
                    if self.populate_restaurant_data(restaurant):
                        stats['successful'] += 1
                    else:
                        stats['failed'] += 1
                    
                    # Add delay between API calls to respect rate limits
                    time.sleep(0.2)
                
                # Add delay between batches
                if i + batch_size < len(restaurants):
                    time.sleep(1)
            
            return stats
            
        except Exception as e:
            logger.error(f"Error populating restaurant data: {e}")
            return stats
    
    def cleanup(self):
        """Clean up resources."""
        self.places_manager.disconnect()
        self.db_manager.disconnect()

def main():
    """Main function to populate Google Places data."""
    parser = argparse.ArgumentParser(description='Populate Google Places data for restaurants')
    parser.add_argument('--batch-size', type=int, default=5, 
                       help='Number of restaurants to process in each batch (default: 5)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    parser.add_argument('--stats-only', action='store_true',
                       help='Only show statistics without populating data')
    
    args = parser.parse_args()
    
    # Check environment variables
    if not os.getenv('DATABASE_URL'):
        logger.error("DATABASE_URL environment variable is required")
        sys.exit(1)
    
    if not os.getenv('GOOGLE_PLACES_API_KEY'):
        logger.error("GOOGLE_PLACES_API_KEY environment variable is required")
        sys.exit(1)
    
    try:
        # Initialize the populator
        populator = GooglePlacesPopulator()
        
        if args.stats_only:
            # Show statistics only
            stats = populator.places_manager.get_statistics()
            print("\n📊 Google Places Data Statistics:")
            print(f"   Total Records: {stats.get('total_records', 0)}")
            print(f"   Active Records: {stats.get('active_records', 0)}")
            print(f"   Records Needing Update: {stats.get('records_needing_update', 0)}")
            print(f"   Records with Errors: {stats.get('error_records', 0)}")
            return
        
        # Run the population
        print(f"\n🔄 Populating Google Places data for restaurants...")
        start_time = time.time()
        
        stats = populator.populate_all_restaurants(args.batch_size, args.dry_run)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Report results
        print(f"\n✅ Population completed in {duration:.2f} seconds:")
        print(f"   Total Restaurants: {stats['total_restaurants']}")
        print(f"   Processed: {stats['processed']}")
        print(f"   Successful: {stats['successful']}")
        print(f"   Failed: {stats['failed']}")
        print(f"   Skipped (already exists): {stats['already_exists']}")
        
        # Clean up
        populator.cleanup()
        
    except Exception as e:
        logger.error(f"Error populating Google Places data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 