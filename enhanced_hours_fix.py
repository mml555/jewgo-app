#!/usr/bin/env python3
"""
Enhanced Hours Data Fix Script
Fetches hours from Google Places API and fixes hours_of_operation data in the database.
"""

import os
import psycopg2
import re
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def connect_to_database():
    """Connect to the PostgreSQL database."""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("Error: DATABASE_URL environment variable not set")
        return None
    
    try:
        conn = psycopg2.connect(database_url)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def get_google_places_hours(place_id, api_key):
    """Fetch hours from Google Places API."""
    if not api_key:
        return None
    
    url = f"https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'fields': 'opening_hours',
        'key': api_key
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] == 'OK' and 'result' in data and 'opening_hours' in data['result']:
            opening_hours = data['result']['opening_hours']
            if 'weekday_text' in opening_hours:
                return opening_hours['weekday_text']
        
        return None
    except Exception as e:
        print(f"Error fetching hours from Google Places: {e}")
        return None

def format_google_hours(weekday_text):
    """Convert Google Places weekday_text to our format."""
    if not weekday_text:
        return None
    
    # Google format: "Monday: 11:00 AM – 10:00 PM"
    # Our format: "Mon 11:00 AM – 10:00 PM"
    
    day_mapping = {
        'Monday': 'Mon',
        'Tuesday': 'Tue', 
        'Wednesday': 'Wed',
        'Thursday': 'Thu',
        'Friday': 'Fri',
        'Saturday': 'Sat',
        'Sunday': 'Sun'
    }
    
    formatted_parts = []
    for day_text in weekday_text:
        if ':' in day_text:
            day, hours = day_text.split(':', 1)
            day = day.strip()
            hours = hours.strip()
            
            if day in day_mapping:
                formatted_parts.append(f"{day_mapping[day]} {hours}")
    
    return ', '.join(formatted_parts) if formatted_parts else None

def normalize_hours_format(hours_str):
    """Normalize hours format to be consistent and parseable."""
    if not hours_str or hours_str in ['Hours not available', 'None']:
        return None
    
    # Remove Unicode characters and normalize spacing
    normalized = hours_str.replace('\u202f', ' ').replace('\u2009', ' ')
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    
    # Handle common patterns and convert to standard format
    patterns = [
        # Convert "Open 24 hours" format
        (r'(\w+)\s+Open\s+24\s+hours', r'\1 12:00 AM – 11:59 PM'),
        # Convert "Closed" format
        (r'(\w+)\s+Closed', r'\1 Closed'),
        # Normalize time formats
        (r'(\d{1,2}):?(\d{2})?\s*(am|pm)', r'\1:\2 \3'),
        # Ensure proper spacing around dashes
        (r'(\d{1,2}:\d{2}\s*(?:AM|PM))\s*[-–—]\s*(\d{1,2}:\d{2}\s*(?:AM|PM))', r'\1 – \2'),
    ]
    
    for pattern, replacement in patterns:
        normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
    
    return normalized

def get_default_hours_for_category(category):
    """Get default hours based on restaurant category."""
    category = category.lower() if category else ''
    
    if 'bakery' in category or 'cafe' in category:
        return "Mon-Fri 7:00 AM – 6:00 PM, Sat 8:00 AM – 5:00 PM, Sun 8:00 AM – 4:00 PM"
    elif 'pizza' in category or 'fast' in category:
        return "Sun-Thu 11:00 AM – 10:00 PM, Fri 11:00 AM – 3:00 PM, Sat 6:00 PM – 11:00 PM"
    elif 'fine' in category or 'steak' in category:
        return "Sun-Thu 5:00 PM – 10:00 PM, Fri 5:00 PM – 11:00 PM, Sat 6:00 PM – 11:00 PM"
    else:
        # Default kosher restaurant hours
        return "Sun-Thu 11:00 AM – 10:00 PM, Fri 11:00 AM – 3:00 PM, Sat Closed"

def analyze_and_fix_hours(conn, use_google_api=False, dry_run=True):
    """Analyze and fix hours data in the database."""
    cursor = conn.cursor()
    
    # Get restaurants with problematic hours
    cursor.execute("""
        SELECT id, name, address, kosher_category, external_id, hours_of_operation, hours
        FROM restaurants 
        WHERE hours_of_operation IS NULL 
           OR hours_of_operation = 'Hours not available' 
           OR hours_of_operation = 'None'
        ORDER BY name
    """)
    
    problematic_restaurants = cursor.fetchall()
    
    print(f"=== Hours Data Fix ===")
    print(f"Found {len(problematic_restaurants)} restaurants with problematic hours")
    print(f"Use Google API: {use_google_api}")
    print(f"Dry run: {dry_run}")
    print()
    
    google_api_key = os.environ.get('GOOGLE_PLACES_API_KEY') if use_google_api else None
    updated_count = 0
    skipped_count = 0
    google_fetched = 0
    
    for restaurant_id, name, address, category, external_id, current_hours, hours in problematic_restaurants:
        new_hours = None
        
        # First, try to normalize existing hours data
        if hours and hours != 'Hours not available':
            new_hours = normalize_hours_format(hours)
        
        # If no hours and Google API is enabled, try to fetch from Google Places
        if not new_hours and use_google_api and external_id:
            print(f"Fetching hours for {name} from Google Places...")
            google_hours = get_google_places_hours(external_id, google_api_key)
            if google_hours:
                new_hours = format_google_hours(google_hours)
                google_fetched += 1
                print(f"  Fetched: {new_hours}")
            else:
                print(f"  No hours found in Google Places")
            
            # Rate limiting for Google API
            time.sleep(0.1)
        
        # If still no hours, use default based on category
        if not new_hours:
            new_hours = get_default_hours_for_category(category)
        
        if dry_run:
            print(f"Would update: {name}")
            print(f"  From: {current_hours}")
            print(f"  To: {new_hours}")
            print()
        else:
            try:
                cursor.execute(
                    "UPDATE restaurants SET hours_of_operation = %s, updated_date = CURRENT_TIMESTAMP WHERE id = %s",
                    (new_hours, restaurant_id)
                )
                updated_count += 1
                print(f"Updated: {name} -> {new_hours}")
            except Exception as e:
                print(f"Error updating {name}: {e}")
                skipped_count += 1
    
    if not dry_run:
        conn.commit()
        print(f"\n=== Update Summary ===")
        print(f"Updated: {updated_count}")
        print(f"Skipped: {skipped_count}")
        if use_google_api:
            print(f"Google API fetched: {google_fetched}")
    
    cursor.close()
    return updated_count, skipped_count, google_fetched

def main():
    """Main function to run the enhanced hours data fix."""
    print("JewGo Enhanced Hours Data Fix Script")
    print("=" * 50)
    
    # Connect to database
    conn = connect_to_database()
    if not conn:
        return
    
    try:
        # Check current state
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN hours_of_operation IS NULL OR hours_of_operation = 'Hours not available' OR hours_of_operation = 'None' THEN 1 END) as missing_hours
            FROM restaurants
        """)
        total, missing_hours = cursor.fetchone()
        cursor.close()
        
        print(f"Total restaurants: {total}")
        print(f"Missing hours: {missing_hours}")
        print(f"Percentage missing: {missing_hours/total*100:.1f}%")
        print()
        
        if missing_hours == 0:
            print("No problematic hours data found!")
            return
        
        # Ask user for options
        print("Options:")
        print("1. Use default hours (no Google API)")
        print("2. Try Google Places API first, then defaults")
        print("3. Exit")
        
        choice = input("\nChoose option (1-3): ").strip()
        
        if choice == '3':
            print("Operation cancelled.")
            return
        
        use_google_api = choice == '2'
        
        if use_google_api and not os.environ.get('GOOGLE_PLACES_API_KEY'):
            print("Warning: GOOGLE_PLACES_API_KEY not set. Will use defaults only.")
            use_google_api = False
        
        # Run dry run first
        print("\n" + "=" * 50)
        print("DRY RUN - No changes will be made")
        print("=" * 50)
        analyze_and_fix_hours(conn, use_google_api, dry_run=True)
        
        # Ask for confirmation
        response = input("\nProceed with actual update? (y/n): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            return
        
        # Run actual update
        print("\n" + "=" * 50)
        print("UPDATING DATABASE")
        print("=" * 50)
        updated, skipped, google_fetched = analyze_and_fix_hours(conn, use_google_api, dry_run=False)
        
        # Final analysis
        print("\n" + "=" * 50)
        print("FINAL ANALYSIS")
        print("=" * 50)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN hours_of_operation IS NULL OR hours_of_operation = 'Hours not available' OR hours_of_operation = 'None' THEN 1 END) as missing_hours
            FROM restaurants
        """)
        final_total, final_missing = cursor.fetchone()
        cursor.close()
        
        print(f"Final state:")
        print(f"Total restaurants: {final_total}")
        print(f"Missing hours: {final_missing}")
        print(f"Percentage missing: {final_missing/final_total*100:.1f}%")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main() 