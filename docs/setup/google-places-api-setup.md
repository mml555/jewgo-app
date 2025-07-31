# 🔑 Google Places API Setup Guide

## Overview

This guide will help you set up Google Places API to enable automatic restaurant hours updates for the JewGo application.

## Prerequisites

- Google Cloud Console account
- Billing enabled on Google Cloud project
- Access to environment variables for deployment

## Step-by-Step Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name: `jewgo-restaurant-hours`
4. Click "Create"

### 2. Enable Required APIs

1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for and enable these APIs:
   - **Places API** (required for hours data)
   - **Maps JavaScript API** (optional, for maps integration)
   - **Geocoding API** (optional, for address validation)

### 3. Create API Key

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "API Key"
3. Copy the generated API key

### 4. Configure API Key Restrictions

1. Click on the created API key
2. Under "Application restrictions", select "HTTP referrers (web sites)"
3. Add your domain: `*.jewgo-app.vercel.app`
4. Under "API restrictions", select "Restrict key"
5. Select only the APIs you enabled:
   - Places API
   - Maps JavaScript API (if enabled)
   - Geocoding API (if enabled)

### 5. Set Up Billing

1. Go to "Billing" in the Google Cloud Console
2. Link a billing account to your project
3. **Important**: Google Places API requires billing to be enabled

### 6. Configure Environment Variables

#### For Production (Vercel)

1. Go to your Vercel project dashboard
2. Navigate to "Settings" → "Environment Variables"
3. Add the following variable:
   ```
   Name: GOOGLE_PLACES_API_KEY
   Value: [your-api-key-here]
   Environment: Production
   ```

#### For Development (Local)

1. Create or update `.env.local` file in the frontend directory:
   ```bash
   GOOGLE_PLACES_API_KEY=your-api-key-here
   ```

2. Create or update `.env` file in the backend directory:
   ```bash
   GOOGLE_PLACES_API_KEY=your-api-key-here
   ```

### 7. Test the API

You can test the API setup using our test scripts:

```bash
# Quick test (no database required)
cd "/Users/mendell/jewgo app"
source backend/venv_py311/bin/activate
python scripts/testing/quick_google_places_test.py

# Comprehensive test with real restaurant data
python scripts/testing/test_real_restaurant_data.py
```

Expected response from quick test:
```
🔍 Google Places API Quick Test
==================================================
✅ Google Places API Key found
🔑 Testing API Key Validity...
   ✅ API Key is valid
📊 Test 1/5
🏪 Testing: McDonald's
📍 Address: 123 Main St, Miami, FL 33101
--------------------------------------------------
1. 🔍 Searching for place...
   Status: OK
   ✅ Found Place ID: ChIJ...
   📍 Google Name: McDonald's
   🏠 Google Address: 123 Main St, Miami, FL 33101
   📞 Phone: (305) 555-0123
   ⭐ Rating: 4.2
   💰 Price Level: 1
```

## Troubleshooting

### Common Issues

#### 1. "API key expired" Error
- **Solution**: Create a new API key in Google Cloud Console
- Go to "APIs & Services" → "Credentials"
- Click "Create Credentials" → "API Key"
- Update your environment variables with the new key

#### 2. "API key not valid" Error
- Check if API key is correctly set in environment variables
- Verify API key restrictions allow your domain
- Ensure billing is enabled

#### 3. "Quota exceeded" Error
- Check current usage in Google Cloud Console
- Implement rate limiting in your application
- Consider upgrading quota limits

#### 4. "Place not found" Error
- Verify the place_id is correct
- Check if the place exists in Google Places
- Use Google Places API to search for correct place_id

#### 5. "Billing not enabled" Error
- Enable billing in Google Cloud Console
- Link a payment method
- Wait for billing to activate (may take a few minutes)

### Debug Commands

```bash
# Test API key validity
curl "https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJN1t_tDeuEmsRUsoyG83frY4&fields=name&key=YOUR_API_KEY"

# Check quota usage
# Go to Google Cloud Console → APIs & Services → Quotas
```

## Current Status

**⚠️ IMPORTANT**: The current API key is expired and needs to be replaced.

**Next Steps**:
1. Create a new API key in Google Cloud Console
2. Update environment variables
3. Test with the quick test script
4. Run comprehensive test with real restaurant data

## Usage in JewGo Application

### Automatic Hours Updates

The application will automatically:
1. Fetch restaurant hours from Google Places API
2. Update the database with current hours
3. Display real-time open/closed status
4. Show weekly schedules

### Manual Hours Update

Admins can manually update hours via the API:

```bash
curl -X POST https://jewgo.onrender.com/api/admin/update-hours \
  -H "Content-Type: application/json" \
  -d '{
    "id": 833,
    "placeId": "ChIJN1t_tDeuEmsRUsoyG83frY4"
  }'
```

### CRON Job Setup

Set up automated updates:

```bash
# Add to crontab (updates every Sunday at 2 AM)
0 2 * * 0 cd /path/to/jewgo-app && node frontend/scripts/update-hours-cron.js
```

## Cost Management

### Pricing (as of 2024)

- **Places API Details**: $17 per 1000 requests
- **Typical Usage**: ~100 requests per week for 50 restaurants
- **Estimated Cost**: ~$0.88 per month

### Cost Optimization

1. **Cache Results**: Store hours data for 7 days
2. **Batch Updates**: Update multiple restaurants in one session
3. **Monitor Usage**: Set up billing alerts
4. **Rate Limiting**: Implement delays between requests

### Billing Alerts

1. Go to "Billing" → "Budgets & alerts"
2. Create budget with alerts at:
   - $5/month (warning)
   - $10/month (critical)

## Security Best Practices

1. **Never expose API key in client-side code**
2. **Use environment variables for all deployments**
3. **Restrict API key to specific domains**
4. **Monitor API usage regularly**
5. **Rotate API keys periodically**

## Support

- [Google Places API Documentation](https://developers.google.com/maps/documentation/places/web-service)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Places API Pricing](https://developers.google.com/maps/pricing)

---

**Last Updated:** 2024  
**Maintained by:** JewGo Development Team 