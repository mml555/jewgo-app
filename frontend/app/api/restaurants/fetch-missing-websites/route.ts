import { NextRequest, NextResponse } from 'next/server';

/**
 * API Route: POST /api/restaurants/fetch-missing-websites
 * 
 * Fetches website links for all restaurants that don't have them.
 * This is a bulk operation that can take some time.
 * 
 * @param request - The incoming request with optional limit parameter
 * @returns JSON response with bulk update information
 */
export async function POST(request: NextRequest) {
  try {
    // Parse the request body to get the limit
    const body = await request.json().catch(() => ({}));
    const limit = body.limit || 10;

    // Validate limit
    if (limit < 1 || limit > 100) {
      return NextResponse.json(
        { error: 'Limit must be between 1 and 100' },
        { status: 400 }
      );
    }

    // Get backend URL from environment
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://jewgo.onrender.com';
    
    // Forward the request to the backend
    const backendResponse = await fetch(
      `${backendUrl}/api/restaurants/fetch-missing-websites`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ limit }),
      }
    );

    const data = await backendResponse.json();

    // Return the same status and data from the backend
    return NextResponse.json(data, { status: backendResponse.status });

  } catch (error) {
    console.error('Error in fetch-missing-websites API route:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error',
        message: 'Failed to fetch missing websites'
      },
      { status: 500 }
    );
  }
} 