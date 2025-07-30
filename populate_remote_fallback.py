#!/usr/bin/env python3
"""
Fallback script to populate remote backend when bulk import endpoint is not available
"""

import json
import requests
import time
import os
from datetime import datetime

# Remote backend URL
REMOTE_BACKEND_URL = "https://jewgo.onrender.com"

def load_local_data():
    """Load restaurant data from local JSON file"""
    try:
        with open('local_restaurants.json', 'r') as f:
            data = json.load(f)
            return data.get('restaurants', [])
    except FileNotFoundError:
        print("❌ local_restaurants.json not found!")
        return []
    except json.JSONDecodeError:
        print("❌ Invalid JSON in local_restaurants.json!")
        return []

def check_remote_backend():
    """Check remote backend status"""
    try:
        response = requests.get(f"{REMOTE_BACKEND_URL}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Remote backend is accessible")
            print(f"📊 Available endpoints: {list(data.get('endpoints', {}).keys())}")
            return data
        else:
            print(f"❌ Remote backend returned status {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"❌ Cannot connect to remote backend: {e}")
        return None

def get_remote_restaurants():
    """Get current restaurants from remote backend"""
    try:
        response = requests.get(f"{REMOTE_BACKEND_URL}/api/restaurants", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('restaurants', [])
        else:
            print(f"❌ Failed to get remote restaurants: {response.status_code}")
            return []
    except requests.RequestException as e:
        print(f"❌ Error getting remote restaurants: {e}")
        return []

def try_individual_restaurant_add(restaurant):
    """Try to add a single restaurant using the existing POST endpoint"""
    try:
        # Use the existing single restaurant endpoint
        response = requests.post(
            f"{REMOTE_BACKEND_URL}/api/admin/restaurants",
            json=restaurant,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('success', False)
        else:
            return False
            
    except requests.RequestException:
        return False

def populate_via_individual_requests(restaurants, batch_size=10):
    """Populate by adding restaurants one by one"""
    print(f"🚀 Attempting to populate via individual requests...")
    print(f"📊 Total restaurants to add: {len(restaurants)}")
    
    success_count = 0
    error_count = 0
    
    for i, restaurant in enumerate(restaurants):
        try:
            if try_individual_restaurant_add(restaurant):
                success_count += 1
                if success_count % 10 == 0:
                    print(f"✅ Progress: {success_count}/{len(restaurants)} restaurants added")
            else:
                error_count += 1
                
            # Add a small delay to avoid overwhelming the server
            time.sleep(0.1)
            
        except Exception as e:
            error_count += 1
            print(f"❌ Error adding restaurant {i}: {e}")
    
    print(f"📊 Final Results:")
    print(f"   ✅ Success: {success_count}")
    print(f"   ❌ Errors: {error_count}")
    
    return success_count > 0

def create_manual_import_script(restaurants):
    """Create a manual import script for the user"""
    script_content = f'''#!/usr/bin/env python3
"""
Manual import script for {len(restaurants)} restaurants
Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

import requests
import json
import time

# Remote backend URL
REMOTE_BACKEND_URL = "{REMOTE_BACKEND_URL}"

# Restaurant data
restaurants = {json.dumps(restaurants, indent=2)}

def add_restaurant(restaurant):
    try:
        response = requests.post(
            f"{{REMOTE_BACKEND_URL}}/api/admin/restaurants",
            json=restaurant,
            timeout=10
        )
        return response.status_code == 200
    except:
        return False

def main():
    print(f"🚀 Adding {{len(restaurants)}} restaurants...")
    
    success_count = 0
    for i, restaurant in enumerate(restaurants):
        if add_restaurant(restaurant):
            success_count += 1
            if success_count % 10 == 0:
                print(f"✅ Added {{success_count}} restaurants...")
        else:
            print(f"❌ Failed to add restaurant {{i+1}}: {{restaurant.get('name', 'Unknown')}}")
        
        time.sleep(0.1)  # Small delay
    
    print(f"🎉 Completed! {{success_count}} restaurants added successfully")

if __name__ == "__main__":
    main()
'''
    
    filename = f"manual_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    with open(filename, 'w') as f:
        f.write(script_content)
    
    print(f"📝 Created manual import script: {filename}")
    return filename

def create_database_export(restaurants):
    """Create a database export file for manual import"""
    filename = f"restaurants_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    export_data = {
        'export_date': datetime.now().isoformat(),
        'total_restaurants': len(restaurants),
        'restaurants': restaurants
    }
    
    with open(filename, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"📝 Created database export: {filename}")
    return filename

def main():
    print("🚀 Starting fallback remote backend population...")
    print("=" * 60)
    
    # Check remote backend
    backend_info = check_remote_backend()
    if not backend_info:
        print("❌ Cannot proceed - remote backend not accessible")
        return
    
    # Load local data
    local_restaurants = load_local_data()
    if not local_restaurants:
        print("❌ No local restaurant data found!")
        return
    
    print(f"📊 Found {len(local_restaurants)} local restaurants")
    
    # Check remote data
    remote_restaurants = get_remote_restaurants()
    print(f"📊 Remote backend has {len(remote_restaurants)} restaurants")
    
    if len(remote_restaurants) > 0:
        print("⚠️  Remote backend already has data!")
        response = input("   Do you want to continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("   Aborting...")
            return
    
    print("\n" + "=" * 60)
    print("🔄 Starting fallback population methods...")
    
    # Method 1: Try individual restaurant additions
    print("\n📡 Method 1: Individual Restaurant Additions")
    print("   (This may take a while for large datasets)")
    
    response = input("   Try individual restaurant additions? (y/N): ")
    if response.lower() == 'y':
        # Limit to first 50 restaurants for testing
        test_restaurants = local_restaurants[:50]
        print(f"   Testing with first {len(test_restaurants)} restaurants...")
        
        if populate_via_individual_requests(test_restaurants):
            print("✅ Individual additions successful!")
            
            # Ask if user wants to continue with all restaurants
            response = input("   Continue with all restaurants? (y/N): ")
            if response.lower() == 'y':
                populate_via_individual_requests(local_restaurants)
        else:
            print("❌ Individual additions failed")
    
    # Method 2: Create manual import script
    print("\n📝 Method 2: Manual Import Script")
    response = input("   Create manual import script? (y/N): ")
    if response.lower() == 'y':
        script_file = create_manual_import_script(local_restaurants)
        print(f"   Run: python {script_file}")
    
    # Method 3: Create database export
    print("\n💾 Method 3: Database Export")
    response = input("   Create database export file? (y/N): ")
    if response.lower() == 'y':
        export_file = create_database_export(local_restaurants)
        print(f"   Export file: {export_file}")
    
    print("\n" + "=" * 60)
    print("📋 Summary of Available Methods:")
    print("1. ✅ Individual restaurant additions (if endpoint available)")
    print("2. 📝 Manual import script (for manual execution)")
    print("3. 💾 Database export file (for manual import)")
    print("4. 🔧 Wait for bulk import endpoint to be deployed")
    print("5. 🗄️  Direct database access (requires credentials)")

if __name__ == "__main__":
    main() 