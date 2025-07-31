-- Migration: Add Eatery Workflow Schema Updates
-- This migration adds the missing columns needed for the enhanced Add Eatery workflow

-- Add missing columns to the restaurants table
ALTER TABLE restaurants 
ADD COLUMN IF NOT EXISTS short_description TEXT,
ADD COLUMN IF NOT EXISTS email TEXT,
ADD COLUMN IF NOT EXISTS google_listing_url TEXT,
ADD COLUMN IF NOT EXISTS category TEXT DEFAULT 'restaurant',
ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'pending_approval',
ADD COLUMN IF NOT EXISTS is_cholov_yisroel BOOLEAN,
ADD COLUMN IF NOT EXISTS is_pas_yisroel BOOLEAN;

-- Add missing columns to the kosher_places table (if using the simpler schema)
ALTER TABLE kosher_places 
ADD COLUMN IF NOT EXISTS short_description TEXT,
ADD COLUMN IF NOT EXISTS email TEXT,
ADD COLUMN IF NOT EXISTS google_listing_url TEXT,
ADD COLUMN IF NOT EXISTS category TEXT DEFAULT 'restaurant',
ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'pending_approval',
ADD COLUMN IF NOT EXISTS is_cholov_yisroel BOOLEAN,
ADD COLUMN IF NOT EXISTS is_pas_yisroel BOOLEAN,
ADD COLUMN IF NOT EXISTS hours_open TEXT,
ADD COLUMN IF NOT EXISTS price_range TEXT;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_restaurants_status ON restaurants(status);
CREATE INDEX IF NOT EXISTS idx_restaurants_category ON restaurants(category);
CREATE INDEX IF NOT EXISTS idx_restaurants_kosher_category ON restaurants(kosher_category);

-- Create indexes for kosher_places table
CREATE INDEX IF NOT EXISTS idx_kosher_places_status ON kosher_places(status);
CREATE INDEX IF NOT EXISTS idx_kosher_places_category ON kosher_places(category);

-- Add comments for documentation
COMMENT ON COLUMN restaurants.short_description IS 'Brief description for mobile display (max 80 chars)';
COMMENT ON COLUMN restaurants.email IS 'Contact email address';
COMMENT ON COLUMN restaurants.google_listing_url IS 'Link to Google Maps or Google My Business listing';
COMMENT ON COLUMN restaurants.category IS 'Business category (restaurant, bakery, etc.)';
COMMENT ON COLUMN restaurants.status IS 'Submission status: pending_approval, approved, rejected';
COMMENT ON COLUMN restaurants.is_cholov_yisroel IS 'True if Chalav Yisrael, false if Chalav Stam (for dairy)';
COMMENT ON COLUMN restaurants.is_pas_yisroel IS 'True if Pas Yisroel (for meat/pareve)';

-- Optional: Create a separate table for owner information
CREATE TABLE IF NOT EXISTS restaurant_owners (
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for restaurant_owners
CREATE INDEX IF NOT EXISTS idx_restaurant_owners_restaurant_id ON restaurant_owners(restaurant_id);

-- Add comments for restaurant_owners table
COMMENT ON TABLE restaurant_owners IS 'Owner information for restaurant submissions';
COMMENT ON COLUMN restaurant_owners.restaurant_id IS 'Reference to the restaurant';
COMMENT ON COLUMN restaurant_owners.name IS 'Owner name';
COMMENT ON COLUMN restaurant_owners.email IS 'Owner email address';
COMMENT ON COLUMN restaurant_owners.phone IS 'Owner phone number'; 