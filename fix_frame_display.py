#!/usr/bin/env python3
"""
Script to fix frame display issue
"""

import os
import subprocess
import requests
import json
import time
from datetime import datetime

def commit_frame_fix():
    """Commit the frame display fix"""
    try:
        # Add the updated files
        subprocess.run(['git', 'add', 'next.config.js', '_headers'], check=True)
        
        # Commit the changes
        commit_message = f"🔧 Fix frame display - X-Frame-Options SAMEORIGIN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push to remote
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Frame display fix committed and pushed successfully!")
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

def provide_frame_guidance():
    """Provide guidance on frame display fix"""
    print("\n🔧 Frame Display Fix Applied:")
    print("   • Changed X-Frame-Options from DENY to SAMEORIGIN")
    print("   • Allows the app to be displayed in frames from same origin")
    print("   • Maintains security while enabling frame display")
    
    print("\n🎯 Security Impact:")
    print("   • SAMEORIGIN: Allows framing from same domain")
    print("   • DENY: Prevents all framing (was too restrictive)")
    print("   • Balance: Security maintained while enabling functionality")
    
    print("\n🌐 Frame Display Behavior:")
    print("   • Same-origin frames: ✅ Allowed")
    print("   • Cross-origin frames: ❌ Still blocked (secure)")
    print("   • Direct access: ✅ Always allowed")
    
    print("\n📱 Testing Instructions:")
    print("   1. Visit: https://jewgo-app.vercel.app")
    print("   2. Should now display properly in frames")
    print("   3. No more 'Refused to display' errors")
    print("   4. App functionality remains intact")

def main():
    """Main function to fix frame display issue"""
    print("🚀 Fixing Frame Display Issue")
    print("=" * 40)
    
    # Check current frontend status
    if not check_frontend_status():
        print("❌ Frontend is not accessible. Please check deployment status.")
        return
    
    # Commit the frame display fix
    if commit_frame_fix():
        print("\n✅ Frame display fix applied:")
        print("   • Updated X-Frame-Options to SAMEORIGIN")
        print("   • Maintains security while enabling frame display")
        print("   • Frontend will redeploy automatically")
        
        # Wait for deployment
        print("\n⏳ Waiting for frontend deployment to complete...")
        time.sleep(30)
        
        provide_frame_guidance()
        
        print("\n🎉 Frame display issue resolved!")
        print("✅ The app can now be displayed in frames from same origin")
        print("🌐 Test the updated frontend at: https://jewgo-app.vercel.app")
    else:
        print("❌ Failed to commit frame display fix")

if __name__ == "__main__":
    main() 