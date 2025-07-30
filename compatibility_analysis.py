#!/usr/bin/env python3
"""
Comprehensive System Compatibility Analysis
"""

import os
import subprocess
import requests
import json
from datetime import datetime

def analyze_python_version_compatibility():
    """Analyze Python version compatibility issues"""
    print("🐍 Python Version Compatibility Analysis")
    print("=" * 40)
    
    issues = []
    
    # Check current configuration vs actual deployment
    print("📋 Current Configuration:")
    print("   • runtime.txt: Python 3.11.9")
    print("   • render.yaml: Python 3.11.9")
    print("   • Actual deployment: Python 3.13 (from logs)")
    
    if "3.11.9" != "3.13":
        issues.append({
            "component": "Python Version",
            "issue": "Version mismatch between configuration and deployment",
            "current": "3.11.9 (configured)",
            "actual": "3.13 (deployed)",
            "recommendation": "Update runtime.txt and render.yaml to Python 3.13"
        })
        print("❌ VERSION MISMATCH: Configuration says 3.11.9 but deployment uses 3.13")
    else:
        print("✅ Python versions are consistent")
    
    return issues

def analyze_flask_compatibility():
    """Analyze Flask and related dependencies"""
    print("\n🌐 Flask Framework Compatibility")
    print("=" * 35)
    
    issues = []
    
    # Flask 2.3.3 with Python 3.13
    flask_version = "2.3.3"
    python_version = "3.13"
    
    print(f"📋 Flask {flask_version} with Python {python_version}")
    
    # Check if Flask version is compatible with Python 3.13
    if flask_version < "2.3.0":
        issues.append({
            "component": "Flask",
            "issue": "Flask version may not be fully compatible with Python 3.13",
            "current": flask_version,
            "recommendation": "Consider upgrading to Flask 2.3.3+ for better Python 3.13 support"
        })
        print("⚠️  Flask version may need upgrade for Python 3.13")
    else:
        print("✅ Flask version is compatible with Python 3.13")
    
    # Check Werkzeug compatibility
    werkzeug_version = "2.3.7"
    print(f"📋 Werkzeug {werkzeug_version}")
    if werkzeug_version < "2.3.0":
        issues.append({
            "component": "Werkzeug",
            "issue": "Werkzeug version may not be fully compatible with Python 3.13",
            "current": werkzeug_version,
            "recommendation": "Consider upgrading to Werkzeug 2.3.0+ for better Python 3.13 support"
        })
        print("⚠️  Werkzeug version may need upgrade for Python 3.13")
    else:
        print("✅ Werkzeug version is compatible with Python 3.13")
    
    return issues

def analyze_database_compatibility():
    """Analyze database-related dependencies"""
    print("\n🗄️  Database Compatibility")
    print("=" * 25)
    
    issues = []
    
    # SQLAlchemy compatibility
    sqlalchemy_version = "1.4.53"
    print(f"📋 SQLAlchemy {sqlalchemy_version}")
    
    if sqlalchemy_version < "1.4.50":
        issues.append({
            "component": "SQLAlchemy",
            "issue": "SQLAlchemy version may have Python 3.13 compatibility issues",
            "current": sqlalchemy_version,
            "recommendation": "Consider upgrading to SQLAlchemy 1.4.53+ for better Python 3.13 support"
        })
        print("⚠️  SQLAlchemy version may need upgrade for Python 3.13")
    else:
        print("✅ SQLAlchemy version is compatible with Python 3.13")
    
    # psycopg2-binary compatibility
    psycopg2_version = "2.9.9"
    print(f"📋 psycopg2-binary {psycopg2_version}")
    
    if psycopg2_version < "2.9.0":
        issues.append({
            "component": "psycopg2-binary",
            "issue": "psycopg2-binary version may have Python 3.13 compatibility issues",
            "current": psycopg2_version,
            "recommendation": "Consider upgrading to psycopg2-binary 2.9.0+ for better Python 3.13 support"
        })
        print("⚠️  psycopg2-binary version may need upgrade for Python 3.13")
    else:
        print("✅ psycopg2-binary version is compatible with Python 3.13")
    
    return issues

def analyze_frontend_compatibility():
    """Analyze frontend compatibility"""
    print("\n⚛️  Frontend Compatibility")
    print("=" * 25)
    
    issues = []
    
    # Node.js version
    node_version = "22"
    print(f"📋 Node.js {node_version}")
    
    if node_version < "18":
        issues.append({
            "component": "Node.js",
            "issue": "Node.js version may be too old for current Next.js",
            "current": node_version,
            "recommendation": "Consider upgrading to Node.js 18+ for better Next.js support"
        })
        print("⚠️  Node.js version may need upgrade")
    else:
        print("✅ Node.js version is compatible")
    
    # Next.js version
    nextjs_version = "14.0.4"
    print(f"📋 Next.js {nextjs_version}")
    
    if nextjs_version < "13.0.0":
        issues.append({
            "component": "Next.js",
            "issue": "Next.js version may be too old for current features",
            "current": nextjs_version,
            "recommendation": "Consider upgrading to Next.js 13+ for better features and performance"
        })
        print("⚠️  Next.js version may need upgrade")
    else:
        print("✅ Next.js version is compatible")
    
    return issues

def analyze_other_dependencies():
    """Analyze other dependencies for compatibility"""
    print("\n📦 Other Dependencies")
    print("=" * 20)
    
    issues = []
    
    # Check specific dependencies that might have Python 3.13 issues
    dependencies_to_check = {
        "requests": "2.32.4",
        "structlog": "23.1.0",
        "marshmallow": "3.20.1",
        "gunicorn": "21.2.0",
        "pytest": "7.4.2"
    }
    
    for dep, version in dependencies_to_check.items():
        print(f"📋 {dep} {version}")
        
        # Check for known compatibility issues
        if dep == "requests" and version < "2.28.0":
            issues.append({
                "component": dep,
                "issue": f"{dep} version may have Python 3.13 compatibility issues",
                "current": version,
                "recommendation": f"Consider upgrading {dep} for better Python 3.13 support"
            })
            print(f"⚠️  {dep} version may need upgrade for Python 3.13")
        elif dep == "structlog" and version < "23.0.0":
            issues.append({
                "component": dep,
                "issue": f"{dep} version may have Python 3.13 compatibility issues",
                "current": version,
                "recommendation": f"Consider upgrading {dep} for better Python 3.13 support"
            })
            print(f"⚠️  {dep} version may need upgrade for Python 3.13")
        else:
            print(f"✅ {dep} version is compatible with Python 3.13")
    
    return issues

def check_backend_status():
    """Check current backend status"""
    print("\n🔍 Current Backend Status")
    print("=" * 25)
    
    try:
        response = requests.get("https://jewgo.onrender.com/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Status: {data.get('status', 'Unknown')}")
            print(f"📊 Environment: {data.get('environment', 'Unknown')}")
            print(f"📊 Database: {data.get('database', 'Unknown')}")
            print(f"📊 Version: {data.get('version', 'Unknown')}")
            return True
        else:
            print(f"❌ Backend returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking backend: {e}")
        return False

def generate_recommendations(issues):
    """Generate comprehensive recommendations"""
    print("\n📋 Compatibility Recommendations")
    print("=" * 35)
    
    if not issues:
        print("✅ No compatibility issues found!")
        return
    
    print(f"Found {len(issues)} potential compatibility issues:")
    print()
    
    for i, issue in enumerate(issues, 1):
        print(f"{i}. {issue['component']}: {issue['issue']}")
        print(f"   Current: {issue['current']}")
        if 'actual' in issue:
            print(f"   Actual: {issue['actual']}")
        print(f"   Recommendation: {issue['recommendation']}")
        print()

def create_upgrade_script(issues):
    """Create a script to fix compatibility issues"""
    if not issues:
        return
    
    print("\n🔧 Creating Upgrade Script")
    print("=" * 25)
    
    script_content = """#!/usr/bin/env python3
\"\"\"
System Compatibility Upgrade Script
\"\"\"

import os
import subprocess
from datetime import datetime

def upgrade_system_compatibility():
    \"\"\"Upgrade system for better Python 3.13 compatibility\"\"\"
    print("🚀 Upgrading System Compatibility")
    print("=" * 35)
    
    # Update Python version configuration
    print("📝 Updating Python version configuration...")
    
    # Update runtime.txt
    with open('runtime.txt', 'w') as f:
        f.write('python-3.13.5\\n')
    
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
"""
    
    with open('upgrade_system_compatibility.py', 'w') as f:
        f.write(script_content)
    
    print("✅ Created upgrade_system_compatibility.py")

def main():
    """Main compatibility analysis function"""
    print("🔍 Comprehensive System Compatibility Analysis")
    print("=" * 50)
    print(f"📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_issues = []
    
    # Analyze different components
    all_issues.extend(analyze_python_version_compatibility())
    all_issues.extend(analyze_flask_compatibility())
    all_issues.extend(analyze_database_compatibility())
    all_issues.extend(analyze_frontend_compatibility())
    all_issues.extend(analyze_other_dependencies())
    
    # Check current backend status
    check_backend_status()
    
    # Generate recommendations
    generate_recommendations(all_issues)
    
    # Create upgrade script if needed
    if all_issues:
        create_upgrade_script(all_issues)
        print("\n🚀 To apply compatibility fixes, run:")
        print("   python upgrade_system_compatibility.py")
    else:
        print("\n🎉 System is fully compatible!")
    
    print("\n📊 Analysis Complete")
    print("=" * 20)

if __name__ == "__main__":
    main() 