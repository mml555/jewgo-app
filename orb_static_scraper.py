#!/usr/bin/env python3
"""
ORB Kosher Static DOM Scraper
Extracts data from ORB Kosher category listing pages using DOM structure.
Infers kosher type and listing type from page headers.
"""

import os
import sys
import asyncio
import logging
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional, Tuple
import re

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database_manager_v3 import EnhancedDatabaseManager as DatabaseManager

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ORBStaticScraper:
    """Static DOM-based ORB Kosher scraper."""
    
    def __init__(self):
        self.base_url = "https://www.orbkosher.com"
        self.db_manager = DatabaseManager()
        
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
                    kosher_type = parts[1].strip()
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
    
    def extract_business_data(self, business_element, kosher_type: str, listing_type: str) -> Optional[Dict]:
        """Extract business data from a single .business-listing element."""
        try:
            # Extract name
            name_elem = business_element.query_selector('.logoTitle')
            name = name_elem.inner_text().strip() if name_elem else None
            
            if not name:
                logger.warning("No name found for business listing")
                return None
            
            # Extract photo
            img_elem = business_element.query_selector('a img')
            photo = None
            if img_elem:
                photo_src = img_elem.get_attribute('src')
                photo = self.normalize_url(photo_src) if photo_src else None
            
            # Extract phone
            phone_elem = business_element.query_selector('.phone a[href^="tel:"]')
            phone = phone_elem.inner_text().strip() if phone_elem else None
            
            # Extract address (real address, not PDF link)
            address_elem = business_element.query_selector('.address a:not([href$=".pdf"])')
            address = address_elem.inner_text().strip() if address_elem else None
            
            # Extract website
            website_elem = business_element.query_selector('a[href^="http"]')
            website = None
            if website_elem:
                website_href = website_elem.get_attribute('href')
                website = website_href if website_href else None
            
            # Extract kosher certificate link
            cert_elem = business_element.query_selector('.address a[href$=".pdf"]')
            kosher_cert_link = None
            if cert_elem:
                cert_href = cert_elem.get_attribute('href')
                kosher_cert_link = self.normalize_url(cert_href) if cert_href else None
            
            # Create business data record
            business_data = {
                'name': name,
                'photo': photo,
                'address': address,
                'phone': phone,
                'website': website,
                'kosher_cert_link': kosher_cert_link,
                'kosher_type': kosher_type.lower(),  # Normalize to lowercase
                'listing_type': listing_type,
                'detail_url': website,  # Use website as detail_url
                'source': 'orb'
            }
            
            logger.info(f"Extracted: {name} ({kosher_type})")
            return business_data
            
        except Exception as e:
            logger.error(f"Error extracting business data: {e}")
            return None
    
    async def scrape_category_page(self, category_url: str) -> List[Dict]:
        """Scrape a single category page."""
        try:
            logger.info(f"Scraping category page: {category_url}")
            
            # Navigate to page
            await self.page.goto(category_url, wait_until='networkidle')
            await asyncio.sleep(2)  # Wait for content to load
            
            # Extract listing type and kosher type from header
            title_elem = await self.page.query_selector('.title_part h3')
            title_text = await title_elem.inner_text() if title_elem else ""
            
            listing_type, kosher_type = self.extract_listing_and_kosher_type(title_text)
            logger.info(f"Category: {listing_type} » {kosher_type}")
            
            # Find all business listings
            business_elements = await self.page.query_selector_all('.business-listing')
            logger.info(f"Found {len(business_elements)} business listings")
            
            businesses = []
            for business_elem in business_elements:
                business_data = self.extract_business_data(business_elem, kosher_type, listing_type)
                if business_data:
                    businesses.append(business_data)
            
            return businesses
            
        except Exception as e:
            logger.error(f"Error scraping category page {category_url}: {e}")
            return []
    
    def save_businesses_to_database(self, businesses: List[Dict]) -> int:
        """Save scraped businesses to database."""
        try:
            logger.info(f"Saving {len(businesses)} businesses to database")
            
            success_count = 0
            for business in businesses:
                try:
                    # Check if business already exists
                    existing = self.db_manager.get_restaurant_by_name(business['name'])
                    
                    if existing:
                        # Update existing business
                        success = self.db_manager.update_restaurant_orb_data(
                            existing['id'],
                            business['address'],
                            business['kosher_type'],
                            'ORB Kosher',
                            business.get('extra_kosher_info')
                        )
                        if success:
                            logger.info(f"Updated existing business: {business['name']}")
                            success_count += 1
                    else:
                        # Create new business
                        success = self.db_manager.add_restaurant_simple(
                            name=business['name'],
                            address=business['address'],
                            phone_number=business.get('phone'),
                            kosher_type=business['kosher_type'],
                            certifying_agency='ORB Kosher',
                            extra_kosher_info=business.get('extra_kosher_info'),
                            source='orb'
                        )
                        if success:
                            logger.info(f"Added new business: {business['name']}")
                            success_count += 1
                    
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
                f"{self.base_url}/category/restaurants/",
                # Add more categories as needed
                # f"{self.base_url}/category/catering/",
                # f"{self.base_url}/category/markets/",
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
            logger.info("Starting ORB Static Scraper")
            
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
                    logger.info(f"{i+1}. {business['name']} - {business['kosher_type']} - {business['address']}")
            
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
    scraper = ORBStaticScraper()
    success = await scraper.run()
    
    if success:
        logger.info("ORB Static Scraper completed successfully")
    else:
        logger.error("ORB Static Scraper failed")
    
    return success

if __name__ == "__main__":
    asyncio.run(main()) 