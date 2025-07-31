import { NextRequest, NextResponse } from 'next/server';

/**
 * API Route: POST /api/restaurants/[id]/fetch-website
 * 
 * Fetches website link for a specific restaurant using Google Places API.
 * This is a backup system when the restaurant doesn't have a website link.
 * 
 * @param request - The incoming request
 * @param params - Route parameters containing the restaurant ID
 * @returns JSON response with website information
 */
export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const restaurantId = params.id;
    
    // Validate restaurant ID
    if (!restaurantId || isNaN(Number(restaurantId))) {
      return NextResponse.json(
        { error: 'Invalid restaurant ID' },
        { status: 400 }
      );
    }

    // Get backend URL from environment
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://jewgo.onrender.com';
    
    // Forward the request to the backend
    const backendResponse = await fetch(
      `${backendUrl}/api/restaurants/${restaurantId}/fetch-website`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        // Forward any body data if needed
        body: JSON.stringify({}),
      }
    );

    const data = await backendResponse.json();

    // Return the same status and data from the backend
    return NextResponse.json(data, { status: backendResponse.status });

  } catch (error) {
    console.error('Error in fetch-website API route:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error',
        message: 'Failed to fetch restaurant website'
      },
      { status: 500 }
    );
  }
} 