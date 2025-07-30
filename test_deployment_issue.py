#!/usr/bin/env python3
"""
Test script to identify deployment issues.
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing module imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import psycopg2
        print("✅ psycopg2 imported successfully")
    except ImportError as e:
        print(f"❌ psycopg2 import failed: {e}")
        return False
    
    try:
        import psycopg
        print("✅ psycopg imported successfully")
    except ImportError as e:
        print(f"❌ psycopg import failed: {e}")
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy imported successfully")
    except ImportError as e:
        print(f"❌ SQLAlchemy import failed: {e}")
        return False
    
    return True

def test_database_connection():
    """Test database connection."""
    print("\n🔍 Testing database connection...")
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL environment variable not set")
        return False
    
    print(f"✅ DATABASE_URL found: {database_url[:50]}...")
    
    try:
        from sqlalchemy import create_engine
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Database connection successful")
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_app_creation():
    """Test if the Flask app can be created."""
    print("\n🔍 Testing Flask app creation...")
    
    try:
        from app import create_app
        app = create_app()
        print("✅ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return False

def main():
    print("🚀 Deployment Issue Diagnostic")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed")
        sys.exit(1)
    
    # Test database connection
    if not test_database_connection():
        print("\n❌ Database connection failed")
        sys.exit(1)
    
    # Test app creation
    if not test_app_creation():
        print("\n❌ App creation failed")
        sys.exit(1)
    
    print("\n✅ All tests passed!")
    print("💡 The issue might be in the deployment process itself")

if __name__ == "__main__":
    main() 