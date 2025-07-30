#!/usr/bin/env python3
"""
Add dummy Google reviews data to test frontend rendering
"""

import os
import json
import psycopg2
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_dummy_reviews_data():
    """Add dummy Google reviews data to restaurants for testing."""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        logger.error("DATABASE_URL environment variable not found")
        return False
    
    try:
        # Connect to database
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        logger.info("Connected to database for adding dummy reviews")
        
        # Sample dummy reviews data
        dummy_reviews = [
            {
                "author_name": "Sarah Cohen",
                "author_url": "https://www.google.com/maps/contrib/123456789",
                "language": "en",
                "original_language": "en",
                "profile_photo_url": "https://lh3.googleusercontent.com/a/default-user",
                "rating": 5,
                "relative_time_description": "2 weeks ago",
                "text": "Amazing kosher food! The service was excellent and the atmosphere was perfect for our family dinner. Highly recommend!",
                "time": int(datetime.now().timestamp()),
                "translated": False
            },
            {
                "author_name": "David Goldstein",
                "author_url": "https://www.google.com/maps/contrib/987654321",
                "language": "en",
                "original_language": "en",
                "profile_photo_url": "https://lh3.googleusercontent.com/a/default-user",
                "rating": 4,
                "relative_time_description": "1 month ago",
                "text": "Great food and reasonable prices. The staff was friendly and the restaurant was clean. Will definitely come back!",
                "time": int(datetime.now().timestamp()),
                "translated": False
            },
            {
                "author_name": "Rachel Schwartz",
                "author_url": "https://www.google.com/maps/contrib/456789123",
                "language": "en",
                "original_language": "en",
                "profile_photo_url": "https://lh3.googleusercontent.com/a/default-user",
                "rating": 5,
                "relative_time_description": "3 weeks ago",
                "text": "Best kosher restaurant in the area! The food is always fresh and delicious. Love the variety of options.",
                "time": int(datetime.now().timestamp()),
                "translated": False
            }
        ]
        
        # Convert to JSON string
        reviews_json = json.dumps(dummy_reviews)
        
        # Update restaurants with dummy reviews data
        update_sql = """
        UPDATE restaurants 
        SET google_rating = %s, 
            google_review_count = %s, 
            google_reviews = %s
        WHERE id IN (
            SELECT id FROM restaurants 
            WHERE (google_reviews IS NULL OR google_reviews = '') 
            AND status = 'active'
            LIMIT 10
        )
        """
        
        cursor.execute(update_sql, (4.5, len(dummy_reviews), reviews_json))
        
        # Get count of updated records
        cursor.execute("SELECT COUNT(*) FROM restaurants WHERE google_reviews IS NOT NULL AND google_reviews != ''")
        updated_count = cursor.fetchone()[0]
        
        # Commit changes
        conn.commit()
        logger.info(f"Added dummy reviews data to {updated_count} restaurants")
        
        # Close connection
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        logger.error(f"Error adding dummy reviews data: {e}")
        return False

if __name__ == "__main__":
    success = add_dummy_reviews_data()
    if success:
        print("✅ Successfully added dummy reviews data")
    else:
        print("❌ Failed to add dummy reviews data") 