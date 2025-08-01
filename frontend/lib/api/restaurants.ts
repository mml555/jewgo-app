import { Restaurant } from '@/types/restaurant';

const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL 
  ? process.env.NEXT_PUBLIC_BACKEND_URL
  : process.env.NODE_ENV === 'production'
  ? 'https://jewgo.onrender.com'
  : 'http://127.0.0.1:8081';

interface RestaurantsResponse {
  restaurants: Restaurant[];
  total: number;
}

interface ApiError {
  message: string;
  status?: number;
  retryable: boolean;
}

export class RestaurantsAPI {
  private static async makeRequest<T>(
    endpoint: string, 
    options: RequestInit = {},
    retries: number = 3
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const defaultHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };

    const config: RequestInit = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    };

    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        console.log(`API request attempt ${attempt}/${retries}: ${url}`);
        
        const response = await fetch(url, config);
        
        if (!response.ok) {
          const error: ApiError = {
            message: `HTTP error! status: ${response.status}`,
            status: response.status,
            retryable: response.status >= 500 || response.status === 429
          };
          
          if (error.retryable && attempt < retries) {
            console.warn(`Retryable error, attempting retry ${attempt + 1}/${retries}`);
            await new Promise(resolve => setTimeout(resolve, 1000 * attempt)); // Exponential backoff
            continue;
          }
          
          throw error;
        }

        // Check if response has content
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
          const data = await response.json();
          console.log(`API request successful: ${url}`);
          return data;
        } else {
          throw new Error('Invalid response format - expected JSON');
        }
      } catch (error) {
        console.error(`API request failed (attempt ${attempt}/${retries}):`, error);
        
        if (attempt === retries) {
          throw error;
        }
        
        // Wait before retry
        await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
      }
    }
    
    throw new Error('All retry attempts failed');
  }

  static async fetchRestaurants(limit: number = 1000): Promise<RestaurantsResponse> {
    try {
      const data = await this.makeRequest<RestaurantsResponse>(`/api/restaurants?limit=${limit}`);
      
      if (!data.restaurants) {
        throw new Error('Invalid response format - missing restaurants array');
      }
      
      return {
        restaurants: data.restaurants,
        total: data.total || data.restaurants.length
      };
    } catch (error) {
      console.error('Failed to fetch restaurants from API:', error);
      
      // Return empty data as fallback
      return {
        restaurants: [],
        total: 0
      };
    }
  }

  static async searchRestaurants(query: string, limit: number = 100): Promise<RestaurantsResponse> {
    try {
      const data = await this.makeRequest<RestaurantsResponse>(`/api/restaurants/search?q=${encodeURIComponent(query)}&limit=${limit}`);
      
      return {
        restaurants: data.restaurants || [],
        total: data.total || 0
      };
    } catch (error) {
      console.error('Failed to search restaurants:', error);
      return {
        restaurants: [],
        total: 0
      };
    }
  }

  static async getRestaurant(id: number): Promise<Restaurant | null> {
    try {
      const data = await this.makeRequest<Restaurant>(`/api/restaurants/${id}`);
      return data;
    } catch (error) {
      console.error(`Failed to fetch restaurant ${id}:`, error);
      return null;
    }
  }

  static async getStatistics(): Promise<any> {
    try {
      const data = await this.makeRequest<any>('/api/statistics');
      return data;
    } catch (error) {
      console.error('Failed to fetch statistics:', error);
      return {
        total_restaurants: 0,
        total_cities: 0,
        total_states: 0
      };
    }
  }

  // Fallback mock data for when API is completely unavailable
  static getMockRestaurants(): Restaurant[] {
    return [
      {
        id: 1,
        name: 'Kosher Deli & Grill',
        address: '123 Main St',
        city: 'Miami',
        state: 'FL',
        zip_code: '33101',
        phone_number: '(305) 555-0123',
        certifying_agency: 'KM',
        kosher_category: 'meat',
        listing_type: 'restaurant',
        status: 'active',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z'
      },
      {
        id: 2,
        name: 'Miami Kosher Market',
        address: '456 Oak Ave',
        city: 'Miami Beach',
        state: 'FL',
        zip_code: '33139',
        phone_number: '(305) 555-0456',
        certifying_agency: 'ORB',
        kosher_category: 'dairy',
        listing_type: 'restaurant',
        status: 'active',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z'
      }
    ];
  }
}

// Export convenience functions
export const fetchRestaurants = (limit?: number) => RestaurantsAPI.fetchRestaurants(limit);
export const searchRestaurants = (query: string, limit?: number) => RestaurantsAPI.searchRestaurants(query, limit);
export const getRestaurant = (id: number) => RestaurantsAPI.getRestaurant(id);
export const getStatistics = () => RestaurantsAPI.getStatistics();
export const getMockRestaurants = () => RestaurantsAPI.getMockRestaurants(); 