-- ORB Kosher Places Table Schema
-- PostgreSQL schema for storing scraped ORB kosher business data

CREATE TABLE IF NOT EXISTS kosher_places (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    photo TEXT,
    address TEXT,
    phone TEXT,
    website TEXT,
    kosher_cert_link TEXT,
    kosher_type TEXT,
    listing_type TEXT,
    detail_url TEXT,
    extra_kosher_info TEXT,
    source TEXT DEFAULT 'orb',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_kosher_places_name ON kosher_places(name);
CREATE INDEX IF NOT EXISTS idx_kosher_places_kosher_type ON kosher_places(kosher_type);
CREATE INDEX IF NOT EXISTS idx_kosher_places_listing_type ON kosher_places(listing_type);
CREATE INDEX IF NOT EXISTS idx_kosher_places_source ON kosher_places(source);

-- Create unique constraint to prevent duplicates
CREATE UNIQUE INDEX IF NOT EXISTS idx_kosher_places_name_address 
ON kosher_places(name, address) 
WHERE name IS NOT NULL AND address IS NOT NULL;

-- Add comments for documentation
COMMENT ON TABLE kosher_places IS 'ORB Kosher business listings scraped from category pages';
COMMENT ON COLUMN kosher_places.name IS 'Business name';
COMMENT ON COLUMN kosher_places.photo IS 'URL to business photo/image';
COMMENT ON COLUMN kosher_places.address IS 'Business address';
COMMENT ON COLUMN kosher_places.phone IS 'Business phone number';
COMMENT ON COLUMN kosher_places.website IS 'Business website URL';
COMMENT ON COLUMN kosher_places.kosher_cert_link IS 'Link to kosher certificate PDF';
COMMENT ON COLUMN kosher_places.kosher_type IS 'Kosher type: dairy, meat, pareve, etc.';
COMMENT ON COLUMN kosher_places.listing_type IS 'Listing type: Restaurants, Catering, Markets, etc.';
COMMENT ON COLUMN kosher_places.detail_url IS 'URL to business detail page';
COMMENT ON COLUMN kosher_places.extra_kosher_info IS 'Additional kosher information (Cholov Yisroel, etc.)';
COMMENT ON COLUMN kosher_places.source IS 'Data source (orb, manual, etc.)'; 