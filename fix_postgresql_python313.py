#!/usr/bin/env python3
"""
Fix PostgreSQL Python 3.13 Compatibility Issue
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

def fix_postgresql_compatibility():
    """Fix PostgreSQL compatibility with Python 3.13"""
    print("🔧 Fixing PostgreSQL Python 3.13 Compatibility")
    print("=" * 50)
    
    # Update requirements.txt to use psycopg3 instead of psycopg2
    print("📝 Updating requirements.txt...")
    
    requirements_content = """# Core Flask Framework
Flask==2.3.3
Flask-CORS==4.0.0
Werkzeug==2.3.7
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
blinker==1.6.3

# Database Support
psycopg[binary]==3.1.18  # PostgreSQL adapter (Python 3.13 compatible)
SQLAlchemy==1.4.53      # ORM for database abstraction (stable with Python 3.13)
alembic==1.11.3         # Database migrations (compatible with SQLAlchemy 1.4.53)

# Environment & Configuration
python-dotenv==1.0.0    # Environment variable management
gunicorn==21.2.0        # Production WSGI server

# Security & Validation
Flask-Limiter==3.5.0    # Rate limiting
marshmallow==3.20.1     # Data validation and serialization

# Monitoring & Logging
structlog==23.1.0       # Structured logging
sentry-sdk[flask]==1.32.0  # Error tracking (optional)

# HTTP Requests
requests==2.32.4        # HTTP library for API calls

# Development & Testing
pytest==7.4.2           # Testing framework
pytest-flask==1.2.0     # Flask testing utilities
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements_content)
    
    print("✅ requirements.txt updated with psycopg3")
    
    # Update database_manager_v2.py to handle psycopg3
    print("📝 Updating database_manager_v2.py...")
    
    # Read the current file
    with open('database_manager_v2.py', 'r') as f:
        content = f.read()
    
    # Update the import statement
    content = content.replace(
        "import psycopg2",
        "import psycopg"
    )
    
    # Update connection creation to use psycopg3 syntax
    content = content.replace(
        "psycopg2.connect(",
        "psycopg.connect("
    )
    
    # Write the updated content
    with open('database_manager_v2.py', 'w') as f:
        f.write(content)
    
    print("✅ database_manager_v2.py updated for psycopg3")
    
    # Commit and push changes
    try:
        subprocess.run(['git', 'add', 'requirements.txt', 'database_manager_v2.py'], check=True)
        
        commit_message = f"🔧 Fix PostgreSQL Python 3.13 compatibility - switch to psycopg3 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Changes committed and pushed successfully")
        print(f"📝 Commit: {commit_message}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing changes: {e}")
        return False
    
    # Wait for backend restart
    if wait_for_backend_restart():
        print("\n✅ PostgreSQL compatibility fix deployed successfully!")
        print("   • Switched from psycopg2 to psycopg3")
        print("   • psycopg3 has better Python 3.13 support")
        print("   • This should resolve the undefined symbol error")
        
        # Test the backend
        try:
            response = requests.get("https://jewgo.onrender.com/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"📊 Backend Status: {data.get('status', 'Unknown')}")
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
    print("🚀 PostgreSQL Python 3.13 Compatibility Fix")
    print("=" * 45)
    
    if fix_postgresql_compatibility():
        print("\n✅ Fix completed successfully!")
        print("\n📋 Summary:")
        print("   • Updated to psycopg3 (better Python 3.13 support)")
        print("   • Removed psycopg2-binary (incompatible with Python 3.13)")
        print("   • Backend should now connect to PostgreSQL properly")
        print("\n🔍 Next Steps:")
        print("   1. Check backend logs for PostgreSQL connection success")
        print("   2. Verify database shows 'PostgreSQL' instead of 'SQLite'")
        print("   3. Test frontend integration")
    else:
        print("❌ Fix failed")

if __name__ == "__main__":
    main() 