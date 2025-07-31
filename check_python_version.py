#!/usr/bin/env python3
"""
Python Version Checker for JewGo App
Enforces Python 3.11.x usage to prevent compatibility issues.
"""

import sys
import subprocess
import os

def check_python_version():
    """Check if the current Python version is compatible with the project."""
    current_version = sys.version_info
    
    print("🐍 Python Version Check for JewGo App")
    print("=" * 50)
    print(f"Current Python version: {current_version.major}.{current_version.minor}.{current_version.micro}")
    
    # Check if we're using Python 3.11.x
    if current_version.major == 3 and current_version.minor == 11:
        print("✅ Python version is compatible (3.11.x)")
        print("✅ All dependencies should work correctly")
        return True
    elif current_version.major == 3 and current_version.minor >= 12:
        print("❌ Python version is TOO NEW (3.12+)")
        print("❌ This will cause compatibility issues with:")
        print("   - psycopg2-binary==2.9.9")
        print("   - Some other dependencies")
        print("\n🔧 To fix this:")
        print("   1. Install Python 3.11.8: brew install python@3.11")
        print("   2. Create a new virtual environment: python3.11 -m venv venv")
        print("   3. Activate it: source venv/bin/activate")
        print("   4. Install dependencies: pip install -r requirements.txt")
        return False
    elif current_version.major == 3 and current_version.minor < 11:
        print("❌ Python version is TOO OLD (< 3.11)")
        print("❌ This project requires Python 3.11.x")
        print("\n🔧 To fix this:")
        print("   1. Install Python 3.11.8: brew install python@3.11")
        print("   2. Create a new virtual environment: python3.11 -m venv venv")
        print("   3. Activate it: source venv/bin/activate")
        print("   4. Install dependencies: pip install -r requirements.txt")
        return False
    else:
        print("❌ Unexpected Python version")
        print("❌ This project requires Python 3.11.x")
        return False

def check_virtual_environment():
    """Check if we're running in a virtual environment."""
    print(f"\n🔧 Virtual Environment Check:")
    
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in a virtual environment")
        print(f"   Virtual env: {sys.prefix}")
        return True
    else:
        print("⚠️  Not running in a virtual environment")
        print("   Consider using a virtual environment for development")
        return False

def check_dependencies():
    """Check if key dependencies are installed."""
    print(f"\n📦 Dependency Check:")
    
    try:
        import psycopg2
        print("✅ psycopg2 is available")
    except ImportError:
        print("❌ psycopg2 is not available")
        print("   Run: pip install -r requirements.txt")
        return False
    
    try:
        import flask
        print("✅ Flask is available")
    except ImportError:
        print("❌ Flask is not available")
        print("   Run: pip install -r requirements.txt")
        return False
    
    try:
        import requests
        print("✅ requests is available")
    except ImportError:
        print("❌ requests is not available")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main function to run all checks."""
    print("🚀 JewGo App - Python Environment Check")
    print("=" * 50)
    
    # Run all checks
    version_ok = check_python_version()
    venv_ok = check_virtual_environment()
    deps_ok = check_dependencies()
    
    print("\n" + "=" * 50)
    print("📋 Summary:")
    print(f"   Python Version: {'✅' if version_ok else '❌'}")
    print(f"   Virtual Environment: {'✅' if venv_ok else '⚠️'}")
    print(f"   Dependencies: {'✅' if deps_ok else '❌'}")
    
    if version_ok and deps_ok:
        print("\n🎉 All checks passed! You're ready to develop.")
        return 0
    else:
        print("\n🔧 Please fix the issues above before continuing.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 