#!/usr/bin/env python3
"""
Redeployment Trigger Script

This script helps trigger a redeployment of the backend to apply the fixes.
It also provides verification tools to check the deployment status.
"""

import os
import sys
import time
import requests
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_endpoint(url, name="endpoint"):
    """Check if an endpoint is responding correctly."""
    try:
        response = requests.get(url, timeout=10)
        logger.info(f"✅ {name}: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                logger.info(f"   Response: {data.get('message', 'No message')}")
            except:
                logger.info(f"   Response: {response.text[:100]}...")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"❌ {name}: {e}")
        return False

def wait_for_deployment(max_wait=300):
    """Wait for deployment to complete."""
    logger.info("⏳ Waiting for deployment to complete...")
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        if check_endpoint("https://jewgo.onrender.com/health", "Health endpoint"):
            logger.info("✅ Deployment appears to be complete!")
            return True
        time.sleep(10)
    
    logger.warning("⏰ Timeout waiting for deployment")
    return False

def verify_fixes():
    """Verify that all fixes are working."""
    logger.info("🔍 Verifying fixes...")
    
    # Check health endpoint
    health_ok = check_endpoint("https://jewgo.onrender.com/health", "Health endpoint")
    
    # Check root endpoint
    root_ok = check_endpoint("https://jewgo.onrender.com/", "Root endpoint")
    
    # Check restaurants endpoint
    restaurants_ok = check_endpoint("https://jewgo.onrender.com/api/restaurants?limit=1", "Restaurants endpoint")
    
    if health_ok and root_ok and restaurants_ok:
        logger.info("🎉 All endpoints are working correctly!")
        return True
    else:
        logger.warning("⚠️  Some endpoints are not working correctly")
        return False

def main():
    """Main script function."""
    logger.info("🚀 Backend Redeployment Verification Script")
    logger.info("=" * 50)
    
    # Check current status
    logger.info("📊 Current Status:")
    check_endpoint("https://jewgo.onrender.com/health", "Health endpoint")
    check_endpoint("https://jewgo.onrender.com/", "Root endpoint")
    
    logger.info("\n📋 Next Steps:")
    logger.info("1. Commit and push the changes to trigger a new deployment")
    logger.info("2. Wait for the deployment to complete (usually 2-5 minutes)")
    logger.info("3. Run this script again to verify the fixes")
    
    logger.info("\n🔧 Manual Verification Commands:")
    logger.info("curl https://jewgo.onrender.com/health")
    logger.info("curl https://jewgo.onrender.com/")
    logger.info("curl https://jewgo.onrender.com/api/restaurants?limit=1")
    
    logger.info("\n📝 Expected Changes After Deployment:")
    logger.info("- Root endpoint (/) should return API information instead of 404")
    logger.info("- Reduced timezone warnings in logs")
    logger.info("- No more development server warnings")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 