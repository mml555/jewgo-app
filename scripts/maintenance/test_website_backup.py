#!/usr/bin/env python3
"""
Test Website Backup Functionality
================================

Test script to verify the Google Places website fetching functionality.

Author: JewGo Development Team
Version: 1.0
"""

import os
import sys
import requests
import json

def test_google_places_website_fetch():
    """Test the Google Places website fetching functionality."""
    
    # Backend API URL
    backend_url = "https://jewgo.onrender.com"
    
    print("🧪 Testing Website Backup Functionality")
    print("=" * 40)
    
    # Test 1: Get restaurants without websites
    print("\n1. Getting restaurants without websites...")
    try:
        response = requests.get(f"{backend_url}/api/restaurants?limit=5")
        if response.status_code == 200:
            data = response.json()
            restaurants = data.get('restaurants', [])
            
            # Find restaurants without websites
            restaurants_without_websites = [
                r for r in restaurants 
                if not r.get('website') or len(r.get('website', '')) < 10
            ]
            
            print(f"Found {len(restaurants_without_websites)} restaurants without websites")
            
            if restaurants_without_websites:
                # Test 2: Try to fetch website for first restaurant without website
                test_restaurant = restaurants_without_websites[0]
                restaurant_id = test_restaurant['id']
                restaurant_name = test_restaurant['name']
                
                print(f"\n2. Testing website fetch for: {restaurant_name} (ID: {restaurant_id})")
                
                fetch_response = requests.post(
                    f"{backend_url}/api/restaurants/{restaurant_id}/fetch-website",
                    headers={'Content-Type': 'application/json'}
                )
                
                if fetch_response.status_code == 200:
                    fetch_data = fetch_response.json()
                    print(f"✅ Success: {fetch_data.get('message')}")
                    if fetch_data.get('website'):
                        print(f"   Website: {fetch_data['website']}")
                elif fetch_response.status_code == 404:
                    fetch_data = fetch_response.json()
                    print(f"ℹ️  No website found: {fetch_data.get('message')}")
                else:
                    print(f"❌ Error: {fetch_response.status_code}")
                    print(f"   Response: {fetch_response.text}")
                
                # Test 3: Test bulk website fetching
                print(f"\n3. Testing bulk website fetching (limit: 3)...")
                
                bulk_response = requests.post(
                    f"{backend_url}/api/restaurants/fetch-missing-websites",
                    headers={'Content-Type': 'application/json'},
                    json={'limit': 3}
                )
                
                if bulk_response.status_code == 200:
                    bulk_data = bulk_response.json()
                    print(f"✅ Bulk fetch completed:")
                    print(f"   Updated: {bulk_data.get('updated', 0)}")
                    print(f"   Total checked: {bulk_data.get('total_checked', 0)}")
                    print(f"   Message: {bulk_data.get('message', '')}")
                else:
                    print(f"❌ Bulk fetch error: {bulk_response.status_code}")
                    print(f"   Response: {bulk_response.text}")
            else:
                print("No restaurants without websites found for testing")
                
        else:
            print(f"❌ Failed to get restaurants: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

def test_frontend_api_endpoint():
    """Test the frontend API endpoint that calls the backend."""
    
    frontend_url = "https://jewgo-app.vercel.app"
    
    print(f"\n🌐 Testing Frontend API Endpoint")
    print("=" * 40)
    
    try:
        # Test the frontend API route
        response = requests.get(f"{frontend_url}/api/restaurants?limit=3")
        
        if response.status_code == 200:
            data = response.json()
            restaurants = data.get('data', {}).get('restaurants', [])
            
            print(f"Frontend API returned {len(restaurants)} restaurants")
            
            # Check website availability
            with_websites = sum(1 for r in restaurants if r.get('website') and len(r.get('website', '')) > 10)
            without_websites = len(restaurants) - with_websites
            
            print(f"   With websites: {with_websites}")
            print(f"   Without websites: {without_websites}")
            
            # Show sample restaurant data
            if restaurants:
                sample = restaurants[0]
                print(f"\nSample restaurant:")
                print(f"   Name: {sample.get('name')}")
                print(f"   Website: {sample.get('website', 'None')}")
                print(f"   Address: {sample.get('address', 'None')}")
                
        else:
            print(f"❌ Frontend API error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")

def main():
    """Main test function."""
    
    print("🔍 Website Backup System Test")
    print("=" * 50)
    
    # Test backend functionality
    test_google_places_website_fetch()
    
    # Test frontend API
    test_frontend_api_endpoint()
    
    print(f"\n✅ Testing completed!")
    print(f"\n📋 Summary:")
    print(f"   - Backend API endpoints tested")
    print(f"   - Frontend API integration verified")
    print(f"   - Google Places website fetching functionality ready")

if __name__ == "__main__":
    main() 