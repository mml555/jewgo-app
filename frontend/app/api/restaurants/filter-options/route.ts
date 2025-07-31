import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // Fetch actual data from the backend API to get real filter options
    const backendUrl = process.env.BACKEND_URL || 'https://jewgo.onrender.com';
    
    // Get restaurants to extract unique values
    const restaurantsResponse = await fetch(`${backendUrl}/api/restaurants?limit=1000`);
    const restaurantsData = await restaurantsResponse.json();
    const restaurants = restaurantsData.restaurants || restaurantsData.data || [];
    
    // Extract unique values from actual data
    const cities = Array.from(new Set(restaurants.map((r: any) => r.city).filter(Boolean))).sort();
    const states = Array.from(new Set(restaurants.map((r: any) => r.state).filter(Boolean))).sort();
    const agencies = Array.from(new Set(restaurants.map((r: any) => r.certifying_agency).filter(Boolean))).sort();
    const listingTypes = Array.from(new Set(restaurants.map((r: any) => r.listing_type || r.category).filter(Boolean))).sort();
    const kosherCategories = Array.from(new Set(restaurants.map((r: any) => r.kosher_category || r.kosher_type).filter(Boolean))).sort();
    const priceRanges = Array.from(new Set(restaurants.map((r: any) => r.price_range).filter(Boolean))).sort();
    
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