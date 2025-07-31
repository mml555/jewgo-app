# Database Schema Documentation

## Overview

This document provides comprehensive details about the JewGo database schema, including table structures, relationships, and data types.

## 🗄️ Database Architecture

### Technology Stack
- **Database**: PostgreSQL (Neon)
- **ORM**: SQLAlchemy 1.4
- **Connection**: Connection pooling with psycopg2
- **Backup**: Automated backups via Neon

### Database Schema
The application uses a single consolidated `restaurants` table with 28 optimized columns for kosher restaurant data.

## 📊 Complete Schema Definition

### Restaurants Table Structure

```sql
CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip_code TEXT,
    phone_number TEXT,
    website TEXT,
    certificate_link TEXT,
    image_url TEXT,
    certifying_agency TEXT NOT NULL,
    kosher_category TEXT CHECK (kosher_category IN ('meat', 'dairy', 'pareve', 'fish', 'unknown')),
    is_cholov_yisroel BOOLEAN,
    listing_type TEXT DEFAULT 'restaurant',
    status TEXT DEFAULT 'active',
    hours_of_operation TEXT,
    hours_open TEXT,
    short_description TEXT,
    price_range TEXT,
    avg_price TEXT,
    menu_pricing JSONB,
    min_avg_meal_cost NUMERIC,
    max_avg_meal_cost NUMERIC,
    notes TEXT,
    latitude NUMERIC,
    longitude NUMERIC,
    google_listing_url TEXT,
    rating NUMERIC,
    star_rating NUMERIC,
    quality_rating NUMERIC,
    review_count INTEGER,
    google_rating NUMERIC,
    google_review_count INTEGER,
    google_reviews TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

## 🔑 Key Schema Updates

### Recent Enhancements
- **Added `is_cholov_yisroel`**: Boolean field for milk supervision level
- **Added `google_listing_url`**: Direct link to Google Business listing
- **Enhanced kosher_category**: Added 'fish' and 'unknown' options
- **Improved validation**: Check constraints for kosher categories
- **JSONB support**: Menu pricing stored as structured JSON
- **Geolocation**: Latitude/longitude for map integration

### Data Quality Improvements
- **Address standardization**: Consistent formatting across all records
- **Phone number validation**: Proper formatting and validation
- **Website validation**: URL format checking and normalization
- **Kosher type validation**: Ensures only valid categories are stored

## 📋 Field Descriptions

### Core Restaurant Information
```sql
-- Primary identification
id INTEGER PRIMARY KEY                    -- Unique restaurant identifier
name VARCHAR(255) NOT NULL               -- Restaurant name (required)

-- Location information
address VARCHAR(500)                     -- Street address
city VARCHAR(100)                        -- City name
state VARCHAR(50)                        -- State abbreviation
zip_code VARCHAR(20)                     -- ZIP code
latitude FLOAT                           -- Latitude coordinate
longitude FLOAT                          -- Longitude coordinate

-- Contact information
phone VARCHAR(50)                        -- Phone number
website VARCHAR(500)                     -- Website URL
email VARCHAR(255)                       -- Email address
```

### Business Details
```sql
-- Business information
price_range VARCHAR(20)                  -- $, $$, $$$, $$$$
image_url VARCHAR(500)                   -- Restaurant image URL
hours_open TEXT                          -- Business hours
category VARCHAR(100) DEFAULT 'restaurant' -- Business category
status VARCHAR(50) DEFAULT 'approved'    -- Restaurant status
```

### Kosher Supervision
```sql
-- Kosher status flags
is_kosher BOOLEAN DEFAULT FALSE          -- General kosher status
is_glatt BOOLEAN DEFAULT FALSE           -- Glatt kosher status
is_cholov_yisroel BOOLEAN DEFAULT FALSE  -- Chalav Yisroel status
is_pas_yisroel BOOLEAN DEFAULT FALSE     -- Pas Yisroel status
is_bishul_yisroel BOOLEAN DEFAULT FALSE  -- Bishul Yisroel status
is_mehadrin BOOLEAN DEFAULT FALSE        -- Mehadrin status
is_hechsher BOOLEAN DEFAULT FALSE        -- Hechsher status

-- Kosher categorization
kosher_type VARCHAR(100)                 -- dairy, meat, pareve, fish, unknown
```

### ORB Integration
```sql
-- ORB certification details
kosher_cert_link VARCHAR(500)            -- Kosher certificate link
detail_url VARCHAR(500)                  -- Detail page URL
short_description TEXT                   -- Brief description
google_listing_url VARCHAR(500)          -- Google listing URL
```

### Pricing & Reviews
```sql
-- Pricing information
avg_price TEXT                           -- Average price text
menu_pricing JSONB                       -- Structured menu pricing
min_avg_meal_cost NUMERIC                -- Minimum meal cost
max_avg_meal_cost NUMERIC                -- Maximum meal cost

-- Rating information
rating NUMERIC                           -- Overall rating
star_rating NUMERIC                      -- Star rating
quality_rating NUMERIC                   -- Quality rating
review_count INTEGER                     -- Number of reviews
google_rating NUMERIC                    -- Google rating
google_review_count INTEGER              -- Google review count
google_reviews TEXT                      -- Google reviews text
```

### Audit Trail
```sql
-- Timestamps
created_at TIMESTAMP DEFAULT NOW()       -- Creation timestamp
updated_at TIMESTAMP DEFAULT NOW()       -- Last update timestamp
notes TEXT                               -- Additional notes
```

## 🔍 Data Validation Rules

### Required Fields
- **name**: Restaurant name (required)
- **address**: Complete address (required)
- **city**: City name (required)
- **state**: State abbreviation (required)
- **certifying_agency**: Kosher certification agency (required)

### Validation Constraints
```sql
-- Kosher category validation
kosher_category TEXT CHECK (kosher_category IN ('meat', 'dairy', 'pareve', 'fish', 'unknown'))

-- Status validation
status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'pending', 'approved'))

-- Price range validation
price_range VARCHAR(20) CHECK (price_range IN ('$', '$$', '$$$', '$$$$'))
```

### Data Quality Standards
- **Phone Numbers**: Standardized format (XXX) XXX-XXXX
- **Websites**: Valid URL format with protocol
- **Emails**: Valid email format
- **Addresses**: Consistent formatting across all records
- **Coordinates**: Valid latitude/longitude pairs

## 📈 Current Data Statistics

### Restaurant Distribution
- **Total Restaurants**: 107
- **Dairy Restaurants**: 99
- **Pareve Restaurants**: 8
- **Meat Restaurants**: 0
- **Fish Restaurants**: 0
- **Unknown Type**: 0

### Kosher Supervision
- **Chalav Yisroel**: 104 restaurants
- **Chalav Stam**: 3 restaurants
- **Pas Yisroel**: 22 restaurants
- **Glatt Kosher**: Various
- **Mehadrin**: Various

### Geographic Distribution
- **States**: FL, NY, CA
- **Cities**: Miami, New York, Los Angeles, etc.
- **Complete Addresses**: 100%

## 🔧 Database Operations

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

## 📊 Query Examples

### Basic Queries
```sql
-- Get all restaurants
SELECT * FROM restaurants WHERE status = 'active';

-- Get restaurants by kosher type
SELECT * FROM restaurants WHERE kosher_category = 'dairy';

-- Get restaurants by certifying agency
SELECT * FROM restaurants WHERE certifying_agency = 'ORB';

-- Get restaurants with Chalav Yisroel
SELECT * FROM restaurants WHERE is_cholov_yisroel = true;
```

### Advanced Queries
```sql
-- Get restaurants by location
SELECT * FROM restaurants 
WHERE latitude BETWEEN 25.0 AND 26.0 
AND longitude BETWEEN -80.5 AND -80.0;

-- Get restaurants with reviews
SELECT * FROM restaurants 
WHERE review_count > 0 
ORDER BY rating DESC;

-- Get restaurants by price range
SELECT * FROM restaurants 
WHERE price_range = '$$' 
AND kosher_category = 'dairy';
```

## 🔍 Indexing Strategy

### Recommended Indexes
```sql
-- Primary key index (automatic)
CREATE INDEX idx_restaurants_name ON restaurants(name);
CREATE INDEX idx_restaurants_city ON restaurants(city);
CREATE INDEX idx_restaurants_state ON restaurants(state);
CREATE INDEX idx_restaurants_kosher_type ON restaurants(kosher_type);
CREATE INDEX idx_restaurants_location ON restaurants(latitude, longitude);
CREATE INDEX idx_restaurants_certifying_agency ON restaurants(certifying_agency);
CREATE INDEX idx_restaurants_status ON restaurants(status);
```

### Performance Optimization
- **Limit Results**: Always use LIMIT for large queries
- **Use Indexes**: Ensure queries use indexed columns
- **Connection Pooling**: Reuse database connections
- **Batch Operations**: Group multiple operations

## 🔐 Security Considerations

### Connection Security
- **SSL/TLS**: Encrypted database connections
- **Connection Pooling**: Secure connection management
- **Environment Variables**: Secure credential storage

### Data Protection
- **Input Sanitization**: Prevent SQL injection
- **Access Control**: Limit database access
- **Audit Logging**: Track database operations

## 📋 Migration Procedures

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

---

*For detailed implementation examples, see the development documentation.* 