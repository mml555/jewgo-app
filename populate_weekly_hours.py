#!/usr/bin/env python3
"""
Populate Weekly Hours
Fetches and populates missing weekly hours for restaurants using Google Places API.
"""

import sqlite3
import requests
import time
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WeeklyHoursPopulator:
    def __init__(self, db_path: str = "restaurants.db", api_key: str = None):
        self.db_path = db_path
        self.api_key = api_key or "AIzaSyDHgNdax5xsC0bMFyh0xp11rLWa12N7THE"  # Use the same key as other scripts
        
    def connect_db(self):
        """Connect to the database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False
    
    def get_restaurants_missing_hours(self) -> list:
        """Get restaurants that are missing weekly hours."""
        try:
            self.cursor.execute("""
                SELECT id, name, address, city, state 
                FROM restaurants 
                WHERE (hours_open IS NULL OR hours_open = '') 
                AND status = 'active'
                ORDER BY name
            """)
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Error getting restaurants missing hours: {e}")
            return []
    
    def search_place(self, name: str, address: str) -> Optional[str]:
        """Search for a place using Google Places API."""
        try:
            # Build search query
            query = f"{name} {address}".strip()
            
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            params = {
                'query': query,
                'key': self.api_key,
                'type': 'restaurant'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == 'OK' and data.get('results'):
                return data['results'][0].get('place_id')
            
            return None
            
        except Exception as e:
            logger.error(f"Error searching place for {name}: {e}")
            return None
    
    def get_place_details(self, place_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a place."""
        try:
            url = "https://maps.googleapis.com/maps/api/place/details/json"
            params = {
                'place_id': place_id,
                'fields': 'opening_hours',
                'key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == 'OK':
                return data.get('result', {})
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting place details: {e}")
            return None
    
    def format_weekly_hours(self, opening_hours: Dict[str, Any]) -> str:
        """Format opening hours for database storage."""
        try:
            if not opening_hours:
                return None
            
            weekday_text = opening_hours.get('weekday_text', [])
            
            if not weekday_text:
                return None
            
            # Format as "Sun-Thu 11am-10pm, Fri 11am-3pm" style
            formatted_hours = []
            
            for day_info in weekday_text:
                # Extract day and hours
                if ':' in day_info:
                    day_part, hours_part = day_info.split(':', 1)
                    day = day_part.strip()
                    hours = hours_part.strip()
                    
                    # Convert to abbreviated format
                    day_abbrev = self.convert_day_to_abbrev(day)
                    formatted_hours.append(f"{day_abbrev} {hours}")
            
            return ', '.join(formatted_hours)
            
        except Exception as e:
            logger.error(f"Error formatting hours: {e}")
            return None
    
    def convert_day_to_abbrev(self, day: str) -> str:
        """Convert full day name to abbreviation."""
        day_mapping = {
            'Monday': 'Mon',
            'Tuesday': 'Tue', 
            'Wednesday': 'Wed',
            'Thursday': 'Thu',
            'Friday': 'Fri',
            'Saturday': 'Sat',
            'Sunday': 'Sun'
        }
        return day_mapping.get(day, day)
    
    def update_restaurant_hours(self, restaurant_id: int, hours_open: str) -> bool:
        """Update restaurant with weekly hours."""
        try:
            self.cursor.execute("""
                UPDATE restaurants 
                SET hours_open = ?, updated_date = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (hours_open, restaurant_id))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error updating restaurant {restaurant_id}: {e}")
            return False
    
    def process_restaurant(self, restaurant_id: int, name: str, address: str, city: str, state: str) -> bool:
        """Process a single restaurant to get weekly hours."""
        try:
            logger.info(f"Processing: {name}")
            
            # Build full address
            full_address = f"{address}, {city}, {state}".strip()
            
            # Search for the place
            place_id = self.search_place(name, full_address)
            
            if not place_id:
                logger.warning(f"No place found for {name}")
                return False
            
            # Get place details
            place_details = self.get_place_details(place_id)
            
            if not place_details:
                logger.warning(f"No details found for {name}")
                return False
            
            # Format hours
            opening_hours = place_details.get('opening_hours', {})
            formatted_hours = self.format_weekly_hours(opening_hours)
            
            if not formatted_hours:
                logger.warning(f"No hours found for {name}")
                return False
            
            # Update database
            success = self.update_restaurant_hours(restaurant_id, formatted_hours)
            
            if success:
                logger.info(f"✅ Updated {name}: {formatted_hours}")
            else:
                logger.error(f"❌ Failed to update {name}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error processing {name}: {e}")
            return False
    
    def run(self, limit: int = None):
        """Main execution function."""
        if not self.connect_db():
            return
        
        try:
            # Get restaurants missing hours
            restaurants = self.get_restaurants_missing_hours()
            
            if not restaurants:
                logger.info("No restaurants missing weekly hours!")
                return
            
            logger.info(f"Found {len(restaurants)} restaurants missing weekly hours")
            
            if limit:
                restaurants = restaurants[:limit]
                logger.info(f"Processing first {limit} restaurants")
            
            # Process restaurants
            success_count = 0
            total_count = len(restaurants)
            
            for i, (restaurant_id, name, address, city, state) in enumerate(restaurants, 1):
                logger.info(f"Progress: {i}/{total_count}")
                
                success = self.process_restaurant(restaurant_id, name, address, city, state)
                if success:
                    success_count += 1
                
                # Rate limiting - wait between requests
                time.sleep(1)
            
            logger.info(f"✅ Completed! Updated {success_count}/{total_count} restaurants")
            
        except Exception as e:
            logger.error(f"Error in main execution: {e}")
        
        finally:
            self.conn.close()

def main():
    """Main function with user interaction."""
    print("🕐 Weekly Hours Populator")
    print("=" * 50)
    
    populator = WeeklyHoursPopulator()
    
    print("\nOptions:")
    print("1. Process all restaurants missing hours")
    print("2. Process first 10 restaurants (test)")
    print("3. Process first 50 restaurants")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        populator.run()
    elif choice == "2":
        populator.run(limit=10)
    elif choice == "3":
        populator.run(limit=50)
    elif choice == "4":
        print("Exiting...")
    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main() 