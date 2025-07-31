# 🗄️ Optimized Restaurants Database Schema

## Overview

This document outlines the optimized database schema for the JewGo application's restaurants table. The schema has been redesigned to be more robust, maintainable, and scalable while preventing future issues.

## 📊 Schema Design Principles

### 🔒 System-Generated / Controlled Fields
These fields are managed by the system and should not be manually modified:

| Field                | Type               | Notes                                  |
| -------------------- | ------------------ | -------------------------------------- |
| `id`                 | SERIAL PRIMARY KEY | Auto-increment                         |
| `created_at`         | TIMESTAMPTZ        | Required, system-generated             |
| `updated_at`         | TIMESTAMPTZ        | Required, system-managed               |
| `current_time_local` | TIMESTAMPTZ        | System-generated (local time snapshot) |
| `hours_parsed`       | BOOLEAN            | Internal flag — OK to keep             |
| `timezone`           | TEXT               | Based on geolocation or ORB data       |

### 🧾 Required Fields (Updated via ORB scrape every 3 weeks)
These fields are required and updated from ORB data:

| Field               | Type                            | Notes                 |
| ------------------- | ------------------------------- | --------------------- |
| `name`              | TEXT                            | ✔ from ORB            |
| `address`           | TEXT                            | ✔ from ORB            |
| `city`              | TEXT                            | ✔ from ORB            |
| `state`             | TEXT                            | ✔ from ORB            |
| `zip_code`          | TEXT                            | ✔ from ORB            |
| `phone_number`      | TEXT                            | ✔ from ORB            |
| `website`           | TEXT                            | ✔ from ORB            |
| `certifying_agency` | TEXT                            | Auto-filled = `"ORB"` |
| `kosher_category`   | ENUM('meat', 'dairy', 'pareve') | ✔ from ORB            |
| `listing_type`      | TEXT                            | ✔ from ORB            |

### 📍 Enriched via Google Places API (on creation or scheduled)
These fields are enriched from external APIs:

| Field                | Type  | Notes                                   |
| -------------------- | ----- | --------------------------------------- |
| `google_listing_url` | TEXT  | Optional (1-time fetch)                 |
| `price_range`        | TEXT  | Optional                                |
| `short_description`  | TEXT  | Optional (e.g. from GMB or internal AI) |
| `hours_of_operation` | TEXT  | Optional (check every 7 days)           |
| `latitude`           | FLOAT | Based on geocoded address               |
| `longitude`          | FLOAT | Based on geocoded address               |

### 🧼 Kosher Details Source ORB data
Kosher-specific information from ORB:

| Field               | Type    | Notes                          |
| ------------------- | ------- | ------------------------------ |
| `is_cholov_yisroel` | BOOLEAN | Optional (only if dairy)       |
| `is_pas_yisroel`    | BOOLEAN | Optional (only if meat/pareve) |

### 🖼️ Display/UX Fields
User-facing display fields:

| Field       | Type                    | Notes                              |
| ----------- | ----------------------- | ---------------------------------- |
| `image_url` | TEXT                    | Optional — fallback to placeholder |
| `specials`  | JSONB\[] or child table | Admin-managed only, frontend only  |

## 🗑️ Removed Fields

The following fields have been removed from the schema:

* `detail_url` — ❌ delete
* `email` — ❌ delete
* `kosher_cert_link` — ❌ delete
* `next_open_time` — ❌ delete (calculate in logic)
* `is_open` — ❌ move to function, not DB
* `status_reason` — ❌ internal only, not DB

## 🔍 Field Mapping

### Old → New Field Names
- `phone` → `phone_number`
- `category` → `listing_type`
- `hours_open` → `hours_of_operation`
- `kosher_type` → `kosher_category`

## 📈 Performance Optimizations

### Indexes
The following indexes have been added for better performance:

```sql
CREATE INDEX idx_restaurants_kosher_category ON restaurants (kosher_category);
CREATE INDEX idx_restaurants_certifying_agency ON restaurants (certifying_agency);
CREATE INDEX idx_restaurants_state ON restaurants (state);
CREATE INDEX idx_restaurants_city ON restaurants (city);
CREATE INDEX idx_restaurants_created_at ON restaurants (created_at);
CREATE INDEX idx_restaurants_location ON restaurants (latitude, longitude);
```

### Constraints
- Required fields are marked as `NOT NULL`
- Default values are set for `certifying_agency` ('ORB')
- Proper data types for all fields

## 🔄 Data Migration

### Migration Script
The migration script `optimize_restaurants_schema.py` handles:

1. **Adding new fields** with proper data types
2. **Migrating data** from old field names to new ones
3. **Removing deprecated fields**
4. **Adding performance indexes**
5. **Setting default values**
6. **Verifying data integrity**

### Running the Migration
```bash
cd backend/database/migrations
python optimize_restaurants_schema.py
```

## 🧠 Automation & Sync Strategy

| Source                | Frequency                   | Fields                                                                                            |
| --------------------- | --------------------------- | ------------------------------------------------------------------------------------------------- |
| **ORB Scrape**        | Every 3 weeks               | name, address, city, state, zip, phone, website, kosher_category, listing_type                  |
| **Google Places API** | Once (then weekly for some) | latitude, longitude, price_range, hours_of_operation, short_description, google_listing_url |
| **Image URL**         | Once                        | fallback to placeholder if none                                                                   |

## 🔧 API Integration

### Frontend Compatibility
The frontend has been updated to work with the new schema:

- Updated field names in API calls
- Modified data mapping functions
- Updated form validation
- Adjusted display logic

### Backend Changes
- Updated database manager methods
- Modified data validation
- Enhanced error handling
- Improved logging

## 🚀 Benefits of New Schema

### ✅ Improved Data Integrity
- Required fields prevent incomplete data
- Proper constraints ensure data quality
- Default values reduce null values

### ✅ Better Performance
- Optimized indexes for common queries
- Reduced table size by removing unused fields
- Efficient data types

### ✅ Enhanced Maintainability
- Clear field categorization
- Consistent naming conventions
- Better documentation

### ✅ Future-Proof Design
- Scalable for additional features
- Flexible for new data sources
- Easy to extend

## 🔍 Monitoring & Maintenance

### Data Quality Checks
- Monitor for null values in required fields
- Track data freshness (last ORB update)
- Validate kosher category consistency

### Performance Monitoring
- Query execution times
- Index usage statistics
- Table size growth

### Backup Strategy
- Daily automated backups
- Point-in-time recovery capability
- Test restore procedures regularly

## 📝 Development Guidelines

### Adding New Fields
1. Determine field category (Required, Enriched, Display, etc.)
2. Add to appropriate section in schema
3. Update migration script
4. Modify database manager methods
5. Update frontend if needed
6. Test thoroughly

### Data Updates
1. Use ORB scraper for core data
2. Use Google Places API for enrichment
3. Validate data before insertion
4. Log all changes for audit trail

### Error Handling
1. Graceful degradation for missing data
2. Clear error messages
3. Fallback values where appropriate
4. Comprehensive logging

## 🎯 Next Steps

1. **Run Migration**: Execute the schema optimization migration
2. **Test Thoroughly**: Verify all functionality works with new schema
3. **Update Documentation**: Keep this document current
4. **Monitor Performance**: Track improvements and issues
5. **Plan Future Enhancements**: Consider additional optimizations

---

*Last Updated: 2024*
*Version: 1.0*
*Maintained by: JewGo Development Team* 