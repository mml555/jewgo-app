'use client';

import { useState, useEffect, useCallback } from 'react';
import Header from '@/components/Header';
import SearchBar from '@/components/SearchBar';
import CategoryNav from '@/components/CategoryNav';
import ActionButtons from '@/components/ActionButtons';
import RestaurantGrid from '@/components/RestaurantGrid';
import BottomNavigation from '@/components/BottomNavigation';
import SplashScreen from '@/components/SplashScreen';

import { Location, sortRestaurantsByDistance, getRestaurantDistance, formatDistance, calculateDistance } from '@/utils/distance';
import { getHoursStatus } from '@/utils/hours';

import { Restaurant } from '@/types/restaurant';
import NavTabs from '@/components/NavTabs';

export default function HomePage() {
  const [allRestaurants, setAllRestaurants] = useState<Restaurant[]>([]);
  const [displayedRestaurants, setDisplayedRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(true);
  const [showSplash, setShowSplash] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(20);
  const [userLocation, setUserLocation] = useState<Location | null>(null);
  const [locationLoading, setLocationLoading] = useState(false);
  const [sortByDistance, setSortByDistance] = useState(false);
  const [activeFilters, setActiveFilters] = useState<{
    agency?: string;
    dietary?: string;
    openNow?: boolean;
    category?: string;
    nearMe?: boolean;
    distanceRadius?: number;
  }>({});
  const [activeTab, setActiveTab] = useState('eatery');

  const handleTabChange = (tab: string) => {
    setActiveTab(tab);
    // Reset to first page when changing tabs
    setCurrentPage(1);
    // Clear search when changing tabs
    setSearchQuery('');
  };


  useEffect(() => {
    console.log('useEffect called - fetching restaurants');
    fetchAllRestaurants();
    requestUserLocation();
  }, []);

  // Debug currentPage changes
  useEffect(() => {
    if (process.env.NODE_ENV === 'development') {
      console.log('=== currentPage changed ===');
      console.log('New currentPage:', currentPage);
    }
  }, [currentPage]);

  const requestUserLocation = () => {
    if (!navigator.geolocation) {
      if (process.env.NODE_ENV === 'development') {
        console.log('Geolocation is not supported by this browser');
      }
      return;
    }

    setLocationLoading(true);
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const location: Location = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        };
        if (process.env.NODE_ENV === 'development') {
          console.log('User location obtained:', location);
        }
        setUserLocation(location);
        setLocationLoading(false);
      },
      (error) => {
        if (process.env.NODE_ENV === 'development') {
          console.log('Error getting location:', error);
        }
        setLocationLoading(false);
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 300000, // 5 minutes
      }
    );
  };

  const handleSortByDistance = () => {
    if (!userLocation) {
      // Request location if not available
      requestUserLocation();
      return;
    }
    setSortByDistance(!sortByDistance);
  };

  const fetchAllRestaurants = async () => {
    try {
      setLoading(true);
      if (process.env.NODE_ENV === 'development') {
        console.log('Fetching restaurants from API...');
      }
      
      // Call the real API
      const response = await fetch('/api/restaurants?limit=1000', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (data.success && data.restaurants) {
        if (process.env.NODE_ENV === 'development') {
          console.log('API returned restaurants:', data.restaurants.length);
        }
        setAllRestaurants(data.restaurants);
      } else {
        throw new Error(data.error || 'Failed to fetch restaurants');
      }
    } catch (error) {
      console.error('Error fetching restaurants:', error);
      setApiError(error instanceof Error ? error.message : 'Unknown error');
    } finally {
      setLoading(false);
      if (process.env.NODE_ENV === 'development') {
      console.log('Loading finished');
    }
    }
  };

  const updateDisplayedRestaurants = useCallback(() => {
    if (process.env.NODE_ENV === 'development') {
      console.log('=== updateDisplayedRestaurants called ===');
      console.log('allRestaurants count:', allRestaurants.length);
    console.log('searchQuery:', searchQuery);
    console.log('activeFilters:', activeFilters);
      console.log('currentPage:', currentPage);
      console.log('itemsPerPage:', itemsPerPage);
      console.log('sortByDistance:', sortByDistance);
      console.log('userLocation:', userLocation);
    }
    
    let filteredRestaurants = allRestaurants;

    // Apply search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filteredRestaurants = allRestaurants.filter(restaurant => {
        // Search in multiple fields
        const searchableFields = [
          restaurant.name,
          restaurant.short_description,
          restaurant.address,
          restaurant.city,
          restaurant.state,
          restaurant.certifying_agency,
          restaurant.kosher_category,
          restaurant.listing_type,
          restaurant.phone_number,
          restaurant.avg_price
        ].filter(Boolean).map(field => field?.toLowerCase());

        // Check if any field contains the query
        return searchableFields.some(field => field?.includes(query));
      });
    }

    // Apply active filters
    if (activeFilters.agency && activeFilters.agency !== 'all') {
      filteredRestaurants = filteredRestaurants.filter(restaurant => {
        if (activeFilters.agency === 'Diamond K') {
          return restaurant.certifying_agency === 'Diamond K';
        } else {
          return restaurant.certifying_agency?.toUpperCase() === activeFilters.agency?.toUpperCase();
        }
      });
    }

    if (activeFilters.dietary) {
      filteredRestaurants = filteredRestaurants.filter(restaurant => {
        const kosherCategory = restaurant.kosher_category?.toLowerCase() || '';
        
        if (activeFilters.dietary === 'meat') {
          return kosherCategory === 'meat';
        } else if (activeFilters.dietary === 'dairy') {
          return kosherCategory === 'dairy';
        } else if (activeFilters.dietary === 'pareve') {
          return kosherCategory === 'pareve';
        }
        return false;
      });
      
      if (process.env.NODE_ENV === 'development') {
        console.log('After dietary filter:', filteredRestaurants.length);
      }
    }

    // Apply "Open Now" filter
    if (activeFilters.openNow) {
      filteredRestaurants = filteredRestaurants.filter(restaurant => {
        const hoursStatus = getHoursStatus(restaurant.hours_open || restaurant.hours_of_operation);
        return hoursStatus.isOpenNow;
      });
      
      if (process.env.NODE_ENV === 'development') {
        console.log('After open now filter:', filteredRestaurants.length);
      }
    }

    // Apply "Near Me" filter (within 5 miles)
    if (activeFilters.nearMe && userLocation) {
      filteredRestaurants = filteredRestaurants.filter(restaurant => {
        if (!restaurant.latitude || !restaurant.longitude) return false;
        
        const distance = calculateDistance(
          userLocation.latitude,
          userLocation.longitude,
          restaurant.latitude,
          restaurant.longitude
        );
        
        return distance <= 5; // Within 5 miles
      });
      
      if (process.env.NODE_ENV === 'development') {
        console.log('After near me filter:', filteredRestaurants.length);
      }
    }

    // Apply category filter
    if (activeFilters.category) {
      filteredRestaurants = filteredRestaurants.filter(restaurant => {
        const category = restaurant.listing_type?.toLowerCase() || '';
        return category === activeFilters.category?.toLowerCase();
      });
      
      if (process.env.NODE_ENV === 'development') {
        console.log('After category filter:', filteredRestaurants.length);
      }
    }

    if (process.env.NODE_ENV === 'development') {
      console.log('filteredRestaurants count:', filteredRestaurants.length);
    }

    // Apply distance sorting if enabled and location is available
    if (sortByDistance && userLocation) {
      filteredRestaurants = sortRestaurantsByDistance(filteredRestaurants, userLocation);
      if (process.env.NODE_ENV === 'development') {
        console.log('Restaurants sorted by distance');
      }
    }

    // Apply pagination
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedRestaurants = filteredRestaurants.slice(startIndex, endIndex);
    
    if (process.env.NODE_ENV === 'development') {
      console.log('Pagination debug:');
      console.log('  currentPage:', currentPage);
      console.log('  itemsPerPage:', itemsPerPage);
      console.log('  startIndex:', startIndex);
      console.log('  endIndex:', endIndex);
      console.log('  filteredRestaurants.length:', filteredRestaurants.length);
      console.log('  paginatedRestaurants count:', paginatedRestaurants.length);
      if (paginatedRestaurants.length > 0) {
        console.log('  First restaurant on this page:', paginatedRestaurants[0].name);
        console.log('  Last restaurant on this page:', paginatedRestaurants[paginatedRestaurants.length - 1].name);
      }
    }
    
    setDisplayedRestaurants(paginatedRestaurants);
    if (process.env.NODE_ENV === 'development') {
      console.log('=== setDisplayedRestaurants called with:', paginatedRestaurants.length, 'restaurants ===');
    }
  }, [allRestaurants, currentPage, searchQuery, activeFilters, sortByDistance, itemsPerPage]);

  // Call updateDisplayedRestaurants when dependencies change
  useEffect(() => {
    if (process.env.NODE_ENV === 'development') {
      console.log('useEffect triggered - updateDisplayedRestaurants');
      console.log('allRestaurants count:', allRestaurants.length);
    }
    updateDisplayedRestaurants();
  }, [updateDisplayedRestaurants]);

  const handleSearch = (query: string) => {
    if (process.env.NODE_ENV === 'development') {
      console.log('=== handleSearch called - setting currentPage to 1 ===');
    }
    setSearchQuery(query);
    setCurrentPage(1);
  };

  const handleFilterChange = (key: string, value: any) => {
    if (process.env.NODE_ENV === 'development') {
      console.log('=== handleFilterChange called - setting currentPage to 1 ===');
    }
    
    // Handle different filter types
    if (key === 'agency' || key === 'dietary' || key === 'category') {
      setActiveFilters(prev => ({
        ...prev,
        [key]: value === 'all' ? undefined : value
      }));
    }
    
    setCurrentPage(1);
  };

  const handleToggleFilter = (key: string, value: boolean) => {
    if (process.env.NODE_ENV === 'development') {
      console.log('=== handleToggleFilter called - setting currentPage to 1 ===');
    }
    
    // Handle different filter types
    if (key === 'openNow' || key === 'nearMe') {
      setActiveFilters(prev => ({
        ...prev,
        [key]: value
      }));
    }
    
    setCurrentPage(1);
  };

  const handleDistanceChange = (distance: number) => {
    if (process.env.NODE_ENV === 'development') {
      console.log('=== handleDistanceChange called with distance:', distance);
    }
    setActiveFilters(prev => ({
      ...prev,
      distanceRadius: distance
    }));
    setCurrentPage(1);
  };

  const handleClearAll = () => {
    if (process.env.NODE_ENV === 'development') {
      console.log('=== handleClearAll called - setting currentPage to 1 ===');
    }
    setSearchQuery('');
    setActiveFilters({});
    setCurrentPage(1);
  };

  const handlePageChange = (page: number) => {
    if (process.env.NODE_ENV === 'development') {
      console.log('=== handlePageChange called ===');
      console.log('Current page before change:', currentPage);
      console.log('New page requested:', page);
      console.log('Total pages:', totalPages);
      console.log('Total filtered restaurants:', totalFilteredRestaurants);
      console.log('Items per page:', itemsPerPage);
    }
    
    if (page < 1 || page > totalPages) {
      if (process.env.NODE_ENV === 'development') {
        console.log('Invalid page number, ignoring');
      }
      return;
    }
    
    setCurrentPage(page);
    // Scroll to top when page changes
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    if (process.env.NODE_ENV === 'development') {
      console.log('=== handlePageChange completed ===');
    }
  };

  const getFilteredCount = () => {
    let filteredRestaurants = allRestaurants;

    // Apply search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filteredRestaurants = allRestaurants.filter(restaurant => {
        const searchableFields = [
          restaurant.name,
          restaurant.short_description,
          restaurant.address,
          restaurant.city,
          restaurant.state,
          restaurant.certifying_agency,
          restaurant.kosher_category,
          restaurant.listing_type,
          restaurant.phone_number,
          restaurant.avg_price
        ].filter(Boolean).map(field => field?.toLowerCase());

        return searchableFields.some(field => field?.includes(query));
      });
      
      if (process.env.NODE_ENV === 'development') {
        console.log('Filtered restaurants count:', filteredRestaurants.length);
      }
    }

    // Apply active filters
    if (activeFilters.agency && activeFilters.agency !== 'all') {
      filteredRestaurants = filteredRestaurants.filter(restaurant => {
        if (activeFilters.agency === 'Diamond K') {
          return restaurant.certifying_agency === 'Diamond K';
        } else {
          return restaurant.certifying_agency?.toUpperCase() === activeFilters.agency?.toUpperCase();
        }
      });
    }

    if (activeFilters.dietary) {
      filteredRestaurants = filteredRestaurants.filter(restaurant => {
        const kosherCategory = restaurant.kosher_category?.toLowerCase() || '';
        
        if (activeFilters.dietary === 'meat') {
          return kosherCategory === 'meat';
        } else if (activeFilters.dietary === 'dairy') {
          return kosherCategory === 'dairy';
        } else if (activeFilters.dietary === 'pareve') {
          return kosherCategory === 'pareve';
        }
        return false;
      });
    }

    // Apply "Open Now" filter
    if (activeFilters.openNow) {
      filteredRestaurants = filteredRestaurants.filter(restaurant => {
        const hoursStatus = getHoursStatus(restaurant.hours_open || restaurant.hours_of_operation);
        return hoursStatus.isOpenNow;
      });
    }

    // Apply "Near Me" filter (within 5 miles)
    if (activeFilters.nearMe && userLocation) {
      filteredRestaurants = filteredRestaurants.filter(restaurant => {
        if (!restaurant.latitude || !restaurant.longitude) return false;
        
        const distance = calculateDistance(
          userLocation.latitude,
          userLocation.longitude,
          restaurant.latitude,
          restaurant.longitude
        );
        
        return distance <= 5; // Within 5 miles
      });
    }

    // Apply category filter
    if (activeFilters.category) {
      filteredRestaurants = filteredRestaurants.filter(restaurant => {
        const category = restaurant.listing_type?.toLowerCase() || '';
        return category === activeFilters.category?.toLowerCase();
      });
    }

    return filteredRestaurants.length;
  };

  const totalFilteredRestaurants = getFilteredCount();
  const totalPages = Math.ceil(totalFilteredRestaurants / itemsPerPage);
  
  if (process.env.NODE_ENV === 'development') {
    console.log('Total pages calculation:', {
      totalFilteredRestaurants,
      itemsPerPage,
      totalPages,
      currentPage
    });
  }
  
  // Debug logging
  console.log('Render state:', {
    loading,
    showSplash,
    allRestaurantsCount: allRestaurants.length,
    displayedRestaurantsCount: displayedRestaurants.length,
    totalFilteredRestaurants,
    totalPages,
    apiError
  });

  // Generate filter description
  const getFilterDescription = () => {
    const filters = [];
    if (activeFilters.agency && activeFilters.agency !== 'all') {
      filters.push(activeFilters.agency);
    }
    if (activeFilters.dietary) {
      filters.push(activeFilters.dietary);
    }
    if (searchQuery.trim()) {
      filters.push(`"${searchQuery}"`);
    }
    return filters.join(' + ');
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Splash Screen */}
      {showSplash && (
        <SplashScreen 
          onComplete={() => setShowSplash(false)}
          duration={1000}
        />
      )}
      
      {/* Header */}
      <Header />
      
      {/* Main Content with proper spacing */}
      <div className="pt-6">
        {/* Search Bar */}
        <div className="px-4 mb-4">
          <SearchBar onSearch={handleSearch} />
        </div>
        
        {/* Navigation Tabs */}
        <NavTabs 
          activeTab={activeTab} 
          onTabChange={handleTabChange} 
        />
      
      {/* Tab Content */}
      {activeTab === 'eatery' && (
        <>
          

                  {/* Action Buttons */}
          <ActionButtons 
            onShowFilters={() => {}} // This will be handled internally by the component
            onShowMap={() => window.location.href = '/live-map'}
            onAddEatery={() => window.location.href = '/add-eatery'}
            activeFilters={activeFilters}
            onFilterChange={handleFilterChange}
            onToggleFilter={handleToggleFilter}
            onDistanceChange={handleDistanceChange}
            onClearAll={handleClearAll}
            userLocation={userLocation ? { lat: userLocation.latitude, lng: userLocation.longitude } : null}
            locationLoading={locationLoading}
            hasActiveFilters={Object.values(activeFilters || {}).some(filter => filter !== undefined && filter !== false)}
          />



          {/* Results Summary */}
          {!loading && (
            <div className="px-4 mb-4">
              <div className="text-sm text-gray-600">
                {getFilterDescription() ? (
                  <span>
                    Found {totalFilteredRestaurants} restaurant{totalFilteredRestaurants !== 1 ? 's' : ''} matching {getFilterDescription()}
                    {totalFilteredRestaurants > 0 && totalPages > 1 && (
                      <span className="text-gray-400 ml-2">
                        (Page {currentPage} of {totalPages})
                      </span>
                    )}
                  </span>
                ) : (
                  <span>
                    Showing {displayedRestaurants.length} of {allRestaurants.length} restaurants
                    {totalPages > 1 && (
                      <span className="text-gray-400 ml-2">
                        (Page {currentPage} of {totalPages})
                      </span>
                    )}
                  </span>
                )}
                {searchQuery.trim() && (
                  <div className="mt-1 text-xs text-jewgo-primary">
                    🔍 Search active: "{searchQuery}"
                  </div>
                )}
              </div>
            </div>
          )}
          
          {/* Restaurant Grid */}
          <div className="px-4 pb-8">
            {loading ? (
              <div className="flex justify-center items-center py-12">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-jewgo-primary"></div>
              </div>
            ) : apiError ? (
              <div className="flex flex-col items-center py-12">
                <div className="text-red-500 text-center mb-4">
                  <h3 className="text-lg font-semibold mb-2">Error Loading Data</h3>
                  <p className="text-sm">{apiError}</p>
                </div>
                <button 
                  onClick={() => {
                    setApiError(null);
                    fetchAllRestaurants();
                  }}
                  className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                >
                  Retry
                </button>
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

      {/* Other Tab Content */}
      {activeTab === 'specials' && (
        <div className="px-4 pb-32">
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <div className="text-gray-500 mb-4">
              <svg className="h-16 w-16 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Specials Coming Soon</h3>
            <p className="text-gray-600">
              Restaurant specials and deals will be available here soon.
            </p>
          </div>
        </div>
      )}

      {activeTab === 'mikvahs' && (
        <div className="px-4 pb-32">
          <div className="flex flex-col items-center justify-center py-12 text-center">
                            <div className="text-gray-500 mb-4">
                  <svg className="h-16 w-16 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    {/* Simple 3-tier ladder going into water */}
                    {/* Water surface */}
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M4 18h16" />
                    {/* Water waves */}
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M6 19h2" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M10 19h2" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M14 19h2" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M18 19h2" />
                    
                    {/* Ladder sides */}
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 6v12" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 6v12" />
                    
                    {/* 3 ladder rungs */}
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 8h8" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h8" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 16h8" />
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
        <div className="px-4 pb-32">
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
        <div className="px-4 pb-32">
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