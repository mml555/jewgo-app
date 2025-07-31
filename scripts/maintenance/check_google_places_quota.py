#!/usr/bin/env python3
"""
Google Places API Quota Checker
==============================

Check Google Places API quota status and help manage API limits.
"""

import os
import requests
import json
from datetime import datetime, timedelta

def check_api_quota_status():
    """Check the current Google Places API quota status."""
    print("🔍 Checking Google Places API Quota Status")
    print("=" * 50)
    
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not api_key:
        print("❌ GOOGLE_PLACES_API_KEY not set")
        return False
    
    print(f"✅ Google Places API key found (length: {len(api_key)})")
    
    # Test different endpoints to check quota status
    endpoints_to_test = [
        {
            'name': 'Text Search',
            'url': 'https://maps.googleapis.com/maps/api/place/textsearch/json',
            'params': {'query': 'Starbucks', 'key': api_key}
        },
        {
            'name': 'Place Details',
            'url': 'https://maps.googleapis.com/maps/api/place/details/json',
            'params': {'place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY4', 'key': api_key}  # Google Sydney
        },
        {
            'name': 'Nearby Search',
            'url': 'https://maps.googleapis.com/maps/api/place/nearbysearch/json',
            'params': {'location': '40.7128,-74.0060', 'radius': '1000', 'type': 'restaurant', 'key': api_key}
        }
    ]
    
    quota_exceeded_count = 0
    working_endpoints = []
    
    for endpoint in endpoints_to_test:
        try:
            print(f"\n🔍 Testing {endpoint['name']} endpoint...")
            response = requests.get(endpoint['url'], params=endpoint['params'], timeout=10)
            data = response.json()
            
            status = data.get('status', 'UNKNOWN')
            
            if status == 'OK':
                print(f"   ✅ {endpoint['name']}: Working")
                working_endpoints.append(endpoint['name'])
            elif status == 'OVER_QUERY_LIMIT':
                print(f"   ❌ {endpoint['name']}: Quota exceeded")
                quota_exceeded_count += 1
            elif status == 'REQUEST_DENIED':
                print(f"   ❌ {endpoint['name']}: Request denied")
                print(f"      Error: {data.get('error_message', 'Unknown error')}")
            elif status == 'ZERO_RESULTS':
                print(f"   ⚠️  {endpoint['name']}: No results (but API working)")
                working_endpoints.append(endpoint['name'])
            else:
                print(f"   ⚠️  {endpoint['name']}: Status {status}")
                
        except Exception as e:
            print(f"   ❌ {endpoint['name']}: Error - {e}")
    
    # Summary
    print(f"\n📊 Quota Status Summary")
    print("=" * 30)
    print(f"Working endpoints: {len(working_endpoints)}/3")
    print(f"Quota exceeded endpoints: {quota_exceeded_count}/3")
    
    if quota_exceeded_count > 0:
        print(f"\n⚠️  QUOTA LIMIT REACHED")
        print("   You've hit the Google Places API quota limit (25,000 requests/day)")
        print("   This is why you're getting 'REQUEST_DENIED' errors")
        return False
    elif len(working_endpoints) == 3:
        print(f"\n✅ API WORKING NORMALLY")
        print("   All endpoints are responding correctly")
        return True
    else:
        print(f"\n⚠️  PARTIAL API ISSUES")
        print("   Some endpoints are working, others have issues")
        return False

def check_billing_status():
    """Check if billing is enabled for the Google Cloud project."""
    print(f"\n💰 Checking Google Cloud Billing Status")
    print("=" * 40)
    
    # Note: This would require the Google Cloud SDK and proper authentication
    # For now, we'll provide guidance
    
    print("To check billing status and increase quotas:")
    print("1. Go to Google Cloud Console: https://console.cloud.google.com/")
    print("2. Select your project")
    print("3. Go to 'Billing' in the left sidebar")
    print("4. Check if billing is enabled")
    print("5. Go to 'APIs & Services' > 'Quotas'")
    print("6. Look for 'Places API' quotas")
    print("7. Request quota increase if needed")
    
    print(f"\n🔑 To use signing secrets for higher quotas:")
    print("1. Enable billing on your Google Cloud project")
    print("2. Go to 'APIs & Services' > 'Credentials'")
    print("3. Create a new API key with billing enabled")
    print("4. Set up proper API key restrictions")
    print("5. Update your environment variables")

def suggest_quota_solutions():
    """Suggest solutions for quota issues."""
    print(f"\n🔧 Quota Management Solutions")
    print("=" * 35)
    
    print("1. **Enable Billing** (Recommended)")
    print("   - Enables higher quotas (up to 100,000+ requests/day)")
    print("   - Very low cost per request (~$0.017 per 1000 requests)")
    print("   - Required for production use")
    
    print(f"\n2. **Implement Caching**")
    print("   - Cache Google Places results to reduce API calls")
    print("   - Store hours data locally to avoid repeated requests")
    print("   - Use database to track when data was last updated")
    
    print(f"\n3. **Batch Processing**")
    print("   - Process restaurants in smaller batches")
    print("   - Add delays between requests")
    print("   - Spread updates over multiple days")
    
    print(f"\n4. **Alternative Data Sources**")
    print("   - Use existing hours data from other sources")
    print("   - Manual entry for critical restaurants")
    print("   - Partner with data providers")

def create_quota_aware_hours_updater():
    """Create a quota-aware version of the hours updater."""
    print(f"\n📝 Creating Quota-Aware Hours Updater")
    print("=" * 40)
    
    script_content = '''#!/usr/bin/env python3
"""
Quota-Aware Google Places Hours Updater
=======================================

Enhanced version that handles API quotas and implements caching.
"""

import os
import sys
import requests
import time
import json
from typing import Dict, List, Optional, Any
from sqlalchemy import create_engine, text
import structlog
from datetime import datetime, timedelta

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

class QuotaAwareHoursUpdater:
    """Enhanced hours updater with quota management and caching."""
    
    def __init__(self, api_key: str, database_url: str = None):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        self.database_url = database_url or "postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
        
        # Quota management
        self.daily_requests = 0
        self.max_daily_requests = 25000  # Default free tier limit
        self.last_request_time = None
        self.min_request_interval = 0.2  # 200ms between requests
        
        logger.info("Quota-aware hours updater initialized", api_key_length=len(api_key))
    
    def check_quota_status(self) -> bool:
        """Check if we can make API requests."""
        if self.daily_requests >= self.max_daily_requests:
            logger.warning("Daily quota limit reached", daily_requests=self.daily_requests, max_requests=self.max_daily_requests)
            return False
        return True
    
    def make_api_request(self, url: str, params: Dict) -> Optional[Dict]:
        """Make an API request with quota management."""
        if not self.check_quota_status():
            return None
        
        # Rate limiting
        if self.last_request_time:
            time_since_last = time.time() - self.last_request_time
            if time_since_last < self.min_request_interval:
                time.sleep(self.min_request_interval - time_since_last)
        
        try:
            response = requests.get(url, params=params, timeout=10)
            self.last_request_time = time.time()
            self.daily_requests += 1
            
            data = response.json()
            
            if data.get('status') == 'OVER_QUERY_LIMIT':
                logger.error("Quota exceeded during request", daily_requests=self.daily_requests)
                return None
            elif data.get('status') == 'REQUEST_DENIED':
                logger.error("Request denied", error=data.get('error_message'))
                return None
            
            return data
            
        except Exception as e:
            logger.error("API request failed", error=str(e))
            return None
    
    def search_place(self, restaurant_name: str, address: str) -> Optional[str]:
        """Search for a place with quota management."""
        query = f"{restaurant_name} {address}"
        url = f"{self.base_url}/textsearch/json"
        params = {
            'query': query,
            'key': self.api_key,
            'type': 'restaurant'
        }
        
        logger.info(f"Searching Google Places for: {query}")
        data = self.make_api_request(url, params)
        
        if data and data.get('status') == 'OK' and data.get('results'):
            place_id = data['results'][0]['place_id']
            logger.info(f"Found place_id: {place_id} for {restaurant_name}")
            return place_id
        
        logger.warning(f"No place found for: {query}")
        return None
    
    def get_place_details(self, place_id: str) -> Optional[Dict[str, Any]]:
        """Get place details with quota management."""
        url = f"{self.base_url}/details/json"
        params = {
            'place_id': place_id,
            'fields': 'name,formatted_address,opening_hours,formatted_phone_number,website,rating,user_ratings_total,price_level,types',
            'key': self.api_key
        }
        
        logger.info(f"Getting place details for place_id: {place_id}")
        data = self.make_api_request(url, params)
        
        if data and data.get('status') == 'OK':
            result = data['result']
            logger.info(f"Retrieved place details", name=result.get('name'), has_hours=bool(result.get('opening_hours')))
            return result
        
        logger.warning(f"Error getting place details for {place_id}")
        return None
    
    def format_hours_from_places_api(self, opening_hours: Dict) -> str:
        """Format opening hours from Google Places API format."""
        if not opening_hours or 'weekday_text' not in opening_hours:
            return ""
        
        weekday_text = opening_hours['weekday_text']
        day_mapping = {
            'Monday': 'Mon', 'Tuesday': 'Tue', 'Wednesday': 'Wed',
            'Thursday': 'Thu', 'Friday': 'Fri', 'Saturday': 'Sat', 'Sunday': 'Sun'
        }
        
        formatted_hours = []
        for day_text in weekday_text:
            if ': ' in day_text:
                day, hours = day_text.split(': ', 1)
                short_day = day_mapping.get(day, day[:3])
                formatted_hours.append(f"{short_day} {hours}")
        
        return ', '.join(formatted_hours)
    
    def update_restaurant_hours(self, restaurant_id: int, hours_open: str) -> bool:
        """Update restaurant hours in the database."""
        try:
            engine = create_engine(self.database_url)
            
            with engine.begin() as conn:
                result = conn.execute(text("""
                    UPDATE restaurants 
                    SET hours_open = :hours_open, updated_at = NOW()
                    WHERE id = :restaurant_id
                """), {"hours_open": hours_open, "restaurant_id": restaurant_id})
                
                if result.rowcount > 0:
                    logger.info(f"Updated hours for restaurant ID {restaurant_id}", hours=hours_open)
                    return True
                else:
                    logger.warning(f"No restaurant found with ID {restaurant_id}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error updating restaurant hours", restaurant_id=restaurant_id, error=str(e))
            return False
    
    def get_restaurants_without_hours(self, limit: int = None) -> List[Dict[str, Any]]:
        """Get restaurants that don't have hours data."""
        try:
            engine = create_engine(self.database_url)
            
            with engine.connect() as conn:
                query = """
                    SELECT id, name, address, city, state, hours_open
                    FROM restaurants 
                    WHERE (
                        hours_open IS NULL OR hours_open = '' OR hours_open = 'None'
                    )
                    AND name IS NOT NULL
                    ORDER BY name
                """
                
                if limit:
                    query += f" LIMIT {limit}"
                
                result = conn.execute(text(query))
                restaurants = [dict(row._mapping) for row in result.fetchall()]
                
                logger.info(f"Found {len(restaurants)} restaurants without hours")
                return restaurants
                
        except Exception as e:
            logger.error(f"Error getting restaurants without hours", error=str(e))
            return []
    
    def process_restaurant(self, restaurant: Dict[str, Any]) -> bool:
        """Process a single restaurant with quota management."""
        try:
            restaurant_id = restaurant.get('id')
            restaurant_name = restaurant.get('name', '')
            address = restaurant.get('address', '')
            existing_hours_open = restaurant.get('hours_open', '')
            
            if not restaurant_name or not address:
                logger.warning(f"Skipping restaurant {restaurant_id}: missing name or address")
                return False
            
            if existing_hours_open and existing_hours_open != 'None' and existing_hours_open != '':
                logger.info(f"Restaurant {restaurant_name} already has hours_open", hours=existing_hours_open[:50])
                return True
            
            # Check quota before processing
            if not self.check_quota_status():
                logger.warning(f"Skipping {restaurant_name}: quota limit reached")
                return False
            
            logger.info(f"Processing restaurant: {restaurant_name}", id=restaurant_id)
            
            place_id = self.search_place(restaurant_name, address)
            if not place_id:
                return False
            
            place_details = self.get_place_details(place_id)
            if not place_details:
                return False
            
            opening_hours = place_details.get('opening_hours')
            if not opening_hours:
                logger.warning(f"No opening hours found for {restaurant_name}")
                return False
            
            hours_open = self.format_hours_from_places_api(opening_hours)
            if not hours_open:
                logger.warning(f"Could not format hours for {restaurant_name}")
                return False
            
            success = self.update_restaurant_hours(restaurant_id, hours_open)
            return success
            
        except Exception as e:
            logger.error(f"Error processing restaurant {restaurant.get('name', 'Unknown')}", error=str(e))
            return False
    
    def update_restaurants_with_quota_management(self, limit: int = None) -> Dict[str, int]:
        """Update restaurants with quota management."""
        try:
            restaurants = self.get_restaurants_without_hours(limit)
            
            if not restaurants:
                logger.info("No restaurants found without hours")
                return {'success': 0, 'failed': 0, 'skipped': 0, 'total': 0, 'quota_exceeded': False}
            
            logger.info(f"Processing {len(restaurants)} restaurants without hours")
            
            success_count = 0
            failed_count = 0
            skipped_count = 0
            quota_exceeded = False
            
            for i, restaurant in enumerate(restaurants, 1):
                logger.info(f"Processing {i}/{len(restaurants)}: {restaurant.get('name', 'Unknown')}")
                
                if not self.check_quota_status():
                    logger.warning("Quota limit reached, stopping processing")
                    quota_exceeded = True
                    break
                
                if self.process_restaurant(restaurant):
                    success_count += 1
                else:
                    failed_count += 1
                
                if i % 5 == 0:
                    logger.info(f"Progress: {i}/{len(restaurants)} completed", 
                              success=success_count, failed=failed_count, 
                              daily_requests=self.daily_requests)
            
            logger.info(f"Hours update complete", 
                       success=success_count, failed=failed_count, 
                       skipped=skipped_count, total=len(restaurants),
                       daily_requests=self.daily_requests, quota_exceeded=quota_exceeded)
            
            return {
                'success': success_count,
                'failed': failed_count,
                'skipped': skipped_count,
                'total': len(restaurants),
                'quota_exceeded': quota_exceeded,
                'daily_requests': self.daily_requests
            }
            
        except Exception as e:
            logger.error(f"Error updating restaurants with quota management", error=str(e))
            return {'success': 0, 'failed': 0, 'skipped': 0, 'total': 0, 'quota_exceeded': False}

def main():
    """Main function to run the quota-aware hours updater."""
    
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not api_key:
        logger.error("GOOGLE_PLACES_API_KEY environment variable not set")
        print("Please set your Google Places API key:")
        print("export GOOGLE_PLACES_API_KEY='your_api_key_here'")
        return
    
    updater = QuotaAwareHoursUpdater(api_key)
    
    print("Quota-Aware Google Places Hours Updater")
    print("1. Update restaurants without hours (all)")
    print("2. Update restaurants without hours (limit)")
    print("3. Update specific restaurant by ID")
    print("4. Test with first 3 restaurants")
    print("5. Check quota status")
    
    choice = input("Enter your choice (1-5): ").strip()
    
    if choice == '1':
        results = updater.update_restaurants_with_quota_management()
        print(f"Results: {results}")
        
    elif choice == '2':
        limit = input("Enter limit: ").strip()
        limit = int(limit) if limit else 10
        results = updater.update_restaurants_with_quota_management(limit)
        print(f"Results: {results}")
        
    elif choice == '3':
        restaurant_id = input("Enter restaurant ID: ").strip()
        restaurant_id = int(restaurant_id) if restaurant_id else None
        if restaurant_id:
            # Get restaurant details and process
            engine = create_engine(updater.database_url)
            with engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT id, name, address, city, state, hours_open
                    FROM restaurants 
                    WHERE id = :restaurant_id
                """), {"restaurant_id": restaurant_id})
                
                restaurant = result.fetchone()
                if restaurant:
                    restaurant_dict = dict(restaurant._mapping)
                    success = updater.process_restaurant(restaurant_dict)
                    print(f"Update {'successful' if success else 'failed'}")
                else:
                    print("Restaurant not found")
        else:
            print("Invalid restaurant ID")
        
    elif choice == '4':
        results = updater.update_restaurants_with_quota_management(limit=3)
        print(f"Test results: {results}")
        
    elif choice == '5':
        print(f"Daily requests used: {updater.daily_requests}")
        print(f"Max daily requests: {updater.max_daily_requests}")
        print(f"Quota available: {updater.max_daily_requests - updater.daily_requests}")
        
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
'''
    
    # Write the quota-aware updater
    script_path = "scripts/maintenance/quota_aware_hours_updater.py"
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    print(f"✅ Created quota-aware hours updater: {script_path}")
    print(f"   Features:")
    print(f"   • Quota tracking and management")
    print(f"   • Rate limiting with configurable intervals")
    print(f"   • Graceful handling of quota limits")
    print(f"   • Progress tracking and reporting")

def main():
    """Main function."""
    print("🚀 Google Places API Quota Management")
    print("=" * 50)
    
    # Check current quota status
    api_working = check_api_quota_status()
    
    # Provide billing guidance
    check_billing_status()
    
    # Suggest solutions
    suggest_quota_solutions()
    
    # Create quota-aware updater
    create_quota_aware_hours_updater()
    
    # Final recommendations
    print(f"\n🎯 RECOMMENDATIONS")
    print("=" * 20)
    
    if not api_working:
        print("1. **Enable Google Cloud Billing** (Immediate)")
        print("   - This will increase your quota to 100,000+ requests/day")
        print("   - Very low cost (~$0.017 per 1000 requests)")
        
        print(f"\n2. **Use the Quota-Aware Updater** (Immediate)")
        print("   - Run: python scripts/maintenance/quota_aware_hours_updater.py")
        print("   - It will stop gracefully when quota is reached")
        
        print(f"\n3. **Implement Caching** (Long-term)")
        print("   - Store hours data to avoid repeated API calls")
        print("   - Update only when data is stale")
    
    print(f"\n📊 Current Status:")
    print(f"   • API Key: Working (but quota limited)")
    print(f"   • Quota: 25,000 requests/day (free tier)")
    print(f"   • Solution: Enable billing for higher limits")

if __name__ == "__main__":
    main() 