#!/usr/bin/env python3
"""
Conservative Import Strategy - Minimal data changes, maximum safety
"""

import json
import requests
import time
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ConservativeImporter:
    def __init__(self):
        self.base_url = "https://jewgo.onrender.com"
        self.session = requests.Session()
        self.session.timeout = 30
        
        # Conservative settings
        self.batch_size = 3  # Small batches
        self.delay_between_requests = 5  # 5 seconds between requests
        self.delay_between_batches = 15  # 15 seconds between batches
        self.max_retries = 3
        
        # Track progress
        self.successful_imports = 0
        self.failed_imports = 0
        self.skipped_imports = 0
        
    def check_backend_health(self):
        """Check if backend is healthy before starting"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                logger.info("✅ Backend is healthy")
                return True
            else:
                logger.error(f"❌ Backend health check failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Backend health check error: {e}")
            return False
    
    def get_existing_restaurants(self):
        """Get list of existing restaurants safely"""
        try:
            response = self.session.get(f"{self.base_url}/api/restaurants?limit=1000")
            if response.status_code == 200:
                data = response.json()
                existing = data.get('data', [])
                existing_ids = {restaurant.get('business_id') for restaurant in existing}
                logger.info(f"📊 Found {len(existing)} existing restaurants")
                return existing_ids
            else:
                logger.warning(f"⚠️ Could not check existing restaurants: {response.status_code}")
                return set()
        except Exception as e:
            logger.error(f"❌ Error checking existing restaurants: {e}")
            return set()
    
    def validate_restaurant_data(self, restaurant):
        """Validate restaurant data before import"""
        required_fields = ['business_id', 'name']
        for field in required_fields:
            if not restaurant.get(field):
                logger.warning(f"⚠️ Missing required field: {field}")
                return False
        
        # Validate certifying_agency
        valid_agencies = ['ORB', 'OU', 'KOF-K', 'Star-K', 'CRC', 'Vaad HaRabbonim']
        if restaurant.get('certifying_agency') not in valid_agencies:
            restaurant['certifying_agency'] = 'ORB'
            logger.info(f"🔧 Fixed certifying_agency to ORB for {restaurant['name']}")
        
        # Validate kosher_category
        valid_categories = ['meat', 'dairy', 'pareve', 'fish', 'unknown']
        if restaurant.get('kosher_category') not in valid_categories:
            restaurant['kosher_category'] = 'unknown'
            logger.info(f"🔧 Fixed kosher_category to unknown for {restaurant['name']}")
        
        # Ensure text fields are strings
        text_fields = ['name', 'website_link', 'phone_number', 'address', 'city', 'state', 'zip_code']
        for field in text_fields:
            if restaurant.get(field) is not None:
                restaurant[field] = str(restaurant[field])
            else:
                restaurant[field] = ""
        
        # Handle numeric fields safely
        numeric_fields = ['rating', 'latitude', 'longitude']
        for field in numeric_fields:
            value = restaurant.get(field)
            if value is not None:
                try:
                    restaurant[field] = float(value)
                except (ValueError, TypeError):
                    restaurant[field] = None
        
        return True
    
    def import_single_restaurant(self, restaurant, retry_count=0):
        """Import a single restaurant with retry logic"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/admin/restaurants",
                json=restaurant,
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info(f"✅ Successfully imported: {restaurant['name']}")
                self.successful_imports += 1
                return True
            elif response.status_code == 409:
                logger.info(f"⏭️ Already exists: {restaurant['name']}")
                self.skipped_imports += 1
                return True
            elif response.status_code == 429:
                logger.warning(f"⏳ Rate limited: {restaurant['name']}")
                if retry_count < self.max_retries:
                    time.sleep(30)  # Wait 30 seconds for rate limit
                    return self.import_single_restaurant(restaurant, retry_count + 1)
                else:
                    logger.error(f"❌ Max retries exceeded for: {restaurant['name']}")
                    self.failed_imports += 1
                    return False
            else:
                logger.error(f"❌ Failed ({response.status_code}): {restaurant['name']}")
                try:
                    error_data = response.json()
                    logger.error(f"   Error details: {error_data}")
                except:
                    logger.error(f"   Raw response: {response.text[:200]}")
                
                self.failed_imports += 1
                return False
                
        except Exception as e:
            logger.error(f"❌ Exception importing {restaurant['name']}: {e}")
            self.failed_imports += 1
            return False
    
    def load_restaurant_data(self):
        """Load restaurant data from file"""
        try:
            with open('local_restaurants.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            restaurants = data.get('restaurants', [])
            logger.info(f"📂 Loaded {len(restaurants)} restaurants from local_restaurants.json")
            return restaurants
        except Exception as e:
            logger.error(f"❌ Error loading restaurant data: {e}")
            return []
    
    def prepare_restaurant_data(self, restaurants, existing_ids):
        """Prepare restaurant data for import"""
        prepared_restaurants = []
        
        for restaurant in restaurants:
            business_id = restaurant.get('business_id', '')
            
            # Skip if already exists
            if business_id in existing_ids:
                continue
            
            # Create formatted restaurant with minimal changes
            formatted_restaurant = {
                'business_id': business_id or f"auto_{len(prepared_restaurants) + 1}",
                'name': restaurant.get('name', '') or f"Restaurant {business_id}",
                'website_link': restaurant.get('website_link') or restaurant.get('website', ''),
                'phone_number': restaurant.get('phone_number', ''),
                'address': restaurant.get('address', ''),
                'city': restaurant.get('city', '') or 'Unknown',
                'state': restaurant.get('state', '') or 'FL',
                'zip_code': restaurant.get('zip_code', ''),
                'certificate_link': restaurant.get('certificate_link', ''),
                'image_url': restaurant.get('image_url', ''),
                'certifying_agency': restaurant.get('certifying_agency', 'ORB'),
                'kosher_category': restaurant.get('kosher_category', 'unknown'),
                'listing_type': restaurant.get('listing_type', 'restaurant'),
                'status': restaurant.get('status', 'active'),
                'rating': restaurant.get('rating') or restaurant.get('google_rating'),
                'price_range': restaurant.get('price_range', ''),
                'hours_of_operation': restaurant.get('hours_of_operation', ''),
                'short_description': restaurant.get('short_description', ''),
                'notes': restaurant.get('notes', ''),
                'latitude': restaurant.get('latitude'),
                'longitude': restaurant.get('longitude'),
                'data_source': restaurant.get('data_source', 'manual'),
                'external_id': restaurant.get('external_id', '')
            }
            
            # Validate and fix data
            if self.validate_restaurant_data(formatted_restaurant):
                prepared_restaurants.append(formatted_restaurant)
        
        logger.info(f"✅ Prepared {len(prepared_restaurants)} restaurants for import")
        return prepared_restaurants
    
    def import_restaurants_conservatively(self, restaurants):
        """Import restaurants using conservative approach"""
        logger.info(f"🚀 Starting conservative import of {len(restaurants)} restaurants")
        
        total_restaurants = len(restaurants)
        
        for i in range(0, total_restaurants, self.batch_size):
            batch = restaurants[i:i + self.batch_size]
            batch_num = (i // self.batch_size) + 1
            total_batches = (total_restaurants + self.batch_size - 1) // self.batch_size
            
            logger.info(f"\n📦 Processing batch {batch_num}/{total_batches} ({len(batch)} restaurants)")
            
            batch_success = 0
            batch_failures = 0
            
            for j, restaurant in enumerate(batch):
                restaurant_num = i + j + 1
                logger.info(f"Processing [{restaurant_num}/{total_restaurants}]: {restaurant['name']}")
                
                if self.import_single_restaurant(restaurant):
                    batch_success += 1
                else:
                    batch_failures += 1
                
                # Delay between requests
                if j < len(batch) - 1:  # Don't delay after last request in batch
                    time.sleep(self.delay_between_requests)
            
            logger.info(f"📊 Batch {batch_num} summary: {batch_success} success, {batch_failures} failures")
            
            # Delay between batches
            if batch_num < total_batches:
                logger.info(f"⏳ Waiting {self.delay_between_batches} seconds before next batch...")
                time.sleep(self.delay_between_batches)
    
    def run_import(self):
        """Run the complete conservative import process"""
        logger.info("🚀 Conservative Restaurant Import Strategy")
        logger.info("=" * 60)
        
        # 1. Check backend health
        if not self.check_backend_health():
            logger.error("❌ Backend is not healthy. Aborting import.")
            return False
        
        # 2. Get existing restaurants
        existing_ids = self.get_existing_restaurants()
        
        # 3. Load restaurant data
        restaurants = self.load_restaurant_data()
        if not restaurants:
            logger.error("❌ No restaurant data loaded. Aborting import.")
            return False
        
        # 4. Prepare restaurant data
        prepared_restaurants = self.prepare_restaurant_data(restaurants, existing_ids)
        if not prepared_restaurants:
            logger.info("✅ No new restaurants to import. All done!")
            return True
        
        # 5. Import restaurants
        self.import_restaurants_conservatively(prepared_restaurants)
        
        # 6. Print summary
        logger.info("\n📊 Import Summary")
        logger.info("=" * 30)
        logger.info(f"✅ Successfully imported: {self.successful_imports}")
        logger.info(f"⏭️ Skipped (already exists): {self.skipped_imports}")
        logger.info(f"❌ Failed to import: {self.failed_imports}")
        logger.info(f"📋 Total processed: {self.successful_imports + self.skipped_imports + self.failed_imports}")
        
        return True

def main():
    """Main function"""
    importer = ConservativeImporter()
    success = importer.run_import()
    
    if success:
        logger.info("🎉 Conservative import process completed!")
    else:
        logger.error("❌ Conservative import process failed!")

if __name__ == "__main__":
    main() 