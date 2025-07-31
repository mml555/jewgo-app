#!/usr/bin/env python3
"""
Check and create database tables.
"""

import os
from sqlalchemy import create_engine, text, inspect
from database_manager_v2 import Base, Restaurant

def check_and_create_tables():
    """Check what tables exist and create missing ones."""
    
    # Set up database URL
    database_url = "postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    
    # Create engine
    engine = create_engine(database_url)
    
    try:
        # Connect and check existing tables
        with engine.connect() as conn:
            # Check what tables exist
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
            print(f"Existing tables: {existing_tables}")
            
            # Check if restaurants table exists
            if 'restaurants' in existing_tables:
                print("✅ restaurants table already exists")
                
                # Check the structure
                columns = inspector.get_columns('restaurants')
                print(f"restaurants table has {len(columns)} columns:")
                for col in columns:
                    print(f"  - {col['name']}: {col['type']}")
            else:
                print("❌ restaurants table does not exist, creating it...")
                
                # Create all tables
                Base.metadata.create_all(bind=engine)
                print("✅ restaurants table created successfully")
                
                # Verify it was created
                inspector = inspect(engine)
                tables_after = inspector.get_table_names()
                print(f"Tables after creation: {tables_after}")
                
                if 'restaurants' in tables_after:
                    print("✅ restaurants table confirmed to exist")
                else:
                    print("❌ restaurants table still not found after creation")
                    
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Checking and creating database tables...")
    success = check_and_create_tables()
    if success:
        print("✅ Database setup completed successfully")
    else:
        print("❌ Database setup failed") 