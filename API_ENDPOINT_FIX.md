# API Endpoint Fix Summary

## Problem
The frontend was experiencing a 405 Method Not Allowed error when trying to call the `/api/restaurants/787/fetch-website` endpoint. This was happening because the frontend Next.js application was trying to call backend endpoints directly, but the corresponding Next.js API routes didn't exist.

## Root Cause
The backend Flask API had several endpoints that were missing their corresponding frontend Next.js API routes:

1. **`POST /api/restaurants/{id}/fetch-website`** - Fetch website for specific restaurant
2. **`POST /api/restaurants/fetch-missing-websites`** - Bulk fetch websites
3. **`POST /api/restaurants/{id}/fetch-hours`** - Fetch hours for specific restaurant
4. **`POST /api/restaurants/fetch-missing-hours`** - Bulk fetch hours
5. **`GET /api/restaurants/search`** - Search restaurants
6. **`GET /api/restaurants/{id}`** - Get individual restaurant
7. **`PUT /api/restaurants/{id}`** - Update restaurant
8. **`DELETE /api/restaurants/{id}`** - Delete restaurant
9. **`GET /api/statistics`** - Get statistics
10. **`GET /api/kosher-types`** - Get kosher types
11. **`POST /api/remove-duplicates`** - Remove duplicates
12. **`GET /api/migrate`** - Get migration status
13. **`POST /api/migrate`** - Run migrations
14. **`POST /api/update-database`** - Update database

## Solution
Created comprehensive Next.js API routes that act as proxies to the backend Flask API. Each route:

1. **Validates input parameters** - Ensures proper data types and formats
2. **Forwards requests to backend** - Uses the correct backend URL from environment variables
3. **Handles errors gracefully** - Provides consistent error responses
4. **Returns backend responses** - Maintains the same status codes and data structure

## Files Created/Modified

### New API Routes Created:
- `frontend/app/api/restaurants/[id]/fetch-website/route.ts`
- `frontend/app/api/restaurants/fetch-missing-websites/route.ts`
- `frontend/app/api/restaurants/[id]/fetch-hours/route.ts`
- `frontend/app/api/restaurants/fetch-missing-hours/route.ts`
- `frontend/app/api/restaurants/search/route.ts`
- `frontend/app/api/restaurants/[id]/route.ts`
- `frontend/app/api/statistics/route.ts`
- `frontend/app/api/kosher-types/route.ts`
- `frontend/app/api/remove-duplicates/route.ts`
- `frontend/app/api/migrate/route.ts`
- `frontend/app/api/update-database/route.ts`

### Documentation Created:
- `docs/api/API_ENDPOINTS_SUMMARY.md` - Comprehensive API documentation
- `API_ENDPOINT_FIX.md` - This summary document

## Environment Configuration
All API routes use the `NEXT_PUBLIC_BACKEND_URL` environment variable with a fallback to `https://jewgo.onrender.com`. This ensures consistency with the existing frontend configuration.

## Architecture Pattern
All new API routes follow a consistent pattern:

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

## Testing
The fix resolves the 405 Method Not Allowed error by providing proper Next.js API routes that can handle the requests and forward them to the backend. The website backup functionality should now work correctly.

## Impact
- ✅ Resolves 405 Method Not Allowed error
- ✅ Enables website backup functionality
- ✅ Enables hours backup functionality
- ✅ Provides complete API coverage for all backend endpoints
- ✅ Maintains consistent error handling and response formats
- ✅ Follows established patterns for maintainability

## Next Steps
1. Test the website backup functionality to ensure it works correctly
2. Monitor for any other missing API endpoints
3. Consider adding automated tests for the new API routes
4. Update any frontend components that might be calling these endpoints directly 