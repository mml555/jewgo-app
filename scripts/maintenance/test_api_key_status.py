#!/usr/bin/env python3
"""
Test API Key Status
==================

Simple script to test if the Google Places API key is expired or quota-limited.
"""

import os
import requests
import json

def test_api_key():
    """Test the Google Places API key status."""
    print("🔍 Testing Google Places API Key Status")
    print("=" * 50)
    
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not api_key:
        print("❌ GOOGLE_PLACES_API_KEY not set")
        return
    
    print(f"✅ API Key found (length: {len(api_key)})")
    print(f"🔑 Key starts with: {api_key[:10]}...")
    
    # Test with a simple query
    test_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': 'Starbucks',
        'key': api_key
    }
    
    print(f"\n🔍 Testing API call...")
    try:
        response = requests.get(test_url, params=params, timeout=10)
        data = response.json()
        
        status = data.get('status', 'UNKNOWN')
        error_message = data.get('error_message', '')
        
        print(f"📊 Response Status: {status}")
        
        if status == 'OK':
            print("✅ API Key is working correctly!")
            print("✅ No quota or expiration issues")
            return True
            
        elif status == 'OVER_QUERY_LIMIT':
            print("❌ QUOTA LIMIT REACHED")
            print("   You've hit the 25,000 requests/day limit")
            print("   Solution: Enable Google Cloud billing")
            return False
            
        elif status == 'REQUEST_DENIED':
            print("❌ REQUEST DENIED")
            if 'expired' in error_message.lower():
                print("   The API key is EXPIRED")
                print("   Solution: Create a new API key")
            elif 'quota' in error_message.lower():
                print("   QUOTA LIMIT reached")
                print("   Solution: Enable Google Cloud billing")
            else:
                print(f"   Error: {error_message}")
                print("   Possible causes:")
                print("   - API key restrictions")
                print("   - Places API not enabled")
                print("   - Billing not enabled")
            return False
            
        elif status == 'INVALID_REQUEST':
            print("❌ INVALID REQUEST")
            print("   The API key format is invalid")
            return False
            
        elif status == 'ZERO_RESULTS':
            print("✅ API Key is working (no results found)")
            print("✅ No quota or expiration issues")
            return True
            
        else:
            print(f"⚠️  UNKNOWN STATUS: {status}")
            print(f"   Error message: {error_message}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def provide_solutions():
    """Provide solutions based on the test results."""
    print(f"\n🔧 SOLUTIONS")
    print("=" * 20)
    
    print("1. **If API Key is EXPIRED:**")
    print("   - Go to Google Cloud Console")
    print("   - Navigate to APIs & Services > Credentials")
    print("   - Create a new API key")
    print("   - Enable billing for the key")
    print("   - Update your environment variables")
    
    print(f"\n2. **If QUOTA LIMIT reached:**")
    print("   - Enable Google Cloud billing")
    print("   - Request quota increase")
    print("   - Use the quota-aware updater")
    print("   - Process restaurants in batches")
    
    print(f"\n3. **If REQUEST DENIED (other reasons):**")
    print("   - Check API key restrictions")
    print("   - Ensure Places API is enabled")
    print("   - Verify billing is active")
    print("   - Check API key permissions")

def main():
    """Main function."""
    print("🚀 Google Places API Key Status Check")
    print("=" * 50)
    
    # Test the API key
    is_working = test_api_key()
    
    # Provide solutions
    provide_solutions()
    
    # Final recommendation
    print(f"\n🎯 RECOMMENDATION")
    print("=" * 20)
    
    if is_working:
        print("✅ Your API key is working!")
        print("✅ You can proceed with the hours update")
        print("🔧 Run: python scripts/maintenance/quota_aware_hours_updater.py")
    else:
        print("❌ API key has issues")
        print("🔧 Follow the solutions above to fix the issue")
        print("📖 See: GOOGLE_PLACES_QUOTA_SETUP_GUIDE.md")

if __name__ == "__main__":
    main() 