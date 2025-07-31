#!/usr/bin/env python3
"""
Periodic Hours Updater
======================

Automatically checks and updates restaurant hours according to Google Places data.
Can be run on a schedule (daily, weekly, etc.) to keep hours current.

Features:
- Updates existing hours data with fresh Google Places data
- Tracks when hours were last updated
- Handles restaurants with and without existing hours
- Configurable update frequency and batch sizes
- Comprehensive logging and reporting
"""

import os
import sys
import requests
import time
import json
from typing import Dict, List, Optional, Any
from sqlalchemy import create_engine, text
import structlog
from datetime import datetime, timedelta
import argparse

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

class PeriodicHoursUpdater:
    """Periodic hours updater that keeps restaurant hours current with Google Places."""
    
    def __init__(self, api_key: str, database_url: str = None):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        self.database_url = database_url or "postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
        
        # Quota management
        self.daily_requests = 0
        self.max_daily_requests = 100000  # Higher limit with billing
        self.last_request_time = None
        self.min_request_interval = 0.2  # 200ms between requests
        
        logger.info("Periodic hours updater initialized", api_key_length=len(api_key))
    
    def check_quota_status(self) -> bool:
        """Check if we can make API requests."""
        if self.daily_requests >= self.max_daily_requests:
            logger.warning("Daily quota limit reached", daily_requests=self.daily_requests, max_requests=self.max_daily_requests)
            return False
        return True
    
    def make_api_request(self, url: str, params: Dict) -> Optional[Dict]:
        """Make an API request with quota management."""
        if not self.check_quota_status():
            return None
        
        # Rate limiting
        if self.last_request_time:
            time_since_last = time.time() - self.last_request_time
            if time_since_last < self.min_request_interval:
                time.sleep(self.min_request_interval - time_since_last)
        
        try:
            response = requests.get(url, params=params, timeout=10)
            self.last_request_time = time.time()
            self.daily_requests += 1
            
            data = response.json()
            
            if data.get('status') == 'OVER_QUERY_LIMIT':
                logger.error("Quota exceeded during request", daily_requests=self.daily_requests)
                return None
            elif data.get('status') == 'REQUEST_DENIED':
                logger.error("Request denied", error=data.get('error_message'))
                return None
            
            return data
            
        except Exception as e:
            logger.error("API request failed", error=str(e))
            return None
    
    def search_place(self, restaurant_name: str, address: str) -> Optional[str]:
        """Search for a place with quota management."""
        query = f"{restaurant_name} {address}"
        url = f"{self.base_url}/textsearch/json"
        params = {
            'query': query,
            'key': self.api_key,
            'type': 'restaurant'
        }
        
        logger.info(f"Searching Google Places for: {query}")
        data = self.make_api_request(url, params)
        
        if data and data.get('status') == 'OK' and data.get('results'):
            place_id = data['results'][0]['place_id']
            logger.info(f"Found place_id: {place_id} for {restaurant_name}")
            return place_id
        
        logger.warning(f"No place found for: {query}")
        return None
    
    def get_place_details(self, place_id: str) -> Optional[Dict[str, Any]]:
        """Get place details with quota management."""
        url = f"{self.base_url}/details/json"
        params = {
            'place_id': place_id,
            'fields': 'name,formatted_address,opening_hours,formatted_phone_number,website,rating,user_ratings_total,price_level,types',
            'key': self.api_key
        }
        
        logger.info(f"Getting place details for place_id: {place_id}")
        data = self.make_api_request(url, params)
        
        if data and data.get('status') == 'OK':
            result = data['result']
            logger.info(f"Retrieved place details", name=result.get('name'), has_hours=bool(result.get('opening_hours')))
            return result
        
        logger.warning(f"Error getting place details for {place_id}")
        return None
    
    def format_hours_from_places_api(self, opening_hours: Dict) -> str:
        """Format opening hours from Google Places API format."""
        if not opening_hours or 'weekday_text' not in opening_hours:
            return ""
        
        weekday_text = opening_hours['weekday_text']
        day_mapping = {
            'Monday': 'Mon', 'Tuesday': 'Tue', 'Wednesday': 'Wed',
            'Thursday': 'Thu', 'Friday': 'Fri', 'Saturday': 'Sat', 'Sunday': 'Sun'
        }
        
        formatted_hours = []
        for day_text in weekday_text:
            if ': ' in day_text:
                day, hours = day_text.split(': ', 1)
                short_day = day_mapping.get(day, day[:3])
                formatted_hours.append(f"{short_day} {hours}")
        
        return ', '.join(formatted_hours)
    
    def get_restaurants_for_periodic_update(self, days_since_update: int = 7, limit: int = None) -> List[Dict[str, Any]]:
        """
        Get restaurants that need periodic hours updates.
        
        Args:
            days_since_update: Update restaurants whose hours are older than this many days
            limit: Maximum number of restaurants to process
        """
        try:
            engine = create_engine(self.database_url)
            
            with engine.connect() as conn:
                # Get restaurants that need updating
                query = """
                    SELECT id, name, address, city, state, hours_open, updated_at
                    FROM restaurants 
                    WHERE (
                        -- Restaurants without hours
                        (hours_open IS NULL OR hours_open = '' OR hours_open = 'None')
                    ) OR (
                        -- Restaurants with old hours (older than specified days)
                        updated_at < NOW() - INTERVAL ':days days'
                    )
                    AND name IS NOT NULL
                    ORDER BY 
                        CASE 
                            WHEN hours_open IS NULL OR hours_open = '' OR hours_open = 'None' THEN 1
                            ELSE 2
                        END,
                        updated_at ASC
                """
                
                if limit:
                    query += f" LIMIT {limit}"
                
                result = conn.execute(text(query), {"days": days_since_update})
                restaurants = [dict(row._mapping) for row in result.fetchall()]
                
                logger.info(f"Found {len(restaurants)} restaurants for periodic update", 
                           days_since_update=days_since_update, limit=limit)
                return restaurants
                
        except Exception as e:
            logger.error(f"Error getting restaurants for periodic update", error=str(e))
            return []
    
    def update_restaurant_hours(self, restaurant_id: int, hours_open: str, place_details: Dict = None) -> bool:
        """
        Update restaurant hours in the database with additional metadata.
        """
        try:
            engine = create_engine(self.database_url)
            
            with engine.begin() as conn:
                # Update hours and metadata
                update_data = {
                    "hours_open": hours_open,
                    "restaurant_id": restaurant_id,
                    "updated_at": datetime.utcnow()
                }
                
                # Add additional metadata if available
                if place_details:
                    if place_details.get('formatted_phone_number'):
                        update_data["phone"] = place_details['formatted_phone_number']
                    if place_details.get('website'):
                        update_data["website"] = place_details['website']
                    if place_details.get('rating'):
                        update_data["rating"] = place_details['rating']
                
                # Build dynamic update query
                set_clauses = []
                params = {"restaurant_id": restaurant_id}
                
                for key, value in update_data.items():
                    if key != "restaurant_id":
                        set_clauses.append(f"{key} = :{key}")
                        params[key] = value
                
                query = f"""
                    UPDATE restaurants 
                    SET {', '.join(set_clauses)}
                    WHERE id = :restaurant_id
                """
                
                result = conn.execute(text(query), params)
                
                if result.rowcount > 0:
                    logger.info(f"Updated restaurant ID {restaurant_id}", 
                               hours=hours_open, additional_fields=len(set_clauses)-1)
                    return True
                else:
                    logger.warning(f"No restaurant found with ID {restaurant_id}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error updating restaurant hours", restaurant_id=restaurant_id, error=str(e))
            return False
    
    def process_restaurant_periodic_update(self, restaurant: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single restaurant for periodic hours update.
        Returns detailed results about the update.
        """
        try:
            restaurant_id = restaurant.get('id')
            restaurant_name = restaurant.get('name', '')
            address = restaurant.get('address', '')
            existing_hours = restaurant.get('hours_open', '')
            last_updated = restaurant.get('updated_at')
            
            if not restaurant_name or not address:
                logger.warning(f"Skipping restaurant {restaurant_id}: missing name or address")
                return {
                    'restaurant_id': restaurant_id,
                    'restaurant_name': restaurant_name,
                    'status': 'skipped',
                    'reason': 'missing_name_or_address',
                    'hours_updated': False
                }
            
            # Check quota before processing
            if not self.check_quota_status():
                logger.warning(f"Skipping {restaurant_name}: quota limit reached")
                return {
                    'restaurant_id': restaurant_id,
                    'restaurant_name': restaurant_name,
                    'status': 'skipped',
                    'reason': 'quota_limit_reached',
                    'hours_updated': False
                }
            
            logger.info(f"Processing periodic update for: {restaurant_name}", 
                       id=restaurant_id, existing_hours=bool(existing_hours), last_updated=last_updated)
            
            # Search for the place
            place_id = self.search_place(restaurant_name, address)
            if not place_id:
                return {
                    'restaurant_id': restaurant_id,
                    'restaurant_name': restaurant_name,
                    'status': 'not_found',
                    'reason': 'place_not_found_in_google',
                    'hours_updated': False
                }
            
            # Get place details
            place_details = self.get_place_details(place_id)
            if not place_details:
                return {
                    'restaurant_id': restaurant_id,
                    'restaurant_name': restaurant_name,
                    'status': 'error',
                    'reason': 'could_not_get_place_details',
                    'hours_updated': False
                }
            
            # Get opening hours
            opening_hours = place_details.get('opening_hours')
            if not opening_hours:
                return {
                    'restaurant_id': restaurant_id,
                    'restaurant_name': restaurant_name,
                    'status': 'no_hours',
                    'reason': 'no_hours_in_google_places',
                    'hours_updated': False
                }
            
            # Format hours
            new_hours = self.format_hours_from_places_api(opening_hours)
            if not new_hours:
                return {
                    'restaurant_id': restaurant_id,
                    'restaurant_name': restaurant_name,
                    'status': 'error',
                    'reason': 'could_not_format_hours',
                    'hours_updated': False
                }
            
            # Check if hours have changed
            hours_changed = existing_hours != new_hours
            
            # Update database
            success = self.update_restaurant_hours(restaurant_id, new_hours, place_details)
            
            if success:
                return {
                    'restaurant_id': restaurant_id,
                    'restaurant_name': restaurant_name,
                    'status': 'updated',
                    'reason': 'hours_updated_successfully',
                    'hours_updated': True,
                    'hours_changed': hours_changed,
                    'old_hours': existing_hours,
                    'new_hours': new_hours,
                    'additional_data_updated': bool(place_details.get('formatted_phone_number') or place_details.get('website'))
                }
            else:
                return {
                    'restaurant_id': restaurant_id,
                    'restaurant_name': restaurant_name,
                    'status': 'error',
                    'reason': 'database_update_failed',
                    'hours_updated': False
                }
                
        except Exception as e:
            logger.error(f"Error processing restaurant {restaurant.get('name', 'Unknown')}", error=str(e))
            return {
                'restaurant_id': restaurant.get('id'),
                'restaurant_name': restaurant.get('name', 'Unknown'),
                'status': 'error',
                'reason': 'exception_occurred',
                'hours_updated': False,
                'error': str(e)
            }
    
    def run_periodic_update(self, days_since_update: int = 7, limit: int = None) -> Dict[str, Any]:
        """
        Run periodic hours update for restaurants.
        
        Args:
            days_since_update: Update restaurants whose hours are older than this many days
            limit: Maximum number of restaurants to process
        """
        try:
            restaurants = self.get_restaurants_for_periodic_update(days_since_update, limit)
            
            if not restaurants:
                logger.info("No restaurants found for periodic update")
                return {
                    'total_processed': 0,
                    'updated': 0,
                    'not_found': 0,
                    'no_hours': 0,
                    'errors': 0,
                    'skipped': 0,
                    'quota_exceeded': False,
                    'daily_requests': self.daily_requests,
                    'results': []
                }
            
            logger.info(f"Starting periodic update for {len(restaurants)} restaurants", 
                       days_since_update=days_since_update, limit=limit)
            
            results = []
            updated_count = 0
            not_found_count = 0
            no_hours_count = 0
            error_count = 0
            skipped_count = 0
            quota_exceeded = False
            
            for i, restaurant in enumerate(restaurants, 1):
                logger.info(f"Processing {i}/{len(restaurants)}: {restaurant.get('name', 'Unknown')}")
                
                if not self.check_quota_status():
                    logger.warning("Quota limit reached, stopping processing")
                    quota_exceeded = True
                    break
                
                result = self.process_restaurant_periodic_update(restaurant)
                results.append(result)
                
                # Count results
                if result['status'] == 'updated':
                    updated_count += 1
                elif result['status'] == 'not_found':
                    not_found_count += 1
                elif result['status'] == 'no_hours':
                    no_hours_count += 1
                elif result['status'] == 'error':
                    error_count += 1
                elif result['status'] == 'skipped':
                    skipped_count += 1
                
                # Progress update every 10 restaurants
                if i % 10 == 0:
                    logger.info(f"Progress: {i}/{len(restaurants)} completed", 
                              updated=updated_count, not_found=not_found_count, 
                              errors=error_count, daily_requests=self.daily_requests)
            
            logger.info(f"Periodic update complete", 
                       total_processed=len(restaurants),
                       updated=updated_count, not_found=not_found_count,
                       no_hours=no_hours_count, errors=error_count,
                       skipped=skipped_count, daily_requests=self.daily_requests,
                       quota_exceeded=quota_exceeded)
            
            return {
                'total_processed': len(restaurants),
                'updated': updated_count,
                'not_found': not_found_count,
                'no_hours': no_hours_count,
                'errors': error_count,
                'skipped': skipped_count,
                'quota_exceeded': quota_exceeded,
                'daily_requests': self.daily_requests,
                'results': results
            }
            
        except Exception as e:
            logger.error(f"Error in periodic update", error=str(e))
            return {
                'total_processed': 0,
                'updated': 0,
                'not_found': 0,
                'no_hours': 0,
                'errors': 1,
                'skipped': 0,
                'quota_exceeded': False,
                'daily_requests': self.daily_requests,
                'results': [],
                'error': str(e)
            }

def main():
    """Main function to run the periodic hours updater."""
    parser = argparse.ArgumentParser(description='Periodic Hours Updater')
    parser.add_argument('--days', type=int, default=7, 
                       help='Update restaurants whose hours are older than this many days (default: 7)')
    parser.add_argument('--limit', type=int, default=None,
                       help='Maximum number of restaurants to process (default: no limit)')
    parser.add_argument('--interactive', action='store_true',
                       help='Run in interactive mode')
    
    args = parser.parse_args()
    
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not api_key:
        logger.error("GOOGLE_PLACES_API_KEY environment variable not set")
        print("Please set your Google Places API key:")
        print("export GOOGLE_PLACES_API_KEY='your_api_key_here'")
        return
    
    updater = PeriodicHoursUpdater(api_key)
    
    if args.interactive:
        print("Periodic Hours Updater")
        print("1. Update restaurants with old hours (default: 7 days)")
        print("2. Update restaurants with old hours (custom days)")
        print("3. Update all restaurants without hours")
        print("4. Update with limit")
        print("5. Check quota status")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            results = updater.run_periodic_update(days_since_update=7, limit=args.limit)
        elif choice == '2':
            days = input("Enter days since last update: ").strip()
            days = int(days) if days else 7
            results = updater.run_periodic_update(days_since_update=days, limit=args.limit)
        elif choice == '3':
            results = updater.run_periodic_update(days_since_update=999999, limit=args.limit)  # Very old
        elif choice == '4':
            limit = input("Enter limit: ").strip()
            limit = int(limit) if limit else 10
            results = updater.run_periodic_update(days_since_update=args.days, limit=limit)
        elif choice == '5':
            print(f"Daily requests used: {updater.daily_requests}")
            print(f"Max daily requests: {updater.max_daily_requests}")
            print(f"Quota available: {updater.max_daily_requests - updater.daily_requests}")
            return
        else:
            print("Invalid choice")
            return
    else:
        # Non-interactive mode
        results = updater.run_periodic_update(days_since_update=args.days, limit=args.limit)
    
    # Print results
    print(f"\n📊 Periodic Update Results")
    print("=" * 40)
    print(f"Total processed: {results['total_processed']}")
    print(f"Updated: {results['updated']}")
    print(f"Not found in Google: {results['not_found']}")
    print(f"No hours available: {results['no_hours']}")
    print(f"Errors: {results['errors']}")
    print(f"Skipped: {results['skipped']}")
    print(f"Daily requests used: {results['daily_requests']}")
    
    if results['quota_exceeded']:
        print(f"⚠️  Quota limit reached during processing")

if __name__ == "__main__":
    main() 