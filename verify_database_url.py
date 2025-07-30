#!/usr/bin/env python3
"""
Verify Database URL Format and Test Connection
"""

import psycopg
from urllib.parse import urlparse

def analyze_database_url(url):
    """Analyze the database URL format"""
    print("🔍 Analyzing Database URL Format")
    print("=" * 35)
    
    try:
        parsed = urlparse(url)
        print(f"✅ URL is valid")
        print(f"📋 Scheme: {parsed.scheme}")
        print(f"📋 Username: {parsed.username}")
        print(f"📋 Password: {'*' * len(parsed.password) if parsed.password else 'None'}")
        print(f"📋 Host: {parsed.hostname}")
        print(f"📋 Port: {parsed.port or 'default (5432)'}")
        print(f"📋 Database: {parsed.path[1:] if parsed.path else 'None'}")
        print(f"📋 Query: {parsed.query}")
        
        # Check if it's a Neon URL
        if 'neon.tech' in parsed.hostname:
            print("✅ This appears to be a Neon PostgreSQL URL")
        else:
            print("⚠️  This doesn't appear to be a Neon URL")
            
        return True
    except Exception as e:
        print(f"❌ URL format error: {e}")
        return False

def test_database_connection(url):
    """Test the database connection"""
    print("\n🔗 Testing Database Connection")
    print("=" * 30)
    
    try:
        print(f"📋 Connecting to: {url.split('@')[1] if '@' in url else 'Unknown'}")
        
        with psycopg.connect(url, connect_timeout=10) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version()")
                version = cur.fetchone()
                print(f"✅ Connection successful!")
                print(f"📊 PostgreSQL version: {version[0] if version else 'Unknown'}")
                
                # Test if we can create a table
                cur.execute("SELECT current_database()")
                db_name = cur.fetchone()
                print(f"📊 Connected to database: {db_name[0] if db_name else 'Unknown'}")
                
                return True
                
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def suggest_alternative_formats():
    """Suggest alternative URL formats"""
    print("\n💡 Alternative URL Formats to Try")
    print("=" * 35)
    
    base_url = "postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb"
    
    alternatives = [
        f"{base_url}?sslmode=require",
        f"{base_url}?sslmode=require&sslcert=&sslkey=&sslrootcert=",
        f"{base_url}?sslmode=verify-full",
        f"{base_url}?sslmode=prefer",
        f"{base_url}?sslmode=require&connect_timeout=10",
        f"{base_url}?sslmode=require&application_name=jewgo_app"
    ]
    
    print("If the current URL doesn't work, try these alternatives:")
    for i, alt in enumerate(alternatives, 1):
        print(f"{i}. {alt}")

def main():
    """Main function"""
    print("🔍 Database URL Verification")
    print("=" * 30)
    
    # The URL from your logs
    database_url = "postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    
    print(f"📋 Testing URL: {database_url}")
    print()
    
    # Analyze the URL format
    if analyze_database_url(database_url):
        print("\n✅ URL format is valid")
        
        # Test the connection
        if test_database_connection(database_url):
            print("\n🎉 SUCCESS: Database URL is correct and working!")
            print("   You can use this exact URL in Render environment variables")
        else:
            print("\n⚠️  Connection failed - trying alternative formats")
            suggest_alternative_formats()
    else:
        print("\n❌ URL format is invalid")
        suggest_alternative_formats()

if __name__ == "__main__":
    main() 