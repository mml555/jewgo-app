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
  private static async wakeUpBackend(): Promise<boolean> {
    try {
      console.log('Attempting to wake up backend service...');
      const response = await fetch(`${API_BASE_URL}/`, {
        method: 'GET',
        signal: AbortSignal.timeout(5000) // 5 second timeout for wake-up
      });
      return response.ok;
    } catch (error) {
      console.log('Wake-up attempt failed, continuing with normal request...');
      return false;
    }
  }

  private static async makeRequest<T>(
    endpoint: string, 
    options: RequestInit = {},
    retries: number = 3,
    timeout: number = 15000 // 15 second timeout
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
        
        // On first attempt, try to wake up the backend if it's the main restaurants endpoint
        if (attempt === 1 && endpoint.includes('/api/restaurants')) {
          await this.wakeUpBackend();
        }
        
        // Create AbortController for timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout);
        
        const response = await fetch(url, {
          ...config,
          signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
          const error: ApiError = {
            message: `HTTP error! status: ${response.status}`,
            status: response.status,
            retryable: response.status >= 500 || response.status === 429
          };
          
          // For 404 errors, don't retry
          if (response.status === 404) {
            throw error;
          }
          
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
        
        // Handle timeout errors specifically
        if (error instanceof Error && error.name === 'AbortError') {
          console.error(`Request timed out after ${timeout}ms`);
          if (attempt === retries) {
            throw new Error(`Request timed out after ${timeout}ms - the backend server may be down or overloaded`);
          }
        }
        
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
      const data = await this.makeRequest<any>(`/api/restaurants?limit=${limit}`);
      
      // Handle different response formats
      let restaurants: Restaurant[] = [];
      let total: number = 0;
      
      if (data && typeof data === 'object') {
        if (Array.isArray(data)) {
          // Direct array response
          restaurants = data;
          total = data.length;
        } else if (data.restaurants && Array.isArray(data.restaurants)) {
          // Wrapped response
          restaurants = data.restaurants;
          total = data.total || data.restaurants.length;
        } else {
          console.warn('Unexpected API response format:', data);
          restaurants = [];
          total = 0;
        }
      }
      
      return {
        restaurants,
        total
      };
    } catch (error) {
      console.error('Failed to fetch restaurants:', error);
      
      // Return empty response on error
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
      
      // Validate the response structure
      if (!data || typeof data !== 'object') {
        console.error(`Invalid response format for restaurant ${id}:`, data);
        return null;
      }
      
      // Check if it's a valid restaurant object
      if (!data.id || !data.name) {
        console.error(`Invalid restaurant data for ID ${id}:`, data);
        return null;
      }
      
      return data;
    } catch (error: any) {
      // Handle 404 errors gracefully
      if (error.status === 404) {
        console.warn(`Restaurant ${id} not found`);
        return null;
      }
      
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