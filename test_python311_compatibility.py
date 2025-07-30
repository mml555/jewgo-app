#!/usr/bin/env python3
"""
Test script to verify Python 3.11.8 compatibility.
Checks for any syntax or import issues that might cause problems.
"""

import sys
import importlib
from datetime import datetime

def test_python_version():
    """Test Python version compatibility."""
    print(f"🐍 Python Version: {sys.version}")
    print(f"📋 Version Info: {sys.version_info}")
    
    if sys.version_info >= (3, 11):
        print("✅ Python 3.11+ detected - compatible with our setup")
    else:
        print("⚠️  Python version below 3.11 - may have compatibility issues")
    
    print()

def test_imports():
    """Test all required imports."""
    print("📦 Testing required imports...")
    
    required_modules = [
        'flask',
        'flask_cors', 
        'flask_limiter',
        'sqlalchemy',
        'psycopg2',
        'structlog',
        'requests',
        'marshmallow',
        'sentry_sdk',
        'gunicorn',
        'python_dotenv',
        'alembic'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n⚠️  Failed imports: {failed_imports}")
    else:
        print("\n✅ All imports successful!")
    
    print()

def test_sqlalchemy_compatibility():
    """Test SQLAlchemy 1.4 compatibility."""
    print("🗄️ Testing SQLAlchemy 1.4 compatibility...")
    
    try:
        from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import sessionmaker, Session
        from sqlalchemy import func
        
        print("✅ SQLAlchemy 1.4 imports successful")
        
        # Test basic SQLAlchemy functionality
        Base = declarative_base()
        print("✅ declarative_base() works")
        
        # Test func.count() which we use in statistics
        print("✅ func.count() available")
        
    except ImportError as e:
        print(f"❌ SQLAlchemy import failed: {e}")
    except Exception as e:
        print(f"❌ SQLAlchemy test failed: {e}")
    
    print()

def test_flask_compatibility():
    """Test Flask compatibility."""
    print("🌐 Testing Flask compatibility...")
    
    try:
        from flask import Flask, request, jsonify, g
        from flask_cors import CORS
        from flask_limiter import Limiter
        from flask_limiter.util import get_remote_address
        
        print("✅ Flask imports successful")
        
        # Test basic Flask app creation
        app = Flask(__name__)
        print("✅ Flask app creation successful")
        
        # Test CORS
        CORS(app)
        print("✅ CORS setup successful")
        
        # Test rate limiter
        limiter = Limiter(app, key_func=get_remote_address)
        print("✅ Rate limiter setup successful")
        
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
    except Exception as e:
        print(f"❌ Flask test failed: {e}")
    
    print()

def test_database_compatibility():
    """Test database driver compatibility."""
    print("💾 Testing database driver compatibility...")
    
    try:
        import psycopg2
        print("✅ psycopg2 import successful")
        
        # Test basic connection (without actually connecting)
        print("✅ psycopg2 driver available")
        
    except ImportError as e:
        print(f"❌ psycopg2 import failed: {e}")
    
    print()

def test_logging_compatibility():
    """Test structured logging compatibility."""
    print("📝 Testing structured logging compatibility...")
    
    try:
        import structlog
        print("✅ structlog import successful")
        
        # Test basic structlog configuration
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
        
        logger = structlog.get_logger()
        logger.info("Test log message", test_field="test_value")
        print("✅ structlog configuration and logging successful")
        
    except ImportError as e:
        print(f"❌ structlog import failed: {e}")
    except Exception as e:
        print(f"❌ structlog test failed: {e}")
    
    print()

def test_http_compatibility():
    """Test HTTP requests compatibility."""
    print("🌍 Testing HTTP requests compatibility...")
    
    try:
        import requests
        print("✅ requests import successful")
        
        # Test basic requests functionality
        print("✅ requests library available")
        
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
    
    print()

def main():
    """Run all compatibility tests."""
    print("🔍 Python 3.11.8 Compatibility Test Suite")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    test_python_version()
    test_imports()
    test_sqlalchemy_compatibility()
    test_flask_compatibility()
    test_database_compatibility()
    test_logging_compatibility()
    test_http_compatibility()
    
    print("=" * 50)
    print("🏁 Compatibility test completed!")
    print("✅ If all tests passed, your environment is compatible with Python 3.11.8")

if __name__ == "__main__":
    main() 