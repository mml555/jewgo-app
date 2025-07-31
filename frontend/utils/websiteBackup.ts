/**
 * Website Backup Utility
 * =====================
 * 
 * Utility functions to automatically fetch website links from Google Places API
 * when restaurants don't have them.
 */

export interface WebsiteFetchResponse {
  success: boolean;
  website?: string;
  message: string;
  restaurant_id?: number;
  restaurant_name?: string;
}

export interface BulkWebsiteFetchResponse {
  success: boolean;
  message: string;
  updated: number;
  total_checked: number;
  limit_used: number;
}

/**
 * Fetch website link for a specific restaurant using Google Places API
 */
export async function fetchRestaurantWebsite(restaurantId: number): Promise<WebsiteFetchResponse> {
  try {
    const response = await fetch(`/api/restaurants/${restaurantId}/fetch-website`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();

    if (response.ok) {
      return {
        success: true,
        website: data.website,
        message: data.message,
        restaurant_id: data.restaurant_id,
        restaurant_name: data.restaurant_name,
      };
    } else {
      return {
        success: false,
        message: data.error || 'Failed to fetch website',
        restaurant_id: restaurantId,
      };
    }
  } catch (error) {
    console.error('Error fetching restaurant website:', error);
    return {
      success: false,
      message: 'Network error while fetching website',
      restaurant_id: restaurantId,
    };
  }
}

/**
 * Fetch website links for multiple restaurants that don't have them
 */
export async function fetchMissingWebsites(limit: number = 10): Promise<BulkWebsiteFetchResponse> {
  try {
    const response = await fetch('/api/restaurants/fetch-missing-websites', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ limit }),
    });

    const data = await response.json();

    if (response.ok) {
      return {
        success: true,
        message: data.message,
        updated: data.updated,
        total_checked: data.total_checked,
        limit_used: data.limit_used,
      };
    } else {
      return {
        success: false,
        message: data.error || 'Failed to fetch missing websites',
        updated: 0,
        total_checked: 0,
        limit_used: limit,
      };
    }
  } catch (error) {
    console.error('Error fetching missing websites:', error);
    return {
      success: false,
      message: 'Network error while fetching missing websites',
      updated: 0,
      total_checked: 0,
      limit_used: limit,
    };
  }
}

/**
 * Check if a restaurant needs a website link and fetch it if needed
 */
export async function ensureRestaurantWebsite(restaurant: any): Promise<string | null> {
  // If restaurant already has a website, return it
  if (restaurant.website && restaurant.website.length > 10) {
    return restaurant.website;
  }

  // Try to fetch website from Google Places API
  const result = await fetchRestaurantWebsite(restaurant.id);
  
  if (result.success && result.website) {
    return result.website;
  }

  return null;
}

/**
 * Get a fallback website link for a restaurant
 * This can be used when the restaurant doesn't have a website
 */
export function getFallbackWebsiteLink(restaurant: any): string | null {
  // If restaurant has a Google listing URL, use that as fallback
  if (restaurant.google_listing_url) {
    return restaurant.google_listing_url;
  }

  // If restaurant has a detail URL, use that as fallback
  if (restaurant.detail_url) {
    return restaurant.detail_url;
  }

  // Create a Google Maps search URL as last resort
  if (restaurant.address) {
    const searchQuery = encodeURIComponent(`${restaurant.name} ${restaurant.address}`);
    return `https://maps.google.com/?q=${searchQuery}`;
  }

  return null;
} 