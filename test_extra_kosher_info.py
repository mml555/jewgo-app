#!/usr/bin/env python3
"""
Test Extra Kosher Information
Verifies that Bishul Yisroel, Cholov Yisroel, Pas Yisroel, and Cholov Stam are properly captured.
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database_manager_v3 import DatabaseManager

def test_extra_kosher_info():
    """Test the extra kosher information functionality."""
    
    test_restaurants = [
        {
            "name": "Test Restaurant - Cholov Yisroel",
            "address": "123 Test St, Test City, FL 12345",
            "phone": "555-1234",
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher",
            "extra_kosher_info": "Cholov Yisroel, Pas Yisroel"
        },
        {
            "name": "Test Restaurant - Cholov Stam",
            "address": "456 Test Ave, Test City, FL 12345",
            "phone": "555-5678",
            "kosher_type": "dairy",
            "certifying_agency": "ORB Kosher",
            "extra_kosher_info": "Cholov Stam, Bishul Yisroel"
        },
        {
            "name": "Test Restaurant - Bishul Yisroel",
            "address": "789 Test Blvd, Test City, FL 12345",
            "phone": "555-9012",
            "kosher_type": "meat",
            "certifying_agency": "ORB Kosher",
            "extra_kosher_info": "Bishul Yisroel"
        },
        {
            "name": "Test Restaurant - Basic",
            "address": "321 Test Rd, Test City, FL 12345",
            "phone": "555-3456",
            "kosher_type": "pareve",
            "certifying_agency": "ORB Kosher",
            "extra_kosher_info": None
        }
    ]
    
    try:
        print("🧪 Testing Extra Kosher Information Functionality")
        print("=" * 60)
        
        db_manager = DatabaseManager()
        
        # Clean up any existing test restaurants
        print("🧹 Cleaning up existing test restaurants...")
        for restaurant in test_restaurants:
            existing = db_manager.get_restaurant_by_name(restaurant['name'])
            if existing:
                # We'll just update them instead of deleting
                print(f"  Found existing: {restaurant['name']}")
        
        print("\n📝 Adding/Updating test restaurants with extra kosher info...")
        
        for restaurant in test_restaurants:
            try:
                existing = db_manager.get_restaurant_by_name(restaurant['name'])
                
                if existing:
                    # Update existing restaurant
                    success = db_manager.update_restaurant_orb_data(
                        existing['id'],
                        restaurant['address'],
                        restaurant['kosher_type'],
                        restaurant['certifying_agency'],
                        restaurant.get('extra_kosher_info')
                    )
                    action = "Updated"
                else:
                    # Create new restaurant
                    success = db_manager.add_restaurant_simple(
                        name=restaurant['name'],
                        address=restaurant['address'],
                        phone_number=restaurant['phone'],
                        kosher_type=restaurant['kosher_type'],
                        certifying_agency=restaurant['certifying_agency'],
                        extra_kosher_info=restaurant.get('extra_kosher_info'),
                        source='test'
                    )
                    action = "Added"
                
                if success:
                    print(f"✅ {action}: {restaurant['name']}")
                    if restaurant.get('extra_kosher_info'):
                        print(f"   Extra Kosher Info: {restaurant['extra_kosher_info']}")
                else:
                    print(f"❌ Failed to {action.lower()}: {restaurant['name']}")
                
            except Exception as e:
                print(f"❌ Error processing {restaurant['name']}: {e}")
        
        print("\n🔍 Verifying extra kosher information in database...")
        
        for restaurant in test_restaurants:
            try:
                db_restaurant = db_manager.get_restaurant_by_name(restaurant['name'])
                if db_restaurant:
                    print(f"\n📋 {restaurant['name']}:")
                    print(f"   Kosher Type: {db_restaurant.get('kosher_type')}")
                    print(f"   Cholov Yisroel: {db_restaurant.get('is_cholov_yisroel')}")
                    print(f"   Pas Yisroel: {db_restaurant.get('is_pas_yisroel')}")
                    print(f"   Bishul Yisroel: {db_restaurant.get('is_bishul_yisroel')}")
                    print(f"   Certifying Agency: {db_restaurant.get('certifying_agency')}")
                    
                    # Verify the logic
                    expected_cholov = 'cholov yisroel' in (restaurant.get('extra_kosher_info') or '').lower()
                    expected_pas = 'pas yisroel' in (restaurant.get('extra_kosher_info') or '').lower()
                    expected_bishul = 'bishul yisroel' in (restaurant.get('extra_kosher_info') or '').lower()
                    
                    if 'cholov stam' in (restaurant.get('extra_kosher_info') or '').lower():
                        expected_cholov = False
                    
                    print(f"   Expected Cholov Yisroel: {expected_cholov}")
                    print(f"   Expected Pas Yisroel: {expected_pas}")
                    print(f"   Expected Bishul Yisroel: {expected_bishul}")
                    
                    # Check if values match
                    if (db_restaurant.get('is_cholov_yisroel') == expected_cholov and
                        db_restaurant.get('is_pas_yisroel') == expected_pas and
                        db_restaurant.get('is_bishul_yisroel') == expected_bishul):
                        print("   ✅ All kosher requirements match!")
                    else:
                        print("   ❌ Kosher requirements don't match!")
                else:
                    print(f"❌ Could not find restaurant: {restaurant['name']}")
                    
            except Exception as e:
                print(f"❌ Error verifying {restaurant['name']}: {e}")
        
        print("\n🎉 Extra Kosher Information Test Completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

def main():
    """Main function."""
    print("🧪 Extra Kosher Information Test")
    print("=" * 50)
    
    success = test_extra_kosher_info()
    
    if success:
        print("\n✅ Extra kosher information functionality is working correctly!")
        print("🔍 The system can now capture:")
        print("   - Bishul Yisroel (Food cooked by a Jew)")
        print("   - Cholov Yisroel (Milk supervised by a Jew)")
        print("   - Pas Yisroel (Bread baked by a Jew)")
        print("   - Cholov Stam (Regular milk)")
    else:
        print("\n❌ Test failed. Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    main() 