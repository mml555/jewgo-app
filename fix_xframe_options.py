#!/usr/bin/env python3
"""
Script to fix X-Frame-Options for frame display
"""

import os
import subprocess
import requests
import time
from datetime import datetime

def commit_xframe_fix():
    """Commit the X-Frame-Options fix"""
    try:
        # Add the updated files
        subprocess.run(['git', 'add', '_headers', 'next.config.js'], check=True)
        
        # Commit the changes
        commit_message = f"🔧 Fix X-Frame-Options to ALLOWALL - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push to remote
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ X-Frame-Options fix committed and pushed successfully!")
        print(f"📝 Commit: {commit_message}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing changes: {e}")
        return False

def check_frontend_deployment():
    """Check if the frontend deployment is working"""
    print("\n🔄 Checking frontend deployment status...")
    
    # Wait for deployment to complete
    time.sleep(30)
    
    try:
        # Test the original Vercel domain
        response = requests.get("https://jewgo-app.vercel.app/", timeout=10)
        if response.status_code == 200:
            print("✅ Original Vercel domain is accessible")
            
            # Check X-Frame-Options header
            x_frame_options = response.headers.get('X-Frame-Options', 'Not set')
            print(f"📋 X-Frame-Options: {x_frame_options}")
            
            if x_frame_options == 'ALLOWALL':
                print("✅ X-Frame-Options set to ALLOWALL - frame display should work!")
                return True
            else:
                print(f"⚠️  X-Frame-Options is {x_frame_options} - may still cause issues")
                return False
        else:
            print(f"❌ Original Vercel domain returned status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error checking frontend: {e}")
        return False

def test_new_vercel_domain():
    """Test the new Vercel domain as well"""
    try:
        response = requests.get("https://jewgo-j953cxrfi-mml555s-projects.vercel.app/", timeout=10)
        if response.status_code == 200:
            print("✅ New Vercel domain is accessible")
            
            x_frame_options = response.headers.get('X-Frame-Options', 'Not set')
            print(f"📋 X-Frame-Options (New): {x_frame_options}")
            
            return True
        else:
            print(f"⚠️  New Vercel domain returned status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error checking new Vercel domain: {e}")
        return False

def provide_guidance():
    """Provide guidance on the X-Frame-Options fix"""
    print("\n🔧 X-Frame-Options Configuration Updated:")
    print("   • Changed from SAMEORIGIN to ALLOWALL")
    print("   • Updated both _headers and next.config.js")
    print("   • Frontend will redeploy automatically")
    
    print("\n🎯 What This Fixes:")
    print("   • Allows pages to be displayed in iframes")
    print("   • Resolves 'Refused to display in frame' errors")
    print("   • Enables embedding in various contexts")
    print("   • Maintains other security headers")
    
    print("\n⚠️  Security Considerations:")
    print("   • ALLOWALL allows embedding from any origin")
    print("   • This is appropriate for public web applications")
    print("   • Other security headers remain active")
    print("   • HTTPS and other protections still in place")
    
    print("\n🚀 Next Steps:")
    print("   1. Wait for Vercel deployment to complete")
    print("   2. Test frame display functionality")
    print("   3. Verify no more X-Frame-Options errors")
    print("   4. Test embedding in different contexts")

def main():
    """Main function to fix X-Frame-Options"""
    print("🚀 Fixing X-Frame-Options for Frame Display")
    print("=" * 50)
    
    # Commit the X-Frame-Options fix
    if commit_xframe_fix():
        print(f"\n✅ X-Frame-Options configuration updated to ALLOWALL")
        print("   • Changed from SAMEORIGIN to ALLOWALL")
        print("   • Updated both _headers and next.config.js")
        print("   • Frontend will redeploy automatically")
        
        # Test the fix
        if check_frontend_deployment():
            print("\n🎉 X-Frame-Options issue resolved!")
            print("✅ Pages can now be displayed in frames")
            print("✅ No more 'Refused to display in frame' errors")
            
            # Test new domain as well
            test_new_vercel_domain()
        else:
            print("\n⚠️  X-Frame-Options fix may still be deploying...")
            print("⏳ Please wait a few minutes and test again")
        
        provide_guidance()
    else:
        print("❌ Failed to commit X-Frame-Options fix")

if __name__ == "__main__":
    main() 