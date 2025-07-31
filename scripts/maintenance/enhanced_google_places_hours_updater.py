#!/usr/bin/env python3
"""
Enhanced Google Places Hours Updater
===================================

Fetches and updates restaurant hours using Google Places API.
Works with the current PostgreSQL database structure.

Author: JewGo Development Team
Version: 2.0
"""

import os
import sys
import requests
import time
import json
from typing import Dict, List, Optional, Any
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

class EnhancedGooglePlacesHoursUpdater:
    """Enhanced hours updater using Google Places API with current database structure."""
    
    def __init__(self, api_key: str, database_url: str = None):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        
        # Use provided database URL or get from environment
        self.database_url = database_url or "postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
        
        logger.info("Enhanced Google Places Hours Updater initialized", api_key_length=len(api_key))
    
    def search_place(self, restaurant_name: str, address: str) -> Optional[str]:
        """
        Search for a place using Google Places API.
        Returns the place_id if found.
        """
        try:
            # Build search query - use restaurant name and address
            query = f"{restaurant_name} {address}"
            
            # Make Places API request
            url = f"{self.base_url}/textsearch/json"
            params = {
                'query': query,
                'key': self.api_key,
                'type': 'restaurant'
            }
            
            logger.info(f"Searching Google Places for: {query}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                place_id = data['results'][0]['place_id']
                logger.info(f"Found place_id: {place_id} for {restaurant_name}")
                return place_id
            else:
                logger.warning(f"No place found for: {query}", status=data.get('status'))
                return None
                
        except Exception as e:
            logger.error(f"Error searching place for {restaurant_name}", error=str(e))
            return None
    
    def get_place_details(self, place_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a place including opening hours.
        """
        try:
            url = f"{self.base_url}/details/json"
            params = {
                'place_id': place_id,
                'fields': 'name,formatted_address,opening_hours,formatted_phone_number,website,rating,user_ratings_total,price_level,types',
                'key': self.api_key
            }
            
            logger.info(f"Getting place details for place_id: {place_id}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'OK':
                result = data['result']
                logger.info(f"Retrieved place details", name=result.get('name'), has_hours=bool(result.get('opening_hours')))
                return result
            else:
                logger.warning(f"Error getting place details", status=data.get('status'))
                return None
                
        except Exception as e:
            logger.error(f"Error getting place details", error=str(e))
            return None
    
    def format_hours_from_places_api(self, opening_hours: Dict) -> str:
        """
        Format opening hours from Google Places API format to our database format.
        """
        if not opening_hours or 'weekday_text' not in opening_hours:
            return None
            
        # Google Places API provides weekday_text as a list of formatted strings
        # e.g., ["Monday: 11:00 AM – 10:00 PM", "Tuesday: 11:00 AM – 10:00 PM", ...]
        weekday_text = opening_hours['weekday_text']
        
        # Convert to our format: "Mon 11:00 AM – 10:00 PM, Tue 11:00 AM – 10:00 PM, ..."
        day_mapping = {
            'Monday': 'Mon',
            'Tuesday': 'Tue', 
            'Wednesday': 'Wed',
            'Thursday': 'Thu',
            'Friday': 'Fri',
            'Saturday': 'Sat',
            'Sunday': 'Sun'
        }
        
        formatted_hours = []
        for day_text in weekday_text:
            # Parse "Monday: 11:00 AM – 10:00 PM"
            if ': ' in day_text:
                day, hours = day_text.split(': ', 1)
                short_day = day_mapping.get(day, day[:3])
                formatted_hours.append(f"{short_day} {hours}")
        
        return ', '.join(formatted_hours)
    
    def update_restaurant_hours(self, restaurant_id: int, hours_open: str) -> bool:
        """
        Update restaurant hours in the database.
        """
        try:
            engine = create_engine(self.database_url)
            
            with engine.begin() as conn:
                # Update the hours_open field
                result = conn.execute(text("""
                    UPDATE restaurants 
                    SET hours_open = :hours_open, updated_at = NOW()
                    WHERE id = :restaurant_id
                """), {"hours_open": hours_open, "restaurant_id": restaurant_id})
                
                if result.rowcount > 0:
                    logger.info(f"Updated hours for restaurant ID {restaurant_id}", hours=hours_open)
                    return True
                else:
                    logger.warning(f"No restaurant found with ID {restaurant_id}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error updating restaurant hours", restaurant_id=restaurant_id, error=str(e))
            return False
    
    def get_restaurants_without_hours(self, limit: int = None) -> List[Dict[str, Any]]:
        """
        Get restaurants that don't have hours data.
        """
        try:
            engine = create_engine(self.database_url)
            
            with engine.connect() as conn:
                query = """
                    SELECT id, name, address, city, state, hours_open, hours_of_operation
                    FROM restaurants 
                    WHERE (
                        (hours_open IS NULL OR hours_open = '' OR hours_open = 'None') 
                        AND (hours_of_operation IS NULL OR hours_of_operation = '' OR hours_of_operation = 'None')
                    ) OR (
                        (hours_open IS NULL OR hours_open = '' OR hours_open = 'None') 
                        AND (hours_of_operation IS NOT NULL AND hours_of_operation != '' AND hours_of_operation != 'None')
                    ) OR (
                        (hours_of_operation IS NULL OR hours_of_operation = '' OR hours_of_operation = 'None') 
                        AND (hours_open IS NOT NULL AND hours_open != '' AND hours_open != 'None')
                    )
                    AND name IS NOT NULL
                    ORDER BY name
                """
                
                if limit:
                    query += f" LIMIT {limit}"
                
                result = conn.execute(text(query))
                restaurants = [dict(row._mapping) for row in result.fetchall()]
                
                logger.info(f"Found {len(restaurants)} restaurants without hours")
                return restaurants
                
        except Exception as e:
            logger.error(f"Error getting restaurants without hours", error=str(e))
            return []
    
    def process_restaurant(self, restaurant: Dict[str, Any]) -> bool:
        """
        Process a single restaurant to find and update hours.
        """
        try:
            restaurant_id = restaurant.get('id')
            restaurant_name = restaurant.get('name', '')
            address = restaurant.get('address', '')
            existing_hours_open = restaurant.get('hours_open', '')
            existing_hours_of_operation = restaurant.get('hours_of_operation', '')
            
            if not restaurant_name or not address:
                logger.warning(f"Skipping restaurant {restaurant_id}: missing name or address")
                return False
            
            # Check if we already have some hours data
            if existing_hours_open and existing_hours_open != 'None' and existing_hours_open != '':
                logger.info(f"Restaurant {restaurant_name} already has hours_open", hours=existing_hours_open[:50])
                # If we have hours_open but not hours_of_operation, copy it
                if not existing_hours_of_operation or existing_hours_of_operation == 'None' or existing_hours_of_operation == '':
                    logger.info(f"Copying hours_open to hours_of_operation for {restaurant_name}")
                    return self.update_restaurant_hours(restaurant_id, existing_hours_open)
                return True
            
            if existing_hours_of_operation and existing_hours_of_operation != 'None' and existing_hours_of_operation != '':
                logger.info(f"Restaurant {restaurant_name} already has hours_of_operation", hours=existing_hours_of_operation[:50])
                # If we have hours_of_operation but not hours_open, copy it
                if not existing_hours_open or existing_hours_open == 'None' or existing_hours_open == '':
                    logger.info(f"Copying hours_of_operation to hours_open for {restaurant_name}")
                    return self.update_restaurant_hours(restaurant_id, existing_hours_of_operation)
                return True
            
            logger.info(f"Processing restaurant: {restaurant_name}", id=restaurant_id)
            
            # Search for the place
            place_id = self.search_place(restaurant_name, address)
            if not place_id:
                logger.warning(f"No place found for {restaurant_name}")
                return False
            
            # Get place details
            place_details = self.get_place_details(place_id)
            if not place_details:
                logger.warning(f"No details found for {restaurant_name}")
                return False
            
            # Get opening hours
            opening_hours = place_details.get('opening_hours')
            if not opening_hours:
                logger.warning(f"No opening hours found for {restaurant_name}")
                return False
            
            # Format hours
            hours_open = self.format_hours_from_places_api(opening_hours)
            if not hours_open:
                logger.warning(f"Could not format hours for {restaurant_name}")
                return False
            
            # Update database
            success = self.update_restaurant_hours(restaurant_id, hours_open)
            
            # Add delay to respect API rate limits
            time.sleep(0.2)  # 200ms delay between requests
            
            return success
            
        except Exception as e:
            logger.error(f"Error processing restaurant {restaurant.get('name', 'Unknown')}", error=str(e))
            return False
    
    def update_restaurants_without_hours(self, limit: int = None) -> Dict[str, int]:
        """
        Update hours for restaurants that don't have them.
        """
        try:
            # Get restaurants without hours
            restaurants = self.get_restaurants_without_hours(limit)
            
            if not restaurants:
                logger.info("No restaurants found without hours")
                return {'success': 0, 'failed': 0, 'skipped': 0, 'total': 0}
            
            logger.info(f"Processing {len(restaurants)} restaurants without hours")
            
            success_count = 0
            failed_count = 0
            skipped_count = 0
            
            for i, restaurant in enumerate(restaurants, 1):
                logger.info(f"Processing {i}/{len(restaurants)}: {restaurant.get('name', 'Unknown')}")
                
                if self.process_restaurant(restaurant):
                    success_count += 1
                else:
                    failed_count += 1
                
                # Progress update every 5 restaurants
                if i % 5 == 0:
                    logger.info(f"Progress: {i}/{len(restaurants)} completed", 
                              success=success_count, failed=failed_count)
            
            logger.info(f"Hours update complete", 
                       success=success_count, failed=failed_count, 
                       skipped=skipped_count, total=len(restaurants))
            
            return {
                'success': success_count,
                'failed': failed_count,
                'skipped': skipped_count,
                'total': len(restaurants)
            }
            
        except Exception as e:
            logger.error(f"Error updating restaurants without hours", error=str(e))
            return {'success': 0, 'failed': 0, 'skipped': 0, 'total': 0}
    
    def update_specific_restaurant(self, restaurant_id: int) -> bool:
        """
        Update hours for a specific restaurant by ID.
        """
        try:
            engine = create_engine(self.database_url)
            
            with engine.connect() as conn:
                # Get restaurant details
                result = conn.execute(text("""
                    SELECT id, name, address, city, state, hours_open, hours_of_operation
                    FROM restaurants 
                    WHERE id = :restaurant_id
                """), {"restaurant_id": restaurant_id})
                
                restaurant = result.fetchone()
                if not restaurant:
                    logger.error(f"Restaurant with ID {restaurant_id} not found")
                    return False
                
                restaurant_dict = dict(restaurant._mapping)
                return self.process_restaurant(restaurant_dict)
                
        except Exception as e:
            logger.error(f"Error updating specific restaurant", restaurant_id=restaurant_id, error=str(e))
            return False

def main():
    """Main function to run the hours updater."""
    
    # Get API key from environment variable
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not api_key:
        logger.error("GOOGLE_PLACES_API_KEY environment variable not set")
        print("Please set your Google Places API key:")
        print("export GOOGLE_PLACES_API_KEY='your_api_key_here'")
        return
    
    # Create updater instance
    updater = EnhancedGooglePlacesHoursUpdater(api_key)
    
    # Ask user what to do
    print("Enhanced Google Places Hours Updater")
    print("1. Update restaurants without hours (all)")
    print("2. Update restaurants without hours (limit)")
    print("3. Update specific restaurant by ID")
    print("4. Test with first 3 restaurants")
    
    choice = input("Enter your choice (1-4): ").strip()
    
    if choice == '1':
        results = updater.update_restaurants_without_hours()
        print(f"Results: {results}")
        
    elif choice == '2':
        limit = input("Enter limit: ").strip()
        limit = int(limit) if limit else 10
        results = updater.update_restaurants_without_hours(limit)
        print(f"Results: {results}")
        
    elif choice == '3':
        restaurant_id = input("Enter restaurant ID: ").strip()
        restaurant_id = int(restaurant_id) if restaurant_id else None
        if restaurant_id:
            success = updater.update_specific_restaurant(restaurant_id)
            print(f"Update {'successful' if success else 'failed'}")
        else:
            print("Invalid restaurant ID")
        
    elif choice == '4':
        results = updater.update_restaurants_without_hours(limit=3)
        print(f"Test results: {results}")
        
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main() 