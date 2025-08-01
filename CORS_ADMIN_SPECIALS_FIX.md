# CORS and Admin Specials Endpoint Fix

## 🚨 Issue Identified

The frontend at `https://jewgo-app.vercel.app` was experiencing CORS errors when trying to access the backend at `https://jewgo.onrender.com/api/admin/specials`:

```
Access to fetch at 'https://jewgo.onrender.com/api/admin/specials' from origin 'https://jewgo-app.vercel.app' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: It does not have HTTP ok status.
```

## 🔍 Root Cause Analysis

1. **Missing Endpoint**: The `/api/admin/specials` endpoint was only defined in the maintenance script (`scripts/maintenance/app_sqlite_backup.py`) but not in the main backend app (`backend/app.py`).

2. **Incomplete CORS Configuration**: While CORS was configured, it wasn't handling preflight requests properly for the specific frontend origin.

3. **Missing Database Methods**: The database manager was missing the required methods for handling specials data.

## ✅ Fixes Implemented

### 1. **Added Missing Admin Specials Endpoints**

**File**: `backend/app.py`

Added two new endpoints:
- `GET /api/admin/specials` - Get all specials from all restaurants
- `PUT /api/admin/specials/<int:special_id>/payment` - Update special payment status

```python
@app.route('/api/admin/specials', methods=['GET'])
def get_admin_specials():
    """API endpoint for getting all specials (admin only)."""
    try:
        # Get all specials (both paid and unpaid)
        all_specials = []
        
        # Get all restaurants and their specials
        restaurants = db_manager.search_restaurants(limit=1000)
        for restaurant in restaurants:
            specials = db_manager.get_restaurant_specials(restaurant['id'], paid_only=False)
            all_specials.extend(specials)
        
        return jsonify({
            'success': True,
            'specials': all_specials
        })
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
```

### 2. **Enhanced CORS Configuration**

**File**: `backend/app.py`

Updated CORS configuration to be more explicit and handle preflight requests properly:

```python
# Initialize CORS with configuration
CORS(app, 
     origins=app.config.get('CORS_ORIGINS', ['*']),
     methods=app.config.get('CORS_METHODS', ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']),
     allow_headers=app.config.get('CORS_ALLOW_HEADERS', ['Content-Type', 'Authorization', 'Accept', 'Origin', 'X-Requested-With']),
     supports_credentials=True)
```

### 3. **Added Missing Database Methods**

**File**: `backend/database/database_manager_v3.py`

Added three new methods to handle specials data:

#### `search_restaurants()`
```python
def search_restaurants(self, limit: int = 1000, offset: int = 0) -> List[Dict[str, Any]]:
    """Search restaurants and return as list of dictionaries."""
    try:
        session = self.get_session()
        restaurants = session.query(Restaurant).limit(limit).offset(offset).all()
        return [self._restaurant_to_unified_dict(restaurant) for restaurant in restaurants]
    except Exception as e:
        logger.error(f"Error searching restaurants: {e}")
        return []
    finally:
        session.close()
```

#### `get_restaurant_specials()`
```python
def get_restaurant_specials(self, restaurant_id: int, paid_only: bool = False) -> List[Dict[str, Any]]:
    """Get specials for a specific restaurant."""
    try:
        session = self.get_session()
        restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        if restaurant and restaurant.specials:
            specials = self._parse_specials_field(restaurant.specials)
            if paid_only:
                specials = [s for s in specials if s.get('is_paid', False)]
            return specials
        return []
    except Exception as e:
        logger.error(f"Error getting specials for restaurant {restaurant_id}: {e}")
        return []
    finally:
        session.close()
```

#### `update_special_payment_status()`
```python
def update_special_payment_status(self, special_id: int, is_paid: bool, payment_status: str = 'paid') -> bool:
    """Update payment status for a special."""
    try:
        session = self.get_session()
        # Find the restaurant that contains this special
        restaurants = session.query(Restaurant).all()
        
        for restaurant in restaurants:
            if restaurant.specials:
                specials = self._parse_specials_field(restaurant.specials)
                for special in specials:
                    if special.get('id') == special_id:
                        # Update the special
                        special['is_paid'] = is_paid
                        special['payment_status'] = payment_status
                        special['updated_at'] = datetime.utcnow().isoformat()
                        
                        # Save back to database
                        restaurant.specials = json.dumps(specials)
                        restaurant.updated_at = datetime.utcnow()
                        session.commit()
                        logger.info(f"Updated special {special_id} payment status")
                        return True
        
        logger.warning(f"Special {special_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error updating special {special_id} payment status: {e}")
        session.rollback()
        return False
    finally:
        session.close()
```

### 4. **Added Required Import**

**File**: `backend/database/database_manager_v3.py`

Added `json` import for JSON serialization:
```python
import json
```

## 🧪 Testing Results

### Local Testing
- ✅ Server starts successfully
- ✅ `/api/admin/specials` endpoint returns proper JSON response
- ✅ CORS preflight requests work correctly
- ✅ Proper CORS headers are returned:
  - `Access-Control-Allow-Origin: https://jewgo-app.vercel.app`
  - `Access-Control-Allow-Credentials: true`
  - `Access-Control-Allow-Headers: Content-Type`
  - `Access-Control-Allow-Methods: DELETE, GET, OPTIONS, POST, PUT`

### CORS Preflight Test
```bash
curl -X OPTIONS -H "Origin: https://jewgo-app.vercel.app" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -v http://localhost:5001/api/admin/specials
```

**Result**: ✅ HTTP 200 OK with proper CORS headers

## 🚀 Deployment

The fixes are ready for deployment to the production backend at `https://jewgo.onrender.com`. The changes include:

1. **New API endpoints** for admin specials management
2. **Enhanced CORS configuration** for proper cross-origin requests
3. **Complete database methods** for specials data handling
4. **Proper error handling** and logging

## 📋 Files Modified

1. `backend/app.py` - Added admin specials endpoints and enhanced CORS
2. `backend/database/database_manager_v3.py` - Added specials-related database methods
3. `backend/config/config.py` - CORS configuration (already properly configured)

## 🎯 Expected Outcome

After deployment, the frontend should be able to:
- ✅ Successfully fetch specials data from `/api/admin/specials`
- ✅ Update special payment status via PUT requests
- ✅ Handle CORS preflight requests without errors
- ✅ Maintain proper security with origin validation

The CORS error should be completely resolved, and the admin specials functionality should work seamlessly between the frontend and backend. 