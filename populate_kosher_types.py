#!/usr/bin/env python3
"""
Populate Kosher Types Script
This script populates the kosher_type field with dairy, meat, or pareve information
based on restaurant names, descriptions, and other available data.
"""

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import structlog

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

def get_database_url():
    """Get database URL from environment."""
    return os.environ.get('DATABASE_URL')

def determine_kosher_type(name, description, cuisine_type):
    """Determine kosher type based on restaurant name and description."""
    name_lower = (name or '').lower()
    desc_lower = (description or '').lower()
    cuisine_lower = (cuisine_type or '').lower()
    
    # Dairy indicators
    dairy_keywords = [
        'dairy', 'milk', 'cheese', 'pizza', 'ice cream', 'yogurt', 'cream',
        'butter', 'lactose', 'cafe', 'coffee', 'latte', 'cappuccino',
        'bakery', 'pastry', 'dessert', 'sweet', 'chocolate', 'milkshake'
    ]
    
    # Meat indicators
    meat_keywords = [
        'meat', 'beef', 'chicken', 'steak', 'burger', 'bbq', 'grill',
        'deli', 'sandwich', 'hot dog', 'sausage', 'brisket', 'pastrami',
        'roast', 'chop', 'rib', 'wings', 'nugget', 'cutlet'
    ]
    
    # Pareve indicators (neutral)
    pareve_keywords = [
        'pareve', 'parve', 'neutral', 'fish', 'sushi', 'vegetarian',
        'vegan', 'salad', 'soup', 'pasta', 'rice', 'noodle', 'asian',
        'chinese', 'japanese', 'thai', 'indian', 'mediterranean'
    ]
    
    # Check for dairy keywords
    for keyword in dairy_keywords:
        if keyword in name_lower or keyword in desc_lower or keyword in cuisine_lower:
            return 'dairy'
    
    # Check for meat keywords
    for keyword in meat_keywords:
        if keyword in name_lower or keyword in desc_lower or keyword in cuisine_lower:
            return 'meat'
    
    # Check for pareve keywords
    for keyword in pareve_keywords:
        if keyword in name_lower or keyword in desc_lower or keyword in cuisine_lower:
            return 'pareve'
    
    # Default to pareve if no clear indicators
    return 'pareve'

def populate_kosher_types():
    """Populate kosher_type field for all restaurants."""
    database_url = get_database_url()
    
    if not database_url:
        logger.error("No database URL found in environment variables")
        print("❌ No database URL found. Please check environment variables.")
        return False
    
    try:
        # Connect to database
        conn = psycopg2.connect(database_url)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        logger.info("Connected to database for kosher type population")
        print("✅ Connected to database")
        
        # Get all restaurants that don't have kosher_type set
        cursor.execute("""
            SELECT id, name, description, cuisine_type, kosher_type 
            FROM restaurants 
            WHERE kosher_type IS NULL OR kosher_type = ''
        """)
        
        restaurants = cursor.fetchall()
        logger.info(f"Found {len(restaurants)} restaurants without kosher_type")
        print(f"📊 Found {len(restaurants)} restaurants without kosher_type")
        
        if not restaurants:
            print("ℹ️  All restaurants already have kosher_type set")
            return True
        
        # Update each restaurant
        updated_count = 0
        for restaurant in restaurants:
            restaurant_id, name, description, cuisine_type, current_kosher_type = restaurant
            
            # Determine kosher type
            kosher_type = determine_kosher_type(name, description, cuisine_type)
            
            # Update the database
            cursor.execute("""
                UPDATE restaurants 
                SET kosher_type = %s 
                WHERE id = %s
            """, (kosher_type, restaurant_id))
            
            logger.info(f"Updated restaurant {restaurant_id}: {name} -> {kosher_type}")
            print(f"✅ {name}: {kosher_type}")
            updated_count += 1
        
        print(f"🎉 Successfully updated {updated_count} restaurants with kosher types")
        
        # Verify the updates
        cursor.execute("""
            SELECT kosher_type, COUNT(*) 
            FROM restaurants 
            WHERE kosher_type IS NOT NULL 
            GROUP BY kosher_type
        """)
        
        results = cursor.fetchall()
        print("\n📋 Kosher Type Distribution:")
        for kosher_type, count in results:
            print(f"  - {kosher_type}: {count} restaurants")
        
        cursor.close()
        conn.close()
        
        logger.info("Kosher type population completed successfully")
        print("🎉 Kosher type population completed successfully!")
        return True
        
    except Exception as e:
        logger.error("Failed to populate kosher types", error=str(e))
        print(f"❌ Failed to populate kosher types: {str(e)}")
        return False

def test_kosher_type_determination():
    """Test the kosher type determination logic."""
    print("🧪 Testing kosher type determination...")
    
    test_cases = [
        ("Pizza Palace", "Best pizza in town", "Italian"),
        ("Steak House", "Premium beef steaks", "American"),
        ("Sushi Bar", "Fresh fish and sushi", "Japanese"),
        ("Ice Cream Shop", "Homemade ice cream", "Dessert"),
        ("BBQ Joint", "Smoked meats", "BBQ"),
        ("Cafe Express", "Coffee and pastries", "Cafe"),
        ("Fish Market", "Fresh seafood", "Seafood"),
        ("Unknown Restaurant", "Generic description", "Restaurant")
    ]
    
    for name, description, cuisine in test_cases:
        kosher_type = determine_kosher_type(name, description, cuisine)
        print(f"  - {name}: {kosher_type}")
    
    print("✅ Kosher type determination test completed")

if __name__ == "__main__":
    print("🍽️  Populate Kosher Types")
    print("=" * 50)
    
    # Test the logic first
    test_kosher_type_determination()
    print()
    
    # Populate the database
    if populate_kosher_types():
        print("\n🎉 All done! Kosher types have been populated.")
    else:
        print("\n❌ Failed to populate kosher types.") 