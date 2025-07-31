#!/usr/bin/env python3
"""
Google Places Description Updater
Fetches descriptions and details from Google Places API and updates restaurant database.
"""

import os
import requests
import time
import json
from typing import Dict, List, Optional, Any
from database_manager import DatabaseManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GooglePlacesDescriptionUpdater:
    """Updates restaurant descriptions using Google Places API."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        self.db_manager = DatabaseManager()
        
    def connect_db(self) -> bool:
        """Connect to the database."""
        return self.db_manager.connect()
    
    def disconnect_db(self):
        """Disconnect from the database."""
        self.db_manager.disconnect()
    
    def search_place(self, restaurant_name: str, address: str) -> Optional[str]:
        """
        Search for a place using Google Places API.
        Returns the place_id if found.
        """
        try:
            # Build search query
            query = f"{restaurant_name} {address}"
            
            # Make Places API request
            url = f"{self.base_url}/textsearch/json"
            params = {
                'query': query,
                'key': self.api_key,
                'type': 'restaurant'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                # Return the first result's place_id
                return data['results'][0]['place_id']
            else:
                logger.warning(f"No place found for: {query}")
                return None
                
        except Exception as e:
            logger.error(f"Error searching place for {restaurant_name}: {e}")
            return None
    
    def get_place_details(self, place_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a place including description.
        """
        try:
            url = f"{self.base_url}/details/json"
            params = {
                'place_id': place_id,
                'fields': 'editorial_summary,reviews,rating,price_level,formatted_address,formatted_phone_number,website,opening_hours,types',
                'key': self.api_key
            }
            
            response = requests.get(url, params=params)
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
    
    def generate_description(self, place_details: Dict[str, Any], restaurant_name: str) -> str:
        """
        Generate a short description from Google Places data.
        """
        try:
            description_parts = []
            
            # Add editorial summary if available
            if 'editorial_summary' in place_details and place_details['editorial_summary'].get('overview'):
                overview = place_details['editorial_summary']['overview']
                # Truncate if too long
                if len(overview) > 200:
                    overview = overview[:197] + "..."
                description_parts.append(overview)
            
            # Add rating if available
            if 'rating' in place_details:
                rating = place_details['rating']
                description_parts.append(f"Rated {rating}/5 stars on Google.")
            
            # Add price level if available
            if 'price_level' in place_details:
                price_level = place_details['price_level']
                price_text = {1: "Budget-friendly", 2: "Moderate", 3: "Expensive", 4: "Very expensive"}.get(price_level, "")
                if price_text:
                    description_parts.append(f"{price_text} pricing.")
            
            # Add types/categories if available
            if 'types' in place_details:
                types = place_details['types']
                # Filter out generic types and get meaningful ones
                meaningful_types = [t for t in types if t not in ['establishment', 'food', 'point_of_interest']]
                if meaningful_types:
                    # Take first 2-3 meaningful types
                    type_display = ", ".join(meaningful_types[:3]).replace("_", " ").title()
                    description_parts.append(f"Specializes in {type_display}.")
            
            # If no description parts, create a basic one
            if not description_parts:
                description_parts.append(f"Kosher {restaurant_name.lower()} establishment.")
            
            # Combine all parts
            description = " ".join(description_parts)
            
            # Ensure it's not too long
            if len(description) > 300:
                description = description[:297] + "..."
            
            return description
            
        except Exception as e:
            logger.error(f"Error generating description: {e}")
            return f"Kosher {restaurant_name.lower()} establishment."
    
    def update_restaurant_description(self, business_id: str, description: str) -> bool:
        """
        Update restaurant description in the database.
        """
        try:
            updates = {
                'short_description': description
            }
            
            success = self.db_manager.update_restaurant(business_id, updates)
            if success:
                logger.info(f"Updated description for restaurant {business_id}")
            else:
                logger.warning(f"Failed to update description for restaurant {business_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error updating restaurant description: {e}")
            return False
    
    def process_restaurant(self, restaurant: Dict[str, Any]) -> bool:
        """
        Process a single restaurant to update its description.
        """
        try:
            restaurant_name = restaurant.get('name', '')
            address = restaurant.get('address', '')
            business_id = restaurant.get('business_id', '')
            
            if not restaurant_name or not address:
                logger.warning(f"Skipping restaurant {business_id}: missing name or address")
                return False
            
            # Check if description already exists and is substantial
            current_description = restaurant.get('short_description', '')
            if current_description and len(current_description) > 50:
                logger.info(f"Restaurant {restaurant_name} already has a substantial description, skipping")
                return True
            
            logger.info(f"Processing restaurant: {restaurant_name}")
            
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
            
            # Generate description
            description = self.generate_description(place_details, restaurant_name)
            
            # Update database
            success = self.update_restaurant_description(business_id, description)
            
            # Add delay to respect API rate limits
            time.sleep(0.1)  # 100ms delay between requests
            
            return success
            
        except Exception as e:
            logger.error(f"Error processing restaurant {restaurant.get('name', 'Unknown')}: {e}")
            return False
    
    def update_all_restaurants(self, limit: int = None) -> Dict[str, int]:
        """
        Update descriptions for all restaurants in the database.
        """
        try:
            if not self.connect_db():
                logger.error("Failed to connect to database")
                return {'success': 0, 'failed': 0, 'skipped': 0}
            
            # Get all restaurants
            restaurants = self.db_manager.search_restaurants(limit=limit or 1000)
            
            logger.info(f"Found {len(restaurants)} restaurants to process")
            
            success_count = 0
            failed_count = 0
            skipped_count = 0
            
            for i, restaurant in enumerate(restaurants, 1):
                logger.info(f"Processing {i}/{len(restaurants)}: {restaurant.get('name', 'Unknown')}")
                
                if self.process_restaurant(restaurant):
                    success_count += 1
                else:
                    failed_count += 1
                
                # Progress update every 10 restaurants
                if i % 10 == 0:
                    logger.info(f"Progress: {i}/{len(restaurants)} completed")
            
            logger.info(f"Update complete. Success: {success_count}, Failed: {failed_count}, Skipped: {skipped_count}")
            
            return {
                'success': success_count,
                'failed': failed_count,
                'skipped': skipped_count,
                'total': len(restaurants)
            }
            
        except Exception as e:
            logger.error(f"Error updating all restaurants: {e}")
            return {'success': 0, 'failed': 0, 'skipped': 0}
        
        finally:
            self.disconnect_db()
    
    def update_specific_restaurant(self, business_id: str) -> bool:
        """
        Update description for a specific restaurant by business_id.
        """
        try:
            if not self.connect_db():
                logger.error("Failed to connect to database")
                return False
            
            restaurant = self.db_manager.get_restaurant(business_id)
            if not restaurant:
                logger.error(f"Restaurant with business_id {business_id} not found")
                return False
            
            return self.process_restaurant(restaurant)
            
        except Exception as e:
            logger.error(f"Error updating specific restaurant: {e}")
            return False
        
        finally:
            self.disconnect_db()

def main():
    """Main function to run the description updater."""
    
    # Get API key from environment variable
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not api_key:
        logger.error("GOOGLE_PLACES_API_KEY environment variable not set")
        print("Please set your Google Places API key:")
        print("export GOOGLE_PLACES_API_KEY='your_api_key_here'")
        return
    
    # Create updater instance
    updater = GooglePlacesDescriptionUpdater(api_key)
    
    # Ask user what to do
    print("Google Places Description Updater")
    print("1. Update all restaurants")
    print("2. Update specific restaurant")
    print("3. Test with first 5 restaurants")
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == '1':
        limit = input("Enter limit (or press Enter for all): ").strip()
        limit = int(limit) if limit else None
        results = updater.update_all_restaurants(limit)
        print(f"Results: {results}")
        
    elif choice == '2':
        business_id = input("Enter business_id: ").strip()
        success = updater.update_specific_restaurant(business_id)
        print(f"Update {'successful' if success else 'failed'}")
        
    elif choice == '3':
        results = updater.update_all_restaurants(limit=5)
        print(f"Test results: {results}")
        
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main() 