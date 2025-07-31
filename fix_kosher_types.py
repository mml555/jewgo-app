#!/usr/bin/env python3
"""
Fix Kosher Types for ORB Restaurants
Update all ORB restaurants to have the correct kosher type based on their source.
"""

import os
import sys
import logging
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database_manager_v3 import EnhancedDatabaseManager as DatabaseManager

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_kosher_types():
    """Fix kosher types for all ORB restaurants."""
    try:
        db_manager = DatabaseManager()
        
        # Get all ORB restaurants
        session = db_manager.get_session()
        orb_restaurants = session.query(db_manager.Restaurant).filter(
            db_manager.Restaurant.source == 'orb'
        ).all()
        
        logger.info(f"Found {len(orb_restaurants)} ORB restaurants to update")
        
        updated_count = 0
        for restaurant in orb_restaurants:
            try:
                # Update kosher type to "dairy" since they come from the dairy category
                old_kosher_type = restaurant.kosher_type
                restaurant.kosher_type = "dairy"
                restaurant.updated_at = datetime.utcnow()
                
                logger.info(f"Updated {restaurant.name}: {old_kosher_type} -> dairy")
                updated_count += 1
                
            except Exception as e:
                logger.error(f"Error updating restaurant {restaurant.name}: {e}")
        
        # Commit all changes
        session.commit()
        logger.info(f"Successfully updated {updated_count} ORB restaurants")
        
        # Also update any restaurants with source='orb' that might be in the legacy table
        legacy_orb_restaurants = session.query(db_manager.Restaurant).filter(
            db_manager.Restaurant.hechsher_details == 'ORB Kosher'
        ).all()
        
        legacy_updated = 0
        for restaurant in legacy_orb_restaurants:
            if restaurant.kosher_type != "dairy":
                old_kosher_type = restaurant.kosher_type
                restaurant.kosher_type = "dairy"
                restaurant.updated_at = datetime.utcnow()
                
                logger.info(f"Updated legacy {restaurant.name}: {old_kosher_type} -> dairy")
                legacy_updated += 1
        
        session.commit()
        logger.info(f"Successfully updated {legacy_updated} legacy ORB restaurants")
        
        return True
        
    except Exception as e:
        logger.error(f"Error fixing kosher types: {e}")
        return False
    finally:
        if 'session' in locals():
            session.close()

def main():
    """Main function."""
    print("🔧 Fixing Kosher Types for ORB Restaurants")
    print("=" * 50)
    
    success = fix_kosher_types()
    
    if success:
        print("\n✅ Kosher types fixed successfully!")
        print("🔍 All ORB restaurants now have kosher_type = 'dairy'")
    else:
        print("\n❌ Failed to fix kosher types.")
    
    return success

if __name__ == "__main__":
    main() 