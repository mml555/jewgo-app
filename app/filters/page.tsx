'use client';

import React, { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import EnhancedFilters, { FilterState } from '@/components/EnhancedFilters';
import RestaurantCard from '@/components/RestaurantCard';
import { Restaurant } from '@/types/restaurant';

const FiltersPage: React.FC = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  // Initialize filters from URL params
  const [filters, setFilters] = useState<FilterState>(() => {
    const initialFilters: FilterState = {};
    
    // Parse URL parameters
    if (searchParams.get('search')) initialFilters.search = searchParams.get('search')!;
    if (searchParams.get('city')) initialFilters.city = searchParams.get('city')!;
    if (searchParams.get('state')) initialFilters.state = searchParams.get('state')!;
    if (searchParams.get('certifying_agency')) initialFilters.certifying_agency = searchParams.get('certifying_agency')!;
    if (searchParams.get('kosher_category')) initialFilters.kosher_category = searchParams.get('kosher_category') as any;
    if (searchParams.get('is_cholov_yisroel')) initialFilters.is_cholov_yisroel = searchParams.get('is_cholov_yisroel') === 'true';
    if (searchParams.get('listing_type')) initialFilters.listing_type = searchParams.get('listing_type')!;
    if (searchParams.get('price_range')) initialFilters.price_range = searchParams.get('price_range')!;
    if (searchParams.get('min_rating')) initialFilters.min_rating = parseFloat(searchParams.get('min_rating')!);
    if (searchParams.get('has_reviews')) initialFilters.has_reviews = searchParams.get('has_reviews') === 'true';
    if (searchParams.get('near_me')) initialFilters.near_me = searchParams.get('near_me') === 'true';
    if (searchParams.get('open_now')) initialFilters.open_now = searchParams.get('open_now') === 'true';
    if (searchParams.get('max_distance')) initialFilters.max_distance = parseInt(searchParams.get('max_distance')!);
    
    return initialFilters;
  });

  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(false);
  const [userLocation, setUserLocation] = useState<{ latitude: number; longitude: number } | null>(null);
  const [locationLoading, setLocationLoading] = useState(false);
  const [availableData, setAvailableData] = useState({
    cities: [],
    states: [],
    agencies: ['ORB', 'KM', 'Star-K', 'CRC', 'Kof-K', 'Diamond K'],
    listingTypes: ['restaurant', 'bakery', 'catering', 'grocery', 'market'],
    priceRanges: ['$', '$$', '$$$', '$$$$']
  });

  // Get user location
  useEffect(() => {
    const getUserLocation = async () => {
      setLocationLoading(true);
      try {
        if (navigator.geolocation) {
          const position = await new Promise<GeolocationPosition>((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject, {
              enableHighAccuracy: true,
              timeout: 10000,
              maximumAge: 300000 // 5 minutes
            });
          });
          
          setUserLocation({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          });
        }
      } catch (error) {
        console.log('Location access denied or unavailable');
      } finally {
        setLocationLoading(false);
      }
    };

    getUserLocation();
  }, []);

  // Load available filter data
  useEffect(() => {
    const loadAvailableData = async () => {
      try {
        // In a real app, you'd fetch this from your API
        const response = await fetch('/api/restaurants/filter-options');
        if (response.ok) {
          const data = await response.json();
          setAvailableData(data);
        }
      } catch (error) {
        console.error('Error loading filter options:', error);
      }
    };

    loadAvailableData();
  }, []);

  // Update URL when filters change
  useEffect(() => {
    const params = new URLSearchParams();
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== false && value !== '') {
        params.set(key, String(value));
      }
    });

    const newUrl = `/filters?${params.toString()}`;
    router.replace(newUrl, { scroll: false });
  }, [filters, router]);

  // Fetch restaurants based on filters
  useEffect(() => {
    const fetchRestaurants = async () => {
      setLoading(true);
      try {
        const params = new URLSearchParams();
        
        // Add filters to query params
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== false && value !== '') {
            params.set(key, String(value));
          }
        });

        // Add location if available
        if (userLocation && filters.near_me) {
          params.set('lat', userLocation.latitude.toString());
          params.set('lng', userLocation.longitude.toString());
          params.set('radius', (filters.max_distance || 10).toString());
        }

        const response = await fetch(`/api/restaurants?${params.toString()}`);
        if (response.ok) {
          const data = await response.json();
          setRestaurants(data.restaurants || []);
        } else {
          console.error('Failed to fetch restaurants');
          setRestaurants([]);
        }
      } catch (error) {
        console.error('Error fetching restaurants:', error);
        setRestaurants([]);
      } finally {
        setLoading(false);
      }
    };

    fetchRestaurants();
  }, [filters, userLocation]);

  const handleFiltersChange = (newFilters: FilterState) => {
    setFilters(newFilters);
  };

  const handleClearAll = () => {
    setFilters({});
  };

  const getFilteredCount = () => {
    return restaurants.length;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Advanced Filters</h1>
              <p className="text-gray-600 mt-1">
                Find the perfect kosher restaurant with our comprehensive filters
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">
                {getFilteredCount()} restaurants found
              </span>
              <button
                onClick={() => router.push('/')}
                className="px-4 py-2 bg-jewgo-primary text-white rounded-lg hover:bg-jewgo-primary-dark transition-colors"
              >
                Back to Search
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Filters Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-8">
              <EnhancedFilters
                filters={filters}
                onFiltersChange={handleFiltersChange}
                onClearAll={handleClearAll}
                userLocation={userLocation}
                locationLoading={locationLoading}
                availableData={availableData}
              />
            </div>
          </div>

          {/* Results */}
          <div className="lg:col-span-3">
            {/* Loading State */}
            {loading && (
              <div className="flex items-center justify-center py-12">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-jewgo-primary"></div>
                <span className="ml-3 text-gray-600">Loading restaurants...</span>
              </div>
            )}

            {/* No Results */}
            {!loading && restaurants.length === 0 && (
              <div className="text-center py-12">
                <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <h3 className="mt-2 text-sm font-medium text-gray-900">No restaurants found</h3>
                <p className="mt-1 text-sm text-gray-500">
                  Try adjusting your filters or search criteria.
                </p>
                <div className="mt-6">
                  <button
                    onClick={handleClearAll}
                    className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-jewgo-primary hover:bg-jewgo-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-jewgo-primary"
                  >
                    Clear All Filters
                  </button>
                </div>
              </div>
            )}

            {/* Results Grid */}
            {!loading && restaurants.length > 0 && (
              <div>
                <div className="mb-6">
                  <h2 className="text-lg font-semibold text-gray-900">
                    {getFilteredCount()} restaurant{getFilteredCount() !== 1 ? 's' : ''} found
                  </h2>
                  <p className="text-sm text-gray-600 mt-1">
                    Showing results based on your selected filters
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                  {restaurants.map((restaurant) => (
                    <RestaurantCard
                      key={restaurant.id}
                      restaurant={restaurant}
                      onClick={() => router.push(`/restaurant/${restaurant.id}`)}
                    />
                  ))}
                </div>

                {/* Load More Button */}
                {restaurants.length >= 20 && (
                  <div className="mt-8 text-center">
                    <button className="px-6 py-3 bg-white border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors">
                      Load More Results
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default FiltersPage; 