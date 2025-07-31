#!/usr/bin/env python3
"""
Production startup script for JewGo Backend API

This script is used to start the application in production mode using Gunicorn.
It ensures proper configuration and environment setup for production deployment.
"""

import os
import sys
from app import app

if __name__ == '__main__':
    # Set production environment
    os.environ['FLASK_ENV'] = 'production'
    os.environ['ENVIRONMENT'] = 'production'
    
    # Import and run with Gunicorn if available, otherwise use Flask development server
    try:
        from gunicorn.app.wsgiapp import WSGIApplication
        
        class StandaloneApplication(WSGIApplication):
            def __init__(self, app_uri, options=None):
                self.options = options or {}
                self.app_uri = app_uri
                super().__init__()
            
            def load_config(self):
                config = {
                    'bind': f"0.0.0.0:{os.environ.get('PORT', '5000')}",
                    'workers': 2,
                    'worker_class': 'sync',
                    'timeout': 120,
                    'keepalive': 2,
                    'max_requests': 1000,
                    'max_requests_jitter': 50,
                    'preload_app': True,
                    'access_logfile': '-',
                    'error_logfile': '-',
                    'loglevel': 'info'
                }
                for key, value in config.items():
                    self.cfg.set(key, value)
        
        options = {}
        StandaloneApplication(app, options).run()
        
    except ImportError:
        # Fallback to Flask development server if Gunicorn is not available
        print("Warning: Gunicorn not available, using Flask development server")
        app.run(
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000)),
            debug=False
        ) 