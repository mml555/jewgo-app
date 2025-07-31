import { NextRequest, NextResponse } from 'next/server';

/**
 * API Route: GET /api/restaurants/[id]
 * 
 * Get a specific restaurant by ID.
 * 
 * @param request - The incoming request
 * @param params - Route parameters containing the restaurant ID
 * @returns JSON response with restaurant data
 */
export async function GET(
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
      `${backendUrl}/api/restaurants/${restaurantId}`,
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
    console.error('Error in restaurant GET API route:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error',
        message: 'Failed to fetch restaurant'
      },
      { status: 500 }
    );
  }
}

/**
 * API Route: PUT /api/restaurants/[id]
 * 
 * Update a specific restaurant by ID.
 * 
 * @param request - The incoming request with update data
 * @param params - Route parameters containing the restaurant ID
 * @returns JSON response with updated restaurant data
 */
export async function PUT(
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

    // Get the request body
    const body = await request.json();

    // Get backend URL from environment
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://jewgo.onrender.com';
    
    // Forward the request to the backend
    const backendResponse = await fetch(
      `${backendUrl}/api/restaurants/${restaurantId}`,
      {
        method: 'PUT',
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
    console.error('Error in restaurant PUT API route:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error',
        message: 'Failed to update restaurant'
      },
      { status: 500 }
    );
  }
}

/**
 * API Route: DELETE /api/restaurants/[id]
 * 
 * Delete a specific restaurant by ID.
 * 
 * @param request - The incoming request
 * @param params - Route parameters containing the restaurant ID
 * @returns JSON response with deletion confirmation
 */
export async function DELETE(
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
      `${backendUrl}/api/restaurants/${restaurantId}`,
      {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    const data = await backendResponse.json();

    // Return the same status and data from the backend
    return NextResponse.json(data, { status: backendResponse.status });

  } catch (error) {
    console.error('Error in restaurant DELETE API route:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error',
        message: 'Failed to delete restaurant'
      },
      { status: 500 }
    );
  }
} 