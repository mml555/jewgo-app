#!/usr/bin/env python3
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
cursor = conn.cursor()

# Check for any remaining processed status indicators
cursor.execute("""
    SELECT COUNT(*) FROM restaurants 
    WHERE hours_of_operation LIKE '%🔴%' 
    OR hours_of_operation LIKE '%🟢%' 
    OR hours_of_operation LIKE '%⚪%'
""")
count = cursor.fetchone()[0]
print(f"Restaurants with processed status indicators: {count}")

# Show sample of current hours format
cursor.execute("""
    SELECT name, hours_of_operation 
    FROM restaurants 
    WHERE hours_of_operation IS NOT NULL 
    LIMIT 3
""")
rows = cursor.fetchall()
print("\nSample hours format:")
for row in rows:
    print(f"  {row[0]}: {row[1]}")

conn.close() 