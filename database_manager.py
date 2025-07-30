#!/usr/bin/env python3
"""
Database Manager Utility
Provides easy-to-use functions for managing restaurant data in the scalable database.
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """High-level database manager for restaurant operations."""
    
    def __init__(self, db_path: str = "restaurants.db"):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Connect to the database."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the database."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def add_restaurant(self, restaurant_data: Dict[str, Any]) -> bool:
        """Add a new restaurant to the database."""
        try:
            # Parse address components
            address_parts = self._parse_address(restaurant_data.get('address', ''))
            
            sql = """
            INSERT INTO restaurants (
                business_id, name, website_link, phone_number, address, city, state, zip_code,
                certificate_link, image_url, certifying_agency, kosher_category, data_source,
                external_id, notes, created_date, updated_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """
            
            values = (
                restaurant_data.get('business_id', ''),
                restaurant_data.get('name', ''),
                restaurant_data.get('website_link', ''),
                restaurant_data.get('phone_number', ''),
                restaurant_data.get('address', ''),
                address_parts['city'],
                address_parts['state'],
                address_parts['zip_code'],
                restaurant_data.get('certificate_link', ''),
                restaurant_data.get('image_url', ''),
                restaurant_data.get('certifying_agency', 'ORB'),
                restaurant_data.get('kosher_category', 'unknown'),
                restaurant_data.get('data_source', 'manual'),
                restaurant_data.get('external_id', ''),
                restaurant_data.get('notes', '')
            )
            
            self.cursor.execute(sql, values)
            self.connection.commit()
            logger.info(f"Added restaurant: {restaurant_data.get('name', 'Unknown')}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding restaurant: {e}")
            return False
    
    def update_restaurant(self, business_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing restaurant."""
        try:
            # Build dynamic update query
            set_clauses = []
            values = []
            
            for key, value in updates.items():
                if key in ['name', 'website_link', 'phone_number', 'address', 'certificate_link', 
                          'image_url', 'certifying_agency', 'kosher_category', 'status', 'rating',
                          'price_range', 'hours_of_operation', 'notes', 'short_description']:
                    set_clauses.append(f"{key} = ?")
                    values.append(value)
            
            if not set_clauses:
                return False
            
            set_clauses.append("updated_date = CURRENT_TIMESTAMP")
            values.append(business_id)
            
            sql = f"""
            UPDATE restaurants 
            SET {', '.join(set_clauses)}
            WHERE business_id = ?
            """
            
            self.cursor.execute(sql, values)
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                logger.info(f"Updated restaurant with business_id: {business_id}")
                return True
            else:
                logger.warning(f"No restaurant found with business_id: {business_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error updating restaurant: {e}")
            return False
    
    def get_restaurant(self, business_id: str) -> Optional[Dict]:
        """Get a restaurant by business_id."""
        try:
            self.cursor.execute("""
                SELECT * FROM restaurants WHERE business_id = ?
            """, (business_id,))
            
            row = self.cursor.fetchone()
            if row:
                return dict(row)
            return None
            
        except Exception as e:
            logger.error(f"Error getting restaurant: {e}")
            return None

    def get_restaurant_by_id(self, restaurant_id: int) -> Optional[Dict]:
        """Get a restaurant by numeric id."""
        try:
            self.cursor.execute("""
                SELECT * FROM restaurants WHERE id = ?
            """, (restaurant_id,))
            
            row = self.cursor.fetchone()
            if row:
                restaurant_dict = dict(row)
                
                # Parse JSON fields
                if restaurant_dict.get('menu_pricing'):
                    try:
                        restaurant_dict['menu_pricing'] = json.loads(restaurant_dict['menu_pricing'])
                    except (json.JSONDecodeError, TypeError):
                        restaurant_dict['menu_pricing'] = None
                
                return restaurant_dict
            return None
            
        except Exception as e:
            logger.error(f"Error getting restaurant by id: {e}")
            return None
    
    def search_restaurants(self, query: str = "", category: str = "", state: str = "", 
                          limit: int = 50, offset: int = 0) -> List[Dict]:
        """Search restaurants with filters."""
        try:
            conditions = ["status = 'active'"]
            values = []
            
            if query:
                conditions.append("(name LIKE ? OR address LIKE ?)")
                values.extend([f"%{query}%", f"%{query}%"])
            
            if category:
                conditions.append("kosher_category = ?")
                values.append(category)
            
            if state:
                conditions.append("state = ?")
                values.append(state)
            
            where_clause = " AND ".join(conditions)
            
            sql = f"""
            SELECT * FROM restaurants 
            WHERE {where_clause}
            ORDER BY name
            LIMIT ? OFFSET ?
            """
            
            values.extend([limit, offset])
            self.cursor.execute(sql, values)
            
            restaurants = []
            for row in self.cursor.fetchall():
                restaurant_dict = dict(row)
                
                # Parse JSON fields
                if restaurant_dict.get('menu_pricing'):
                    try:
                        restaurant_dict['menu_pricing'] = json.loads(restaurant_dict['menu_pricing'])
                    except (json.JSONDecodeError, TypeError):
                        restaurant_dict['menu_pricing'] = None
                
                restaurants.append(restaurant_dict)
            
            return restaurants
            
        except Exception as e:
            logger.error(f"Error searching restaurants: {e}")
            return []

    def search_restaurants_near_location(self, lat: float, lng: float, radius: float = 50,
                                       query: str = "", category: str = "", 
                                       limit: int = 50, offset: int = 0) -> List[Dict]:
        """Search restaurants near a specific location using Haversine formula."""
        try:
            conditions = ["status = 'active'"]
            values = []
            
            # Add distance calculation using Haversine formula
            distance_formula = """
            (3959 * acos(cos(radians(?)) * cos(radians(latitude)) * 
            cos(radians(longitude) - radians(?)) + sin(radians(?)) * 
            sin(radians(latitude)))) AS distance
            """
            
            if query:
                conditions.append("(name LIKE ? OR address LIKE ?)")
                values.extend([f"%{query}%", f"%{query}%"])
            
            if category:
                conditions.append("kosher_category = ?")
                values.append(category)
            
            where_clause = " AND ".join(conditions)
            
            # Use a subquery to filter by distance
            sql = f"""
            SELECT *, {distance_formula}
            FROM restaurants 
            WHERE {where_clause}
            AND (3959 * acos(cos(radians(?)) * cos(radians(latitude)) * 
                cos(radians(longitude) - radians(?)) + sin(radians(?)) * 
                sin(radians(latitude)))) <= ?
            ORDER BY distance
            LIMIT ? OFFSET ?
            """
            
            # Add parameters for distance calculation and filtering
            values = [lat, lng, lat] + values + [lat, lng, lat, radius, limit, offset]
            self.cursor.execute(sql, values)
            
            restaurants = []
            for row in self.cursor.fetchall():
                restaurant_dict = dict(row)
                
                # Parse JSON fields
                if restaurant_dict.get('menu_pricing'):
                    try:
                        restaurant_dict['menu_pricing'] = json.loads(restaurant_dict['menu_pricing'])
                    except (json.JSONDecodeError, TypeError):
                        restaurant_dict['menu_pricing'] = None
                
                restaurants.append(restaurant_dict)
            
            return restaurants
            
        except Exception as e:
            logger.error(f"Error searching restaurants near location: {e}")
            return []
    
    def get_restaurants_by_category(self, category: str, limit: int = 50) -> List[Dict]:
        """Get restaurants by kosher category."""
        try:
            self.cursor.execute("""
                SELECT * FROM restaurants 
                WHERE kosher_category = ? AND status = 'active'
                ORDER BY name
                LIMIT ?
            """, (category, limit))
            
            return [dict(row) for row in self.cursor.fetchall()]
            
        except Exception as e:
            logger.error(f"Error getting restaurants by category: {e}")
            return []
    
    def get_restaurants_by_location(self, state: str = "", city: str = "", limit: int = 50) -> List[Dict]:
        """Get restaurants by location."""
        try:
            conditions = ["status = 'active'"]
            values = []
            
            if state:
                conditions.append("state = ?")
                values.append(state)
            
            if city:
                conditions.append("city = ?")
                values.append(city)
            
            where_clause = " AND ".join(conditions)
            
            sql = f"""
            SELECT * FROM restaurants 
            WHERE {where_clause}
            ORDER BY name
            LIMIT ?
            """
            
            values.append(limit)
            self.cursor.execute(sql, values)
            
            return [dict(row) for row in self.cursor.fetchall()]
            
        except Exception as e:
            logger.error(f"Error getting restaurants by location: {e}")
            return []
    
    def add_review(self, restaurant_id: int, review_data: Dict[str, Any]) -> bool:
        """Add a review for a restaurant."""
        try:
            sql = """
            INSERT INTO reviews (
                restaurant_id, reviewer_name, reviewer_email, rating, review_text
            ) VALUES (?, ?, ?, ?, ?)
            """
            
            values = (
                restaurant_id,
                review_data.get('reviewer_name', ''),
                review_data.get('reviewer_email', ''),
                review_data.get('rating', 5),
                review_data.get('review_text', '')
            )
            
            self.cursor.execute(sql, values)
            self.connection.commit()
            
            # Update restaurant rating
            self._update_restaurant_rating(restaurant_id)
            
            logger.info(f"Added review for restaurant ID: {restaurant_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding review: {e}")
            return False
    
    def get_reviews(self, restaurant_id: int, limit: int = 10) -> List[Dict]:
        """Get reviews for a restaurant."""
        try:
            # Check if reviews table exists
            self.cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='reviews'
            """)
            if not self.cursor.fetchone():
                logger.info("Reviews table does not exist, returning empty list")
                return []
            
            self.cursor.execute("""
                SELECT * FROM reviews 
                WHERE restaurant_id = ? AND is_approved = 1
                ORDER BY review_date DESC
                LIMIT ?
            """, (restaurant_id, limit))
            
            return [dict(row) for row in self.cursor.fetchall()]
            
        except Exception as e:
            logger.error(f"Error getting reviews: {e}")
            return []
    
    def add_tag_to_restaurant(self, restaurant_id: int, tag_name: str) -> bool:
        """Add a tag to a restaurant."""
        try:
            # First, ensure the tag exists
            self.cursor.execute("""
                INSERT OR IGNORE INTO tags (name) VALUES (?)
            """, (tag_name,))
            
            # Get the tag ID
            self.cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
            tag_row = self.cursor.fetchone()
            
            if not tag_row:
                return False
            
            tag_id = tag_row[0]
            
            # Add the restaurant-tag relationship
            self.cursor.execute("""
                INSERT OR IGNORE INTO restaurant_tags (restaurant_id, tag_id) 
                VALUES (?, ?)
            """, (restaurant_id, tag_id))
            
            self.connection.commit()
            logger.info(f"Added tag '{tag_name}' to restaurant ID: {restaurant_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding tag: {e}")
            return False
    
    def get_restaurant_tags(self, restaurant_id: int) -> List[Dict]:
        """Get tags for a restaurant."""
        try:
            # Check if tags and restaurant_tags tables exist
            self.cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name IN ('tags', 'restaurant_tags')
            """)
            existing_tables = [row[0] for row in self.cursor.fetchall()]
            if len(existing_tables) < 2:
                logger.info("Tags tables do not exist, returning empty list")
                return []
            
            self.cursor.execute("""
                SELECT t.* FROM tags t
                JOIN restaurant_tags rt ON t.id = rt.tag_id
                WHERE rt.restaurant_id = ?
                ORDER BY t.name
            """, (restaurant_id,))
            
            return [dict(row) for row in self.cursor.fetchall()]
            
        except Exception as e:
            logger.error(f"Error getting restaurant tags: {e}")
            return []
    
    def get_restaurant_count(self) -> int:
        """Get total number of restaurants in the database."""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM restaurants")
            return self.cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Error getting restaurant count: {e}")
            return 0

    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive database statistics."""
        try:
            stats = {}
            
            # Basic counts
            self.cursor.execute("SELECT COUNT(*) FROM restaurants")
            stats['total_restaurants'] = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM restaurants WHERE status = 'active'")
            stats['active_restaurants'] = self.cursor.fetchone()[0]
            
            # Category breakdown
            self.cursor.execute("""
                SELECT kosher_category, COUNT(*) as count 
                FROM restaurants 
                WHERE status = 'active'
                GROUP BY kosher_category 
                ORDER BY count DESC
            """)
            stats['category_breakdown'] = dict(self.cursor.fetchall())
            
            # Geographic breakdown
            self.cursor.execute("""
                SELECT state, COUNT(*) as count 
                FROM restaurants 
                WHERE status = 'active' AND state IS NOT NULL AND state != ''
                GROUP BY state 
                ORDER BY count DESC
                LIMIT 10
            """)
            stats['top_states'] = dict(self.cursor.fetchall())
            
            # Data completeness
            self.cursor.execute("""
                SELECT 
                    COUNT(CASE WHEN certificate_link IS NOT NULL AND certificate_link != '' THEN 1 END) as with_certificates,
                    COUNT(CASE WHEN phone_number IS NOT NULL AND phone_number != '' THEN 1 END) as with_phones,
                    COUNT(CASE WHEN website_link IS NOT NULL AND website_link != '' THEN 1 END) as with_websites,
                    COUNT(CASE WHEN image_url IS NOT NULL AND image_url != '' THEN 1 END) as with_images
                FROM restaurants
                WHERE status = 'active'
            """)
            completeness = self.cursor.fetchone()
            stats['data_completeness'] = {
                'with_certificates': completeness[0],
                'with_phones': completeness[1],
                'with_websites': completeness[2],
                'with_images': completeness[3]
            }
            
            # Recent activity
            self.cursor.execute("""
                SELECT COUNT(*) FROM restaurants 
                WHERE updated_date >= datetime('now', '-7 days')
            """)
            stats['recently_updated'] = self.cursor.fetchone()[0]
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}
    
    def export_to_json(self, filename: str, filters: Dict[str, Any] = None) -> bool:
        """Export restaurants to JSON file."""
        try:
            conditions = ["status = 'active'"]
            values = []
            
            if filters:
                if filters.get('category'):
                    conditions.append("kosher_category = ?")
                    values.append(filters['category'])
                
                if filters.get('state'):
                    conditions.append("state = ?")
                    values.append(filters['state'])
                
                if filters.get('query'):
                    conditions.append("(name LIKE ? OR address LIKE ?)")
                    values.extend([f"%{filters['query']}%", f"%{filters['query']}%"])
            
            where_clause = " AND ".join(conditions)
            
            sql = f"""
            SELECT * FROM restaurants 
            WHERE {where_clause}
            ORDER BY name
            """
            
            self.cursor.execute(sql, values)
            restaurants = [dict(row) for row in self.cursor.fetchall()]
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(restaurants, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Exported {len(restaurants)} restaurants to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            return False
    
    def _parse_address(self, address: str) -> Dict[str, str]:
        """Parse address into components."""
        parts = {
            'city': '',
            'state': '',
            'zip_code': '',
            'country': 'USA'
        }
        
        if not address:
            return parts
        
        address_parts = address.split(',')
        if len(address_parts) >= 2:
            parts['city'] = address_parts[1].strip()
            if len(address_parts) >= 3:
                state_zip = address_parts[2].strip().split()
                if len(state_zip) >= 2:
                    parts['state'] = state_zip[0]
                    parts['zip_code'] = state_zip[1]
        
        return parts
    
    def _update_restaurant_rating(self, restaurant_id: int):
        """Update restaurant's average rating based on reviews."""
        try:
            self.cursor.execute("""
                UPDATE restaurants 
                SET rating = (
                    SELECT AVG(rating) 
                    FROM reviews 
                    WHERE restaurant_id = ? AND is_approved = 1
                ),
                review_count = (
                    SELECT COUNT(*) 
                    FROM reviews 
                    WHERE restaurant_id = ? AND is_approved = 1
                )
                WHERE id = ?
            """, (restaurant_id, restaurant_id, restaurant_id))
            
            self.connection.commit()
            
        except Exception as e:
            logger.error(f"Error updating restaurant rating: {e}")

    def get_restaurant_specials(self, restaurant_id: int, paid_only: bool = True) -> List[Dict]:
        """Get specials for a specific restaurant."""
        try:
            sql = """
            SELECT id, restaurant_id, title, description, discount_percent, discount_amount,
                   start_date, end_date, is_paid, payment_status, special_type, priority, is_active,
                   created_date, updated_date
            FROM restaurant_specials
            WHERE restaurant_id = ? AND is_active = 1
            """
            
            if paid_only:
                sql += " AND is_paid = 1"
            
            sql += " ORDER BY priority ASC, created_date DESC LIMIT 3"
            
            self.cursor.execute(sql, (restaurant_id,))
            specials = []
            
            for row in self.cursor.fetchall():
                specials.append({
                    'id': row['id'],
                    'restaurant_id': row['restaurant_id'],
                    'title': row['title'],
                    'description': row['description'],
                    'discount_percent': row['discount_percent'],
                    'discount_amount': row['discount_amount'],
                    'start_date': row['start_date'],
                    'end_date': row['end_date'],
                    'is_paid': bool(row['is_paid']),
                    'payment_status': row['payment_status'],
                    'special_type': row['special_type'],
                    'priority': row['priority'],
                    'is_active': bool(row['is_active']),
                    'created_date': row['created_date'],
                    'updated_date': row['updated_date']
                })
            
            return specials
            
        except Exception as e:
            logger.error(f"Error getting restaurant specials: {e}")
            return []

    def add_restaurant_special(self, special_data: Dict[str, Any]) -> bool:
        """Add a new special for a restaurant."""
        try:
            sql = """
            INSERT INTO restaurant_specials (
                restaurant_id, title, description, discount_percent, discount_amount,
                start_date, end_date, is_paid, payment_status, special_type, priority, is_active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            values = (
                special_data.get('restaurant_id'),
                special_data.get('title'),
                special_data.get('description'),
                special_data.get('discount_percent'),
                special_data.get('discount_amount'),
                special_data.get('start_date'),
                special_data.get('end_date'),
                special_data.get('is_paid', False),
                special_data.get('payment_status', 'unpaid'),
                special_data.get('special_type', 'discount'),
                special_data.get('priority', 1),
                special_data.get('is_active', True)
            )
            
            self.cursor.execute(sql, values)
            self.connection.commit()
            logger.info(f"Added special for restaurant {special_data.get('restaurant_id')}: {special_data.get('title')}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding restaurant special: {e}")
            return False

    def update_special_payment_status(self, special_id: int, is_paid: bool, payment_status: str = 'paid') -> bool:
        """Update the payment status of a special."""
        try:
            sql = """
            UPDATE restaurant_specials 
            SET is_paid = ?, payment_status = ?, payment_date = CURRENT_TIMESTAMP, updated_date = CURRENT_TIMESTAMP
            WHERE id = ?
            """
            
            self.cursor.execute(sql, (is_paid, payment_status, special_id))
            self.connection.commit()
            logger.info(f"Updated payment status for special {special_id}: {payment_status}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating special payment status: {e}")
            return False

# Example usage functions
def example_usage():
    """Example of how to use the DatabaseManager."""
    db = DatabaseManager()
    
    if not db.connect():
        print("Failed to connect to database")
        return
    
    try:
        # Search for restaurants
        restaurants = db.search_restaurants(query="pizza", category="dairy", limit=10)
        print(f"Found {len(restaurants)} pizza restaurants")
        
        # Get statistics
        stats = db.get_statistics()
        print(f"Total restaurants: {stats.get('total_restaurants', 0)}")
        
        # Add a new restaurant
        new_restaurant = {
            'business_id': 'test_001',
            'name': 'Test Restaurant',
            'address': '123 Test St, Test City, FL 12345',
            'phone_number': '555-1234',
            'kosher_category': 'dairy'
        }
        
        if db.add_restaurant(new_restaurant):
            print("Successfully added test restaurant")
        
        # Export data
        db.export_to_json('exported_restaurants.json', {'category': 'dairy'})
        
    finally:
        db.disconnect()

if __name__ == "__main__":
    example_usage() 