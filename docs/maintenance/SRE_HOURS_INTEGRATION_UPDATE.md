# 🚀 SRE Update: Restaurant Hours Integration & Display System

## 📋 Overview

This document outlines the Site Reliability Engineering (SRE) updates required to support the new Restaurant Hours Integration & Display system.

## 🗄️ Database Changes

### New Columns Added
- `hours_of_operation` (TEXT) - Human-readable hours format
- `hours_json` (JSONB) - Structured hours data from Google Places API
- `hours_last_updated` (TIMESTAMPTZ) - Timestamp of last update
- `timezone` (TEXT) - Restaurant's timezone

### Database View Created
```sql
CREATE OR REPLACE VIEW restaurant_today_hours AS
SELECT
  id,
  (string_to_array(hours_of_operation, E'\n'))[extract(dow from now()) + 1] AS todays_hours
FROM restaurants;
```

### Migration Status
✅ **COMPLETED** - Migration applied successfully to production database

## 🔧 Environment Configuration

### Required Environment Variables
```bash
# Google Places API
GOOGLE_API_KEY=your_google_places_api_key

# Database (already configured)
DATABASE_URL=postgresql://...
```

### API Key Setup
1. Enable Google Places API in Google Cloud Console
2. Create API key with appropriate restrictions
3. Set up billing (required for Places API)
4. Monitor usage quotas

## 📊 Monitoring & Alerting

### Key Metrics to Monitor

#### Database Performance
```sql
-- Monitor hours data freshness
SELECT 
  COUNT(*) as total_restaurants,
  COUNT(hours_last_updated) as with_hours,
  AVG(EXTRACT(EPOCH FROM (NOW() - hours_last_updated))/86400) as avg_days_since_update
FROM restaurants;

-- Monitor hours update frequency
SELECT 
  DATE(hours_last_updated) as update_date,
  COUNT(*) as restaurants_updated
FROM restaurants 
WHERE hours_last_updated IS NOT NULL
GROUP BY DATE(hours_last_updated)
ORDER BY update_date DESC;
```

#### API Performance
- Google Places API response times
- API quota usage
- Error rates for hours fetching
- Rate limiting incidents

#### Application Performance
- Hours display component load times
- API endpoint response times (`/api/admin/update-hours`)
- CRON job execution success rate

### Alerting Rules

#### Critical Alerts
```yaml
# Database connectivity
- alert: DatabaseConnectionFailed
  expr: up{job="database"} == 0
  for: 1m
  labels:
    severity: critical

# Google Places API quota exceeded
- alert: GooglePlacesAPIQuotaExceeded
  expr: google_places_api_quota_usage > 0.9
  for: 5m
  labels:
    severity: warning

# Hours update job failure
- alert: HoursUpdateJobFailed
  expr: hours_update_job_success_rate < 0.8
  for: 1h
  labels:
    severity: warning
```

#### Warning Alerts
```yaml
# Stale hours data
- alert: StaleHoursData
  expr: avg_days_since_hours_update > 7
  for: 2h
  labels:
    severity: warning

# High API error rate
- alert: HighHoursAPIErrorRate
  expr: rate(hours_api_errors_total[5m]) > 0.1
  for: 10m
  labels:
    severity: warning
```

## 🔄 Automated Processes

### CRON Job Configuration
```bash
# Weekly hours update (every Sunday at 2 AM)
0 2 * * 0 cd /path/to/jewgo-app && node frontend/scripts/update-hours-cron.js

# Daily health check
0 6 * * * cd /path/to/jewgo-app && node scripts/health-check.js
```

### GitHub Actions (Alternative)
```yaml
name: Update Restaurant Hours
on:
  schedule:
    - cron: '0 2 * * 0'  # Every Sunday at 2 AM
  workflow_dispatch:  # Manual trigger

jobs:
  update-hours:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - run: node frontend/scripts/update-hours-cron.js
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
```

## 🧪 Health Checks

### Database Health
```sql
-- Check hours data integrity
SELECT 
  COUNT(*) as total_restaurants,
  COUNT(hours_of_operation) as with_hours_text,
  COUNT(hours_json) as with_hours_json,
  COUNT(timezone) as with_timezone
FROM restaurants;

-- Check for invalid JSON in hours_json
SELECT id, hours_json 
FROM restaurants 
WHERE hours_json IS NOT NULL 
  AND hours_json::text NOT LIKE '[%]';
```

### API Health
```bash
# Test hours update endpoint
curl -X POST http://localhost:3000/api/admin/update-hours \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "placeId": "test"}'

# Test Google Places API
curl "https://maps.googleapis.com/maps/api/place/details/json?place_id=test&key=$GOOGLE_API_KEY"
```

### Application Health
```bash
# Test hours display component
npm test components/HoursDisplay.test.tsx

# Test utility functions
npm test lib/utils/hours.test.ts
```

## 📈 Performance Optimization

### Database Indexes
```sql
-- Index for hours update queries
CREATE INDEX IF NOT EXISTS idx_restaurants_hours_last_updated 
ON restaurants(hours_last_updated);

-- Index for timezone-based queries
CREATE INDEX IF NOT EXISTS idx_restaurants_timezone 
ON restaurants(timezone);

-- Composite index for efficient hours updates
CREATE INDEX IF NOT EXISTS idx_restaurants_hours_update 
ON restaurants(hours_last_updated, google_listing_url) 
WHERE google_listing_url IS NOT NULL;
```

### Caching Strategy
```typescript
// Cache hours data for 1 hour
const HOURS_CACHE_TTL = 60 * 60 * 1000; // 1 hour

// Redis cache key pattern
const HOURS_CACHE_KEY = (restaurantId: number) => 
  `restaurant:hours:${restaurantId}`;
```

### Rate Limiting
```typescript
// Google Places API rate limiting
const RATE_LIMIT = {
  requestsPerMinute: 60,
  requestsPerDay: 1000,
  delayBetweenRequests: 100 // ms
};
```

## 🚨 Incident Response

### Common Issues & Solutions

#### 1. Google Places API Quota Exceeded
**Symptoms:** 403 errors, "quota exceeded" messages
**Solutions:**
- Check API usage in Google Cloud Console
- Implement exponential backoff
- Consider upgrading API quota
- Cache responses to reduce API calls

#### 2. Database Connection Issues
**Symptoms:** Connection timeouts, connection pool exhaustion
**Solutions:**
- Check database server status
- Monitor connection pool usage
- Implement connection retry logic
- Scale database resources if needed

#### 3. Hours Data Inconsistency
**Symptoms:** Missing hours, incorrect timezone data
**Solutions:**
- Run data validation queries
- Trigger manual hours update
- Check Google Places API response quality
- Implement data validation rules

#### 4. CRON Job Failures
**Symptoms:** Hours not updating automatically
**Solutions:**
- Check CRON job logs
- Verify environment variables
- Test job manually
- Implement job monitoring

### Escalation Procedures
1. **Level 1:** Automated alerts and self-healing
2. **Level 2:** On-call engineer notification
3. **Level 3:** Team lead escalation
4. **Level 4:** Emergency response team

## 📊 Metrics Dashboard

### Grafana Dashboard Queries
```sql
-- Hours Update Success Rate
SELECT 
  DATE(hours_last_updated) as date,
  COUNT(*) as updates
FROM restaurants 
WHERE hours_last_updated >= NOW() - INTERVAL '7 days'
GROUP BY DATE(hours_last_updated)
ORDER BY date;

-- API Response Times
SELECT 
  AVG(response_time) as avg_response_time,
  MAX(response_time) as max_response_time,
  COUNT(*) as total_requests
FROM api_logs 
WHERE endpoint = '/api/admin/update-hours'
  AND timestamp >= NOW() - INTERVAL '1 hour';
```

## 🔮 Future Enhancements

### Planned SRE Improvements
- [ ] Implement circuit breaker for Google Places API
- [ ] Add distributed tracing for hours update requests
- [ ] Create automated rollback procedures
- [ ] Implement A/B testing for hours display
- [ ] Add predictive scaling based on usage patterns

### Performance Targets
- Hours update success rate: >95%
- API response time: <500ms
- Database query performance: <100ms
- CRON job reliability: >99%

## 📞 Contact Information

### On-Call Schedule
- **Primary:** [On-call engineer]
- **Secondary:** [Backup engineer]
- **Escalation:** [Team lead]

### Communication Channels
- **Slack:** #jewgo-sre
- **Email:** sre@jewgo.com
- **PagerDuty:** JewGo SRE Team

---

**Last Updated:** 2024  
**Next Review:** 2024 (monthly)  
**Maintained by:** JewGo SRE Team 