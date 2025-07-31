#!/usr/bin/env python3
"""
ORB Kosher Restaurant Scraper
Scrapes kosher restaurant data from ORB Kosher website and populates the database.
"""

import os
import json
import time
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
from database_manager_v2 import EnhancedDatabaseManager
import structlog

# Configure structured logging
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

class ORBKosherScraper:
    """Scraper for ORB Kosher restaurant data."""
    
    def __init__(self, database_url: str = None):
        """Initialize the scraper with database connection."""
        self.database_url = database_url or os.environ.get('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is required")
        
        self.db_manager = EnhancedDatabaseManager(self.database_url)
        self.db_manager.connect()
        logger.info("ORB Kosher scraper initialized")
    
    def extract_phone_number(self, text: str) -> Optional[str]:
        """Extract phone number from text using regex."""
        # Look for phone number patterns
        phone_patterns = [
            r'(\d{3}-\d{3}-\d{4})',  # 305-123-4567
            r'(\d{3}\.\d{3}\.\d{4})',  # 305.123.4567
            r'(\d{3}\s\d{3}\s\d{4})',  # 305 123 4567
            r'\((\d{3})\)\s*(\d{3})-(\d{4})',  # (305) 123-4567
        ]
        
        for pattern in phone_patterns:
            match = re.search(pattern, text)
            if match:
                if len(match.groups()) == 3:  # (305) 123-4567 format
                    return f"({match.group(1)}) {match.group(2)}-{match.group(3)}"
                else:
                    return match.group(1)
        
        return None
    
    def extract_address_components(self, address_text: str) -> Dict[str, str]:
        """Extract city, state, zip from address text."""
        if not address_text:
            return {'city': '', 'state': '', 'zip_code': ''}
        
        # Common Florida cities and states
        florida_cities = [
            'Miami', 'Fort Lauderdale', 'Hollywood', 'Boca Raton', 'West Palm Beach',
            'Aventura', 'Sunny Isles Beach', 'Surfside', 'Hallandale Beach',
            'Dania Beach', 'Davie', 'Cooper City', 'Coral Springs', 'Deerfield Beach',
            'Delray Beach', 'Boynton Beach', 'Lake Worth', 'Palm Beach Gardens',
            'North Miami Beach', 'Oakland Park', 'Pembroke Park', 'Pompano Beach',
            'Tamarac', 'Weston', 'Plantation', 'Miramar', 'Pembroke Pines'
        ]
        
        address_parts = address_text.split(',')
        city = state = zip_code = ''
        
        if len(address_parts) >= 2:
            # Try to extract city from the second part
            city_part = address_parts[1].strip()
            for florida_city in florida_cities:
                if florida_city.lower() in city_part.lower():
                    city = florida_city
                    break
            
            # Extract state and zip from the last part
            if len(address_parts) >= 3:
                state_zip_part = address_parts[2].strip()
                # Look for state abbreviation (FL) and zip code
                state_match = re.search(r'\b(FL|Florida)\b', state_zip_part, re.IGNORECASE)
                zip_match = re.search(r'\b(\d{5})\b', state_zip_part)
                
                if state_match:
                    state = 'FL'
                if zip_match:
                    zip_code = zip_match.group(1)
        
        return {
            'city': city,
            'state': state,
            'zip_code': zip_code
        }
    
    def determine_kosher_type(self, text: str) -> str:
        """Determine kosher type from text."""
        text_lower = text.lower()
        
        if 'meat' in text_lower:
            return 'Meat'
        elif 'dairy' in text_lower:
            return 'Dairy'
        elif 'parve' in text_lower or 'pareve' in text_lower:
            return 'Parve'
        else:
            return 'Restaurant'  # Default
    
    def extract_kosher_flags(self, text: str) -> Dict[str, bool]:
        """Extract kosher certification flags from text."""
        text_lower = text.lower()
        
        return {
            'is_kosher': True,  # All ORB restaurants are kosher
            'is_glatt': 'glatt' in text_lower,
            'is_cholov_yisroel': 'cholov yisroel' in text_lower,
            'is_pas_yisroel': 'pas yisroel' in text_lower,
            'is_bishul_yisroel': 'bishul yisroel' in text_lower,
            'is_mehadrin': 'mehadrin' in text_lower,
            'is_hechsher': True,  # All ORB restaurants have hechsher
        }
    
    def scrape_restaurant_details(self, page, detail_url: str) -> Dict[str, Any]:
        """Scrape detailed information from a restaurant's detail page."""
        try:
            page.goto(detail_url, wait_until='networkidle')
            time.sleep(2)  # Allow page to load
            
            soup = BeautifulSoup(page.content(), "html.parser")
            
            # Extract all text content
            content = soup.select_one(".fusion-post-content")
            if not content:
                content = soup.select_one("main") or soup.select_one("body")
            
            text = content.get_text(separator="\n") if content else ""
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            
            # Initialize data
            details = {
                'address': '',
                'phone': '',
                'website': '',
                'kosher_type': 'Restaurant',
                'extra_info': '',
                'image_url': '',
                'description': ''
            }
            
            # Extract information from text
            for line in lines:
                line_lower = line.lower()
                
                # Address extraction
                if 'address:' in line_lower:
                    details['address'] = line.replace('Address:', '').replace('address:', '').strip()
                elif any(city in line_lower for city in ['miami', 'fort lauderdale', 'boca raton', 'hollywood', 'aventura']):
                    if not details['address'] and len(line) > 10:
                        details['address'] = line
                
                # Phone extraction
                if 'phone:' in line_lower:
                    details['phone'] = line.replace('Phone:', '').replace('phone:', '').strip()
                elif not details['phone']:
                    phone = self.extract_phone_number(line)
                    if phone:
                        details['phone'] = phone
                
                # Website extraction
                if 'website:' in line_lower or 'www.' in line_lower or 'http' in line_lower:
                    details['website'] = line.replace('Website:', '').replace('website:', '').strip()
                
                # Kosher type extraction
                if any(kosher_type in line_lower for kosher_type in ['meat', 'dairy', 'parve', 'pareve']):
                    details['kosher_type'] = self.determine_kosher_type(line)
                
                # Extra kosher info
                if any(term in line_lower for term in ['pas yisroel', 'cholov yisroel', 'glatt', 'mehadrin']):
                    details['extra_info'] += line + " "
            
            # Extract image
            image_elem = soup.select_one(".fusion-post-thumbnail img") or soup.select_one("img")
            if image_elem and image_elem.get('src'):
                details['image_url'] = image_elem['src']
            
            # Create description from available info
            description_parts = []
            if details['kosher_type'] != 'Restaurant':
                description_parts.append(f"Kosher {details['kosher_type']} restaurant")
            if details['extra_info']:
                description_parts.append(details['extra_info'])
            
            details['description'] = ' '.join(description_parts) if description_parts else 'Kosher restaurant certified by ORB'
            
            return details
            
        except Exception as e:
            logger.error("Error scraping restaurant details", error=str(e), url=detail_url)
            return {
                'address': '',
                'phone': '',
                'website': '',
                'kosher_type': 'Restaurant',
                'extra_info': '',
                'image_url': '',
                'description': 'Kosher restaurant certified by ORB'
            }
    
    def scrape_orb_category(self, category_url: str, category_name: str = "Restaurant") -> List[Dict[str, Any]]:
        """Scrape all restaurants from a category page."""
        all_data = []
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                page.goto(category_url, wait_until='networkidle')
                time.sleep(3)  # Allow page to load
                
                page_num = 1
                while True:
                    logger.info(f"Scraping page {page_num} of {category_name}")
                    
                    soup = BeautifulSoup(page.content(), "html.parser")
                    
                    # Find restaurant listings
                    # Look for different possible selectors
                    listings = (
                        soup.select(".fusion-post-wrapper") or
                        soup.select(".restaurant-listing") or
                        soup.select("article") or
                        soup.select(".listing-item")
                    )
                    
                    if not listings:
                        # Try to find any links that might be restaurant listings
                        links = soup.select("a[href*='/listings/']") or soup.select("a[href*='/restaurant/']")
                        if links:
                            listings = [{'link': link} for link in links]
                    
                    if not listings:
                        logger.warning(f"No listings found on page {page_num}")
                        break
                    
                    for listing in listings:
                        try:
                            # Extract restaurant name and link
                            if hasattr(listing, 'select_one'):
                                name_elem = listing.select_one("h2 a") or listing.select_one("h3 a") or listing.select_one("a")
                            else:
                                name_elem = listing.get('link')
                            
                            if not name_elem:
                                continue
                            
                            if hasattr(name_elem, 'text'):
                                name = name_elem.text.strip()
                                detail_url = name_elem.get('href', '')
                            else:
                                name = name_elem.text.strip()
                                detail_url = name_elem.get('href', '')
                            
                            if not name or not detail_url:
                                continue
                            
                            # Skip if we already have this restaurant
                            if any(item['name'] == name for item in all_data):
                                continue
                            
                            logger.info(f"Scraping details for: {name}")
                            
                            # Scrape detailed information
                            details = self.scrape_restaurant_details(page, detail_url)
                            
                            # Extract address components
                            address_components = self.extract_address_components(details['address'])
                            
                            # Extract kosher flags
                            kosher_flags = self.extract_kosher_flags(details['extra_info'])
                            
                            # Create restaurant data
                            restaurant_data = {
                                'name': name,
                                'address': details['address'],
                                'city': address_components['city'],
                                'state': address_components['state'],
                                'zip_code': address_components['zip_code'],
                                'phone': details['phone'],
                                'website': details['website'],
                                'cuisine_type': details['kosher_type'],
                                'description': details['description'],
                                'image_url': details['image_url'],
                                'hechsher_details': 'ORB Kosher',
                                'is_kosher': kosher_flags['is_kosher'],
                                'is_glatt': kosher_flags['is_glatt'],
                                'is_cholov_yisroel': kosher_flags['is_cholov_yisroel'],
                                'is_pas_yisroel': kosher_flags['is_pas_yisroel'],
                                'is_bishul_yisroel': kosher_flags['is_bishul_yisroel'],
                                'is_mehadrin': kosher_flags['is_mehadrin'],
                                'is_hechsher': kosher_flags['is_hechsher'],
                                'rating': 4.0,  # Default rating for ORB restaurants
                                'review_count': 0,
                                'price_range': '$$',  # Default price range
                                'hours': 'Hours vary by location',
                                'created_at': datetime.utcnow(),
                                'updated_at': datetime.utcnow()
                            }
                            
                            all_data.append(restaurant_data)
                            
                            # Rate limiting
                            time.sleep(1)
                            
                        except Exception as e:
                            logger.error("Error processing restaurant listing", error=str(e))
                            continue
                    
                    # Check for next page
                    next_button = page.locator(".pagination-next, .next, a[rel='next']")
                    if next_button.count() > 0 and next_button.first.is_enabled():
                        next_button.first.click()
                        time.sleep(2)
                        page_num += 1
                    else:
                        break
                
            except Exception as e:
                logger.error("Error during scraping", error=str(e))
            finally:
                browser.close()
        
        logger.info(f"Scraped {len(all_data)} restaurants from {category_name}")
        return all_data
    
    def insert_restaurants_to_db(self, restaurants: List[Dict[str, Any]]) -> int:
        """Insert scraped restaurants into the database."""
        inserted_count = 0
        
        for restaurant in restaurants:
            try:
                # Check if restaurant already exists
                existing = self.db_manager.search_restaurants(
                    query=restaurant['name'],
                    limit=1
                )
                
                if existing:
                    logger.info(f"Restaurant already exists: {restaurant['name']}")
                    continue
                
                # Insert new restaurant
                success = self.db_manager.add_restaurant(restaurant)
                if success:
                    inserted_count += 1
                    logger.info(f"Inserted restaurant: {restaurant['name']}")
                else:
                    logger.error(f"Failed to insert restaurant: {restaurant['name']}")
                
            except Exception as e:
                logger.error(f"Error inserting restaurant {restaurant['name']}", error=str(e))
                continue
        
        logger.info(f"Successfully inserted {inserted_count} new restaurants")
        return inserted_count
    
    def scrape_all_categories(self) -> int:
        """Scrape all restaurant categories from ORB Kosher."""
        categories = [
            {
                'url': 'https://www.orbkosher.com/category/restaurants/',
                'name': 'Restaurant'
            }
        ]
        
        total_inserted = 0
        
        for category in categories:
            logger.info(f"Starting to scrape category: {category['name']}")
            
            try:
                restaurants = self.scrape_orb_category(
                    category['url'],
                    category['name']
                )
                
                if restaurants:
                    inserted = self.insert_restaurants_to_db(restaurants)
                    total_inserted += inserted
                
            except Exception as e:
                logger.error(f"Error scraping category {category['name']}", error=str(e))
                continue
        
        return total_inserted
    
    def save_to_json(self, restaurants: List[Dict[str, Any]], filename: str = None):
        """Save scraped data to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"orb_restaurants_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(restaurants, f, indent=2, default=str)
        
        logger.info(f"Saved {len(restaurants)} restaurants to {filename}")
    
    def close(self):
        """Close database connection."""
        if self.db_manager:
            self.db_manager.close()

def main():
    """Main function to run the scraper."""
    try:
        scraper = ORBKosherScraper()
        
        logger.info("Starting ORB Kosher restaurant scraping")
        
        # Scrape all categories
        total_inserted = scraper.scrape_all_categories()
        
        logger.info(f"Scraping completed. Total restaurants inserted: {total_inserted}")
        
    except Exception as e:
        logger.error("Error in main scraper function", error=str(e))
    finally:
        if 'scraper' in locals():
            scraper.close()

if __name__ == "__main__":
    main() 