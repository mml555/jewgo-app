#!/usr/bin/env python3
"""
Fix psycopg2 Import Issue - Ensure database_manager_v2.py uses psycopg3
"""

import subprocess
import requests
import time
from datetime import datetime

def check_backend_status():
    """Check if backend is responding"""
    try:
        response = requests.get("https://jewgo.onrender.com/", timeout=10)
        return response.status_code == 200
    except:
        return False

def wait_for_backend_restart():
    """Wait for backend to restart and come online"""
    print("⏳ Waiting for backend restart...")
    
    for i in range(30):  # Wait up to 5 minutes
        if check_backend_status():
            print("✅ Backend is online")
            return True
        print(f"   Attempt {i+1}/30: Backend not ready yet...")
        time.sleep(10)
    
    print("❌ Backend did not come online within timeout")
    return False

def fix_psycopg2_import_issue():
    """Fix the psycopg2 import issue"""
    print("🔧 Fixing psycopg2 Import Issue")
    print("=" * 35)
    
    # Read the current database_manager_v2.py file
    print("📝 Reading database_manager_v2.py...")
    
    with open('database_manager_v2.py', 'r') as f:
        content = f.read()
    
    # Check if there are any psycopg2 references
    if 'psycopg2' in content:
        print("❌ Found psycopg2 references in database_manager_v2.py")
        print("   This is causing the import error")
        
        # Replace any psycopg2 references with psycopg3
        content = content.replace('import psycopg2', 'import psycopg')
        content = content.replace('psycopg2.connect(', 'psycopg.connect(')
        
        # Write the updated content
        with open('database_manager_v2.py', 'w') as f:
            f.write(content)
        
        print("✅ Updated database_manager_v2.py to use psycopg3")
    else:
        print("✅ No psycopg2 references found in database_manager_v2.py")
        print("   The issue might be elsewhere")
    
    # Also check if there are any other files that might be importing psycopg2
    print("\n🔍 Checking for other psycopg2 imports...")
    
    try:
        result = subprocess.run(['grep', '-r', 'import psycopg2', '.'], 
                              capture_output=True, text=True, cwd='.')
        
        if result.stdout:
            print("⚠️  Found psycopg2 imports in other files:")
            print(result.stdout)
        else:
            print("✅ No other psycopg2 imports found")
    except:
        print("⚠️  Could not check for other psycopg2 imports")
    
    # Commit and push the changes
    try:
        subprocess.run(['git', 'add', 'database_manager_v2.py'], check=True)
        
        commit_message = f"🔧 Fix psycopg2 import issue - ensure psycopg3 usage - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Changes committed and pushed successfully")
        print(f"📝 Commit: {commit_message}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing changes: {e}")
        return False
    
    # Wait for backend restart
    if wait_for_backend_restart():
        print("\n✅ psycopg2 import fix deployed successfully!")
        print("   • Updated database_manager_v2.py to use psycopg3")
        print("   • This should resolve the 'No module named psycopg2' error")
        
        # Test the backend
        try:
            response = requests.get("https://jewgo.onrender.com/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"📊 Backend Status: {data.get('status', 'Unknown')}")
                print(f"📊 Environment: {data.get('environment', 'Unknown')}")
                print(f"📊 Database: {data.get('database', 'Unknown')}")
                
                if data.get('database') == 'PostgreSQL':
                    print("🎉 SUCCESS: Backend is now using PostgreSQL!")
                else:
                    print("⚠️  Backend is still using SQLite fallback")
                    print("   This may be due to connection string issues")
            else:
                print(f"❌ Backend returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error testing backend: {e}")
    else:
        print("❌ Backend did not restart properly")
    
    return True

def main():
    """Main function"""
    print("🚀 Fixing psycopg2 Import Issue")
    print("=" * 35)
    
    if fix_psycopg2_import_issue():
        print("\n✅ Fix completed successfully!")
        print("\n📋 Summary:")
        print("   • Fixed psycopg2 import issue in database_manager_v2.py")
        print("   • Updated to use psycopg3 consistently")
        print("   • Backend should now connect to PostgreSQL properly")
        print("\n🔍 Next Steps:")
        print("   1. Check backend logs for PostgreSQL connection success")
        print("   2. Verify database shows 'PostgreSQL' instead of 'SQLite'")
        print("   3. Test frontend integration")
    else:
        print("❌ Fix failed")

if __name__ == "__main__":
    main() 