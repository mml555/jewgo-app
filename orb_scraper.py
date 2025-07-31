#!/usr/bin/env python3
"""
ORB Kosher Website Scraper
Scrapes restaurant information from ORB Kosher website and populates the database.
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin, urlparse
import logging
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database_manager_v3 import DatabaseManager

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ORBScraper:
    def __init__(self):
        self.base_url = "https://www.orbkosher.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.db_manager = DatabaseManager()
        
    def get_restaurant_categories(self):
        """Get all restaurant categories from ORB website."""
        try:
            url = f"{self.base_url}/category/restaurants/"
            logger.info(f"Fetching restaurant categories from: {url}")
            
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find category links - ORB typically has dairy, meat, pareve categories
            categories = []
            
            # Look for category navigation or links
            category_links = soup.find_all('a', href=re.compile(r'/category/restaurants/'))
            
            for link in category_links:
                href = link.get('href')
                text = link.get_text(strip=True)
                if href and text:
                    categories.append({
                        'name': text,
                        'url': urljoin(self.base_url, href)
                    })
            
            # If no categories found, try to find them in the page content
            if not categories:
                # Look for common kosher categories
                category_texts = soup.find_all(text=re.compile(r'(Dairy|Meat|Pareve|Fish|Vegetarian)', re.IGNORECASE))
                for text in category_texts:
                    if text.strip():
                        categories.append({
                            'name': text.strip(),
                            'url': url  # Use base URL for now
                        })
            
            logger.info(f"Found {len(categories)} categories: {[c['name'] for c in categories]}")
            return categories
            
        except Exception as e:
            logger.error(f"Error fetching restaurant categories: {e}")
            return []
    
    def scrape_restaurants_from_category(self, category_url, category_name):
        """Scrape restaurants from a specific category page."""
        restaurants = []
        
        try:
            logger.info(f"Scraping restaurants from category: {category_name}")
            response = self.session.get(category_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find restaurant listings
            # Look for restaurant cards or listings
            restaurant_elements = soup.find_all(['div', 'article'], class_=re.compile(r'(restaurant|listing|card)', re.IGNORECASE))
            
            if not restaurant_elements:
                # Try alternative selectors
                restaurant_elements = soup.find_all('div', class_=re.compile(r'(item|entry)', re.IGNORECASE))
            
            logger.info(f"Found {len(restaurant_elements)} restaurant elements")
            
            for element in restaurant_elements:
                restaurant_data = self.extract_restaurant_data(element, category_name)
                if restaurant_data:
                    restaurants.append(restaurant_data)
                    logger.info(f"Extracted: {restaurant_data['name']}")
            
            # If no restaurants found with selectors, try to parse the page content
            if not restaurants:
                restaurants = self.parse_page_content_for_restaurants(soup, category_name)
            
            return restaurants
            
        except Exception as e:
            logger.error(f"Error scraping category {category_name}: {e}")
            return []
    
    def extract_restaurant_data(self, element, category_name):
        """Extract restaurant data from a single element."""
        try:
            # Extract restaurant name
            name_elem = element.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) or element.find(class_=re.compile(r'(name|title)', re.IGNORECASE))
            name = name_elem.get_text(strip=True) if name_elem else None
            
            if not name:
                return None
            
            # Extract address
            address_elem = element.find(class_=re.compile(r'(address|location)', re.IGNORECASE)) or element.find(text=re.compile(r'\d+.*(Street|Ave|Road|Blvd|St|Dr)', re.IGNORECASE))
            address = address_elem.get_text(strip=True) if hasattr(address_elem, 'get_text') else str(address_elem) if address_elem else None
            
            # Extract phone number
            phone_elem = element.find(class_=re.compile(r'(phone|tel)', re.IGNORECASE)) or element.find(text=re.compile(r'\d{3}-\d{3}-\d{4}'))
            phone = phone_elem.get_text(strip=True) if hasattr(phone_elem, 'get_text') else str(phone_elem) if phone_elem else None
            
            # Determine kosher type based on category
            kosher_type = self.determine_kosher_type_from_category(category_name)
            
            return {
                'name': name,
                'address': address,
                'phone_number': phone,
                'kosher_type': kosher_type,
                'certifying_agency': 'ORB Kosher',
                'source': 'orb',
                'category': category_name
            }
            
        except Exception as e:
            logger.error(f"Error extracting restaurant data: {e}")
            return None
    
    def parse_page_content_for_restaurants(self, soup, category_name):
        """Parse page content to find restaurant information when structured elements aren't found."""
        restaurants = []
        
        try:
            # Look for text patterns that indicate restaurant listings
            # This is a fallback method when structured HTML isn't available
            
            # Find all text blocks that might contain restaurant info
            text_blocks = soup.find_all(text=True)
            
            current_restaurant = {}
            
            for text in text_blocks:
                text = text.strip()
                if not text:
                    continue
                
                # Look for restaurant name patterns
                if re.match(r'^[A-Z][a-zA-Z\s&\'-]+$', text) and len(text) > 3:
                    # This might be a restaurant name
                    if current_restaurant and current_restaurant.get('name'):
                        # Save previous restaurant
                        if current_restaurant.get('name') and current_restaurant.get('address'):
                            current_restaurant['kosher_type'] = self.determine_kosher_type_from_category(category_name)
                            current_restaurant['certifying_agency'] = 'ORB Kosher'
                            current_restaurant['source'] = 'orb'
                            current_restaurant['category'] = category_name
                            restaurants.append(current_restaurant.copy())
                    
                    current_restaurant = {'name': text}
                
                # Look for address patterns
                elif re.search(r'\d+.*(Street|Ave|Road|Blvd|St|Dr).*[A-Z]{2}\s\d{5}', text):
                    if current_restaurant:
                        current_restaurant['address'] = text
                
                # Look for phone patterns
                elif re.search(r'\d{3}-\d{3}-\d{4}', text):
                    if current_restaurant:
                        current_restaurant['phone_number'] = text
            
            # Add the last restaurant
            if current_restaurant and current_restaurant.get('name') and current_restaurant.get('address'):
                current_restaurant['kosher_type'] = self.determine_kosher_type_from_category(category_name)
                current_restaurant['certifying_agency'] = 'ORB Kosher'
                current_restaurant['source'] = 'orb'
                current_restaurant['category'] = category_name
                restaurants.append(current_restaurant)
            
            return restaurants
            
        except Exception as e:
            logger.error(f"Error parsing page content: {e}")
            return []
    
    def determine_kosher_type_from_category(self, category_name):
        """Determine kosher type based on category name."""
        category_lower = category_name.lower()
        
        if 'dairy' in category_lower:
            return 'dairy'
        elif 'meat' in category_lower:
            return 'meat'
        elif 'pareve' in category_lower or 'parve' in category_lower:
            return 'pareve'
        elif 'fish' in category_lower:
            return 'pareve'
        elif 'vegetarian' in category_lower:
            return 'pareve'
        else:
            # Default based on common patterns
            return 'pareve'
    
    def scrape_all_restaurants(self):
        """Scrape all restaurants from ORB website."""
        all_restaurants = []
        
        try:
            # Get categories
            categories = self.get_restaurant_categories()
            
            if not categories:
                # If no categories found, try scraping the main restaurants page
                logger.info("No categories found, scraping main restaurants page")
                restaurants = self.scrape_restaurants_from_category(
                    f"{self.base_url}/category/restaurants/", 
                    "Restaurants"
                )
                all_restaurants.extend(restaurants)
            else:
                # Scrape each category
                for category in categories:
                    logger.info(f"Scraping category: {category['name']}")
                    restaurants = self.scrape_restaurants_from_category(
                        category['url'], 
                        category['name']
                    )
                    all_restaurants.extend(restaurants)
                    
                    # Be respectful with delays
                    time.sleep(2)
            
            logger.info(f"Total restaurants scraped: {len(all_restaurants)}")
            return all_restaurants
            
        except Exception as e:
            logger.error(f"Error scraping all restaurants: {e}")
            return []
    
    def save_restaurants_to_database(self, restaurants):
        """Save scraped restaurants to the database."""
        try:
            logger.info(f"Saving {len(restaurants)} restaurants to database")
            
            success_count = 0
            for restaurant in restaurants:
                try:
                    # Check if restaurant already exists
                    existing = self.db_manager.get_restaurant_by_name(restaurant['name'])
                    
                    if existing:
                        # Update existing restaurant with ORB data
                        self.db_manager.update_restaurant_orb_data(
                            existing['id'],
                            restaurant['address'],
                            restaurant['kosher_type'],
                            restaurant['certifying_agency']
                        )
                        logger.info(f"Updated existing restaurant: {restaurant['name']}")
                    else:
                        # Create new restaurant
                        self.db_manager.add_restaurant_simple(
                            name=restaurant['name'],
                            address=restaurant['address'],
                            phone_number=restaurant.get('phone_number'),
                            kosher_type=restaurant['kosher_type'],
                            certifying_agency=restaurant['certifying_agency'],
                            source=restaurant['source']
                        )
                        logger.info(f"Added new restaurant: {restaurant['name']}")
                    
                    success_count += 1
                    
                except Exception as e:
                    logger.error(f"Error saving restaurant {restaurant['name']}: {e}")
            
            logger.info(f"Successfully saved {success_count} restaurants")
            return success_count
            
        except Exception as e:
            logger.error(f"Error saving restaurants to database: {e}")
            return 0

def main():
    """Main function to run the ORB scraper."""
    try:
        logger.info("Starting ORB Kosher scraper")
        
        scraper = ORBScraper()
        
        # Scrape restaurants
        restaurants = scraper.scrape_all_restaurants()
        
        if restaurants:
            logger.info(f"Scraped {len(restaurants)} restaurants")
            
            # Save to database
            saved_count = scraper.save_restaurants_to_database(restaurants)
            
            logger.info(f"Successfully saved {saved_count} restaurants to database")
            
            # Print sample of scraped data
            logger.info("Sample scraped restaurants:")
            for i, restaurant in enumerate(restaurants[:5]):
                logger.info(f"{i+1}. {restaurant['name']} - {restaurant['kosher_type']} - {restaurant['address']}")
        
        else:
            logger.warning("No restaurants were scraped")
        
        logger.info("ORB scraper completed")
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main() 