#!/usr/bin/env python3
"""
Remove Duplicates via API Script
================================

This script removes duplicate restaurants by using the existing API endpoints.
It identifies duplicates and removes them through the database.

Author: JewGo Development Team
Version: 1.0
Last Updated: 2024
"""

import requests
import json
from collections import defaultdict

def get_all_restaurants():
    """Get all restaurants from the API."""
    url = "https://jewgo.onrender.com/api/restaurants?limit=1000"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('restaurants', [])
    else:
        print(f"Error getting restaurants: {response.status_code}")
        return []

def find_duplicates(restaurants):
    """Find duplicate restaurants by name."""
    name_groups = defaultdict(list)
    
    for restaurant in restaurants:
        name = restaurant.get('name', '')
        if name:
            name_groups[name].append(restaurant)
    
    duplicates = {}
    for name, group in name_groups.items():
        if len(group) > 1:
            duplicates[name] = group
    
    return duplicates

def remove_duplicates_via_direct_api():
    """Remove duplicates by calling the database directly."""
    print("🔍 Finding duplicates...")
    
    # Get all restaurants
    restaurants = get_all_restaurants()
    print(f"📊 Total restaurants: {len(restaurants)}")
    
    # Find duplicates
    duplicates = find_duplicates(restaurants)
    
    if not duplicates:
        print("✅ No duplicates found!")
        return
    
    print(f"🚨 Found {len(duplicates)} restaurants with duplicates:")
    
    total_removed = 0
    removed_details = []
    
    for name, group in duplicates.items():
        print(f"\n📝 Restaurant: {name}")
        print(f"   - Total entries: {len(group)}")
        
        # Sort by ID to keep the oldest (lowest ID)
        group.sort(key=lambda x: x.get('id', 0))
        
        # Keep the first (oldest) entry
        keep_restaurant = group[0]
        remove_restaurants = group[1:]
        
        print(f"   - Keeping ID: {keep_restaurant.get('id')}")
        print(f"   - Removing IDs: {[r.get('id') for r in remove_restaurants]}")
        
        # Remove duplicates by calling the database directly
        # Since we don't have a direct delete endpoint, we'll use a workaround
        # We'll create a simple SQL script that can be run
        
        removed_details.append({
            'name': name,
            'kept_id': keep_restaurant.get('id'),
            'removed_ids': [r.get('id') for r in remove_restaurants],
            'total_duplicates': len(group)
        })
        
        total_removed += len(remove_restaurants)
    
    print(f"\n📋 Summary:")
    print(f"   - Restaurants with duplicates: {len(duplicates)}")
    print(f"   - Total entries to remove: {total_removed}")
    print(f"   - Remaining restaurants after cleanup: {len(restaurants) - total_removed}")
    
    # Create SQL script for manual execution
    create_sql_script(removed_details)
    
    return removed_details

def create_sql_script(removed_details):
    """Create a SQL script to remove duplicates."""
    sql_script = """-- Remove Duplicate Restaurants SQL Script
-- Generated automatically by remove_duplicates_via_api.py

"""
    
    for detail in removed_details:
        name = detail['name']
        removed_ids = detail['removed_ids']
        
        sql_script += f"-- Remove duplicates for: {name}\n"
        for restaurant_id in removed_ids:
            sql_script += f"DELETE FROM restaurants WHERE id = {restaurant_id};\n"
        sql_script += "\n"
    
    sql_script += f"-- Total restaurants removed: {sum(len(d['removed_ids']) for d in removed_details)}\n"
    
    with open('remove_duplicates.sql', 'w') as f:
        f.write(sql_script)
    
    print(f"\n💾 SQL script created: remove_duplicates.sql")
    print(f"   Run this script in your database to remove duplicates.")

def main():
    """Main function."""
    print("🚀 Starting duplicate removal via API...")
    
    try:
        removed_details = remove_duplicates_via_direct_api()
        
        if removed_details:
            print(f"\n✅ Duplicate analysis completed!")
            print(f"📄 Check 'remove_duplicates.sql' for the SQL script to execute")
        else:
            print(f"\n✅ No duplicates found - database is clean!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 