import { Restaurant } from '@/types/restaurant';

/**
 * Validates if a restaurant object has the required properties
 */
export function isValidRestaurant(restaurant: any): restaurant is Restaurant {
  return (
    restaurant &&
    typeof restaurant === 'object' &&
    typeof restaurant.id === 'number' &&
    typeof restaurant.name === 'string' &&
    typeof restaurant.address === 'string' &&
    typeof restaurant.city === 'string' &&
    typeof restaurant.state === 'string' &&
    typeof restaurant.certifying_agency === 'string' &&
    typeof restaurant.kosher_category === 'string' &&
    typeof restaurant.listing_type === 'string' &&
    typeof restaurant.status === 'string'
  );
}

/**
 * Validates and filters an array of restaurants
 */
export function validateRestaurants(restaurants: any[]): Restaurant[] {
  if (!Array.isArray(restaurants)) {
    console.warn('validateRestaurants: Input is not an array:', typeof restaurants);
    return [];
  }

  const validRestaurants = restaurants.filter(isValidRestaurant);
  
  if (validRestaurants.length !== restaurants.length) {
    console.warn(`validateRestaurants: Filtered out ${restaurants.length - validRestaurants.length} invalid restaurants`);
  }

  return validRestaurants;
}

/**
 * Safely accesses nested object properties
 */
export function safeGet<T>(obj: any, path: string, defaultValue: T): T {
  try {
    const keys = path.split('.');
    let result = obj;
    
    for (const key of keys) {
      if (result == null || typeof result !== 'object') {
        return defaultValue;
      }
      result = result[key];
    }
    
    return result !== undefined ? result : defaultValue;
  } catch (error) {
    console.warn('safeGet error:', error);
    return defaultValue;
  }
}

/**
 * Safely filters an array
 */
export function safeFilter<T>(array: T[] | null | undefined, predicate: (item: T) => boolean): T[] {
  if (!Array.isArray(array)) {
    console.warn('safeFilter: Input is not an array:', typeof array);
    return [];
  }
  
  try {
    return array.filter(predicate);
  } catch (error) {
    console.error('safeFilter error:', error);
    return [];
  }
}

/**
 * Safely maps an array
 */
export function safeMap<T, U>(array: T[] | null | undefined, mapper: (item: T) => U): U[] {
  if (!Array.isArray(array)) {
    console.warn('safeMap: Input is not an array:', typeof array);
    return [];
  }
  
  try {
    return array.map(mapper);
  } catch (error) {
    console.error('safeMap error:', error);
    return [];
  }
}

/**
 * Validates API response structure
 */
export function validateApiResponse(response: any): { isValid: boolean; data?: any; error?: string } {
  if (!response) {
    return { isValid: false, error: 'Response is null or undefined' };
  }

  if (typeof response !== 'object') {
    return { isValid: false, error: 'Response is not an object' };
  }

  // Check if response has restaurants property
  if (response.restaurants && !Array.isArray(response.restaurants)) {
    return { isValid: false, error: 'Restaurants property is not an array' };
  }

  // Check if response has data property
  if (response.data && !Array.isArray(response.data)) {
    return { isValid: false, error: 'Data property is not an array' };
  }

  return { isValid: true, data: response };
} 