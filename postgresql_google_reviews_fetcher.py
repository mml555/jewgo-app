#!/usr/bin/env python3
"""
PostgreSQL Google Reviews Fetcher
Fetches restaurant reviews and ratings from Google Places API for PostgreSQL database
"""

import requests
import psycopg2
import time
import json
import os
from typing import Dict, Optional, List
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PostgreSQLGoogleReviewsFetcher:
    def __init__(self, api_key: str, database_url: str):
        self.api_key = api_key
        self.database_url = database_url
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        
    def connect_db(self) -> psycopg2.extensions.connection:
        """Connect to the PostgreSQL database"""
        return psycopg2.connect(self.database_url)
    
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
        Update restaurant with Google reviews data
        """
        conn = None
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            
            # Extract data
            google_rating = google_data.get('rating', 0)
            google_review_count = google_data.get('user_ratings_total', 0)
            reviews = google_data.get('reviews', [])
            
            # Convert reviews to JSON string
            reviews_json = json.dumps(reviews) if reviews else None
            
            # Update the restaurant
            cursor.execute("""
                UPDATE restaurants 
                SET google_rating = %s, google_review_count = %s, google_reviews = %s
                WHERE id = %s
            """, (google_rating, google_review_count, reviews_json, restaurant_id))
            
            conn.commit()
            logger.info(f"Updated restaurant {restaurant_id} with Google reviews data")
            return True
            
        except Exception as e:
            logger.error(f"Error updating restaurant {restaurant_id}: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()
    
    def get_restaurants_without_google_reviews(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get restaurants that don't have Google reviews data
        """
        conn = None
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            
            query = """
                SELECT id, name, address, city, state
                FROM restaurants 
                WHERE (google_reviews IS NULL OR google_reviews = '')
                AND address IS NOT NULL 
                AND city IS NOT NULL 
                AND state IS NOT NULL
                ORDER BY id
            """
            
            if limit:
                query += f" LIMIT {limit}"
            
            cursor.execute(query)
            restaurants = []
            for row in cursor.fetchall():
                restaurants.append({
                    'id': row[0],
                    'name': row[1],
                    'address': row[2],
                    'city': row[3],
                    'state': row[4]
                })
            
            return restaurants
            
        except Exception as e:
            logger.error(f"Error getting restaurants without Google reviews: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def process_restaurants(self, limit: Optional[int] = None) -> Dict[str, int]:
        """
        Process restaurants to fetch Google reviews
        """
        restaurants = self.get_restaurants_without_google_reviews(limit)
        
        results = {
            'total': len(restaurants),
            'success': 0,
            'failed': 0,
            'no_data': 0
        }
        
        logger.info(f"Processing {len(restaurants)} restaurants for Google reviews")
        
        for i, restaurant in enumerate(restaurants, 1):
            logger.info(f"Processing {i}/{len(restaurants)}: {restaurant['name']}")
            
            try:
                # Search for the restaurant on Google
                google_data = self.search_place_by_address(
                    restaurant['name'],
                    restaurant['address'],
                    restaurant['city'],
                    restaurant['state']
                )
                
                if google_data and google_data.get('reviews'):
                    # Update restaurant with Google data
                    if self.update_restaurant_reviews(restaurant['id'], google_data):
                        results['success'] += 1
                        logger.info(f"✅ Updated {restaurant['name']} with {len(google_data['reviews'])} reviews")
                    else:
                        results['failed'] += 1
                        logger.error(f"❌ Failed to update {restaurant['name']}")
                else:
                    results['no_data'] += 1
                    logger.warning(f"⚠️ No Google data found for {restaurant['name']}")
                
                # Rate limiting - wait between requests
                time.sleep(1)
                
            except Exception as e:
                results['failed'] += 1
                logger.error(f"Error processing {restaurant['name']}: {e}")
                time.sleep(1)
        
        return results
    
    def generate_report(self, results: Dict[str, int]) -> str:
        """
        Generate a report of the processing results
        """
        success_rate = (results['success'] / results['total'] * 100) if results['total'] > 0 else 0
        report = f"""
Google Reviews Fetch Report
==========================

Total restaurants processed: {results['total']}
Successfully updated: {results['success']}
Failed to update: {results['failed']}
No Google data found: {results['no_data']}

Success rate: {success_rate:.1f}%
        """
        return report

def main():
    # Get API key from environment variable
    api_key = os.environ.get('GOOGLE_PLACES_API_KEY')
    database_url = os.environ.get('DATABASE_URL')
    
    if not api_key:
        logger.error("GOOGLE_PLACES_API_KEY environment variable not found")
        return
    
    if not database_url:
        logger.error("DATABASE_URL environment variable not found")
        return
    
    # Create fetcher instance
    fetcher = PostgreSQLGoogleReviewsFetcher(api_key, database_url)
    
    # Process restaurants (limit to 50 for testing)
    results = fetcher.process_restaurants(limit=50)
    
    # Generate and save report
    report = fetcher.generate_report(results)
    logger.info(report)
    
    # Save report to file
    with open('postgresql_google_reviews_report.txt', 'w') as f:
        f.write(report)
    
    logger.info("Report saved to postgresql_google_reviews_report.txt")

if __name__ == "__main__":
    main() 