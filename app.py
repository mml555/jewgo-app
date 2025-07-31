#!/usr/bin/env python3
"""
JewGo Backend API Server - Root Entry Point
===========================================

This is the root entry point for the JewGo backend API server.
It imports and runs the Flask application from the backend directory.

Author: JewGo Development Team
Version: 3.0
Last Updated: 2024
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import and run the Flask app from backend
from app import app

# Initialize database on startup
with app.app_context():
    try:
        from database.database_manager_v3 import EnhancedDatabaseManager
        db_manager = EnhancedDatabaseManager()
        db_manager.connect()
        print("✅ Database connection established")
    except Exception as e:
        print(f"⚠️  Database connection failed: {e}")

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('ENVIRONMENT') != 'production'
    ) 