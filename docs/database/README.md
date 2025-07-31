# Database Guide

## Overview

This guide covers the database architecture, schema, and management for the JewGo application.

## 🗄️ Database Architecture

### Technology Stack
- **Database**: PostgreSQL (Neon)
- **ORM**: SQLAlchemy 1.4
- **Connection**: Connection pooling with psycopg2
- **Backup**: Automated backups via Neon

### Database Schema
The application uses a single consolidated `restaurants` table with 28 optimized columns for kosher restaurant data.

## 📊 Schema Overview

### Core Restaurant Information
```sql
-- Primary identification
id INTEGER PRIMARY KEY
name VARCHAR(255) NOT NULL

-- Location information
address VARCHAR(500)
city VARCHAR(100)
state VARCHAR(50)
zip_code VARCHAR(20)
latitude FLOAT
longitude FLOAT

-- Contact information
phone VARCHAR(50)
website VARCHAR(500)
email VARCHAR(255)
```

### Business Details
```sql
-- Business information
price_range VARCHAR(20)  -- $, $$, $$$, $$$$
image_url VARCHAR(500)
hours_open TEXT
category VARCHAR(100) DEFAULT 'restaurant'
status VARCHAR(50) DEFAULT 'approved'
```

### Kosher Supervision
```sql
-- Kosher status flags
is_kosher BOOLEAN DEFAULT FALSE
is_glatt BOOLEAN DEFAULT FALSE
is_cholov_yisroel BOOLEAN DEFAULT FALSE
is_pas_yisroel BOOLEAN DEFAULT FALSE
is_bishul_yisroel BOOLEAN DEFAULT FALSE
is_mehadrin BOOLEAN DEFAULT FALSE
is_hechsher BOOLEAN DEFAULT FALSE

-- Kosher categorization
kosher_type VARCHAR(100)  -- dairy, meat, pareve
```

### ORB Integration
```sql
-- ORB certification details
kosher_cert_link VARCHAR(500)
detail_url VARCHAR(500)
short_description TEXT
google_listing_url VARCHAR(500)
```

### Audit Trail
```sql
-- Timestamps
created_at TIMESTAMP DEFAULT NOW()
updated_at TIMESTAMP DEFAULT NOW()
```

## 📈 Current Data Statistics

- **Total Restaurants**: 107
- **Dairy Restaurants**: 99
- **Pareve Restaurants**: 8
- **Chalav Yisroel**: 104
- **Pas Yisroel**: 22
- **Glatt Kosher**: Various
- **Mehadrin**: Various

## 🔧 Database Management

### Connection Management
```python
# Database URL format
DATABASE_URL = "postgresql://user:password@host:port/database"

# Connection pooling
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
```

### Session Management
```python
# Get database session
session = db_manager.get_session()

# Use session for operations
restaurants = session.query(Restaurant).all()

# Always close session
session.close()
```

### Error Handling
```python
try:
    session = db_manager.get_session()
    # Database operations
except SQLAlchemyError as e:
    logger.error(f"Database error: {e}")
    session.rollback()
finally:
    session.close()
```

## 📋 Data Operations

### Querying Restaurants
```python
# Get all restaurants
restaurants = db_manager.get_all_places(limit=100, offset=0)

# Search restaurants
results = db_manager.search_places(
    query="kosher",
    category="restaurant",
    state="FL",
    limit=50
)

# Location-based search
nearby = db_manager.search_restaurants_near_location(
    lat=25.7617,
    lng=-80.1918,
    radius=10
)
```

### Adding Restaurants
```python
# Add restaurant with basic info
success = db_manager.add_restaurant_simple(
    name="Kosher Deli",
    address="123 Main St",
    phone_number="(555) 123-4567",
    kosher_type="meat",
    certifying_agency="ORB"
)

# Add restaurant with full data
restaurant_data = {
    "name": "Restaurant Name",
    "address": "Address",
    "city": "City",
    "state": "State",
    "kosher_type": "dairy",
    "is_cholov_yisroel": True,
    # ... other fields
}
success = db_manager.add_restaurant(restaurant_data)
```

### Updating Restaurants
```python
# Update ORB data
success = db_manager.update_restaurant_orb_data(
    restaurant_id=1,
    address="New Address",
    kosher_type="dairy",
    certifying_agency="ORB",
    extra_kosher_info="Chalav Yisroel"
)
```

## 🔍 Data Validation

### Input Validation
- **Required Fields**: name, kosher_type, certifying_agency
- **Data Types**: Proper type checking for all fields
- **Length Limits**: Enforced for VARCHAR fields
- **Boolean Flags**: Proper boolean validation

### Data Quality
- **Duplicate Detection**: Check for existing restaurants
- **Address Validation**: Verify address format
- **Phone Validation**: Standardize phone number format
- **Email Validation**: Verify email format

## 📊 Backup & Recovery

### Automated Backups
- **Neon Backups**: Daily automated backups
- **Point-in-time Recovery**: Available for 7 days
- **Backup Retention**: 30 days of backups

### Manual Backups
```bash
# Export data to JSON
python scripts/maintenance/app_sqlite_backup.py

# Import data from JSON
python scripts/maintenance/populate_remote_backend.py
```

### Recovery Procedures
1. **Identify Issue**: Check logs and error messages
2. **Stop Services**: Pause application if needed
3. **Restore Backup**: Use Neon point-in-time recovery
4. **Verify Data**: Check data integrity
5. **Restart Services**: Resume normal operation

## 🔧 Migration Management

### Schema Changes
```python
# Example migration
def upgrade_schema():
    # Add new column
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE restaurants ADD COLUMN new_field VARCHAR(100)"))
        conn.commit()
```

### Data Migration
```python
# Migrate existing data
def migrate_data():
    session = db_manager.get_session()
    try:
        restaurants = session.query(Restaurant).all()
        for restaurant in restaurants:
            # Update data as needed
            restaurant.new_field = "default_value"
        session.commit()
    finally:
        session.close()
```

## 📈 Performance Optimization

### Indexing Strategy
```sql
-- Primary key index (automatic)
CREATE INDEX idx_restaurants_name ON restaurants(name);
CREATE INDEX idx_restaurants_city ON restaurants(city);
CREATE INDEX idx_restaurants_state ON restaurants(state);
CREATE INDEX idx_restaurants_kosher_type ON restaurants(kosher_type);
CREATE INDEX idx_restaurants_location ON restaurants(latitude, longitude);
```

### Query Optimization
- **Limit Results**: Always use LIMIT for large queries
- **Use Indexes**: Ensure queries use indexed columns
- **Connection Pooling**: Reuse database connections
- **Batch Operations**: Group multiple operations

## 🔐 Security

### Connection Security
- **SSL/TLS**: Encrypted database connections
- **Connection Pooling**: Secure connection management
- **Environment Variables**: Secure credential storage

### Data Protection
- **Input Sanitization**: Prevent SQL injection
- **Access Control**: Limit database access
- **Audit Logging**: Track database operations

## 📁 Detailed Guides

### [Schema Details](./schema.md)
- Complete schema documentation
- Field descriptions and constraints
- Index and constraint definitions
- Data type specifications

### [Migrations](./migrations.md)
- Migration procedures
- Schema change management
- Data migration strategies
- Rollback procedures

## 🚨 Troubleshooting

### Common Issues
- **Connection Errors**: Check DATABASE_URL and network
- **Performance Issues**: Review query optimization
- **Data Integrity**: Verify backup and recovery procedures
- **Migration Errors**: Check migration scripts and data

### Debugging
```python
# Enable SQL logging
import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Check connection
session = db_manager.get_session()
result = session.execute(text("SELECT 1"))
print("Database connection successful")
session.close()
```

---

*For detailed schema information, see the schema documentation.* 