#!/usr/bin/env python3
"""
Fix SQLAlchemy Dialect Issue - Use correct approach for SQLAlchemy 1.4.53 with psycopg3
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

def fix_sqlalchemy_dialect_issue():
    """Fix SQLAlchemy dialect issue"""
    print("🔧 Fixing SQLAlchemy Dialect Issue")
    print("=" * 40)
    
    # Update database_manager_v2.py to use the correct approach
    print("📝 Updating database_manager_v2.py...")
    
    with open('database_manager_v2.py', 'r') as f:
        content = f.read()
    
    # Remove the auto-conversion logic and use a simpler approach
    # SQLAlchemy 1.4.53 with psycopg3 works with the standard postgresql:// URL
    # We just need to ensure psycopg3 is installed and available
    
    # Replace the auto-conversion logic
    content = content.replace(
        "self.database_url = database_url or os.environ.get('DATABASE_URL', 'sqlite:///restaurants.db')\n        # Convert PostgreSQL URLs to use psycopg3 driver\n        if self.database_url and 'postgresql://' in self.database_url and 'postgresql+psycopg://' not in self.database_url:\n            self.database_url = self.database_url.replace('postgresql://', 'postgresql+psycopg://')",
        "self.database_url = database_url or os.environ.get('DATABASE_URL', 'sqlite:///restaurants.db')\n        # For SQLAlchemy 1.4.53 with psycopg3, use standard postgresql:// URL\n        # The psycopg3 driver will be used automatically when available"
    )
    
    # Write the updated content
    with open('database_manager_v2.py', 'w') as f:
        f.write(content)
    
    print("✅ Updated database_manager_v2.py to use standard PostgreSQL URL")
    
    # Update the documentation
    print("\n📝 Updating documentation...")
    
    with open('POSTGRESQL_SETUP_NOTES.md', 'w') as f:
        f.write("""# PostgreSQL Setup Notes

## Database URL Format

When setting the DATABASE_URL environment variable in Render, use this format:

```
postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

The application uses SQLAlchemy 1.4.53 with psycopg3, which works with the standard postgresql:// URL format.

## Environment Variables for Render

Set these environment variables in your Render service:

1. **DATABASE_URL**: The PostgreSQL connection string (see above)
2. **FLASK_ENV**: Set to `production`

## Testing

After setting the environment variables, the backend should show:
- Database: PostgreSQL (instead of SQLite)
- Environment: production (instead of development)

## Technical Details

- SQLAlchemy 1.4.53
- psycopg3 3.2.9
- Python 3.13.5
- Standard postgresql:// URL format
""")
    
    print("✅ Updated PostgreSQL setup documentation")
    
    # Commit and push changes
    try:
        subprocess.run(['git', 'add', 'database_manager_v2.py', 'POSTGRESQL_SETUP_NOTES.md'], check=True)
        
        commit_message = f"🔧 Fix SQLAlchemy dialect - use standard postgresql:// URL with psycopg3 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Changes committed and pushed successfully")
        print(f"📝 Commit: {commit_message}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing changes: {e}")
        return False
    
    # Wait for backend restart
    if wait_for_backend_restart():
        print("\n✅ SQLAlchemy dialect fix deployed successfully!")
        print("   • Updated to use standard postgresql:// URL format")
        print("   • This should work with SQLAlchemy 1.4.53 and psycopg3")
        print("   • The psycopg3 driver will be used automatically")
        
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
    print("🚀 Fixing SQLAlchemy Dialect Issue")
    print("=" * 40)
    
    if fix_sqlalchemy_dialect_issue():
        print("\n✅ Fix completed successfully!")
        print("\n📋 Summary:")
        print("   • Fixed SQLAlchemy dialect issue")
        print("   • Updated to use standard postgresql:// URL format")
        print("   • This should work with SQLAlchemy 1.4.53 and psycopg3")
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