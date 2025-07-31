# Database Schema Changes Documentation

## 🗄️ Overview

This document details all database schema changes, migrations, and data quality improvements made to the JewGo application. The database has evolved from a simple structure to a comprehensive system supporting advanced features and data validation.

---

## 📊 Database Architecture

### Technology Stack
- **Database**: PostgreSQL 14+
- **ORM**: SQLAlchemy (Python)
- **Migration Tool**: Alembic
- **Connection Pooling**: SQLAlchemy Pool
- **Backup**: Automated daily backups

### Database Instance
- **Hosting**: Railway (Managed PostgreSQL)
- **Version**: PostgreSQL 14.8
- **Storage**: 1GB (expandable)
- **Connections**: 20 concurrent connections
- **Backup Retention**: 7 days

---

## 🏗️ Schema Evolution

### Initial Schema (v1.0)
```sql
CREATE TABLE kosher_places (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    detail_url TEXT UNIQUE,
    category TEXT,
    photo TEXT,
    address TEXT,
    phone TEXT,
    website TEXT,
    kosher_cert_link TEXT,
    kosher_type TEXT,
    extra_kosher_info TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Current Schema (v3.0)
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

---

## 🔄 Migration History

### Migration 1: Table Rename and Restructure
```sql
-- Rename kosher_places to restaurants
ALTER TABLE kosher_places RENAME TO restaurants;

-- Add new required columns
ALTER TABLE restaurants ADD COLUMN city TEXT NOT NULL DEFAULT '';
ALTER TABLE restaurants ADD COLUMN state TEXT NOT NULL DEFAULT '';
ALTER TABLE restaurants ADD COLUMN zip_code TEXT;
ALTER TABLE restaurants ADD COLUMN phone_number TEXT;
ALTER TABLE restaurants ADD COLUMN image_url TEXT;
ALTER TABLE restaurants ADD COLUMN certifying_agency TEXT NOT NULL DEFAULT 'Unknown';
ALTER TABLE restaurants ADD COLUMN kosher_category TEXT DEFAULT 'unknown';
ALTER TABLE restaurants ADD COLUMN listing_type TEXT DEFAULT 'restaurant';
ALTER TABLE restaurants ADD COLUMN status TEXT DEFAULT 'active';
```

### Migration 2: Data Quality Improvements
```sql
-- Add constraints for kosher categories
ALTER TABLE restaurants ADD CONSTRAINT check_kosher_category 
CHECK (kosher_category IN ('meat', 'dairy', 'pareve', 'fish', 'unknown'));

-- Add validation for certifying agencies
ALTER TABLE restaurants ADD CONSTRAINT check_certifying_agency 
CHECK (certifying_agency IN ('ORB', 'KM', 'Star-K', 'CRC', 'Kof-K', 'Diamond K', 'Unknown'));

-- Add geolocation columns
ALTER TABLE restaurants ADD COLUMN latitude NUMERIC;
ALTER TABLE restaurants ADD COLUMN longitude NUMERIC;
```

### Migration 3: Enhanced Features
```sql
-- Add Chalav Yisrael support
ALTER TABLE restaurants ADD COLUMN is_cholov_yisroel BOOLEAN;

-- Add Google integration
ALTER TABLE restaurants ADD COLUMN google_listing_url TEXT;

-- Add rating and review fields
ALTER TABLE restaurants ADD COLUMN rating NUMERIC;
ALTER TABLE restaurants ADD COLUMN star_rating NUMERIC;
ALTER TABLE restaurants ADD COLUMN quality_rating NUMERIC;
ALTER TABLE restaurants ADD COLUMN review_count INTEGER;
ALTER TABLE restaurants ADD COLUMN google_rating NUMERIC;
ALTER TABLE restaurants ADD COLUMN google_review_count INTEGER;
ALTER TABLE restaurants ADD COLUMN google_reviews TEXT;

-- Add menu pricing support
ALTER TABLE restaurants ADD COLUMN menu_pricing JSONB;
ALTER TABLE restaurants ADD COLUMN min_avg_meal_cost NUMERIC;
ALTER TABLE restaurants ADD COLUMN max_avg_meal_cost NUMERIC;
```

---

## 📋 Field Definitions

### Core Information
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | SERIAL | Yes | Primary key, auto-incrementing |
| `name` | TEXT | Yes | Restaurant name |
| `address` | TEXT | Yes | Street address |
| `city` | TEXT | Yes | City name |
| `state` | TEXT | Yes | State or province |
| `zip_code` | TEXT | No | Postal code |

### Contact Information
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `phone_number` | TEXT | No | Contact phone number |
| `website` | TEXT | No | Restaurant website URL |
| `certificate_link` | TEXT | No | Kosher certification link |

### Kosher Information
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `certifying_agency` | TEXT | Yes | Kosher certification agency |
| `kosher_category` | TEXT | Yes | Type of kosher (meat/dairy/pareve) |
| `is_cholov_yisroel` | BOOLEAN | No | Chalav Yisrael certification |

### Business Information
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `listing_type` | TEXT | Yes | Business type (restaurant/bakery/etc) |
| `status` | TEXT | Yes | Active/inactive status |
| `hours_of_operation` | TEXT | No | Operating hours |
| `hours_open` | TEXT | No | Current open/closed status |
| `short_description` | TEXT | No | Brief description |
| `price_range` | TEXT | No | Price level indicator |

### Location & Maps
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `latitude` | NUMERIC | No | GPS latitude coordinate |
| `longitude` | NUMERIC | No | GPS longitude coordinate |
| `google_listing_url` | TEXT | No | Google Business listing URL |

### Ratings & Reviews
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `rating` | NUMERIC | No | Internal rating (1-5) |
| `star_rating` | NUMERIC | No | Star rating display |
| `quality_rating` | NUMERIC | No | Quality assessment |
| `review_count` | INTEGER | No | Number of reviews |
| `google_rating` | NUMERIC | No | Google rating |
| `google_review_count` | INTEGER | No | Google review count |
| `google_reviews` | TEXT | No | JSON string of reviews |

### Pricing Information
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `avg_price` | TEXT | No | Average meal price |
| `menu_pricing` | JSONB | No | Structured menu pricing data |
| `min_avg_meal_cost` | NUMERIC | No | Minimum meal cost |
| `max_avg_meal_cost` | NUMERIC | No | Maximum meal cost |

### Metadata
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image_url` | TEXT | No | Restaurant image URL |
| `notes` | TEXT | No | Additional notes |
| `created_at` | TIMESTAMPTZ | Yes | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | Yes | Last update timestamp |

---

## 🔒 Constraints & Validation

### Check Constraints
```sql
-- Kosher category validation
ALTER TABLE restaurants ADD CONSTRAINT check_kosher_category 
CHECK (kosher_category IN ('meat', 'dairy', 'pareve', 'fish', 'unknown'));

-- Certifying agency validation
ALTER TABLE restaurants ADD CONSTRAINT check_certifying_agency 
CHECK (certifying_agency IN ('ORB', 'KM', 'Star-K', 'CRC', 'Kof-K', 'Diamond K', 'Unknown'));

-- Rating validation
ALTER TABLE restaurants ADD CONSTRAINT check_rating 
CHECK (rating >= 0 AND rating <= 5);

-- Price validation
ALTER TABLE restaurants ADD CONSTRAINT check_price_range 
CHECK (min_avg_meal_cost <= max_avg_meal_cost);
```

### Not Null Constraints
```sql
-- Required fields
ALTER TABLE restaurants ALTER COLUMN name SET NOT NULL;
ALTER TABLE restaurants ALTER COLUMN address SET NOT NULL;
ALTER TABLE restaurants ALTER COLUMN city SET NOT NULL;
ALTER TABLE restaurants ALTER COLUMN state SET NOT NULL;
ALTER TABLE restaurants ALTER COLUMN certifying_agency SET NOT NULL;
ALTER TABLE restaurants ALTER COLUMN kosher_category SET NOT NULL;
```

### Unique Constraints
```sql
-- Prevent duplicate restaurants
ALTER TABLE restaurants ADD CONSTRAINT unique_restaurant_name_address 
UNIQUE (name, address, city, state);
```

---

## 📈 Indexes for Performance

### Primary Indexes
```sql
-- Primary key (automatic)
CREATE INDEX idx_restaurants_id ON restaurants(id);

-- Name search optimization
CREATE INDEX idx_restaurants_name ON restaurants USING gin(to_tsvector('english', name));

-- Location-based queries
CREATE INDEX idx_restaurants_location ON restaurants(city, state);
CREATE INDEX idx_restaurants_coordinates ON restaurants(latitude, longitude);
```

### Secondary Indexes
```sql
-- Kosher filtering
CREATE INDEX idx_restaurants_kosher_category ON restaurants(kosher_category);
CREATE INDEX idx_restaurants_certifying_agency ON restaurants(certifying_agency);

-- Status and type filtering
CREATE INDEX idx_restaurants_status ON restaurants(status);
CREATE INDEX idx_restaurants_listing_type ON restaurants(listing_type);

-- Rating and review queries
CREATE INDEX idx_restaurants_rating ON restaurants(rating DESC);
CREATE INDEX idx_restaurants_google_rating ON restaurants(google_rating DESC);

-- Timestamp queries
CREATE INDEX idx_restaurants_created_at ON restaurants(created_at DESC);
CREATE INDEX idx_restaurants_updated_at ON restaurants(updated_at DESC);
```

### Composite Indexes
```sql
-- Multi-criteria search
CREATE INDEX idx_restaurants_search ON restaurants 
USING gin(to_tsvector('english', name || ' ' || address || ' ' || city));

-- Location + category filtering
CREATE INDEX idx_restaurants_location_category ON restaurants(city, kosher_category);

-- Agency + category filtering
CREATE INDEX idx_restaurants_agency_category ON restaurants(certifying_agency, kosher_category);
```

---

## 🧹 Data Quality Improvements

### Address Standardization
```python
def standardize_address(address: str) -> str:
    """Standardize address formatting"""
    # Remove extra whitespace
    address = ' '.join(address.split())
    
    # Remove trailing commas
    address = address.rstrip(',')
    
    # Standardize common abbreviations
    replacements = {
        'St.': 'Street',
        'Ave.': 'Avenue',
        'Blvd.': 'Boulevard',
        'Rd.': 'Road',
        'Dr.': 'Drive'
    }
    
    for old, new in replacements.items():
        address = address.replace(old, new)
    
    return address
```

### Phone Number Validation
```python
def validate_phone_number(phone: str) -> str:
    """Validate and format phone numbers"""
    import re
    
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Validate length (10 digits for US numbers)
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone  # Return original if can't format
```

### Website Validation
```python
def validate_website(url: str) -> str:
    """Validate and normalize website URLs"""
    import re
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Remove trailing slashes
    url = url.rstrip('/')
    
    # Basic URL validation
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if url_pattern.match(url):
        return url
    else:
        return None
```

---

## 🔄 Data Migration Scripts

### Migration Script: Update Kosher Categories
```python
def update_kosher_categories():
    """Update kosher categories to standardized values"""
    updates = {
        'meat': ['meat', 'fleishig', 'fleishigs'],
        'dairy': ['dairy', 'milchig', 'milchigs', 'milch'],
        'pareve': ['pareve', 'parve', 'neutral'],
        'fish': ['fish', 'seafood'],
        'unknown': ['unknown', 'unspecified', '']
    }
    
    for new_category, old_categories in updates.items():
        for old_category in old_categories:
            execute_query(
                "UPDATE restaurants SET kosher_category = %s WHERE kosher_category = %s",
                (new_category, old_category)
            )
```

### Migration Script: Add Chalav Yisrael Data
```python
def add_chalav_yisrael_data():
    """Add Chalav Yisrael information based on certifying agency"""
    # ORB dairy restaurants are typically Chalav Stam
    execute_query(
        "UPDATE restaurants SET is_cholov_yisroel = FALSE WHERE certifying_agency = 'ORB' AND kosher_category = 'dairy'"
    )
    
    # Some agencies are known for Chalav Yisrael
    chalav_yisrael_agencies = ['KM', 'Star-K']
    for agency in chalav_yisrael_agencies:
        execute_query(
            "UPDATE restaurants SET is_cholov_yisroel = TRUE WHERE certifying_agency = %s AND kosher_category = 'dairy'",
            (agency,)
        )
```

### Migration Script: Geocode Addresses
```python
def geocode_addresses():
    """Add latitude/longitude coordinates for addresses"""
    from geopy.geocoders import Nominatim
    
    geolocator = Nominatim(user_agent="jewgo_app")
    
    # Get restaurants without coordinates
    restaurants = execute_query(
        "SELECT id, address, city, state FROM restaurants WHERE latitude IS NULL OR longitude IS NULL"
    )
    
    for restaurant in restaurants:
        try:
            full_address = f"{restaurant['address']}, {restaurant['city']}, {restaurant['state']}"
            location = geolocator.geocode(full_address)
            
            if location:
                execute_query(
                    "UPDATE restaurants SET latitude = %s, longitude = %s WHERE id = %s",
                    (location.latitude, location.longitude, restaurant['id'])
                )
        except Exception as e:
            print(f"Error geocoding {restaurant['id']}: {e}")
```

---

## 📊 Data Quality Metrics

### Completeness Metrics
```sql
-- Overall data completeness
SELECT 
    COUNT(*) as total_restaurants,
    COUNT(CASE WHEN phone_number IS NOT NULL THEN 1 END) as with_phone,
    COUNT(CASE WHEN website IS NOT NULL THEN 1 END) as with_website,
    COUNT(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 END) as with_coordinates,
    COUNT(CASE WHEN image_url IS NOT NULL THEN 1 END) as with_images
FROM restaurants;
```

### Accuracy Metrics
```sql
-- Data validation results
SELECT 
    kosher_category,
    COUNT(*) as count,
    COUNT(CASE WHEN kosher_category IN ('meat', 'dairy', 'pareve', 'fish', 'unknown') THEN 1 END) as valid_count
FROM restaurants 
GROUP BY kosher_category;
```

### Consistency Metrics
```sql
-- Address format consistency
SELECT 
    COUNT(*) as total_addresses,
    COUNT(CASE WHEN address ~ '^[A-Za-z0-9\s,.-]+$' THEN 1 END) as properly_formatted
FROM restaurants;
```

---

## 🔧 Maintenance Procedures

### Regular Maintenance Tasks
```sql
-- Update timestamps
UPDATE restaurants SET updated_at = NOW() WHERE updated_at < NOW() - INTERVAL '1 day';

-- Clean up orphaned records
DELETE FROM restaurants WHERE status = 'inactive' AND updated_at < NOW() - INTERVAL '1 year';

-- Optimize table
VACUUM ANALYZE restaurants;

-- Update statistics
ANALYZE restaurants;
```

### Backup Procedures
```bash
#!/bin/bash
# Daily backup script

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_NAME="jewgo_production"

# Create backup
pg_dump $DB_NAME > $BACKUP_DIR/restaurants_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/restaurants_$DATE.sql

# Remove old backups (keep 7 days)
find $BACKUP_DIR -name "restaurants_*.sql.gz" -mtime +7 -delete
```

---

## 🚀 Performance Optimization

### Query Optimization
```sql
-- Use indexes effectively
EXPLAIN ANALYZE SELECT * FROM restaurants 
WHERE city = 'New York' AND kosher_category = 'dairy'
ORDER BY rating DESC;

-- Optimize text search
CREATE INDEX idx_restaurants_fulltext ON restaurants 
USING gin(to_tsvector('english', name || ' ' || address || ' ' || city || ' ' || short_description));
```

### Connection Pooling
```python
# SQLAlchemy connection pool configuration
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

---

## 🔮 Future Schema Enhancements

### Planned Additions
- **User reviews table**: Store user-generated reviews
- **Restaurant hours table**: Detailed operating hours
- **Menu items table**: Individual menu items with pricing
- **Photos table**: Multiple restaurant photos
- **Events table**: Special events and promotions

### Schema Evolution Strategy
- **Backward compatibility**: Maintain API compatibility
- **Gradual migration**: Migrate data in phases
- **Feature flags**: Enable new features gradually
- **Rollback procedures**: Ability to revert changes

---

*Last Updated: January 2025*
*Version: 3.0.0* 