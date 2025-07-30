'use client';

import { useState, useEffect, useCallback } from 'react';
import { useSearchParams } from 'next/navigation';
import Header from '@/components/Header';
import SearchBar from '@/components/SearchBar';
import ActionButtons from '@/components/ActionButtons';
import InteractiveRestaurantMap from '@/components/InteractiveRestaurantMap';
import BottomNavigation from '@/components/BottomNavigation';
import NavTabs from '@/components/NavTabs';
import { Restaurant } from '@/types/restaurant';

export default function LiveMapClient() {
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
  const [activeTab, setActiveTab] = useState('eatery');

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

  // Fetch restaurants on component mount
  useEffect(() => {
    fetchRestaurants();
  }, []);

  // Request location automatically when live map loads
  useEffect(() => {
    getUserLocation();
  }, []);

  useEffect(() => {
    // Fetch restaurants when user location changes
    if (userLocation) {
      fetchRestaurants();
    }
  }, [userLocation]);

  useEffect(() => {
    console.log('Live map useEffect triggered - updateDisplayedRestaurants');
    console.log('Live map allRestaurants count:', allRestaurants.length);
    console.log('searchQuery:', searchQuery);
    console.log('activeFilters:', activeFilters);
    console.log('userLocation:', userLocation);

    let filtered = [...allRestaurants];

    // Apply search query filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase().trim();
      filtered = filtered.filter(restaurant => 
        restaurant.name.toLowerCase().includes(query) ||
        restaurant.address.toLowerCase().includes(query) ||
        restaurant.city.toLowerCase().includes(query) ||
        restaurant.state.toLowerCase().includes(query) ||
        (restaurant.cuisine_type && restaurant.cuisine_type.toLowerCase().includes(query)) ||
        (restaurant.hechsher_details && restaurant.hechsher_details.toLowerCase().includes(query))
      );
    }

    // Apply agency filter
    if (activeFilters.agency) {
      filtered = filtered.filter(restaurant => 
        restaurant.hechsher_details && 
        restaurant.hechsher_details.toLowerCase().includes(activeFilters.agency!.toLowerCase())
      );
    }

    // Apply dietary filter
    if (activeFilters.dietary) {
      filtered = filtered.filter(restaurant => {
        const hechsher = restaurant.hechsher_details?.toLowerCase() || '';
        switch (activeFilters.dietary) {
          case 'meat':
            return hechsher.includes('meat') || hechsher.includes('fleishig');
          case 'dairy':
            return hechsher.includes('dairy') || hechsher.includes('milchig');
          case 'pareve':
            return hechsher.includes('pareve') || hechsher.includes('parve');
          default:
            return true;
        }
      });
    }

    // Apply category filter
    if (activeFilters.category) {
      filtered = filtered.filter(restaurant => 
        restaurant.cuisine_type && 
        restaurant.cuisine_type.toLowerCase().includes(activeFilters.category!.toLowerCase())
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

    // Apply "open now" filter
    if (activeFilters.openNow) {
      const now = new Date();
      const currentDay = now.toLocaleDateString('en-US', { weekday: 'lowercase' });
      const currentTime = now.getHours() * 60 + now.getMinutes(); // Convert to minutes

      filtered = filtered.filter(restaurant => {
        if (!restaurant.hours_of_operation) return false;
        
        try {
          const hours = typeof restaurant.hours_of_operation === 'string' 
            ? JSON.parse(restaurant.hours_of_operation) 
            : restaurant.hours_of_operation;
          
          if (!Array.isArray(hours)) return false;
          
          const todayHours = hours.find(h => h.day === currentDay);
          if (!todayHours) return false;
          
          const openTime = timeToMinutes(todayHours.open);
          const closeTime = timeToMinutes(todayHours.close);
          
          if (openTime === -1 || closeTime === -1) return false;
          
          // Handle cases where restaurant is open past midnight
          if (closeTime < openTime) {
            return currentTime >= openTime || currentTime <= closeTime;
          } else {
            return currentTime >= openTime && currentTime <= closeTime;
          }
        } catch (error) {
          console.error('Error parsing hours for restaurant:', restaurant.name, error);
          return false;
        }
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

    console.log('Filtered restaurants count:', filtered.length);
    setDisplayedRestaurants(filtered);
  }, [allRestaurants, searchQuery, activeFilters, userLocation]);

  // Helper function to convert time string to minutes
  const timeToMinutes = (timeStr: string): number => {
    const time = timeStr.toLowerCase().trim();
    const match = time.match(/(\d+):?(\d*)\s*(am|pm)/);
    
    if (!match) return -1;
    
    let hours = parseInt(match[1]);
    const minutes = match[2] ? parseInt(match[2]) : 0;
    const period = match[3];
    
    if (period === 'pm' && hours !== 12) hours += 12;
    if (period === 'am' && hours === 12) hours = 0;
    
    return hours * 60 + minutes;
  };

  const fetchRestaurants = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://jewgo.onrender.com';
      const apiUrl = `${backendUrl}/api/restaurants`;
      
      if (userLocation) {
        // If there's a search query, fetch all restaurants to ensure we can find the specific restaurant
        // Otherwise, fetch restaurants within 50 miles of user location
        const url = searchQuery.trim() 
          ? `${apiUrl}?limit=1000`
          : `${apiUrl}?limit=200&lat=${userLocation.latitude}&lng=${userLocation.longitude}&radius=50`;
        
        console.log('Live map fetching from:', url);
        const response = await fetch(url);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.restaurants && Array.isArray(data.restaurants)) {
          setAllRestaurants(data.restaurants);
        } else {
          throw new Error('Invalid response format');
        }
      } else {
        // If no user location, fetch all restaurants
        const response = await fetch(`${apiUrl}?limit=1000`);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.restaurants && Array.isArray(data.restaurants)) {
          setAllRestaurants(data.restaurants);
        } else {
          throw new Error('Invalid response format');
        }
      }
    } catch (err) {
      console.error('Error fetching restaurants:', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch restaurants');
    } finally {
      setLoading(false);
    }
  }, [userLocation, searchQuery]);

  const getUserLocation = () => {
    if (!navigator.geolocation) {
      setLocationError('Geolocation is not supported by this browser.');
      return;
    }

    setLocationLoading(true);
    setLocationError(null);

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setUserLocation({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          accuracy: position.coords.accuracy
        });
        setLocationLoading(false);
      },
      (error) => {
        setLocationError(getLocationErrorMessage(error.code));
        setLocationLoading(false);
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 300000 // 5 minutes
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
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
  };

  const updateDisplayedRestaurants = () => {
    console.log('updateDisplayedRestaurants called');
    console.log('allRestaurants count:', allRestaurants.length);
    console.log('searchQuery:', searchQuery);
    console.log('activeFilters:', activeFilters);
    console.log('userLocation:', userLocation);

    let filtered = [...allRestaurants];

    // Apply search query filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase().trim();
      filtered = filtered.filter(restaurant => 
        restaurant.name.toLowerCase().includes(query) ||
        restaurant.address.toLowerCase().includes(query) ||
        restaurant.city.toLowerCase().includes(query) ||
        restaurant.state.toLowerCase().includes(query) ||
        (restaurant.cuisine_type && restaurant.cuisine_type.toLowerCase().includes(query)) ||
        (restaurant.hechsher_details && restaurant.hechsher_details.toLowerCase().includes(query))
      );
    }

    // Apply agency filter
    if (activeFilters.agency) {
      filtered = filtered.filter(restaurant => 
        restaurant.hechsher_details && 
        restaurant.hechsher_details.toLowerCase().includes(activeFilters.agency!.toLowerCase())
      );
    }

    // Apply dietary filter
    if (activeFilters.dietary) {
      filtered = filtered.filter(restaurant => {
        const hechsher = restaurant.hechsher_details?.toLowerCase() || '';
        switch (activeFilters.dietary) {
          case 'meat':
            return hechsher.includes('meat') || hechsher.includes('fleishig');
          case 'dairy':
            return hechsher.includes('dairy') || hechsher.includes('milchig');
          case 'pareve':
            return hechsher.includes('pareve') || hechsher.includes('parve');
          default:
            return true;
        }
      });
    }

    // Apply category filter
    if (activeFilters.category) {
      filtered = filtered.filter(restaurant => 
        restaurant.cuisine_type && 
        restaurant.cuisine_type.toLowerCase().includes(activeFilters.category!.toLowerCase())
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

    // Apply "open now" filter
    if (activeFilters.openNow) {
      const now = new Date();
      const currentDay = now.toLocaleDateString('en-US', { weekday: 'lowercase' });
      const currentTime = now.getHours() * 60 + now.getMinutes(); // Convert to minutes

      filtered = filtered.filter(restaurant => {
        if (!restaurant.hours_of_operation) return false;
        
        try {
          const hours = typeof restaurant.hours_of_operation === 'string' 
            ? JSON.parse(restaurant.hours_of_operation) 
            : restaurant.hours_of_operation;
          
          if (!Array.isArray(hours)) return false;
          
          const todayHours = hours.find(h => h.day === currentDay);
          if (!todayHours) return false;
          
          const openTime = timeToMinutes(todayHours.open);
          const closeTime = timeToMinutes(todayHours.close);
          
          if (openTime === -1 || closeTime === -1) return false;
          
          // Handle cases where restaurant is open past midnight
          if (closeTime < openTime) {
            return currentTime >= openTime || currentTime <= closeTime;
          } else {
            return currentTime >= openTime && currentTime <= closeTime;
          }
        } catch (error) {
          console.error('Error parsing hours for restaurant:', restaurant.name, error);
          return false;
        }
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

    console.log('Filtered restaurants count:', filtered.length);
    setDisplayedRestaurants(filtered);
  };

  // Helper function to convert time string to minutes
  const timeToMinutes = (timeStr: string): number => {
    const time = timeStr.toLowerCase().trim();
    const match = time.match(/(\d+):?(\d*)\s*(am|pm)/);
    
    if (!match) return -1;
    
    let hours = parseInt(match[1]);
    const minutes = match[2] ? parseInt(match[2]) : 0;
    const period = match[3];
    
    if (period === 'pm' && hours !== 12) hours += 12;
    if (period === 'am' && hours === 12) hours = 0;
    
    return hours * 60 + minutes;
  };

  const handleRestaurantSearch = (query: string) => {
    setSearchQuery(query);
  };

  const handleFilterChange = (key: string, value: any) => {
    setActiveFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleToggleFilter = (key: string, value: boolean) => {
    setActiveFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleDistanceChange = (distance: number) => {
    setActiveFilters(prev => ({ ...prev, distanceRadius: distance }));
  };

  const handleClearAll = () => {
    setSearchQuery('');
    setActiveFilters({});
  };

  const handleRestaurantSelect = (restaurantId: number) => {
    const restaurant = allRestaurants.find(r => r.id === restaurantId);
    setSelectedRestaurant(restaurant || null);
  };

  const getFilteredCount = () => {
    return displayedRestaurants.length;
  };

  const hasActiveFilters = () => {
    return searchQuery.trim() || 
           Object.values(activeFilters).some(value => 
             value !== undefined && value !== false && value !== ''
           );
  };

  const handleTabChange = (tab: string) => {
    setActiveTab(tab);
  };

  const getFilterDescription = () => {
    const filters = [];
    if (searchQuery.trim()) filters.push(`"${searchQuery}"`);
    if (activeFilters.agency) filters.push(`${activeFilters.agency} certified`);
    if (activeFilters.dietary) filters.push(`${activeFilters.dietary} only`);
    if (activeFilters.category) filters.push(`${activeFilters.category} cuisine`);
    if (activeFilters.nearMe) filters.push(`within ${activeFilters.distanceRadius || 10} miles`);
    if (activeFilters.openNow) filters.push('open now');
    
    return filters.length > 0 ? filters.join(', ') : 'All restaurants';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-500">Loading restaurants...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-red-500">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header title="Live Map" showBackButton />
      
      <div className="px-4 py-2 bg-white border-b border-gray-100">
        <SearchBar 
          onSearch={handleRestaurantSearch}
          placeholder="Search restaurants..."
          value={searchQuery}
        />
      </div>

      <div className="px-4 py-2 bg-white border-b border-gray-100">
        <ActionButtons />
      </div>

      <div className="px-4 py-2 bg-white border-b border-gray-100">
        <NavTabs activeTab={activeTab} onTabChange={handleTabChange} />
      </div>

      {/* Location Status */}
      {locationLoading && (
        <div className="px-4 py-2 bg-blue-50 text-blue-700 text-sm">
          Getting your location...
        </div>
      )}
      
      {locationError && (
        <div className="px-4 py-2 bg-yellow-50 text-yellow-700 text-sm">
          {locationError}
          <button 
            onClick={getUserLocation}
            className="ml-2 underline hover:no-underline"
          >
            Try again
          </button>
        </div>
      )}

      {/* Filter Summary */}
      {hasActiveFilters() && (
        <div className="px-4 py-2 bg-gray-50 text-sm text-gray-600 border-b border-gray-200">
          {getFilterDescription()} • {getFilteredCount()} restaurants
          <button 
            onClick={handleClearAll}
            className="ml-2 text-blue-600 hover:text-blue-800 underline"
          >
            Clear all
          </button>
        </div>
      )}

      {/* Map Component */}
      <div className="flex-1 relative">
        <InteractiveRestaurantMap
          restaurants={displayedRestaurants}
          userLocation={userLocation}
          selectedRestaurant={selectedRestaurant}
          onRestaurantSelect={handleRestaurantSelect}
          mapCenter={mapCenter}
          loading={loading}
        />
      </div>

      <BottomNavigation activeTab={activeTab} />
    </div>
  );
} 