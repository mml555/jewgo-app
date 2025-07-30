#!/usr/bin/env python3
"""
Script to check deployment status and provide information about validation logic update
"""

import requests
import json
from datetime import datetime

# Remote backend URL
REMOTE_BACKEND_URL = "https://jewgo.onrender.com"

def check_deployment_status():
    """Check the current deployment status"""
    try:
        print("🔍 Checking remote backend deployment status...")
        print("=" * 50)
        
        response = requests.get(f"{REMOTE_BACKEND_URL}/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            current_version = data.get('version', 'unknown')
            
            print(f"📊 Current Version: {current_version}")
            print(f"🎯 Target Version: 1.0.3")
            print(f"📡 Status: {data.get('status', 'unknown')}")
            print(f"📝 Message: {data.get('message', 'N/A')}")
            
            if current_version == '1.0.3':
                print("\n✅ DEPLOYMENT COMPLETED SUCCESSFULLY!")
                print("🔧 FPT Feed Validation Logic is now active!")
                return True
            else:
                print(f"\n⏳ Deployment in progress...")
                print(f"   Current version: {current_version}")
                print(f"   Expected version: 1.0.3")
                print(f"   This may take 5-10 minutes for Render to complete the deployment")
                return False
                
        else:
            print(f"❌ Remote backend returned status {response.status_code}")
            print("   This might indicate the backend is still deploying...")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Cannot connect to remote backend: {e}")
        print("   This might indicate the backend is still deploying...")
        return False

def show_validation_features():
    """Show the new validation features that will be available"""
    print("\n🔧 NEW FPT FEED VALIDATION FEATURES:")
    print("=" * 50)
    print("✅ Certifying Agency Validation")
    print("   - Validates against: ORB, OU, KOF-K, Star-K, CRC, Vaad HaRabbonim")
    print("   - Prevents invalid agency assignments")
    print()
    print("✅ Kosher Category Validation")
    print("   - Validates against: meat, dairy, pareve, fish, unknown")
    print("   - Ensures proper category classification")
    print()
    print("✅ Business ID Duplicate Detection")
    print("   - Checks for existing business IDs in the database")
    print("   - Prevents duplicate restaurant entries")
    print()
    print("✅ Data Format Validation")
    print("   - Phone number format validation")
    print("   - Website URL format validation")
    print("   - Address completeness validation")
    print()
    print("✅ Required Field Validation")
    print("   - Ensures restaurant name is provided")
    print("   - Ensures business ID is provided")
    print()

def show_deployment_instructions():
    """Show instructions for monitoring deployment"""
    print("📋 DEPLOYMENT MONITORING INSTRUCTIONS:")
    print("=" * 50)
    print("1. The code changes have been successfully pushed to the repository")
    print("2. Render is automatically deploying the updated code")
    print("3. Deployment typically takes 5-10 minutes")
    print("4. You can monitor progress by running this script periodically:")
    print("   python check_deployment_status.py")
    print()
    print("5. Once version shows 1.0.3, the validation logic will be active")
    print("6. All new restaurant additions will be validated against FPT feed")
    print()

def main():
    """Main function"""
    print("🚀 JewGo Backend Deployment Status Check")
    print("=" * 50)
    print(f"⏰ Checked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check current status
    is_deployed = check_deployment_status()
    
    # Show features
    show_validation_features()
    
    # Show instructions
    show_deployment_instructions()
    
    if not is_deployed:
        print("🔄 Deployment Status: IN PROGRESS")
        print("   Please check again in a few minutes")
    else:
        print("✅ Deployment Status: COMPLETED")
        print("   FPT feed validation is now active!")

if __name__ == "__main__":
    main() 