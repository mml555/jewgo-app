# API Documentation

## Overview

This guide documents the RESTful API endpoints for the JewGo application, including request/response formats, authentication, and error handling.

## 🔗 Base URLs

- **Production**: `https://jewgo.onrender.com`
- **Development**: `http://localhost:5000`

## 🔐 Authentication

### NextAuth.js Integration
The frontend uses NextAuth.js for authentication with Google OAuth.

### API Authentication
Most endpoints are public, but some require authentication:
- **User-specific data**: Requires valid session
- **Admin operations**: Requires admin privileges
- **Data submission**: May require authentication

## 📋 Endpoints

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "restaurants_count": 107,
  "version": "3.0"
}
```

### Restaurants

#### Get All Restaurants
```http
GET /api/restaurants
```

**Query Parameters:**
- `limit` (optional): Number of results (default: 50, max: 1000)
- `offset` (optional): Pagination offset (default: 0)
- `search` (optional): Search query
- `city` (optional): Filter by city
- `state` (optional): Filter by state
- `certifying_agency` (optional): Filter by certifying agency
- `kosher_category` (optional): Filter by kosher type
- `is_cholov_yisroel` (optional): Filter by Chalav Yisroel status
- `listing_type` (optional): Filter by business category
- `price_range` (optional): Filter by price range
- `min_rating` (optional): Minimum rating filter
- `has_reviews` (optional): Filter by review availability
- `open_now` (optional): Filter by current availability
- `lat` (optional): Latitude for location-based search
- `lng` (optional): Longitude for location-based search
- `radius` (optional): Search radius in miles

**Response:**
```json
{
  "restaurants": [
    {
      "id": 1,
      "name": "Kosher Deli & Grill",
      "address": "123 Main Street",
      "city": "Miami",
      "state": "FL",
      "zip_code": "33101",
      "phone": "(555) 123-4567",
      "website": "https://example.com",
      "certifying_agency": "ORB",
      "kosher_category": "meat",
      "listing_type": "restaurant",
      "status": "active",
      "hours_of_operation": "Mon-Fri: 11AM-9PM",
      "short_description": "Authentic kosher deli",
      "price_range": "$$",
      "image_url": "https://example.com/image.jpg",
      "latitude": 25.7617,
      "longitude": -80.1918,
      "rating": 4.5,
      "review_count": 25,
      "is_kosher": true,
      "is_glatt": true,
      "is_cholov_yisroel": false,
      "is_pas_yisroel": true,
      "is_bishul_yisroel": false,
      "is_mehadrin": false,
      "is_hechsher": true,
      "kosher_type": "meat",
      "kosher_cert_link": "https://example.com/cert",
      "detail_url": "https://example.com/details",
      "email": "info@example.com",
      "google_listing_url": "https://maps.google.com",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 107,
  "limit": 50,
  "offset": 0
}
```

#### Get Restaurant by ID
```http
GET /api/restaurants/{id}
```

**Response:**
```json
{
  "id": 1,
  "name": "Kosher Deli & Grill",
  // ... same structure as above
}
```

#### Search Restaurants
```http
GET /api/restaurants/search?q={query}
```

**Query Parameters:**
- `q` (required): Search query
- `limit` (optional): Number of results (default: 50)
- `offset` (optional): Pagination offset (default: 0)

**Response:**
```json
{
  "restaurants": [...],
  "query": "kosher",
  "total": 25,
  "limit": 50,
  "offset": 0
}
```

#### Submit New Restaurant
```http
POST /api/restaurants
```

**Request Body:**
```json
{
  "name": "New Restaurant",
  "short_description": "Brief description",
  "description": "Detailed description",
  "certifying_agency": "ORB",
  "kosher_category": "dairy",
  "is_cholov_yisroel": true,
  "is_pas_yisroel": false,
  "kosher_cert_link": "https://example.com/cert",
  "phone": "(555) 123-4567",
  "email": "info@restaurant.com",
  "address": "123 Main St",
  "website": "https://restaurant.com",
  "google_listing_url": "https://maps.google.com",
  "hours_open": "Mon-Fri: 11AM-9PM",
  "price_range": "$$",
  "image_url": "https://example.com/image.jpg",
  "category": "restaurant",
  "user_type": "owner",
  "owner_info": {
    "name": "Owner Name",
    "email": "owner@restaurant.com",
    "phone": "(555) 987-6543"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Restaurant submitted successfully for review",
  "data": {
    "id": 108,
    "name": "New Restaurant",
    // ... submitted data
  }
}
```

### Filter Options
```http
GET /api/restaurants/filter-options
```

**Response:**
```json
{
  "success": true,
  "data": {
    "cities": ["Miami", "Miami Beach", "Boca Raton"],
    "states": ["FL", "NY", "CA"],
    "agencies": ["ORB", "KM", "Star-K", "CRC"],
    "listingTypes": ["restaurant", "bakery", "catering"],
    "priceRanges": ["$", "$$", "$$$", "$$$$"],
    "kosherCategories": ["meat", "dairy", "pareve"]
  }
}
```

### Statistics
```http
GET /api/statistics
```

**Response:**
```json
{
  "total_restaurants": 107,
  "dairy_restaurants": 99,
  "pareve_restaurants": 8,
  "chalav_yisroel": 104,
  "pas_yisroel": 22,
  "states": ["FL", "NY", "CA"],
  "cities": ["Miami", "New York", "Los Angeles"]
}
```

### Kosher Types
```http
GET /api/kosher-types
```

**Response:**
```json
{
  "kosher_types": {
    "dairy": 99,
    "meat": 8,
    "pareve": 0
  },
  "chalav_yisroel": 104,
  "chalav_stam": 3,
  "pas_yisroel": 22
}
```

## 🔍 Frontend API Routes

### Restaurant Management
```http
GET /api/restaurants/{id}/approve
POST /api/restaurants/{id}/approve
POST /api/restaurants/{id}/reject
```

### Authentication
```http
GET /api/auth/[...nextauth]
```

## 📊 Error Handling

### Error Response Format
```json
{
  "error": "Error type",
  "message": "Human-readable error message",
  "details": {
    "field": "Specific field error"
  }
}
```

### Common Error Codes
- `400`: Bad Request - Invalid input data
- `401`: Unauthorized - Authentication required
- `403`: Forbidden - Insufficient permissions
- `404`: Not Found - Resource not found
- `422`: Unprocessable Entity - Validation errors
- `500`: Internal Server Error - Server error

### Validation Errors
```json
{
  "error": "Validation failed",
  "message": "Input validation failed",
  "errors": [
    {
      "field": "name",
      "message": "Restaurant name is required"
    },
    {
      "field": "email",
      "message": "Invalid email format"
    }
  ]
}
```

## 🔧 Rate Limiting

- **Public endpoints**: 100 requests per minute
- **Authenticated endpoints**: 1000 requests per minute
- **Admin endpoints**: 5000 requests per minute

## 📝 Request/Response Examples

### Search Example
```bash
curl "https://jewgo.onrender.com/api/restaurants?search=kosher&city=Miami&limit=10"
```

### Filter Example
```bash
curl "https://jewgo.onrender.com/api/restaurants?certifying_agency=ORB&kosher_category=dairy&is_cholov_yisroel=true"
```

### Location Search Example
```bash
curl "https://jewgo.onrender.com/api/restaurants?lat=25.7617&lng=-80.1918&radius=10"
```

## 🚀 SDK Examples

### JavaScript/TypeScript
```javascript
// Get restaurants
const response = await fetch('https://jewgo.onrender.com/api/restaurants');
const data = await response.json();

// Search restaurants
const searchResponse = await fetch(
  'https://jewgo.onrender.com/api/restaurants?search=kosher&limit=20'
);
const searchData = await searchResponse.json();

// Submit restaurant
const submitResponse = await fetch('https://jewgo.onrender.com/api/restaurants', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(restaurantData)
});
```

### Python
```python
import requests

# Get restaurants
response = requests.get('https://jewgo.onrender.com/api/restaurants')
data = response.json()

# Search restaurants
search_response = requests.get(
    'https://jewgo.onrender.com/api/restaurants',
    params={'search': 'kosher', 'limit': 20}
)
search_data = search_response.json()
```

## 📊 API Status

### Health Check
```bash
curl https://jewgo.onrender.com/health
```

### Response Times
- **Average**: < 200ms
- **95th percentile**: < 500ms
- **99th percentile**: < 1000ms

## 🔄 Versioning

- **Current Version**: v3.0
- **Version Header**: `X-API-Version: 3.0`
- **Backward Compatibility**: Maintained for 6 months

## 📞 Support

- **Documentation**: This guide
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: Contact development team

---

*For detailed implementation examples, see the development documentation.* 