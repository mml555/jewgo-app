ALTER TABLE restaurants
  ADD COLUMN IF NOT EXISTS hours_of_operation TEXT,
  ADD COLUMN IF NOT EXISTS hours_json JSONB,
  ADD COLUMN IF NOT EXISTS hours_last_updated TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS timezone TEXT;

-- Optional view for today’s display
CREATE OR REPLACE VIEW restaurant_today_hours AS
SELECT
  id,
  (regexp_split_to_table(hours_of_operation, E'\n'))[extract(dow from now()) + 1] AS todays_hours
FROM restaurants;