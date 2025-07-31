#!/usr/bin/env python3
"""
Debug script to identify exact schema mismatch issues
"""

import requests
import json
import time

REMOTE_BACKEND_URL = "https://jewgo.onrender.com"

def test_minimal_restaurant():
    """Test with minimal required fields only"""
    minimal_data = {
        "business_id": "test_001",
        "name": "Test Restaurant"
    }
    
    print("🧪 Testing minimal restaurant (required fields only)...")
    print(f"Data: {json.dumps(minimal_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{REMOTE_BACKEND_URL}/api/admin/restaurants",
            json=minimal_data,
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Minimal restaurant added successfully!")
                return True
            else:
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_with_optional_fields():
    """Test with optional fields"""
    test_data = {
        "business_id": "test_002",
        "name": "Test Restaurant 2",
        "website_link": "https://test.com",
        "phone_number": "(555) 123-4567",
        "address": "123 Test St",
        "city": "Test City",
        "state": "FL",
        "zip_code": "12345",
        "rating": 4.5,
        "price_range": "$$",
        "latitude": 25.7617,
        "longitude": -80.1918
    }
    
    print("\n🧪 Testing with optional fields...")
    print(f"Data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{REMOTE_BACKEND_URL}/api/admin/restaurants",
            json=test_data,
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Restaurant with optional fields added successfully!")
                return True
            else:
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_data_types():
    """Test different data types"""
    test_cases = [
        {
            "name": "Float rating",
            "data": {
                "business_id": "test_003",
                "name": "Test Restaurant 3",
                "rating": 4.5,
                "latitude": 25.7617,
                "longitude": -80.1918
            }
        },
        {
            "name": "String rating",
            "data": {
                "business_id": "test_004",
                "name": "Test Restaurant 4",
                "rating": "4.5",
                "latitude": "25.7617",
                "longitude": "-80.1918"
            }
        },
        {
            "name": "Null values",
            "data": {
                "business_id": "test_005",
                "name": "Test Restaurant 5",
                "rating": None,
                "latitude": None,
                "longitude": None
            }
        }
    ]
    
    print("\n🧪 Testing different data types...")
    
    for test_case in test_cases:
        print(f"\n--- Testing: {test_case['name']} ---")
        print(f"Data: {json.dumps(test_case['data'], indent=2)}")
        
        try:
            response = requests.post(
                f"{REMOTE_BACKEND_URL}/api/admin/restaurants",
                json=test_case['data'],
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print("✅ Success!")
                else:
                    print(f"❌ Failed: {result.get('error', 'Unknown error')}")
            else:
                print(f"❌ HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(1)  # Rate limiting

def check_database_status():
    """Check current database status"""
    print("\n📊 Checking database status...")
    
    try:
        # Check health
        health_response = requests.get(f"{REMOTE_BACKEND_URL}/health", timeout=10)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"Health: {health_data}")
        
        # Check restaurants count
        restaurants_response = requests.get(f"{REMOTE_BACKEND_URL}/api/restaurants?limit=1", timeout=10)
        if restaurants_response.status_code == 200:
            restaurants_data = restaurants_response.json()
            print(f"Restaurants count: {restaurants_data.get('count', 0)}")
            
    except Exception as e:
        print(f"❌ Error checking status: {e}")

def main():
    print("🔍 Debugging Schema Issues")
    print("=" * 50)
    
    # Check current status
    check_database_status()
    
    # Test minimal restaurant
    if test_minimal_restaurant():
        print("\n✅ Minimal restaurant works! The issue is with optional fields.")
        
        # Test with optional fields
        test_with_optional_fields()
        
        # Test data types
        test_data_types()
    else:
        print("\n❌ Even minimal restaurant fails. Check database connection or basic setup.")
    
    print("\n📋 Summary:")
    print("• If minimal restaurant works but others fail: Data type or field validation issue")
    print("• If all fail: Database connection or basic setup issue")
    print("• Check the specific error messages above for clues")

if __name__ == "__main__":
    main() 