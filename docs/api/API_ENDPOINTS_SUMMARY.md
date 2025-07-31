# API Endpoints Summary

## Overview
This document summarizes all the API endpoints that have been created to bridge the frontend Next.js application with the backend Flask API. These endpoints were created to resolve the 405 Method Not Allowed error that was occurring when the frontend tried to call backend endpoints directly.

## Frontend API Routes Created

### Restaurant Endpoints

#### Individual Restaurant Operations
- **`GET /api/restaurants/[id]`** - Get a specific restaurant by ID
- **`PUT /api/restaurants/[id]`** - Update a specific restaurant by ID  
- **`DELETE /api/restaurants/[id]`** - Delete a specific restaurant by ID

#### Restaurant Search
- **`GET /api/restaurants/search`** - Search restaurants with various filters and parameters

#### Website Backup System
- **`POST /api/restaurants/[id]/fetch-website`** - Fetch website link for a specific restaurant using Google Places API
- **`POST /api/restaurants/fetch-missing-websites`** - Fetch website links for all restaurants that don't have them (bulk operation)

#### Hours Backup System
- **`POST /api/restaurants/[id]/fetch-hours`** - Fetch operating hours for a specific restaurant using Google Places API
- **`POST /api/restaurants/fetch-missing-hours`** - Fetch operating hours for all restaurants that don't have them (bulk operation)

#### Restaurant Management
- **`GET /api/restaurants`** - Get all restaurants with filtering and pagination
- **`POST /api/restaurants`** - Submit a new restaurant for review

### System Endpoints

#### Statistics and Analytics
- **`GET /api/statistics`** - Get application statistics and metrics

#### Data Management
- **`GET /api/kosher-types`** - Get available kosher types and categories
- **`POST /api/remove-duplicates`** - Remove duplicate restaurants from the database
- **`GET /api/migrate`** - Get migration status and information
- **`POST /api/migrate`** - Run database migrations
- **`POST /api/update-database`** - Update database schema and data

## Architecture Pattern

All frontend API routes follow a consistent pattern:

1. **Input Validation** - Validate request parameters and body data
2. **Backend Proxy** - Forward requests to the appropriate backend endpoint
3. **Error Handling** - Provide consistent error responses
4. **Response Forwarding** - Return the same status and data from the backend

### Example Structure
```typescript
export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    // 1. Validate input
    const restaurantId = params.id;
    if (!restaurantId || isNaN(Number(restaurantId))) {
      return NextResponse.json(
        { error: 'Invalid restaurant ID' },
        { status: 400 }
      );
    }

    // 2. Get backend URL from environment
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://jewgo.onrender.com';
    
    // 3. Forward request to backend
    const backendResponse = await fetch(
      `${backendUrl}/api/restaurants/${restaurantId}/fetch-website`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({}),
      }
    );

    const data = await backendResponse.json();

    // 4. Return backend response
    return NextResponse.json(data, { status: backendResponse.status });

  } catch (error) {
    // 5. Handle errors
    console.error('Error in API route:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

## Environment Variables

The API routes use the following environment variables:

- **`NEXT_PUBLIC_BACKEND_URL`** - The URL of the backend Flask API (defaults to `https://jewgo.onrender.com`)

## Error Handling

All endpoints implement consistent error handling:

- **400 Bad Request** - Invalid input parameters
- **404 Not Found** - Resource not found
- **500 Internal Server Error** - Backend errors or network issues

## Security Considerations

- Input validation on all parameters
- Proper error messages that don't expose internal details
- Environment-based backend URL configuration
- Consistent HTTP status code forwarding

## Testing

To test these endpoints:

1. Ensure the backend is running and accessible
2. Set the `NEXT_PUBLIC_BACKEND_URL` environment variable
3. Use tools like Postman or curl to test each endpoint
4. Verify that responses match the backend API documentation

## Maintenance

When adding new backend endpoints:

1. Create a corresponding frontend API route
2. Follow the established pattern for consistency
3. Add proper error handling and validation
4. Update this documentation
5. Test the endpoint thoroughly

## Related Files

- `frontend/utils/websiteBackup.ts` - Utility functions for website backup operations
- `backend/app.py` - Backend Flask API implementation
- `docs/api/README.md` - General API documentation 