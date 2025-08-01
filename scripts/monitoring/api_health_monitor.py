#!/usr/bin/env python3
"""
API Health Monitor
=================

This script monitors the JewGo API endpoints to ensure they're working correctly
and alerts on any issues. It can be run as a cron job for continuous monitoring.

Author: JewGo Development Team
Version: 1.0
"""

import requests
import json
import time
import sys
import os
from datetime import datetime
from typing import Dict, Any, List

# Configuration
API_BASE_URL = "https://jewgo.onrender.com"
HEALTH_ENDPOINTS = [
    "/health",
    "/api/restaurants?limit=10",
    "/api/statistics",
    "/api/kosher-types"
]

# Test restaurant IDs to check
TEST_RESTAURANT_IDS = [1262, 1100, 1377]  # Include the problematic ID and range endpoints

class APIHealthMonitor:
    def __init__(self):
        self.results = []
        self.errors = []
        
    def check_endpoint(self, endpoint: str, expected_status: int = 200) -> Dict[str, Any]:
        """Check a single API endpoint."""
        url = f"{API_BASE_URL}{endpoint}"
        start_time = time.time()
        
        try:
            response = requests.get(url, timeout=30)
            response_time = time.time() - start_time
            
            result = {
                "endpoint": endpoint,
                "url": url,
                "status_code": response.status_code,
                "response_time": round(response_time, 3),
                "success": response.status_code == expected_status,
                "timestamp": datetime.now().isoformat()
            }
            
            # Try to parse JSON response
            try:
                result["data"] = response.json()
            except json.JSONDecodeError:
                result["data"] = None
                result["error"] = "Invalid JSON response"
            
            if not result["success"]:
                self.errors.append(f"Endpoint {endpoint} failed: {response.status_code}")
                
            return result
            
        except requests.exceptions.Timeout:
            error_msg = f"Timeout for endpoint {endpoint}"
            self.errors.append(error_msg)
            return {
                "endpoint": endpoint,
                "url": url,
                "status_code": None,
                "response_time": None,
                "success": False,
                "error": error_msg,
                "timestamp": datetime.now().isoformat()
            }
        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed for endpoint {endpoint}: {str(e)}"
            self.errors.append(error_msg)
            return {
                "endpoint": endpoint,
                "url": url,
                "status_code": None,
                "response_time": None,
                "success": False,
                "error": error_msg,
                "timestamp": datetime.now().isoformat()
            }
    
    def check_restaurant_endpoints(self) -> List[Dict[str, Any]]:
        """Check specific restaurant endpoints."""
        results = []
        
        for restaurant_id in TEST_RESTAURANT_IDS:
            endpoint = f"/api/restaurants/{restaurant_id}"
            result = self.check_endpoint(endpoint)
            results.append(result)
            
            # Add a small delay between requests
            time.sleep(0.5)
            
        return results
    
    def run_health_check(self) -> Dict[str, Any]:
        """Run comprehensive health check."""
        print(f"Starting API health check at {datetime.now()}")
        print(f"Base URL: {API_BASE_URL}")
        print("-" * 50)
        
        # Check basic health endpoints
        for endpoint in HEALTH_ENDPOINTS:
            result = self.check_endpoint(endpoint)
            self.results.append(result)
            print(f"✓ {endpoint}: {result['status_code']} ({result['response_time']}s)")
        
        # Check specific restaurant endpoints
        print("\nChecking restaurant endpoints...")
        restaurant_results = self.check_restaurant_endpoints()
        self.results.extend(restaurant_results)
        
        for result in restaurant_results:
            status = "✓" if result["success"] else "✗"
            print(f"{status} {result['endpoint']}: {result['status_code']} ({result['response_time']}s)")
        
        # Generate summary
        total_checks = len(self.results)
        successful_checks = sum(1 for r in self.results if r["success"])
        failed_checks = total_checks - successful_checks
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_checks": total_checks,
            "successful_checks": successful_checks,
            "failed_checks": failed_checks,
            "success_rate": round((successful_checks / total_checks) * 100, 2),
            "errors": self.errors,
            "results": self.results
        }
        
        print("\n" + "=" * 50)
        print(f"Health Check Summary:")
        print(f"Total checks: {total_checks}")
        print(f"Successful: {successful_checks}")
        print(f"Failed: {failed_checks}")
        print(f"Success rate: {summary['success_rate']}%")
        
        if self.errors:
            print(f"\nErrors found:")
            for error in self.errors:
                print(f"  - {error}")
        
        return summary
    
    def save_results(self, summary: Dict[str, Any], filename: str = None):
        """Save results to a JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"api_health_check_{timestamp}.json"
        
        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)
        filepath = os.path.join("logs", filename)
        
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\nResults saved to: {filepath}")
        return filepath

def main():
    """Main function."""
    monitor = APIHealthMonitor()
    
    try:
        summary = monitor.run_health_check()
        
        # Save results
        monitor.save_results(summary)
        
        # Exit with error code if there are failures
        if summary["failed_checks"] > 0:
            print(f"\n❌ Health check failed with {summary['failed_checks']} errors")
            sys.exit(1)
        else:
            print(f"\n✅ All health checks passed!")
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\nHealth check interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Health check failed with exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 