'use client';

import { useState, useEffect, useRef } from 'react';
import { Restaurant } from '@/types/restaurant';
import Link from 'next/link';

interface UserLocation {
  latitude: number;
  longitude: number;
  accuracy?: number;
}

interface InteractiveRestaurantMapProps {
  restaurants: Restaurant[];
  onRestaurantSelect?: (restaurantId: number) => void;
  selectedRestaurantId?: number;
  userLocation?: UserLocation | null;
  mapCenter?: { lat: number; lng: number } | null;
  className?: string;
}



export default function InteractiveRestaurantMap({ 
  restaurants, 
  onRestaurantSelect,
  selectedRestaurantId,
  userLocation,
  mapCenter,
  className = "h-96"
}: InteractiveRestaurantMapProps) {
  const [mapLoaded, setMapLoaded] = useState(false);
  const [mapError, setMapError] = useState<string | null>(null);
  const [selectedMarker, setSelectedMarker] = useState<Restaurant | null>(null);
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<any>(null);
  const markersRef = useRef<any[]>([]);
  const userLocationMarkerRef = useRef<any>(null);
  const infoWindowRef = useRef<any>(null);
  const [apiLoaded, setApiLoaded] = useState(false);

  // Filter restaurants with valid coordinates and addresses
  const restaurantsWithCoords = restaurants.filter(restaurant => {
    // Check if restaurant has valid coordinates
    if (!restaurant.latitude || !restaurant.longitude) return false;
    
    const lat = parseFloat(restaurant.latitude.toString());
    const lng = parseFloat(restaurant.longitude.toString());
    
    if (isNaN(lat) || isNaN(lng)) return false;
    if (lat === 0 && lng === 0) return false;
    
    // Only check for valid coordinate ranges (latitude: -90 to 90, longitude: -180 to 180)
    if (lat < -90 || lat > 90 || lng < -180 || lng > 180) return false;
    
    return true;
  });

  // Debug logging
  console.log('InteractiveRestaurantMap Debug:', {
    totalRestaurants: restaurants.length,
    restaurantsWithCoords: restaurantsWithCoords.length,
    userLocation: !!userLocation,
    mapCenter: !!mapCenter
  });

  // Load Google Maps API
  useEffect(() => {
    const loadGoogleMapsAPI = () => {
      // Check if API is already loaded and fully initialized
      if (window.google && window.google.maps && window.google.maps.LatLngBounds) {
        setApiLoaded(true);
        return;
      }

      // Check if script is already loading
      if (document.querySelector('script[src*="maps.googleapis.com"]')) {
        // Wait for the existing script to load
        const checkInterval = setInterval(() => {
          if (window.google && window.google.maps && window.google.maps.LatLngBounds) {
            setApiLoaded(true);
            clearInterval(checkInterval);
          }
        }, 100);
        
        // Timeout after 10 seconds
        setTimeout(() => {
          clearInterval(checkInterval);
          if (!window.google || !window.google.maps) {
            setMapError('Google Maps API failed to load');
          }
        }, 10000);
        
        return;
      }

      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=${process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY}&libraries=places,geometry&loading=async`;
      script.async = true;
      script.defer = true;
      
      script.onload = () => {
        // Wait for the API to be fully initialized
        const checkInterval = setInterval(() => {
          if (window.google && window.google.maps && window.google.maps.LatLngBounds) {
            setApiLoaded(true);
            clearInterval(checkInterval);
          }
        }, 100);
        
        // Timeout after 10 seconds
        setTimeout(() => {
          clearInterval(checkInterval);
          if (!window.google || !window.google.maps) {
            setMapError('Google Maps API failed to initialize');
          }
        }, 10000);
      };
      
      script.onerror = () => {
        setMapError('Failed to load Google Maps API');
      };

      document.head.appendChild(script);
    };

    loadGoogleMapsAPI();
  }, []);

  // Initialize map (only once)
  useEffect(() => {
    if (!apiLoaded || !mapRef.current || mapError) return;

    try {
      // Verify Google Maps API is fully loaded
      if (!window.google || !window.google.maps || !window.google.maps.LatLngBounds) {
        console.error('Google Maps API not fully loaded');
        setMapError('Google Maps API not fully loaded');
        return;
      }

      // Only create map if it doesn't exist
      if (!mapInstanceRef.current) {
        // Calculate initial bounds and center
        const bounds = new window.google.maps.LatLngBounds();
        let center = { lat: 25.7617, lng: -80.1918 }; // Miami default

        // If user location is available, use it as center
        if (userLocation) {
          center = { lat: userLocation.latitude, lng: userLocation.longitude };
          bounds.extend(new window.google.maps.LatLng(userLocation.latitude, userLocation.longitude));
        }

        // Add restaurant locations to bounds
        if (restaurantsWithCoords.length > 0) {
          restaurantsWithCoords.forEach(restaurant => {
            if (restaurant.latitude !== undefined && restaurant.longitude !== undefined) {
              bounds.extend(new window.google.maps.LatLng(restaurant.latitude, restaurant.longitude));
            }
          });
        }

        // Create map
        const map = new window.google.maps.Map(mapRef.current, {
          center: center,
          zoom: userLocation ? 14 : 10, // Very zoomed in view if user location available
          mapTypeId: window.google.maps.MapTypeId.ROADMAP,
          styles: [
            {
              featureType: 'poi',
              elementType: 'labels',
              stylers: [{ visibility: 'simplified' }]
            },
            {
              featureType: 'transit',
              elementType: 'labels',
              stylers: [{ visibility: 'simplified' }]
            },
            {
              featureType: 'water',
              elementType: 'geometry',
              stylers: [{ color: '#e3f2fd' }]
            },
            {
              featureType: 'poi.park',
              elementType: 'geometry',
              stylers: [{ color: '#e8f5e8' }]
            }
          ],
          zoomControl: true,
          mapTypeControl: false,
          scaleControl: true,
          streetViewControl: false,
          rotateControl: false,
          fullscreenControl: true,
          gestureHandling: 'cooperative'
        });

        mapInstanceRef.current = map;



        // Create info window
        infoWindowRef.current = new window.google.maps.InfoWindow({
          disableAutoPan: false,
          maxWidth: 300
        });

        // If mapCenter is provided (from URL parameters), center on it
        if (mapCenter) {
          map.setCenter(mapCenter);
          map.setZoom(16); // Zoom in close to the specific location
        } else if (userLocation) {
          // If user location is available, center on it with proper zoom
          map.setCenter({ lat: userLocation.latitude, lng: userLocation.longitude });
          map.setZoom(14); // Very zoomed in view as default
        } else if (restaurantsWithCoords.length > 0) {
          // Only fit bounds if no user location (fallback to restaurant bounds)
          map.fitBounds(bounds);
        }

        setMapLoaded(true);
      }

    } catch (error) {
      console.error('Error initializing map:', error);
      setMapError('Failed to initialize map');
    }

  }, [apiLoaded, mapError, userLocation, mapCenter]);

  // Update user location marker when userLocation changes
  useEffect(() => {
    if (!mapInstanceRef.current || !mapLoaded || !userLocation) return;

    try {
      const map = mapInstanceRef.current;

      // Remove existing user location marker
      if (userLocationMarkerRef.current) {
        userLocationMarkerRef.current.setMap(null);
      }

      // Create user location marker
      const userPosition = new window.google.maps.LatLng(userLocation.latitude, userLocation.longitude);
      
      // Create a custom user location marker
      const userMarkerIcon = {
        url: `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(`
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="16" cy="16" r="8" fill="#4285F4" stroke="white" stroke-width="3"/>
            <circle cx="16" cy="16" r="4" fill="white"/>
            <circle cx="16" cy="16" r="12" fill="#4285F4" opacity="0.3"/>
          </svg>
        `)}`,
        scaledSize: new window.google.maps.Size(32, 32),
        anchor: new window.google.maps.Point(16, 16)
      };

      userLocationMarkerRef.current = new window.google.maps.Marker({
        position: userPosition,
        map: map,
        icon: userMarkerIcon,
        title: 'Your Location',
        zIndex: 1000 // Ensure it's on top
      });

      // Add click listener to user location marker
      userLocationMarkerRef.current.addListener('click', () => {
        // Center map on user location with standard zoom
        map.panTo(userPosition);
        map.setZoom(10); // Standard 10-mile view
        
        if (infoWindowRef.current) {
          const content = `
            <div class="p-3 max-w-xs">
              <div class="flex items-center space-x-2">
                <div class="w-3 h-3 bg-blue-500 rounded-full"></div>
                <h3 class="font-semibold text-gray-900 text-sm">Your Location</h3>
              </div>
              <p class="text-gray-600 text-xs mt-1">
                ${userLocation.latitude.toFixed(6)}, ${userLocation.longitude.toFixed(6)}
              </p>
              ${userLocation.accuracy ? `
                <p class="text-gray-500 text-xs mt-1">
                  Accuracy: ±${Math.round(userLocation.accuracy)} meters
                </p>
              ` : ''}
            </div>
          `;
          infoWindowRef.current.setContent(content);
          infoWindowRef.current.open(map, userLocationMarkerRef.current);
        }
      });

    } catch (error) {
      console.error('Error updating user location marker:', error);
    }

  }, [userLocation, mapLoaded]);

  // Update map center when userLocation changes (for location searches)
  useEffect(() => {
    if (!mapInstanceRef.current || !mapLoaded || !userLocation) return;

    try {
      const map = mapInstanceRef.current;
      console.log('Updating map center to user location:', userLocation);
      
      // Smoothly pan to the new location
      map.panTo({ lat: userLocation.latitude, lng: userLocation.longitude });
      map.setZoom(14); // Zoom in to show the area
      
    } catch (error) {
      console.error('Error updating map center:', error);
    }
  }, [userLocation, mapLoaded]);

  // Update map center when mapCenter prop changes (for URL parameters)
  useEffect(() => {
    console.log('mapCenter prop changed:', mapCenter);
    console.log('mapLoaded:', mapLoaded);
    console.log('mapInstanceRef.current:', !!mapInstanceRef.current);
    
    if (!mapInstanceRef.current || !mapLoaded || !mapCenter) {
      console.log('Skipping map center update - conditions not met');
      return;
    }

    try {
      const map = mapInstanceRef.current;
      console.log('Updating map center from URL parameters:', mapCenter);
      
      // Smoothly pan to the specific restaurant location
      map.panTo(mapCenter);
      map.setZoom(16); // Zoom in close to the specific location
      
      console.log('Map center updated successfully');
      
    } catch (error) {
      console.error('Error updating map center from URL parameters:', error);
    }
  }, [mapCenter, mapLoaded]);

  // Update markers when restaurants or selectedRestaurantId changes
  useEffect(() => {
    if (!mapInstanceRef.current || !mapLoaded || restaurantsWithCoords.length === 0) return;

    try {
      const map = mapInstanceRef.current;

      // Clear existing markers
      markersRef.current.forEach(marker => marker.setMap(null));
      markersRef.current = [];

      // Create markers
      restaurantsWithCoords.forEach(restaurant => {
        if (restaurant.latitude === undefined || restaurant.longitude === undefined) {
          return; // Skip restaurants without coordinates
        }
        const position = new window.google.maps.LatLng(restaurant.latitude, restaurant.longitude);
        const isSelected = selectedRestaurantId === restaurant.id;

        // Calculate distance from user if available
        let distanceFromUser: number | null = null;
        if (userLocation) {
          const R = 3959; // Earth's radius in miles
          const dLat = (restaurant.latitude - userLocation.latitude) * Math.PI / 180;
          const dLon = (restaurant.longitude - userLocation.longitude) * Math.PI / 180;
          const a = 
            Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(userLocation.latitude * Math.PI / 180) * Math.cos(restaurant.latitude * Math.PI / 180) * 
            Math.sin(dLon/2) * Math.sin(dLon/2);
          const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
          distanceFromUser = R * c;
        }

        let marker;
        
        // Get marker color based on kosher category
        const getMarkerColor = (category?: string) => {
          switch (category?.toLowerCase()) {
            case 'meat':
              return '#dc2626'; // Bright red for meat
            case 'dairy':
              return '#2563eb'; // Bright blue for dairy
            case 'pareve':
              return '#059669'; // Bright green for pareve
            default:
              return '#4b5563'; // Dark gray for unknown
          }
        };

        const markerColor = getMarkerColor(restaurant.kosher_category);
        const finalColor = isSelected ? '#FFD700' : markerColor; // Gold if selected, otherwise category color

        // Try to use AdvancedMarkerElement (recommended by Google)
        if (window.google.maps.marker && window.google.maps.marker.AdvancedMarkerElement) {
          try {
            const pinElement = new window.google.maps.marker.PinElement({
              background: finalColor,
              borderColor: '#000000',
              glyphColor: '#FFFFFF',
              scale: 1.5
            });
            
            marker = new window.google.maps.marker.AdvancedMarkerElement({
              position: position,
              map: map,
              content: pinElement.element,
              title: restaurant.name
            });
          } catch (error) {
            console.warn('AdvancedMarkerElement failed, falling back to regular Marker:', error);
            // Fallback to regular marker
            const pinIcon = {
              url: `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(`
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z" 
                        fill="${finalColor}" 
                        stroke="#000000" 
                        stroke-width="1.5"/>
                  <circle cx="12" cy="9" r="2.5" fill="white"/>
                  <circle cx="12" cy="9" r="1.5" fill="${finalColor}"/>
                </svg>
              `)}`,
              scaledSize: new window.google.maps.Size(32, 32),
              anchor: new window.google.maps.Point(12, 24)
            };
            
            marker = new window.google.maps.Marker({
              position: position,
              map: map,
              icon: pinIcon,
              title: restaurant.name
            });
          }
        } else {
          // Fallback to regular marker if AdvancedMarkerElement is not available
          const pinIcon = {
            url: `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(`
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z" 
                      fill="${finalColor}" 
                      stroke="#000000" 
                      stroke-width="1.5"/>
                <circle cx="12" cy="9" r="2.5" fill="white"/>
                <circle cx="12" cy="9" r="1.5" fill="${finalColor}"/>
              </svg>
            `)}`,
            scaledSize: new window.google.maps.Size(32, 32),
            anchor: new window.google.maps.Point(12, 24)
          };
          
          marker = new window.google.maps.Marker({
            position: position,
            map: map,
            icon: pinIcon,
            title: restaurant.name
          });
        }

        // Add click listener with immediate execution
        marker.addListener('click', () => {
          console.log('Marker clicked:', restaurant.name); // Debug log
          
          // Update state immediately
          setSelectedMarker(restaurant);
          onRestaurantSelect?.(restaurant.id);
          
          // Show info window immediately
          if (infoWindowRef.current) {
            const content = createInfoWindowContent(restaurant, distanceFromUser);
            infoWindowRef.current.setContent(content);
            infoWindowRef.current.open(map, marker);
          }
        });

        markersRef.current.push(marker);
      });

    } catch (error) {
      console.error('Error updating markers:', error);
    }

  }, [restaurantsWithCoords, selectedRestaurantId, mapLoaded, userLocation]);

  // Helper function to get safe image URLs (avoid Google Places photo URLs)
  const getSafeImageUrl = (restaurant: Restaurant) => {
    const isGooglePlacesUrl = restaurant.image_url?.includes('maps.googleapis.com/maps/api/place/photo');
    if (isGooglePlacesUrl) {
      return null; // Skip Google Places URLs to avoid 403 errors
    }
    return restaurant.image_url;
  };

  const createInfoWindowContent = (restaurant: Restaurant, distanceFromUser?: number | null) => {
    const safeImageUrl = getSafeImageUrl(restaurant);
    
    return `
      <div class="p-3 max-w-xs relative">
        <button onclick="this.parentElement.parentElement.parentElement.close()" 
                class="absolute top-2 right-2 text-gray-400 hover:text-gray-600 text-lg font-bold leading-none">
          ×
        </button>
        <div class="flex items-start space-x-3">
          ${safeImageUrl ? `
            <img src="${safeImageUrl}" alt="${restaurant.name}" 
                 class="w-16 h-12 object-cover rounded-lg flex-shrink-0"
                 loading="lazy" />
          ` : `
            <div class="w-16 h-12 bg-gray-200 rounded-lg flex-shrink-0 flex items-center justify-center">
              <span class="text-gray-400 text-xs">No Image</span>
            </div>
          `}
          <div class="flex-1 min-w-0">
            <h3 class="font-semibold text-gray-900 text-sm leading-tight mb-1">${restaurant.name}</h3>
            <p class="text-gray-600 text-xs mb-1">${restaurant.address}</p>
            ${distanceFromUser !== null && distanceFromUser !== undefined ? `
              <p class="text-blue-600 text-xs font-medium mb-1">📍 ${distanceFromUser.toFixed(1)} miles away</p>
            ` : ''}
            ${restaurant.certifying_agency ? `
              <span class="inline-block bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded-full mb-1">
                ${restaurant.certifying_agency}
              </span>
            ` : ''}
            ${restaurant.kosher_category ? `
              <span class="inline-block ${restaurant.kosher_category === 'meat' ? 'bg-red-100 text-red-800' : restaurant.kosher_category === 'dairy' ? 'bg-blue-100 text-blue-800' : restaurant.kosher_category === 'pareve' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'} text-xs px-2 py-1 rounded-full mb-1">
                ${restaurant.kosher_category}
              </span>
            ` : ''}
            ${restaurant.avg_price ? `
              <p class="text-green-600 text-xs font-medium">${restaurant.avg_price}</p>
            ` : ''}
          </div>
        </div>
        <div class="mt-3 pt-2 border-t border-gray-200">
          <a href="/restaurant/${restaurant.id}" 
             class="text-blue-600 hover:text-blue-800 text-xs font-medium">
            View Details →
          </a>
        </div>
      </div>
    `;
  };

  // Show loading state
  if (!apiLoaded && !mapError) {
    return (
      <div className={`bg-gray-100 rounded-lg flex items-center justify-center ${className}`}>
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-jewgo-primary mx-auto mb-4"></div>
          <p className="text-gray-600">Loading interactive map...</p>
        </div>
      </div>
    );
  }

  // Show error state
  if (mapError) {
    return (
      <div className={`bg-gray-100 rounded-lg flex items-center justify-center ${className}`}>
        <div className="text-center">
          <div className="text-red-500 text-4xl mb-4">⚠️</div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Map Error</h3>
          <p className="text-gray-600 mb-4">{mapError}</p>
        </div>
      </div>
    );
  }

  if (restaurantsWithCoords.length === 0) {
    return (
      <div className={`bg-gray-100 rounded-lg flex items-center justify-center ${className}`}>
        <div className="text-center">
          <div className="text-gray-400 text-4xl mb-4">🗺️</div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2">No Location Data</h3>
          <p className="text-gray-600">No restaurants with location data available</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`relative bg-white rounded-lg shadow-lg overflow-hidden ${className}`}>
      {/* Map Container */}
      <div 
        ref={mapRef} 
        className="w-full h-full"
      />

      {/* Restaurant Count */}
      <div className="absolute bottom-4 left-4 bg-white/95 backdrop-blur-sm rounded-lg px-3 py-2 shadow-lg">
        <div className="text-xs font-medium text-gray-700">
          {restaurantsWithCoords.length} restaurants
          {userLocation && (
            <span className="text-blue-600 ml-2">📍 Your location</span>
          )}
        </div>
      </div>

      {/* Color Legend */}
      <div className="absolute top-4 left-4 bg-white/95 backdrop-blur-sm rounded-lg px-3 py-2 shadow-lg">
        <div className="text-xs font-medium text-gray-700 mb-2">Kosher Types:</div>
        <div className="space-y-1">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <span className="text-xs text-gray-600">Meat</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-blue-500"></div>
            <span className="text-xs text-gray-600">Dairy</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span className="text-xs text-gray-600">Pareve</span>
          </div>
        </div>
      </div>

      {/* Center on User Location Button */}
      {userLocation && (
        <div className="absolute top-4 right-4">
          <button
            onClick={() => {
              if (mapInstanceRef.current && userLocation) {
                mapInstanceRef.current.panTo(new window.google.maps.LatLng(userLocation.latitude, userLocation.longitude));
                mapInstanceRef.current.setZoom(10); // Standard 10-mile view instead of zoomed in
              }
            }}
            className="bg-white/95 backdrop-blur-sm rounded-lg p-2 shadow-lg hover:bg-white transition-colors"
            title="Center on your location"
          >
            <svg className="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
      )}
    </div>
  );
} 