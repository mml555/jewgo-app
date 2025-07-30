#!/usr/bin/env python3
"""
Redeploy script to fix psycopg2 compatibility issue.
The application was failing because SQLAlchemy 1.4.53 expects psycopg2
but only psycopg (version 3) was installed.
"""

import os
import subprocess
import sys
from datetime import datetime

def main():
    print(f"🚀 Starting redeploy with psycopg2 compatibility fix - {datetime.now()}")
    
    # Check if we're in the right directory
    if not os.path.exists('requirements.txt'):
        print("❌ Error: requirements.txt not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Verify the fix is in place
    with open('requirements.txt', 'r') as f:
        content = f.read()
        if 'psycopg2-binary==2.9.9' not in content:
            print("❌ Error: psycopg2-binary not found in requirements.txt")
            sys.exit(1)
    
    print("✅ psycopg2-binary fix confirmed in requirements.txt")
    
    # Commit the changes
    try:
        subprocess.run(['git', 'add', 'requirements.txt'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Fix: Add psycopg2-binary for SQLAlchemy 1.4.53 compatibility'], check=True)
        print("✅ Changes committed to git")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git commit failed: {e}")
        sys.exit(1)
    
    # Push to trigger redeploy
    try:
        subprocess.run(['git', 'push'], check=True)
        print("✅ Changes pushed to repository")
        print("🔄 Render will automatically redeploy with the fix")
        print("📊 Monitor deployment at: https://dashboard.render.com/web/srv-jewgo")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git push failed: {e}")
        sys.exit(1)
    
    print("🎉 Redeploy initiated successfully!")
    print("⏱️  Deployment typically takes 2-3 minutes")
    print("🔗 Live URL: https://jewgo.onrender.com")

if __name__ == "__main__":
    main() 