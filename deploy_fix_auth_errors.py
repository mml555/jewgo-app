#!/usr/bin/env python3
"""
Deployment script to fix NextAuth and environment issues
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_environment():
    """Check current environment setup"""
    print("🔍 Checking environment setup...")
    
    # Check if we're in the right directory
    if not Path("package.json").exists():
        print("❌ package.json not found. Please run this script from the project root.")
        return False
    
    # Check Node.js version
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        print(f"✅ Node.js version: {result.stdout.strip()}")
    except:
        print("❌ Node.js not found")
        return False
    
    # Check npm version
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        print(f"✅ npm version: {result.stdout.strip()}")
    except:
        print("❌ npm not found")
        return False
    
    return True

def install_dependencies():
    """Install npm dependencies"""
    return run_command("npm install", "Installing npm dependencies")

def build_project():
    """Build the Next.js project"""
    return run_command("npm run build", "Building Next.js project")

def create_env_file():
    """Create a basic .env.local file if it doesn't exist"""
    env_file = Path(".env.local")
    
    if env_file.exists():
        print("✅ .env.local file already exists")
        return True
    
    print("📝 Creating .env.local file...")
    
    env_content = """# NextAuth Configuration
NEXTAUTH_URL=https://jewgo-app.vercel.app
NEXTAUTH_SECRET=your-nextauth-secret-key-here-change-in-production

# Google Maps API Key (optional)
# NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-google-maps-api-key-here

# Backend API URL
NEXT_PUBLIC_BACKEND_URL=https://jewgo.onrender.com

# Environment
NODE_ENV=production
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env.local file created")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env.local file: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🧪 Testing API endpoints...")
    
    # Test the test endpoint
    try:
        import requests
        response = requests.get("https://jewgo-app.vercel.app/api/test", timeout=10)
        if response.status_code == 200:
            print("✅ API test endpoint working")
        else:
            print(f"⚠️ API test endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"❌ API test failed: {e}")
    
    # Test NextAuth endpoint
    try:
        response = requests.get("https://jewgo-app.vercel.app/api/auth/session", timeout=10)
        if response.status_code == 200:
            print("✅ NextAuth session endpoint working")
        else:
            print(f"⚠️ NextAuth session endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"❌ NextAuth test failed: {e}")

def main():
    """Main deployment function"""
    print("🚀 Starting deployment fix for NextAuth and environment issues...")
    
    # Check environment
    if not check_environment():
        print("❌ Environment check failed. Please fix the issues above.")
        return False
    
    # Create env file
    if not create_env_file():
        print("❌ Failed to create environment file.")
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies.")
        return False
    
    # Build project
    if not build_project():
        print("❌ Failed to build project.")
        return False
    
    # Test endpoints
    test_api_endpoints()
    
    print("\n🎉 Deployment fix completed!")
    print("\n📋 Next steps:")
    print("1. Deploy to Vercel: git push origin main")
    print("2. Set environment variables in Vercel dashboard:")
    print("   - NEXTAUTH_URL: https://jewgo-app.vercel.app")
    print("   - NEXTAUTH_SECRET: (generate a secure secret)")
    print("   - NEXT_PUBLIC_BACKEND_URL: https://jewgo.onrender.com")
    print("3. Test the application")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 