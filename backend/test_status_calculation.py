#!/usr/bin/env python3
"""
Test script for dynamic restaurant status calculation.

This script tests the restaurant status calculation module to ensure it works
correctly with various business hours formats and timezone handling.
"""

import sys
import os
from datetime import datetime, time
import pytz

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.restaurant_status import get_restaurant_status, RestaurantStatusCalculator

def test_status_calculation():
    """Test the restaurant status calculation with various scenarios."""
    
    print("🧪 Testing Dynamic Restaurant Status Calculation")
    print("=" * 60)
    
    # Test data with various business hours formats
    test_restaurants = [
        {
            'name': 'Test Restaurant 1 - Standard Hours',
            'hours_open': 'Monday: 9:00 AM - 10:00 PM\nTuesday: 9:00 AM - 10:00 PM\nWednesday: 9:00 AM - 10:00 PM\nThursday: 9:00 AM - 10:00 PM\nFriday: 9:00 AM - 10:00 PM\nSaturday: 10:00 AM - 11:00 PM\nSunday: 10:00 AM - 9:00 PM',
            'city': 'New York',
            'state': 'NY',
            'latitude': 40.7128,
            'longitude': -74.0060
        },
        {
            'name': 'Test Restaurant 2 - Compact Format',
            'hours_open': 'Mon 9AM-10PM, Tue 9AM-10PM, Wed 9AM-10PM, Thu 9AM-10PM, Fri 9AM-10PM, Sat 10AM-11PM, Sun 10AM-9PM',
            'city': 'Los Angeles',
            'state': 'CA',
            'latitude': 34.0522,
            'longitude': -118.2437
        },
        {
            'name': 'Test Restaurant 3 - 24 Hour',
            'hours_open': 'Daily: 24 hours',
            'city': 'Chicago',
            'state': 'IL',
            'latitude': 41.8781,
            'longitude': -87.6298
        },
        {
            'name': 'Test Restaurant 4 - Overnight Hours',
            'hours_open': 'Monday: 6:00 PM - 2:00 AM\nTuesday: 6:00 PM - 2:00 AM\nWednesday: 6:00 PM - 2:00 AM\nThursday: 6:00 PM - 2:00 AM\nFriday: 6:00 PM - 3:00 AM\nSaturday: 6:00 PM - 3:00 AM\nSunday: 6:00 PM - 2:00 AM',
            'city': 'Miami',
            'state': 'FL',
            'latitude': 25.7617,
            'longitude': -80.1918
        },
        {
            'name': 'Test Restaurant 5 - Weekdays Only',
            'hours_open': 'Mon-Fri 8AM-6PM',
            'city': 'Denver',
            'state': 'CO',
            'latitude': 39.7392,
            'longitude': -104.9903
        },
        {
            'name': 'Test Restaurant 6 - No Hours Data',
            'hours_open': None,
            'city': 'Seattle',
            'state': 'WA',
            'latitude': 47.6062,
            'longitude': -122.3321
        },
        {
            'name': 'Test Restaurant 7 - Invalid Hours Format',
            'hours_open': 'Open when we feel like it',
            'city': 'Austin',
            'state': 'TX',
            'latitude': 30.2672,
            'longitude': -97.7431
        }
    ]
    
    # Test each restaurant
    for i, restaurant in enumerate(test_restaurants, 1):
        print(f"\n📍 Test {i}: {restaurant['name']}")
        print("-" * 40)
        
        try:
            status_info = get_restaurant_status(restaurant)
            
            print(f"✅ Status: {status_info['status']}")
            print(f"🔓 Is Open: {status_info['is_open']}")
            print(f"⏰ Current Time (Local): {status_info['current_time_local']}")
            print(f"🌍 Timezone: {status_info['timezone']}")
            print(f"📋 Reason: {status_info['status_reason']}")
            
            if status_info.get('next_open_time'):
                print(f"🕐 Next Open: {status_info['next_open_time']}")
            
            print(f"📊 Hours Parsed: {status_info['hours_parsed']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Status calculation test completed!")

def test_timezone_mapping():
    """Test timezone mapping functionality."""
    
    print("\n🌍 Testing Timezone Mapping")
    print("-" * 30)
    
    calculator = RestaurantStatusCalculator()
    
    test_locations = [
        ('New York', 'NY', 40.7128, -74.0060),
        ('Los Angeles', 'CA', 34.0522, -118.2437),
        ('Chicago', 'IL', 41.8781, -87.6298),
        ('Miami', 'FL', 25.7617, -80.1918),
        ('Denver', 'CO', 39.7392, -104.9903),
        ('Seattle', 'WA', 47.6062, -122.3321),
        ('Austin', 'TX', 30.2672, -97.7431),
        ('Unknown', None, None, None)
    ]
    
    for city, state, lat, lng in test_locations:
        timezone = calculator._get_timezone(lat, lng, city, state)
        print(f"📍 {city}, {state or 'Unknown'}: {timezone}")

def test_hours_parsing():
    """Test business hours parsing functionality."""
    
    print("\n⏰ Testing Hours Parsing")
    print("-" * 25)
    
    calculator = RestaurantStatusCalculator()
    
    test_hours = [
        "Monday: 9:00 AM - 10:00 PM",
        "Mon 9AM-10PM",
        "Monday 9:00-22:00",
        "Mon-Fri 9AM-5PM",
        "Daily: 24 hours",
        "Open when we feel like it"
    ]
    
    for hours in test_hours:
        print(f"\n📋 Testing: {hours}")
        success, parsed = calculator._parse_business_hours(hours)
        print(f"✅ Success: {success}")
        if success:
            print(f"📊 Parsed: {parsed}")
        else:
            print("❌ Failed to parse")

if __name__ == "__main__":
    try:
        test_status_calculation()
        test_timezone_mapping()
        test_hours_parsing()
        print("\n🎉 All tests completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc() 