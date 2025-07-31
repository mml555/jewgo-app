# 🧪 Testing Real Restaurant Hours Integration

## Overview

This guide will help you test the restaurant hours integration with real Google Places API data using your "My Project 29915" setup.

## Prerequisites

- ✅ Google Places API key from "My Project 29915"
- ✅ API key has Places API enabled
- ✅ Billing enabled on Google Cloud project
- ✅ API key restrictions configured (if needed)

## Step 1: Test Your API Key

### Option A: Quick Test (Shell Script)

1. Edit the `test_api_key.sh` file:
   ```bash
   nano test_api_key.sh
   ```

2. Replace `YOUR_API_KEY` with your actual API key:
   ```bash
   API_KEY="AIzaSyC..."  # Your actual key here
   ```

3. Make the script executable and run it:
   ```bash
   chmod +x test_api_key.sh
   ./test_api_key.sh
   ```

### Option B: Python Test (More Detailed)

1. Edit the `test_real_restaurant_hours.py` file:
   ```bash
   nano test_real_restaurant_hours.py
   ```

2. Replace the API key at the top:
   ```python
   GOOGLE_API_KEY = "AIzaSyC..."  # Your actual key here
   ```

3. Run the test:
   ```bash
   python3 test_real_restaurant_hours.py
   ```

## Step 2: Expected Results

### ✅ Successful API Test
```
🔍 Testing Google Places API Connection
==================================================
📊 API Response Status: OK
✅ Restaurant: McDonald's
🕐 Open Now: true
📅 Weekday Text:
   Monday: 6:00 AM – 12:00 AM
   Tuesday: 6:00 AM – 12:00 AM
   Wednesday: 6:00 AM – 12:00 AM
   ...
🌍 UTC Offset: -300 minutes
```

### ✅ Successful Restaurant Search
```
🍽️  Searching for Kosher Restaurants in Miami
==================================================
📊 Found 20 restaurants

1. Kosher Kingdom
   📍 123 Main St, Miami, FL
   🆔 Place ID: ChIJ...
   ⭐ Rating: 4.2
   🟢 Currently Open
```

## Step 3: Test Backend Integration

Once your API key is working, test the backend integration:

### Test Hours Update Endpoint

```bash
# Test with a real restaurant place_id
curl -X POST https://jewgo.onrender.com/api/admin/update-hours \
  -H "Content-Type: application/json" \
  -d '{
    "id": 833,
    "placeId": "ChIJ..."  # Real place_id from search results
  }'
```

### Expected Response
```json
{
  "success": true,
  "message": "Hours updated successfully",
  "restaurant_id": 833,
  "hours_updated": true,
  "timezone": "America/New_York"
}
```

## Step 4: Verify Frontend Display

1. Visit your deployed frontend: `https://jewgo-app.vercel.app`
2. Navigate to a restaurant page (e.g., `/restaurant/833`)
3. Check the hours section for:
   - ✅ Today's hours displayed
   - ✅ Open/closed status badge
   - ✅ Expandable weekly schedule
   - ✅ Last updated timestamp

## Step 5: Test with Real Kosher Restaurants

### Find Real Kosher Restaurants

Use the Python script to search for real kosher restaurants:

```python
# The script will automatically search for:
# "kosher restaurant miami"
# "kosher deli miami beach"
# "jewish restaurant miami"
```

### Test Multiple Restaurants

1. **Kosher Kingdom** (if found)
2. **Miami Kosher Market**
3. **Kosher Pizza Place**
4. **Jewish Deli**

## Step 6: Troubleshooting

### Common Issues

#### 1. "REQUEST_DENIED" Error
**Solution:**
- Check API key is correct
- Verify Places API is enabled
- Check API key restrictions
- Ensure billing is enabled

#### 2. "QUOTA_EXCEEDED" Error
**Solution:**
- Check current usage in Google Cloud Console
- Wait for quota reset (usually daily)
- Consider upgrading quota limits

#### 3. "ZERO_RESULTS" Error
**Solution:**
- Try different search terms
- Check location/address
- Verify restaurant exists on Google Maps

#### 4. Backend Update Fails
**Solution:**
- Check if restaurant ID exists in database
- Verify place_id is valid
- Check backend logs for errors

### Debug Commands

```bash
# Test API key directly
curl "https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJN1t_tDeuEmsRUsoyG83frY4&fields=name&key=YOUR_API_KEY"

# Check backend status
curl https://jewgo.onrender.com/api/restaurants?limit=1

# Test hours update endpoint
curl -X POST https://jewgo.onrender.com/api/admin/update-hours \
  -H "Content-Type: application/json" \
  -d '{"id": 833, "placeId": "test"}'
```

## Step 7: Production Testing

### Test Scenarios

1. **Real Restaurant Hours**
   - Find a real kosher restaurant
   - Update its hours via API
   - Verify display on frontend

2. **Multiple Updates**
   - Update several restaurants
   - Check for rate limiting
   - Verify data consistency

3. **Error Handling**
   - Test with invalid place_id
   - Test with non-existent restaurant
   - Verify graceful error handling

4. **Performance**
   - Test response times
   - Check database updates
   - Monitor API usage

## Step 8: Monitor and Optimize

### Monitor API Usage

1. Go to Google Cloud Console
2. Navigate to "APIs & Services" → "Quotas"
3. Monitor Places API usage
4. Set up billing alerts

### Optimize for Production

1. **Cache Results**: Store hours for 7 days
2. **Batch Updates**: Update multiple restaurants together
3. **Rate Limiting**: Add delays between requests
4. **Error Recovery**: Implement retry logic

## Success Criteria

### ✅ API Integration
- [ ] API key works correctly
- [ ] Can search for restaurants
- [ ] Can retrieve hours data
- [ ] Backend update endpoint works

### ✅ Frontend Display
- [ ] Hours display correctly
- [ ] Open/closed status accurate
- [ ] Weekly schedule expandable
- [ ] Mobile responsive

### ✅ Data Quality
- [ ] Hours data is accurate
- [ ] Timezone handling correct
- [ ] Last updated timestamps work
- [ ] Error handling graceful

### ✅ Performance
- [ ] API responses under 2 seconds
- [ ] Frontend loads quickly
- [ ] Database updates efficient
- [ ] No memory leaks

## Next Steps

Once testing is complete:

1. **Deploy to Production**: Configure API key in production environment
2. **Set Up Monitoring**: Monitor API usage and errors
3. **Automate Updates**: Set up CRON jobs for regular updates
4. **User Feedback**: Gather feedback on hours display
5. **Optimize**: Based on usage patterns and feedback

---

**Test Date:** 2025-07-31  
**Project:** My Project 29915  
**Status:** Ready for Testing  
**Maintained by:** JewGo Development Team 