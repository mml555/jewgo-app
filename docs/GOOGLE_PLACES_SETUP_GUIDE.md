# Google Places API Setup Guide

This guide will help you set up Google Places API to automatically update missing zip codes and address information for restaurants.

## 🔑 Getting a Google Places API Key

### 1. Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable billing for your project (required for API usage)

### 2. Enable the Places API
1. Go to the [APIs & Services > Library](https://console.cloud.google.com/apis/library)
2. Search for "Places API"
3. Click on "Places API" and click "Enable"

### 3. Create API Credentials
1. Go to [APIs & Services > Credentials](https://console.cloud.google.com/apis/credentials)
2. Click "Create Credentials" > "API Key"
3. Copy your API key
4. **Important**: Restrict the API key to only Places API for security

### 4. Set Up API Key Restrictions
1. Click on your API key to edit it
2. Under "Application restrictions", select "HTTP referrers" or "IP addresses"
3. Under "API restrictions", select "Restrict key" and choose "Places API"
4. Save the changes

## 🚀 Setting Up the Address Updater

### 1. Install Required Dependencies
```bash
pip install requests
```

### 2. Set Environment Variable
```bash
export GOOGLE_PLACES_API_KEY='your_api_key_here'
```

### 3. Test the Setup
```bash
python test_address_updater.py
```

This will test the API with "26 Sushi and wok" restaurant.

### 4. View Restaurants with Missing Zip Codes
```bash
python test_address_updater.py list
```

This will show all restaurants that need zip code updates.

## 🔧 Running the Address Updater

### 1. Test Run (10 restaurants)
```bash
python google_places_address_updater.py
```

### 2. Full Run (all restaurants)
Edit the script and change `limit=10` to `limit=None` in the `main()` function.

## 📊 What the Updater Does

### Searches for Missing Information:
- **Zip Codes**: Finds missing postal codes
- **Addresses**: Gets properly formatted addresses
- **Ratings**: Updates Google ratings and review counts
- **Websites**: Finds official restaurant websites
- **Phone Numbers**: Gets formatted phone numbers

### Example Update:
**Before:**
```
Name: 26 Sushi and wok
Address: 9487 Harding Ave, Surfside, FL (Zip code not available)
```

**After:**
```
Name: 26 Sushi and wok
Address: 9487 Harding Ave, Surfside, FL 33154
Rating: 4.2 (150 reviews)
Website: https://26sushi.com
Phone: (305) 123-4567
```

## ⚠️ Important Notes

### Rate Limiting
- Google Places API has rate limits
- The script includes 100ms delays between requests
- Process restaurants in batches to avoid hitting limits

### API Costs
- Google Places API has usage costs
- Text Search: $0.017 per request
- Place Details: $0.017 per request
- Monitor usage in Google Cloud Console

### Data Accuracy
- Google Places data is generally very accurate
- Cross-reference with existing data before updating
- Some restaurants might not be found if names don't match exactly

## 🛠️ Customization

### Modify Search Queries
Edit the `search_place_by_address` method to improve search accuracy:

```python
# Add more specific search terms
search_query = f"{name} restaurant, {address}, {city}, {state}"
```

### Add More Fields
Extract additional information from Google Places:

```python
# Add to the fields parameter in get_place_details
'fields': 'address_components,website,formatted_phone_number,opening_hours,price_level,types'
```

### Filter Results
Add logic to filter results based on confidence:

```python
# Check if the result is likely the correct restaurant
if place.get('rating', 0) > 3.0 and 'restaurant' in place.get('types', []):
    # Proceed with update
```

## 📈 Monitoring and Reports

The script generates a report file `address_update_report.txt` with:
- Total restaurants processed
- Successfully updated count
- Not found count
- Error count
- Success rate percentage

## 🔒 Security Best Practices

1. **Never commit API keys to version control**
2. **Use environment variables for API keys**
3. **Restrict API keys to specific IPs/domains**
4. **Monitor API usage regularly**
5. **Set up billing alerts**

## 🆘 Troubleshooting

### Common Issues:

1. **"API key not valid"**
   - Check if the API key is correct
   - Ensure Places API is enabled
   - Verify API key restrictions

2. **"Quota exceeded"**
   - Wait for quota reset (usually daily)
   - Reduce batch size
   - Check billing status

3. **"No results found"**
   - Restaurant name might not match exactly
   - Try different search variations
   - Check if restaurant exists in Google Places

4. **"Database connection error"**
   - Ensure `restaurants.db` exists
   - Check file permissions
   - Verify database schema

## 📞 Support

If you encounter issues:
1. Check the Google Places API documentation
2. Review the error logs in the console output
3. Verify your API key and billing setup
4. Test with a single restaurant first 