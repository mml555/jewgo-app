#!/usr/bin/env python3
"""
Google Places Hours Updater
Fetches missing hours data from Google Places API and Google Knowledge Graph
"""

import sqlite3
import requests
import json
import time
import os
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote_plus

# Configuration
GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
GOOGLE_KNOWLEDGE_GRAPH_API_KEY = os.getenv('GOOGLE_KNOWLEDGE_GRAPH_API_KEY')

class GoogleHoursUpdater:
    def __init__(self, db_path: str = 'restaurants.db'):
        self.db_path = db_path
        self.session = requests.Session()
        
    def get_restaurants_without_hours(self) -> List[Dict]:
        """Get restaurants that don't have hours data or have incomplete hours data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
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
        """)
        
        restaurants = []
        for row in cursor.fetchall():
            restaurants.append({
                'id': row[0],
                'name': row[1],
                'address': row[2],
                'city': row[3],
                'state': row[4],
                'hours_open': row[5],
                'hours_of_operation': row[6],
                'google_places_id': None
            })
        
        conn.close()
        return restaurants
    
    def search_google_places(self, query: str, location: str = None) -> Optional[Dict]:
        """Search for a place using Google Places API Text Search"""
        if not GOOGLE_PLACES_API_KEY:
            print("❌ Google Places API key not found")
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
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                return data['results'][0]  # Return first result
            else:
                print(f"⚠️  No results found for: {search_query}")
                return None
                
        except Exception as e:
            print(f"❌ Error searching Google Places: {e}")
            return None
    
    def get_place_details(self, place_id: str) -> Optional[Dict]:
        """Get detailed information about a place using Google Places API"""
        if not GOOGLE_PLACES_API_KEY:
            print("❌ Google Places API key not found")
            return None
            
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        
        params = {
            'place_id': place_id,
            'key': GOOGLE_PLACES_API_KEY,
            'fields': 'name,formatted_address,opening_hours,formatted_phone_number,website,rating,user_ratings_total,price_level,types'
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK':
                return data['result']
            else:
                print(f"⚠️  Error getting place details: {data['status']}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting place details: {e}")
            return None
    
    def search_google_knowledge_graph(self, query: str) -> Optional[Dict]:
        """Search Google Knowledge Graph for business information"""
        if not GOOGLE_KNOWLEDGE_GRAPH_API_KEY:
            print("❌ Google Knowledge Graph API key not found")
            return None
            
        url = "https://kgsearch.googleapis.com/v1/entities:search"
        
        params = {
            'query': query,
            'key': GOOGLE_KNOWLEDGE_GRAPH_API_KEY,
            'types': 'Restaurant',
            'limit': 1
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('itemListElement'):
                return data['itemListElement'][0]['result']
            else:
                print(f"⚠️  No Knowledge Graph results for: {query}")
                return None
                
        except Exception as e:
            print(f"❌ Error searching Knowledge Graph: {e}")
            return None
    
    def format_hours_from_places_api(self, opening_hours: Dict) -> str:
        """Format opening hours from Google Places API format"""
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
        """Update restaurant hours in the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if hours_of_operation:
            cursor.execute("""
                UPDATE restaurants 
                SET hours_open = ?, hours_of_operation = ?
                WHERE id = ?
            """, (hours_open, hours_of_operation, restaurant_id))
        else:
            cursor.execute("""
                UPDATE restaurants 
                SET hours_open = ?
                WHERE id = ?
            """, (hours_open, restaurant_id))
        
        conn.commit()
        conn.close()
        print(f"✅ Updated hours for restaurant ID {restaurant_id}")
    
    def process_restaurant(self, restaurant: Dict) -> bool:
        """Process a single restaurant to find and update hours"""
        print(f"\n🔍 Processing: {restaurant['name']}")
        
        # Check if we already have some hours data
        existing_hours_open = restaurant.get('hours_open')
        existing_hours_of_operation = restaurant.get('hours_of_operation')
        
        if existing_hours_open and existing_hours_open != 'None' and existing_hours_open != '':
            print(f"  ℹ️  Already has hours_open: {existing_hours_open[:50]}...")
            # If we have hours_open but not hours_of_operation, copy it
            if not existing_hours_of_operation or existing_hours_of_operation == 'None' or existing_hours_of_operation == '':
                print(f"  📝 Copying hours_open to hours_of_operation")
                self.update_restaurant_hours(restaurant['id'], existing_hours_open, existing_hours_open)
                return True
        
        if existing_hours_of_operation and existing_hours_of_operation != 'None' and existing_hours_of_operation != '':
            print(f"  ℹ️  Already has hours_of_operation: {existing_hours_of_operation[:50]}...")
            # If we have hours_of_operation but not hours_open, copy it
            if not existing_hours_open or existing_hours_open == 'None' or existing_hours_open == '':
                print(f"  📝 Copying hours_of_operation to hours_open")
                self.update_restaurant_hours(restaurant['id'], existing_hours_of_operation, existing_hours_of_operation)
                return True
        
        # Try Google Places API first
        if restaurant.get('google_places_id'):
            print(f"  📍 Using existing Google Places ID: {restaurant['google_places_id']}")
            place_details = self.get_place_details(restaurant['google_places_id'])
            
            if place_details and 'opening_hours' in place_details:
                hours_open = self.format_hours_from_places_api(place_details['opening_hours'])
                if hours_open:
                    self.update_restaurant_hours(restaurant['id'], hours_open)
                    return True
        
        # Try searching Google Places API
        search_query = restaurant['name']
        location = f"{restaurant.get('city', '')} {restaurant.get('state', '')}".strip()
        
        print(f"  🔎 Searching Google Places: {search_query}")
        place_result = self.search_google_places(search_query, location)
        
        if place_result:
            place_id = place_result['place_id']
            print(f"  📍 Found place ID: {place_id}")
            
            # Get detailed information
            place_details = self.get_place_details(place_id)
            
            if place_details and 'opening_hours' in place_details:
                hours_open = self.format_hours_from_places_api(place_details['opening_hours'])
                if hours_open:
                    self.update_restaurant_hours(restaurant['id'], hours_open)
                    return True
        
        # Try Google Knowledge Graph as fallback
        print(f"  🔍 Searching Knowledge Graph: {search_query}")
        kg_result = self.search_google_knowledge_graph(search_query)
        
        if kg_result:
            print(f"  📊 Found Knowledge Graph result: {kg_result.get('name', 'Unknown')}")
            # Note: Knowledge Graph doesn't typically provide detailed hours
            # But we could extract other useful information here
        
        print(f"  ❌ No hours found for: {restaurant['name']}")
        return False
    
    def run(self):
        """Main execution function"""
        print("🚀 Starting Google Hours Updater")
        print("=" * 50)
        
        # Check API keys
        if not GOOGLE_PLACES_API_KEY:
            print("❌ GOOGLE_PLACES_API_KEY environment variable not set")
            return
        
        # Get restaurants without hours
        restaurants = self.get_restaurants_without_hours()
        print(f"📊 Found {len(restaurants)} restaurants without hours data")
        
        if not restaurants:
            print("✅ All restaurants already have hours data!")
            return
        
        # Process each restaurant
        success_count = 0
        for i, restaurant in enumerate(restaurants, 1):
            print(f"\n[{i}/{len(restaurants)}] Processing restaurant...")
            
            if self.process_restaurant(restaurant):
                success_count += 1
            
            # Rate limiting - be nice to Google's APIs
            time.sleep(1)
        
        print("\n" + "=" * 50)
        print(f"✅ Completed! Updated {success_count}/{len(restaurants)} restaurants")
        print(f"📊 Success rate: {(success_count/len(restaurants)*100):.1f}%")

if __name__ == "__main__":
    updater = GoogleHoursUpdater()
    updater.run() 