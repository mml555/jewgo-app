#!/usr/bin/env python3
"""
Test ORB Category URLs
Check which ORB category URLs exist and work for different kosher types.
"""

import asyncio
import logging
from playwright.async_api import async_playwright

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_orb_categories():
    """Test different ORB category URLs to see which ones exist."""
    
    # Define potential category URLs to test
    category_urls = [
        # Dairy (confirmed working)
        "https://www.orbkosher.com/category/restaurants/",
        
        # Meat categories
        "https://www.orbkosher.com/category/restaurants-meat/",
        "https://www.orbkosher.com/category/meat-restaurants/",
        "https://www.orbkosher.com/category/meat/",
        "https://www.orbkosher.com/category/restaurants/meat/",
        
        # Pareve categories
        "https://www.orbkosher.com/category/restaurants-pareve/",
        "https://www.orbkosher.com/category/pareve-restaurants/",
        "https://www.orbkosher.com/category/pareve/",
        "https://www.orbkosher.com/category/restaurants/pareve/",
        
        # Fish categories
        "https://www.orbkosher.com/category/restaurants-fish/",
        "https://www.orbkosher.com/category/fish-restaurants/",
        "https://www.orbkosher.com/category/fish/",
        "https://www.orbkosher.com/category/restaurants/fish/",
        
        # Other categories
        "https://www.orbkosher.com/category/catering/",
        "https://www.orbkosher.com/category/markets/",
        "https://www.orbkosher.com/category/grocery/",
        "https://www.orbkosher.com/category/bakeries/",
    ]
    
    results = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Set user agent
        await page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        for url in category_urls:
            try:
                logger.info(f"Testing: {url}")
                
                # Navigate to page
                response = await page.goto(url, wait_until='networkidle', timeout=10000)
                
                if response.status == 200:
                    # Check if page has business listings
                    business_elements = await page.query_selector_all('.business-listing')
                    
                    # Get page title
                    title = await page.title()
                    
                    # Get category header
                    title_elem = await page.query_selector('.title_part h3')
                    category_header = await title_elem.inner_text() if title_elem else "No header found"
                    
                    result = {
                        'url': url,
                        'status': 'success',
                        'status_code': response.status,
                        'business_count': len(business_elements),
                        'title': title,
                        'category_header': category_header
                    }
                    
                    logger.info(f"✅ {url} - {len(business_elements)} businesses - {category_header}")
                    
                else:
                    result = {
                        'url': url,
                        'status': 'error',
                        'status_code': response.status,
                        'business_count': 0,
                        'title': 'Error',
                        'category_header': 'Not found'
                    }
                    
                    logger.warning(f"❌ {url} - Status {response.status}")
                    
            except Exception as e:
                result = {
                    'url': url,
                    'status': 'error',
                    'status_code': 0,
                    'business_count': 0,
                    'title': 'Error',
                    'category_header': str(e)
                }
                
                logger.error(f"❌ {url} - Error: {e}")
            
            results.append(result)
            
            # Be respectful with delays
            await asyncio.sleep(2)
        
        await browser.close()
    
    # Print summary
    print("\n" + "="*80)
    print("ORB CATEGORY URL TEST RESULTS")
    print("="*80)
    
    working_categories = []
    for result in results:
        if result['status'] == 'success' and result['business_count'] > 0:
            working_categories.append(result)
            print(f"✅ {result['url']}")
            print(f"   Businesses: {result['business_count']}")
            print(f"   Header: {result['category_header']}")
            print()
    
    print(f"Total working categories: {len(working_categories)}")
    print("="*80)
    
    return working_categories

async def main():
    """Main function."""
    print("🧪 Testing ORB Category URLs")
    print("="*50)
    
    working_categories = await test_orb_categories()
    
    if working_categories:
        print("\n✅ Found working ORB categories!")
        print("🔍 Ready to scrape additional kosher types.")
    else:
        print("\n❌ No additional categories found.")
    
    return working_categories

if __name__ == "__main__":
    asyncio.run(main()) 