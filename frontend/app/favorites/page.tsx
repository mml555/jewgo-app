'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import BottomNavigation from '@/components/BottomNavigation';
import NavTabs from '@/components/NavTabs';
import SearchBar from '@/components/SearchBar';
import { getFavorites, removeFromFavorites, FavoriteRestaurant } from '@/utils/favorites';
import { formatDistance } from '@/utils/distance';

export default function FavoritesPage() {
  const router = useRouter();
  const [favorites, setFavorites] = useState<FavoriteRestaurant[]>([]);
  const [filteredFavorites, setFilteredFavorites] = useState<FavoriteRestaurant[]>([]);
  const [userLocation, setUserLocation] = useState<{ latitude: number; longitude: number } | null>(null);
  const [activeFilters, setActiveFilters] = useState<{
    agency?: string;
    dietary?: string;
    openNow?: boolean;
    category?: string;
    nearMe?: boolean;
    distanceRadius?: number;
  }>({});
  const [activeTab, setActiveTab] = useState('eatery');
  const [searchQuery, setSearchQuery] = useState('');

  // Load favorites on component mount
  useEffect(() => {
    setFavorites(getFavorites());
    
    // Don't request location automatically - wait for user interaction
    // if (navigator.geolocation) {
    //   navigator.geolocation.getCurrentPosition(
    //     (position) => {
    //       setUserLocation({
    //         latitude: position.coords.latitude,
    //         longitude: position.coords.longitude
    //       });
    //     },
    //     (error) => {
    //       console.log('Location not available:', error);
    //     }
    //   );
    // }
  }, []);

  // Apply filters when favorites or filters change
  useEffect(() => {
    let filtered = [...favorites];

    // Apply search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(favorite => 
        favorite.name.toLowerCase().includes(query) ||
        favorite.address?.toLowerCase().includes(query) ||
        favorite.short_description?.toLowerCase().includes(query) ||
        favorite.certifying_agency?.toLowerCase().includes(query) ||
        favorite.kosher_category?.toLowerCase().includes(query)
      );
    }

    // Apply agency filter
    if (activeFilters.agency && activeFilters.agency !== 'all') {
      filtered = filtered.filter(favorite => 
        favorite.certifying_agency?.toLowerCase() === activeFilters.agency?.toLowerCase()
      );
    }

    // Apply dietary filter
    if (activeFilters.dietary && activeFilters.dietary !== 'all') {
      filtered = filtered.filter(favorite => 
        favorite.kosher_category?.toLowerCase() === activeFilters.dietary?.toLowerCase()
      );
    }

    // Apply category filter
    if (activeFilters.category && activeFilters.category !== 'all') {
      filtered = filtered.filter(favorite => 
        favorite.listing_type?.toLowerCase() === activeFilters.category?.toLowerCase()
      );
    }

    setFilteredFavorites(filtered);
  }, [favorites, activeFilters, searchQuery]);

  const removeFavorite = (id: number) => {
    const success = removeFromFavorites(id);
    if (success) {
      setFavorites(getFavorites()); // Refresh the list
    }
  };

  const handleFilterChange = (key: string, value: any) => {
    setActiveFilters(prev => ({
      ...prev,
      [key]: value === 'all' ? undefined : value
    }));
  };

  const handleToggleFilter = (key: string, value: boolean) => {
    setActiveFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleDistanceChange = (distance: number) => {
    setActiveFilters(prev => ({
      ...prev,
      distanceRadius: distance
    }));
  };

  const handleClearAll = () => {
    setActiveFilters({});
  };

  const handleTabChange = (tab: string) => {
    setActiveTab(tab);
  };

  const handleSearch = useCallback((query: string) => {
    setSearchQuery(query);
  }, []);

  // ✅ Phase 1: Implement handler function
  const handleExploreRestaurants = () => {
    router.push('/');
  };

  const handleViewDetails = (restaurant: FavoriteRestaurant) => {
    router.push(`/restaurant/${restaurant.id}`);
  };

  const handleGetDirections = (restaurant: FavoriteRestaurant) => {
    if (restaurant.latitude && restaurant.longitude) {
      router.push(`/live-map?lat=${restaurant.latitude}&lng=${restaurant.longitude}&name=${encodeURIComponent(restaurant.name)}`);
    } else {
      // Fallback to Google Maps search
      const searchQuery = encodeURIComponent(`${restaurant.name} ${restaurant.address || ''}`);
      window.open(`https://www.google.com/maps/search/${searchQuery}`, '_blank');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <Header />

      {/* Search Bar */}
      <div className="px-4 py-4">
        <SearchBar onSearch={handleSearch} />
      </div>

      {/* Navigation Tabs */}
      <NavTabs activeTab={activeTab} onTabChange={handleTabChange} />
      
      {/* Content */}
      <div className="px-4 py-6 pb-24">
        <div className="max-w-4xl mx-auto">
          {/* Page Header */}
          <div className="text-center mb-8">
            <div className="text-4xl mb-4">❤️</div>
            <h1 className="text-2xl font-bold text-gray-800 mb-2">My Favorites</h1>
            <p className="text-gray-600">Your saved kosher establishments</p>
          </div>



          {/* Favorites List */}
          {filteredFavorites.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">💔</div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">No Favorites Yet</h3>
              <p className="text-gray-600 mb-6">Start exploring and save your favorite kosher establishments!</p>
              {/* ✅ Phase 1: Updated button with onClick handler */}
              <button 
                onClick={handleExploreRestaurants}
                className="bg-jewgo-primary text-white px-6 py-3 rounded-lg font-medium hover:bg-jewgo-primary-dark transition-colors"
                aria-label="Explore Restaurants"
              >
                Explore Restaurants
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredFavorites.map((favorite) => {
                // Calculate distance if user location is available
                let distanceText = '';
                if (userLocation && favorite.latitude && favorite.longitude) {
                  const distance = formatDistance(
                    Math.sqrt(
                      Math.pow(userLocation.latitude - parseFloat(favorite.latitude.toString()), 2) +
                      Math.pow(userLocation.longitude - parseFloat(favorite.longitude.toString()), 2)
                    ) * 111 // Rough conversion to km
                  );
                  distanceText = ` • ${distance}`;
                }

                return (
                  <div key={favorite.id} className="bg-white rounded-lg shadow-md p-4">
                    <div className="flex items-start space-x-4">
                      {/* Restaurant Image */}
                      <div className="w-20 h-20 bg-gray-200 rounded-lg flex-shrink-0">
                        <div className="w-full h-full bg-gradient-to-br from-gray-300 to-gray-400 rounded-lg flex items-center justify-center">
                          <span className="text-2xl">🍽️</span>
                        </div>
                      </div>

                      {/* Restaurant Info */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h3 className="font-semibold text-gray-800 text-lg mb-1">{favorite.name}</h3>
                            <p className="text-gray-600 text-sm mb-2">
                              {favorite.address}
                              {distanceText && <span className="text-gray-500">{distanceText}</span>}
                            </p>
                            
                            {/* Description */}
                            {favorite.short_description && (
                              <p className="text-gray-600 text-sm mb-2 line-clamp-2">
                                {favorite.short_description}
                              </p>
                            )}

                            {/* Certifying Agency and Kosher Category */}
                            <div className="flex items-center space-x-2 mb-2">
                              {favorite.certifying_agency && (
                                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-jewgo-primary/10 text-jewgo-primary">
                                  {favorite.certifying_agency}
                                </span>
                              )}
                              {favorite.kosher_category && (
                                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700">
                                  {favorite.kosher_category}
                                </span>
                              )}
                            </div>

                            {/* Added Date */}
                            <p className="text-xs text-gray-500">
                              Added {new Date(favorite.addedAt).toLocaleDateString()}
                            </p>
                          </div>

                          {/* Remove Button */}
                          <button
                            onClick={() => removeFavorite(favorite.id)}
                            className="text-pink-500 hover:text-pink-700 transition-colors p-2"
                            title="Remove from favorites"
                          >
                            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                              <path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                            </svg>
                          </button>
                        </div>

                        {/* Action Buttons */}
                        <div className="flex space-x-3 mt-4">
                          <button 
                            onClick={() => handleViewDetails(favorite)}
                            className="flex-1 bg-jewgo-primary text-white py-2 px-4 rounded-lg text-sm font-medium hover:bg-jewgo-primary-dark transition-colors"
                          >
                            View Details
                          </button>
                          <button 
                            onClick={() => handleGetDirections(favorite)}
                            className="flex-1 bg-gray-100 text-gray-700 py-2 px-4 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors"
                          >
                            Get Directions
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {/* Stats */}
          {favorites.length > 0 && (
            <div className="mt-8 bg-white rounded-lg shadow-md p-4">
              <h3 className="font-semibold text-gray-800 mb-3">Favorites Summary</h3>
              <div className="grid grid-cols-3 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-jewgo-primary">{favorites.length}</div>
                  <div className="text-sm text-gray-600">Total Favorites</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-jewgo-primary">
                    {favorites.filter(f => f.certifying_agency === 'ORB').length}
                  </div>
                  <div className="text-sm text-gray-600">ORB Certified</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-jewgo-primary">
                    {favorites.filter(f => f.kosher_category === 'meat').length}
                  </div>
                  <div className="text-sm text-gray-600">Meat Restaurants</div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Bottom Navigation */}
      <BottomNavigation />
    </div>
  );
} 