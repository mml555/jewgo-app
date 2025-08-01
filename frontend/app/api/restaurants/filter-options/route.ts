import { NextResponse } from 'next/server';

// Force dynamic rendering for API routes
export const dynamic = 'force-dynamic'

export async function GET() {
  try {
    // Fetch actual data from the backend API to get real filter options
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://jewgo.onrender.com';
    
    // Get restaurants to extract unique values
    const restaurantsResponse = await fetch(`${backendUrl}/api/restaurants?limit=1000`);
    
    // Check if response is JSON
    const contentType = restaurantsResponse.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      console.warn('Backend returned non-JSON response for restaurants:', contentType);
      throw new Error('Backend service unavailable');
    }
    
    const restaurantsData = await restaurantsResponse.json();
    const restaurants = restaurantsData.restaurants || restaurantsData.data || [];
    
    // Extract unique values from actual data
    const cities = Array.from(new Set(restaurants.map((r: { city?: string }) => r.city).filter(Boolean))).sort();
    const states = Array.from(new Set(restaurants.map((r: { state?: string }) => r.state).filter(Boolean))).sort();
    const agencies = Array.from(new Set(restaurants.map((r: { certifying_agency?: string }) => r.certifying_agency).filter(Boolean))).sort();
    const listingTypes = Array.from(new Set(restaurants.map((r: { listing_type?: string; category?: string }) => r.listing_type || r.category).filter(Boolean))).sort();
    const kosherCategories = Array.from(new Set(restaurants.map((r: { kosher_category?: string; kosher_type?: string }) => r.kosher_category || r.kosher_type).filter(Boolean))).sort();
    const priceRanges = Array.from(new Set(restaurants.map((r: { price_range?: string }) => r.price_range).filter(Boolean))).sort();
    
    const filterOptions = {
      cities,
      states,
      agencies,
      listingTypes,
      priceRanges,
      kosherCategories
    };

    return NextResponse.json({
      success: true,
      data: filterOptions
    });

  } catch (error) {
    console.error('Error fetching filter options:', error);
    
    // Fallback to static options if API fails
    const fallbackOptions = {
      cities: ['Miami', 'Miami Beach', 'Boca Raton', 'Fort Lauderdale'],
      states: ['FL', 'NY', 'CA', 'IL'],
      agencies: ['ORB', 'KM', 'Star-K', 'CRC', 'Kof-K', 'Diamond K'],
      listingTypes: ['restaurant', 'bakery', 'catering', 'grocery', 'market'],
      priceRanges: ['$', '$$', '$$$', '$$$$'],
      kosherCategories: ['meat', 'dairy', 'pareve']
    };
    
    return NextResponse.json({
      success: true,
      data: fallbackOptions
    });
  }
} 