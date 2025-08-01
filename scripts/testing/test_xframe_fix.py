#!/usr/bin/env python3
"""
Test script to verify X-Frame-Options fix
"""

import requests
import time
from datetime import datetime

def test_xframe_options():
    """Test X-Frame-Options header on deployed sites"""
    print("🔧 Testing X-Frame-Options Configuration")
    print("=" * 50)
    
    # List of domains to test
    domains = [
        "https://jewgo-app.vercel.app/",
        "https://jewgo-j953cxrfi-mml555s-projects.vercel.app/"
    ]
    
    for domain in domains:
        print(f"\n🌐 Testing: {domain}")
        try:
            response = requests.get(domain, timeout=10)
            if response.status_code == 200:
                print(f"✅ Status: {response.status_code}")
                
                # Check X-Frame-Options header
                x_frame_options = response.headers.get('X-Frame-Options', 'Not set')
                print(f"📋 X-Frame-Options: {x_frame_options}")
                
                if x_frame_options == 'ALLOWALL':
                    print("✅ Frame display should work!")
                elif x_frame_options == 'DENY':
                    print("❌ Frame display will be blocked")
                elif x_frame_options == 'SAMEORIGIN':
                    print("⚠️  Frame display only from same origin")
                else:
                    print(f"❓ Unknown X-Frame-Options value: {x_frame_options}")
                    
            else:
                print(f"❌ Status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: {e}")
    
    print(f"\n⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    test_xframe_options() 