#!/usr/bin/env python3
"""
Enhanced Google Places Website Updater
=====================================

Fetches website links from Google Places API and updates restaurant database.
This is a backup system to automatically find website links when they're missing.

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

class EnhancedGooglePlacesWebsiteUpdater:
    """Enhanced website updater using Google Places API with current database structure."""
    
    def __init__(self, api_key: str, database_url: str = None):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        
        # Use provided database URL or get from environment
        self.database_url = database_url or "postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
        
        logger.info("Enhanced Google Places Website Updater initialized", api_key_length=len(api_key))
    
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
        Get detailed information about a place including website.
        """
        try:
            url = f"{self.base_url}/details/json"
            params = {
                'place_id': place_id,
                'fields': 'website,url,name,formatted_address,formatted_phone_number',
                'key': self.api_key
            }
            
            logger.info(f"Getting place details for place_id: {place_id}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'OK':
                result = data['result']
                logger.info(f"Retrieved place details", name=result.get('name'), has_website=bool(result.get('website')))
                return result
            else:
                logger.warning(f"Error getting place details", status=data.get('status'))
                return None
                
        except Exception as e:
            logger.error(f"Error getting place details", error=str(e))
            return None
    
    def validate_website_url(self, url: str) -> bool:
        """
        Validate if a website URL is accessible and properly formatted.
        """
        try:
            # Basic URL validation
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Test if website is accessible (with shorter timeout for efficiency)
            response = requests.head(url, timeout=3, allow_redirects=True)
            is_valid = response.status_code == 200
            logger.debug(f"Website validation", url=url, status_code=response.status_code, is_valid=is_valid)
            return is_valid
            
        except Exception as e:
            logger.debug(f"Website validation failed", url=url, error=str(e))
            return False
    
    def update_restaurant_website(self, restaurant_id: int, website_url: str) -> bool:
        """
        Update restaurant website URL in the database.
        """
        try:
            engine = create_engine(self.database_url)
            
            with engine.begin() as conn:
                # Update the website field
                result = conn.execute(text("""
                    UPDATE restaurants 
                    SET website = :website_url, updated_at = NOW()
                    WHERE id = :restaurant_id
                """), {"website_url": website_url, "restaurant_id": restaurant_id})
                
                if result.rowcount > 0:
                    logger.info(f"Updated website for restaurant ID {restaurant_id}", website=website_url)
                    return True
                else:
                    logger.warning(f"No restaurant found with ID {restaurant_id}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error updating restaurant website", restaurant_id=restaurant_id, error=str(e))
            return False
    
    def process_restaurant(self, restaurant: Dict[str, Any]) -> bool:
        """
        Process a single restaurant to update its website link.
        """
        try:
            restaurant_id = restaurant.get('id')
            restaurant_name = restaurant.get('name', '')
            address = restaurant.get('address', '')
            current_website = restaurant.get('website', '')
            
            if not restaurant_name or not address:
                logger.warning(f"Skipping restaurant {restaurant_id}: missing name or address")
                return False
            
            # Check if website already exists and is substantial
            if current_website and len(current_website) > 10:
                logger.info(f"Restaurant {restaurant_name} already has a website, skipping", website=current_website)
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
            
            # Get website
            website_url = place_details.get('website', '')
            if not website_url:
                logger.warning(f"No website found for {restaurant_name}")
                return False
            
            # Validate website
            if not self.validate_website_url(website_url):
                logger.warning(f"Invalid website URL for {restaurant_name}", website=website_url)
                return False
            
            # Update database
            success = self.update_restaurant_website(restaurant_id, website_url)
            
            # Add delay to respect API rate limits
            time.sleep(0.2)  # 200ms delay between requests
            
            return success
            
        except Exception as e:
            logger.error(f"Error processing restaurant {restaurant.get('name', 'Unknown')}", error=str(e))
            return False
    
    def get_restaurants_without_websites(self, limit: int = None) -> List[Dict[str, Any]]:
        """
        Get restaurants that don't have website links.
        """
        try:
            engine = create_engine(self.database_url)
            
            with engine.connect() as conn:
                query = """
                    SELECT id, name, address, city, state, website
                    FROM restaurants 
                    WHERE website IS NULL OR website = '' OR website = ' '
                    ORDER BY name
                """
                
                if limit:
                    query += f" LIMIT {limit}"
                
                result = conn.execute(text(query))
                restaurants = [dict(row._mapping) for row in result.fetchall()]
                
                logger.info(f"Found {len(restaurants)} restaurants without websites")
                return restaurants
                
        except Exception as e:
            logger.error(f"Error getting restaurants without websites", error=str(e))
            return []
    
    def update_restaurants_without_websites(self, limit: int = None) -> Dict[str, int]:
        """
        Update website links for restaurants that don't have them.
        """
        try:
            # Get restaurants without websites
            restaurants = self.get_restaurants_without_websites(limit)
            
            if not restaurants:
                logger.info("No restaurants found without websites")
                return {'success': 0, 'failed': 0, 'skipped': 0, 'total': 0}
            
            logger.info(f"Processing {len(restaurants)} restaurants without websites")
            
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
            
            logger.info(f"Update complete", 
                       success=success_count, failed=failed_count, 
                       skipped=skipped_count, total=len(restaurants))
            
            return {
                'success': success_count,
                'failed': failed_count,
                'skipped': skipped_count,
                'total': len(restaurants)
            }
            
        except Exception as e:
            logger.error(f"Error updating restaurants without websites", error=str(e))
            return {'success': 0, 'failed': 0, 'skipped': 0, 'total': 0}
    
    def update_specific_restaurant(self, restaurant_id: int) -> bool:
        """
        Update website link for a specific restaurant by ID.
        """
        try:
            engine = create_engine(self.database_url)
            
            with engine.connect() as conn:
                # Get restaurant details
                result = conn.execute(text("""
                    SELECT id, name, address, city, state, website
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
    """Main function to run the website updater."""
    
    # Get API key from environment variable
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not api_key:
        logger.error("GOOGLE_PLACES_API_KEY environment variable not set")
        print("Please set your Google Places API key:")
        print("export GOOGLE_PLACES_API_KEY='your_api_key_here'")
        return
    
    # Create updater instance
    updater = EnhancedGooglePlacesWebsiteUpdater(api_key)
    
    # Ask user what to do
    print("Enhanced Google Places Website Updater")
    print("1. Update restaurants without websites (all)")
    print("2. Update restaurants without websites (limit)")
    print("3. Update specific restaurant by ID")
    print("4. Test with first 3 restaurants")
    
    choice = input("Enter your choice (1-4): ").strip()
    
    if choice == '1':
        results = updater.update_restaurants_without_websites()
        print(f"Results: {results}")
        
    elif choice == '2':
        limit = input("Enter limit: ").strip()
        limit = int(limit) if limit else 10
        results = updater.update_restaurants_without_websites(limit)
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
        results = updater.update_restaurants_without_websites(limit=3)
        print(f"Test results: {results}")
        
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main() 