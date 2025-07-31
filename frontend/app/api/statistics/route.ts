import { NextRequest, NextResponse } from 'next/server';

/**
 * API Route: GET /api/statistics
 * 
 * Get application statistics and metrics.
 * 
 * @param request - The incoming request
 * @returns JSON response with statistics data
 */
export async function GET(request: NextRequest) {
  try {
    // Get backend URL from environment
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://jewgo.onrender.com';
    
    // Forward the request to the backend
    const backendResponse = await fetch(
      `${backendUrl}/api/statistics`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    const data = await backendResponse.json();

    // Return the same status and data from the backend
    return NextResponse.json(data, { status: backendResponse.status });

  } catch (error) {
    console.error('Error in statistics API route:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error',
        message: 'Failed to fetch statistics'
      },
      { status: 500 }
    );
  }
} 