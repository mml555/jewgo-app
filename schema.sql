-- ORB Kosher Scraper Database Schema
-- PostgreSQL schema for storing kosher business data

-- Create the kosher_places table
CREATE TABLE IF NOT EXISTS kosher_places (
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

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_kosher_places_name ON kosher_places(name);
CREATE INDEX IF NOT EXISTS idx_kosher_places_category ON kosher_places(category);
CREATE INDEX IF NOT EXISTS idx_kosher_places_kosher_type ON kosher_places(kosher_type);
CREATE INDEX IF NOT EXISTS idx_kosher_places_created_at ON kosher_places(created_at);

-- Create a full-text search index for searching across multiple fields
CREATE INDEX IF NOT EXISTS idx_kosher_places_search ON kosher_places USING gin(
    to_tsvector('english', 
        COALESCE(name, '') || ' ' || 
        COALESCE(address, '') || ' ' || 
        COALESCE(extra_kosher_info, '')
    )
);

-- Add comments for documentation
COMMENT ON TABLE kosher_places IS 'Kosher business listings scraped from ORB Kosher';
COMMENT ON COLUMN kosher_places.name IS 'Business name';
COMMENT ON COLUMN kosher_places.detail_url IS 'ORB detail page URL (unique)';
COMMENT ON COLUMN kosher_places.category IS 'Business category (e.g., Restaurant)';
COMMENT ON COLUMN kosher_places.photo IS 'Image URL from detail page';
COMMENT ON COLUMN kosher_places.address IS 'Street address';
COMMENT ON COLUMN kosher_places.phone IS 'Phone number';
COMMENT ON COLUMN kosher_places.website IS 'Business website URL';
COMMENT ON COLUMN kosher_places.kosher_cert_link IS 'Kosher certification link';
COMMENT ON COLUMN kosher_places.kosher_type IS 'General kosher type (Meat, Dairy, Parve)';
COMMENT ON COLUMN kosher_places.extra_kosher_info IS 'Special kosher requirements (Cholov Yisroel, etc.)';
COMMENT ON COLUMN kosher_places.created_at IS 'Timestamp when record was created'; 