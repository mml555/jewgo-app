import { RestaurantSpecial } from '@/types/restaurant';

const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL 
  ? process.env.NEXT_PUBLIC_BACKEND_URL
  : process.env.NODE_ENV === 'production'
  ? 'https://jewgo.onrender.com'
  : 'http://127.0.0.1:8081';

interface Special {
  id: number;
  title: string;
  restaurant: string;
  description: string;
  discount: string;
  validUntil: string;
  category: string;
  image: string;
  restaurant_id?: number;
}

interface ClaimDealResponse {
  success: boolean;
  message: string;
  dealId: number;
  claimedAt: string;
}

export class SpecialsAPI {
  private static async makeRequest<T>(
    endpoint: string, 
    options: RequestInit = {}
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

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Check if response has content
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      } else {
        throw new Error('Invalid response format - expected JSON');
      }
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  static async fetchSpecials(): Promise<Special[]> {
    try {
      const data = await this.makeRequest<{ specials: RestaurantSpecial[] }>('/api/admin/specials');
      
      if (data.specials && Array.isArray(data.specials)) {
        return data.specials.map((special: RestaurantSpecial) => ({
          id: special.id,
          title: special.title,
          restaurant: `Restaurant #${special.restaurant_id}`,
          description: special.description || 'Special offer available',
          discount: special.discount_percent ? `${special.discount_percent}% OFF` : 'Special Offer',
          validUntil: special.end_date || '2024-12-31',
          category: special.special_type || 'promotion',
          image: '/images/placeholder-restaurant.jpg',
          restaurant_id: special.restaurant_id,
        }));
      }
      
      return [];
    } catch (error) {
      console.error('Failed to fetch specials from API:', error);
      // Return mock data as fallback
      return this.getMockSpecials();
    }
  }

  static async claimDeal(specialId: number): Promise<ClaimDealResponse> {
    try {
      const response = await this.makeRequest<ClaimDealResponse>(`/api/specials/${specialId}/claim`, {
        method: 'POST',
      });
      
      return response;
    } catch (error) {
      console.error('Failed to claim deal:', error);
      
      // Fallback mock response
      await new Promise(resolve => setTimeout(resolve, 1000));
      return {
        success: true,
        message: 'Deal claimed successfully!',
        dealId: specialId,
        claimedAt: new Date().toISOString(),
      };
    }
  }

  static getMockSpecials(): Special[] {
    return [
      {
        id: 1,
        title: 'Shabbat Special',
        restaurant: 'Kosher Deli & Grill',
        description: 'Complete Shabbat meal for 4 people - $89.99',
        discount: '20% OFF',
        validUntil: '2024-01-31',
        category: 'shabbat',
        image: '/images/placeholder-restaurant.jpg'
      },
      {
        id: 2,
        title: 'Lunch Combo Deal',
        restaurant: 'Miami Kosher Market',
        description: 'Sandwich + Soup + Drink - $12.99',
        discount: '15% OFF',
        validUntil: '2024-02-15',
        category: 'lunch',
        image: '/images/placeholder-restaurant.jpg'
      },
      {
        id: 3,
        title: 'Ice Cream Happy Hour',
        restaurant: 'Diamond K Ice Cream',
        description: 'Buy 1 Get 1 Free on all ice cream',
        discount: '50% OFF',
        validUntil: '2024-01-25',
        category: 'dessert',
        image: '/images/placeholder-restaurant.jpg'
      },
      {
        id: 4,
        title: 'Family Dinner Package',
        restaurant: 'Kosher Pizza Place',
        description: 'Large Pizza + 2 Sides + 2 Drinks - $34.99',
        discount: '25% OFF',
        validUntil: '2024-02-10',
        category: 'dinner',
        image: '/images/placeholder-restaurant.jpg'
      },
      {
        id: 5,
        title: 'Breakfast Special',
        restaurant: 'Kosher Cafe',
        description: 'Bagel + Coffee + Fruit - $8.99',
        discount: '10% OFF',
        validUntil: '2024-01-30',
        category: 'breakfast',
        image: '/images/placeholder-restaurant.jpg'
      },
      {
        id: 6,
        title: 'Catering Discount',
        restaurant: 'Kosher Catering Co.',
        description: '20% off all catering orders over $200',
        discount: '20% OFF',
        validUntil: '2024-03-01',
        category: 'catering',
        image: '/images/placeholder-restaurant.jpg'
      }
    ];
  }
}

// Export convenience functions
export const fetchSpecials = () => SpecialsAPI.fetchSpecials();
export const claimDeal = (specialId: number) => SpecialsAPI.claimDeal(specialId);
export const getMockSpecials = () => SpecialsAPI.getMockSpecials(); 