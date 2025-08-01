#!/usr/bin/env python3
"""
Backend Restart Script for JewGo
===============================

This script helps restart the backend service on Render when it's experiencing timeout issues.
It can be used to:
1. Check the current status of the backend
2. Trigger a manual restart if needed
3. Monitor the restart process

Usage:
    python scripts/deployment/restart_backend.py --check
    python scripts/deployment/restart_backend.py --restart
    python scripts/deployment/restart_backend.py --monitor
"""

import os
import sys
import time
import json
import requests
import argparse
from datetime import datetime
from typing import Dict, Any, Optional

# Configuration
BACKEND_URL = "https://jewgo.onrender.com"
HEALTH_ENDPOINT = f"{BACKEND_URL}/health"
RESTAURANTS_ENDPOINT = f"{BACKEND_URL}/api/restaurants"

class BackendMonitor:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 15  # 15 second timeout
    
    def check_health(self) -> Dict[str, Any]:
        """Check the health of the backend service."""
        try:
            start_time = time.time()
            response = self.session.get(HEALTH_ENDPOINT)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "healthy",
                    "response_time": response_time,
                    "data": data,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "unhealthy",
                    "response_time": response_time,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "timestamp": datetime.now().isoformat()
                }
        except requests.exceptions.Timeout:
            return {
                "status": "timeout",
                "response_time": 15000,
                "error": "Request timed out after 15 seconds",
                "timestamp": datetime.now().isoformat()
            }
        except requests.exceptions.ConnectionError:
            return {
                "status": "connection_error",
                "response_time": 0,
                "error": "Connection failed - service may be down",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "response_time": 0,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def check_restaurants_api(self) -> Dict[str, Any]:
        """Check if the restaurants API is working."""
        try:
            start_time = time.time()
            response = self.session.get(f"{RESTAURANTS_ENDPOINT}?limit=1")
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "working",
                    "response_time": response_time,
                    "has_data": bool(data.get("restaurants") or (isinstance(data, list) and len(data) > 0)),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "response_time": response_time,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "timestamp": datetime.now().isoformat()
                }
        except requests.exceptions.Timeout:
            return {
                "status": "timeout",
                "response_time": 15000,
                "error": "Request timed out after 15 seconds",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "response_time": 0,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def print_status(self, health_status: Dict[str, Any], restaurants_status: Dict[str, Any]):
        """Print a formatted status report."""
        print("🔍 JewGo Backend Status Report")
        print("=" * 50)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Health endpoint status
        print("🏥 Health Endpoint:")
        if health_status["status"] == "healthy":
            print(f"  ✅ Status: Healthy ({health_status['response_time']:.0f}ms)")
            if "data" in health_status:
                data = health_status["data"]
                print(f"  📊 Database: {data.get('database', 'unknown')}")
                print(f"  🍽️  Restaurants: {data.get('restaurants_count', 'unknown')}")
                print(f"  🔧 Version: {data.get('version', 'unknown')}")
        else:
            print(f"  ❌ Status: {health_status['status'].title()}")
            print(f"  ⏱️  Response Time: {health_status['response_time']:.0f}ms")
            if "error" in health_status:
                print(f"  🚨 Error: {health_status['error']}")
        print()
        
        # Restaurants API status
        print("🍽️  Restaurants API:")
        if restaurants_status["status"] == "working":
            print(f"  ✅ Status: Working ({restaurants_status['response_time']:.0f}ms)")
            print(f"  📊 Has Data: {restaurants_status.get('has_data', 'unknown')}")
        else:
            print(f"  ❌ Status: {restaurants_status['status'].title()}")
            print(f"  ⏱️  Response Time: {restaurants_status['response_time']:.0f}ms")
            if "error" in restaurants_status:
                print(f"  🚨 Error: {restaurants_status['error']}")
        print()
        
        # Overall assessment
        if health_status["status"] == "healthy" and restaurants_status["status"] == "working":
            print("🎉 Overall Status: All systems operational!")
        elif health_status["status"] in ["timeout", "connection_error"]:
            print("⚠️  Overall Status: Backend appears to be down or in sleep mode")
            print("   💡 Try visiting https://jewgo.onrender.com to wake up the service")
        else:
            print("⚠️  Overall Status: Backend has issues")
    
    def monitor_restart(self, duration: int = 300):
        """Monitor the backend during a restart process."""
        print(f"🔄 Monitoring backend restart for {duration} seconds...")
        print("=" * 50)
        
        start_time = time.time()
        check_interval = 10  # Check every 10 seconds
        
        while time.time() - start_time < duration:
            health_status = self.check_health()
            restaurants_status = self.check_restaurants_api()
            
            elapsed = time.time() - start_time
            print(f"\n[{elapsed:.0f}s] Status Check:")
            self.print_status(health_status, restaurants_status)
            
            # If both endpoints are working, we can stop monitoring
            if (health_status["status"] == "healthy" and 
                restaurants_status["status"] == "working"):
                print("\n🎉 Backend is back online!")
                break
            
            # Wait before next check
            if time.time() - start_time < duration:
                print(f"\n⏳ Waiting {check_interval} seconds before next check...")
                time.sleep(check_interval)
        else:
            print(f"\n⏰ Monitoring period ({duration}s) completed")

def main():
    parser = argparse.ArgumentParser(description="JewGo Backend Monitor and Restart Tool")
    parser.add_argument("--check", action="store_true", help="Check current backend status")
    parser.add_argument("--restart", action="store_true", help="Trigger manual restart (opens Render dashboard)")
    parser.add_argument("--monitor", action="store_true", help="Monitor backend status")
    parser.add_argument("--duration", type=int, default=300, help="Monitoring duration in seconds (default: 300)")
    
    args = parser.parse_args()
    
    if not any([args.check, args.restart, args.monitor]):
        parser.print_help()
        return
    
    monitor = BackendMonitor()
    
    if args.check:
        print("🔍 Checking backend status...")
        health_status = monitor.check_health()
        restaurants_status = monitor.check_restaurants_api()
        monitor.print_status(health_status, restaurants_status)
    
    if args.restart:
        print("🔄 Manual Restart Instructions:")
        print("=" * 50)
        print("1. Open your browser and go to: https://dashboard.render.com")
        print("2. Find the 'jewgo-backend' service")
        print("3. Click on the service to open its dashboard")
        print("4. Click the 'Manual Deploy' button")
        print("5. Wait for the deployment to complete")
        print("6. Use --monitor to watch the restart process")
        print()
        print("💡 Alternative: Visit https://jewgo.onrender.com to wake up the service")
    
    if args.monitor:
        monitor.monitor_restart(args.duration)

if __name__ == "__main__":
    main() 