#!/usr/bin/env python3
"""
Show ORB Restaurant Statistics
============================

This script displays comprehensive statistics about the loaded ORB restaurant data
in the database.

Author: JewGo Development Team
Version: 1.0
"""

import os
import sys
from sqlalchemy import func

# Import database manager and Restaurant model
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database.database_manager_v3 import EnhancedDatabaseManager, Restaurant

def show_orb_statistics():
    """Display comprehensive statistics about the loaded ORB restaurant data."""
    
    # Initialize database manager
    db_manager = EnhancedDatabaseManager()
    if not db_manager.connect():
        print("❌ Failed to connect to database")
        return False
    
    try:
        session = db_manager.get_session()
        
        # Get total count
        total_count = session.query(Restaurant).count()
        
        # Get kosher category distribution
        kosher_types = session.query(
            Restaurant.kosher_category,
            func.count(Restaurant.kosher_category)
        ).group_by(Restaurant.kosher_category).all()
        
        # Get certifying agency distribution
        agencies = session.query(
            Restaurant.certifying_agency,
            func.count(Restaurant.certifying_agency)
        ).group_by(Restaurant.certifying_agency).all()
        
        # Get city distribution (top 15)
        cities = session.query(
            Restaurant.city,
            func.count(Restaurant.city)
        ).group_by(Restaurant.city).order_by(func.count(Restaurant.city).desc()).limit(15).all()
        
        # Get state distribution
        states = session.query(
            Restaurant.state,
            func.count(Restaurant.state)
        ).group_by(Restaurant.state).all()
        
        # Get restaurants with missing data
        missing_phone = session.query(Restaurant).filter(
            Restaurant.phone_number == "(555) 000-0000"
        ).count()
        
        missing_address = session.query(Restaurant).filter(
            Restaurant.address == "Address not available"
        ).count()
        
        missing_zip = session.query(Restaurant).filter(
            Restaurant.zip_code == "00000"
        ).count()
        
        # Print statistics
        print("=" * 60)
        print("📊 ORB RESTAURANT DATA STATISTICS")
        print("=" * 60)
        print(f"Total Restaurants: {total_count}")
        print()
        
        print("🥩 Kosher Category Distribution:")
        for kosher_type, count in kosher_types:
            percentage = (count / total_count) * 100
            print(f"  • {kosher_type.capitalize()}: {count} restaurants ({percentage:.1f}%)")
        print()
        
        print("🏛️ Certifying Agency Distribution:")
        for agency, count in agencies:
            percentage = (count / total_count) * 100
            print(f"  • {agency}: {count} restaurants ({percentage:.1f}%)")
        print()
        
        print("🏙️ Top 15 Cities:")
        for city, count in cities:
            percentage = (count / total_count) * 100
            print(f"  • {city}: {count} restaurants ({percentage:.1f}%)")
        print()
        
        print("🗺️ State Distribution:")
        for state, count in states:
            percentage = (count / total_count) * 100
            print(f"  • {state}: {count} restaurants ({percentage:.1f}%)")
        print()
        
        print("⚠️ Data Quality Issues:")
        print(f"  • Missing phone numbers: {missing_phone} restaurants")
        print(f"  • Missing addresses: {missing_address} restaurants")
        print(f"  • Missing ZIP codes: {missing_zip} restaurants")
        print()
        
        # Calculate data completeness
        complete_data = total_count - max(missing_phone, missing_address, missing_zip)
        completeness = (complete_data / total_count) * 100
        print(f"📈 Data Completeness: {completeness:.1f}%")
        print("=" * 60)
        
        session.close()
        db_manager.disconnect()
        
        return True
        
    except Exception as e:
        print(f"❌ Error getting statistics: {e}")
        return False

if __name__ == "__main__":
    success = show_orb_statistics()
    
    if not success:
        sys.exit(1) 