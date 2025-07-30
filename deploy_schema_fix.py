#!/usr/bin/env python3
"""
Deploy schema fix to add missing columns to the database.
This script should be run on the deployed environment.
"""

import os
import psycopg2
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

def fix_database_schema():
    """Add missing columns to the restaurants table."""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL environment variable not found")
        return False
    
    try:
        # Connect to database
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("🔧 Connected to database successfully")
        
        # SQL statements to add missing columns
        alter_statements = [
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS phone TEXT",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS website TEXT",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS cuisine_type TEXT",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS price_range TEXT",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS review_count INTEGER",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS description TEXT",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS image_url TEXT",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS is_kosher BOOLEAN DEFAULT FALSE",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS is_glatt BOOLEAN DEFAULT FALSE",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS is_cholov_yisroel BOOLEAN DEFAULT FALSE",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS is_pas_yisroel BOOLEAN DEFAULT FALSE",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS is_bishul_yisroel BOOLEAN DEFAULT FALSE",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS is_mehadrin BOOLEAN DEFAULT FALSE",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS is_hechsher BOOLEAN DEFAULT FALSE",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS hechsher_details TEXT",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        ]
        
        # Execute each ALTER statement
        for sql in alter_statements:
            try:
                cursor.execute(sql)
                print(f"✅ Executed: {sql}")
            except Exception as e:
                print(f"⚠️  Warning: {sql} - {e}")
        
        # Commit changes
        conn.commit()
        print("✅ Schema update completed successfully")
        
        # Verify the table structure
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'restaurants'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        print(f"\n📋 Current table structure ({len(columns)} columns):")
        for col_name, col_type in columns:
            print(f"  {col_name:<25} {col_type}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing database schema: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Fixing database schema...")
    success = fix_database_schema()
    
    if success:
        print("\n🎉 Database schema fixed successfully!")
        print("Your Flask API should now work without column errors.")
    else:
        print("\n❌ Failed to fix database schema.") 