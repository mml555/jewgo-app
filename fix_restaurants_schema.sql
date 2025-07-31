-- Fix restaurants table schema to match kosher_places
-- Add missing columns for proper consolidation

-- Add missing columns to restaurants table
ALTER TABLE restaurants 
ADD COLUMN IF NOT EXISTS kosher_cert_link TEXT,
ADD COLUMN IF NOT EXISTS detail_url TEXT,
ADD COLUMN IF NOT EXISTS hours_open TEXT;

-- Update existing records to have proper kosher certification info
UPDATE restaurants 
SET hechsher_details = 'ORB Kosher' 
WHERE hechsher_details IS NULL OR hechsher_details = '';

-- Set all existing restaurants as approved
UPDATE restaurants 
SET status = 'approved' 
WHERE status IS NULL OR status = 'pending_approval';

-- Set all existing restaurants as kosher
UPDATE restaurants 
SET is_kosher = true 
WHERE is_kosher IS NULL;

-- Set all existing restaurants as having hechsher
UPDATE restaurants 
SET is_hechsher = true 
WHERE is_hechsher IS NULL;

-- Normalize kosher_type values
UPDATE restaurants 
SET kosher_type = 'meat' 
WHERE kosher_type = 'Kosher' OR kosher_type IS NULL;

-- Add comments for new columns
COMMENT ON COLUMN restaurants.kosher_cert_link IS 'Link to kosher certificate PDF';
COMMENT ON COLUMN restaurants.detail_url IS 'URL to business detail page';
COMMENT ON COLUMN restaurants.hours_open IS 'Business hours information'; 