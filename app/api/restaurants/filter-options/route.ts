import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // In a real implementation, you would query your database
    // to get the actual available options from your data
    
    // For now, return static options based on the database schema
    const filterOptions = {
      cities: [
        'New York',
        'Los Angeles',
        'Chicago',
        'Miami',
        'Boston',
        'Philadelphia',
        'Washington DC',
        'Atlanta',
        'Dallas',
        'Houston',
        'Phoenix',
        'Denver',
        'Seattle',
        'San Francisco',
        'Las Vegas',
        'Orlando',
        'Tampa',
        'Austin',
        'Nashville',
        'Portland'
      ],
      states: [
        'New York',
        'California',
        'Illinois',
        'Florida',
        'Texas',
        'Pennsylvania',
        'Ohio',
        'Georgia',
        'North Carolina',
        'Michigan',
        'New Jersey',
        'Virginia',
        'Washington',
        'Arizona',
        'Massachusetts',
        'Tennessee',
        'Indiana',
        'Missouri',
        'Maryland',
        'Colorado'
      ],
      agencies: [
        'ORB',
        'KM', 
        'Star-K',
        'CRC',
        'Kof-K',
        'Diamond K',
        'OU',
        'OK',
        'Chabad',
        'Local Rabbi'
      ],
      listingTypes: [
        'restaurant',
        'bakery',
        'catering',
        'grocery',
        'market',
        'deli',
        'pizza',
        'ice cream',
        'coffee shop',
        'food truck'
      ],
      priceRanges: [
        '$',
        '$$',
        '$$$',
        '$$$$'
      ],
      kosherCategories: [
        'meat',
        'dairy',
        'pareve',
        'fish',
        'unknown'
      ]
    };

    return NextResponse.json({
      success: true,
      data: filterOptions
    });

  } catch (error) {
    console.error('Error fetching filter options:', error);
    return NextResponse.json({
      success: false,
      message: 'Failed to fetch filter options'
    }, { status: 500 });
  }
} 