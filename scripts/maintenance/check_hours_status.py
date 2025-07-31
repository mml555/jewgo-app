#!/usr/bin/env python3
"""
Check Hours Data Status
=======================

Simple script to check the current status of hours data in the database
and provide a summary of the hours backup system implementation.
"""

import os
import sys
import requests
from typing import Dict, List, Any

def check_hours_data_status():
    """Check the current status of hours data in the database."""
    print("🔍 Checking Hours Data Status")
    print("=" * 50)
    
    # Try to get data from backend API
    backend_url = "https://jewgo.onrender.com"
    
    try:
        print("📡 Attempting to connect to backend...")
        response = requests.get(f"{backend_url}/api/restaurants?limit=50", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            restaurants = data.get('restaurants', [])
            
            if restaurants:
                analyze_hours_data(restaurants)
            else:
                print("❌ No restaurants data found in API response")
                
        else:
            print(f"❌ Backend API returned status code: {response.status_code}")
            print("   This indicates the backend may need redeployment.")
            
    except requests.exceptions.Timeout:
        print("❌ Backend API timeout - server may be down")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend API")
    except Exception as e:
        print(f"❌ Error connecting to backend: {e}")

def analyze_hours_data(restaurants: List[Dict[str, Any]]):
    """Analyze the hours data from restaurants."""
    total_restaurants = len(restaurants)
    
    # Count restaurants with and without hours
    with_hours = 0
    without_hours = 0
    hours_examples = []
    no_hours_examples = []
    
    for restaurant in restaurants:
        hours_open = restaurant.get('hours_open', '')
        
        if hours_open and hours_open != 'None' and len(hours_open) > 10:
            with_hours += 1
            if len(hours_examples) < 3:
                hours_examples.append({
                    'name': restaurant.get('name', 'Unknown'),
                    'hours': hours_open[:60] + '...' if len(hours_open) > 60 else hours_open
                })
        else:
            without_hours += 1
            if len(no_hours_examples) < 3:
                no_hours_examples.append(restaurant.get('name', 'Unknown'))
    
    # Calculate coverage percentage
    coverage_percentage = (with_hours / total_restaurants * 100) if total_restaurants > 0 else 0
    
    print(f"📊 Hours Data Analysis")
    print(f"   Total restaurants checked: {total_restaurants}")
    print(f"   ✅ Restaurants with hours: {with_hours}")
    print(f"   ❌ Restaurants without hours: {without_hours}")
    print(f"   📈 Hours coverage: {coverage_percentage:.1f}%")
    
    if hours_examples:
        print(f"\n📋 Sample restaurants with hours:")
        for i, example in enumerate(hours_examples, 1):
            print(f"   {i}. {example['name']}")
            print(f"      Hours: {example['hours']}")
    
    if no_hours_examples:
        print(f"\n📋 Sample restaurants without hours:")
        for i, name in enumerate(no_hours_examples, 1):
            print(f"   {i}. {name}")

def check_google_places_api_status():
    """Check if Google Places API key is working."""
    print(f"\n🔍 Checking Google Places API Status")
    print("=" * 50)
    
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    
    if not api_key:
        print("❌ GOOGLE_PLACES_API_KEY not set")
        return False
    
    print(f"✅ Google Places API key found (length: {len(api_key)})")
    
    # Test the API key
    try:
        test_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=Starbucks&key={api_key}"
        response = requests.get(test_url, timeout=10)
        data = response.json()
        
        if data.get('status') == 'OK':
            print("✅ Google Places API key is working")
            return True
        elif data.get('status') == 'REQUEST_DENIED':
            print("❌ Google Places API key is expired or invalid")
            print(f"   Error: {data.get('error_message', 'Unknown error')}")
            return False
        else:
            print(f"⚠️  Google Places API returned status: {data.get('status')}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Google Places API: {e}")
        return False

def show_implementation_summary():
    """Show a summary of the hours backup system implementation."""
    print(f"\n📋 Hours Backup System Implementation Summary")
    print("=" * 60)
    
    print("✅ COMPLETED COMPONENTS:")
    print("   • Enhanced hours updater script")
    print("   • Backend API endpoints for hours fetching")
    print("   • Google Places helper functions")
    print("   • Frontend utilities for hours backup")
    print("   • Test script for system validation")
    print("   • Comprehensive documentation")
    
    print(f"\n🔧 SYSTEM FEATURES:")
    print("   • Automatic hours fetching from Google Places API")
    print("   • Hours formatting from Google format to database format")
    print("   • Rate limiting and error handling")
    print("   • Bulk and individual restaurant updates")
    print("   • Frontend integration for real-time hours fetching")
    
    print(f"\n📁 FILES CREATED/MODIFIED:")
    print("   • scripts/maintenance/enhanced_google_places_hours_updater.py")
    print("   • backend/app.py (added hours API endpoints)")
    print("   • backend/utils/google_places_helper.py (added hours functions)")
    print("   • frontend/utils/hoursBackup.ts")
    print("   • scripts/maintenance/test_hours_backup.py")
    print("   • HOURS_BACKUP_SYSTEM_SUMMARY.md")
    
    print(f"\n🚀 USAGE INSTRUCTIONS:")
    print("   1. Renew Google Places API key")
    print("   2. Redeploy backend to enable new API endpoints")
    print("   3. Run: python scripts/maintenance/enhanced_google_places_hours_updater.py")
    print("   4. Choose option 1 to update all restaurants without hours")

def main():
    """Main function."""
    print("🚀 Google Places Hours Backup System - Status Check")
    print("=" * 70)
    
    # Check current hours data status
    check_hours_data_status()
    
    # Check Google Places API status
    api_working = check_google_places_api_status()
    
    # Show implementation summary
    show_implementation_summary()
    
    # Final status and recommendations
    print(f"\n📊 FINAL STATUS & RECOMMENDATIONS")
    print("=" * 50)
    
    if api_working:
        print("✅ Google Places API is working")
        print("✅ Hours backup system is ready to use")
        print("🔧 Next step: Run the hours updater script")
    else:
        print("❌ Google Places API key needs renewal")
        print("🔧 Next step: Renew API key and redeploy backend")
    
    print(f"\n📈 Expected Outcome:")
    print("   • Hours coverage will increase significantly")
    print("   • Users will see accurate opening hours")
    print("   • Better user experience with complete restaurant information")

if __name__ == "__main__":
    main() 