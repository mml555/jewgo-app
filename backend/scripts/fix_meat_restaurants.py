#!/usr/bin/env python3
"""
Fix Meat Restaurants Script
===========================

This script fixes the kosher categorization for meat restaurants that are 
currently miscategorized as dairy. It identifies meat restaurants by name
and updates their kosher_type and kosher_category to 'meat'.

Author: JewGo Development Team
Version: 1.0
Last Updated: 2024
"""

import sys
import os
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database_manager_v3 import EnhancedDatabaseManager
import structlog

# Configure structured logging
logger = structlog.get_logger()

def fix_meat_restaurants():
    """Fix kosher categorization for meat restaurants."""
    try:
        # Initialize database manager
        db_manager = EnhancedDatabaseManager()
        
        if not db_manager.connect():
            logger.error("Failed to connect to database")
            return False
        
        # List of restaurants that should be meat (based on name analysis)
        meat_restaurants = [
            "JZ Steakhouse",
            "The W Kosher Steakhouse", 
            "Capas Burger",
            "Smash House Burgers Boca",
            "Smash House Burgers Miami",
            "Holy Smokes BBQ and Grill (Food Truck)",
            "Avi's Grill, Inc.",
            "Barakeh Shawarma & Grill",
            "Ben Yehuda Grill",
            "Bissaleh Alma Grill & Bar",
            "Bissli Grill",
            "Century Grill",
            "Grill Place",
            "Grill Xpress",
            "Lasso Kosher Grill",
            "PX Grill Mediterranean Cuisine",
            "Plantation Pita & Grill",
            "Sunrise Pita & Grill (Davie)",
            "Tagine by Alma Grill",
            "The Cave Kosher Bar & Grill",
            "Hummus Vegas & Grill (Hollywood)"
        ]
        
        session = db_manager.get_session()
        from database.database_manager_v3 import Restaurant
        
        updated_count = 0
        
        for restaurant_name in meat_restaurants:
            try:
                # Find the restaurant
                restaurant = session.query(Restaurant).filter(
                    Restaurant.name == restaurant_name
                ).first()
                
                if restaurant:
                    # Update kosher type and category
                    old_type = restaurant.kosher_type
                    restaurant.kosher_type = 'meat'
                    restaurant.kosher_category = 'meat'
                    restaurant.updated_at = datetime.utcnow()
                    
                    session.commit()
                    updated_count += 1
                    logger.info(f"Updated {restaurant_name}: {old_type} -> meat")
                else:
                    logger.warning(f"Restaurant not found: {restaurant_name}")
                    
            except Exception as e:
                logger.error(f"Error updating {restaurant_name}: {e}")
                session.rollback()
                continue
        
        logger.info(f"Successfully updated {updated_count} meat restaurants")
        
        # Show final statistics
        kosher_types = session.query(
            Restaurant.kosher_type,
            db_manager.db.func.count(Restaurant.kosher_type)
        ).group_by(Restaurant.kosher_type).all()
        
        logger.info("Final Kosher Type Distribution:")
        for kosher_type, count in kosher_types:
            logger.info(f"  - {kosher_type}: {count} restaurants")
        
        session.close()
        db_manager.disconnect()
        
        return True
        
    except Exception as e:
        logger.error(f"Error fixing meat restaurants: {e}")
        return False

if __name__ == "__main__":
    success = fix_meat_restaurants()
    if success:
        print("✅ Meat restaurants fixed successfully!")
    else:
        print("❌ Failed to fix meat restaurants")
        sys.exit(1) 