#!/usr/bin/env python3
"""
Check Database Schema Script
===========================

This script connects to the database and checks the actual schema
to understand the column types and constraints.
"""

import os
import sys
from sqlalchemy import create_engine, text

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from config.config import get_config

def check_schema():
    """Check the database schema."""
    config = get_config()
    
    # Create engine
    engine = create_engine(config.DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # Get table information
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'restaurants'
                ORDER BY ordinal_position;
            """))
            
            print("Database Schema for 'restaurants' table:")
            print("=" * 60)
            
            for row in result:
                print(f"{row[0]:<25} {row[1]:<15} {'NULL' if row[2] == 'YES' else 'NOT NULL':<10} {row[3] or ''}")
                
    except Exception as e:
        print(f"Error checking schema: {e}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    check_schema() 