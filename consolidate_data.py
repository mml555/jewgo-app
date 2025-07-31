#!/usr/bin/env python3
"""
Data Consolidation Script
Merges kosher_places data into restaurants table and consolidates the schema
"""

import os
import psycopg2
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataConsolidator:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Connect to the database."""
        try:
            self.conn = psycopg2.connect(self.database_url)
            self.cursor = self.conn.cursor()
            logger.info("Connected to database successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the database."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logger.info("Disconnected from database")
    
    def get_kosher_places_data(self) -> List[Dict]:
        """Fetch all data from kosher_places table."""
        try:
            self.cursor.execute("""
                SELECT id, name, detail_url, category, photo, address, phone, 
                       website, kosher_cert_link, kosher_type, extra_kosher_info, 
                       created_at, short_description, email, google_listing_url, 
                       status, is_cholov_yisroel, is_pas_yisroel, hours_open, price_range
                FROM kosher_places
                ORDER BY id
            """)
            
            columns = [desc[0] for desc in self.cursor.description]
            rows = self.cursor.fetchall()
            
            data = []
            for row in rows:
                data.append(dict(zip(columns, row)))
            
            logger.info(f"Fetched {len(data)} records from kosher_places")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching kosher_places data: {e}")
            return []
    
    def get_existing_restaurants(self) -> Dict[str, Dict]:
        """Get existing restaurants by name and address for deduplication."""
        try:
            self.cursor.execute("""
                SELECT id, name, address, phone, website, kosher_type, hechsher_details
                FROM restaurants
            """)
            
            existing = {}
            for row in self.cursor.fetchall():
                key = f"{row[1]}_{row[2]}"  # name_address
                existing[key] = {
                    'id': row[0],
                    'name': row[1],
                    'address': row[2],
                    'phone': row[3],
                    'website': row[4],
                    'kosher_type': row[5],
                    'hechsher_details': row[6]
                }
            
            logger.info(f"Found {len(existing)} existing restaurants")
            return existing
            
        except Exception as e:
            logger.error(f"Error fetching existing restaurants: {e}")
            return {}
    
    def parse_address(self, address: str) -> Tuple[str, str, str]:
        """Parse address into city, state, zip_code."""
        if not address:
            return None, None, None
        
        # Simple parsing - can be enhanced
        parts = address.split(',')
        if len(parts) >= 3:
            city = parts[-2].strip() if len(parts) > 2 else None
            state_zip = parts[-1].strip() if len(parts) > 1 else None
            
            # Extract state and zip from last part
            if state_zip:
                state_zip_parts = state_zip.split()
                if len(state_zip_parts) >= 2:
                    state = state_zip_parts[0]
                    zip_code = state_zip_parts[-1]
                else:
                    state = state_zip_parts[0] if state_zip_parts else None
                    zip_code = None
            else:
                state = None
                zip_code = None
        else:
            city = None
            state = None
            zip_code = None
        
        return city, state, zip_code
    
    def normalize_kosher_type(self, kosher_type: str) -> str:
        """Normalize kosher type values."""
        if not kosher_type:
            return None
        
        kosher_type = kosher_type.lower().strip()
        
        # Map ORB values to standardized values
        mapping = {
            'kosher': 'meat',  # Default to meat if just "kosher"
            'dairy': 'dairy',
            'meat': 'meat',
            'pareve': 'pareve',
            'parve': 'pareve',
            'fleishig': 'meat',
            'milchig': 'dairy',
            'neutral': 'pareve'
        }
        
        return mapping.get(kosher_type, kosher_type)
    
    def consolidate_record(self, kosher_place: Dict, existing_restaurants: Dict) -> Optional[Dict]:
        """Consolidate a kosher_place record into restaurants format."""
        name = kosher_place.get('name')
        address = kosher_place.get('address')
        
        if not name or not address:
            logger.warning(f"Skipping record with missing name or address: {name}")
            return None
        
        # Check for duplicates
        key = f"{name}_{address}"
        if key in existing_restaurants:
            existing = existing_restaurants[key]
            logger.info(f"Found duplicate: {name} - will update existing record")
            return self.update_existing_record(existing, kosher_place)
        
        # Parse address
        city, state, zip_code = self.parse_address(address)
        
        # Normalize kosher type
        kosher_type = self.normalize_kosher_type(kosher_place.get('kosher_type'))
        
        # Map kosher_places fields to restaurants fields
        consolidated = {
            'name': name,
            'address': address,
            'city': city,
            'state': state,
            'zip_code': zip_code,
            'phone': kosher_place.get('phone'),
            'website': kosher_place.get('website'),
            'cuisine_type': kosher_place.get('category', 'Restaurant'),
            'kosher_type': kosher_type,
            'hechsher_details': kosher_place.get('extra_kosher_info'),
            'image_url': kosher_place.get('photo'),
            'kosher_cert_link': kosher_place.get('kosher_cert_link'),
            'short_description': kosher_place.get('short_description'),
            'email': kosher_place.get('email'),
            'google_listing_url': kosher_place.get('google_listing_url'),
            'hours_open': kosher_place.get('hours_open'),
            'price_range': kosher_place.get('price_range'),
            'is_kosher': True,  # All kosher_places are kosher
            'is_hechsher': True,  # All have hechsher
            'category': 'restaurant',
            'status': 'approved',  # Mark as approved since from ORB
            'created_at': kosher_place.get('created_at') or datetime.now(),
            'updated_at': datetime.now(),
            'detail_url': kosher_place.get('detail_url')
        }
        
        return consolidated
    
    def update_existing_record(self, existing: Dict, kosher_place: Dict) -> Optional[Dict]:
        """Update existing restaurant record with kosher_places data."""
        # Only update if kosher_places has better/missing data
        updates = {}
        
        # Update kosher certification if missing
        if not existing.get('hechsher_details') and kosher_place.get('extra_kosher_info'):
            updates['hechsher_details'] = kosher_place.get('extra_kosher_info')
        
        # Update kosher type if missing or different
        if not existing.get('kosher_type') and kosher_place.get('kosher_type'):
            updates['kosher_type'] = self.normalize_kosher_type(kosher_place.get('kosher_type'))
        
        # Update other fields if missing
        if not existing.get('website') and kosher_place.get('website'):
            updates['website'] = kosher_place.get('website')
        
        if not existing.get('phone') and kosher_place.get('phone'):
            updates['phone'] = kosher_place.get('phone')
        
        if updates:
            updates['id'] = existing['id']
            updates['updated_at'] = datetime.now()
            return updates
        
        return None
    
    def insert_restaurant(self, data: Dict) -> bool:
        """Insert a new restaurant record."""
        try:
            self.cursor.execute("""
                INSERT INTO restaurants (
                    name, address, city, state, zip_code, phone, website, 
                    cuisine_type, kosher_type, hechsher_details, image_url, 
                    kosher_cert_link, short_description, email, google_listing_url,
                    hours_open, price_range, is_kosher, is_hechsher, category, 
                    status, created_at, updated_at, detail_url
                ) VALUES (
                    %(name)s, %(address)s, %(city)s, %(state)s, %(zip_code)s, 
                    %(phone)s, %(website)s, %(cuisine_type)s, %(kosher_type)s, 
                    %(hechsher_details)s, %(image_url)s, %(kosher_cert_link)s, 
                    %(short_description)s, %(email)s, %(google_listing_url)s,
                    %(hours_open)s, %(price_range)s, %(is_kosher)s, %(is_hechsher)s, 
                    %(category)s, %(status)s, %(created_at)s, %(updated_at)s, %(detail_url)s
                )
            """, data)
            
            return True
            
        except Exception as e:
            logger.error(f"Error inserting restaurant {data.get('name')}: {e}")
            return False
    
    def update_restaurant(self, data: Dict) -> bool:
        """Update an existing restaurant record."""
        try:
            # Build dynamic UPDATE query
            update_fields = []
            values = []
            
            for key, value in data.items():
                if key not in ['id', 'created_at'] and value is not None:
                    update_fields.append(f"{key} = %s")
                    values.append(value)
            
            if not update_fields:
                return True  # Nothing to update
            
            values.append(data['id'])  # For WHERE clause
            
            query = f"""
                UPDATE restaurants 
                SET {', '.join(update_fields)}, updated_at = NOW()
                WHERE id = %s
            """
            
            self.cursor.execute(query, values)
            return True
            
        except Exception as e:
            logger.error(f"Error updating restaurant {data.get('name')}: {e}")
            return False
    
    def run_consolidation(self):
        """Run the complete data consolidation process."""
        logger.info("Starting data consolidation process...")
        
        # Get existing data
        kosher_places = self.get_kosher_places_data()
        existing_restaurants = self.get_existing_restaurants()
        
        if not kosher_places:
            logger.error("No kosher_places data found")
            return
        
        # Process each kosher_place record
        inserted_count = 0
        updated_count = 0
        skipped_count = 0
        
        for kosher_place in kosher_places:
            try:
                consolidated = self.consolidate_record(kosher_place, existing_restaurants)
                
                if not consolidated:
                    skipped_count += 1
                    continue
                
                if 'id' in consolidated:
                    # Update existing record
                    if self.update_restaurant(consolidated):
                        updated_count += 1
                        logger.info(f"Updated: {consolidated['name']}")
                    else:
                        skipped_count += 1
                else:
                    # Insert new record
                    if self.insert_restaurant(consolidated):
                        inserted_count += 1
                        logger.info(f"Inserted: {consolidated['name']}")
                    else:
                        skipped_count += 1
                
                # Commit every 10 records
                if (inserted_count + updated_count) % 10 == 0:
                    self.conn.commit()
                    logger.info(f"Committed {inserted_count + updated_count} records...")
                
            except Exception as e:
                logger.error(f"Error processing {kosher_place.get('name')}: {e}")
                skipped_count += 1
        
        # Final commit
        self.conn.commit()
        
        # Summary
        logger.info("=== CONSOLIDATION SUMMARY ===")
        logger.info(f"Total kosher_places processed: {len(kosher_places)}")
        logger.info(f"New restaurants inserted: {inserted_count}")
        logger.info(f"Existing restaurants updated: {updated_count}")
        logger.info(f"Records skipped: {skipped_count}")
        logger.info(f"Total restaurants after consolidation: {inserted_count + updated_count + len(existing_restaurants)}")
    
    def cleanup_kosher_places(self):
        """Optionally clean up kosher_places table after consolidation."""
        try:
            # First, create a backup
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS kosher_places_backup AS 
                SELECT * FROM kosher_places
            """)
            self.conn.commit()
            logger.info("Created kosher_places_backup table")
            
            # Then truncate kosher_places (or you can drop it)
            self.cursor.execute("TRUNCATE TABLE kosher_places")
            self.conn.commit()
            logger.info("Cleaned up kosher_places table")
            
        except Exception as e:
            logger.error(f"Error cleaning up kosher_places: {e}")

def main():
    """Main execution function."""
    # Get database URL from environment
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        logger.error("DATABASE_URL environment variable not set")
        return
    
    # Initialize consolidator
    consolidator = DataConsolidator(database_url)
    
    try:
        # Connect to database
        if not consolidator.connect():
            return
        
        # Run consolidation
        consolidator.run_consolidation()
        
        # Ask user if they want to clean up kosher_places
        response = input("\nDo you want to clean up the kosher_places table? (y/N): ")
        if response.lower() == 'y':
            consolidator.cleanup_kosher_places()
        
        logger.info("Data consolidation completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during consolidation: {e}")
    
    finally:
        consolidator.disconnect()

if __name__ == "__main__":
    main() 