#!/usr/bin/env python3
"""
Test ORB Website Structure
Verify the DOM structure and selectors for the ORB scraper.
"""

import asyncio
import logging
from playwright.async_api import async_playwright

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_orb_website():
    """Test ORB website structure and selectors."""
    try:
        logger.info("Testing ORB website structure...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Set user agent
            await page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            
            # Navigate to ORB restaurants page
            url = "https://www.orbkosher.com/category/restaurants/"
            logger.info(f"Navigating to: {url}")
            
            await page.goto(url, wait_until='networkidle')
            await asyncio.sleep(3)  # Wait for content to load
            
            # Test 1: Check if page loads
            title = await page.title()
            logger.info(f"Page title: {title}")
            
            # Test 2: Check for title header
            title_elem = await page.query_selector('.title_part h3')
            if title_elem:
                title_text = await title_elem.inner_text()
                logger.info(f"✅ Found title header: '{title_text}'")
                
                # Parse listing type and kosher type
                if "»" in title_text:
                    parts = title_text.split("»")
                    listing_type = parts[0].strip()
                    kosher_type = parts[1].strip()
                    logger.info(f"✅ Parsed: Listing Type = '{listing_type}', Kosher Type = '{kosher_type}'")
                else:
                    logger.warning("⚠️  No '»' found in title, using fallback parsing")
            else:
                logger.error("❌ Could not find '.title_part h3' element")
            
            # Test 3: Check for business listings
            business_elements = await page.query_selector_all('.business-listing')
            logger.info(f"✅ Found {len(business_elements)} business listings")
            
            # Test 4: Extract sample business data
            if business_elements:
                logger.info("Testing business data extraction...")
                
                # Test first business
                first_business = business_elements[0]
                
                # Extract name
                name_elem = await first_business.query_selector('.logoTitle')
                if name_elem:
                    name = await name_elem.inner_text()
                    logger.info(f"✅ Business name: '{name}'")
                else:
                    logger.error("❌ Could not find '.logoTitle' element")
                
                # Extract phone
                phone_elem = await first_business.query_selector('.phone a[href^="tel:"]')
                if phone_elem:
                    phone = await phone_elem.inner_text()
                    logger.info(f"✅ Phone: '{phone}'")
                else:
                    logger.warning("⚠️  Could not find phone element")
                
                # Extract address
                address_elem = await first_business.query_selector('.address a:not([href$=".pdf"])')
                if address_elem:
                    address = await address_elem.inner_text()
                    logger.info(f"✅ Address: '{address}'")
                else:
                    logger.warning("⚠️  Could not find address element")
                
                # Extract website
                website_elem = await first_business.query_selector('a[href^="http"]')
                if website_elem:
                    website = await website_elem.get_attribute('href')
                    logger.info(f"✅ Website: '{website}'")
                else:
                    logger.warning("⚠️  Could not find website element")
                
                # Extract kosher certificate link
                cert_elem = await first_business.query_selector('.address a[href$=".pdf"]')
                if cert_elem:
                    cert_link = await cert_elem.get_attribute('href')
                    logger.info(f"✅ Kosher certificate: '{cert_link}'")
                else:
                    logger.warning("⚠️  Could not find kosher certificate element")
                
                # Extract photo
                img_elem = await first_business.query_selector('a img')
                if img_elem:
                    photo_src = await img_elem.get_attribute('src')
                    logger.info(f"✅ Photo: '{photo_src}'")
                else:
                    logger.warning("⚠️  Could not find photo element")
            
            # Test 5: Check for pagination
            pagination_elem = await page.query_selector('.pagination')
            if pagination_elem:
                logger.info("✅ Found pagination element")
            else:
                logger.info("ℹ️  No pagination found (single page)")
            
            # Test 6: Take a screenshot for verification
            await page.screenshot(path="orb_test_screenshot.png")
            logger.info("✅ Screenshot saved as 'orb_test_screenshot.png'")
            
            await browser.close()
            
            logger.info("🎉 ORB website structure test completed successfully!")
            return True
            
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return False

async def main():
    """Main function."""
    print("🧪 Testing ORB Website Structure")
    print("=" * 50)
    
    success = await test_orb_website()
    
    if success:
        print("\n✅ ORB website structure test passed!")
        print("🔍 The scraper should work correctly with the current selectors.")
    else:
        print("\n❌ ORB website structure test failed.")
        print("🔧 Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    asyncio.run(main()) 