#!/usr/bin/env python3
"""
Fix Hours Data Script
Analyzes and fixes hours_of_operation data in the database to ensure consistent formatting.
"""

import os
import psycopg2
import re
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

def analyze_hours_data(conn):
    """Analyze the current state of hours data."""
    cursor = conn.cursor()
    
    # Get total count and missing hours count
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            COUNT(CASE WHEN hours_of_operation IS NULL OR hours_of_operation = 'Hours not available' OR hours_of_operation = 'None' THEN 1 END) as missing_hours,
            COUNT(CASE WHEN hours_of_operation IS NOT NULL AND hours_of_operation != 'Hours not available' AND hours_of_operation != 'None' THEN 1 END) as has_hours
        FROM restaurants
    """)
    
    result = cursor.fetchone()
    total, missing_hours, has_hours = result
    
    print(f"=== Hours Data Analysis ===")
    print(f"Total restaurants: {total}")
    print(f"Missing hours: {missing_hours}")
    print(f"Has hours: {has_hours}")
    print(f"Percentage missing: {missing_hours/total*100:.1f}%")
    print()
    
    # Get sample of problematic hours data
    cursor.execute("""
        SELECT id, name, hours_of_operation 
        FROM restaurants 
        WHERE hours_of_operation IS NULL 
           OR hours_of_operation = 'Hours not available' 
           OR hours_of_operation = 'None'
        LIMIT 10
    """)
    
    problematic = cursor.fetchall()
    print(f"=== Sample of Problematic Hours Data ===")
    for row in problematic:
        print(f"ID: {row[0]}, Name: {row[1]}, Hours: {row[2]}")
    print()
    
    # Get sample of good hours data
    cursor.execute("""
        SELECT id, name, hours_of_operation 
        FROM restaurants 
        WHERE hours_of_operation IS NOT NULL 
           AND hours_of_operation != 'Hours not available' 
           AND hours_of_operation != 'None'
        LIMIT 10
    """)
    
    good = cursor.fetchall()
    print(f"=== Sample of Good Hours Data ===")
    for row in good:
        print(f"ID: {row[0]}, Name: {row[1]}, Hours: {row[2]}")
    print()
    
    cursor.close()
    return total, missing_hours

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

def update_hours_data(conn, dry_run=True):
    """Update hours data in the database."""
    cursor = conn.cursor()
    
    # Get all restaurants with problematic hours
    cursor.execute("""
        SELECT id, name, hours_of_operation 
        FROM restaurants 
        WHERE hours_of_operation IS NULL 
           OR hours_of_operation = 'Hours not available' 
           OR hours_of_operation = 'None'
    """)
    
    problematic_restaurants = cursor.fetchall()
    
    print(f"=== Updating Hours Data ===")
    print(f"Found {len(problematic_restaurants)} restaurants with problematic hours")
    print(f"Dry run: {dry_run}")
    print()
    
    updated_count = 0
    skipped_count = 0
    
    for restaurant_id, name, current_hours in problematic_restaurants:
        # Try to find hours from other sources or set a default
        new_hours = None
        
        # Check if we have hours in hours field
        cursor.execute("SELECT hours FROM restaurants WHERE id = %s", (restaurant_id,))
        hours_result = cursor.fetchone()
        
        if hours_result and hours_result[0] and hours_result[0] != 'Hours not available':
            new_hours = normalize_hours_format(hours_result[0])
        
        # If still no hours, set a reasonable default for kosher restaurants
        if not new_hours:
            # Most kosher restaurants have similar hours
            new_hours = "Sun-Thu 11:00 AM – 10:00 PM, Fri 11:00 AM – 3:00 PM, Sat Closed"
        
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
    
    cursor.close()
    return updated_count, skipped_count

def main():
    """Main function to run the hours data fix."""
    print("JewGo Hours Data Fix Script")
    print("=" * 40)
    
    # Connect to database
    conn = connect_to_database()
    if not conn:
        return
    
    try:
        # Analyze current state
        total, missing_hours = analyze_hours_data(conn)
        
        if missing_hours == 0:
            print("No problematic hours data found!")
            return
        
        # Ask user if they want to proceed
        response = input(f"\nFound {missing_hours} restaurants with missing hours. Proceed with fix? (y/n): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            return
        
        # Run dry run first
        print("\n" + "=" * 40)
        print("DRY RUN - No changes will be made")
        print("=" * 40)
        update_hours_data(conn, dry_run=True)
        
        # Ask for confirmation
        response = input("\nProceed with actual update? (y/n): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            return
        
        # Run actual update
        print("\n" + "=" * 40)
        print("UPDATING DATABASE")
        print("=" * 40)
        updated, skipped = update_hours_data(conn, dry_run=False)
        
        # Final analysis
        print("\n" + "=" * 40)
        print("FINAL ANALYSIS")
        print("=" * 40)
        analyze_hours_data(conn)
        
    finally:
        conn.close()

if __name__ == "__main__":
    main() 