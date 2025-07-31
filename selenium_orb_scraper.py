#!/usr/bin/env python3
"""
Selenium-based ORB Kosher Restaurant Scraper
Scrapes kosher restaurant data from ORB Kosher website using Selenium.
"""

import os
import json
import time
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

class SeleniumORBScraper:
    """Selenium-based scraper for ORB Kosher restaurant data."""
    
    def __init__(self):
        """Initialize the scraper."""
        self.scraped_data = []
        self.driver = None
    
    def setup_driver(self):
        """Setup Chrome driver with options."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
        except Exception as e:
            print(f"Error setting up Chrome driver: {e}")
            print("Make sure Chrome is installed and chromedriver is in PATH")
            return False
        
        return True
    
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
    
    def scrape_restaurant_details(self, detail_url: str) -> Dict[str, Any]:
        """Scrape detailed information from a restaurant's detail page."""
        try:
            self.driver.get(detail_url)
            time.sleep(2)  # Allow page to load
            
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            
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
            print(f"Error scraping restaurant details: {str(e)}")
            return {
                'address': '',
                'phone': '',
                'website': '',
                'kosher_type': 'Restaurant',
                'extra_info': '',
                'image_url': '',
                'description': 'Kosher restaurant certified by ORB'
            }
    
    def extract_restaurant_from_listing(self, listing_div) -> Dict[str, Any]:
        """Extract restaurant information from a business listing div."""
        try:
            # Extract restaurant name
            name_elem = listing_div.select_one("a[title]")
            if not name_elem:
                return None
            
            name = name_elem.get('title', '').strip()
            if not name:
                return None
            
            # Extract website URL
            website = name_elem.get('href', '') if name_elem.get('href') else ''
            
            # Extract phone number
            phone_elem = listing_div.select_one("a[onclick*='getClick']")
            phone = ''
            if phone_elem:
                phone_text = phone_elem.get_text().strip()
                phone = self.extract_phone_number(phone_text)
            
            # Extract address
            address_elem = listing_div.select_one("a[data-clipboard-text]")
            address = ''
            if address_elem:
                address = address_elem.get('data-clipboard-text', '').strip()
            
            # Extract address components
            address_components = self.extract_address_components(address)
            
            # Determine kosher type from the page context
            kosher_type = 'Restaurant'  # Default
            
            # Create restaurant data
            restaurant_data = {
                'name': name,
                'address': address,
                'city': address_components['city'],
                'state': address_components['state'],
                'zip_code': address_components['zip_code'],
                'phone': phone,
                'website': website,
                'cuisine_type': kosher_type,
                'description': f'Kosher restaurant certified by ORB',
                'image_url': '',
                'hechsher_details': 'ORB Kosher',
                'is_kosher': True,
                'is_glatt': False,
                'is_cholov_yisroel': False,
                'is_pas_yisroel': False,
                'is_bishul_yisroel': False,
                'is_mehadrin': False,
                'is_hechsher': True,
                'rating': 4.0,  # Default rating for ORB restaurants
                'review_count': 0,
                'price_range': '$$',  # Default price range
                'hours': 'Hours vary by location',
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            return restaurant_data
            
        except Exception as e:
            print(f"Error extracting restaurant from listing: {str(e)}")
            return None
    
    def scrape_orb_category(self, category_url: str, category_name: str = "Restaurant") -> List[Dict[str, Any]]:
        """Scrape all restaurants from a category page."""
        all_data = []
        
        try:
            self.driver.get(category_url)
            time.sleep(3)  # Allow page to load
            
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            
            # Find restaurant listings using the correct selector
            listings = soup.select(".business-listing")
            
            print(f"Found {len(listings)} restaurant listings")
            
            for listing in listings:
                try:
                    restaurant_data = self.extract_restaurant_from_listing(listing)
                    
                    if restaurant_data:
                        # Skip if we already have this restaurant
                        if any(item['name'] == restaurant_data['name'] for item in all_data):
                            continue
                        
                        print(f"Scraped: {restaurant_data['name']}")
                        all_data.append(restaurant_data)
                        
                except Exception as e:
                    print(f"Error processing restaurant listing: {str(e)}")
                    continue
            
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
        
        print(f"Scraped {len(all_data)} restaurants from {category_name}")
        return all_data
    
    def scrape_all_categories(self) -> List[Dict[str, Any]]:
        """Scrape all restaurant categories from ORB Kosher."""
        categories = [
            {
                'url': 'https://www.orbkosher.com/category/restaurants/',
                'name': 'Restaurant'
            }
        ]
        
        all_restaurants = []
        
        for category in categories:
            print(f"Starting to scrape category: {category['name']}")
            
            try:
                restaurants = self.scrape_orb_category(
                    category['url'],
                    category['name']
                )
                
                if restaurants:
                    all_restaurants.extend(restaurants)
                
            except Exception as e:
                print(f"Error scraping category {category['name']}: {str(e)}")
                continue
        
        return all_restaurants
    
    def save_to_json(self, restaurants: List[Dict[str, Any]], filename: str = None):
        """Save scraped data to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"orb_restaurants_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(restaurants, f, indent=2, default=str)
        
        print(f"Saved {len(restaurants)} restaurants to {filename}")
        return filename
    
    def close(self):
        """Close the browser driver."""
        if self.driver:
            self.driver.quit()

def main():
    """Main function to run the scraper."""
    scraper = None
    try:
        scraper = SeleniumORBScraper()
        
        print("Starting ORB Kosher restaurant scraping with Selenium")
        print("=" * 60)
        
        # Setup driver
        if not scraper.setup_driver():
            print("Failed to setup Chrome driver. Exiting.")
            return
        
        # Scrape all categories
        restaurants = scraper.scrape_all_categories()
        
        if restaurants:
            # Save to JSON
            filename = scraper.save_to_json(restaurants)
            
            print(f"\nScraping completed successfully!")
            print(f"Total restaurants scraped: {len(restaurants)}")
            print(f"Data saved to: {filename}")
            
            # Show sample data
            print("\nSample restaurant data:")
            print("-" * 30)
            for i, restaurant in enumerate(restaurants[:3], 1):
                print(f"\n{i}. {restaurant['name']}")
                print(f"   Address: {restaurant['address']}")
                print(f"   Phone: {restaurant['phone']}")
                print(f"   City: {restaurant['city']}")
                print(f"   Website: {restaurant['website']}")
        
        else:
            print("No restaurants found during scraping")
        
    except Exception as e:
        print(f"Error in main scraper function: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    main() 