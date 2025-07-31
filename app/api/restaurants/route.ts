import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

// Validation schema for restaurant submission
const RestaurantSubmissionSchema = z.object({
  // Basic Info
  name: z.string().min(1, "Restaurant name is required").max(255),
  short_description: z.string().max(80, "Short description must be 80 characters or less"),
  description: z.string().optional(),
  certifying_agency: z.string().min(1, "Certifying agency is required"),
  kosher_category: z.enum(['meat', 'dairy', 'pareve']),
  
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
    
    // Pagination
    const limit = parseInt(searchParams.get('limit') || '50');
    const offset = parseInt(searchParams.get('offset') || '0');
    
    // Filter parameters
    const search = searchParams.get('search');
    const city = searchParams.get('city');
    const state = searchParams.get('state');
    const certifying_agency = searchParams.get('certifying_agency');
    const kosher_category = searchParams.get('kosher_category');
    const is_cholov_yisroel = searchParams.get('is_cholov_yisroel');
    const listing_type = searchParams.get('listing_type');
    const price_range = searchParams.get('price_range');
    const min_rating = searchParams.get('min_rating');
    const has_reviews = searchParams.get('has_reviews');
    const open_now = searchParams.get('open_now');
    const status = searchParams.get('status') || 'approved';
    
    // Location-based filtering
    const lat = searchParams.get('lat');
    const lng = searchParams.get('lng');
    const radius = searchParams.get('radius');
    
    // TODO: In a real implementation, you would:
    // 1. Connect to your database
    // 2. Build a dynamic query based on the filters
    // 3. Apply location-based filtering if coordinates are provided
    // 4. Apply rating and review filters
    // 5. Apply hours filtering for "open now"
    
    // For now, return enhanced mock data that matches our schema
    const mockRestaurants = [
      {
        id: 1,
        name: "Kosher Delight Restaurant",
        address: "123 Main Street",
        city: "New York",
        state: "NY",
        zip_code: "10001",
        phone_number: "(555) 123-4567",
        website: "https://kosherdelight.com",
        certificate_link: "https://orbkosher.com/certificate/123",
        image_url: "https://example.com/restaurant1.jpg",
        google_listing_url: "https://maps.google.com/restaurant1",
        certifying_agency: "ORB",
        kosher_category: "meat",
        is_cholov_yisroel: null,
        listing_type: "restaurant",
        status: "approved",
        hours_of_operation: "Mon-Fri: 11AM-10PM, Sat: 6PM-11PM, Sun: 12PM-9PM",
        hours_open: "Open",
        short_description: "Authentic kosher cuisine in a warm, welcoming atmosphere",
        price_range: "$$",
        avg_price: "$25-35",
        menu_pricing: {
          "appetizers": { min: 8, max: 15, avg: 12 },
          "main_courses": { min: 18, max: 45, avg: 28 },
          "desserts": { min: 6, max: 12, avg: 9 }
        },
        min_avg_meal_cost: 25,
        max_avg_meal_cost: 35,
        notes: "Glatt kosher, family-friendly",
        latitude: 40.7128,
        longitude: -74.0060,
        rating: 4.5,
        star_rating: 4.5,
        quality_rating: 4.3,
        review_count: 127,
        google_rating: 4.4,
        google_review_count: 89,
        google_reviews: "[]",
        created_at: "2024-01-15T10:00:00Z",
        updated_at: "2024-01-20T15:30:00Z"
      },
      {
        id: 2,
        name: "Dairy Palace",
        address: "456 Oak Avenue",
        city: "Los Angeles",
        state: "CA",
        zip_code: "90210",
        phone_number: "(555) 987-6543",
        website: "https://dairypalace.com",
        certificate_link: "https://orbkosher.com/certificate/456",
        image_url: "https://example.com/restaurant2.jpg",
        google_listing_url: "https://maps.google.com/restaurant2",
        certifying_agency: "KM",
        kosher_category: "dairy",
        is_cholov_yisroel: true,
        listing_type: "restaurant",
        status: "approved",
        hours_of_operation: "Mon-Sun: 7AM-11PM",
        hours_open: "Open",
        short_description: "Chalav Yisrael dairy restaurant with fresh pastries",
        price_range: "$$$",
        avg_price: "$35-50",
        menu_pricing: {
          "breakfast": { min: 12, max: 25, avg: 18 },
          "lunch": { min: 18, max: 35, avg: 26 },
          "dinner": { min: 25, max: 55, avg: 40 }
        },
        min_avg_meal_cost: 35,
        max_avg_meal_cost: 50,
        notes: "Chalav Yisrael, Pas Yisrael",
        latitude: 34.0522,
        longitude: -118.2437,
        rating: 4.8,
        star_rating: 4.8,
        quality_rating: 4.7,
        review_count: 203,
        google_rating: 4.6,
        google_review_count: 156,
        google_reviews: "[]",
        created_at: "2024-01-10T09:00:00Z",
        updated_at: "2024-01-18T12:15:00Z"
      },
      {
        id: 3,
        name: "Pareve Paradise",
        address: "789 Pine Street",
        city: "Chicago",
        state: "IL",
        zip_code: "60601",
        phone_number: "(555) 456-7890",
        website: "https://pareveparadise.com",
        certificate_link: "https://orbkosher.com/certificate/789",
        image_url: "https://example.com/restaurant3.jpg",
        google_listing_url: "https://maps.google.com/restaurant3",
        certifying_agency: "Star-K",
        kosher_category: "pareve",
        is_cholov_yisroel: null,
        listing_type: "restaurant",
        status: "approved",
        hours_of_operation: "Mon-Thu: 11AM-9PM, Fri: 11AM-3PM, Sun: 5PM-9PM",
        hours_open: "Open",
        short_description: "Fresh pareve cuisine with Mediterranean influences",
        price_range: "$$",
        avg_price: "$20-30",
        menu_pricing: {
          "salads": { min: 8, max: 18, avg: 13 },
          "main_dishes": { min: 15, max: 32, avg: 24 },
          "sides": { min: 5, max: 12, avg: 8 }
        },
        min_avg_meal_cost: 20,
        max_avg_meal_cost: 30,
        notes: "Pas Yisrael, Bishul Yisrael",
        latitude: 41.8781,
        longitude: -87.6298,
        rating: 4.2,
        star_rating: 4.2,
        quality_rating: 4.0,
        review_count: 89,
        google_rating: 4.1,
        google_review_count: 67,
        google_reviews: "[]",
        created_at: "2024-01-12T11:00:00Z",
        updated_at: "2024-01-19T14:20:00Z"
      }
    ];
    
    // Apply filters to mock data (in real implementation, this would be done in the database query)
    let filteredRestaurants = mockRestaurants;
    
    if (search) {
      filteredRestaurants = filteredRestaurants.filter(restaurant => 
        restaurant.name.toLowerCase().includes(search.toLowerCase()) ||
        restaurant.short_description?.toLowerCase().includes(search.toLowerCase())
      );
    }
    
    if (city) {
      filteredRestaurants = filteredRestaurants.filter(restaurant => 
        restaurant.city === city
      );
    }
    
    if (state) {
      filteredRestaurants = filteredRestaurants.filter(restaurant => 
        restaurant.state === state
      );
    }
    
    if (certifying_agency) {
      filteredRestaurants = filteredRestaurants.filter(restaurant => 
        restaurant.certifying_agency === certifying_agency
      );
    }
    
    if (kosher_category) {
      filteredRestaurants = filteredRestaurants.filter(restaurant => 
        restaurant.kosher_category === kosher_category
      );
    }
    
    if (is_cholov_yisroel !== null) {
      const isCholovYisroel = is_cholov_yisroel === 'true';
      filteredRestaurants = filteredRestaurants.filter(restaurant => 
        restaurant.is_cholov_yisroel === isCholovYisroel
      );
    }
    
    if (listing_type) {
      filteredRestaurants = filteredRestaurants.filter(restaurant => 
        restaurant.listing_type === listing_type
      );
    }
    
    if (price_range) {
      filteredRestaurants = filteredRestaurants.filter(restaurant => 
        restaurant.price_range === price_range
      );
    }
    
    if (min_rating) {
      const minRating = parseFloat(min_rating);
      filteredRestaurants = filteredRestaurants.filter(restaurant => 
        restaurant.rating && restaurant.rating >= minRating
      );
    }
    
    if (has_reviews === 'true') {
      filteredRestaurants = filteredRestaurants.filter(restaurant => 
        restaurant.review_count && restaurant.review_count > 0
      );
    }
    
    if (open_now === 'true') {
      filteredRestaurants = filteredRestaurants.filter(restaurant => 
        restaurant.hours_open === 'Open'
      );
    }
    
    // Apply pagination
    const paginatedRestaurants = filteredRestaurants.slice(offset, offset + limit);
    
    return NextResponse.json({
      success: true,
      restaurants: paginatedRestaurants,
      pagination: {
        limit,
        offset,
        total: filteredRestaurants.length,
        pages: Math.ceil(filteredRestaurants.length / limit)
      },
      filters: {
        applied: {
          search,
          city,
          state,
          certifying_agency,
          kosher_category,
          is_cholov_yisroel,
          listing_type,
          price_range,
          min_rating,
          has_reviews,
          open_now
        }
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