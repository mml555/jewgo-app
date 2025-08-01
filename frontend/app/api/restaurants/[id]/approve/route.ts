import { NextRequest, NextResponse } from 'next/server';

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const restaurantId = parseInt(id);
    
    if (isNaN(restaurantId)) {
      return NextResponse.json({
        success: false,
        message: 'Invalid restaurant ID'
      }, { status: 400 });
    }

    const body = await request.json();
    const { status } = body;

    // TODO: Update restaurant status in database
    // For now, we'll simulate the database update
    console.log(`Approving restaurant ${restaurantId} with status: ${status}`);
    
    // In a real implementation, you would:
    // 1. Connect to your database
    // 2. Update the restaurant status to 'approved'
    // 3. Send notification emails if needed
    // 4. Update any related records

    return NextResponse.json({
      success: true,
      message: 'Restaurant approved successfully',
      data: {
        id: restaurantId,
        status: 'approved',
        updated_at: new Date().toISOString()
      }
    });

  } catch (error) {
    console.error('Error approving restaurant:', error);
    return NextResponse.json({
      success: false,
      message: 'Failed to approve restaurant'
    }, { status: 500 });
  }
} 