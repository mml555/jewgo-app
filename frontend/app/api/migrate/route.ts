import { NextRequest, NextResponse } from 'next/server';

/**
 * API Route: GET /api/migrate
 * 
 * Get migration status and information.
 * 
 * @param request - The incoming request
 * @returns JSON response with migration information
 */
export async function GET() {
  try {
    // Get backend URL from environment
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://jewgo.onrender.com';
    
    // Forward the request to the backend
    const backendResponse = await fetch(
      `${backendUrl}/api/migrate`,
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
    console.error('Error in migrate GET API route:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error',
        message: 'Failed to get migration status'
      },
      { status: 500 }
    );
  }
}

/**
 * API Route: POST /api/migrate
 * 
 * Run database migrations.
 * 
 * @param request - The incoming request
 * @returns JSON response with migration results
 */
export async function POST(request: NextRequest) {
  try {
    // Get the request body
    const body = await request.json();

    // Get backend URL from environment
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://jewgo.onrender.com';
    
    // Forward the request to the backend
    const backendResponse = await fetch(
      `${backendUrl}/api/migrate`,
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
    console.error('Error in migrate POST API route:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error',
        message: 'Failed to run migration'
      },
      { status: 500 }
    );
  }
} 