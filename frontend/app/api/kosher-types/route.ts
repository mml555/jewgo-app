import { NextRequest, NextResponse } from 'next/server';

// Force dynamic rendering for API routes
export const dynamic = 'force-dynamic'

/**
 * API Route: GET /api/kosher-types
 * 
 * Get available kosher types and categories.
 * 
 * @param request - The incoming request
 * @returns JSON response with kosher types data
 */
export async function GET(request: NextRequest) {
  try {
    // Get backend URL from environment
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://jewgo.onrender.com';
    
    // Forward the request to the backend
    const backendResponse = await fetch(
      `${backendUrl}/api/kosher-types`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    // Check if response is JSON
    const contentType = backendResponse.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      console.warn('Backend returned non-JSON response for kosher-types:', contentType);
      return NextResponse.json(
        { 
          error: 'Backend service unavailable',
          message: 'Kosher types service is currently unavailable'
        },
        { status: 503 }
      );
    }

    const data = await backendResponse.json();

    // Return the same status and data from the backend
    return NextResponse.json(data, { status: backendResponse.status });

  } catch (error) {
    console.error('Error in kosher-types API route:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error',
        message: 'Failed to fetch kosher types'
      },
      { status: 500 }
    );
  }
} 