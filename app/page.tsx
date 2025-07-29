'use client';

import { useState, useEffect } from 'react';
import Header from '@/components/Header';
import SearchBar from '@/components/SearchBar';
import CategoryNav from '@/components/CategoryNav';
import ActionButtons from '@/components/ActionButtons';
import RestaurantGrid from '@/components/RestaurantGrid';
import BottomNavigation from '@/components/BottomNavigation';
import SplashScreen from '@/components/SplashScreen';
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
  const [userLocation, setUserLocation] = useState<{latitude: number, longitude: number} | null>(null);
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
    setCurrentPage(1);
    setSearchQuery('');
  };

  useEffect(() => {
    console.log('useEffect called - fetching restaurants');
    fetchAllRestaurants();
    // Don't request location automatically - wait for user interaction
  }, []);

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
              const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://jewgo.onrender.com';
      const response = await fetch(`${backendUrl}/api/restaurants?limit=1000`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Restaurants fetched:', data.restaurants?.length || 0);
      
      if (data.restaurants) {
        setAllRestaurants(data.restaurants);
        setDisplayedRestaurants(data.restaurants.slice(0, itemsPerPage));
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

  const handleSearch = (query: string) => {
    console.log('=== handleSearch called - setting currentPage to 1 ===');
    setSearchQuery(query);
    setCurrentPage(1);
  };

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
    setCurrentPage(page);
  };

  const getFilteredCount = () => {
    return allRestaurants.length;
  };

  const totalFilteredRestaurants = getFilteredCount();
  const totalPages = Math.ceil(totalFilteredRestaurants / itemsPerPage);

  if (showSplash) {
    return <SplashScreen />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="pb-20">
        {/* Header */}
        <Header />

        {/* Main Content */}
        {activeTab === 'eatery' && (
          <>
            {/* Search and Filters */}
            <div className="px-4 py-4 space-y-4">
              <SearchBar onSearch={handleSearch} />
              <CategoryNav 
                selectedFilters={activeFilters}
                onFilterChange={handleFilterChange}
                onToggleFilter={handleToggleFilter}
                onDistanceChange={handleDistanceChange}
                onClearAll={handleClearAll}
              />
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
            <div className="px-4">
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
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M4 18h16" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M6 19h2" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M10 19h2" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M14 19h2" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M18 19h2" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 6v12" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 6v12" />
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