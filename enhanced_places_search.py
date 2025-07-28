#!/usr/bin/env python3
"""
Enhanced Google Places Search
Tries multiple search strategies to find restaurants that failed with the original approach.
"""

import sqlite3
import requests
import time
import logging
from typing import Dict, Any, Optional, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedPlacesSearch:
    def __init__(self, db_path: str = "restaurants.db", api_key: str = None):
        self.db_path = db_path
        self.api_key = api_key or "AIzaSyDHgNdax5xsC0bMFyh0xp11rLWa12N7THE"
        
    def connect_db(self):
        """Connect to the database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False
    
    def get_failed_restaurants(self) -> List[tuple]:
        """Get restaurants that failed to get hours or other data."""
        try:
            self.cursor.execute("""
                SELECT id, name, address, city, state, listing_type, kosher_category
                FROM restaurants 
                WHERE (hours_open IS NULL OR hours_open = '') 
                AND status = 'active'
                ORDER BY name
            """)
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Error getting failed restaurants: {e}")
            return []
    
    def search_place_enhanced(self, name: str, address: str, city: str, state: str) -> Optional[str]:
        """Enhanced search that tries multiple strategies."""
        
        # Strategy 1: Name + Full Address (original approach)
        query1 = f"{name} {address}, {city}, {state}".strip()
        place_id = self._search_place_single(query1)
        if place_id:
            logger.info(f"✅ Found with Strategy 1: {name}")
            return place_id
        
        # Strategy 2: Name + City, State (without street address)
        query2 = f"{name} {city}, {state}".strip()
        place_id = self._search_place_single(query2)
        if place_id:
            logger.info(f"✅ Found with Strategy 2: {name}")
            return place_id
        
        # Strategy 3: Name only
        query3 = name.strip()
        place_id = self._search_place_single(query3)
        if place_id:
            logger.info(f"✅ Found with Strategy 3: {name}")
            return place_id
        
        # Strategy 4: Address only (without name)
        query4 = f"{address}, {city}, {state}".strip()
        place_id = self._search_place_single(query4)
        if place_id:
            logger.info(f"✅ Found with Strategy 4: {name}")
            return place_id
        
        # Strategy 5: City + Restaurant type (if we have listing_type)
        # This would be implemented if we had listing_type data
        
        logger.warning(f"❌ All strategies failed for: {name}")
        return None
    
    def _search_place_single(self, query: str) -> Optional[str]:
        """Single search attempt with a specific query."""
        try:
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
            logger.error(f"Error in single search for '{query}': {e}")
            return None
    
    def get_place_details(self, place_id: str, fields: str = "opening_hours,formatted_address,name") -> Optional[Dict[str, Any]]:
        """Get detailed information about a place."""
        try:
            url = "https://maps.googleapis.com/maps/api/place/details/json"
            params = {
                'place_id': place_id,
                'fields': fields,
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
    
    def process_restaurant(self, restaurant_id: int, name: str, address: str, city: str, state: str, listing_type: str, kosher_category: str) -> bool:
        """Process a single restaurant with enhanced search."""
        try:
            logger.info(f"Processing: {name}")
            
            # Try enhanced search
            place_id = self.search_place_enhanced(name, address, city, state)
            
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
            # Get restaurants that failed
            restaurants = self.get_failed_restaurants()
            
            if not restaurants:
                logger.info("No restaurants to retry!")
                return
            
            logger.info(f"Found {len(restaurants)} restaurants to retry with enhanced search")
            
            if limit:
                restaurants = restaurants[:limit]
                logger.info(f"Processing first {limit} restaurants")
            
            # Process restaurants
            success_count = 0
            total_count = len(restaurants)
            
            for i, (restaurant_id, name, address, city, state, listing_type, kosher_category) in enumerate(restaurants, 1):
                logger.info(f"Progress: {i}/{total_count}")
                
                success = self.process_restaurant(restaurant_id, name, address, city, state, listing_type, kosher_category)
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
    print("🔍 Enhanced Google Places Search")
    print("=" * 50)
    
    searcher = EnhancedPlacesSearch()
    
    print("\nOptions:")
    print("1. Retry all failed restaurants")
    print("2. Retry first 5 restaurants (test)")
    print("3. Retry first 20 restaurants")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        searcher.run()
    elif choice == "2":
        searcher.run(limit=5)
    elif choice == "3":
        searcher.run(limit=20)
    elif choice == "4":
        print("Exiting...")
    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main() 