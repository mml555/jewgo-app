import { NextRequest, NextResponse } from 'next/server';

export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const restaurantId = parseInt(params.id);
    
    if (isNaN(restaurantId)) {
      return NextResponse.json({
        success: false,
        message: 'Invalid restaurant ID'
      }, { status: 400 });
    }

    const body = await request.json();
    const { status, rejection_reason } = body;

    // TODO: Update restaurant status in database
    // For now, we'll simulate the database update
    console.log(`Rejecting restaurant ${restaurantId} with reason: ${rejection_reason}`);
    
    // In a real implementation, you would:
    // 1. Connect to your database
    // 2. Update the restaurant status to 'rejected'
    // 3. Store the rejection reason
    // 4. Send notification emails to the submitter
    // 5. Update any related records

    return NextResponse.json({
      success: true,
      message: 'Restaurant rejected successfully',
      data: {
        id: restaurantId,
        status: 'rejected',
        rejection_reason,
        updated_at: new Date().toISOString()
      }
    });

  } catch (error) {
    console.error('Error rejecting restaurant:', error);
    return NextResponse.json({
      success: false,
      message: 'Failed to reject restaurant'
    }, { status: 500 });
  }
} 