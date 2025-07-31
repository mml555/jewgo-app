#!/usr/bin/env python3
"""
Test Reviews System
Demonstrates the Google and Yelp reviews integration
"""

import sqlite3
import json
import os

def test_reviews_system():
    """Test the reviews system with sample data"""
    
    print("🔍 Testing Reviews System")
    print("=" * 50)
    
    # Connect to database
    conn = sqlite3.connect("restaurants.db")
    cursor = conn.cursor()
    
    # Get restaurants with Google reviews
    cursor.execute("""
        SELECT name, google_rating, google_review_count, google_reviews
        FROM restaurants 
        WHERE google_rating > 0 
        ORDER BY google_rating DESC 
        LIMIT 3
    """)
    
    restaurants = cursor.fetchall()
    
    if not restaurants:
        print("❌ No restaurants with Google reviews found")
        print("💡 Run the Google reviews fetcher first:")
        print("   python enhanced_google_reviews_fetcher.py")
        return
    
    print(f"✅ Found {len(restaurants)} restaurants with Google reviews")
    print()
    
    for i, (name, rating, review_count, reviews_json) in enumerate(restaurants, 1):
        print(f"🏪 {i}. {name}")
        print(f"   ⭐ Google Rating: {rating}/5.0")
        print(f"   📊 Total Reviews: {review_count}")
        
        if reviews_json:
            try:
                reviews = json.loads(reviews_json)
                print(f"   📝 Sample Reviews: {len(reviews)} available")
                
                # Show first review
                if reviews:
                    first_review = reviews[0]
                    author = first_review.get('author_name', 'Anonymous')
                    text = first_review.get('text', '')[:100] + "..." if len(first_review.get('text', '')) > 100 else first_review.get('text', '')
                    print(f"   👤 Sample: \"{text}\" - {author}")
                
            except json.JSONDecodeError:
                print("   ❌ Error parsing reviews JSON")
        else:
            print("   📝 No review text available")
        
        print()
    
    # Summary
    cursor.execute("""
        SELECT COUNT(*) 
        FROM restaurants 
        WHERE google_rating > 0
    """)
    
    google_count = cursor.fetchone()[0]
    
    print(f"📊 Summary: {google_count} restaurants have Google reviews")
    print("💡 To add more Google reviews:")
    print("   python enhanced_google_reviews_fetcher.py")
    
    print()
    print("🎯 Frontend Integration:")
    print("   • Visit: http://localhost:3000")
    print("   • Click on any restaurant with reviews")
    print("   • Look for the 'Reviews & Ratings' section")
    print("   • View Google reviews and ratings")
    
    print()
    print("📊 Database Schema:")
    print("   • google_rating: REAL (1.0-5.0)")
    print("   • google_review_count: INTEGER")
    print("   • google_reviews: TEXT (JSON)")
    
    conn.close()

def show_api_response():
    """Show what the API returns for reviews"""
    
    print("\n🌐 API Response Example:")
    print("=" * 50)
    
    import requests
    
    try:
        response = requests.get("http://localhost:8081/api/restaurants?limit=1")
        if response.status_code == 200:
            data = response.json()
            restaurant = data['restaurants'][0]
            
            print("📡 API Response Structure:")
            print(json.dumps({
                'name': restaurant.get('name'),
                'google_rating': restaurant.get('google_rating'),
                'google_review_count': restaurant.get('google_review_count'),
                'google_reviews': f"JSON string ({len(restaurant.get('google_reviews', ''))} chars)" if restaurant.get('google_reviews') else None
            }, indent=2))
        else:
            print(f"❌ API Error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Backend server not running")
        print("💡 Start the backend: python app.py")

if __name__ == "__main__":
    test_reviews_system()
    show_api_response() 