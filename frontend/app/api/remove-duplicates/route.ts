import { NextRequest, NextResponse } from 'next/server';

/**
 * API Route: POST /api/remove-duplicates
 * 
 * Remove duplicate restaurants from the database.
 * 
 * @param request - The incoming request
 * @returns JSON response with duplicate removal results
 */
export async function POST(request: NextRequest) {
  try {
    // Get the request body
    const body = await request.json();

    // Get backend URL from environment
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://jewgo.onrender.com';
    
    // Forward the request to the backend
    const backendResponse = await fetch(
      `${backendUrl}/api/remove-duplicates`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      }
    );

    const data = await backendResponse.json();

    // Return the same status and data from the backend
    return NextResponse.json(data, { status: backendResponse.status });

  } catch (error) {
    console.error('Error in remove-duplicates API route:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error',
        message: 'Failed to remove duplicates'
      },
      { status: 500 }
    );
  }
} 