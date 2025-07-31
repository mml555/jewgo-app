#!/usr/bin/env python3
"""
ORB Kosher Scraper V2 - Preview Mode
====================================

This is a preview version that collects data but doesn't save to the database.
Use this to review the data before committing to the database.

Author: JewGo Development Team
Version: 2.0 Preview
Last Updated: 2024
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

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ORBScraperV2Preview:
    """ORB Kosher scraper preview mode - collects data without saving to database."""
    
    def __init__(self):
        self.base_url = "https://www.orbkosher.com"
        
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
            # Extract business name
            name_element = await business_element.query_selector('.logoTitle, .business-name, h3, h4')
            name = await name_element.text_content() if name_element else "Unknown Business"
            name = name.strip()
            
            # Extract address
            address_element = await business_element.query_selector('.address, .business-address')
            address = await address_element.text_content() if address_element else ""
            address = address.strip()
            
            # Extract phone number
            phone_element = await business_element.query_selector('.phone, .business-phone')
            phone = await phone_element.text_content() if phone_element else ""
            phone = phone.strip()
            
            # Extract website URL
            website_element = await business_element.query_selector('a[href*="http"]')
            website = await website_element.get_attribute('href') if website_element else ""
            
            # Extract image URL
            img_element = await business_element.query_selector('img')
            image_url = await img_element.get_attribute('src') if img_element else ""
            image_url = self.normalize_url(image_url) if image_url else ""
            
            # Extract kosher certificate link
            cert_element = await business_element.query_selector('a[href*="pdf"]')
            kosher_cert_link = await cert_element.get_attribute('href') if cert_element else ""
            kosher_cert_link = self.normalize_url(kosher_cert_link) if kosher_cert_link else ""
            
            # Extract detail URL
            detail_element = await business_element.query_selector('a[href*="/business/"]')
            detail_url = await detail_element.get_attribute('href') if detail_element else ""
            detail_url = self.normalize_url(detail_url) if detail_url else ""
            
            # Parse address components
            address_components = self.extract_address_components(address)
            
            # Determine Chalav Yisroel/Stam status
            is_cholov_yisroel = name not in self.chalav_stam_restaurants
            
            # Determine Pas Yisroel status
            is_pas_yisroel = name in self.pas_yisroel_restaurants
            
            # Create business data dictionary
            business_data = {
                'name': name,
                'address': address,
                'city': address_components.get('city', ''),
                'state': address_components.get('state', 'FL'),
                'zip_code': address_components.get('zip_code', ''),
                'phone_number': phone,
                'website': website,
                'image_url': image_url,
                'kosher_type': kosher_type,
                'is_cholov_yisroel': is_cholov_yisroel,
                'is_pas_yisroel': is_pas_yisroel,
                'certifying_agency': 'ORB',
                'kosher_cert_link': kosher_cert_link,
                'detail_url': detail_url,
                'short_description': 'Kosher {} restaurant certified by ORB'.format(kosher_type),
                'google_listing_url': None,
                'latitude': None,
                'longitude': None,
                'hours': None,
                'hours_open': None,
                'category': 'restaurant',
                'listing_type': listing_type,
                'price_range': '',
                'email': '',
                'status': 'active',
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
            
            businesses = []
            
            # For the main restaurants page, we need to scrape each section separately
            if '/category/restaurants/' in category_url:
                # Scrape dairy section
                logger.info("Scraping dairy section...")
                dairy_businesses = await self.scrape_section('dairy')
                businesses.extend(dairy_businesses)
                
                # Scrape meat section
                logger.info("Scraping meat section...")
                meat_businesses = await self.scrape_section('meat')
                businesses.extend(meat_businesses)
                
            else:
                # For other pages (like fish), use the original logic
                kosher_type = 'unknown'
                if 'fish' in category_url:
                    kosher_type = 'pareve'  # ORB fish are pareve
                
                listing_type = 'Businesses'
                logger.info(f"Category: {listing_type} » {kosher_type}")
                
                # Find all business listings
                business_elements = await self.page.query_selector_all('.business-listing')
                logger.info(f"Found {len(business_elements)} business listings")
                
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
    
    async def scrape_section(self, section_type: str) -> List[Dict]:
        """Scrape a specific section (dairy or meat) from the restaurants page."""
        try:
            # Look for the section header
            section_selector = f"h3:has-text('Restaurants » {section_type.capitalize()}')"
            
            # Find the section and get all business listings within it
            section_elements = await self.page.query_selector_all('.section-col-miami')
            
            businesses = []
            kosher_type = section_type.lower()
            
            for section in section_elements:
                # Check if this section contains the right header
                header = await section.query_selector('h3')
                if header:
                    header_text = await header.text_content()
                    if f'Restaurants » {section_type.capitalize()}' in header_text:
                        logger.info(f"Found {section_type} section")
                        
                        # Find all business listings in this section
                        business_elements = await section.query_selector_all('.business-listing')
                        logger.info(f"Found {len(business_elements)} {section_type} business listings")
                        
                        for business_element in business_elements:
                            try:
                                business_data = await self.extract_business_data(business_element, kosher_type, 'Restaurants')
                                if business_data:
                                    businesses.append(business_data)
                                    logger.info(f"Extracted: {business_data['name']} ({kosher_type})")
                            except Exception as e:
                                logger.error(f"Error processing business element: {e}")
                                continue
                        break
            
            return businesses
            
        except Exception as e:
            logger.error(f"Error scraping {section_type} section: {e}")
            return []
    
    async def scrape_all_categories(self) -> List[Dict]:
        """Scrape all available ORB categories."""
        try:
            # Define ORB category URLs
            category_urls = [
                f"{self.base_url}/category/restaurants/",  # Main restaurants page (contains dairy and meat sections)
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
            logger.info("Starting ORB Scraper V2 Preview Mode")
            
            # Setup Playwright
            if not await self.setup_playwright():
                return False
            
            # Scrape all categories
            businesses = await self.scrape_all_categories()
            
            if businesses:
                logger.info(f"Scraping completed. Found {len(businesses)} businesses")
                
                # Show sample results
                logger.info("Sample scraped businesses:")
                for i, business in enumerate(businesses[:10]):
                    logger.info(f"{i+1}. {business['name']} - {business['kosher_type']} - {business['address']}")
                
                # Show statistics
                kosher_types = {}
                for business in businesses:
                    kosher_type = business.get('kosher_type', 'unknown')
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
                
                # Show detailed breakdown by category
                logger.info("\nDetailed Breakdown by Category:")
                for kosher_type in ['dairy', 'meat', 'pareve']:
                    type_businesses = [b for b in businesses if b.get('kosher_type') == kosher_type]
                    logger.info(f"\n{kosher_type.upper()} RESTAURANTS ({len(type_businesses)}):")
                    for business in type_businesses:
                        logger.info(f"  - {business['name']}")
                
            else:
                logger.warning("No businesses were scraped")
            
            return True
            
        except Exception as e:
            logger.error(f"Scraper failed: {e}")
            return False
        finally:
            await self.cleanup()

async def main():
    """Main entry point."""
    scraper = ORBScraperV2Preview()
    success = await scraper.run()
    
    if success:
        print("\n✅ Preview scraping completed successfully!")
        print("Review the data above before deciding to save to database.")
    else:
        print("\n❌ Preview scraping failed!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 