#!/usr/bin/env python3
"""
Monitoring Setup Script for JewGo API
Sets up UptimeRobot and Cronitor monitoring for API endpoints
"""

import json
import requests
import os
import sys
from typing import Dict, Any

class MonitoringSetup:
    def __init__(self):
        self.uptimerobot_api_key = os.environ.get('UPTIMEROBOT_API_KEY')
        self.cronitor_api_key = os.environ.get('CRONITOR_API_KEY')
        self.api_url = os.environ.get('API_URL', 'https://jewgo.onrender.com')
        self.frontend_url = os.environ.get('FRONTEND_URL', 'https://jewgo.com')
        
    def setup_uptimerobot(self):
        """Set up UptimeRobot monitors."""
        if not self.uptimerobot_api_key:
            print("❌ UPTIMEROBOT_API_KEY not found in environment variables")
            return False
            
        print("🔧 Setting up UptimeRobot monitors...")
        
        # Load configuration
        with open('monitoring/uptimerobot-config.json', 'r') as f:
            config = json.load(f)
        
        # Update URLs with actual domain
        for monitor in config['monitors']:
            monitor['url'] = monitor['url'].replace('https://jewgo.onrender.com', self.api_url)
            monitor['url'] = monitor['url'].replace('https://jewgo.com', self.frontend_url)
        
        # Create monitors via UptimeRobot API
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cache-Control': 'no-cache'
        }
        
        for monitor in config['monitors']:
            data = {
                'api_key': self.uptimerobot_api_key,
                'format': 'json',
                'type': 1,  # HTTP(s)
                'url': monitor['url'],
                'friendly_name': monitor['name'],
                'interval': monitor['interval'],
                'timeout': monitor['timeout'],
                'alert_contacts': ','.join(monitor['alert_contacts'])
            }
            
            try:
                response = requests.post(
                    'https://api.uptimerobot.com/v2/newMonitor',
                    headers=headers,
                    data=data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('stat') == 'ok':
                        print(f"✅ Created UptimeRobot monitor: {monitor['name']}")
                    else:
                        print(f"❌ Failed to create monitor {monitor['name']}: {result.get('error', {}).get('message')}")
                else:
                    print(f"❌ HTTP error creating monitor {monitor['name']}: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error creating UptimeRobot monitor {monitor['name']}: {e}")
        
        return True
    
    def setup_cronitor(self):
        """Set up Cronitor monitors."""
        if not self.cronitor_api_key:
            print("❌ CRONITOR_API_KEY not found in environment variables")
            return False
            
        print("🔧 Setting up Cronitor monitors...")
        
        # Load configuration
        with open('monitoring/cronitor-config.json', 'r') as f:
            config = json.load(f)
        
        # Update URLs with actual domain
        for monitor in config['monitors']:
            monitor['url'] = monitor['url'].replace('https://jewgo.onrender.com', self.api_url)
            monitor['url'] = monitor['url'].replace('https://jewgo.com', self.frontend_url)
        
        headers = {
            'Authorization': f'Bearer {self.cronitor_api_key}',
            'Content-Type': 'application/json'
        }
        
        for monitor in config['monitors']:
            data = {
                'name': monitor['name'],
                'display_name': monitor['display_name'],
                'type': 'http',
                'url': monitor['url'],
                'interval': monitor['interval'],
                'timeout': monitor['timeout'],
                'retries': monitor['retries'],
                'expected_status': monitor['expected_status'],
                'tags': monitor['tags'],
                'group': monitor['group']
            }
            
            try:
                response = requests.post(
                    'https://cronitor.io/api/monitors',
                    headers=headers,
                    json=data
                )
                
                if response.status_code in [200, 201]:
                    print(f"✅ Created Cronitor monitor: {monitor['display_name']}")
                else:
                    print(f"❌ Failed to create Cronitor monitor {monitor['display_name']}: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error creating Cronitor monitor {monitor['display_name']}: {e}")
        
        return True
    
    def test_endpoints(self):
        """Test the monitoring endpoints to ensure they're working."""
        print("🧪 Testing monitoring endpoints...")
        
        endpoints = [
            f"{self.api_url}/health",
            f"{self.api_url}/ping",
            f"{self.api_url}/api/restaurants?limit=1",
            self.frontend_url
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(endpoint, timeout=30)
                if response.status_code == 200:
                    print(f"✅ {endpoint} - Status: {response.status_code}")
                else:
                    print(f"⚠️  {endpoint} - Status: {response.status_code}")
            except Exception as e:
                print(f"❌ {endpoint} - Error: {e}")
    
    def generate_instructions(self):
        """Generate setup instructions."""
        print("\n📋 Manual Setup Instructions:")
        print("=" * 50)
        
        print("\n🔧 UptimeRobot Setup:")
        print("1. Go to https://uptimerobot.com and create an account")
        print("2. Get your API key from Account Settings > API")
        print("3. Set environment variable: UPTIMEROBOT_API_KEY=your_api_key")
        print("4. Run: python monitoring/setup_monitoring.py --uptimerobot")
        
        print("\n🔧 Cronitor Setup:")
        print("1. Go to https://cronitor.io and create an account")
        print("2. Get your API key from Account Settings > API")
        print("3. Set environment variable: CRONITOR_API_KEY=your_api_key")
        print("4. Run: python monitoring/setup_monitoring.py --cronitor")
        
        print("\n🔧 Manual Monitor Creation:")
        print("Create these monitors manually if automated setup fails:")
        
        monitors = [
            {
                "name": "JewGo API Health Check",
                "url": f"{self.api_url}/health",
                "expected": "status: healthy"
            },
            {
                "name": "JewGo API Ping",
                "url": f"{self.api_url}/ping",
                "expected": "pong: true"
            },
            {
                "name": "JewGo API Restaurants",
                "url": f"{self.api_url}/api/restaurants?limit=1",
                "expected": "success: true"
            },
            {
                "name": "JewGo Frontend",
                "url": self.frontend_url,
                "expected": "status: 200"
            }
        ]
        
        for i, monitor in enumerate(monitors, 1):
            print(f"{i}. {monitor['name']}")
            print(f"   URL: {monitor['url']}")
            print(f"   Expected: {monitor['expected']}")
            print()

def main():
    setup = MonitoringSetup()
    
    if len(sys.argv) > 1:
        if '--test' in sys.argv:
            setup.test_endpoints()
        elif '--uptimerobot' in sys.argv:
            setup.setup_uptimerobot()
        elif '--cronitor' in sys.argv:
            setup.setup_cronitor()
        elif '--all' in sys.argv:
            setup.test_endpoints()
            setup.setup_uptimerobot()
            setup.setup_cronitor()
        else:
            setup.generate_instructions()
    else:
        setup.generate_instructions()

if __name__ == "__main__":
    main() 