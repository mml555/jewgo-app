#!/usr/bin/env python3
"""
System Compatibility Upgrade Script
"""

import os
import subprocess
from datetime import datetime

def upgrade_system_compatibility():
    """Upgrade system for better Python 3.13 compatibility"""
    print("🚀 Upgrading System Compatibility")
    print("=" * 35)
    
    # Update Python version configuration
    print("📝 Updating Python version configuration...")
    
    # Update runtime.txt
    with open('runtime.txt', 'w') as f:
        f.write('python-3.13.5\n')
    
    # Update render.yaml
    render_yaml_content = '''services:
  - type: web
    name: jewgo-backend
    env: python
    pythonVersion: "3.13.5"
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.13.5
'''
    
    with open('render.yaml', 'w') as f:
        f.write(render_yaml_content)
    
    print("✅ Python version configuration updated")
    
    # Update requirements.txt with latest compatible versions
    print("📝 Updating requirements.txt...")
    
    requirements_content = '''# Core Flask Framework
Flask==2.3.3
Flask-CORS==4.0.0
Werkzeug==2.3.7
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
blinker==1.6.3

# Database Support
psycopg2-binary==2.9.9  # PostgreSQL adapter (binary - Python 3.13 compatible)
SQLAlchemy==1.4.53      # ORM for database abstraction (stable with Python 3.13)
alembic==1.11.3         # Database migrations (compatible with SQLAlchemy 1.4.53)

# Environment & Configuration
python-dotenv==1.0.0    # Environment variable management
gunicorn==21.2.0        # Production WSGI server

# Security & Validation
Flask-Limiter==3.5.0    # Rate limiting
marshmallow==3.20.1     # Data validation and serialization

# Monitoring & Logging
structlog==23.1.0       # Structured logging
sentry-sdk[flask]==1.32.0  # Error tracking (optional)

# HTTP Requests
requests==2.32.4        # HTTP library for API calls

# Development & Testing
pytest==7.4.2           # Testing framework
pytest-flask==1.2.0     # Flask testing utilities
'''
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements_content)
    
    print("✅ requirements.txt updated")
    
    # Commit and push changes
    try:
        subprocess.run(['git', 'add', 'runtime.txt', 'render.yaml', 'requirements.txt'], check=True)
        
        commit_message = f"🔧 System compatibility upgrade - Python 3.13 configuration - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Changes committed and pushed successfully")
        print(f"📝 Commit: {commit_message}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing changes: {e}")
        return False
    
    return True

if __name__ == "__main__":
    upgrade_system_compatibility()
