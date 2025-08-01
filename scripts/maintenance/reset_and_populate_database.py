#!/usr/bin/env python3
"""
Database Reset and Population Script
===================================

This script empties the restaurants database and populates it with 50 sample restaurants
that match the current schema. The sample data includes a variety of kosher restaurants
with different categories, locations, and kosher supervision levels.

Features:
- Empties existing restaurant data
- Populates with 50 diverse sample restaurants
- Matches current database schema exactly
- Includes realistic kosher supervision data
- Provides geographic diversity
- Includes proper error handling and logging

Author: JewGo Development Team
Version: 1.0
"""

import os
import sys
import logging
from datetime import datetime, time
import random
from typing import List, Dict, Any

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from database.database_manager_v3 import EnhancedDatabaseManager, Restaurant
from config.config import get_config
from sqlalchemy import text

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database_reset.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DatabasePopulator:
    """Handles database reset and population with sample data."""
    
    def __init__(self):
        """Initialize the database populator."""
        self.config = get_config()
        self.db_manager = EnhancedDatabaseManager(self.config.DATABASE_URL)
        self.sample_restaurants = []
        
    def connect(self) -> bool:
        """Connect to the database."""
        try:
            success = self.db_manager.connect()
            if success:
                logger.info("Successfully connected to database")
                return True
            else:
                logger.error("Failed to connect to database")
                return False
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            return False
    
    def empty_database(self) -> bool:
        """Empty all restaurants from the database."""
        try:
            session = self.db_manager.get_session()
            
            # Delete all restaurants
            deleted_count = session.query(Restaurant).delete()
            session.commit()
            session.close()
            
            logger.info(f"Successfully deleted {deleted_count} restaurants from database")
            return True
            
        except Exception as e:
            logger.error(f"Error emptying database: {e}")
            if 'session' in locals():
                session.rollback()
                session.close()
            return False
    
    def generate_sample_restaurants(self) -> List[Dict[str, Any]]:
        """Generate 50 sample restaurants with realistic data."""
        
        # Sample data arrays
        cities = [
            ("Miami", "FL", 25.7617, -80.1918),
            ("New York", "NY", 40.7128, -74.0060),
            ("Los Angeles", "CA", 34.0522, -118.2437),
            ("Chicago", "IL", 41.8781, -87.6298),
            ("Houston", "TX", 29.7604, -95.3698),
            ("Phoenix", "AZ", 33.4484, -112.0740),
            ("Philadelphia", "PA", 39.9526, -75.1652),
            ("San Antonio", "TX", 29.4241, -98.4936),
            ("San Diego", "CA", 32.7157, -117.1611),
            ("Dallas", "TX", 32.7767, -96.7970)
        ]
        
        kosher_categories = ['meat', 'dairy', 'pareve', 'fish']
        kosher_weights = [0.3, 0.5, 0.15, 0.05]  # 30% meat, 50% dairy, 15% pareve, 5% fish
        
        certifying_agencies = ['ORB', 'OU', 'Kof-K', 'Star-K', 'CRC']
        
        restaurant_types = [
            'Restaurant', 'Cafe', 'Deli', 'Pizzeria', 'Bakery', 
            'Ice Cream Shop', 'Catering', 'Food Truck', 'Kosher Market'
        ]
        
        price_ranges = ['$', '$$', '$$$', '$$$$']
        price_weights = [0.2, 0.5, 0.25, 0.05]  # More mid-range restaurants
        
        # Generate 50 restaurants
        restaurants = []
        
        for i in range(50):
            # Select random city
            city, state, lat, lng = random.choice(cities)
            
            # Add some geographic variation
            lat += random.uniform(-0.1, 0.1)
            lng += random.uniform(-0.1, 0.1)
            
            # Select kosher category with weights
            kosher_category = random.choices(kosher_categories, weights=kosher_weights)[0]
            
            # Determine kosher supervision based on category
            is_cholov_yisroel = kosher_category == 'dairy' and random.random() > 0.3
            is_pas_yisroel = kosher_category in ['meat', 'pareve'] and random.random() > 0.4
            
            # Generate restaurant name
            restaurant_type = random.choice(restaurant_types)
            name_suffixes = ['Kosher', 'Jewish', 'Hebrew', 'Shalom', 'Mazel', 'Kosher Delight']
            name = f"{random.choice(['Miami', 'New York', 'Los Angeles', 'Chicago', 'Houston'])} {restaurant_type}"
            if random.random() > 0.5:
                name += f" {random.choice(name_suffixes)}"
            
            # Generate address
            street_numbers = [str(random.randint(100, 9999))]
            street_names = ['Main St', 'Oak Ave', 'Pine Rd', 'Maple Dr', 'Cedar Ln', 'Elm St', 'Washington Ave']
            address = f"{random.choice(street_numbers)} {random.choice(street_names)}"
            
            # Generate phone number
            area_codes = ['305', '212', '310', '312', '713', '602', '215', '210', '619', '214']
            phone = f"({random.choice(area_codes)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
            
            # Generate website
            website = f"https://www.{name.lower().replace(' ', '').replace('-', '')}.com"
            
            # Generate hours
            hours = self._generate_hours()
            
            # Generate pricing
            price_range = random.choices(price_ranges, weights=price_weights)[0]
            min_cost = random.randint(8, 25) if price_range == '$' else random.randint(15, 35) if price_range == '$$' else random.randint(25, 60) if price_range == '$$$' else random.randint(50, 100)
            max_cost = min_cost + random.randint(5, 15)
            
            # Generate ratings
            rating = round(random.uniform(3.5, 5.0), 1)
            review_count = random.randint(10, 500)
            
            restaurant_data = {
                'name': name,
                'address': address,
                'city': city,
                'state': state,
                'zip_code': str(random.randint(10000, 99999)),
                'phone_number': phone,
                'website': website,
                'certifying_agency': random.choice(certifying_agencies),
                'kosher_category': kosher_category,
                'is_cholov_yisroel': is_cholov_yisroel,
                'is_pas_yisroel': is_pas_yisroel,
                'listing_type': restaurant_type.lower(),
                'hours_of_operation': hours,
                'short_description': f"Authentic kosher {restaurant_type.lower()} serving delicious {kosher_category} cuisine.",
                'price_range': price_range,
                'latitude': lat,
                'longitude': lng,
                'hours_json': None,
                'specials': None,
                'image_url': None,
                'google_listing_url': None,
                'timezone': None,
                'hours_last_updated': None,
                'current_time_local': None
            }
            
            restaurants.append(restaurant_data)
        
        return restaurants
    
    def _generate_hours(self) -> str:
        """Generate realistic business hours."""
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        hours = []
        
        for day in days:
            if day == 'Friday':
                # Friday hours (typically shorter for Shabbat)
                open_time = time(random.randint(6, 10), random.choice([0, 30]))
                close_time = time(random.randint(14, 16), random.choice([0, 30]))
            elif day == 'Saturday':
                # Saturday closed for Shabbat
                hours.append(f"{day}: Closed")
                continue
            elif day == 'Sunday':
                # Sunday hours (often later start)
                open_time = time(random.randint(8, 12), random.choice([0, 30]))
                close_time = time(random.randint(20, 22), random.choice([0, 30]))
            else:
                # Weekday hours
                open_time = time(random.randint(6, 9), random.choice([0, 30]))
                close_time = time(random.randint(20, 23), random.choice([0, 30]))
            
            hours.append(f"{day}: {open_time.strftime('%I:%M %p')} - {close_time.strftime('%I:%M %p')}")
        
        return '\n'.join(hours)
    
    def populate_database(self, restaurants: List[Dict[str, Any]]) -> bool:
        """Populate the database with sample restaurants using raw SQL."""
        try:
            session = self.db_manager.get_session()
            added_count = 0
            
            for restaurant_data in restaurants:
                try:
                    # Use raw SQL to avoid JSONB type issues
                    sql = """
                    INSERT INTO restaurants (
                        name, address, city, state, zip_code, phone_number, website,
                        certifying_agency, kosher_category, is_cholov_yisroel, is_pas_yisroel,
                        listing_type, hours_of_operation, short_description, price_range,
                        latitude, longitude, hours_json, specials, image_url, google_listing_url,
                        timezone, hours_last_updated, current_time_local, hours_parsed
                    ) VALUES (
                        :name, :address, :city, :state, :zip_code, :phone_number, :website,
                        :certifying_agency, :kosher_category, :is_cholov_yisroel, :is_pas_yisroel,
                        :listing_type, :hours_of_operation, :short_description, :price_range,
                        :latitude, :longitude, :hours_json, :specials, :image_url, :google_listing_url,
                        :timezone, :hours_last_updated, :current_time_local, :hours_parsed
                    )
                    """
                    
                    # Prepare data for SQL insertion
                    sql_data = {
                        'name': restaurant_data['name'],
                        'address': restaurant_data['address'],
                        'city': restaurant_data['city'],
                        'state': restaurant_data['state'],
                        'zip_code': restaurant_data['zip_code'],
                        'phone_number': restaurant_data['phone_number'],
                        'website': restaurant_data['website'],
                        'certifying_agency': restaurant_data['certifying_agency'],
                        'kosher_category': restaurant_data['kosher_category'],
                        'is_cholov_yisroel': restaurant_data['is_cholov_yisroel'],
                        'is_pas_yisroel': restaurant_data['is_pas_yisroel'],
                        'listing_type': restaurant_data['listing_type'],
                        'hours_of_operation': restaurant_data['hours_of_operation'],
                        'short_description': restaurant_data['short_description'],
                        'price_range': restaurant_data['price_range'],
                        'latitude': restaurant_data['latitude'],
                        'longitude': restaurant_data['longitude'],
                        'hours_json': None,  # JSONB field - set to NULL
                        'specials': None,    # JSONB field - set to NULL
                        'image_url': None,
                        'google_listing_url': None,
                        'timezone': None,
                        'hours_last_updated': None,
                        'current_time_local': None,
                        'hours_parsed': False
                    }
                    
                    session.execute(text(sql), sql_data)
                    added_count += 1
                    
                    if added_count % 10 == 0:
                        logger.info(f"Added {added_count} restaurants...")
                        
                except Exception as e:
                    logger.error(f"Error adding restaurant {restaurant_data.get('name', 'Unknown')}: {e}")
                    continue
            
            session.commit()
            session.close()
            
            logger.info(f"Successfully added {added_count} restaurants to database")
            return True
            
        except Exception as e:
            logger.error(f"Error populating database: {e}")
            if 'session' in locals():
                session.rollback()
                session.close()
            return False
    
    def verify_population(self) -> Dict[str, Any]:
        """Verify the database population and return statistics."""
        try:
            session = self.db_manager.get_session()
            
            # Get total count
            total_count = session.query(Restaurant).count()
            
            # Get counts by kosher category
            categories = session.query(Restaurant.kosher_category).all()
            category_counts = {}
            for category in categories:
                cat = category[0]
                category_counts[cat] = category_counts.get(cat, 0) + 1
            
            # Get counts by state
            states = session.query(Restaurant.state).all()
            state_counts = {}
            for state in states:
                st = state[0]
                state_counts[st] = state_counts.get(st, 0) + 1
            
            session.close()
            
            stats = {
                'total_restaurants': total_count,
                'by_category': category_counts,
                'by_state': state_counts,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Database verification complete: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error verifying database population: {e}")
            return {}
    
    def run(self) -> bool:
        """Run the complete database reset and population process."""
        logger.info("Starting database reset and population process...")
        
        # Step 1: Connect to database
        if not self.connect():
            logger.error("Failed to connect to database. Exiting.")
            return False
        
        # Step 2: Empty database
        logger.info("Emptying existing restaurant data...")
        if not self.empty_database():
            logger.error("Failed to empty database. Exiting.")
            return False
        
        # Step 3: Generate sample data
        logger.info("Generating sample restaurant data...")
        self.sample_restaurants = self.generate_sample_restaurants()
        logger.info(f"Generated {len(self.sample_restaurants)} sample restaurants")
        
        # Step 4: Populate database
        logger.info("Populating database with sample data...")
        if not self.populate_database(self.sample_restaurants):
            logger.error("Failed to populate database. Exiting.")
            return False
        
        # Step 5: Verify population
        logger.info("Verifying database population...")
        stats = self.verify_population()
        
        if stats:
            logger.info("Database reset and population completed successfully!")
            logger.info(f"Final statistics: {stats}")
            return True
        else:
            logger.error("Database verification failed.")
            return False
    
    def cleanup(self):
        """Clean up database connection."""
        try:
            self.db_manager.disconnect()
            logger.info("Database connection closed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

def main():
    """Main function to run the database reset and population."""
    logger.info("=" * 60)
    logger.info("DATABASE RESET AND POPULATION SCRIPT")
    logger.info("=" * 60)
    
    # Create populator instance
    populator = DatabasePopulator()
    
    try:
        # Run the process
        success = populator.run()
        
        if success:
            logger.info("✅ Database reset and population completed successfully!")
            return 0
        else:
            logger.error("❌ Database reset and population failed!")
            return 1
            
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1
    finally:
        populator.cleanup()

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 