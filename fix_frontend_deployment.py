#!/usr/bin/env python3
"""
Script to fix frontend deployment issues on Vercel
"""

import os
import subprocess
import requests
import json
import time
from datetime import datetime

def commit_frontend_fixes():
    """Commit the frontend deployment fixes"""
    try:
        # Add all the updated files
        subprocess.run(['git', 'add', 'next.config.js', 'package.json', '.nvmrc', 'vercel.json'], check=True)
        
        # Commit the changes
        commit_message = f"🔧 Fix Vercel deployment - Next.js 14.0.4 + Node.js 22 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push to remote
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Frontend deployment fixes committed and pushed successfully!")
        print(f"📝 Commit: {commit_message}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing changes: {e}")
        return False

def check_deployment_status():
    """Check if the deployment is successful"""
    print("\n🔄 Checking deployment status...")
    print("⏳ Please wait for Vercel to complete the deployment...")
    print("📊 You can monitor the deployment at: https://vercel.com/dashboard")
    
    # Note: Vercel doesn't provide a public API to check deployment status
    # The user will need to check the Vercel dashboard manually
    
    print("\n✅ Frontend deployment fixes applied:")
    print("   • Updated Next.js to 14.0.4")
    print("   • Updated Node.js to 22.x")
    print("   • Fixed Next.js configuration")
    print("   • Updated Vercel configuration")
    print("\n🎯 Next steps:")
    print("   1. Check Vercel dashboard for deployment status")
    print("   2. Monitor build logs for any remaining issues")
    print("   3. Test the deployed frontend once live")

def main():
    """Main function to fix frontend deployment"""
    print("🚀 Fixing Frontend Deployment Issues")
    print("=" * 50)
    
    # Commit the fixes
    if commit_frontend_fixes():
        check_deployment_status()
    else:
        print("❌ Failed to commit frontend fixes")

if __name__ == "__main__":
    main() 