export interface Restaurant {
  id: number;
  created_at?: string;
  updated_at?: string;
  name: string;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  phone_number: string;
  website?: string;
  certificate_link?: string;
  image_url?: string;
  google_listing_url?: string;
  certifying_agency: string;
  kosher_category: 'meat' | 'dairy' | 'pareve';
  is_cholov_yisroel?: boolean;
  is_pas_yisroel?: boolean;
  listing_type: string;
  status: string;
  status_reason?: string;
  is_open?: boolean;
  next_open_time?: string;
  hours_of_operation?: string;
  hours_open?: string;
  hours_json?: string;
  hours_last_updated?: string;
  timezone?: string;
  current_time_local?: string;
  hours_parsed?: boolean;
  short_description?: string;
  price_range?: string;
  avg_price?: string;
  menu_pricing?: MenuPricing;
  min_avg_meal_cost?: number;
  max_avg_meal_cost?: number;
  notes?: string;
  latitude?: number;
  longitude?: number;
  specials?: RestaurantSpecial[];
  // Rating and review fields
  rating?: number;
  star_rating?: number;
  quality_rating?: number;
  review_count?: number;
  // Google Reviews
  google_rating?: number;
  google_review_count?: number;
  google_reviews?: string; // JSON string of reviews
}

export interface RestaurantSpecial {
  id: number;
  restaurant_id: number;
  title: string;
  description?: string;
  discount_percent?: number;
  discount_amount?: number;
  start_date?: string;
  end_date?: string;
  is_paid: boolean;
  payment_status: string;
  special_type: 'discount' | 'promotion' | 'event';
  priority: number;
  is_active: boolean;
  created_date: string;
  updated_date: string;
}

export interface MenuPricing {
  [section: string]: {
    min: number;
    max: number;
    avg: number;
  };
}

export interface RestaurantCardProps {
  restaurant: Restaurant;
  onClick?: () => void;
}

export interface RestaurantGridProps {
  restaurants: Restaurant[];
  currentPage?: number;
  totalPages?: number;
  onPageChange?: (page: number) => void;
  totalRestaurants?: number;
}

export interface SearchBarProps {
  onSearch: (query: string) => void;
}

export interface CategoryNavProps {
  selectedCategory: string;
  onCategoryChange: (category: string) => void;
}

 