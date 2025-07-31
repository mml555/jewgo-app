#!/usr/bin/env python3
"""
Deployment Setup Verification Script
===================================

This script verifies that all necessary files for Render deployment are present
and properly configured.

Author: JewGo Development Team
Version: 1.0
Last Updated: 2024
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and print status."""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - MISSING")
        return False

def check_render_yaml():
    """Check render.yaml configuration."""
    if os.path.exists('render.yaml'):
        print("✅ render.yaml found (optional)")
        return True
    else:
        print("ℹ️  render.yaml not found (using Procfile instead)")
        return True

def check_requirements():
    """Check requirements.txt files."""
    root_req = check_file_exists('requirements.txt', 'Root requirements.txt')
    backend_req = check_file_exists('backend/requirements.txt', 'Backend requirements.txt')
    return root_req and backend_req

def check_runtime():
    """Check runtime.txt configuration."""
    if not check_file_exists('runtime.txt', 'runtime.txt'):
        return False
    
    try:
        with open('runtime.txt', 'r') as f:
            version = f.read().strip()
        print(f"✅ Python version: {version}")
        return True
    except Exception as e:
        print(f"❌ runtime.txt: Error reading - {e}")
        return False

def check_procfile():
    """Check Procfile configuration."""
    if not check_file_exists('Procfile', 'Procfile'):
        return False
    
    try:
        with open('Procfile', 'r') as f:
            content = f.read().strip()
        print(f"✅ Procfile content: {content}")
        return True
    except Exception as e:
        print(f"❌ Procfile: Error reading - {e}")
        return False

def check_backend_files():
    """Check essential backend files."""
    files_to_check = [
        ('app.py', 'Root Flask application'),
        ('backend/app.py', 'Backend Flask application'),
        ('backend/config/gunicorn.conf.py', 'Gunicorn configuration'),
        ('backend/database/database_manager_v3.py', 'Database manager'),
    ]
    
    all_exist = True
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_exist = False
    
    return all_exist

def main():
    """Main verification function."""
    print("🔍 JewGo Deployment Setup Verification")
    print("=" * 50)
    
    checks = [
        ("render.yaml", check_render_yaml),
        ("requirements.txt", check_requirements),
        ("runtime.txt", check_runtime),
        ("Procfile", check_procfile),
        ("backend files", check_backend_files),
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        if check_func():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All deployment files are properly configured!")
        print("🚀 Ready for Render deployment")
        return 0
    else:
        print("⚠️  Some issues found. Please fix them before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 