#!/usr/bin/env python3
"""
Restaurant Data Validation Tool
Validates restaurant data against Google Knowledge Graph and identifies missing/incorrect information
"""

import sqlite3
import json
import time
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote_plus

class RestaurantDataValidator:
    def __init__(self, db_path: str = "restaurants.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        
    def get_restaurants_for_validation(self, limit: int = 10) -> List[Dict]:
        """Get restaurants that need validation"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, name, website, hours_of_operation, hours_open, 
                   phone_number, address, city, state, zip_code, 
                   image_url, short_description
            FROM restaurants 
            WHERE status = 'active'
            ORDER BY id
            LIMIT ?
        """, (limit,))
        
        restaurants = []
        for row in cursor.fetchall():
            restaurants.append(dict(row))
        
        return restaurants
    
    def search_google_knowledge_graph(self, restaurant_name: str, city: str, state: str) -> Optional[Dict]:
        """Search Google Knowledge Graph for restaurant information"""
        try:
            # Create search query
            search_query = f"{restaurant_name} restaurant {city} {state}"
            encoded_query = quote_plus(search_query)
            
            # Google search URL (this would need to be enhanced with actual API calls)
            search_url = f"https://www.google.com/search?q={encoded_query}"
            
            print(f"🔍 Searching: {search_query}")
            print(f"📎 URL: {search_url}")
            
            # For now, return a mock response structure
            # In a real implementation, you'd use Google's Knowledge Graph API
            return {
                "search_query": search_query,
                "search_url": search_url,
                "found": True,
                "data_quality": "mock"
            }
            
        except Exception as e:
            print(f"❌ Error searching Google Knowledge Graph: {e}")
            return None
    
    def analyze_data_quality(self, restaurant: Dict) -> Dict:
        """Analyze the quality of restaurant data"""
        issues = []
        missing_fields = []
        potential_improvements = []
        
        # Check for missing website
        if not restaurant.get('website') or restaurant['website'] in ['null', '', 'http://Www.google.com']:
            missing_fields.append('website')
            issues.append("Missing or invalid website")
        
        # Check for missing hours
        if not restaurant.get('hours_of_operation') or restaurant['hours_of_operation'] == 'Hours not available':
            missing_fields.append('hours_of_operation')
            issues.append("Missing hours of operation")
        
        # Check for missing phone
        if not restaurant.get('phone_number'):
            missing_fields.append('phone_number')
            issues.append("Missing phone number")
        
        # Check for missing description
        if not restaurant.get('short_description') or len(restaurant.get('short_description', '')) < 50:
            missing_fields.append('short_description')
            issues.append("Missing or incomplete description")
        
        # Check for missing image
        if not restaurant.get('image_url'):
            missing_fields.append('image_url')
            issues.append("Missing restaurant image")
        
        # Check for inconsistent hours format
        if restaurant.get('hours_of_operation') and restaurant.get('hours_open'):
            if restaurant['hours_of_operation'] != restaurant['hours_open']:
                potential_improvements.append("Hours format inconsistency between hours_of_operation and hours_open")
        
        # Check for generic website URLs
        if restaurant.get('website') and 'google.com' in restaurant['website'].lower():
            issues.append("Website appears to be a Google search result, not actual website")
        
        return {
            "restaurant_id": restaurant['id'],
            "restaurant_name": restaurant['name'],
            "issues": issues,
            "missing_fields": missing_fields,
            "potential_improvements": potential_improvements,
            "data_quality_score": max(0, 100 - (len(issues) * 20))
        }
    
    def validate_restaurants(self, limit: int = 10) -> List[Dict]:
        """Validate multiple restaurants and return analysis"""
        restaurants = self.get_restaurants_for_validation(limit)
        validation_results = []
        
        print(f"🔍 Validating {len(restaurants)} restaurants...")
        print("=" * 60)
        
        for restaurant in restaurants:
            print(f"\n📍 {restaurant['name']} (ID: {restaurant['id']})")
            
            # Analyze data quality
            quality_analysis = self.analyze_data_quality(restaurant)
            validation_results.append(quality_analysis)
            
            # Search Google Knowledge Graph
            if restaurant.get('city') and restaurant.get('state'):
                kg_result = self.search_google_knowledge_graph(
                    restaurant['name'], 
                    restaurant['city'], 
                    restaurant['state']
                )
                quality_analysis['google_kg_result'] = kg_result
            
            # Print analysis
            if quality_analysis['issues']:
                print(f"❌ Issues: {', '.join(quality_analysis['issues'])}")
            else:
                print("✅ No major issues found")
            
            if quality_analysis['potential_improvements']:
                print(f"⚠️  Improvements: {', '.join(quality_analysis['potential_improvements'])}")
            
            print(f"📊 Data Quality Score: {quality_analysis['data_quality_score']}/100")
            
            # Add delay to avoid rate limiting
            time.sleep(1)
        
        return validation_results
    
    def generate_validation_report(self, validation_results: List[Dict]) -> str:
        """Generate a comprehensive validation report"""
        report = []
        report.append("# Restaurant Data Validation Report")
        report.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Restaurants Analyzed: {len(validation_results)}")
        report.append("")
        
        # Summary statistics
        total_issues = sum(len(result['issues']) for result in validation_results)
        avg_quality_score = sum(result['data_quality_score'] for result in validation_results) / len(validation_results)
        
        report.append("## Summary")
        report.append(f"- Total Issues Found: {total_issues}")
        report.append(f"- Average Data Quality Score: {avg_quality_score:.1f}/100")
        report.append("")
        
        # Detailed results
        report.append("## Detailed Results")
        for result in validation_results:
            report.append(f"### {result['restaurant_name']} (ID: {result['restaurant_id']})")
            report.append(f"- Quality Score: {result['data_quality_score']}/100")
            
            if result['issues']:
                report.append("- Issues:")
                for issue in result['issues']:
                    report.append(f"  - {issue}")
            
            if result['potential_improvements']:
                report.append("- Potential Improvements:")
                for improvement in result['potential_improvements']:
                    report.append(f"  - {improvement}")
            
            if result.get('google_kg_result'):
                report.append(f"- Google Knowledge Graph: {result['google_kg_result']['search_url']}")
            
            report.append("")
        
        return "\n".join(report)
    
    def close(self):
        """Close database connection"""
        self.conn.close()

def main():
    """Main function to run validation"""
    validator = RestaurantDataValidator()
    
    try:
        print("🚀 Starting Restaurant Data Validation")
        print("=" * 60)
        
        # Validate restaurants
        validation_results = validator.validate_restaurants(limit=5)
        
        # Generate report
        report = validator.generate_validation_report(validation_results)
        
        # Save report
        with open("restaurant_validation_report.md", "w") as f:
            f.write(report)
        
        print("\n" + "=" * 60)
        print("✅ Validation Complete!")
        print("📄 Report saved to: restaurant_validation_report.md")
        
        # Print summary
        total_issues = sum(len(result['issues']) for result in validation_results)
        avg_score = sum(result['data_quality_score'] for result in validation_results) / len(validation_results)
        
        print(f"\n📊 Summary:")
        print(f"- Restaurants analyzed: {len(validation_results)}")
        print(f"- Total issues found: {total_issues}")
        print(f"- Average quality score: {avg_score:.1f}/100")
        
    except Exception as e:
        print(f"❌ Error during validation: {e}")
    finally:
        validator.close()

if __name__ == "__main__":
    main() 