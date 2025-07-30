#!/usr/bin/env python3
"""
Alternative Import Methods - Multiple approaches for restaurant data import
"""

import json
import requests
import time
import csv
import sqlite3
from datetime import datetime
from typing import List, Dict, Any

class AlternativeImportMethods:
    def __init__(self):
        self.base_url = "https://jewgo.onrender.com"
        self.session = requests.Session()
        self.session.timeout = 30
        
    def method_1_bulk_import_api(self, restaurants: List[Dict[str, Any]]):
        """
        Method 1: Use bulk import API endpoint
        """
        print("🔄 Method 1: Bulk Import API")
        print("=" * 40)
        
        # Check if bulk import endpoint exists
        try:
            response = self.session.get(f"{self.base_url}/api/admin/restaurants/bulk")
            if response.status_code == 405:  # Method not allowed, but endpoint exists
                print("✅ Bulk import endpoint exists")
                
                # Prepare bulk data
                bulk_data = {
                    "restaurants": restaurants[:50]  # Limit to 50 for testing
                }
                
                response = self.session.post(
                    f"{self.base_url}/api/admin/restaurants/bulk",
                    json=bulk_data,
                    timeout=60
                )
                
                if response.status_code == 200:
                    print("✅ Bulk import successful")
                    return True
                else:
                    print(f"❌ Bulk import failed: {response.status_code}")
                    return False
            else:
                print("❌ Bulk import endpoint not available")
                return False
                
        except Exception as e:
            print(f"❌ Bulk import error: {e}")
            return False
    
    def method_2_staged_import(self, restaurants: List[Dict[str, Any]]):
        """
        Method 2: Staged import with validation at each stage
        """
        print("\n🔄 Method 2: Staged Import")
        print("=" * 40)
        
        stages = [
            {"name": "Basic Info", "fields": ["business_id", "name", "city", "state"]},
            {"name": "Contact Info", "fields": ["phone_number", "website_link", "address"]},
            {"name": "Kosher Info", "fields": ["certifying_agency", "kosher_category"]},
            {"name": "Full Data", "fields": ["rating", "latitude", "longitude", "notes"]}
        ]
        
        successful_imports = 0
        
        for restaurant in restaurants[:10]:  # Test with first 10
            print(f"\n📋 Processing: {restaurant.get('name', 'Unknown')}")
            
            # Stage 1: Basic info
            stage1_data = {field: restaurant.get(field, '') for field in stages[0]["fields"]}
            stage1_data.update({
                'certifying_agency': 'ORB',
                'kosher_category': 'unknown',
                'listing_type': 'restaurant',
                'status': 'active'
            })
            
            try:
                response = self.session.post(
                    f"{self.base_url}/api/admin/restaurants",
                    json=stage1_data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    print(f"✅ Stage 1 successful")
                    successful_imports += 1
                else:
                    print(f"❌ Stage 1 failed: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Stage 1 error: {e}")
            
            time.sleep(2)  # Delay between restaurants
        
        print(f"\n📊 Staged import completed: {successful_imports} successful")
        return successful_imports > 0
    
    def method_3_csv_import(self, restaurants: List[Dict[str, Any]]):
        """
        Method 3: Export to CSV and import via file upload
        """
        print("\n🔄 Method 3: CSV Import")
        print("=" * 40)
        
        # Create CSV file
        csv_filename = "restaurants_import.csv"
        
        try:
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                # Define CSV headers based on database schema
                fieldnames = [
                    'business_id', 'name', 'website_link', 'phone_number', 'address',
                    'city', 'state', 'zip_code', 'certificate_link', 'image_url',
                    'certifying_agency', 'kosher_category', 'listing_type', 'status',
                    'rating', 'price_range', 'hours_of_operation', 'short_description',
                    'notes', 'latitude', 'longitude', 'data_source', 'external_id'
                ]
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for restaurant in restaurants[:20]:  # Export first 20 for testing
                    # Prepare CSV row
                    csv_row = {}
                    for field in fieldnames:
                        value = restaurant.get(field, '')
                        if field == 'certifying_agency':
                            value = 'ORB'  # Default value
                        elif field == 'kosher_category':
                            value = restaurant.get(field, 'unknown')
                        elif field in ['rating', 'latitude', 'longitude']:
                            try:
                                value = float(restaurant.get(field, 0)) if restaurant.get(field) else ''
                            except:
                                value = ''
                        else:
                            value = str(restaurant.get(field, ''))
                        
                        csv_row[field] = value
                    
                    writer.writerow(csv_row)
            
            print(f"✅ CSV file created: {csv_filename}")
            print(f"📊 Exported {min(20, len(restaurants))} restaurants to CSV")
            
            # Try to upload CSV file (if endpoint exists)
            try:
                with open(csv_filename, 'rb') as f:
                    files = {'file': (csv_filename, f, 'text/csv')}
                    response = self.session.post(
                        f"{self.base_url}/api/admin/restaurants/import-csv",
                        files=files,
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        print("✅ CSV import successful")
                        return True
                    else:
                        print(f"❌ CSV import failed: {response.status_code}")
                        return False
                        
            except Exception as e:
                print(f"❌ CSV upload error: {e}")
                print("📋 CSV file created for manual import")
                return False
                
        except Exception as e:
            print(f"❌ CSV creation error: {e}")
            return False
    
    def method_4_direct_database_insertion(self, restaurants: List[Dict[str, Any]]):
        """
        Method 4: Direct database insertion (if we had database access)
        """
        print("\n🔄 Method 4: Direct Database Insertion")
        print("=" * 40)
        
        print("⚠️ This method requires direct database access")
        print("📋 Would require:")
        print("   - Database connection credentials")
        print("   - Direct SQL insertion")
        print("   - Bypass API validation")
        
        # This is a theoretical approach
        sample_sql = """
        INSERT INTO restaurants (
            business_id, name, website_link, phone_number, address,
            city, state, zip_code, certificate_link, image_url,
            certifying_agency, kosher_category, listing_type, status,
            rating, price_range, hours_of_operation, short_description,
            notes, latitude, longitude, data_source, external_id,
            created_at, updated_at
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, NOW(), NOW()
        )
        """
        
        print(f"📋 Sample SQL for {len(restaurants)} restaurants would be generated")
        return False
    
    def method_5_manual_import_script(self, restaurants: List[Dict[str, Any]]):
        """
        Method 5: Generate manual import script
        """
        print("\n🔄 Method 5: Manual Import Script")
        print("=" * 40)
        
        script_filename = "manual_import_script.py"
        
        try:
            with open(script_filename, 'w') as f:
                f.write("#!/usr/bin/env python3\n")
                f.write('"""Manual Import Script - Generated for manual execution"""\n\n')
                f.write("import requests\n")
                f.write("import time\n\n")
                f.write("def manual_import():\n")
                f.write("    base_url = 'https://jewgo.onrender.com'\n")
                f.write("    session = requests.Session()\n\n")
                
                for i, restaurant in enumerate(restaurants[:10]):  # First 10 for script
                    f.write(f"    # Restaurant {i+1}: {restaurant.get('name', 'Unknown')}\n")
                    f.write("    try:\n")
                    f.write("        response = session.post(\n")
                    f.write("            f'{base_url}/api/admin/restaurants',\n")
                    f.write("            json={\n")
                    
                    # Write restaurant data
                    for key, value in restaurant.items():
                        if isinstance(value, str):
                            f.write(f"                '{key}': '{value}',\n")
                        elif value is None:
                            f.write(f"                '{key}': None,\n")
                        else:
                            f.write(f"                '{key}': {value},\n")
                    
                    f.write("            },\n")
                    f.write("            timeout=30\n")
                    f.write("        )\n")
                    f.write("        print(f'Restaurant {i+1}: {response.status_code}')\n")
                    f.write("    except Exception as e:\n")
                    f.write(f"        print(f'Restaurant {i+1}: Error - {{e}}')\n")
                    f.write("    time.sleep(5)\n\n")
                
                f.write("if __name__ == '__main__':\n")
                f.write("    manual_import()\n")
            
            print(f"✅ Manual import script created: {script_filename}")
            print("📋 You can run this script manually when backend is stable")
            return True
            
        except Exception as e:
            print(f"❌ Script creation error: {e}")
            return False
    
    def method_6_validation_bypass_import(self, restaurants: List[Dict[str, Any]]):
        """
        Method 6: Import with minimal validation (bypass strict checks)
        """
        print("\n🔄 Method 6: Validation Bypass Import")
        print("=" * 40)
        
        successful_imports = 0
        
        for restaurant in restaurants[:5]:  # Test with first 5
            # Create minimal restaurant data with only required fields
            minimal_data = {
                'business_id': restaurant.get('business_id', f'minimal_{successful_imports + 1}'),
                'name': restaurant.get('name', f'Minimal Restaurant {successful_imports + 1}'),
                'city': restaurant.get('city', 'Unknown'),
                'state': restaurant.get('state', 'FL'),
                'certifying_agency': 'ORB',
                'kosher_category': 'unknown',
                'listing_type': 'restaurant',
                'status': 'active'
            }
            
            try:
                response = self.session.post(
                    f"{self.base_url}/api/admin/restaurants",
                    json=minimal_data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    print(f"✅ Minimal import successful: {minimal_data['name']}")
                    successful_imports += 1
                else:
                    print(f"❌ Minimal import failed: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Minimal import error: {e}")
            
            time.sleep(3)  # Longer delay for minimal approach
        
        print(f"\n📊 Validation bypass completed: {successful_imports} successful")
        return successful_imports > 0
    
    def run_all_methods(self):
        """
        Run all alternative import methods
        """
        print("🚀 Alternative Import Methods")
        print("=" * 60)
        
        # Load restaurant data
        try:
            with open('local_restaurants.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            restaurants = data.get('restaurants', [])
            print(f"📂 Loaded {len(restaurants)} restaurants for testing")
            
        except Exception as e:
            print(f"❌ Error loading restaurant data: {e}")
            return
        
        # Test each method
        methods = [
            self.method_1_bulk_import_api,
            self.method_2_staged_import,
            self.method_3_csv_import,
            self.method_4_direct_database_insertion,
            self.method_5_manual_import_script,
            self.method_6_validation_bypass_import
        ]
        
        results = {}
        
        for i, method in enumerate(methods, 1):
            print(f"\n{'='*60}")
            print(f"Testing Method {i}")
            print(f"{'='*60}")
            
            try:
                result = method(restaurants)
                results[f"Method {i}"] = result
                print(f"Method {i} result: {'✅ Success' if result else '❌ Failed'}")
            except Exception as e:
                print(f"Method {i} error: {e}")
                results[f"Method {i}"] = False
        
        # Summary
        print(f"\n{'='*60}")
        print("📊 Alternative Methods Summary")
        print(f"{'='*60}")
        
        for method_name, result in results.items():
            status = "✅ Success" if result else "❌ Failed"
            print(f"{method_name}: {status}")
        
        successful_methods = sum(1 for result in results.values() if result)
        print(f"\n🎯 Successful methods: {successful_methods}/{len(methods)}")

def main():
    """Main function"""
    importer = AlternativeImportMethods()
    importer.run_all_methods()

if __name__ == "__main__":
    main() 