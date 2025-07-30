#!/usr/bin/env python3
"""
Deployment Schema Fix Script
This script should be run on the production server to fix the database schema.
"""

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

def get_database_url():
    """Get database URL from environment or Render configuration."""
    # Try different environment variable names
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        # Try Render-specific environment variables
        database_url = os.environ.get('RENDER_DATABASE_URL')
    
    if not database_url:
        # Try PostgreSQL-specific variables
        pg_host = os.environ.get('PGHOST')
        pg_port = os.environ.get('PGPORT', '5432')
        pg_database = os.environ.get('PGDATABASE')
        pg_user = os.environ.get('PGUSER')
        pg_password = os.environ.get('PGPASSWORD')
        
        if all([pg_host, pg_database, pg_user, pg_password]):
            database_url = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"
    
    return database_url

def fix_database_schema():
    """Fix database schema by adding missing Google reviews columns."""
    database_url = get_database_url()
    
    if not database_url:
        logger.error("No database URL found in environment variables")
        print("❌ No database URL found. Please check environment variables.")
        return False
    
    try:
        # Connect to database
        conn = psycopg2.connect(database_url)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        logger.info("Connected to database for schema fix")
        print("✅ Connected to database")
        
        # Check if columns already exist
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'restaurants' 
            AND column_name IN ('google_rating', 'google_review_count', 'google_reviews')
        """)
        
        existing_columns = [row[0] for row in cursor.fetchall()]
        logger.info("Existing Google review columns", columns=existing_columns)
        print(f"📊 Found existing columns: {existing_columns}")
        
        # Add missing columns
        columns_added = []
        
        if 'google_rating' not in existing_columns:
            logger.info("Adding google_rating column")
            cursor.execute("ALTER TABLE restaurants ADD COLUMN google_rating FLOAT")
            columns_added.append('google_rating')
            print("✅ Added google_rating column")
        
        if 'google_review_count' not in existing_columns:
            logger.info("Adding google_review_count column")
            cursor.execute("ALTER TABLE restaurants ADD COLUMN google_review_count INTEGER")
            columns_added.append('google_review_count')
            print("✅ Added google_review_count column")
        
        if 'google_reviews' not in existing_columns:
            logger.info("Adding google_reviews column")
            cursor.execute("ALTER TABLE restaurants ADD COLUMN google_reviews TEXT")
            columns_added.append('google_reviews')
            print("✅ Added google_reviews column")
        
        if columns_added:
            # Update existing records to have default values
            logger.info("Updating existing records with default values")
            cursor.execute("""
                UPDATE restaurants 
                SET google_rating = rating,
                    google_review_count = review_count,
                    google_reviews = '[]'
                WHERE google_rating IS NULL 
                   OR google_review_count IS NULL 
                   OR google_reviews IS NULL
            """)
            print("✅ Updated existing records with default values")
        else:
            print("ℹ️  All required columns already exist")
        
        # Verify the changes
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'restaurants' 
            AND column_name IN ('google_rating', 'google_review_count', 'google_reviews')
            ORDER BY column_name
        """)
        
        columns = cursor.fetchall()
        logger.info("Schema fix completed", columns=columns)
        print(f"📋 Final schema: {columns}")
        
        # Test a query to make sure everything works
        cursor.execute("SELECT id, name, google_rating, google_review_count FROM restaurants LIMIT 1")
        result = cursor.fetchone()
        logger.info("Test query successful", result=result)
        print("✅ Test query successful")
        
        cursor.close()
        conn.close()
        
        logger.info("Database schema fix completed successfully")
        print("🎉 Database schema fix completed successfully!")
        return True
        
    except Exception as e:
        logger.error("Failed to fix database schema", error=str(e))
        print(f"❌ Failed to fix database schema: {str(e)}")
        return False

def check_database_health():
    """Check if the database is working properly after the fix."""
    database_url = get_database_url()
    
    if not database_url:
        print("❌ No database URL found for health check")
        return False
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT COUNT(*) FROM restaurants")
        count = cursor.fetchone()[0]
        print(f"📊 Total restaurants in database: {count}")
        
        # Test Google reviews query
        cursor.execute("SELECT id, name, google_rating, google_review_count FROM restaurants LIMIT 5")
        results = cursor.fetchall()
        print(f"✅ Google reviews query successful - found {len(results)} restaurants")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Database health check failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Deploying database schema fix...")
    print("=" * 50)
    
    if fix_database_schema():
        print("\n🔍 Running health check...")
        if check_database_health():
            print("\n🎉 Deployment successful! Database is ready.")
        else:
            print("\n⚠️  Schema fix completed but health check failed.")
    else:
        print("\n❌ Deployment failed!") 