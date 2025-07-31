#!/usr/bin/env python3
"""
Basic ORB Kosher Scraper with Neon PostgreSQL Integration
Uses only requests and regex parsing for maximum compatibility.
"""

import os
import re
import time
import logging
import requests
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('orb_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BasicORBScraper:
    """Basic ORB Kosher scraper with database integration."""
    
    def __init__(self):
        self.base_url = "https://www.orbkosher.com"
        self.category_url = f"{self.base_url}/category/restaurants/"
        self.db_url = os.getenv("DATABASE_URL")
        
        if not self.db_url:
            raise ValueError("DATABASE_URL environment variable not set")
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        self.db_conn = None
        self.db_cursor = None
        
    def setup_database(self):
        """Setup database connection and create table if needed."""
        try:
            self.db_conn = psycopg2.connect(self.db_url)
            self.db_cursor = self.db_conn.cursor()
            
            # Create table if it doesn't exist (now using restaurants table)
            self.db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS restaurants (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    address TEXT,
                    city TEXT,
                    state TEXT,
                    zip_code TEXT,
                    phone TEXT,
                    website TEXT,
                    cuisine_type TEXT,
                    price_range TEXT,
                    rating FLOAT,
                    review_count INTEGER,
                    google_rating FLOAT,
                    google_review_count INTEGER,
                    google_reviews TEXT,
                    latitude FLOAT,
                    longitude FLOAT,
                    hours TEXT,
                    description TEXT,
                    image_url TEXT,
                    is_kosher BOOLEAN DEFAULT FALSE,
                    is_glatt BOOLEAN DEFAULT FALSE,
                    is_cholov_yisroel BOOLEAN DEFAULT FALSE,
                    is_pas_yisroel BOOLEAN DEFAULT FALSE,
                    is_bishul_yisroel BOOLEAN DEFAULT FALSE,
                    is_mehadrin BOOLEAN DEFAULT FALSE,
                    is_hechsher BOOLEAN DEFAULT FALSE,
                    hechsher_details TEXT,
                    kosher_type TEXT,
                    kosher_cert_link TEXT,
                    detail_url TEXT,
                    short_description TEXT,
                    email TEXT,
                    google_listing_url TEXT,
                    hours_open TEXT,
                    category TEXT DEFAULT 'restaurant',
                    status TEXT DEFAULT 'approved',
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)
            self.db_conn.commit()
            logger.info("Database connection established and table created")
            
        except Exception as e:
            logger.error(f"Database setup failed: {e}")
            raise
    
    def get_page_content(self, url: str) -> Optional[str]:
        """Get page content with error handling."""
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Add delay to be respectful
            time.sleep(2)
            
            return response.text
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None
    
    def extract_text_by_label(self, html_content: str, label: str) -> Optional[str]:
        """Extract text by looking for a specific label using regex."""
        try:
            # Look for the label in various formats
            patterns = [
                rf'{re.escape(label)}:\s*([^<\n]+)',
                rf'{re.escape(label)}\s*([^<\n]+)',
                rf'{re.escape(label.lower())}:\s*([^<\n]+)',
                rf'{re.escape(label.lower())}\s*([^<\n]+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, html_content, re.IGNORECASE)
                if match:
                    result = match.group(1).strip()
                    if result:
                        return result
            
            return None
            
        except Exception as e:
            logger.warning(f"Error extracting text for label '{label}': {e}")
            return None
    
    def extract_website_from_text(self, text: str) -> Optional[str]:
        """Extract website URL from text content."""
        try:
            # Look for common website patterns
            url_patterns = [
                r'https?://[^\s<>]+',
                r'www\.[^\s<>]+',
                r'[^\s<>]+\.com',
                r'[^\s<>]+\.org',
                r'[^\s<>]+\.net'
            ]
            
            for pattern in url_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if not match.startswith(('http://', 'https://')):
                        match = 'https://' + match
                    return match
            
            return None
            
        except Exception as e:
            logger.warning(f"Error extracting website: {e}")
            return None
    
    def extract_kosher_info(self, html_content: str) -> tuple:
        """Extract kosher type and extra kosher information."""
        try:
            kosher_type = None
            extra_info = []
            
            # Look for kosher type indicators
            kosher_indicators = [
                "Meat", "Dairy", "Parve", "Fleishig", "Milchig", "Pareve",
                "Glatt", "Cholov Yisroel", "Pas Yisroel", "Bishul Yisroel"
            ]
            
            # Get all text content (remove HTML tags)
            text_content = re.sub(r'<[^>]+>', ' ', html_content).lower()
            
            # Check for kosher types
            for indicator in kosher_indicators:
                if indicator.lower() in text_content:
                    if kosher_type is None:
                        kosher_type = indicator
                    else:
                        extra_info.append(indicator)
            
            # Look for specific kosher requirements
            special_requirements = [
                "Cholov Yisroel", "Pas Yisroel", "Bishul Yisroel",
                "Mehadrin", "Hechsher", "Kosher Certified"
            ]
            
            for requirement in special_requirements:
                if requirement.lower() in text_content and requirement not in extra_info:
                    extra_info.append(requirement)
            
            extra_kosher_info = ", ".join(extra_info) if extra_info else None
            
            return kosher_type, extra_kosher_info
            
        except Exception as e:
            logger.warning(f"Error extracting kosher info: {e}")
            return None, None
    
    def extract_restaurants_from_page(self, html_content: str) -> List[Dict]:
        """Extract restaurant information directly from the listing page."""
        try:
            restaurants = []
            
            # Pattern to match restaurant listings
            # Look for spans with class "logoTitle" that contain restaurant names
            restaurant_pattern = r'<span[^>]*class=["\'][^"\']*logoTitle[^"\']*["\'][^>]*>([^<]+)</span>'
            name_matches = re.findall(restaurant_pattern, html_content)
            
            # Pattern to match addresses
            address_pattern = r'<span[^>]*class=["\'][^"\']*address[^"\']*["\'][^>]*>.*?<a[^>]*>([^<]+)</a>'
            address_matches = re.findall(address_pattern, html_content)
            
            # Pattern to match website links
            website_pattern = r'<a[^>]*title=["\']([^"\']+)["\'][^>]*href=["\']([^"\']+)["\'][^>]*target=["\']_blank["\'][^>]*>'
            website_matches = re.findall(website_pattern, html_content)
            
            # Pattern to match certificate links
            cert_pattern = r'<a[^>]*href=["\']([^"\']*\.pdf)["\'][^>]*title=["\']([^"\']+)["\'][^>]*>'
            cert_matches = re.findall(cert_pattern, html_content)
            
            logger.info(f"Found {len(name_matches)} restaurant names")
            logger.info(f"Found {len(address_matches)} addresses")
            logger.info(f"Found {len(website_matches)} website links")
            logger.info(f"Found {len(cert_matches)} certificate links")
            
            # Create restaurant data
            for i, name in enumerate(name_matches):
                if i < len(address_matches):
                    address = address_matches[i]
                else:
                    address = None
                
                # Find website for this restaurant
                website = None
                for website_name, website_url in website_matches:
                    if website_name.strip() == name.strip():
                        website = website_url
                        break
                
                # Find certificate for this restaurant
                cert_link = None
                for cert_url, cert_name in cert_matches:
                    if name.strip() in cert_name:
                        cert_link = urljoin(self.base_url, cert_url)
                        break
                
                restaurant_data = {
                    "name": name.strip(),
                    "detail_url": f"https://www.orbkosher.com/restaurant/{i+1}",  # Generate a URL
                    "category": "Restaurant",
                    "photo": None,  # No photos in this format
                    "address": address,
                    "phone": None,  # Phone not directly available
                    "website": website,
                    "kosher_cert_link": cert_link,
                    "kosher_type": "Kosher",  # All ORB restaurants are kosher
                    "extra_kosher_info": "ORB Certified"
                }
                
                restaurants.append(restaurant_data)
            
            return restaurants
            
        except Exception as e:
            logger.warning(f"Error extracting restaurants: {e}")
            return []
    
    def extract_name_from_page(self, html_content: str) -> str:
        """Extract business name from page content."""
        try:
            # Look for h1 tags
            h1_pattern = r'<h1[^>]*>([^<]+)</h1>'
            match = re.search(h1_pattern, html_content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
            
            # Look for title tags
            title_pattern = r'<title[^>]*>([^<]+)</title>'
            match = re.search(title_pattern, html_content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
            
            return "Unknown"
            
        except Exception as e:
            logger.warning(f"Error extracting name: {e}")
            return "Unknown"
    
    def extract_image_from_page(self, html_content: str) -> Optional[str]:
        """Extract image URL from page content."""
        try:
            # Look for img tags
            img_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
            match = re.search(img_pattern, html_content, re.IGNORECASE)
            if match:
                img_url = match.group(1)
                if not img_url.startswith('http'):
                    img_url = urljoin(self.base_url, img_url)
                return img_url
            
            return None
            
        except Exception as e:
            logger.warning(f"Error extracting image: {e}")
            return None
    
    def scrape_detail_page(self, detail_url: str) -> Optional[Dict]:
        """Scrape individual business detail page."""
        try:
            logger.info(f"Scraping detail page: {detail_url}")
            
            html_content = self.get_page_content(detail_url)
            if not html_content:
                return None
            
            # Extract basic information
            name = self.extract_name_from_page(html_content)
            
            # Extract photo
            photo = self.extract_image_from_page(html_content)
            
            # Extract address
            address = self.extract_text_by_label(html_content, "Address")
            
            # Extract phone
            phone = self.extract_text_by_label(html_content, "Phone")
            
            # Extract website from text content
            website = self.extract_website_from_text(html_content)
            
            # Extract kosher information
            kosher_type, extra_kosher_info = self.extract_kosher_info(html_content)
            
            # Kosher cert link is the same as detail URL
            kosher_cert_link = detail_url
            
            return {
                "name": name,
                "detail_url": detail_url,
                "category": "Restaurant",
                "photo": photo,
                "address": address,
                "phone": phone,
                "website": website,
                "kosher_cert_link": kosher_cert_link,
                "kosher_type": kosher_type,
                "extra_kosher_info": extra_kosher_info
            }
            
        except Exception as e:
            logger.error(f"Error scraping detail page {detail_url}: {e}")
            return None
    
    def scrape_listing_page(self, page_url: str) -> List[Dict]:
        """Scrape a listing page and return business data."""
        try:
            logger.info(f"Scraping listing page: {page_url}")
            
            html_content = self.get_page_content(page_url)
            if not html_content:
                return []
            
            # Extract restaurants directly from the listing page
            restaurants = self.extract_restaurants_from_page(html_content)
            
            logger.info(f"Found {len(restaurants)} restaurants on the page")
            
            return restaurants
            
        except Exception as e:
            logger.error(f"Error scraping listing page {page_url}: {e}")
            return []
    
    def insert_business(self, business_data: Dict) -> bool:
        """Insert business data into database."""
        try:
            self.db_cursor.execute("""
                INSERT INTO restaurants (
                    name, detail_url, category, image_url,
                    address, phone, website, kosher_cert_link,
                    kosher_type, hechsher_details, is_kosher, is_hechsher
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (detail_url) DO NOTHING;
            """, (
                business_data["name"],
                business_data["detail_url"],
                business_data["category"],
                business_data["photo"],
                business_data["address"],
                business_data["phone"],
                business_data["website"],
                business_data["kosher_cert_link"],
                business_data["kosher_type"],
                business_data["extra_kosher_info"],
                True,  # is_kosher
                True   # is_hechsher
            ))
            
            self.db_conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error inserting business data: {e}")
            self.db_conn.rollback()
            return False
    
    def scrape_all_pages(self, max_pages: int = 2):
        """Scrape all pages with pagination."""
        try:
            page_num = 1
            total_businesses = 0
            
            while page_num <= max_pages:
                if page_num == 1:
                    page_url = self.category_url
                else:
                    page_url = f"{self.category_url}page/{page_num}/"
                
                logger.info(f"Scraping page {page_num}: {page_url}")
                
                businesses = self.scrape_listing_page(page_url)
                
                if not businesses:
                    logger.info(f"No businesses found on page {page_num}, stopping pagination")
                    break
                
                # Insert businesses into database
                for business in businesses:
                    if self.insert_business(business):
                        total_businesses += 1
                        logger.info(f"Inserted: {business['name']}")
                    else:
                        logger.warning(f"Failed to insert: {business['name']}")
                
                page_num += 1
                
                # Delay between pages
                time.sleep(3)
            
            logger.info(f"Scraping completed. Total businesses processed: {total_businesses}")
            
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
    
    def cleanup(self):
        """Cleanup resources."""
        try:
            if self.db_cursor:
                self.db_cursor.close()
            if self.db_conn:
                self.db_conn.close()
            if self.session:
                self.session.close()
            
            logger.info("Cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def run(self, max_pages: int = 2):
        """Main execution method."""
        try:
            logger.info("Starting Basic ORB Kosher scraper")
            
            # Setup
            self.setup_database()
            
            # Scrape
            self.scrape_all_pages(max_pages)
            
            # Cleanup
            self.cleanup()
            
            logger.info("Basic ORB Kosher scraper completed successfully")
            
        except Exception as e:
            logger.error(f"Scraper failed: {e}")
            self.cleanup()
            raise

def main():
    """Main entry point."""
    scraper = BasicORBScraper()
    scraper.run(max_pages=1)  # Start with 1 page

if __name__ == "__main__":
    main() 