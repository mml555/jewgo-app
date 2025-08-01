#!/usr/bin/env python3
"""
Analyze Hours Format in Database
================================

This script analyzes the current hours data format in the database to identify
inconsistencies and help standardize the format.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database_manager_v3 import EnhancedDatabaseManager, Restaurant

def analyze_hours_data():
    """Analyze the current hours data format in the database."""
    
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
        
        # Analyze different formats
        formats = {}
        sample_data = {}
        
        for restaurant in restaurants_with_hours:
            hours = restaurant.hours_of_operation
            
            # Determine format type
            if not hours:
                continue
                
            # Check for common patterns
            if 'Mon' in hours and 'Tue' in hours:
                format_type = 'Abbreviated Days (Mon, Tue, etc.)'
            elif 'Monday' in hours and 'Tuesday' in hours:
                format_type = 'Full Days (Monday, Tuesday, etc.)'
            elif '24/7' in hours or '24 hours' in hours:
                format_type = '24/7 Format'
            elif 'AM' in hours and 'PM' in hours:
                format_type = 'AM/PM Format'
            elif ':' in hours and len(hours) < 50:
                format_type = 'Simple Time Format'
            elif hours.isdigit() or hours.replace(':', '').isdigit():
                format_type = 'Numeric Format'
            else:
                format_type = 'Other/Unknown Format'
            
            # Count formats
            if format_type not in formats:
                formats[format_type] = 0
                sample_data[format_type] = []
            
            formats[format_type] += 1
            
            # Store sample data (limit to 3 per format)
            if len(sample_data[format_type]) < 3:
                sample_data[format_type].append({
                    'restaurant': restaurant.name,
                    'hours': hours
                })
        
        # Print analysis results
        print("📋 Hours Format Analysis:")
        print("-" * 40)
        
        for format_type, count in sorted(formats.items(), key=lambda x: x[1], reverse=True):
            print(f"\n🔸 {format_type}: {count} restaurants")
            
            if format_type in sample_data:
                print("   Sample data:")
                for sample in sample_data[format_type]:
                    print(f"   - {sample['restaurant']}: {sample['hours']}")
        
        # Check for potential issues
        print(f"\n🔍 Potential Issues:")
        print("-" * 40)
        
        # Check for very long hours strings
        long_hours = session.query(Restaurant).filter(
            (Restaurant.hours_of_operation.isnot(None)) &
            (Restaurant.hours_of_operation != '') &
            (Restaurant.hours_of_operation != ' ') &
            (Restaurant.hours_of_operation != 'None')
        ).all()
        
        long_hours_count = 0
        for restaurant in long_hours:
            if restaurant.hours_of_operation and len(restaurant.hours_of_operation) > 200:
                long_hours_count += 1
                if long_hours_count <= 3:
                    print(f"   - Very long hours string ({len(restaurant.hours_of_operation)} chars): {restaurant.name}")
                    print(f"     Hours: {restaurant.hours_of_operation[:100]}...")
        
        if long_hours_count > 3:
            print(f"   - ... and {long_hours_count - 3} more restaurants with very long hours strings")
        
        # Check for restaurants without hours
        restaurants_without_hours = session.query(Restaurant).filter(
            (Restaurant.hours_of_operation.is_(None)) |
            (Restaurant.hours_of_operation == '') |
            (Restaurant.hours_of_operation == ' ') |
            (Restaurant.hours_of_operation == 'None')
        ).count()
        
        print(f"\n📊 Summary:")
        print("-" * 40)
        print(f"   Total restaurants: {session.query(Restaurant).count()}")
        print(f"   Restaurants with hours: {len(restaurants_with_hours)}")
        print(f"   Restaurants without hours: {restaurants_without_hours}")
        print(f"   Hours format types: {len(formats)}")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        print("-" * 40)
        print("   1. Standardize to a consistent format (e.g., 'Mon 11:00 AM – 10:00 PM')")
        print("   2. Use abbreviated day names (Mon, Tue, Wed, etc.)")
        print("   3. Use consistent time format (12-hour with AM/PM)")
        print("   4. Separate days with commas")
        print("   5. Consider using JSON structure for more complex hours data")
        
    except Exception as e:
        print(f"❌ Error analyzing hours data: {e}")
    
    finally:
        session.close()
        db_manager.disconnect()

if __name__ == "__main__":
    analyze_hours_data() 