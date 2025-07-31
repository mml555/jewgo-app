# Google Places API Quota Setup Guide

## 🚨 Current Issue: API Quota Limit Reached

You've hit the Google Places API quota limit of 25,000 requests per day. This is preventing the hours backup system from working. Here's how to resolve this:

---

## 🔧 Solution: Enable Google Cloud Billing

### **Step 1: Enable Billing on Google Cloud Project**

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account
   - Select your project (or create a new one)

2. **Enable Billing**
   - In the left sidebar, click on "Billing"
   - Click "Link a billing account" or "Create billing account"
   - Add a payment method (credit card required)
   - Enable billing for your project

3. **Verify Billing Status**
   - Go to "Billing" → "Account management"
   - Ensure billing is enabled and active

### **Step 2: Increase API Quotas**

1. **Navigate to APIs & Services**
   - Go to "APIs & Services" → "Quotas"
   - Search for "Places API"

2. **Request Quota Increase**
   - Find "Places API - Text Search requests per day"
   - Click "Edit Quotas"
   - Request increase from 25,000 to 100,000+ requests/day
   - Submit the request (usually approved quickly)

3. **Check Other Quotas**
   - "Places API - Place Details requests per day"
   - "Places API - Nearby Search requests per day"
   - Request increases for these as well

---

## 🔑 Using Signing Secrets for Higher Quotas

### **What are Signing Secrets?**

Signing secrets (also called API keys with billing) allow you to:
- Make more API requests per day
- Access premium features
- Get better rate limits
- Use advanced authentication

### **Step 3: Create New API Key with Billing**

1. **Go to Credentials**
   - Navigate to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"

2. **Configure API Key**
   - Give it a name (e.g., "JewGo Places API")
   - Enable billing for this key
   - Set up restrictions:
     - **Application restrictions**: HTTP referrers
     - **API restrictions**: Places API only

3. **Set Up Restrictions**
   ```
   Application restrictions: HTTP referrers
   Website restrictions: 
   - https://jewgo.vercel.app/*
   - https://jewgo.onrender.com/*
   - localhost:3000/*
   
   API restrictions: Places API
   ```

### **Step 4: Update Environment Variables**

1. **Update Backend Environment**
   ```bash
   # In your backend deployment (Render)
   GOOGLE_PLACES_API_KEY=your_new_api_key_with_billing
   ```

2. **Update Frontend Environment**
   ```bash
   # In your frontend deployment (Vercel)
   GOOGLE_PLACES_API_KEY=your_new_api_key_with_billing
   ```

3. **Update Local Environment**
   ```bash
   export GOOGLE_PLACES_API_KEY='your_new_api_key_with_billing'
   ```

---

## 💰 Cost Analysis

### **Google Places API Pricing (with billing enabled)**

| API Call Type | Cost per 1,000 requests |
|---------------|------------------------|
| Text Search | $0.017 |
| Place Details | $0.017 |
| Nearby Search | $0.017 |

### **Estimated Costs for JewGo**

- **100 restaurants**: ~200 API calls = $0.0034
- **1,000 restaurants**: ~2,000 API calls = $0.034
- **10,000 restaurants**: ~20,000 API calls = $0.34

**Total cost for updating all restaurants**: Less than $1.00

---

## 🚀 Implementation Steps

### **Immediate Actions**

1. **Enable Google Cloud Billing**
   ```bash
   # Follow Steps 1-2 above
   # This will increase your quota to 100,000+ requests/day
   ```

2. **Create New API Key**
   ```bash
   # Follow Step 3 above
   # Create API key with billing enabled
   ```

3. **Update Environment Variables**
   ```bash
   # Update GOOGLE_PLACES_API_KEY in all environments
   ```

4. **Test the New API Key**
   ```bash
   # Test with the quota checker
   python scripts/maintenance/check_google_places_quota.py
   ```

5. **Run Hours Update**
   ```bash
   # Use the quota-aware updater
   python scripts/maintenance/quota_aware_hours_updater.py
   ```

### **Alternative: Use Quota-Aware Updater**

If you can't enable billing immediately, use the quota-aware updater:

```bash
# This will process restaurants until quota is reached
python scripts/maintenance/quota_aware_hours_updater.py

# Choose option 2 and set a limit (e.g., 10 restaurants)
# This will process 10 restaurants and stop gracefully
```

---

## 🔍 Troubleshooting

### **Common Issues**

1. **"API key expired" error**
   - Solution: Create new API key with billing enabled
   - Ensure billing is active on your Google Cloud project

2. **"Quota exceeded" error**
   - Solution: Enable billing and request quota increase
   - Use quota-aware updater to process in batches

3. **"Request denied" error**
   - Check API key restrictions
   - Ensure Places API is enabled
   - Verify billing is active

### **Verification Steps**

1. **Test API Key**
   ```bash
   curl "https://maps.googleapis.com/maps/api/place/textsearch/json?query=Starbucks&key=YOUR_NEW_API_KEY"
   ```

2. **Check Quota Status**
   ```bash
   python scripts/maintenance/check_google_places_quota.py
   ```

3. **Test Hours Updater**
   ```bash
   python scripts/maintenance/quota_aware_hours_updater.py
   # Choose option 4 (test with 3 restaurants)
   ```

---

## 📊 Expected Results

### **After Enabling Billing**

- **Quota Limit**: 25,000 → 100,000+ requests/day
- **Cost**: ~$0.017 per 1,000 requests
- **Hours Coverage**: 0% → 70-90%
- **Processing Speed**: Can process all restaurants in one run

### **Success Metrics**

- ✅ API calls working without "REQUEST_DENIED" errors
- ✅ Hours data being fetched and stored
- ✅ Frontend displaying accurate hours
- ✅ Users seeing improved restaurant information

---

## 🎯 Next Steps

1. **Enable Google Cloud Billing** (Priority 1)
2. **Create new API key with billing** (Priority 1)
3. **Update environment variables** (Priority 1)
4. **Test the system** (Priority 2)
5. **Run full hours update** (Priority 2)
6. **Monitor results** (Priority 3)

---

## 💡 Pro Tips

### **Cost Optimization**

1. **Cache Results**: Store hours data to avoid repeated API calls
2. **Batch Processing**: Process restaurants in batches
3. **Update Frequency**: Only update hours when needed
4. **Error Handling**: Skip restaurants that can't be found

### **Performance Optimization**

1. **Rate Limiting**: Use 200ms delays between requests
2. **Parallel Processing**: Process multiple restaurants simultaneously
3. **Retry Logic**: Retry failed requests with exponential backoff
4. **Monitoring**: Track API usage and costs

---

## 📞 Support

If you encounter issues:

1. **Google Cloud Support**: https://cloud.google.com/support
2. **Places API Documentation**: https://developers.google.com/maps/documentation/places/web-service
3. **Billing Support**: https://cloud.google.com/billing/docs/support

---

**The key is enabling billing - this will immediately solve your quota issues and allow the hours backup system to work properly!** 