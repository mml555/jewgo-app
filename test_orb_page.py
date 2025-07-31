#!/usr/bin/env python3
"""
Test script to examine ORB Kosher website structure
"""

import requests
import re

def test_orb_page():
    """Test the ORB Kosher restaurant page structure."""
    url = "https://www.orbkosher.com/category/restaurants/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        print(f"Fetching: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        html_content = response.text
        
        print(f"Page size: {len(html_content)} characters")
        print(f"Status code: {response.status_code}")
        
        # Look for any links
        href_pattern = r'href=["\']([^"\']+)["\']'
        all_links = re.findall(href_pattern, html_content)
        
        print(f"\nTotal links found: {len(all_links)}")
        
        # Show first 20 links
        print("\nFirst 20 links:")
        for i, link in enumerate(all_links[:20]):
            print(f"{i+1}. {link}")
        
        # Look for restaurant-related content
        restaurant_keywords = ['restaurant', 'kosher', 'food', 'dining', 'cafe', 'bakery']
        
        print(f"\nLooking for restaurant-related content...")
        for keyword in restaurant_keywords:
            count = html_content.lower().count(keyword)
            if count > 0:
                print(f"'{keyword}' appears {count} times")
        
        # Look for common HTML patterns
        print(f"\nHTML structure analysis:")
        print(f"<h1> tags: {len(re.findall(r'<h1[^>]*>', html_content))}")
        print(f"<h2> tags: {len(re.findall(r'<h2[^>]*>', html_content))}")
        print(f"<h3> tags: {len(re.findall(r'<h3[^>]*>', html_content))}")
        print(f"<article> tags: {len(re.findall(r'<article[^>]*>', html_content))}")
        print(f"<div> tags: {len(re.findall(r'<div[^>]*>', html_content))}")
        
        # Save a larger sample of the HTML for inspection
        with open('orb_page_full.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\nSaved full HTML to 'orb_page_full.html'")
        
        # Look for any text that might be restaurant names
        print(f"\nLooking for potential restaurant names...")
        
        # Look for text that might be restaurant names (capitalized words)
        name_pattern = r'>([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)<'
        potential_names = re.findall(name_pattern, html_content)
        
        # Filter for likely restaurant names
        restaurant_names = []
        for name in potential_names:
            if len(name) > 3 and any(keyword in name.lower() for keyword in ['restaurant', 'cafe', 'bakery', 'deli', 'pizza', 'grill']):
                restaurant_names.append(name)
        
        print(f"Potential restaurant names found: {len(restaurant_names)}")
        for i, name in enumerate(restaurant_names[:10]):
            print(f"{i+1}. {name}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_orb_page() 