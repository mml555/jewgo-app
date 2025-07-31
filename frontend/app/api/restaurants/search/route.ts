import { NextRequest, NextResponse } from 'next/server';

/**
 * API Route: GET /api/restaurants/search
 * 
 * Search restaurants with various filters and parameters.
 * 
 * @param request - The incoming request with search parameters
 * @returns JSON response with filtered restaurants
 */
export async function GET(request: NextRequest) {
  try {
    // Get search parameters from the URL
    const { searchParams } = new URL(request.url);
    
    // Get backend URL from environment
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://jewgo.onrender.com';
    
    // Build the search URL with all parameters
    const searchUrl = new URL(`${backendUrl}/api/restaurants/search`);
    
    // Forward all search parameters to the backend
    searchParams.forEach((value, key) => {
      searchUrl.searchParams.append(key, value);
    });
    
    // Forward the request to the backend
    const backendResponse = await fetch(searchUrl.toString(), {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = await backendResponse.json();

    // Return the same status and data from the backend
    return NextResponse.json(data, { status: backendResponse.status });

  } catch (error) {
    console.error('Error in restaurants search API route:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error',
        message: 'Failed to search restaurants'
      },
      { status: 500 }
    );
  }
} 