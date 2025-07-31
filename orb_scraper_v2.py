#!/usr/bin/env python3
"""
ORB Kosher Scraper V2
Maps ORB data to current database schema and includes Chalav Stam and Pas Yisroel information.
"""

import asyncio
import logging
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database_manager_v3 import EnhancedDatabaseManager as DatabaseManager

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ORBScraperV2:
    """ORB Kosher scraper that maps to current database schema."""
    
    def __init__(self):
        self.base_url = "https://www.orbkosher.com"
        self.db_manager = DatabaseManager()
        
        # Chalav Stam restaurants (only these 3 should be Chalav Stam)
        self.chalav_stam_restaurants = [
            "Cafe 95 at JARC",
            "Hollywood Deli", 
            "Sobol Boynton Beach"
        ]
        
        # Pas Yisroel restaurants (only these specific restaurants)
        self.pas_yisroel_restaurants = [
            "Grand Cafe Hollywood",
            "Yum Berry Cafe & Sushi Bar", 
            "Pita Xpress",
            "Mizrachi's Pizza in Hollywood",
            "Boca Grill",
            "Shalom Haifa",
            "Chill & Grill Pita Boca",
            "Hummus Achla Hallandale",
            "Jon's Place",
            "Levy's Shawarma",
            "Holy Smokes BBQ and Grill (Food Truck)",
            "Friendship Cafe & Catering",
            "Tagine by Alma Grill",
            "Lox N Bagel (Bagel Factory Cafe)",
            "Kosher Bagel Cove",
            "Cafe Noir",
            "Grill Xpress",
            "PX Grill Mediterranean Cuisine",
            "Carmela's Boca",
            "Ariel's Delicious Pizza",
            "Oak and Ember",
            "Rave Pizza & Sushi",
            "Burnt Smokehouse and Bar",
            "Vish Hummus Hollywood"
        ]
        
    async def setup_playwright(self):
        """Setup Playwright browser."""
        try:
            from playwright.async_api import async_playwright
            
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            self.page = await self.browser.new_page()
            
            # Set user agent
            await self.page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            
            logger.info("Playwright browser setup completed")
            return True
            
        except Exception as e:
            logger.error(f"Playwright setup failed: {e}")
            return False
    
    def extract_listing_and_kosher_type(self, title_text: str) -> Tuple[str, str]:
        """Extract listing type and kosher type from title header."""
        try:
            # Parse: "Restaurants » Dairy" -> ("Restaurants", "Dairy")
            if "»" in title_text:
                parts = title_text.split("»")
                if len(parts) >= 2:
                    listing_type = parts[0].strip()
                    kosher_type = parts[1].strip().lower()  # Convert to lowercase
                    return listing_type, kosher_type
            
            # Fallback: try to extract from text
            title_lower = title_text.lower()
            
            # Determine kosher type from keywords
            if 'dairy' in title_lower:
                kosher_type = 'dairy'
            elif 'meat' in title_lower:
                kosher_type = 'meat'
            elif 'pareve' in title_lower or 'parve' in title_lower:
                kosher_type = 'pareve'
            elif 'fish' in title_lower:
                kosher_type = 'pareve'
            else:
                kosher_type = 'unknown'
            
            # Determine listing type
            if 'restaurant' in title_lower:
                listing_type = 'Restaurants'
            elif 'catering' in title_lower:
                listing_type = 'Catering'
            elif 'market' in title_lower or 'grocery' in title_lower:
                listing_type = 'Markets'
            else:
                listing_type = 'Businesses'
            
            return listing_type, kosher_type
            
        except Exception as e:
            logger.error(f"Error extracting listing and kosher type from '{title_text}': {e}")
            return 'Businesses', 'unknown'
    
    def normalize_url(self, url: str, base_url: str = None) -> str:
        """Normalize URL to full URL."""
        if not url:
            return None
        
        if base_url is None:
            base_url = self.base_url
        
        # If already absolute URL
        if url.startswith(('http://', 'https://')):
            return url
        
        # If relative URL, prepend base URL
        return urljoin(base_url, url)
    
    def extract_address_components(self, address_text: str) -> Dict[str, str]:
        """Extract city, state, zip from address."""
        components = {
            'city': '',
            'state': '',
            'zip_code': ''
        }
        
        if not address_text:
            return components
        
        try:
            # Split by comma
            parts = address_text.split(',')
            if len(parts) >= 2:
                # Last part should contain city, state, zip
                city_state_zip = parts[-1].strip()
                
                # Look for state (FL)
                if 'FL' in city_state_zip:
                    components['state'] = 'FL'
                    city_zip_parts = city_state_zip.replace('FL', '').strip()
                    
                    # Try to extract zip code (5 digits)
                    import re
                    zip_match = re.search(r'\d{5}', city_zip_parts)
                    if zip_match:
                        components['zip_code'] = zip_match.group()
                        components['city'] = city_zip_parts.replace(zip_match.group(), '').strip()
                    else:
                        components['city'] = city_zip_parts
                
                # If we have more parts, the first part might be the street address
                if len(parts) >= 2:
                    components['address'] = parts[0].strip()
            
        except Exception as e:
            logger.error(f"Error extracting address components from '{address_text}': {e}")
        
        return components
    
    async def extract_business_data(self, business_element, kosher_type: str, listing_type: str) -> Optional[Dict]:
        """Extract business data from a single .business-listing element."""
        try:
            # Extract name
            name_elem = await business_element.query_selector('.logoTitle')
            name = await name_elem.inner_text() if name_elem else None
            if name:
                name = name.strip()
            
            if not name:
                logger.warning("No name found for business listing")
                return None
            
            # Extract photo
            img_elem = await business_element.query_selector('a img')
            photo = None
            if img_elem:
                photo_src = await img_elem.get_attribute('src')
                photo = self.normalize_url(photo_src) if photo_src else None
            
            # Extract phone
            phone_elem = await business_element.query_selector('.phone a[href^="tel:"]')
            phone = None
            if phone_elem:
                phone = await phone_elem.inner_text()
                phone = phone.strip() if phone else None
            
            # Extract address (real address, not PDF link)
            address_elem = await business_element.query_selector('.address a:not([href$=".pdf"])')
            address = None
            if address_elem:
                address = await address_elem.inner_text()
                address = address.strip() if address else None
            
            # Extract website
            website_elem = await business_element.query_selector('a[href^="http"]')
            website = None
            if website_elem:
                website_href = await website_elem.get_attribute('href')
                website = website_href if website_href else None
            
            # Extract kosher certificate link
            cert_elem = await business_element.query_selector('.address a[href$=".pdf"]')
            kosher_cert_link = None
            if cert_elem:
                cert_href = await cert_elem.get_attribute('href')
                kosher_cert_link = self.normalize_url(cert_href) if cert_href else None
            
            # Extract address components
            address_components = self.extract_address_components(address)
            
            # Determine Chalav Yisroel and Pas Yisroel status
            is_cholov_yisroel = True  # Default to Chalav Yisroel
            if name in self.chalav_stam_restaurants:
                is_cholov_yisroel = False
            
            is_pas_yisroel = False  # Default to not Pas Yisroel
            if name in self.pas_yisroel_restaurants:
                is_pas_yisroel = True
            
            # Map to current database schema
            business_data = {
                'name': name,
                'address': address or '',
                'city': address_components.get('city', ''),
                'state': address_components.get('state', ''),
                'zip_code': address_components.get('zip_code', ''),
                'phone': phone or '',
                'website': website or '',
                'kosher_type': kosher_type,
                'status': 'active',
                'hours_open': '',
                'short_description': f"Kosher {kosher_type} restaurant certified by ORB",
                'price_range': '',
                'image_url': photo or '',
                'latitude': None,
                'longitude': None,
                'rating': None,
                'review_count': None,
                'google_rating': None,
                'google_review_count': None,
                'google_reviews': None,
                'is_kosher': True,
                'is_glatt': False,
                'is_cholov_yisroel': is_cholov_yisroel,
                'is_pas_yisroel': is_pas_yisroel,
                'is_bishul_yisroel': False,
                'is_mehadrin': False,
                'is_hechsher': True,
                'kosher_cert_link': kosher_cert_link or '',
                'detail_url': website or '',
                'email': '',
                'google_listing_url': '',
                'category': 'restaurant',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            return business_data
            
        except Exception as e:
            logger.error(f"Error extracting business data: {e}")
            return None
    
    async def scrape_category_page(self, category_url: str) -> List[Dict]:
        """Scrape all businesses from a category page."""
        try:
            logger.info(f"Scraping category page: {category_url}")
            
            await self.page.goto(category_url, wait_until='networkidle')
            await asyncio.sleep(3)  # Allow page to load
            
            # Determine kosher type from URL
            kosher_type = 'unknown'
            if 'restaurants' in category_url:
                kosher_type = 'dairy'  # ORB restaurants are dairy
            elif 'fish' in category_url:
                kosher_type = 'pareve'  # ORB fish are pareve
            
            listing_type = 'Restaurants' if 'restaurants' in category_url else 'Businesses'
            logger.info(f"Category: {listing_type} » {kosher_type}")
            
            # Find all business listings
            business_elements = await self.page.query_selector_all('.business-listing')
            logger.info(f"Found {len(business_elements)} business listings")
            
            businesses = []
            for business_element in business_elements:
                try:
                    business_data = await self.extract_business_data(business_element, kosher_type, listing_type)
                    if business_data:
                        businesses.append(business_data)
                        logger.info(f"Extracted: {business_data['name']} ({kosher_type})")
                except Exception as e:
                    logger.error(f"Error processing business element: {e}")
                    continue
            
            return businesses
            
        except Exception as e:
            logger.error(f"Error scraping category page {category_url}: {e}")
            return []
    
    def save_businesses_to_database(self, businesses: List[Dict]) -> int:
        """Save businesses to the database."""
        try:
            if not businesses:
                logger.warning("No businesses to save")
                return 0
            
            success_count = 0
            
            for business in businesses:
                try:
                    # Add restaurant (no duplicate checking since we cleaned the database)
                    success = self.db_manager.add_restaurant(business)
                    if success:
                        success_count += 1
                        logger.info(f"Added restaurant: {business['name']}")
                    else:
                        logger.error(f"Failed to add restaurant: {business['name']}")
                    
                except Exception as e:
                    logger.error(f"Error saving business {business['name']}: {e}")
            
            logger.info(f"Successfully saved {success_count} businesses")
            return success_count
            
        except Exception as e:
            logger.error(f"Error saving businesses to database: {e}")
            return 0
    
    async def scrape_all_categories(self) -> List[Dict]:
        """Scrape all available ORB categories."""
        try:
            # Define ORB category URLs
            category_urls = [
                f"{self.base_url}/category/restaurants/",  # Dairy (238 restaurants)
                f"{self.base_url}/category/fish/",  # Fish/Pareve (13 businesses)
            ]
            
            all_businesses = []
            
            for category_url in category_urls:
                logger.info(f"Scraping category: {category_url}")
                businesses = await self.scrape_category_page(category_url)
                all_businesses.extend(businesses)
                
                # Be respectful with delays
                await asyncio.sleep(3)
            
            logger.info(f"Total businesses scraped: {len(all_businesses)}")
            return all_businesses
            
        except Exception as e:
            logger.error(f"Error scraping all categories: {e}")
            return []
    
    async def cleanup(self):
        """Cleanup Playwright resources."""
        try:
            if hasattr(self, 'browser'):
                await self.browser.close()
            if hasattr(self, 'playwright'):
                await self.playwright.stop()
            logger.info("Playwright cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    async def run(self):
        """Main execution method."""
        try:
            logger.info("Starting ORB Scraper V2")
            
            # Connect to database
            if not self.db_manager.connect():
                logger.error("Failed to connect to database")
                return False
            
            # Setup Playwright
            if not await self.setup_playwright():
                return False
            
            # Scrape all categories
            businesses = await self.scrape_all_categories()
            
            if businesses:
                # Save to database
                saved_count = self.save_businesses_to_database(businesses)
                
                logger.info(f"Scraping completed. Saved {saved_count} businesses")
                
                # Show sample results
                logger.info("Sample scraped businesses:")
                for i, business in enumerate(businesses[:5]):
                    logger.info(f"{i+1}. {business['name']} - {business['kosher_category']} - {business['address']}")
                
                # Show statistics
                kosher_types = {}
                for business in businesses:
                    kosher_type = business.get('kosher_category', 'unknown')
                    kosher_types[kosher_type] = kosher_types.get(kosher_type, 0) + 1
                
                logger.info("Kosher Type Statistics:")
                for kosher_type, count in kosher_types.items():
                    logger.info(f"  - {kosher_type}: {count} restaurants")
                
                # Show Chalav Yisroel statistics
                chalav_yisroel_count = sum(1 for b in businesses if b.get('is_cholov_yisroel', False))
                chalav_stam_count = sum(1 for b in businesses if not b.get('is_cholov_yisroel', True))
                pas_yisroel_count = sum(1 for b in businesses if b.get('is_pas_yisroel', False))
                
                logger.info("Kosher Supervision Statistics:")
                logger.info(f"  - Chalav Yisroel: {chalav_yisroel_count}")
                logger.info(f"  - Chalav Stam: {chalav_stam_count}")
                logger.info(f"  - Pas Yisroel: {pas_yisroel_count}")
            
            else:
                logger.warning("No businesses were scraped")
            
            return True
            
        except Exception as e:
            logger.error(f"Scraper failed: {e}")
            return False
        finally:
            await self.cleanup()
            self.db_manager.disconnect()

async def main():
    """Main entry point."""
    scraper = ORBScraperV2()
    success = await scraper.run()
    
    if success:
        logger.info("ORB Scraper V2 completed successfully")
    else:
        logger.error("ORB Scraper V2 failed")
    
    return success

if __name__ == "__main__":
    asyncio.run(main()) 