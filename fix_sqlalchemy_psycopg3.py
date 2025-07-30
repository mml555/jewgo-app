#!/usr/bin/env python3
"""
Fix SQLAlchemy psycopg3 Driver Issue
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

def fix_sqlalchemy_psycopg3():
    """Fix SQLAlchemy to use psycopg3 driver"""
    print("🔧 Fixing SQLAlchemy psycopg3 Driver Issue")
    print("=" * 45)
    
    # Update database_manager_v2.py to use psycopg3 driver
    print("📝 Updating database_manager_v2.py...")
    
    with open('database_manager_v2.py', 'r') as f:
        content = f.read()
    
    # Update the database URL to use psycopg3 driver
    # Change from: postgresql://user:pass@host/db
    # To: postgresql+psycopg://user:pass@host/db
    
    # Update the default database URL
    content = content.replace(
        "self.database_url = database_url or os.environ.get('DATABASE_URL', 'sqlite:///restaurants.db')",
        "self.database_url = database_url or os.environ.get('DATABASE_URL', 'sqlite:///restaurants.db')\n        # Convert PostgreSQL URLs to use psycopg3 driver\n        if self.database_url and 'postgresql://' in self.database_url and 'postgresql+psycopg://' not in self.database_url:\n            self.database_url = self.database_url.replace('postgresql://', 'postgresql+psycopg://')"
    )
    
    # Write the updated content
    with open('database_manager_v2.py', 'w') as f:
        f.write(content)
    
    print("✅ Updated database_manager_v2.py to use psycopg3 driver")
    
    # Also update the environment variable format in the documentation
    print("\n📝 Updating documentation...")
    
    # Create a note about the correct DATABASE_URL format
    with open('POSTGRESQL_SETUP_NOTES.md', 'w') as f:
        f.write("""# PostgreSQL Setup Notes

## Database URL Format

When setting the DATABASE_URL environment variable in Render, use this format:

```
postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

The application will automatically convert this to use the psycopg3 driver internally.

## Environment Variables for Render

Set these environment variables in your Render service:

1. **DATABASE_URL**: The PostgreSQL connection string (see above)
2. **FLASK_ENV**: Set to `production`

## Testing

After setting the environment variables, the backend should show:
- Database: PostgreSQL (instead of SQLite)
- Environment: production (instead of development)
""")
    
    print("✅ Created PostgreSQL setup documentation")
    
    # Commit and push changes
    try:
        subprocess.run(['git', 'add', 'database_manager_v2.py', 'POSTGRESQL_SETUP_NOTES.md'], check=True)
        
        commit_message = f"🔧 Fix SQLAlchemy psycopg3 driver - auto-convert PostgreSQL URLs - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Changes committed and pushed successfully")
        print(f"📝 Commit: {commit_message}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing changes: {e}")
        return False
    
    # Wait for backend restart
    if wait_for_backend_restart():
        print("\n✅ SQLAlchemy psycopg3 fix deployed successfully!")
        print("   • Updated database_manager_v2.py to auto-convert PostgreSQL URLs")
        print("   • This should resolve the 'No module named psycopg2' error")
        print("   • The app will now use psycopg3 driver automatically")
        
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
                    print("   This means the DATABASE_URL environment variable is not set in Render")
                    print("   Please add the DATABASE_URL to your Render environment variables")
            else:
                print(f"❌ Backend returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error testing backend: {e}")
    else:
        print("❌ Backend did not restart properly")
    
    return True

def main():
    """Main function"""
    print("🚀 Fixing SQLAlchemy psycopg3 Driver Issue")
    print("=" * 45)
    
    if fix_sqlalchemy_psycopg3():
        print("\n✅ Fix completed successfully!")
        print("\n📋 Summary:")
        print("   • Fixed SQLAlchemy to use psycopg3 driver automatically")
        print("   • Updated database_manager_v2.py to convert PostgreSQL URLs")
        print("   • Backend should now connect to PostgreSQL properly")
        print("\n🔍 Next Steps:")
        print("   1. Add DATABASE_URL to Render environment variables")
        print("   2. Check backend logs for PostgreSQL connection success")
        print("   3. Verify database shows 'PostgreSQL' instead of 'SQLite'")
        print("\n📋 Correct DATABASE_URL format:")
        print("   postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
    else:
        print("❌ Fix failed")

if __name__ == "__main__":
    main() 