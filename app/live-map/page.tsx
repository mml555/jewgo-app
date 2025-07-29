'use client';

import { useState, useEffect, useCallback } from 'react';
import { useSearchParams } from 'next/navigation';
import Header from '@/components/Header';
import SearchBar from '@/components/SearchBar';
import ActionButtons from '@/components/ActionButtons';
import InteractiveRestaurantMap from '@/components/InteractiveRestaurantMap';
import BottomNavigation from '@/components/BottomNavigation';
import { Restaurant } from '@/types/restaurant';

export default function LiveMapPage() {
  const searchParams = useSearchParams();
  const [allRestaurants, setAllRestaurants] = useState<Restaurant[]>([]);
  const [displayedRestaurants, setDisplayedRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRestaurant, setSelectedRestaurant] = useState<Restaurant | null>(null);
  const [userLocation, setUserLocation] = useState<{latitude: number, longitude: number, accuracy?: number} | null>(null);
  const [locationLoading, setLocationLoading] = useState(false);
  const [locationError, setLocationError] = useState<string | null>(null);
  const [activeFilters, setActiveFilters] = useState<{
    agency?: string;
    dietary?: string;
    openNow?: boolean;
    category?: string;
    nearMe?: boolean;
    distanceRadius?: number;
  }>({});
  const [mapCenter, setMapCenter] = useState<{lat: number, lng: number} | null>(null);

  // Handle URL parameters for centering map on specific location
  useEffect(() => {
    const lat = searchParams.get('lat');
    const lng = searchParams.get('lng');
    const name = searchParams.get('name');
    
    if (lat && lng) {
      const latitude = parseFloat(lat);
      const longitude = parseFloat(lng);
      
      // Validate coordinates are numbers and within valid ranges
      if (!isNaN(latitude) && !isNaN(longitude) && 
          latitude >= -90 && latitude <= 90 && 
          longitude >= -180 && longitude <= 180) {
        setMapCenter({ lat: latitude, lng: longitude });
        if (name) {
          const decodedName = decodeURIComponent(name);
          setSearchQuery(decodedName);
        }
      } else {
        console.warn('Invalid coordinates in URL parameters:', { lat, lng, latitude, longitude });
        // Don't set map center if coordinates are invalid
      }
    }
  }, [searchParams]);

  useEffect(() => {
    getUserLocation();
  }, []);

  useEffect(() => {
    if (userLocation) {
      fetchRestaurants();
    }
  }, [userLocation]);

  useEffect(() => {
    console.log('Live map useEffect triggered - updateDisplayedRestaurants');
    console.log('Live map allRestaurants count:', allRestaurants.length);
    updateDisplayedRestaurants();
  }, [allRestaurants, searchQuery, activeFilters, userLocation]);

  const fetchRestaurants = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const apiUrl = process.env.NODE_ENV === 'production' 
        ? 'http://localhost:8081/api/restaurants'
        : 'http://127.0.0.1:8081/api/restaurants';
      
      if (userLocation) {
        // If there's a search query, fetch all restaurants to ensure we can find the specific restaurant
        // Otherwise, fetch restaurants within 50 miles of user location
        const url = searchQuery.trim() 
          ? `${apiUrl}?limit=1000`
          : `${apiUrl}?limit=200&lat=${userLocation.latitude}&lng=${userLocation.longitude}&radius=50`;
        
        console.log('Live map fetching from:', url);
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error('Failed to fetch restaurants');
        }
        const data = await response.json();
        
        if (data.success && data.restaurants) {
          console.log('Live map API returned restaurants:', data.restaurants.length);
          console.log('Live map setting allRestaurants:', data.restaurants.length);
          setAllRestaurants(data.restaurants);
        } else {
          throw new Error(data.error || 'Failed to fetch restaurants');
        }
      } else {
        const response = await fetch(`${apiUrl}?limit=1000`);
        if (!response.ok) {
          throw new Error('Failed to fetch restaurants');
        }
        const data = await response.json();
        
        if (data.success && data.restaurants) {
          console.log('Live map API returned restaurants:', data.restaurants.length);
          console.log('Live map setting allRestaurants:', data.restaurants.length);
          setAllRestaurants(data.restaurants);
        } else {
          throw new Error(data.error || 'Failed to fetch restaurants');
        }
      }
    } catch (error) {
      console.error('Error fetching restaurants:', error);
    } finally {
      setLoading(false);
    }
  }, [userLocation, searchQuery]);

  const getUserLocation = () => {
    if (!navigator.geolocation) {
      setLocationError('Geolocation is not supported by this browser');
      return;
    }

    setLocationLoading(true);
    setLocationError(null);

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const location = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          accuracy: position.coords.accuracy,
        };
        setUserLocation(location);
        setLocationLoading(false);
      },
      (error) => {
        const errorMessage = getLocationErrorMessage(error.code);
        setLocationError(errorMessage);
        setLocationLoading(false);
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 300000,
      }
    );
  };

  const getLocationErrorMessage = (code: number): string => {
    switch (code) {
      case 1:
        return 'Location access denied. Please enable location services.';
      case 2:
        return 'Location unavailable. Please try again.';
      case 3:
        return 'Location request timed out. Please try again.';
      default:
        return 'Unable to get your location. Please try again.';
    }
  };

  const calculateDistance = (lat1: number, lon1: number, lat2: number, lon2: number): number => {
    const R = 3959; // Earth's radius in miles
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
      Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  };

  const updateDisplayedRestaurants = () => {
    console.log('Live map updateDisplayedRestaurants called with:', {
      allRestaurantsCount: allRestaurants.length,
      searchQuery,
      activeFilters
    });
    
    let filteredRestaurants = [...allRestaurants];

    // Apply search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      console.log('Live map search query:', query);
      console.log('Live map first few restaurant names:', allRestaurants.slice(0, 3).map(r => r.name));
      
      filteredRestaurants = filteredRestaurants.filter(restaurant => {
        const searchableFields = [
          restaurant.name,
          restaurant.address,
          restaurant.city,
          restaurant.state,
          restaurant.certifying_agency,
          restaurant.kosher_category,
          restaurant.listing_type,
          restaurant.phone_number,
          restaurant.avg_price
        ].filter(Boolean).map(field => field?.toLowerCase());

        const matches = searchableFields.some(field => field?.includes(query));
        if (restaurant.name.toLowerCase().includes('17') || restaurant.name.toLowerCase().includes('restaurant')) {
          console.log('Live map checking restaurant:', restaurant.name, 'matches:', matches);
        }
        return matches;
      });
    }

    // Apply agency filter
    if (activeFilters.agency && activeFilters.agency !== 'all') {
      filteredRestaurants = filteredRestaurants.filter(restaurant => {
        if (activeFilters.agency === 'Diamond K') {
          return restaurant.certifying_agency === 'Diamond K';
        } else {
          return restaurant.certifying_agency?.toUpperCase() === activeFilters.agency?.toUpperCase();
        }
      });
    }

    // Apply dietary filter
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

    // Apply category filter
    if (activeFilters.category && activeFilters.category !== 'all') {
      filteredRestaurants = filteredRestaurants.filter(restaurant => {
        const listingType = restaurant.listing_type?.toLowerCase() || '';
        return listingType === activeFilters.category?.toLowerCase();
      });
    }

    // Apply distance radius filter
    if (activeFilters.distanceRadius && userLocation) {
      filteredRestaurants = filteredRestaurants.filter(restaurant => {
        const distance = calculateDistance(
          userLocation.latitude,
          userLocation.longitude,
          parseFloat(String(restaurant.latitude) || '0'),
          parseFloat(String(restaurant.longitude) || '0')
        );
        return distance <= activeFilters.distanceRadius!;
      });
    }

    // Apply "Open Now" filter
    if (activeFilters.openNow) {
      const now = new Date();
      const currentDay = now.getDay(); // 0 = Sunday, 1 = Monday, etc.
      const currentTime = now.getHours() * 100 + now.getMinutes(); // Convert to HHMM format
      
      filteredRestaurants = filteredRestaurants.filter(restaurant => {
        // This is a simplified check - you might want to implement more sophisticated hours checking
        // For now, we'll assume restaurants are open if they have hours data
        return restaurant.hours_of_operation && restaurant.hours_of_operation.trim() !== '';
      });
    }

    // Sort by distance if user location is available
    if (userLocation) {
      filteredRestaurants.sort((a, b) => {
        const distanceA = calculateDistance(
          userLocation.latitude,
          userLocation.longitude,
          parseFloat(String(a.latitude) || '0'),
          parseFloat(String(a.longitude) || '0')
        );
        const distanceB = calculateDistance(
          userLocation.latitude,
          userLocation.longitude,
          parseFloat(String(b.latitude) || '0'),
          parseFloat(String(b.longitude) || '0')
        );
        return distanceA - distanceB;
      });
    }

    console.log('Live map setting displayedRestaurants:', filteredRestaurants.length);
    setDisplayedRestaurants(filteredRestaurants);
  };

  const handleRestaurantSearch = (query: string) => {
    setSearchQuery(query);
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
    setSearchQuery('');
  };

  const handleRestaurantSelect = (restaurantId: number) => {
    const restaurant = allRestaurants.find(r => r.id === restaurantId);
    setSelectedRestaurant(restaurant || null);
  };

  const getFilteredCount = () => {
    return displayedRestaurants.length;
  };

  const hasActiveFilters = () => {
    return !!(
      activeFilters.agency ||
      activeFilters.dietary ||
      activeFilters.category ||
      activeFilters.openNow ||
      activeFilters.distanceRadius ||
      searchQuery.trim()
    );
  };

  const getFilterDescription = () => {
    const filters = [];
    if (activeFilters.agency) {
      filters.push(activeFilters.agency);
    }
    if (activeFilters.dietary) {
      filters.push(activeFilters.dietary);
    }
    if (activeFilters.category) {
      filters.push(activeFilters.category);
    }
    if (activeFilters.openNow) {
      filters.push('Open Now');
    }
    if (activeFilters.distanceRadius) {
      filters.push(`${activeFilters.distanceRadius} miles`);
    }
    if (searchQuery.trim()) {
      filters.push(`"${searchQuery}"`);
    }
    return filters.join(' + ');
  };

  const totalFilteredRestaurants = displayedRestaurants.length;

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <Header />
      
      {/* Search Bar */}
      <div className="px-4 py-4">
        <SearchBar onSearch={handleRestaurantSearch} />
      </div>

      {/* Location Status */}
      <div className="px-4 mb-3">
        {locationLoading && (
          <div className="flex items-center space-x-2 text-sm text-blue-600 bg-blue-50 px-3 py-2 rounded-lg">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
            <span>Getting your location...</span>
          </div>
        )}
        
        {locationError && (
          <div className="flex items-center justify-between text-sm text-red-600 bg-red-50 px-3 py-2 rounded-lg">
            <span>{locationError}</span>
            <button 
              onClick={getUserLocation}
              className="text-red-800 hover:text-red-900 font-medium"
            >
              Retry
            </button>
          </div>
        )}

        {userLocation && (
          <div className="flex items-center justify-between text-sm text-green-600 bg-green-50 px-3 py-2 rounded-lg">
            <span>📍 Location found! Showing nearby restaurants</span>
          </div>
        )}
      </div>

      {/* Action Buttons with Advanced Filters */}
      <ActionButtons
        onShowFilters={() => {}} // This will be handled by the modal in ActionButtons
        onShowMap={() => {
          window.location.href = '/'; // Navigate to explore page (list view)
        }}
        onAddEatery={() => {
          window.location.href = '/add-eatery';
        }}
        activeFilters={activeFilters}
        onFilterChange={handleFilterChange}
        onToggleFilter={handleToggleFilter}
        onDistanceChange={handleDistanceChange}
        onClearAll={handleClearAll}
        userLocation={userLocation ? { lat: userLocation.latitude, lng: userLocation.longitude } : null}
        locationLoading={locationLoading}
        hasActiveFilters={hasActiveFilters()}
        isOnMapPage={true}
      />

      {/* Results Summary */}
      {!loading && (
        <div className="px-4 mb-4">
          <div className="text-sm text-gray-600">
            {getFilterDescription() ? (
              <span>
                Found {totalFilteredRestaurants} restaurant{totalFilteredRestaurants !== 1 ? 's' : ''} matching {getFilterDescription()}
              </span>
            ) : (
              <span>
                Showing {displayedRestaurants.length} of {allRestaurants.length} restaurants
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

      {/* Main Content */}
      <div className="px-4 pb-20">
        {loading ? (
          <div className="flex flex-col justify-center items-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-jewgo-primary mb-4"></div>
            <p className="text-gray-600 text-sm">Loading restaurants...</p>
            {userLocation && (
              <p className="text-gray-500 text-xs mt-2">Searching within 50 miles of your location</p>
            )}
          </div>
        ) : (
          <InteractiveRestaurantMap
            restaurants={displayedRestaurants}
            onRestaurantSelect={handleRestaurantSelect}
            selectedRestaurantId={selectedRestaurant?.id}
            userLocation={userLocation}
            mapCenter={mapCenter}
            className="h-[calc(100vh-400px)]"
          />
        )}
      </div>
      
      {/* Bottom Navigation */}
      <BottomNavigation />
    </div>
  );
} 