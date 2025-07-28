#!/usr/bin/env python3
"""
Check Website Links
Analyzes restaurant website links to identify problematic ones.
"""

import sqlite3
import re
from urllib.parse import urlparse

def check_website_links():
    """Check and categorize website links."""
    
    # Connect to database
    conn = sqlite3.connect('restaurants.db')
    cursor = conn.cursor()
    
    # Get all restaurants with websites
    cursor.execute("""
        SELECT name, website_link, address 
        FROM restaurants 
        WHERE website_link IS NOT NULL AND website_link != ''
        ORDER BY name
    """)
    
    restaurants = cursor.fetchall()
    
    print("🔍 Analyzing Website Links")
    print("=" * 60)
    
    # Categories for problematic links
    third_party_platforms = [
        'clover.com', 'toasttab.com', 'doordash.com', 'grubhub.com', 
        'ubereats.com', 'postmates.com', 'seamless.com', 'chownow.com',
        'squareup.com', 'online-ordering', 'order-online'
    ]
    
    social_media = [
        'facebook.com', 'instagram.com', 'twitter.com', 'youtube.com',
        'linkedin.com', 'tiktok.com'
    ]
    
    problematic_links = []
    good_links = []
    
    for name, website, address in restaurants:
        if not website:
            continue
            
        # Parse URL
        try:
            parsed = urlparse(website)
            domain = parsed.netloc.lower()
            
            # Check for problematic patterns
            is_problematic = False
            issue_type = ""
            
            # Check for third-party platforms
            for platform in third_party_platforms:
                if platform in domain or platform in website.lower():
                    is_problematic = True
                    issue_type = "Third-party ordering platform"
                    break
            
            # Check for social media
            for social in social_media:
                if social in domain:
                    is_problematic = True
                    issue_type = "Social media page"
                    break
            
            # Check for obvious issues
            if 'test' in domain or 'example' in domain:
                is_problematic = True
                issue_type = "Test/example domain"
            
            if is_problematic:
                problematic_links.append({
                    'name': name,
                    'website': website,
                    'issue': issue_type,
                    'address': address
                })
            else:
                good_links.append({
                    'name': name,
                    'website': website,
                    'address': address
                })
                
        except Exception as e:
            problematic_links.append({
                'name': name,
                'website': website,
                'issue': f"Invalid URL: {e}",
                'address': address
            })
    
    # Print results
    print(f"\n📊 Summary:")
    print(f"Total restaurants with websites: {len(restaurants)}")
    print(f"✅ Good links: {len(good_links)}")
    print(f"⚠️  Problematic links: {len(problematic_links)}")
    
    if problematic_links:
        print(f"\n⚠️  Problematic Links:")
        print("-" * 60)
        for item in problematic_links:
            print(f"🍽️  {item['name']}")
            print(f"   🔗 {item['website']}")
            print(f"   ❌ Issue: {item['issue']}")
            print(f"   📍 {item['address']}")
            print()
    
    print(f"\n✅ Good Links (first 10):")
    print("-" * 60)
    for item in good_links[:10]:
        print(f"🍽️  {item['name']}")
        print(f"   🔗 {item['website']}")
        print(f"   📍 {item['address']}")
        print()
    
    if len(good_links) > 10:
        print(f"... and {len(good_links) - 10} more good links")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    print("-" * 60)
    print("1. Remove links to third-party ordering platforms")
    print("2. Replace social media links with actual websites when possible")
    print("3. Consider using Google Maps links as fallback for problematic URLs")
    print("4. Validate all remaining links manually")
    
    conn.close()
    
    return problematic_links, good_links

def suggest_improvements():
    """Suggest improvements for website links."""
    
    print(f"\n🔧 Suggested Improvements:")
    print("=" * 60)
    
    # Example of how to update problematic links
    print("""
    # Example SQL to remove problematic links:
    
    -- Remove third-party ordering platforms
    UPDATE restaurants 
    SET website_link = NULL 
    WHERE website_link LIKE '%clover.com%' 
       OR website_link LIKE '%toasttab.com%'
       OR website_link LIKE '%doordash.com%';
    
    -- Remove social media links
    UPDATE restaurants 
    SET website_link = NULL 
    WHERE website_link LIKE '%facebook.com%'
       OR website_link LIKE '%instagram.com%';
    
    -- Remove test/example domains
    UPDATE restaurants 
    SET website_link = NULL 
    WHERE website_link LIKE '%test%'
       OR website_link LIKE '%example%';
    """)

if __name__ == "__main__":
    problematic, good = check_website_links()
    suggest_improvements() 