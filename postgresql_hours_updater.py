#!/usr/bin/env python3
"""
PostgreSQL Hours Updater
Fetches missing hours data from Google Places API and updates PostgreSQL database.
"""

import os
import requests
import json
import time
import logging
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote_plus
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

class PostgreSQLHoursUpdater:
    def __init__(self):
        self.session = requests.Session()
        
    def connect_db(self):
        """Connect to PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(DATABASE_URL)
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False
    
    def get_restaurants_without_hours(self) -> List[Dict]:
        """Get restaurants that don't have hours data."""
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT id, name, address, city, state, hours_open, hours_of_operation
                    FROM restaurants 
                    WHERE (
                        (hours_open IS NULL OR hours_open = '' OR hours_open = 'None') 
                        AND (hours_of_operation IS NULL OR hours_of_operation = '' OR hours_of_operation = 'None')
                    )
                    AND name IS NOT NULL
                    AND status = 'active'
                    ORDER BY name
                """)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error getting restaurants without hours: {e}")
            return []
    
    def search_google_places(self, query: str, location: str = None) -> Optional[Dict]:
        """Search for a place using Google Places API Text Search."""
        if not GOOGLE_PLACES_API_KEY:
            logger.error("Google Places API key not found")
            return None
            
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        
        # Build search query
        search_query = query
        if location:
            search_query += f" {location}"
        
        params = {
            'query': search_query,
            'key': GOOGLE_PLACES_API_KEY,
            'type': 'restaurant'
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                return data['results'][0]  # Return first result
            else:
                logger.warning(f"No results found for: {search_query}")
                return None
                
        except Exception as e:
            logger.error(f"Error searching Google Places: {e}")
            return None
    
    def get_place_details(self, place_id: str) -> Optional[Dict]:
        """Get detailed information about a place using Google Places API."""
        if not GOOGLE_PLACES_API_KEY:
            logger.error("Google Places API key not found")
            return None
            
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        
        params = {
            'place_id': place_id,
            'key': GOOGLE_PLACES_API_KEY,
            'fields': 'name,formatted_address,opening_hours,formatted_phone_number,website,rating,user_ratings_total,price_level,types'
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK':
                return data['result']
            else:
                logger.warning(f"Error getting place details: {data['status']}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting place details: {e}")
            return None
    
    def format_hours_from_places_api(self, opening_hours: Dict) -> str:
        """Format opening hours from Google Places API format."""
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
    
    def update_restaurant_hours(self, restaurant_id: int, hours_open: str, hours_of_operation: str = None):
        """Update restaurant hours in the PostgreSQL database."""
        try:
            with self.conn.cursor() as cursor:
                if hours_of_operation:
                    cursor.execute("""
                        UPDATE restaurants 
                        SET hours_open = %s, hours_of_operation = %s, updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                    """, (hours_open, hours_of_operation, restaurant_id))
                else:
                    cursor.execute("""
                        UPDATE restaurants 
                        SET hours_open = %s, updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                    """, (hours_open, restaurant_id))
                
                self.conn.commit()
                logger.info(f"✅ Updated hours for restaurant ID {restaurant_id}")
                return True
        except Exception as e:
            logger.error(f"Error updating restaurant {restaurant_id}: {e}")
            self.conn.rollback()
            return False
    
    def process_restaurant(self, restaurant: Dict) -> bool:
        """Process a single restaurant to find and update hours."""
        logger.info(f"🔍 Processing: {restaurant['name']}")
        
        # Check if we already have some hours data
        existing_hours_open = restaurant.get('hours_open')
        existing_hours_of_operation = restaurant.get('hours_of_operation')
        
        if existing_hours_open and existing_hours_open != 'None' and existing_hours_open != '':
            logger.info(f"  ℹ️  Already has hours_open: {existing_hours_open[:50]}...")
            # If we have hours_open but not hours_of_operation, copy it
            if not existing_hours_of_operation or existing_hours_of_operation == 'None' or existing_hours_of_operation == '':
                logger.info(f"  📝 Copying hours_open to hours_of_operation")
                return self.update_restaurant_hours(restaurant['id'], existing_hours_open, existing_hours_open)
        
        if existing_hours_of_operation and existing_hours_of_operation != 'None' and existing_hours_of_operation != '':
            logger.info(f"  ℹ️  Already has hours_of_operation: {existing_hours_of_operation[:50]}...")
            # If we have hours_of_operation but not hours_open, copy it
            if not existing_hours_open or existing_hours_open == 'None' or existing_hours_open == '':
                logger.info(f"  📝 Copying hours_of_operation to hours_open")
                return self.update_restaurant_hours(restaurant['id'], existing_hours_of_operation, existing_hours_of_operation)
        
        # Try searching Google Places API
        search_query = restaurant['name']
        location = f"{restaurant.get('city', '')} {restaurant.get('state', '')}".strip()
        
        logger.info(f"  🔎 Searching Google Places: {search_query}")
        place_result = self.search_google_places(search_query, location)
        
        if place_result:
            place_id = place_result['place_id']
            logger.info(f"  📍 Found place ID: {place_id}")
            
            # Get detailed information
            place_details = self.get_place_details(place_id)
            
            if place_details and 'opening_hours' in place_details:
                hours_open = self.format_hours_from_places_api(place_details['opening_hours'])
                if hours_open:
                    return self.update_restaurant_hours(restaurant['id'], hours_open)
        
        logger.warning(f"  ❌ No hours found for: {restaurant['name']}")
        return False
    
    def run(self, limit: int = None):
        """Main execution function."""
        logger.info("🚀 Starting PostgreSQL Hours Updater")
        logger.info("=" * 50)
        
        # Check API keys
        if not GOOGLE_PLACES_API_KEY:
            logger.error("GOOGLE_PLACES_API_KEY environment variable not set")
            return
        
        if not DATABASE_URL:
            logger.error("DATABASE_URL environment variable not set")
            return
        
        # Connect to database
        if not self.connect_db():
            return
        
        try:
            # Get restaurants without hours
            restaurants = self.get_restaurants_without_hours()
            logger.info(f"📊 Found {len(restaurants)} restaurants without hours data")
            
            if not restaurants:
                logger.info("✅ All restaurants already have hours data!")
                return
            
            if limit:
                restaurants = restaurants[:limit]
                logger.info(f"Processing first {limit} restaurants")
            
            # Process each restaurant
            success_count = 0
            total_count = len(restaurants)
            
            for i, restaurant in enumerate(restaurants, 1):
                logger.info(f"\n[{i}/{total_count}] Processing restaurant...")
                
                if self.process_restaurant(restaurant):
                    success_count += 1
                
                # Rate limiting - be nice to Google's APIs
                time.sleep(1)
            
            logger.info("\n" + "=" * 50)
            logger.info(f"✅ Completed! Updated {success_count}/{total_count} restaurants")
            logger.info(f"📊 Success rate: {(success_count/total_count*100):.1f}%")
            
        except Exception as e:
            logger.error(f"Error in main execution: {e}")
        
        finally:
            self.conn.close()

def main():
    """Main function with user interaction."""
    print("🕐 PostgreSQL Hours Updater")
    print("=" * 50)
    
    updater = PostgreSQLHoursUpdater()
    
    print("\nOptions:")
    print("1. Process all restaurants missing hours")
    print("2. Process first 10 restaurants (test)")
    print("3. Process first 50 restaurants")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        updater.run()
    elif choice == "2":
        updater.run(limit=10)
    elif choice == "3":
        updater.run(limit=50)
    elif choice == "4":
        print("Exiting...")
    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main() 