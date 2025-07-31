#!/usr/bin/env python3
"""
Test ORB Scraper Logic
Simple test to verify the ORB scraper can extract restaurant information.
"""

import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def test_orb_scraping():
    """Test basic ORB scraping functionality."""
    try:
        print("Testing ORB scraper...")
        
        # Test basic connection to ORB website
        base_url = "https://www.orbkosher.com"
        url = f"{base_url}/category/restaurants/"
        
        print(f"Fetching: {url}")
        
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        response = session.get(url)
        response.raise_for_status()
        
        print(f"Response status: {response.status_code}")
        print(f"Content length: {len(response.content)}")
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for restaurant information
        print("\nLooking for restaurant data...")
        
        # Find all text that might be restaurant names
        text_elements = soup.find_all(text=True)
        restaurant_candidates = []
        
        for text in text_elements:
            text = text.strip()
            if len(text) > 3 and re.match(r'^[A-Z][a-zA-Z\s&\'-]+$', text):
                # This might be a restaurant name
                restaurant_candidates.append(text)
        
        print(f"Found {len(restaurant_candidates)} potential restaurant names:")
        for i, name in enumerate(restaurant_candidates[:10]):  # Show first 10
            print(f"  {i+1}. {name}")
        
        # Look for addresses
        address_candidates = []
        for text in text_elements:
            text = text.strip()
            if re.search(r'\d+.*(Street|Ave|Road|Blvd|St|Dr).*[A-Z]{2}\s\d{5}', text):
                address_candidates.append(text)
        
        print(f"\nFound {len(address_candidates)} potential addresses:")
        for i, addr in enumerate(address_candidates[:5]):  # Show first 5
            print(f"  {i+1}. {addr}")
        
        print("\nORB scraper test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error testing ORB scraper: {e}")
        return False

if __name__ == "__main__":
    test_orb_scraping() 