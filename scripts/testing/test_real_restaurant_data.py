#!/usr/bin/env python3
"""
Test Google Places API with Real Restaurant Data
===============================================

This script tests the Google Places API integration using real restaurant data
from the JewGo database. It will:

1. Connect to the database and fetch real restaurants
2. Test Google Places API for each restaurant
3. Compare existing data with Google Places data
4. Generate a comprehensive test report
5. Test hours fetching and formatting
6. Test website fetching
7. Test place search accuracy

Author: JewGo Development Team
Version: 1.0
"""

import os
import sys
import requests
import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
import structlog

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from database.database_manager_v3 import EnhancedDatabaseManager
from utils.google_places_helper import (
    search_google_places_website, 
    search_google_places_hours,
    format_hours_from_places_api
)

# Configure structured logging
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

class GooglePlacesTester:
    """Comprehensive Google Places API tester for real restaurant data."""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_PLACES_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_PLACES_API_KEY environment variable not set")
        
        self.db_manager = None
        self.test_results = []
        self.stats = {
            'total_tested': 0,
            'successful_searches': 0,
            'successful_hours': 0,
            'successful_websites': 0,
            'failed_searches': 0,
            'api_errors': 0,
            'rate_limit_hits': 0
        }
    
    def connect_database(self):
        """Connect to the database."""
        try:
            database_url = os.getenv('DATABASE_URL')
            if not database_url:
                raise ValueError("DATABASE_URL environment variable not set")
            
            self.db_manager = EnhancedDatabaseManager(database_url)
            if not self.db_manager.connect():
                raise Exception("Failed to connect to database")
            
            logger.info("Successfully connected to database")
            return True
            
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False
    
    def get_test_restaurants(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get a sample of restaurants from the database for testing."""
        try:
            restaurants = self.db_manager.get_restaurants(limit=limit, offset=0)
            return [self.db_manager._restaurant_to_unified_dict(r) for r in restaurants]
        except Exception as e:
            logger.error(f"Failed to get restaurants: {e}")
            return []
    
    def test_place_search(self, restaurant: Dict[str, Any]) -> Dict[str, Any]:
        """Test Google Places search for a restaurant."""
        result = {
            'restaurant_id': restaurant.get('id'),
            'restaurant_name': restaurant.get('name'),
            'restaurant_address': restaurant.get('address'),
            'search_success': False,
            'place_id': None,
            'google_name': None,
            'google_address': None,
            'confidence_score': 0,
            'error': None
        }
        
        try:
            # Build search query
            query = f"{restaurant['name']} {restaurant['address']}"
            
            # Search for the place
            search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            search_params = {
                'query': query,
                'key': self.api_key,
                'type': 'restaurant'
            }
            
            response = requests.get(search_url, params=search_params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                place = data['results'][0]
                result.update({
                    'search_success': True,
                    'place_id': place['place_id'],
                    'google_name': place.get('name'),
                    'google_address': place.get('formatted_address'),
                    'confidence_score': self._calculate_confidence_score(restaurant, place)
                })
                self.stats['successful_searches'] += 1
            else:
                result['error'] = f"Search failed: {data.get('status')} - {data.get('error_message', 'Unknown error')}"
                self.stats['failed_searches'] += 1
                
        except requests.exceptions.RequestException as e:
            result['error'] = f"Request error: {e}"
            self.stats['api_errors'] += 1
        except Exception as e:
            result['error'] = f"Unexpected error: {e}"
            self.stats['api_errors'] += 1
        
        return result
    
    def test_hours_fetching(self, place_id: str, restaurant_name: str) -> Dict[str, Any]:
        """Test fetching hours from Google Places API."""
        result = {
            'hours_success': False,
            'hours_formatted': None,
            'hours_raw': None,
            'error': None
        }
        
        try:
            # Get place details for hours
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                'place_id': place_id,
                'fields': 'opening_hours',
                'key': self.api_key
            }
            
            response = requests.get(details_url, params=details_params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'OK' and 'result' in data:
                opening_hours = data['result'].get('opening_hours')
                if opening_hours and 'weekday_text' in opening_hours:
                    hours_formatted = format_hours_from_places_api(opening_hours)
                    result.update({
                        'hours_success': True,
                        'hours_formatted': hours_formatted,
                        'hours_raw': opening_hours
                    })
                    self.stats['successful_hours'] += 1
                else:
                    result['error'] = "No hours data available"
            else:
                result['error'] = f"Hours fetch failed: {data.get('status')} - {data.get('error_message', 'Unknown error')}"
                
        except requests.exceptions.RequestException as e:
            result['error'] = f"Request error: {e}"
            self.stats['api_errors'] += 1
        except Exception as e:
            result['error'] = f"Unexpected error: {e}"
            self.stats['api_errors'] += 1
        
        return result
    
    def test_website_fetching(self, place_id: str, restaurant_name: str) -> Dict[str, Any]:
        """Test fetching website from Google Places API."""
        result = {
            'website_success': False,
            'website_url': None,
            'error': None
        }
        
        try:
            # Get place details for website
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                'place_id': place_id,
                'fields': 'website',
                'key': self.api_key
            }
            
            response = requests.get(details_url, params=details_params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'OK' and 'result' in data:
                website = data['result'].get('website')
                if website:
                    result.update({
                        'website_success': True,
                        'website_url': website
                    })
                    self.stats['successful_websites'] += 1
                else:
                    result['error'] = "No website available"
            else:
                result['error'] = f"Website fetch failed: {data.get('status')} - {data.get('error_message', 'Unknown error')}"
                
        except requests.exceptions.RequestException as e:
            result['error'] = f"Request error: {e}"
            self.stats['api_errors'] += 1
        except Exception as e:
            result['error'] = f"Unexpected error: {e}"
            self.stats['api_errors'] += 1
        
        return result
    
    def _calculate_confidence_score(self, restaurant: Dict[str, Any], place: Dict[str, Any]) -> float:
        """Calculate confidence score for place match."""
        score = 0.0
        
        # Name similarity (case-insensitive)
        restaurant_name = restaurant['name'].lower()
        google_name = place.get('name', '').lower()
        
        if restaurant_name in google_name or google_name in restaurant_name:
            score += 0.4
        elif any(word in google_name for word in restaurant_name.split()):
            score += 0.2
        
        # Address similarity
        restaurant_address = restaurant['address'].lower()
        google_address = place.get('formatted_address', '').lower()
        
        if restaurant_address in google_address or google_address in restaurant_address:
            score += 0.4
        elif any(word in google_address for word in restaurant_address.split()):
            score += 0.2
        
        # Phone number match (if available)
        if restaurant.get('phone_number') and place.get('formatted_phone_number'):
            if restaurant['phone_number'].replace('-', '').replace(' ', '') == \
               place['formatted_phone_number'].replace('-', '').replace(' ', ''):
                score += 0.2
        
        return min(score, 1.0)
    
    def run_comprehensive_test(self, limit: int = 10):
        """Run comprehensive test on real restaurant data."""
        print("🔍 Google Places API Real Restaurant Data Test")
        print("=" * 60)
        
        # Connect to database
        if not self.connect_database():
            print("❌ Failed to connect to database")
            return
        
        # Get test restaurants
        restaurants = self.get_test_restaurants(limit)
        if not restaurants:
            print("❌ No restaurants found in database")
            return
        
        print(f"📊 Testing {len(restaurants)} restaurants from database")
        print()
        
        # Test each restaurant
        for i, restaurant in enumerate(restaurants, 1):
            print(f"🏪 Testing Restaurant {i}/{len(restaurants)}: {restaurant['name']}")
            print(f"   Address: {restaurant['address']}")
            
            # Test place search
            search_result = self.test_place_search(restaurant)
            
            if search_result['search_success']:
                print(f"   ✅ Found on Google Places (Confidence: {search_result['confidence_score']:.2f})")
                print(f"   📍 Google Name: {search_result['google_name']}")
                print(f"   🏠 Google Address: {search_result['google_address']}")
                
                # Test hours fetching
                hours_result = self.test_hours_fetching(search_result['place_id'], restaurant['name'])
                if hours_result['hours_success']:
                    print(f"   🕒 Hours: {hours_result['hours_formatted']}")
                else:
                    print(f"   ❌ Hours: {hours_result['error']}")
                
                # Test website fetching
                website_result = self.test_website_fetching(search_result['place_id'], restaurant['name'])
                if website_result['website_success']:
                    print(f"   🌐 Website: {website_result['website_url']}")
                else:
                    print(f"   ❌ Website: {website_result['error']}")
                
            else:
                print(f"   ❌ Not found on Google Places: {search_result['error']}")
            
            self.stats['total_tested'] += 1
            self.test_results.append({
                'restaurant': restaurant,
                'search_result': search_result,
                'hours_result': hours_result if search_result['search_success'] else None,
                'website_result': website_result if search_result['search_success'] else None
            })
            
            print()
            
            # Rate limiting - wait between requests
            if i < len(restaurants):
                time.sleep(1)
        
        # Generate report
        self._generate_report()
    
    def _generate_report(self):
        """Generate comprehensive test report."""
        print("📋 TEST REPORT")
        print("=" * 60)
        
        # Statistics
        print(f"📊 Total Restaurants Tested: {self.stats['total_tested']}")
        print(f"✅ Successful Searches: {self.stats['successful_searches']}")
        print(f"❌ Failed Searches: {self.stats['failed_searches']}")
        print(f"🕒 Successful Hours Fetches: {self.stats['successful_hours']}")
        print(f"🌐 Successful Website Fetches: {self.stats['successful_websites']}")
        print(f"🚫 API Errors: {self.stats['api_errors']}")
        
        # Success rates
        if self.stats['total_tested'] > 0:
            search_rate = (self.stats['successful_searches'] / self.stats['total_tested']) * 100
            hours_rate = (self.stats['successful_hours'] / self.stats['successful_searches']) * 100 if self.stats['successful_searches'] > 0 else 0
            website_rate = (self.stats['successful_websites'] / self.stats['successful_searches']) * 100 if self.stats['successful_searches'] > 0 else 0
            
            print(f"\n📈 Success Rates:")
            print(f"   Search Success Rate: {search_rate:.1f}%")
            print(f"   Hours Fetch Rate: {hours_rate:.1f}%")
            print(f"   Website Fetch Rate: {website_rate:.1f}%")
        
        # Detailed results
        print(f"\n📝 DETAILED RESULTS:")
        print("-" * 60)
        
        for result in self.test_results:
            restaurant = result['restaurant']
            search = result['search_result']
            
            print(f"\n🏪 {restaurant['name']}")
            print(f"   ID: {restaurant['id']}")
            print(f"   Address: {restaurant['address']}")
            
            if search['search_success']:
                print(f"   ✅ Found (Confidence: {search['confidence_score']:.2f})")
                print(f"   📍 Google: {search['google_name']}")
                
                if result['hours_result'] and result['hours_result']['hours_success']:
                    print(f"   🕒 Hours: {result['hours_result']['hours_formatted']}")
                
                if result['website_result'] and result['website_result']['website_success']:
                    print(f"   🌐 Website: {result['website_result']['website_url']}")
            else:
                print(f"   ❌ Not found: {search['error']}")
        
        # Save detailed results to file
        self._save_detailed_results()
    
    def _save_detailed_results(self):
        """Save detailed test results to JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"google_places_test_results_{timestamp}.json"
        
        results_data = {
            'test_timestamp': datetime.now().isoformat(),
            'statistics': self.stats,
            'results': self.test_results
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(results_data, f, indent=2, default=str)
            print(f"\n💾 Detailed results saved to: {filename}")
        except Exception as e:
            print(f"\n❌ Failed to save results: {e}")

def main():
    """Main function."""
    try:
        # Check environment variables
        if not os.getenv('GOOGLE_PLACES_API_KEY'):
            print("❌ GOOGLE_PLACES_API_KEY environment variable not set")
            print("\nTo set your API key:")
            print("export GOOGLE_PLACES_API_KEY='your_api_key_here'")
            return
        
        if not os.getenv('DATABASE_URL'):
            print("❌ DATABASE_URL environment variable not set")
            print("\nTo set your database URL:")
            print("export DATABASE_URL='your_database_url_here'")
            return
        
        # Create tester and run test
        tester = GooglePlacesTester()
        
        # Get number of restaurants to test (default 10)
        limit = int(os.getenv('TEST_LIMIT', '10'))
        tester.run_comprehensive_test(limit=limit)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        logger.error(f"Test failed", error=str(e))

if __name__ == "__main__":
    main() 