#!/usr/bin/env python3
"""
Reset Restaurant IDs
==================

This script resets restaurant IDs to start from 1 and be sequential.
"""

import sys
import os
import structlog

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database_manager_v3 import EnhancedDatabaseManager

# Configure structured logging
logger = structlog.get_logger()

def reset_restaurant_ids():
    """Reset restaurant IDs to start from 1 and be sequential."""
    try:
        # Initialize database manager
        db_manager = EnhancedDatabaseManager()
        
        if not db_manager.connect():
            logger.error("Failed to connect to database")
            return False
        
        session = db_manager.get_session()
        from database.database_manager_v3 import Restaurant
        
        # Get all restaurants ordered by current ID
        restaurants = session.query(Restaurant).order_by(Restaurant.id).all()
        
        logger.info(f"Found {len(restaurants)} restaurants to reset")
        
        if not restaurants:
            logger.info("No restaurants found to reset")
            return True
        
        # Create a mapping of old ID to new sequential ID
        id_mapping = {}
        for i, restaurant in enumerate(restaurants, 1):
            old_id = restaurant.id
            id_mapping[old_id] = i
            logger.info(f"Mapping restaurant '{restaurant.name}' from ID {old_id} to ID {i}")
        
        # Update each restaurant with new sequential ID
        for old_id, new_id in id_mapping.items():
            restaurant = session.query(Restaurant).filter(Restaurant.id == old_id).first()
            if restaurant:
                # Temporarily set ID to a very high number to avoid conflicts
                temp_id = 999999 + new_id
                restaurant.id = temp_id
                session.commit()
        
        # Now set the final sequential IDs
        for old_id, new_id in id_mapping.items():
            restaurant = session.query(Restaurant).filter(Restaurant.id == 999999 + new_id).first()
            if restaurant:
                restaurant.id = new_id
                session.commit()
                logger.info(f"Set restaurant '{restaurant.name}' to ID {new_id}")
        
        # Reset the PostgreSQL sequence
        try:
            session.execute("SELECT setval('restaurants_id_seq', (SELECT MAX(id) FROM restaurants))")
            session.commit()
            logger.info("Reset PostgreSQL sequence")
        except Exception as e:
            logger.warning(f"Could not reset sequence: {e}")
        
        # Verify the results
        final_restaurants = session.query(Restaurant).order_by(Restaurant.id).all()
        logger.info(f"Final restaurant count: {len(final_restaurants)}")
        
        # Show first few restaurants with their new IDs
        logger.info("First 10 restaurants with new IDs:")
        for i, restaurant in enumerate(final_restaurants[:10]):
            logger.info(f"  {restaurant.id}. {restaurant.name} ({restaurant.kosher_category})")
        
        session.close()
        db_manager.disconnect()
        
        return True
        
    except Exception as e:
        logger.error(f"Error resetting restaurant IDs: {e}")
        return False

if __name__ == "__main__":
    success = reset_restaurant_ids()
    
    if success:
        print("✅ Restaurant IDs reset successfully!")
    else:
        print("❌ Failed to reset restaurant IDs!")
        sys.exit(1) 