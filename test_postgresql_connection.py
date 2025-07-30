#!/usr/bin/env python3
"""
Test PostgreSQL Connection and Environment Variables
"""

import os
import requests
import json
from datetime import datetime

def check_backend_status():
    """Check current backend status"""
    print("🔍 Current Backend Status")
    print("=" * 25)
    
    try:
        response = requests.get("https://jewgo.onrender.com/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Status: {data.get('status', 'Unknown')}")
            print(f"📊 Environment: {data.get('environment', 'Unknown')}")
            print(f"📊 Database: {data.get('database', 'Unknown')}")
            print(f"📊 Version: {data.get('version', 'Unknown')}")
            return data
        else:
            print(f"❌ Backend returned status: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error checking backend: {e}")
        return None

def test_postgresql_connection():
    """Test PostgreSQL connection directly"""
    print("\n🗄️  Testing PostgreSQL Connection")
    print("=" * 35)
    
    # Test with psycopg3
    try:
        import psycopg
        print("✅ psycopg3 is available")
        
        # Get the database URL from the logs
        database_url = "postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
        
        print(f"📋 Testing connection to: {database_url.split('@')[1] if '@' in database_url else 'Unknown'}")
        
        # Test connection
        with psycopg.connect(database_url, connect_timeout=10) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version()")
                version = cur.fetchone()
                print(f"✅ PostgreSQL connection successful!")
                print(f"📊 PostgreSQL version: {version[0] if version else 'Unknown'}")
                return True
                
    except ImportError:
        print("❌ psycopg3 is not available")
        return False
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def check_environment_variables():
    """Check environment variables"""
    print("\n🔧 Environment Variables Check")
    print("=" * 30)
    
    # Check local environment
    print("📋 Local Environment:")
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        print(f"   • DATABASE_URL: {database_url.split('@')[1] if '@' in database_url else 'Set'}")
    else:
        print("   • DATABASE_URL: Not set")
    
    flask_env = os.environ.get('FLASK_ENV')
    print(f"   • FLASK_ENV: {flask_env or 'Not set'}")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("   • .env file: Exists")
        with open('.env', 'r') as f:
            content = f.read()
            if 'DATABASE_URL' in content:
                print("   • DATABASE_URL in .env: Yes")
            else:
                print("   • DATABASE_URL in .env: No")
    else:
        print("   • .env file: Does not exist")

def check_render_environment():
    """Check Render environment variables"""
    print("\n☁️  Render Environment Check")
    print("=" * 30)
    
    print("📋 Render Environment Variables:")
    print("   • These are set in the Render dashboard")
    print("   • DATABASE_URL should be set to PostgreSQL connection string")
    print("   • FLASK_ENV should be set to 'production'")
    
    print("\n🔧 To check Render environment variables:")
    print("   1. Go to https://dashboard.render.com")
    print("   2. Select your jewgo-backend service")
    print("   3. Go to 'Environment' tab")
    print("   4. Check if DATABASE_URL is set correctly")

def create_connection_test_script():
    """Create a script to test connection on Render"""
    print("\n🔧 Creating Connection Test Script")
    print("=" * 35)
    
    script_content = """#!/usr/bin/env python3
\"\"\"
PostgreSQL Connection Test Script
Run this on Render to test the connection
\"\"\"

import os
import sys

def test_connection():
    print("🔍 Testing PostgreSQL Connection on Render")
    print("=" * 40)
    
    # Check environment variables
    print("📋 Environment Variables:")
    database_url = os.environ.get('DATABASE_URL')
    flask_env = os.environ.get('FLASK_ENV')
    
    print(f"   • DATABASE_URL: {'Set' if database_url else 'Not set'}")
    print(f"   • FLASK_ENV: {flask_env or 'Not set'}")
    
    if database_url:
        print(f"   • Database host: {database_url.split('@')[1].split('/')[0] if '@' in database_url else 'Unknown'}")
    
    # Test psycopg3
    try:
        import psycopg
        print("\\n✅ psycopg3 is available")
        
        if database_url:
            print("\\n🔗 Testing connection...")
            with psycopg.connect(database_url, connect_timeout=10) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT version()")
                    version = cur.fetchone()
                    print(f"✅ Connection successful!")
                    print(f"📊 PostgreSQL version: {version[0] if version else 'Unknown'}")
                    return True
        else:
            print("❌ DATABASE_URL not set")
            return False
            
    except ImportError as e:
        print(f"❌ psycopg3 import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
"""
    
    with open('render_connection_test.py', 'w') as f:
        f.write(script_content)
    
    print("✅ Created render_connection_test.py")
    print("📝 You can run this on Render to test the connection")

def provide_recommendations():
    """Provide recommendations for fixing the issue"""
    print("\n📋 Recommendations")
    print("=" * 20)
    
    print("1. 🔧 Check Render Environment Variables:")
    print("   • Go to Render dashboard > jewgo-backend > Environment")
    print("   • Ensure DATABASE_URL is set to PostgreSQL connection string")
    print("   • Ensure FLASK_ENV is set to 'production'")
    
    print("\\n2. 🔍 Test Connection on Render:")
    print("   • Upload render_connection_test.py to your repository")
    print("   • Run it on Render to test the connection")
    
    print("\\n3. 🔄 Alternative Solutions:")
    print("   • If psycopg3 still has issues, try asyncpg")
    print("   • Or use a different PostgreSQL provider")
    print("   • Consider using Supabase or Railway PostgreSQL")

def main():
    """Main function"""
    print("🔍 PostgreSQL Connection Diagnosis")
    print("=" * 35)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check current backend status
    backend_data = check_backend_status()
    
    # Test PostgreSQL connection locally
    connection_success = test_postgresql_connection()
    
    # Check environment variables
    check_environment_variables()
    
    # Check Render environment
    check_render_environment()
    
    # Create test script
    create_connection_test_script()
    
    # Provide recommendations
    provide_recommendations()
    
    print("\\n📊 Summary:")
    if backend_data and backend_data.get('database') == 'SQLite':
        print("❌ Backend is using SQLite fallback")
        print("   This indicates PostgreSQL connection is failing")
    elif connection_success:
        print("✅ Local PostgreSQL connection works")
        print("   Issue is likely with Render environment variables")
    else:
        print("❌ PostgreSQL connection is failing")
        print("   Need to check environment variables and connection string")

if __name__ == "__main__":
    main() 