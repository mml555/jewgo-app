import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

// Validation schema for restaurant submission
const RestaurantSubmissionSchema = z.object({
  // Basic Info
  name: z.string().min(1, "Restaurant name is required").max(255),
  short_description: z.string().max(80, "Short description must be 80 characters or less"),
  description: z.string().optional(),
  certifying_agency: z.string().min(1, "Certifying agency is required"),
  kosher_category: z.enum(['meat', 'dairy', 'pareve'], {
    required_error: "Kosher category is required"
  }),
  
  // Kosher Info
  is_cholov_yisroel: z.boolean().optional(),
  is_pas_yisroel: z.boolean().optional(),
  kosher_cert_link: z.string().url().optional().or(z.literal('')),
  
  // Contact & Location
  phone: z.string().min(1, "Phone number is required"),
  email: z.string().email().optional().or(z.literal('')),
  address: z.string().min(1, "Address is required"),
  website: z.string().url().optional().or(z.literal('')),
  google_listing_url: z.string().url().optional().or(z.literal('')),
  
  // Business Info
  hours_open: z.string().min(1, "Hours are required"),
  price_range: z.string().optional(),
  
  // Images
  image_url: z.string().url().optional().or(z.literal('')),
  
  // Meta
  category: z.string().default('restaurant'),
  user_type: z.enum(['owner', 'community']),
  owner_info: z.object({
    name: z.string().optional(),
    email: z.string().email().optional(),
    phone: z.string().optional()
  }).optional()
}).refine((data) => {
  // Conditional validation for kosher subcategories
  if (data.kosher_category === 'dairy' && data.is_cholov_yisroel === undefined) {
    return false;
  }
  if (['meat', 'pareve'].includes(data.kosher_category) && data.is_pas_yisroel === undefined) {
    return false;
  }
  return true;
}, {
  message: "Kosher subcategory is required",
  path: ["kosher_category"]
});

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Validate the request body
    const validatedData = RestaurantSubmissionSchema.parse(body);
    
    // Transform data for database insertion
    const restaurantData = {
      name: validatedData.name,
      short_description: validatedData.short_description,
      description: validatedData.description || null,
      certifying_agency: validatedData.certifying_agency,
      kosher_category: validatedData.kosher_category,
      is_cholov_yisroel: validatedData.kosher_category === 'dairy' ? validatedData.is_cholov_yisroel : null,
      is_pas_yisroel: ['meat', 'pareve'].includes(validatedData.kosher_category) ? validatedData.is_pas_yisroel : null,
      kosher_cert_link: validatedData.kosher_cert_link || null,
      phone: validatedData.phone,
      email: validatedData.email || null,
      address: validatedData.address,
      website: validatedData.website || null,
      google_listing_url: validatedData.google_listing_url || null,
      hours_open: validatedData.hours_open,
      price_range: validatedData.price_range || null,
      image_url: validatedData.image_url || null,
      category: validatedData.category,
      status: 'pending_approval', // Default status for new submissions
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };

    // TODO: Insert into database
    // For now, we'll simulate the database insertion
    console.log('Restaurant submission:', restaurantData);
    
    // In a real implementation, you would:
    // 1. Connect to your database
    // 2. Insert the restaurant data
    // 3. Handle owner information if provided
    // 4. Send notification emails if needed
    
    return NextResponse.json({
      success: true,
      message: 'Restaurant submitted successfully for review',
      data: {
        id: Math.floor(Math.random() * 10000), // Simulated ID
        ...restaurantData
      }
    }, { status: 201 });

  } catch (error) {
    console.error('Restaurant submission error:', error);
    
    if (error instanceof z.ZodError) {
      return NextResponse.json({
        success: false,
        message: 'Validation failed',
        errors: error.errors
      }, { status: 400 });
    }
    
    return NextResponse.json({
      success: false,
      message: 'Internal server error'
    }, { status: 500 });
  }
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const limit = parseInt(searchParams.get('limit') || '50');
    const offset = parseInt(searchParams.get('offset') || '0');
    const status = searchParams.get('status') || 'approved';
    
    // TODO: Fetch restaurants from database
    // For now, return mock data
    const mockRestaurants = [
      {
        id: 1,
        name: "Sample Kosher Restaurant",
        short_description: "Delicious kosher cuisine",
        kosher_category: "meat",
        certifying_agency: "OU",
        status: "approved"
      }
    ];
    
    return NextResponse.json({
      success: true,
      data: mockRestaurants,
      pagination: {
        limit,
        offset,
        total: mockRestaurants.length
      }
    });

  } catch (error) {
    console.error('Error fetching restaurants:', error);
    return NextResponse.json({
      success: false,
      message: 'Failed to fetch restaurants'
    }, { status: 500 });
  }
} 