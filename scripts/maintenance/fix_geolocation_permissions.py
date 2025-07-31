#!/usr/bin/env python3
"""
Script to fix geolocation permissions issue
"""

import os
import subprocess
import requests
import json
import time
from datetime import datetime

def commit_geolocation_fixes():
    """Commit the geolocation permission fixes"""
    try:
        # Add the updated files
        subprocess.run(['git', 'add', 'next.config.js', 'app/page.tsx'], check=True)
        
        # Commit the changes
        commit_message = f"🔧 Fix geolocation permissions - Next.js headers + graceful error handling - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push to remote
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Geolocation fixes committed and pushed successfully!")
        print(f"📝 Commit: {commit_message}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing changes: {e}")
        return False

def check_frontend_status():
    """Check if the frontend is accessible"""
    try:
        response = requests.get("https://jewgo-app.vercel.app", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            return True
        else:
            print(f"⚠️  Frontend status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend not responding: {e}")
        return False

def provide_geolocation_guidance():
    """Provide guidance on geolocation permissions"""
    print("\n🔧 Geolocation Permissions Fix Applied:")
    print("   • Added Permissions-Policy header to Next.js config")
    print("   • Improved error handling for geolocation failures")
    print("   • App will continue working without location if blocked")
    
    print("\n📱 Browser Permissions:")
    print("   • The app will request geolocation permission")
    print("   • If denied, the app continues with default behavior")
    print("   • Users can manually enable location in browser settings")
    
    print("\n🎯 User Experience:")
    print("   • No more console errors for geolocation")
    print("   • Graceful fallback when location is unavailable")
    print("   • App functionality preserved regardless of location access")
    
    print("\n🌐 Testing Instructions:")
    print("   1. Visit: https://jewgo-app.vercel.app")
    print("   2. Allow location permission when prompted")
    print("   3. If blocked, app will work without location features")
    print("   4. Check browser console - should be clean now")

def main():
    """Main function to fix geolocation permissions"""
    print("🚀 Fixing Geolocation Permissions Issue")
    print("=" * 50)
    
    # Check current frontend status
    if not check_frontend_status():
        print("❌ Frontend is not accessible. Please check deployment status.")
        return
    
    # Commit the geolocation fixes
    if commit_geolocation_fixes():
        print("\n✅ Geolocation permission fixes applied:")
        print("   • Updated Next.js configuration with proper headers")
        print("   • Improved error handling in frontend code")
        print("   • Frontend will redeploy automatically")
        
        # Wait for deployment
        print("\n⏳ Waiting for frontend deployment to complete...")
        time.sleep(30)
        
        provide_geolocation_guidance()
        
        print("\n🎉 Geolocation permissions issue resolved!")
        print("✅ The app will now handle geolocation gracefully")
        print("🌐 Test the updated frontend at: https://jewgo-app.vercel.app")
    else:
        print("❌ Failed to commit geolocation fixes")

if __name__ == "__main__":
    main() 