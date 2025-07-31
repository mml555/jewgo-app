#!/usr/bin/env python3
"""
Simple ORB Kosher Scraper with Neon PostgreSQL Integration
Uses requests and BeautifulSoup for compatibility with Python 3.13.
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
from bs4 import BeautifulSoup

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

class SimpleORBScraper:
    """Simple ORB Kosher scraper with database integration."""
    
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
    
    def get_page_content(self, url: str) -> Optional[BeautifulSoup]:
        """Get page content with error handling."""
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Add delay to be respectful
            time.sleep(2)
            
            return BeautifulSoup(response.content, 'html.parser')
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None
    
    def extract_text_by_label(self, soup: BeautifulSoup, label: str) -> Optional[str]:
        """Extract text by looking for a specific label."""
        try:
            # Look for the label in various formats
            patterns = [
                f"{label}:",
                f"{label}",
                f"{label.lower()}:",
                f"{label.lower()}"
            ]
            
            for pattern in patterns:
                # Find elements containing the label
                elements = soup.find_all(text=re.compile(re.escape(pattern), re.IGNORECASE))
                for element in elements:
                    parent = element.parent
                    if parent:
                        # Get the text after the label
                        text = parent.get_text()
                        if pattern in text:
                            # Extract text after the label
                            parts = text.split(pattern, 1)
                            if len(parts) > 1:
                                result = parts[1].strip()
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
                r'https?://[^\s]+',
                r'www\.[^\s]+',
                r'[^\s]+\.com',
                r'[^\s]+\.org',
                r'[^\s]+\.net'
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
    
    def extract_kosher_info(self, soup: BeautifulSoup) -> tuple:
        """Extract kosher type and extra kosher information."""
        try:
            kosher_type = None
            extra_info = []
            
            # Look for kosher type indicators
            kosher_indicators = [
                "Meat", "Dairy", "Parve", "Fleishig", "Milchig", "Pareve",
                "Glatt", "Cholov Yisroel", "Pas Yisroel", "Bishul Yisroel"
            ]
            
            # Get all text content
            text_content = soup.get_text().lower()
            
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
    
    def scrape_detail_page(self, detail_url: str) -> Optional[Dict]:
        """Scrape individual business detail page."""
        try:
            logger.info(f"Scraping detail page: {detail_url}")
            
            soup = self.get_page_content(detail_url)
            if not soup:
                return None
            
            # Extract basic information
            name = soup.find('h1')
            name = name.get_text().strip() if name else "Unknown"
            
            # Extract photo
            photo = None
            img_tag = soup.find('img')
            if img_tag and img_tag.get('src'):
                photo = urljoin(self.base_url, img_tag['src'])
            
            # Extract address
            address = self.extract_text_by_label(soup, "Address")
            
            # Extract phone
            phone = self.extract_text_by_label(soup, "Phone")
            
            # Extract website from text content
            website = None
            text_content = soup.get_text()
            website = self.extract_website_from_text(text_content)
            
            # Extract kosher information
            kosher_type, extra_kosher_info = self.extract_kosher_info(soup)
            
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
            
            soup = self.get_page_content(page_url)
            if not soup:
                return []
            
            businesses = []
            
            # Find business listings (adjust selectors based on actual page structure)
            listings = soup.find_all(['div', 'article'], class_=re.compile(r'listing|business|restaurant|item', re.IGNORECASE))
            
            if not listings:
                # Try alternative selectors
                listings = soup.find_all('a', href=re.compile(r'/restaurant/|/business/'))
            
            for listing in listings:
                try:
                    # Find the link to detail page
                    link = listing.find('a', href=True)
                    if not link:
                        continue
                    
                    detail_url = link['href']
                    if not detail_url.startswith('http'):
                        detail_url = urljoin(self.base_url, detail_url)
                    
                    # Get business name
                    name_elem = listing.find(['h2', 'h3', 'h4', 'strong'])
                    name = name_elem.get_text().strip() if name_elem else "Unknown"
                    
                    # Scrape detail page
                    business_data = self.scrape_detail_page(detail_url)
                    if business_data:
                        businesses.append(business_data)
                    
                    # Small delay between requests
                    time.sleep(1)
                    
                except Exception as e:
                    logger.warning(f"Error processing listing: {e}")
                    continue
            
            return businesses
            
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
    
    def scrape_all_pages(self, max_pages: int = 3):
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
    
    def run(self, max_pages: int = 3):
        """Main execution method."""
        try:
            logger.info("Starting Simple ORB Kosher scraper")
            
            # Setup
            self.setup_database()
            
            # Scrape
            self.scrape_all_pages(max_pages)
            
            # Cleanup
            self.cleanup()
            
            logger.info("Simple ORB Kosher scraper completed successfully")
            
        except Exception as e:
            logger.error(f"Scraper failed: {e}")
            self.cleanup()
            raise

def main():
    """Main entry point."""
    scraper = SimpleORBScraper()
    scraper.run(max_pages=2)  # Start with 2 pages

if __name__ == "__main__":
    main() 