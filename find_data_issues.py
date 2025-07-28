#!/usr/bin/env python3
"""
Find Restaurant Data Issues
Identifies restaurants with missing or incorrect information
"""

import sqlite3
from typing import Dict, List

class RestaurantIssueFinder:
    def __init__(self, db_path: str = "restaurants.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        
    def find_restaurants_with_issues(self) -> Dict[str, List[Dict]]:
        """Find restaurants with various data quality issues"""
        cursor = self.conn.cursor()
        
        issues = {
            "invalid_websites": [],
            "missing_hours": [],
            "missing_phone": [],
            "missing_description": [],
            "missing_image": [],
            "hours_inconsistency": []
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
                issues["invalid_websites"].append(restaurant_dict)
            
            # Check for missing hours
            if (not restaurant['hours_of_operation'] or 
                restaurant['hours_of_operation'] == 'Hours not available'):
                issues["missing_hours"].append(restaurant_dict)
            
            # Check for missing phone
            if not restaurant['phone_number']:
                issues["missing_phone"].append(restaurant_dict)
            
            # Check for missing description
            if (not restaurant['short_description'] or 
                len(restaurant['short_description']) < 50):
                issues["missing_description"].append(restaurant_dict)
            
            # Check for missing image
            if not restaurant['image_url']:
                issues["missing_image"].append(restaurant_dict)
            
            # Check for hours inconsistency
            if (restaurant['hours_of_operation'] and restaurant['hours_open'] and
                restaurant['hours_of_operation'] != restaurant['hours_open']):
                issues["hours_inconsistency"].append(restaurant_dict)
        
        return issues
    
    def print_issue_report(self, issues: Dict[str, List[Dict]]):
        """Print a detailed report of found issues"""
        print("🔍 Restaurant Data Quality Issues Report")
        print("=" * 60)
        
        total_issues = sum(len(restaurants) for restaurants in issues.values())
        print(f"📊 Total restaurants with issues: {total_issues}")
        print()
        
        for issue_type, restaurants in issues.items():
            if restaurants:
                print(f"❌ {issue_type.replace('_', ' ').title()}: {len(restaurants)} restaurants")
                for restaurant in restaurants[:5]:  # Show first 5
                    print(f"   - {restaurant['name']} (ID: {restaurant['id']})")
                    if issue_type == "invalid_websites":
                        print(f"     Website: {restaurant['website']}")
                    elif issue_type == "missing_hours":
                        print(f"     Hours: {restaurant['hours_of_operation']}")
                    elif issue_type == "hours_inconsistency":
                        print(f"     hours_of_operation: {restaurant['hours_of_operation']}")
                        print(f"     hours_open: {restaurant['hours_open']}")
                if len(restaurants) > 5:
                    print(f"   ... and {len(restaurants) - 5} more")
                print()
        
        # Show specific examples
        print("📋 Specific Examples:")
        print("-" * 30)
        
        if issues["invalid_websites"]:
            example = issues["invalid_websites"][0]
            print(f"🚫 Invalid Website Example:")
            print(f"   Restaurant: {example['name']}")
            print(f"   Current Website: {example['website']}")
            print(f"   Google Search: https://www.google.com/search?q={example['name']} restaurant {example['city']} {example['state']}")
            print()
        
        if issues["missing_hours"]:
            example = issues["missing_hours"][0]
            print(f"⏰ Missing Hours Example:")
            print(f"   Restaurant: {example['name']}")
            print(f"   Current Hours: {example['hours_of_operation']}")
            print(f"   Google Search: https://www.google.com/search?q={example['name']} hours {example['city']} {example['state']}")
            print()
    
    def generate_update_suggestions(self, issues: Dict[str, List[Dict]]) -> str:
        """Generate suggestions for updating restaurant data"""
        suggestions = []
        suggestions.append("# Restaurant Data Update Suggestions")
        suggestions.append("Based on Google Knowledge Graph validation")
        suggestions.append("")
        
        if issues["invalid_websites"]:
            suggestions.append("## Website Updates Needed")
            suggestions.append("The following restaurants have invalid or Google search URLs as websites:")
            suggestions.append("")
            for restaurant in issues["invalid_websites"][:10]:  # Top 10
                search_query = f"{restaurant['name']} restaurant {restaurant['city']} {restaurant['state']}"
                suggestions.append(f"### {restaurant['name']} (ID: {restaurant['id']})")
                suggestions.append(f"- Current: {restaurant['website']}")
                suggestions.append(f"- Google Search: https://www.google.com/search?q={search_query}")
                suggestions.append(f"- Action: Check Google Knowledge Graph for official website")
                suggestions.append("")
        
        if issues["missing_hours"]:
            suggestions.append("## Hours Updates Needed")
            suggestions.append("The following restaurants are missing hours information:")
            suggestions.append("")
            for restaurant in issues["missing_hours"][:10]:  # Top 10
                search_query = f"{restaurant['name']} hours {restaurant['city']} {restaurant['state']}"
                suggestions.append(f"### {restaurant['name']} (ID: {restaurant['id']})")
                suggestions.append(f"- Current: {restaurant['hours_of_operation']}")
                suggestions.append(f"- Google Search: https://www.google.com/search?q={search_query}")
                suggestions.append(f"- Action: Check Google Knowledge Graph for business hours")
                suggestions.append("")
        
        if issues["missing_description"]:
            suggestions.append("## Description Updates Needed")
            suggestions.append("The following restaurants need better descriptions:")
            suggestions.append("")
            for restaurant in issues["missing_description"][:10]:  # Top 10
                search_query = f"{restaurant['name']} restaurant {restaurant['city']} {restaurant['state']}"
                suggestions.append(f"### {restaurant['name']} (ID: {restaurant['id']})")
                suggestions.append(f"- Current: {restaurant['short_description'][:100]}...")
                suggestions.append(f"- Google Search: https://www.google.com/search?q={search_query}")
                suggestions.append(f"- Action: Check Google Knowledge Graph for business description")
                suggestions.append("")
        
        return "\n".join(suggestions)
    
    def close(self):
        """Close database connection"""
        self.conn.close()

def main():
    """Main function to find and report issues"""
    finder = RestaurantIssueFinder()
    
    try:
        print("🔍 Finding Restaurant Data Issues...")
        print("=" * 60)
        
        # Find issues
        issues = finder.find_restaurants_with_issues()
        
        # Print report
        finder.print_issue_report(issues)
        
        # Generate suggestions
        suggestions = finder.generate_update_suggestions(issues)
        
        # Save suggestions
        with open("restaurant_update_suggestions.md", "w") as f:
            f.write(suggestions)
        
        print("📄 Update suggestions saved to: restaurant_update_suggestions.md")
        
    except Exception as e:
        print(f"❌ Error finding issues: {e}")
    finally:
        finder.close()

if __name__ == "__main__":
    main() 