#!/usr/bin/env python3
"""
PostgreSQL Connection Test Script
Run this on Render to test the connection
"""

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
        print("\n✅ psycopg3 is available")
        
        if database_url:
            print("\n🔗 Testing connection...")
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
