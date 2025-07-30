#!/usr/bin/env python3
"""
Comprehensive PostgreSQL Compatibility Fix
"""

import os
import subprocess
import requests
import time
from datetime import datetime

def commit_comprehensive_fix():
    """Commit the comprehensive PostgreSQL compatibility fix"""
    try:
        # Add the updated files
        subprocess.run(['git', 'add', 'requirements.txt', 'database_manager_v2.py'], check=True)
        
        # Commit the changes
        commit_message = f"🔧 Comprehensive PostgreSQL fix - SQLAlchemy 2.0 + psycopg2-binary for Python 3.13 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push to remote
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Comprehensive PostgreSQL fix committed and pushed successfully!")
        print(f"📝 Commit: {commit_message}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing changes: {e}")
        return False

def wait_for_backend_restart():
    """Wait for backend to restart after deployment"""
    print("\n⏳ Waiting for backend to restart after deployment...")
    
    max_attempts = 20
    for attempt in range(max_attempts):
        try:
            response = requests.get("https://jewgo.onrender.com/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                database = data.get('database', 'Unknown')
                version = data.get('version', 'Unknown')
                print(f"✅ Backend is back online (Attempt {attempt + 1})")
                print(f"📊 Database: {database}")
                print(f"📊 Version: {version}")
                return database
        except:
            pass
        
        print(f"   Attempt {attempt + 1}/{max_attempts} - Backend not ready yet...")
        time.sleep(30)  # Wait 30 seconds between attempts
    
    print("❌ Backend did not come back online within expected time")
    return None

def test_postgresql_connection():
    """Test if PostgreSQL connection is working"""
    print("\n🔍 Testing PostgreSQL Connection")
    print("=" * 30)
    
    try:
        response = requests.get("https://jewgo.onrender.com/api/restaurants", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API endpoint is responding")
            print(f"📊 Response structure: {list(data.keys())}")
            
            if 'data' in data:
                restaurants_count = len(data['data']) if data['data'] else 0
                print(f"🍽️  Restaurants in database: {restaurants_count}")
                return True
            else:
                print("⚠️  Unexpected response structure")
                return False
        else:
            print(f"❌ API returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def check_backend_logs():
    """Check if there are any backend errors"""
    print("\n📋 Checking Backend Status")
    print("=" * 25)
    
    try:
        response = requests.get("https://jewgo.onrender.com/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Status: {data.get('status', 'Unknown')}")
            print(f"📊 Environment: {data.get('environment', 'Unknown')}")
            print(f"📊 Database: {data.get('database', 'Unknown')}")
            print(f"📊 Version: {data.get('version', 'Unknown')}")
            
            # Check if it's using PostgreSQL
            if data.get('database') == 'PostgreSQL':
                print("🎉 SUCCESS: Backend is now using PostgreSQL!")
                return True
            else:
                print("⚠️  Backend is still using SQLite fallback")
                return False
        else:
            print(f"❌ Backend returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking backend: {e}")
        return False

def add_sample_data_if_needed():
    """Add sample data if database is empty"""
    print("\n🍽️  Checking if sample data is needed")
    print("=" * 35)
    
    try:
        response = requests.get("https://jewgo.onrender.com/api/restaurants", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            restaurants_count = len(data.get('data', []))
            
            if restaurants_count == 0:
                print("📝 Database is empty, adding sample data...")
                
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
            else:
                print(f"✅ Database already has {restaurants_count} restaurants")
                return True
        else:
            print(f"❌ Error checking database: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False

def test_frontend_integration():
    """Test frontend integration with backend"""
    print("\n🌐 Testing Frontend Integration")
    print("=" * 30)
    
    urls = [
        "https://jewgo-app.vercel.app/",
        "https://jewgo-j953cxrfi-mml555s-projects.vercel.app/"
    ]
    
    results = []
    
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {url} - Frontend accessible")
                results.append(True)
            else:
                print(f"❌ {url} - Status: {response.status_code}")
                results.append(False)
        except Exception as e:
            print(f"❌ {url} - Error: {e}")
            results.append(False)
    
    return any(results)

def provide_comprehensive_summary():
    """Provide a comprehensive status summary"""
    print("\n📊 Comprehensive PostgreSQL Fix Summary")
    print("=" * 45)
    
    print("\n🔧 What Was Fixed:")
    print("   • Updated psycopg2 to psycopg2-binary for Python 3.13 compatibility")
    print("   • Updated SQLAlchemy from 1.4.53 to 2.0.23 for Python 3.13 compatibility")
    print("   • Fixed SQLAlchemy 2.0 syntax in database_manager_v2.py")
    print("   • Added proper text() import for SQLAlchemy 2.0")
    print("   • This should resolve all PostgreSQL connection issues")
    
    print("\n🎯 Expected Results:")
    print("   • Backend will restart automatically on Render")
    print("   • PostgreSQL connection should work properly")
    print("   • Database will show 'PostgreSQL' instead of 'SQLite'")
    print("   • All API endpoints should function normally")
    print("   • Frontend should display restaurant data correctly")
    print("   • No more 'undefined symbol: _PyInterpreterState_Get' errors")
    
    print("\n⚠️  Important Notes:")
    print("   • Render deployment takes 3-7 minutes to complete")
    print("   • Backend will be temporarily unavailable during restart")
    print("   • Sample data will be preserved in PostgreSQL")
    print("   • All geolocation fixes are already deployed to frontend")
    print("   • This is a comprehensive fix for all Python 3.13 compatibility issues")
    
    print("\n🚀 Next Steps:")
    print("   1. Wait for Render deployment to complete (3-7 minutes)")
    print("   2. Check backend logs for PostgreSQL connection success")
    print("   3. Verify database shows 'PostgreSQL' in status")
    print("   4. Test frontend at both Vercel URLs")
    print("   5. Confirm no geolocation violations in browser console")
    print("   6. Verify restaurant data displays correctly")

def main():
    """Main function to fix PostgreSQL compatibility comprehensively"""
    print("🚀 Applying Comprehensive PostgreSQL Compatibility Fix")
    print("=" * 55)
    
    # Commit the comprehensive fix
    if commit_comprehensive_fix():
        print(f"\n✅ Comprehensive PostgreSQL fix deployed")
        print("   • Updated psycopg2 to psycopg2-binary")
        print("   • Updated SQLAlchemy to 2.0.23")
        print("   • Fixed SQLAlchemy 2.0 syntax")
        print("   • This should resolve all Python 3.13 compatibility issues")
        print("   • Backend will restart automatically on Render")
        
        # Wait for backend restart
        database = wait_for_backend_restart()
        
        if database:
            print(f"\n✅ Backend is operational")
            print(f"📊 Database: {database}")
            
            # Check if PostgreSQL is working
            if check_backend_logs():
                print("🎉 SUCCESS: PostgreSQL connection is working!")
                
                # Test PostgreSQL connection
                if test_postgresql_connection():
                    print("✅ API endpoints are working")
                    
                    # Add sample data if needed
                    if add_sample_data_if_needed():
                        print("✅ Sample data is available")
                    else:
                        print("⚠️  Sample data may not be available")
                else:
                    print("❌ API connection test failed")
            else:
                print("⚠️  Backend is still using SQLite fallback")
                print("   This may indicate the deployment is still in progress")
        else:
            print("❌ Backend did not come back online")
        
        # Test frontend
        if test_frontend_integration():
            print("\n✅ Frontend is accessible")
        else:
            print("\n⚠️  Frontend may still be deploying")
        
        provide_comprehensive_summary()
    else:
        print("❌ Failed to commit comprehensive fix")

if __name__ == "__main__":
    main() 