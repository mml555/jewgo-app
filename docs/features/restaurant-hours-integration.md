# 🕐 Restaurant Hours Integration & Display

## Overview

This feature allows each restaurant listing to display accurate hours information from Google Places API, including today's hours, weekly schedule, and real-time open/closed status.

## 🗂️ Project Structure

```
/lib/google/places.ts           # Google Places API integration
/lib/utils/hours.ts             # Hours formatting utilities
/db/migrations/hours.sql        # Database schema updates
/db/sync/updateHours.ts         # Hours sync logic
/components/HoursDisplay.tsx    # React component for display
/app/api/admin/update-hours     # API route for manual updates
/scripts/update-hours-cron.js   # Automated CRON job
```

## 🗄️ Database Schema

### New Columns Added

| Column | Type | Description |
|--------|------|-------------|
| `hours_of_operation` | TEXT | Human-readable hours (e.g., "Monday: 11:00 AM – 9:00 PM") |
| `hours_json` | JSONB | Structured hours data from Google Places API |
| `hours_last_updated` | TIMESTAMPTZ | Timestamp of last hours update |
| `timezone` | TEXT | Restaurant's timezone |

### Database View

```sql
CREATE OR REPLACE VIEW restaurant_today_hours AS
SELECT
  id,
  (string_to_array(hours_of_operation, E'\n'))[extract(dow from now()) + 1] AS todays_hours
FROM restaurants;
```

## 🔌 Google Places API Integration

### Function: `fetchPlaceDetails(place_id: string)`

Fetches opening hours and timezone information from Google Places API.

**Returns:**
- `hoursText`: Formatted text for display
- `hoursJson`: Structured data for logic
- `timezone`: Restaurant's timezone

**Example Response:**
```json
{
  "hoursText": "Monday: 11:00 AM – 9:00 PM\nTuesday: 11:00 AM – 9:00 PM",
  "hoursJson": [
    {
      "open": { "day": 1, "time": "1100" },
      "close": { "day": 1, "time": "2100" }
    }
  ],
  "timezone": "America/New_York"
}
```

## 🧠 Utility Functions

### `formatHours(hoursText: string): string[]`
Splits hours text into array of daily schedules.

### `getTodayHours(hoursText: string): string`
Extracts today's hours based on current day of week.

### `isOpenNow(hoursJson: any[]): boolean`
Determines if restaurant is currently open using structured data.

### `formatTime(time: string): string`
Converts 24-hour format to 12-hour display format.

## 💻 Frontend Component

### `HoursDisplay` Component

**Props:**
- `hoursOfOperation?: string` - Formatted hours text
- `hoursJson?: any[]` - Structured hours data
- `hoursLastUpdated?: string` - Last update timestamp

**Features:**
- Shows today's hours prominently
- Displays open/closed status badge
- Expandable dropdown for full week
- Last updated timestamp
- Graceful fallback for missing data

**Usage:**
```tsx
<HoursDisplay 
  hoursOfOperation="Monday: 11:00 AM – 9:00 PM\nTuesday: 11:00 AM – 9:00 PM"
  hoursJson={[/* structured data */]}
  hoursLastUpdated="2024-01-15T10:30:00Z"
/>
```

## 🔄 Sync & Update Logic

### Manual Update
```typescript
await updateRestaurantHours(restaurantId, placeId);
```

### Automated CRON Job
Runs weekly to update stale records:
```bash
# Every Sunday at 2 AM
0 2 * * 0 node scripts/update-hours-cron.js
```

### API Endpoint
`POST /api/admin/update-hours`
```json
{
  "id": 123,
  "placeId": "ChIJ..."
}
```

## 🚀 Implementation Steps

### 1. Database Migration
```bash
psql "$DATABASE_URL" -f db/migrations/hours.sql
```

### 2. Environment Setup
Add to `.env.local`:
```
GOOGLE_API_KEY=your_google_places_api_key
```

### 3. Manual Testing
```bash
# Test API endpoint
curl -X POST http://localhost:3000/api/admin/update-hours \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "placeId": "ChIJ..."}'
```

### 4. CRON Setup
Add to your deployment platform (Vercel, GitHub Actions, etc.):
```yaml
# Example: GitHub Actions
- name: Update Restaurant Hours
  run: node scripts/update-hours-cron.js
  schedule: "0 2 * * 0"  # Every Sunday at 2 AM
```

## 📊 Data Flow

1. **Initial Setup**: Restaurant added with `google_listing_url`
2. **First Sync**: `updateRestaurantHours()` fetches and stores hours
3. **Display**: `HoursDisplay` component shows formatted hours
4. **Auto-Update**: CRON job updates stale records weekly
5. **Manual Update**: Admin can trigger updates via API

## 🔧 Configuration

### Google Places API
- Enable Places API in Google Cloud Console
- Set up API key with appropriate restrictions
- Monitor usage and quotas

### Update Frequency
- Default: 7 days
- Configurable in CRON script
- Manual updates available via API

### Error Handling
- Graceful fallbacks for missing data
- Rate limiting protection
- Comprehensive logging

## 🧪 Testing

### Unit Tests
```bash
# Test utility functions
npm test lib/utils/hours.test.ts

# Test component
npm test components/HoursDisplay.test.tsx
```

### Integration Tests
```bash
# Test API endpoint
npm test app/api/admin/update-hours.test.ts

# Test sync logic
npm test db/sync/updateHours.test.ts
```

## 📈 Monitoring

### Key Metrics
- Hours update success rate
- API call frequency
- Data freshness
- Error rates

### Logging
- Structured logs for all operations
- Error tracking and alerting
- Performance monitoring

## 🔮 Future Enhancements

### Planned Features
- [ ] Holiday hours support
- [ ] Special event hours
- [ ] Timezone-aware display
- [ ] Hours change notifications
- [ ] Bulk update interface

### Performance Optimizations
- [ ] Caching layer for API responses
- [ ] Batch processing for updates
- [ ] CDN for static hours data
- [ ] Progressive loading

## 🆘 Troubleshooting

### Common Issues

**API Rate Limiting**
- Implement exponential backoff
- Increase delay between requests
- Monitor API quotas

**Missing Place IDs**
- Validate `google_listing_url` format
- Extract place_id correctly
- Handle edge cases

**Timezone Issues**
- Use proper timezone mapping
- Handle daylight saving time
- Validate timezone data

### Debug Commands
```bash
# Check current hours data
psql "$DATABASE_URL" -c "SELECT id, hours_of_operation, hours_last_updated FROM restaurants LIMIT 5;"

# Test Google Places API
curl "https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJ...&key=$GOOGLE_API_KEY"

# Run manual update
node scripts/update-hours-cron.js
```

---

*Last Updated: 2024*
*Maintained by: JewGo Development Team* 