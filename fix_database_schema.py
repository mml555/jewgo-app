#!/usr/bin/env python3
"""
Fix database schema by adding missing columns to match SQLAlchemy model.
This script should be run on the deployed environment where DATABASE_URL is available.
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
import structlog

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

def get_missing_columns():
    """Get list of columns that need to be added to the database."""
    return [
        ('phone', 'TEXT'),
        ('website', 'TEXT'),
        ('cuisine_type', 'TEXT'),
        ('price_range', 'TEXT'),
        ('review_count', 'INTEGER'),
        ('description', 'TEXT'),
        ('image_url', 'TEXT'),
        ('is_kosher', 'BOOLEAN DEFAULT FALSE'),
        ('is_glatt', 'BOOLEAN DEFAULT FALSE'),
        ('is_cholov_yisroel', 'BOOLEAN DEFAULT FALSE'),
        ('is_pas_yisroel', 'BOOLEAN DEFAULT FALSE'),
        ('is_bishul_yisroel', 'BOOLEAN DEFAULT FALSE'),
        ('is_mehadrin', 'BOOLEAN DEFAULT FALSE'),
        ('is_hechsher', 'BOOLEAN DEFAULT FALSE'),
        ('hechsher_details', 'TEXT'),
        ('created_at', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'),
        ('updated_at', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
    ]

def check_and_fix_schema():
    """Check current schema and add missing columns."""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        logger.error("DATABASE_URL environment variable not found")
        return False
    
    try:
        # Connect to database
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        logger.info("Connected to database successfully")
        
        # Get current columns
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'restaurants'
            ORDER BY ordinal_position;
        """)
        
        existing_columns = [row['column_name'] for row in cursor.fetchall()]
        logger.info("Current columns", columns=existing_columns)
        
        # Get missing columns
        missing_columns = get_missing_columns()
        columns_to_add = [col for col, _ in missing_columns if col not in existing_columns]
        
        if not columns_to_add:
            logger.info("No missing columns found - schema is up to date")
            return True
        
        logger.info("Adding missing columns", columns=columns_to_add)
        
        # Add missing columns
        for column_name, column_type in missing_columns:
            if column_name not in existing_columns:
                try:
                    sql = f"ALTER TABLE restaurants ADD COLUMN {column_name} {column_type}"
                    cursor.execute(sql)
                    logger.info(f"Added column: {column_name} ({column_type})")
                except Exception as e:
                    logger.error(f"Failed to add column {column_name}", error=str(e))
                    # Continue with other columns
        
        # Commit changes
        conn.commit()
        logger.info("Schema update completed successfully")
        
        # Verify the changes
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'restaurants'
            ORDER BY ordinal_position;
        """)
        
        updated_columns = [row['column_name'] for row in cursor.fetchall()]
        logger.info("Updated columns", columns=updated_columns)
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        logger.error("Error fixing database schema", error=str(e))
        return False

def create_indexes():
    """Create useful indexes for better performance."""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        logger.error("DATABASE_URL environment variable not found")
        return False
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Create indexes for better query performance
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_restaurants_name ON restaurants(name)",
            "CREATE INDEX IF NOT EXISTS idx_restaurants_city ON restaurants(city)",
            "CREATE INDEX IF NOT EXISTS idx_restaurants_state ON restaurants(state)",
            "CREATE INDEX IF NOT EXISTS idx_restaurants_is_kosher ON restaurants(is_kosher)",
            "CREATE INDEX IF NOT EXISTS idx_restaurants_cuisine_type ON restaurants(cuisine_type)",
            "CREATE INDEX IF NOT EXISTS idx_restaurants_rating ON restaurants(rating)"
        ]
        
        for index_sql in indexes:
            try:
                cursor.execute(index_sql)
                logger.info(f"Created index: {index_sql}")
            except Exception as e:
                logger.error(f"Failed to create index: {index_sql}", error=str(e))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info("Indexes created successfully")
        return True
        
    except Exception as e:
        logger.error("Error creating indexes", error=str(e))
        return False

if __name__ == "__main__":
    print("🔧 Fixing database schema...")
    
    success = check_and_fix_schema()
    if success:
        print("✅ Schema fixed successfully!")
        
        # Create indexes for better performance
        print("🔧 Creating indexes...")
        index_success = create_indexes()
        if index_success:
            print("✅ Indexes created successfully!")
        else:
            print("⚠️  Index creation failed, but schema is fixed")
    else:
        print("❌ Schema fix failed!") 