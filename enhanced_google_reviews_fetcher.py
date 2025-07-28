#!/usr/bin/env python3
"""
Enhanced Google Reviews Fetcher
Fetches restaurant reviews and ratings from Google Places API with review text
"""

import requests
import sqlite3
import time
import json
import os
from typing import Dict, Optional, List
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedGoogleReviewsFetcher:
    def __init__(self, api_key: str, db_path: str = "restaurants.db"):
        self.api_key = api_key
        self.db_path = db_path
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        
    def connect_db(self) -> sqlite3.Connection:
        """Connect to the SQLite database"""
        return sqlite3.connect(self.db_path)
    
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
                
                # Get detailed place information including reviews
                place_id = place['place_id']
                detailed_info = self.get_place_details(place_id)
                
                if detailed_info:
                    return {
                        'place_id': place_id,
                        'formatted_address': place.get('formatted_address', ''),
                        'rating': place.get('rating'),
                        'user_ratings_total': place.get('user_ratings_total'),
                        'reviews': detailed_info.get('reviews', []),
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
            'fields': 'reviews,website,formatted_phone_number,opening_hours,rating,user_ratings_total'
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
    
    def update_restaurant_reviews(self, restaurant_id: int, google_data: Dict) -> bool:
        """
        Update restaurant with Google review data
        """
        conn = self.connect_db()
        cursor = conn.cursor()
        
        try:
            # Extract review data
            google_rating = google_data.get('rating', 0)
            google_review_count = google_data.get('user_ratings_total', 0)
            
            # Get reviews (limit to 5 most recent)
            reviews = google_data.get('reviews', [])[:5]
            
            # Store reviews as JSON
            reviews_json = json.dumps(reviews) if reviews else None
            
            # Update database
            cursor.execute("""
                UPDATE restaurants 
                SET google_rating = ?, google_review_count = ?, google_reviews = ?
                WHERE id = ?
            """, (google_rating, google_review_count, reviews_json, restaurant_id))
            
            conn.commit()
            logger.info(f"Updated Google reviews for restaurant ID {restaurant_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating restaurant {restaurant_id}: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def process_restaurants(self, limit: Optional[int] = None) -> Dict[str, int]:
        """
        Process restaurants to fetch Google reviews
        """
        conn = self.connect_db()
        cursor = conn.cursor()
        
        # Get restaurants that don't have Google review data yet
        cursor.execute("""
            SELECT id, name, address, city, state 
            FROM restaurants 
            WHERE (google_reviews IS NULL OR google_reviews = '')
            AND address IS NOT NULL 
            AND address != ''
        """)
        
        restaurants = cursor.fetchall()
        conn.close()
        
        if limit:
            restaurants = restaurants[:limit]
        
        logger.info(f"Found {len(restaurants)} restaurants to update with Google reviews")
        
        updated_count = 0
        not_found_count = 0
        error_count = 0
        
        for i, (restaurant_id, name, address, city, state) in enumerate(restaurants, 1):
            logger.info(f"Processing {i}/{len(restaurants)}: {name}")
            
            try:
                # Search for the place
                google_data = self.search_place_by_address(name, address, city, state)
                
                if google_data:
                    # Update the restaurant
                    if self.update_restaurant_reviews(restaurant_id, google_data):
                        updated_count += 1
                        review_count = len(google_data.get('reviews', []))
                        logger.info(f"✓ Updated {name} with {review_count} Google reviews")
                    else:
                        error_count += 1
                        logger.warning(f"✗ Failed to update {name}")
                else:
                    not_found_count += 1
                    logger.warning(f"✗ Not found: {name}")
                
                # Rate limiting - Google Places API has limits
                time.sleep(0.2)  # 200ms delay between requests
                
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
Enhanced Google Reviews Update Report
====================================

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
    
    # Initialize fetcher
    fetcher = EnhancedGoogleReviewsFetcher(api_key)
    
    # Process all restaurants
    logger.info("Starting enhanced Google reviews update process...")
    results = fetcher.process_restaurants(limit=None)
    
    # Generate and print report
    report = fetcher.generate_report(results)
    print(report)
    
    # Save report to file
    with open('enhanced_google_reviews_report.txt', 'w') as f:
        f.write(report)
    
    logger.info("Report saved to enhanced_google_reviews_report.txt")

if __name__ == "__main__":
    main() 