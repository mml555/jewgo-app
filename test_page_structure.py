#!/usr/bin/env python3
"""
Test script to examine the page structure of ORB Kosher website.
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def test_page_structure():
    """Test the page structure to understand how to scrape it."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        
        url = "https://www.orbkosher.com/category/restaurants/"
        print(f"Loading page: {url}")
        
        driver.get(url)
        time.sleep(5)  # Wait for page to load
        
        # Get page source
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        
        print(f"Page title: {soup.title.string if soup.title else 'No title'}")
        
        # Look for different possible selectors
        selectors_to_try = [
            ".fusion-post-wrapper",
            ".restaurant-listing", 
            "article",
            ".listing-item",
            ".post",
            ".entry",
            "h2 a",
            "h3 a",
            "a[href*='/listings/']",
            "a[href*='/restaurant/']"
        ]
        
        print("\nTrying different selectors:")
        for selector in selectors_to_try:
            elements = soup.select(selector)
            print(f"  {selector}: {len(elements)} elements found")
            
            if elements:
                print(f"    First element: {elements[0]}")
                if hasattr(elements[0], 'text'):
                    print(f"    Text: {elements[0].text.strip()[:100]}...")
        
        # Look for any links that might be restaurant listings
        all_links = soup.find_all('a', href=True)
        restaurant_links = [link for link in all_links if '/listings/' in link.get('href', '') or '/restaurant/' in link.get('href', '')]
        
        print(f"\nRestaurant links found: {len(restaurant_links)}")
        for i, link in enumerate(restaurant_links[:5]):
            print(f"  {i+1}. {link.get('href')} - {link.text.strip()}")
        
        # Save page source for inspection
        with open('orb_page_source.html', 'w', encoding='utf-8') as f:
            f.write(page_source)
        print(f"\nPage source saved to: orb_page_source.html")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_page_structure() 