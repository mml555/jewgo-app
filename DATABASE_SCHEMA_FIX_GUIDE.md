# 🔧 Database Schema Fix Guide

**Issue:** The production backend is failing with the error:
```
column restaurants.google_rating does not exist
```

**Root Cause:** The database schema is missing the Google reviews columns that were added to the code but not migrated to the production database.

**Solution:** Run the deployment schema fix script on the production server.

---

## 🚀 **Quick Fix (Recommended)**

### **Step 1: Access the Production Server**

The backend is deployed on Render at: `https://jewgo.onrender.com`

### **Step 2: Run the Schema Fix Script**

1. **SSH into the Render server** (if you have access)
2. **Navigate to the project directory**
3. **Run the fix script:**

```bash
python deploy_schema_fix.py
```

### **Step 3: Verify the Fix**

The script will automatically:
- ✅ Connect to the database
- ✅ Add missing columns (`google_rating`, `google_review_count`, `google_reviews`)
- ✅ Update existing records with default values
- ✅ Run health checks
- ✅ Verify the fix worked

---

## 🔍 **Alternative Methods**

### **Method 1: Render Console (If SSH not available)**

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Navigate to your JewGo service
3. Go to **Shell** tab
4. Run: `python deploy_schema_fix.py`

### **Method 2: Manual SQL Commands**

If you have direct database access, run these SQL commands:

```sql
-- Add missing columns
ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS google_rating FLOAT;
ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS google_review_count INTEGER;
ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS google_reviews TEXT;

-- Update existing records
UPDATE restaurants 
SET google_rating = rating,
    google_review_count = review_count,
    google_reviews = '[]'
WHERE google_rating IS NULL 
   OR google_review_count IS NULL 
   OR google_reviews IS NULL;
```

### **Method 3: Redeploy with Schema Migration**

1. Add the schema fix to your deployment process
2. Redeploy the application
3. The fix will run automatically during deployment

---

## 📊 **What the Fix Does**

### **Columns Added:**
- `google_rating` (FLOAT) - Google Places rating
- `google_review_count` (INTEGER) - Number of Google reviews
- `google_reviews` (TEXT) - JSON string of review data

### **Data Migration:**
- Existing restaurants get default values:
  - `google_rating` = existing `rating`
  - `google_review_count` = existing `review_count`
  - `google_reviews` = `'[]'` (empty array)

### **Verification:**
- Tests database connectivity
- Verifies columns exist
- Runs sample queries
- Confirms API functionality

---

## 🛠️ **Troubleshooting**

### **If the script fails:**

1. **Check environment variables:**
   ```bash
   echo $DATABASE_URL
   ```

2. **Test database connection:**
   ```bash
   python -c "import psycopg2; print('Database connection test')"
   ```

3. **Check permissions:**
   - Ensure the database user has ALTER TABLE permissions
   - Verify the DATABASE_URL is correct

### **If columns already exist:**
- The script will skip adding existing columns
- It will still update any NULL values with defaults

### **If you get permission errors:**
- Contact your database administrator
- Ensure the user has schema modification rights

---

## 🔄 **Post-Fix Verification**

### **Check API Endpoints:**

1. **Health Check:**
   ```bash
   curl https://jewgo.onrender.com/health
   ```

2. **Restaurants API:**
   ```bash
   curl https://jewgo.onrender.com/api/restaurants?limit=1
   ```

3. **Expected Response:**
   ```json
   {
     "restaurants": [
       {
         "id": 1,
         "name": "Restaurant Name",
         "google_rating": 4.5,
         "google_review_count": 100,
         "google_reviews": "[]"
       }
     ]
   }
   ```

### **Monitor Logs:**
- Check Render logs for any remaining errors
- Verify the API is responding correctly
- Monitor for any new issues

---

## 📈 **Performance Impact**

### **During Fix:**
- ⚠️ **Brief downtime** (1-2 minutes)
- 🔒 **Table locks** during ALTER operations
- 📊 **Data migration** for existing records

### **After Fix:**
- ✅ **Improved performance** with proper schema
- ✅ **No more column errors**
- ✅ **Full API functionality restored**

---

## 🚨 **Emergency Rollback**

If something goes wrong, you can rollback:

```sql
-- Remove the added columns (if needed)
ALTER TABLE restaurants DROP COLUMN IF EXISTS google_rating;
ALTER TABLE restaurants DROP COLUMN IF EXISTS google_review_count;
ALTER TABLE restaurants DROP COLUMN IF EXISTS google_reviews;
```

---

## 📞 **Support**

If you encounter issues:

1. **Check the logs** in Render dashboard
2. **Verify environment variables** are set correctly
3. **Test database connectivity** manually
4. **Contact support** if the issue persists

---

## ✅ **Success Criteria**

The fix is successful when:

- ✅ No more `column restaurants.google_rating does not exist` errors
- ✅ API endpoints return 200 status codes
- ✅ Restaurant data includes Google review fields
- ✅ Health check endpoint works
- ✅ Frontend can fetch restaurant data

---

**🎉 Once completed, your JewGo application will be fully functional with the new Google reviews features!** 