#!/usr/bin/env python3
"""
Google Places Address Updater
Uses Google Places API to verify and update missing zip codes and address information
"""

import sqlite3
import requests
import time
import json
import os
from typing import Dict, Optional, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GooglePlacesAddressUpdater:
    def __init__(self, api_key: str, db_path: str = "restaurants.db"):
        self.api_key = api_key
        self.db_path = db_path
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        
    def connect_db(self) -> sqlite3.Connection:
        """Connect to the SQLite database"""
        return sqlite3.connect(self.db_path)
    
    def get_restaurants_with_missing_zip(self) -> list:
        """Get restaurants that have empty zip codes"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, address, city, state, zip_code 
            FROM restaurants 
            WHERE (zip_code IS NULL OR zip_code = '' OR zip_code = 'NULL')
            AND address IS NOT NULL 
            AND address != ''
        """)
        
        restaurants = cursor.fetchall()
        conn.close()
        
        return restaurants
    
    def search_place_by_address(self, name: str, address: str, city: str, state: str) -> Optional[Dict]:
        """
        Search for a place using Google Places API
        """
        # Build search query
        search_query = f"{name}, {address}, {city}, {state}"
        
        # Text Search API endpoint
        url = f"{self.base_url}/textsearch/json"
        params = {
            'query': search_query,
            'key': self.api_key,
            'type': 'restaurant'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                # Get the first result
                place = data['results'][0]
                
                # Get detailed place information
                place_id = place['place_id']
                detailed_info = self.get_place_details(place_id)
                
                if detailed_info:
                    return {
                        'place_id': place_id,
                        'formatted_address': place.get('formatted_address', ''),
                        'address_components': detailed_info.get('address_components', []),
                        'geometry': place.get('geometry', {}),
                        'rating': place.get('rating'),
                        'user_ratings_total': place.get('user_ratings_total'),
                        'website': detailed_info.get('website', ''),
                        'formatted_phone_number': detailed_info.get('formatted_phone_number', ''),
                        'opening_hours': detailed_info.get('opening_hours', {})
                    }
            
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching for place {name}: {e}")
            return None
    
    def get_place_details(self, place_id: str) -> Optional[Dict]:
        """
        Get detailed information about a place using Place Details API
        """
        url = f"{self.base_url}/details/json"
        params = {
            'place_id': place_id,
            'key': self.api_key,
            'fields': 'address_components,website,formatted_phone_number,opening_hours'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK':
                return data['result']
            
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting place details for {place_id}: {e}")
            return None
    
    def extract_address_components(self, address_components: list) -> Dict[str, str]:
        """
        Extract address components from Google Places API response
        """
        components = {}
        
        for component in address_components:
            types = component.get('types', [])
            
            if 'street_number' in types:
                components['street_number'] = component.get('long_name', '')
            elif 'route' in types:
                components['route'] = component.get('long_name', '')
            elif 'locality' in types:
                components['city'] = component.get('long_name', '')
            elif 'administrative_area_level_1' in types:
                components['state'] = component.get('short_name', '')
            elif 'postal_code' in types:
                components['zip_code'] = component.get('long_name', '')
            elif 'country' in types:
                components['country'] = component.get('short_name', '')
        
        return components
    
    def update_restaurant_address(self, restaurant_id: int, address_data: Dict) -> bool:
        """
        Update restaurant address information in the database
        """
        conn = self.connect_db()
        cursor = conn.cursor()
        
        try:
            # Extract address components
            address_components = self.extract_address_components(address_data.get('address_components', []))
            
            # Build update query
            updates = []
            params = []
            
            # Update zip code if found
            if 'zip_code' in address_components:
                updates.append("zip_code = ?")
                params.append(address_components['zip_code'])
            
            # Update address if we have better formatted address
            if address_data.get('formatted_address'):
                updates.append("address = ?")
                params.append(address_data['formatted_address'])
            
            # Update city if found and different
            if 'city' in address_components:
                updates.append("city = ?")
                params.append(address_components['city'])
            
            # Update state if found and different
            if 'state' in address_components:
                updates.append("state = ?")
                params.append(address_components['state'])
            
            # Update rating if available
            if address_data.get('rating'):
                updates.append("rating = ?")
                params.append(address_data['rating'])
            
            # Update review count if available
            if address_data.get('user_ratings_total'):
                updates.append("review_count = ?")
                params.append(address_data['user_ratings_total'])
            
            # Update website if available
            if address_data.get('website'):
                updates.append("website = ?")
                params.append(address_data['website'])
            
            # Update phone number if available
            if address_data.get('formatted_phone_number'):
                updates.append("phone_number = ?")
                params.append(address_data['formatted_phone_number'])
            
            if updates:
                params.append(restaurant_id)
                query = f"UPDATE restaurants SET {', '.join(updates)} WHERE id = ?"
                cursor.execute(query, params)
                conn.commit()
                logger.info(f"Updated restaurant ID {restaurant_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error updating restaurant {restaurant_id}: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def process_restaurants(self, limit: Optional[int] = None) -> Dict[str, int]:
        """
        Process restaurants with missing zip codes
        """
        restaurants = self.get_restaurants_with_missing_zip()
        
        if limit:
            restaurants = restaurants[:limit]
        
        logger.info(f"Found {len(restaurants)} restaurants with missing zip codes")
        
        updated_count = 0
        not_found_count = 0
        error_count = 0
        
        for i, (restaurant_id, name, address, city, state, zip_code) in enumerate(restaurants, 1):
            logger.info(f"Processing {i}/{len(restaurants)}: {name}")
            
            try:
                # Search for the place
                place_data = self.search_place_by_address(name, address, city, state)
                
                if place_data:
                    # Update the restaurant
                    if self.update_restaurant_address(restaurant_id, place_data):
                        updated_count += 1
                        logger.info(f"✓ Updated {name}")
                    else:
                        error_count += 1
                        logger.warning(f"✗ Failed to update {name}")
                else:
                    not_found_count += 1
                    logger.warning(f"✗ Not found: {name}")
                
                # Rate limiting - Google Places API has limits
                time.sleep(0.1)  # 100ms delay between requests
                
            except Exception as e:
                error_count += 1
                logger.error(f"Error processing {name}: {e}")
                time.sleep(1)  # Longer delay on error
        
        return {
            'total_processed': len(restaurants),
            'updated': updated_count,
            'not_found': not_found_count,
            'errors': error_count
        }
    
    def generate_report(self, results: Dict[str, int]) -> str:
        """
        Generate a summary report
        """
        success_rate = (results['updated'] / results['total_processed'] * 100) if results['total_processed'] > 0 else 0
        report = f"""
Google Places Address Update Report
==================================

Total restaurants processed: {results['total_processed']}
Successfully updated: {results['updated']}
Not found: {results['not_found']}
Errors: {results['errors']}

Success rate: {success_rate:.1f}%
        """
        return report

def main():
    # Get API key from environment variable
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    
    if not api_key:
        logger.error("Please set GOOGLE_PLACES_API_KEY environment variable")
        return
    
    # Initialize updater
    updater = GooglePlacesAddressUpdater(api_key)
    
    # Process restaurants (limit to 10 for testing)
    logger.info("Starting address update process...")
    results = updater.process_restaurants(limit=10)
    
    # Generate and print report
    report = updater.generate_report(results)
    print(report)
    
    # Save report to file
    with open('address_update_report.txt', 'w') as f:
        f.write(report)
    
    logger.info("Report saved to address_update_report.txt")

if __name__ == "__main__":
    main() 