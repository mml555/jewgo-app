#!/usr/bin/env python3
"""
Check Certifying Agency
======================

This script checks the certifying agency field and related data in the restaurant records.

Author: JewGo Development Team
Version: 1.0
"""

import requests
import json
import re

def check_certifying_agency():
    """Check the certifying agency field and related data."""
    
    backend_url = "https://jewgo.onrender.com/api/restaurants?limit=10"
    
    print("🔍 Checking Certifying Agency Data")
    print("=" * 40)
    print(f"URL: {backend_url}")
    print()
    
    try:
        response = requests.get(backend_url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'restaurants' in data:
                restaurants = data['restaurants']
                print(f"Found {len(restaurants)} restaurants")
                print()
                
                # Check what fields are available
                if restaurants:
                    first_restaurant = restaurants[0]
                    print("Available fields in restaurant data:")
                    for key, value in first_restaurant.items():
                        print(f"  - {key}: {type(value).__name__} = {str(value)[:50]}{'...' if len(str(value)) > 50 else ''}")
                    
                    print()
                    print("Certifying Agency Related Fields:")
                    
                    # Check for certifying_agency field
                    if 'certifying_agency' in first_restaurant:
                        print(f"  ✅ certifying_agency: {first_restaurant['certifying_agency']}")
                    else:
                        print(f"  ❌ certifying_agency: NOT FOUND")
                    
                    # Check for kosher_cert_link
                    if 'kosher_cert_link' in first_restaurant:
                        cert_link = first_restaurant['kosher_cert_link']
                        print(f"  ✅ kosher_cert_link: {cert_link}")
                        
                        # Try to extract agency from the link
                        if cert_link:
                            agency = extract_agency_from_link(cert_link)
                            print(f"  📋 Extracted agency from link: {agency}")
                    else:
                        print(f"  ❌ kosher_cert_link: NOT FOUND")
                    
                    # Check for kosher_category
                    if 'kosher_category' in first_restaurant:
                        print(f"  ✅ kosher_category: {first_restaurant['kosher_category']}")
                    else:
                        print(f"  ❌ kosher_category: NOT FOUND")
                    
                    # Check for kosher_type
                    if 'kosher_type' in first_restaurant:
                        print(f"  ✅ kosher_type: {first_restaurant['kosher_type']}")
                    else:
                        print(f"  ❌ kosher_type: NOT FOUND")
                    
                    print()
                    print("Sample Restaurant Data:")
                    print(f"  Name: {first_restaurant.get('name', 'N/A')}")
                    print(f"  Address: {first_restaurant.get('address', 'N/A')}")
                    print(f"  State: {first_restaurant.get('state', 'N/A')}")
                    print(f"  Kosher Category: {first_restaurant.get('kosher_category', 'N/A')}")
                    print(f"  Kosher Type: {first_restaurant.get('kosher_type', 'N/A')}")
                    print(f"  Cert Link: {first_restaurant.get('kosher_cert_link', 'N/A')}")
                    
                    # Check a few more restaurants for patterns
                    print()
                    print("Certifying Agency Patterns (first 5 restaurants):")
                    for i, restaurant in enumerate(restaurants[:5], 1):
                        cert_link = restaurant.get('kosher_cert_link', '')
                        agency = extract_agency_from_link(cert_link) if cert_link else 'No link'
                        print(f"  {i}. {restaurant.get('name', 'N/A')}: {agency}")
                        
        else:
            print(f"❌ API error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

def extract_agency_from_link(cert_link):
    """Extract certifying agency from certificate link."""
    if not cert_link:
        return "No link"
    
    # Common patterns in ORB links
    if 'orbkosher.com' in cert_link:
        return "ORB"
    elif 'oukosher.org' in cert_link:
        return "OU"
    elif 'crcweb.org' in cert_link:
        return "CRC"
    elif 'star-k.org' in cert_link:
        return "Star-K"
    elif 'ok.org' in cert_link:
        return "OK"
    elif 'kof-k.org' in cert_link:
        return "Kof-K"
    elif 'chabad.org' in cert_link:
        return "Chabad"
    else:
        # Try to extract from the filename
        filename = cert_link.split('/')[-1] if '/' in cert_link else cert_link
        if filename and '.' in filename:
            # Remove file extension and try to extract agency
            name_without_ext = filename.split('.')[0]
            # Look for common agency patterns
            if any(agency in name_without_ext.upper() for agency in ['ORB', 'OU', 'CRC', 'STAR', 'OK', 'KOF']):
                return name_without_ext
        return "Unknown"

if __name__ == "__main__":
    check_certifying_agency()
    print("\n🎉 Certifying agency check completed!") 