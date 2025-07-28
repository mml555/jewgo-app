#!/usr/bin/env python3
"""
Menu Pricing Updater
Updates restaurants with detailed menu section pricing information.
"""

import sqlite3
import json
import logging
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MenuPricingUpdater:
    def __init__(self, db_path: str = "restaurants.db"):
        self.db_path = db_path
        
    def connect_db(self):
        """Connect to the database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False
    
    def get_restaurants_without_pricing(self) -> List[tuple]:
        """Get restaurants that don't have menu pricing data."""
        try:
            self.cursor.execute("""
                SELECT id, name, listing_type, kosher_category 
                FROM restaurants 
                WHERE (menu_pricing IS NULL OR menu_pricing = '') 
                AND status = 'active'
                ORDER BY name
            """)
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Error getting restaurants without pricing: {e}")
            return []
    
    def generate_sample_pricing(self, restaurant_name: str, listing_type: str, kosher_category: str) -> Dict[str, Any]:
        """Generate sample pricing data based on restaurant type."""
        
        # Base pricing templates for different restaurant types
        pricing_templates = {
            'restaurant': {
                'A LA BRUNCH': {'min': 15.95, 'max': 18.95, 'avg': 17.45},
                'A LA WRAP': {'min': 17.95, 'max': 21.95, 'avg': 19.95},
                'A LA BOWL': {'min': 21.95, 'max': 25.95, 'avg': 23.15},
                'A LA SALAD': {'min': 19.95, 'max': 21.95, 'avg': 21.45},
                'Build Your Own': {'min': 15.95, 'max': 25.95, 'avg': 19.20},
                'Kids Menu': {'min': 5.95, 'max': 15.95, 'avg': 9.95}
            },
            'pizza': {
                'Small Pizza': {'min': 12.95, 'max': 16.95, 'avg': 14.95},
                'Medium Pizza': {'min': 16.95, 'max': 20.95, 'avg': 18.95},
                'Large Pizza': {'min': 20.95, 'max': 24.95, 'avg': 22.95},
                'Extra Large Pizza': {'min': 24.95, 'max': 28.95, 'avg': 26.95},
                'Pizza Slices': {'min': 3.95, 'max': 5.95, 'avg': 4.95},
                'Sides': {'min': 4.95, 'max': 8.95, 'avg': 6.95}
            },
            'sushi': {
                'Maki Rolls': {'min': 8.95, 'max': 14.95, 'avg': 11.95},
                'Nigiri': {'min': 3.95, 'max': 6.95, 'avg': 5.45},
                'Sashimi': {'min': 12.95, 'max': 18.95, 'avg': 15.95},
                'Specialty Rolls': {'min': 14.95, 'max': 22.95, 'avg': 18.95},
                'Appetizers': {'min': 6.95, 'max': 12.95, 'avg': 9.95},
                'Soups & Salads': {'min': 4.95, 'max': 8.95, 'avg': 6.95}
            },
            'bakery': {
                'Breads': {'min': 4.95, 'max': 8.95, 'avg': 6.95},
                'Pastries': {'min': 3.95, 'max': 6.95, 'avg': 5.45},
                'Cakes': {'min': 18.95, 'max': 35.95, 'avg': 27.45},
                'Cookies': {'min': 2.95, 'max': 4.95, 'avg': 3.95},
                'Specialty Items': {'min': 8.95, 'max': 15.95, 'avg': 12.45}
            },
            'cafe': {
                'Coffee & Drinks': {'min': 3.95, 'max': 6.95, 'avg': 5.45},
                'Breakfast Items': {'min': 8.95, 'max': 14.95, 'avg': 11.95},
                'Sandwiches': {'min': 9.95, 'max': 15.95, 'avg': 12.95},
                'Salads': {'min': 10.95, 'max': 16.95, 'avg': 13.95},
                'Desserts': {'min': 5.95, 'max': 9.95, 'avg': 7.95}
            },
            'deli': {
                'Sandwiches': {'min': 8.95, 'max': 14.95, 'avg': 11.95},
                'Wraps': {'min': 9.95, 'max': 15.95, 'avg': 12.95},
                'Salads': {'min': 7.95, 'max': 12.95, 'avg': 10.45},
                'Sides': {'min': 3.95, 'max': 6.95, 'avg': 5.45},
                'Beverages': {'min': 2.95, 'max': 4.95, 'avg': 3.95}
            }
        }
        
        # Determine which template to use based on listing type and kosher category
        template_key = 'restaurant'  # default
        
        if listing_type:
            listing_lower = listing_type.lower()
            if 'pizza' in listing_lower:
                template_key = 'pizza'
            elif 'sushi' in listing_lower:
                template_key = 'sushi'
            elif 'bakery' in listing_lower or 'bakery' in restaurant_name.lower():
                template_key = 'bakery'
            elif 'cafe' in listing_lower or 'cafe' in restaurant_name.lower():
                template_key = 'cafe'
            elif 'deli' in listing_lower or 'deli' in restaurant_name.lower():
                template_key = 'deli'
        
        # Get the appropriate template
        template = pricing_templates.get(template_key, pricing_templates['restaurant'])
        
        # Add some variation based on kosher category
        variation_factor = 1.0
        if kosher_category == 'meat':
            variation_factor = 1.1  # Meat restaurants tend to be slightly more expensive
        elif kosher_category == 'dairy':
            variation_factor = 1.05  # Dairy restaurants slightly more expensive
        elif kosher_category == 'pareve':
            variation_factor = 0.95  # Pareve restaurants slightly less expensive
        
        # Apply variation to the template
        pricing_data = {}
        for section, prices in template.items():
            pricing_data[section] = {
                'min': round(prices['min'] * variation_factor, 2),
                'max': round(prices['max'] * variation_factor, 2),
                'avg': round(prices['avg'] * variation_factor, 2)
            }
        
        return pricing_data
    
    def update_restaurant_pricing(self, restaurant_id: int, pricing_data: Dict[str, Any]) -> bool:
        """Update restaurant with menu pricing data."""
        try:
            pricing_json = json.dumps(pricing_data, indent=2)
            
            self.cursor.execute("""
                UPDATE restaurants 
                SET menu_pricing = ?, updated_date = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (pricing_json, restaurant_id))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error updating restaurant {restaurant_id}: {e}")
            return False
    
    def process_restaurant(self, restaurant_id: int, name: str, listing_type: str, kosher_category: str) -> bool:
        """Process a single restaurant to generate pricing data."""
        try:
            logger.info(f"Processing: {name}")
            
            # Generate pricing data
            pricing_data = self.generate_sample_pricing(name, listing_type, kosher_category)
            
            # Update database
            success = self.update_restaurant_pricing(restaurant_id, pricing_data)
            
            if success:
                logger.info(f"✅ Updated {name} with {len(pricing_data)} menu sections")
                # Log a sample of the pricing
                first_section = list(pricing_data.keys())[0]
                sample_prices = pricing_data[first_section]
                logger.info(f"   Sample: {first_section} - ${sample_prices['min']}-${sample_prices['max']} (avg: ${sample_prices['avg']})")
            else:
                logger.error(f"❌ Failed to update {name}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error processing {name}: {e}")
            return False
    
    def run(self, limit: int = None):
        """Main execution function."""
        if not self.connect_db():
            return
        
        try:
            # Get restaurants without pricing
            restaurants = self.get_restaurants_without_pricing()
            
            if not restaurants:
                logger.info("No restaurants missing menu pricing!")
                return
            
            logger.info(f"Found {len(restaurants)} restaurants missing menu pricing")
            
            if limit:
                restaurants = restaurants[:limit]
                logger.info(f"Processing first {limit} restaurants")
            
            # Process restaurants
            success_count = 0
            total_count = len(restaurants)
            
            for i, (restaurant_id, name, listing_type, kosher_category) in enumerate(restaurants, 1):
                logger.info(f"Progress: {i}/{total_count}")
                
                success = self.process_restaurant(restaurant_id, name, listing_type, kosher_category)
                if success:
                    success_count += 1
            
            logger.info(f"✅ Completed! Updated {success_count}/{total_count} restaurants")
            
        except Exception as e:
            logger.error(f"Error in main execution: {e}")
        
        finally:
            self.conn.close()

def main():
    """Main function with user interaction."""
    print("💰 Menu Pricing Updater")
    print("=" * 50)
    
    updater = MenuPricingUpdater()
    
    print("\nOptions:")
    print("1. Process all restaurants missing pricing")
    print("2. Process first 10 restaurants (test)")
    print("3. Process first 50 restaurants")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        updater.run()
    elif choice == "2":
        updater.run(limit=10)
    elif choice == "3":
        updater.run(limit=50)
    elif choice == "4":
        print("Exiting...")
    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main() 