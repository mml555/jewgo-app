#!/usr/bin/env python3
"""
Fix Broken Website Links
Identifies and fixes various types of broken website links.
"""

import sqlite3
import re
from urllib.parse import urlparse

def find_broken_links():
    """Find various types of broken website links."""
    
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
    
    print("🔍 Finding Broken Website Links")
    print("=" * 60)
    
    # Patterns for broken links
    broken_patterns = [
        # Generic/placeholder domains
        (r'google\.com', 'Google homepage (not restaurant website)'),
        (r'youtube\.com', 'YouTube page (not restaurant website)'),
        (r'example\.com', 'Example domain'),
        (r'test\.com', 'Test domain'),
        (r'placeholder', 'Placeholder link'),
        
        # Common redirect/error pages
        (r'404', '404 error page'),
        (r'error', 'Error page'),
        (r'not-found', 'Not found page'),
        
        # Generic search engines
        (r'bing\.com', 'Bing search (not restaurant website)'),
        (r'yahoo\.com', 'Yahoo (not restaurant website)'),
        
        # Social media (already handled, but double-check)
        (r'facebook\.com', 'Facebook page'),
        (r'instagram\.com', 'Instagram page'),
        (r'twitter\.com', 'Twitter page'),
        
        # Third-party platforms (already handled, but double-check)
        (r'clover\.com', 'Clover ordering platform'),
        (r'toasttab\.com', 'Toast ordering platform'),
        (r'doordash\.com', 'DoorDash delivery'),
        (r'grubhub\.com', 'GrubHub delivery'),
        (r'ubereats\.com', 'UberEats delivery'),
    ]
    
    broken_links = []
    good_links = []
    
    for name, website, address in restaurants:
        if not website:
            continue
            
        # Check for broken patterns
        is_broken = False
        issue_type = ""
        
        for pattern, description in broken_patterns:
            if re.search(pattern, website, re.IGNORECASE):
                is_broken = True
                issue_type = description
                break
        
        # Additional checks
        if is_broken:
            broken_links.append({
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
    
    # Print results
    print(f"\n📊 Summary:")
    print(f"Total restaurants with websites: {len(restaurants)}")
    print(f"✅ Good links: {len(good_links)}")
    print(f"❌ Broken links: {len(broken_links)}")
    
    if broken_links:
        print(f"\n❌ Broken Links Found:")
        print("-" * 60)
        for item in broken_links:
            print(f"🍽️  {item['name']}")
            print(f"   🔗 {item['website']}")
            print(f"   ❌ Issue: {item['issue']}")
            print(f"   📍 {item['address']}")
            print()
    
    conn.close()
    return broken_links, good_links

def fix_broken_links():
    """Fix broken website links by removing them."""
    
    conn = sqlite3.connect('restaurants.db')
    cursor = conn.cursor()
    
    print("🔧 Fixing Broken Links")
    print("=" * 60)
    
    # Remove various types of broken links
    broken_patterns = [
        "website_link LIKE '%google.com%'",
        "website_link LIKE '%youtube.com%'",
        "website_link LIKE '%example.com%'",
        "website_link LIKE '%test.com%'",
        "website_link LIKE '%placeholder%'",
        "website_link LIKE '%404%'",
        "website_link LIKE '%error%'",
        "website_link LIKE '%not-found%'",
        "website_link LIKE '%bing.com%'",
        "website_link LIKE '%yahoo.com%'",
        "website_link LIKE '%facebook.com%'",
        "website_link LIKE '%instagram.com%'",
        "website_link LIKE '%twitter.com%'",
        "website_link LIKE '%clover.com%'",
        "website_link LIKE '%toasttab.com%'",
        "website_link LIKE '%doordash.com%'",
        "website_link LIKE '%grubhub.com%'",
        "website_link LIKE '%ubereats.com%'"
    ]
    
    # Build the WHERE clause
    where_clause = " OR ".join(broken_patterns)
    
    # Count before
    cursor.execute(f"SELECT COUNT(*) FROM restaurants WHERE {where_clause}")
    count_before = cursor.fetchone()[0]
    
    # Remove broken links
    cursor.execute(f"UPDATE restaurants SET website_link = NULL WHERE {where_clause}")
    
    # Count after
    cursor.execute(f"SELECT COUNT(*) FROM restaurants WHERE {where_clause}")
    count_after = cursor.fetchone()[0]
    
    # Get final counts
    cursor.execute("SELECT COUNT(*) FROM restaurants WHERE website_link IS NOT NULL AND website_link != ''")
    good_links = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM restaurants WHERE website_link IS NULL OR website_link = ''")
    no_website = cursor.fetchone()[0]
    
    print(f"✅ Fixed {count_before - count_after} broken links")
    print(f"📊 Final Status:")
    print(f"   • Restaurants with good websites: {good_links}")
    print(f"   • Restaurants with Google Maps fallback: {no_website}")
    print(f"   • Total restaurants: {good_links + no_website}")
    
    conn.commit()
    conn.close()

def verify_fixes():
    """Verify that broken links have been fixed."""
    
    conn = sqlite3.connect('restaurants.db')
    cursor = conn.cursor()
    
    print("\n✅ Verifying Fixes")
    print("=" * 60)
    
    # Check for any remaining broken patterns
    remaining_broken = cursor.execute("""
        SELECT name, website_link 
        FROM restaurants 
        WHERE website_link LIKE '%google.com%' 
           OR website_link LIKE '%youtube.com%'
           OR website_link LIKE '%example.com%'
           OR website_link LIKE '%test.com%'
           OR website_link LIKE '%placeholder%'
           OR website_link LIKE '%404%'
           OR website_link LIKE '%error%'
           OR website_link LIKE '%not-found%'
           OR website_link LIKE '%bing.com%'
           OR website_link LIKE '%yahoo.com%'
           OR website_link LIKE '%facebook.com%'
           OR website_link LIKE '%instagram.com%'
           OR website_link LIKE '%twitter.com%'
           OR website_link LIKE '%clover.com%'
           OR website_link LIKE '%toasttab.com%'
           OR website_link LIKE '%doordash.com%'
           OR website_link LIKE '%grubhub.com%'
           OR website_link LIKE '%ubereats.com%'
    """).fetchall()
    
    if remaining_broken:
        print("❌ Still found broken links:")
        for name, website in remaining_broken:
            print(f"   • {name}: {website}")
    else:
        print("✅ All broken links have been fixed!")
    
    # Show some good examples
    good_examples = cursor.execute("""
        SELECT name, website_link 
        FROM restaurants 
        WHERE website_link IS NOT NULL AND website_link != ''
        LIMIT 5
    """).fetchall()
    
    print(f"\n✅ Good Website Examples:")
    for name, website in good_examples:
        print(f"   • {name}: {website}")
    
    conn.close()

if __name__ == "__main__":
    print("🔍 Step 1: Finding broken links...")
    broken, good = find_broken_links()
    
    if broken:
        print(f"\n🔧 Step 2: Fixing {len(broken)} broken links...")
        fix_broken_links()
        
        print(f"\n✅ Step 3: Verifying fixes...")
        verify_fixes()
    else:
        print("✅ No broken links found!") 