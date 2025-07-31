'use client';

import { useState, useEffect, useMemo, useCallback } from 'react';
import Header from '@/components/Header';
import EnhancedSearch from '@/components/EnhancedSearch';
import ActionButtons from '@/components/ActionButtons';
import RestaurantGrid from '@/components/RestaurantGrid';
import BottomNavigation from '@/components/BottomNavigation';
import SplashScreen from '@/components/SplashScreen';
import { Restaurant } from '@/types/restaurant';
import NavTabs from '@/components/NavTabs';

export default function HomePageClient() {
  const [allRestaurants, setAllRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(true);
  const [showSplash, setShowSplash] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(20);
  const [userLocation, setUserLocation] = useState<{latitude: number, longitude: number} | null>(null);
  const [locationLoading, setLocationLoading] = useState(false);
  const [sortByDistance, setSortByDistance] = useState(false);
  const [activeFilters, setActiveFilters] = useState<{
    agency?: string;
    kosherType?: string;
    openNow?: boolean;
    category?: string;
    nearMe?: boolean;
    distanceRadius?: number;
    is_cholov_yisroel?: boolean;
    is_pas_yisroel?: boolean;
    is_glatt?: boolean;
    is_mehadrin?: boolean;
    is_bishul_yisroel?: boolean;
  }>({});
  const [activeTab, setActiveTab] = useState('eatery');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (mounted) {
      console.log('useEffect called - fetching restaurants');
      fetchAllRestaurants();
    }
  }, [mounted]);

  // Memoized filtered restaurants to prevent unnecessary recalculations
  const filteredRestaurants = useMemo(() => {
    if (allRestaurants.length === 0) return [];
    
    let filtered = [...allRestaurants];
    
    // Apply search query filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase().trim();
      filtered = filtered.filter(restaurant => 
        restaurant.name?.toLowerCase().includes(query) ||
        restaurant.address?.toLowerCase().includes(query) ||
        restaurant.city?.toLowerCase().includes(query) ||
        restaurant.state?.toLowerCase().includes(query) ||
        restaurant.certifying_agency?.toLowerCase().includes(query) ||
        restaurant.listing_type?.toLowerCase().includes(query) ||
        restaurant.kosher_category?.toLowerCase().includes(query)
      );
    }
    
    // Apply agency filter
    if (activeFilters.agency) {
      filtered = filtered.filter(restaurant => 
        restaurant.certifying_agency && 
        restaurant.certifying_agency.toLowerCase().includes(activeFilters.agency!.toLowerCase())
      );
    }
    
    // Apply kosher type filter
    if (activeFilters.kosherType && activeFilters.kosherType !== 'all') {
      filtered = filtered.filter(restaurant => {
        const kosherCategory = restaurant.kosher_category?.toLowerCase() || restaurant.kosher_type?.toLowerCase() || '';
        return kosherCategory === activeFilters.kosherType.toLowerCase();
      });
    }
    
    // Apply kosher features filters
    if (activeFilters.is_cholov_yisroel) {
      filtered = filtered.filter(restaurant => restaurant.is_cholov_yisroel === true);
    }
    
    if (activeFilters.is_pas_yisroel) {
      filtered = filtered.filter(restaurant => restaurant.is_pas_yisroel === true);
    }
    
    if (activeFilters.is_glatt) {
      filtered = filtered.filter(restaurant => restaurant.is_glatt === true);
    }
    
    if (activeFilters.is_mehadrin) {
      filtered = filtered.filter(restaurant => restaurant.is_mehadrin === true);
    }
    
    if (activeFilters.is_bishul_yisroel) {
      filtered = filtered.filter(restaurant => restaurant.is_bishul_yisroel === true);
    }
    
    // Apply category filter
    if (activeFilters.category) {
      filtered = filtered.filter(restaurant => 
        restaurant.listing_type && 
        restaurant.listing_type.toLowerCase().includes(activeFilters.category!.toLowerCase())
      );
    }
    
    // Apply "near me" filter
    if (activeFilters.nearMe && userLocation) {
      const maxDistance = activeFilters.distanceRadius || 10; // Default 10 miles
      filtered = filtered.filter(restaurant => {
        if (!restaurant.latitude || !restaurant.longitude) return false;
        const distance = calculateDistance(
          userLocation.latitude, 
          userLocation.longitude, 
          restaurant.latitude, 
          restaurant.longitude
        );
        return distance <= maxDistance;
      });
    }
    
    // Sort by distance if user location is available
    if (userLocation) {
      filtered.sort((a, b) => {
        if (!a.latitude || !a.longitude) return 1;
        if (!b.latitude || !b.longitude) return -1;
        
        const distanceA = calculateDistance(
          userLocation.latitude, 
          userLocation.longitude, 
          a.latitude, 
          a.longitude
        );
        const distanceB = calculateDistance(
          userLocation.latitude, 
          userLocation.longitude, 
          b.latitude, 
          b.longitude
        );
        
        return distanceA - distanceB;
      });
    }
    
    return filtered;
  }, [allRestaurants, searchQuery, activeFilters, userLocation]);

  // Memoized paginated restaurants
  const displayedRestaurants = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const result = filteredRestaurants.slice(startIndex, endIndex);
    console.log(`Pagination: Page ${currentPage}, showing ${result.length} restaurants (${startIndex}-${endIndex} of ${filteredRestaurants.length})`);
    return result;
  }, [filteredRestaurants, currentPage, itemsPerPage]);

  // Memoized total count and pages
  const totalFilteredRestaurants = useMemo(() => filteredRestaurants.length, [filteredRestaurants]);
  const totalPages = useMemo(() => {
    const pages = Math.ceil(totalFilteredRestaurants / itemsPerPage);
    console.log(`Total pages calculation: ${totalFilteredRestaurants} restaurants, ${itemsPerPage} per page = ${pages} pages`);
    return pages;
  }, [totalFilteredRestaurants, itemsPerPage]);

  // Validate current page when total pages change
  useEffect(() => {
    // Only reset to page 1 if current page is greater than total pages AND total pages is greater than 0
    // This prevents unnecessary resets when filters are applied
    if (totalPages > 0 && currentPage > totalPages) {
      console.log(`Page validation: Resetting from page ${currentPage} to page 1 (total pages: ${totalPages})`);
      setCurrentPage(1);
    }
  }, [totalPages, currentPage]);

  const handleTabChange = (tab: string) => {
    // If specials tab is clicked, redirect to the specials page
    if (tab === 'specials') {
      window.location.href = '/specials';
      return;
    }
    
    setActiveTab(tab);
    setCurrentPage(1);
    setSearchQuery('');
  };

  const requestUserLocation = () => {
    if (!navigator.geolocation) {
      console.log('Geolocation is not supported by this browser');
      return;
    }

    // Only request location if not already obtained
    if (userLocation) {
      console.log('Location already available:', userLocation);
      return;
    }

    setLocationLoading(true);
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const location = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        };
        console.log('User location obtained:', location);
        setUserLocation(location);
        setLocationLoading(false);
      },
      (error) => {
        console.log('Error getting location:', error);
        
        // Handle specific geolocation errors gracefully
        if (error.code === 1) {
          console.log('Geolocation permission denied or blocked by policy');
          // Continue without location - app will work with default behavior
        } else if (error.code === 2) {
          console.log('Geolocation position unavailable');
        } else if (error.code === 3) {
          console.log('Geolocation request timed out');
        }
        
        setLocationLoading(false);
        // Don't set an error state - just continue without location
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 300000,
      }
    );
  };

  // Function to request location on user interaction
  const handleLocationRequest = () => {
    console.log('User requested location access');
    requestUserLocation();
  };

  const fetchAllRestaurants = async () => {
    try {
      console.log('Fetching restaurants...');
      const response = await fetch('/api/restaurants?limit=1000');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Restaurants fetched:', data.data?.length || 0);
      
      if (data.data) {
        setAllRestaurants(data.data);
        // Removed setDisplayedRestaurants since we now use memoized displayedRestaurants
      } else {
        setApiError('No restaurants data received');
      }
    } catch (error) {
      console.error('Error fetching restaurants:', error);
      setApiError('Failed to fetch restaurants');
    } finally {
      setLoading(false);
      setShowSplash(false);
    }
  };

  const handleSearch = useCallback((query: string) => {
    setSearchQuery(query);
    setCurrentPage(1); // Reset to first page when searching
  }, []);

  const handleResultsUpdate = useCallback((results: Restaurant[]) => {
    console.log('Enhanced search results:', results.length, 'restaurants');
    // Update the all restaurants with the enhanced results
    // The displayed restaurants will be automatically updated via memoization
    setAllRestaurants(results);
  }, []);

  const handleFilterChange = (key: string, value: any) => {
    setActiveFilters(prev => ({ ...prev, [key]: value }));
    setCurrentPage(1);
    
    // Request location when user enables location-based features
    if (key === 'nearMe' && value === true) {
      handleLocationRequest();
    }
  };

  const handleToggleFilter = (key: string, value: boolean) => {
    setActiveFilters(prev => ({ ...prev, [key]: value }));
    setCurrentPage(1);
  };

  const handleDistanceChange = (distance: number) => {
    setActiveFilters(prev => ({ ...prev, distanceRadius: distance }));
    setCurrentPage(1);
  };

  const handleClearAll = () => {
    setActiveFilters({});
    setSearchQuery('');
    setCurrentPage(1);
  };

  const handlePageChange = (page: number) => {
    console.log(`HomePageClient: Changing page from ${currentPage} to ${page}`);
    setCurrentPage(page);
  };

  // Helper function to calculate distance between two points
  const calculateDistance = (lat1: number, lon1: number, lat2: number, lon2: number): number => {
    const R = 3959; // Earth's radius in miles
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
  };

  // Don't render until mounted to prevent hydration issues
  if (!mounted) {
    return <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-gray-500">Loading...</div>
    </div>;
  }

  if (showSplash) {
    return <SplashScreen />;
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <div className="flex-1 pb-20 sm:pb-24">
        {/* Header */}
        <Header />

        {/* Search and Navigation Section */}
        <div className="sticky top-0 z-40 bg-white/95 backdrop-blur-sm border-b border-gray-100">
          {/* Search Bar */}
          <div className="px-4 py-3 sm:px-6">
            <EnhancedSearch onSearch={handleSearch} onResultsUpdate={handleResultsUpdate} />
          </div>

          {/* Navigation Tabs */}
          <div className="px-4 sm:px-6">
            <NavTabs activeTab={activeTab} onTabChange={handleTabChange} />
          </div>
        </div>

        {/* Main Content */}
        {activeTab === 'eatery' && (
          <>
            {/* Action Buttons */}
            <div className="px-4 py-4 sm:px-6 sm:py-6 space-y-4">
              <ActionButtons 
                isOnMapPage={false}
                onShowFilters={() => {}}
                onShowMap={() => window.location.href = '/live-map'}
                onAddEatery={() => window.location.href = '/add-eatery'}
                onFilterChange={handleFilterChange}
                onToggleFilter={handleToggleFilter}
                onDistanceChange={handleDistanceChange}
                onClearAll={handleClearAll}
                activeFilters={activeFilters}
                userLocation={userLocation ? { lat: userLocation.latitude, lng: userLocation.longitude } : null}
                locationLoading={locationLoading}
                hasActiveFilters={Object.values(activeFilters || {}).some(filter => filter !== undefined && filter !== false)}
              />
            </div>

            {/* Restaurant Grid */}
            <div className="px-4 sm:px-6 pb-4">
              {loading ? (
                <div className="flex justify-center items-center py-12">
                  <div className="text-gray-500">Loading restaurants...</div>
                </div>
              ) : apiError ? (
                <div className="flex justify-center items-center py-12">
                  <div className="text-red-500">{apiError}</div>
                </div>
              ) : (
                <RestaurantGrid 
                  restaurants={displayedRestaurants} 
                  currentPage={currentPage}
                  totalPages={totalPages}
                  onPageChange={handlePageChange}
                  totalRestaurants={totalFilteredRestaurants}
                  userLocation={userLocation}
                  loading={loading}
                />
              )}
            </div>
          </>
        )}

        {activeTab === 'mikvahs' && (
          <div className="px-4 sm:px-6 pb-32">
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <div className="text-gray-500 mb-4">
                <svg className="h-16 w-16 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 18h16" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M6 19h2" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M10 19h2" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M14 19h2" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M18 19h2" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 6v12" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 6v12" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 8h8" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h8" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16h8" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">Mikvahs Coming Soon</h3>
              <p className="text-gray-600">
                Mikvah locations and information will be available here soon.
              </p>
            </div>
          </div>
        )}

        {activeTab === 'shuls' && (
          <div className="px-4 sm:px-6 pb-32">
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <div className="text-gray-500 mb-4">
                <svg className="h-16 w-16 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">Shuls Coming Soon</h3>
              <p className="text-gray-600">
                Synagogue locations and information will be available here soon.
              </p>
            </div>
          </div>
        )}

        {activeTab === 'stores' && (
          <div className="px-4 sm:px-6 pb-32">
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <div className="text-gray-500 mb-4">
                <svg className="h-16 w-16 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">Stores Coming Soon</h3>
              <p className="text-gray-600">
                Kosher grocery stores and markets will be available here soon.
              </p>
            </div>
          </div>
        )}
        
        {/* Bottom Navigation */}
        <BottomNavigation />
      </div>
    </div>
  );
} 