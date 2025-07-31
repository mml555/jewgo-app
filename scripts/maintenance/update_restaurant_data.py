#!/usr/bin/env python3
"""
Restaurant Data Update Tool
Updates restaurant data with missing information from Google Knowledge Graph
"""

import sqlite3
import time
from typing import Dict, List, Optional
from urllib.parse import quote_plus

class RestaurantDataUpdater:
    def __init__(self, db_path: str = "restaurants.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        
    def get_restaurants_needing_updates(self) -> Dict[str, List[Dict]]:
        """Get restaurants that need specific updates"""
        cursor = self.conn.cursor()
        
        updates_needed = {
            "invalid_websites": [],
            "missing_hours": [],
            "missing_phone": [],
            "missing_description": [],
            "missing_image": []
        }
        
        # Get all active restaurants
        cursor.execute("""
            SELECT id, name, website, hours_of_operation, hours_open, 
                   phone_number, address, city, state, zip_code, 
                   image_url, short_description
            FROM restaurants 
            WHERE status = 'active'
            ORDER BY id
        """)
        
        restaurants = cursor.fetchall()
        
        for restaurant in restaurants:
            restaurant_dict = dict(restaurant)
            
            # Check for invalid websites
            if (restaurant['website'] and 
                ('google.com' in restaurant['website'].lower() or 
                 restaurant['website'] in ['null', ''])):
                updates_needed["invalid_websites"].append(restaurant_dict)
            
            # Check for missing hours
            if (not restaurant['hours_of_operation'] or 
                restaurant['hours_of_operation'] == 'Hours not available' or
                restaurant['hours_of_operation'] == 'None'):
                updates_needed["missing_hours"].append(restaurant_dict)
            
            # Check for missing phone
            if not restaurant['phone_number']:
                updates_needed["missing_phone"].append(restaurant_dict)
            
            # Check for missing description
            if (not restaurant['short_description'] or 
                len(restaurant['short_description']) < 50 or
                'Authentic Kosher Restaurant' in restaurant['short_description']):
                updates_needed["missing_description"].append(restaurant_dict)
            
            # Check for missing image
            if not restaurant['image_url']:
                updates_needed["missing_image"].append(restaurant_dict)
        
        return updates_needed
    
    def generate_google_search_url(self, restaurant: Dict, search_type: str = "general") -> str:
        """Generate Google search URL for restaurant information"""
        name = restaurant['name']
        city = restaurant.get('city', '')
        state = restaurant.get('state', '')
        
        if search_type == "hours":
            query = f"{name} hours {city} {state}"
        elif search_type == "phone":
            query = f"{name} phone number {city} {state}"
        elif search_type == "website":
            query = f"{name} official website {city} {state}"
        else:
            query = f"{name} restaurant {city} {state}"
        
        encoded_query = quote_plus(query)
        return f"https://www.google.com/search?q={encoded_query}"
    
    def update_restaurant_website(self, restaurant_id: int, new_website: str) -> bool:
        """Update restaurant website"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE restaurants 
                SET website = ? 
                WHERE id = ?
            """, (new_website, restaurant_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"❌ Error updating website for restaurant {restaurant_id}: {e}")
            return False
    
    def update_restaurant_hours(self, restaurant_id: int, new_hours: str) -> bool:
        """Update restaurant hours"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE restaurants 
                SET hours_of_operation = ?, hours_open = ? 
                WHERE id = ?
            """, (new_hours, new_hours, restaurant_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"❌ Error updating hours for restaurant {restaurant_id}: {e}")
            return False
    
    def update_restaurant_phone(self, restaurant_id: int, new_phone: str) -> bool:
        """Update restaurant phone number"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE restaurants 
                SET phone_number = ? 
                WHERE id = ?
            """, (new_phone, restaurant_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"❌ Error updating phone for restaurant {restaurant_id}: {e}")
            return False
    
    def update_restaurant_description(self, restaurant_id: int, new_description: str) -> bool:
        """Update restaurant description"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE restaurants 
                SET short_description = ? 
                WHERE id = ?
            """, (new_description, restaurant_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"❌ Error updating description for restaurant {restaurant_id}: {e}")
            return False
    
    def update_restaurant_image(self, restaurant_id: int, new_image_url: str) -> bool:
        """Update restaurant image URL"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE restaurants 
                SET image_url = ? 
                WHERE id = ?
            """, (new_image_url, restaurant_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"❌ Error updating image for restaurant {restaurant_id}: {e}")
            return False
    
    def print_update_plan(self, updates_needed: Dict[str, List[Dict]]):
        """Print a plan for updating restaurant data"""
        print("🔄 Restaurant Data Update Plan")
        print("=" * 60)
        
        total_updates = sum(len(restaurants) for restaurants in updates_needed.values())
        print(f"📊 Total updates needed: {total_updates}")
        print()
        
        for update_type, restaurants in updates_needed.items():
            if restaurants:
                print(f"🔧 {update_type.replace('_', ' ').title()}: {len(restaurants)} restaurants")
                for restaurant in restaurants[:3]:  # Show first 3
                    print(f"   - {restaurant['name']} (ID: {restaurant['id']})")
                    if update_type == "invalid_websites":
                        print(f"     Current: {restaurant['website']}")
                        print(f"     Search: {self.generate_google_search_url(restaurant, 'website')}")
                    elif update_type == "missing_hours":
                        print(f"     Current: {restaurant['hours_of_operation']}")
                        print(f"     Search: {self.generate_google_search_url(restaurant, 'hours')}")
                    elif update_type == "missing_phone":
                        print(f"     Current: {restaurant['phone_number']}")
                        print(f"     Search: {self.generate_google_search_url(restaurant, 'phone')}")
                if len(restaurants) > 3:
                    print(f"   ... and {len(restaurants) - 3} more")
                print()
    
    def generate_update_instructions(self, updates_needed: Dict[str, List[Dict]]) -> str:
        """Generate detailed update instructions"""
        instructions = []
        instructions.append("# Restaurant Data Update Instructions")
        instructions.append("Manual updates needed based on Google Knowledge Graph research")
        instructions.append("")
        
        for update_type, restaurants in updates_needed.items():
            if restaurants:
                instructions.append(f"## {update_type.replace('_', ' ').title()}")
                instructions.append(f"Total restaurants: {len(restaurants)}")
                instructions.append("")
                
                for restaurant in restaurants[:20]:  # Top 20
                    instructions.append(f"### {restaurant['name']} (ID: {restaurant['id']})")
                    
                    if update_type == "invalid_websites":
                        instructions.append(f"- **Current Website**: {restaurant['website']}")
                        instructions.append(f"- **Google Search**: {self.generate_google_search_url(restaurant, 'website')}")
                        instructions.append("- **Action**: Find official website from Google Knowledge Graph")
                        instructions.append("- **Update Command**: `update_restaurant_website({restaurant['id']}, 'new_website_url')`")
                    
                    elif update_type == "missing_hours":
                        instructions.append(f"- **Current Hours**: {restaurant['hours_of_operation']}")
                        instructions.append(f"- **Google Search**: {self.generate_google_search_url(restaurant, 'hours')}")
                        instructions.append("- **Action**: Find business hours from Google Knowledge Graph")
                        instructions.append("- **Update Command**: `update_restaurant_hours({restaurant['id']}, 'new_hours')`")
                    
                    elif update_type == "missing_phone":
                        instructions.append(f"- **Current Phone**: {restaurant['phone_number']}")
                        instructions.append(f"- **Google Search**: {self.generate_google_search_url(restaurant, 'phone')}")
                        instructions.append("- **Action**: Find phone number from Google Knowledge Graph")
                        instructions.append("- **Update Command**: `update_restaurant_phone({restaurant['id']}, 'new_phone')`")
                    
                    elif update_type == "missing_description":
                        current_desc = restaurant['short_description'][:100] + "..." if len(restaurant['short_description']) > 100 else restaurant['short_description']
                        instructions.append(f"- **Current Description**: {current_desc}")
                        instructions.append(f"- **Google Search**: {self.generate_google_search_url(restaurant)}")
                        instructions.append("- **Action**: Find detailed description from Google Knowledge Graph")
                        instructions.append("- **Update Command**: `update_restaurant_description({restaurant['id']}, 'new_description')`")
                    
                    elif update_type == "missing_image":
                        instructions.append(f"- **Current Image**: {restaurant['image_url']}")
                        instructions.append(f"- **Google Search**: {self.generate_google_search_url(restaurant)}")
                        instructions.append("- **Action**: Find restaurant image from Google Places")
                        instructions.append("- **Update Command**: `update_restaurant_image({restaurant['id']}, 'new_image_url')`")
                    
                    instructions.append("")
        
        return "\n".join(instructions)
    
    def close(self):
        """Close database connection"""
        self.conn.close()

def main():
    """Main function to generate update plan"""
    updater = RestaurantDataUpdater()
    
    try:
        print("🔄 Generating Restaurant Data Update Plan...")
        print("=" * 60)
        
        # Get restaurants needing updates
        updates_needed = updater.get_restaurants_needing_updates()
        
        # Print update plan
        updater.print_update_plan(updates_needed)
        
        # Generate detailed instructions
        instructions = updater.generate_update_instructions(updates_needed)
        
        # Save instructions
        with open("restaurant_update_instructions.md", "w") as f:
            f.write(instructions)
        
        print("📄 Detailed instructions saved to: restaurant_update_instructions.md")
        print("\n🚀 Ready to start manual updates!")
        print("💡 Use the generated Google search URLs to find correct information")
        
    except Exception as e:
        print(f"❌ Error generating update plan: {e}")
    finally:
        updater.close()

if __name__ == "__main__":
    main() 