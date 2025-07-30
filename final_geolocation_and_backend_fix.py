#!/usr/bin/env python3
"""
Final Geolocation and Backend Fix
"""

import os
import subprocess
import requests
import time
from datetime import datetime

def commit_geolocation_fix():
    """Commit the final geolocation fixes"""
    try:
        # Add the updated files
        subprocess.run(['git', 'add', 'app/favorites/page.tsx'], check=True)
        
        # Commit the changes
        commit_message = f"🔧 Final geolocation fix - remove automatic location from favorites - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push to remote
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Final geolocation fix committed and pushed successfully!")
        print(f"📝 Commit: {commit_message}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing changes: {e}")
        return False

def check_backend_status():
    """Check backend status and restart if needed"""
    print("\n🔍 Checking Backend Status")
    print("=" * 25)
    
    try:
        response = requests.get("https://jewgo.onrender.com/", timeout=10)
        
        if response.status_code == 200:
            print("✅ Backend is healthy and responding")
            return True
        else:
            print(f"❌ Backend returned status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend is not responding: {e}")
        print("🔄 Backend may be restarting or experiencing issues")
        return False

def wait_for_backend():
    """Wait for backend to come back online"""
    print("\n⏳ Waiting for backend to come back online...")
    
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            response = requests.get("https://jewgo.onrender.com/", timeout=10)
            if response.status_code == 200:
                print(f"✅ Backend is back online after {attempt + 1} attempts")
                return True
        except:
            pass
        
        print(f"   Attempt {attempt + 1}/{max_attempts} - Backend not ready yet...")
        time.sleep(30)  # Wait 30 seconds between attempts
    
    print("❌ Backend did not come back online within expected time")
    return False

def add_sample_data():
    """Add sample data to the backend"""
    print("\n🍽️  Adding Sample Restaurant Data")
    print("=" * 30)
    
    try:
        # Sample restaurant data
        sample_restaurants = [
            {
                "business_id": "sample_001",
                "name": "Kosher Deli & Grill",
                "website_link": "https://example.com/kosher-deli",
                "phone_number": "(555) 123-4567",
                "address": "123 Main Street",
                "city": "Miami",
                "state": "FL",
                "zip_code": "33101",
                "certificate_link": "https://example.com/cert1",
                "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=400",
                "certifying_agency": "ORB",
                "kosher_category": "meat",
                "listing_type": "restaurant",
                "status": "active",
                "rating": 4.5,
                "price_range": "$$",
                "hours_of_operation": "Mon-Fri: 11AM-9PM, Sat: 12PM-10PM, Sun: Closed",
                "short_description": "Authentic kosher deli serving traditional Jewish cuisine with a modern twist.",
                "notes": "Glatt kosher certified by ORB",
                "latitude": 25.7617,
                "longitude": -80.1918,
                "data_source": "manual"
            },
            {
                "business_id": "sample_002",
                "name": "Shalom Pizza & Pasta",
                "website_link": "https://example.com/shalom-pizza",
                "phone_number": "(555) 234-5678",
                "address": "456 Ocean Drive",
                "city": "Miami Beach",
                "state": "FL",
                "zip_code": "33139",
                "certificate_link": "https://example.com/cert2",
                "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400",
                "certifying_agency": "ORB",
                "kosher_category": "dairy",
                "listing_type": "restaurant",
                "status": "active",
                "rating": 4.2,
                "price_range": "$",
                "hours_of_operation": "Daily: 11AM-11PM",
                "short_description": "Kosher pizza and pasta restaurant with authentic Italian flavors.",
                "notes": "Dairy restaurant - no meat products",
                "latitude": 25.7907,
                "longitude": -80.1300,
                "data_source": "manual"
            },
            {
                "business_id": "sample_003",
                "name": "Mazel Tov Bakery",
                "website_link": "https://example.com/mazel-tov-bakery",
                "phone_number": "(555) 345-6789",
                "address": "789 Biscayne Blvd",
                "city": "Miami",
                "state": "FL",
                "zip_code": "33132",
                "certificate_link": "https://example.com/cert3",
                "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400",
                "certifying_agency": "ORB",
                "kosher_category": "dairy",
                "listing_type": "bakery",
                "status": "active",
                "rating": 4.8,
                "price_range": "$",
                "hours_of_operation": "Mon-Sat: 6AM-8PM, Sun: 7AM-6PM",
                "short_description": "Traditional Jewish bakery specializing in challah, rugelach, and other kosher pastries.",
                "notes": "Parve and dairy options available",
                "latitude": 25.7749,
                "longitude": -80.1977,
                "data_source": "manual"
            }
        ]
        
        success_count = 0
        for i, restaurant in enumerate(sample_restaurants, 1):
            try:
                print(f"📝 Adding restaurant {i}/{len(sample_restaurants)}: {restaurant['name']}")
                
                response = requests.post(
                    "https://jewgo.onrender.com/api/admin/restaurants",
                    json=restaurant,
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        print(f"✅ Successfully added: {restaurant['name']}")
                        success_count += 1
                    else:
                        print(f"❌ Failed to add: {restaurant['name']} - {data.get('message', 'Unknown error')}")
                else:
                    print(f"❌ HTTP Error {response.status_code}: {restaurant['name']}")
                    
            except Exception as e:
                print(f"❌ Error adding {restaurant['name']}: {e}")
        
        print(f"\n📊 Results: {success_count}/{len(sample_restaurants)} restaurants added successfully")
        return success_count > 0
        
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
        return False

def test_frontend_access():
    """Test frontend accessibility"""
    print("\n🌐 Testing Frontend Access")
    print("=" * 25)
    
    urls = [
        "https://jewgo-app.vercel.app/",
        "https://jewgo-j953cxrfi-mml555s-projects.vercel.app/"
    ]
    
    results = []
    
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {url} - Accessible")
                results.append(True)
            else:
                print(f"❌ {url} - Status: {response.status_code}")
                results.append(False)
        except Exception as e:
            print(f"❌ {url} - Error: {e}")
            results.append(False)
    
    return any(results)

def provide_guidance():
    """Provide guidance on the fixes"""
    print("\n🔧 Final Fixes Applied:")
    print("   • Removed automatic geolocation from favorites page")
    print("   • All geolocation requests now require user interaction")
    print("   • Frontend will redeploy automatically")
    
    print("\n🎯 What This Fixes:")
    print("   • Eliminates all 'Only request geolocation information in response to a user gesture' violations")
    print("   • Improves user privacy and browser compliance")
    print("   • Maintains all location-based functionality")
    print("   • Users can still access location features when needed")
    
    print("\n⚠️  Backend Status:")
    print("   • Backend may be restarting (common with Render)")
    print("   • Sample data will be re-added when backend is available")
    print("   • Application will work once backend is back online")
    
    print("\n🚀 Next Steps:")
    print("   1. Wait for Vercel deployment to complete")
    print("   2. Wait for backend to come back online")
    print("   3. Test the application at both Vercel URLs")
    print("   4. Verify no geolocation violations in browser console")
    print("   5. Confirm restaurant data displays correctly")

def main():
    """Main function to fix remaining issues"""
    print("🚀 Applying Final Geolocation and Backend Fixes")
    print("=" * 50)
    
    # Commit the geolocation fix
    if commit_geolocation_fix():
        print(f"\n✅ Final geolocation fix deployed")
        print("   • Removed automatic geolocation from favorites page")
        print("   • All geolocation violations should now be resolved")
        print("   • Frontend will redeploy automatically")
        
        # Check backend status
        if check_backend_status():
            print("\n✅ Backend is operational")
            
            # Add sample data
            if add_sample_data():
                print("✅ Sample data added successfully")
            else:
                print("⚠️  Failed to add sample data")
        else:
            print("\n⚠️  Backend is not responding")
            print("🔄 Waiting for backend to come back online...")
            
            if wait_for_backend():
                print("✅ Backend is back online")
                
                # Add sample data
                if add_sample_data():
                    print("✅ Sample data added successfully")
                else:
                    print("⚠️  Failed to add sample data")
            else:
                print("❌ Backend did not come back online")
        
        # Test frontend
        if test_frontend_access():
            print("\n✅ Frontend is accessible")
        else:
            print("\n⚠️  Frontend may still be deploying")
        
        provide_guidance()
    else:
        print("❌ Failed to commit geolocation fix")

if __name__ == "__main__":
    main() 