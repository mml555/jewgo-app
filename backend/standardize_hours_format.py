#!/usr/bin/env python3
"""
Standardize Hours Format in Database
====================================

This script standardizes the hours format in the database to ensure consistency
across all restaurants. It converts various formats to a standardized format.
"""

import os
import sys
import re
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database_manager_v3 import EnhancedDatabaseManager, Restaurant

def standardize_time_format(time_str):
    """Convert time to consistent 12-hour format with AM/PM."""
    if not time_str:
        return time_str
    
    # Remove extra spaces and normalize
    time_str = time_str.strip()
    
    # Handle common variations
    time_str = time_str.replace('am', 'AM').replace('pm', 'PM')
    time_str = time_str.replace('a.m.', 'AM').replace('p.m.', 'PM')
    time_str = time_str.replace('a.m', 'AM').replace('p.m', 'PM')
    
    # Handle 24-hour format conversion
    if ':' in time_str and len(time_str) <= 5:
        try:
            # Check if it's 24-hour format (no AM/PM)
            if 'AM' not in time_str.upper() and 'PM' not in time_str.upper():
                hour, minute = time_str.split(':')
                hour = int(hour)
                minute = int(minute)
                
                if hour == 0:
                    return f"12:{minute:02d} AM"
                elif hour < 12:
                    return f"{hour}:{minute:02d} AM"
                elif hour == 12:
                    return f"12:{minute:02d} PM"
                else:
                    return f"{hour-12}:{minute:02d} PM"
        except:
            pass
    
    return time_str

def parse_hours_string(hours_str):
    """Parse hours string and return standardized format."""
    if not hours_str:
        return ""
    
    # Handle special cases
    if 'closed' in hours_str.lower() or '🔴 closed' in hours_str.lower():
        return "Closed"
    
    if '24/7' in hours_str or '24 hours' in hours_str:
        return "Open 24/7"
    
    # Day mappings
    day_mapping = {
        'monday': 'Mon', 'mon': 'Mon',
        'tuesday': 'Tue', 'tue': 'Tue',
        'wednesday': 'Wed', 'wed': 'Wed',
        'thursday': 'Thu', 'thu': 'Thu',
        'friday': 'Fri', 'fri': 'Fri',
        'saturday': 'Sat', 'sat': 'Sat',
        'sunday': 'Sun', 'sun': 'Sun'
    }
    
    # Split by common separators
    parts = re.split(r'[,|•]', hours_str)
    standardized_parts = []
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # Handle "Sun-Thu" format
        if '-' in part and any(day in part.lower() for day in day_mapping.keys()):
            # Extract day range and time
            day_part, time_part = part.split(' ', 1) if ' ' in part else (part, '')
            
            if '-' in day_part:
                start_day, end_day = day_part.split('-')
                start_day = day_mapping.get(start_day.lower(), start_day)
                end_day = day_mapping.get(end_day.lower(), end_day)
                
                if time_part:
                    # Standardize time format
                    if '–' in time_part or '-' in time_part:
                        start_time, end_time = re.split(r'[–-]', time_part)
                        start_time = standardize_time_format(start_time.strip())
                        end_time = standardize_time_format(end_time.strip())
                        standardized_parts.append(f"{start_day}-{end_day} {start_time} – {end_time}")
                    else:
                        time_part = standardize_time_format(time_part)
                        standardized_parts.append(f"{start_day}-{end_day} {time_part}")
                else:
                    standardized_parts.append(f"{start_day}-{end_day}")
        
        # Handle individual day format
        elif any(day in part.lower() for day in day_mapping.keys()):
            # Extract day and time
            words = part.split()
            if len(words) >= 2:
                day = day_mapping.get(words[0].lower(), words[0])
                time_part = ' '.join(words[1:])
                
                if '–' in time_part or '-' in time_part:
                    start_time, end_time = re.split(r'[–-]', time_part)
                    start_time = standardize_time_format(start_time.strip())
                    end_time = standardize_time_format(end_time.strip())
                    standardized_parts.append(f"{day} {start_time} – {end_time}")
                else:
                    time_part = standardize_time_format(time_part)
                    standardized_parts.append(f"{day} {time_part}")
            else:
                day = day_mapping.get(part.lower(), part)
                standardized_parts.append(day)
        
        # Handle time-only parts
        elif ':' in part or 'am' in part.lower() or 'pm' in part.lower():
            time_part = standardize_time_format(part)
            if time_part:
                standardized_parts.append(time_part)
        
        # Handle "Closed" or other status
        elif 'closed' in part.lower():
            standardized_parts.append("Closed")
        
        else:
            # Keep as is if we can't parse it
            standardized_parts.append(part)
    
    return ', '.join(standardized_parts)

def standardize_hours_in_database():
    """Standardize hours format for all restaurants in the database."""
    
    # Initialize database manager
    db_manager = EnhancedDatabaseManager()
    if not db_manager.connect():
        print("❌ Failed to connect to database")
        return
    
    session = db_manager.get_session()
    
    try:
        # Get all restaurants with hours data
        restaurants_with_hours = session.query(Restaurant).filter(
            (Restaurant.hours_of_operation.isnot(None)) &
            (Restaurant.hours_of_operation != '') &
            (Restaurant.hours_of_operation != ' ') &
            (Restaurant.hours_of_operation != 'None')
        ).all()
        
        print(f"📊 Found {len(restaurants_with_hours)} restaurants with hours data")
        print("=" * 60)
        
        updated_count = 0
        unchanged_count = 0
        
        for restaurant in restaurants_with_hours:
            original_hours = restaurant.hours_of_operation
            standardized_hours = parse_hours_string(original_hours)
            
            if standardized_hours != original_hours:
                print(f"🔄 Updating {restaurant.name}:")
                print(f"   Before: {original_hours}")
                print(f"   After:  {standardized_hours}")
                print("-" * 40)
                
                restaurant.hours_of_operation = standardized_hours
                updated_count += 1
            else:
                unchanged_count += 1
        
        # Commit changes
        if updated_count > 0:
            session.commit()
            print(f"\n✅ Successfully updated {updated_count} restaurants")
            print(f"📊 {unchanged_count} restaurants already had correct format")
        else:
            print(f"\n📊 All {unchanged_count} restaurants already have correct format")
        
        print(f"\n🎯 Summary:")
        print(f"   Total restaurants processed: {len(restaurants_with_hours)}")
        print(f"   Updated: {updated_count}")
        print(f"   Unchanged: {unchanged_count}")
        
    except Exception as e:
        print(f"❌ Error standardizing hours: {e}")
        session.rollback()
    
    finally:
        session.close()
        db_manager.disconnect()

if __name__ == "__main__":
    standardize_hours_in_database() 