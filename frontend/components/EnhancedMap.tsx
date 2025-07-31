'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { Restaurant } from '@/types/restaurant';

interface EnhancedMapProps {
  restaurants: Restaurant[];
  onRestaurantSelect?: (restaurant: Restaurant) => void;
  initialCenter?: { lat: number; lng: number };
  initialZoom?: number;
}



export default function EnhancedMap({ 
  restaurants, 
  onRestaurantSelect,
  initialCenter = { lat: 25.7617, lng: -80.1918 }, // Miami default
  initialZoom = 10
}: EnhancedMapProps) {
  const [selectedRestaurant, setSelectedRestaurant] = useState<Restaurant | null>(null);
  const [mapLoaded, setMapLoaded] = useState(false);
  const [mapError, setMapError] = useState<string | null>(null);
  const [userLocation, setUserLocation] = useState<{ lat: number; lng: number } | null>(null);

  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<any>(null);
  const markersRef = useRef<any[]>([]);
  const infoWindowRef = useRef<any>(null);
  const clustererRef = useRef<any>(null);

  // Filter restaurants with valid coordinates
  const restaurantsWithCoords = restaurants.filter(restaurant => {
    // Check if coordinates exist and are valid numbers
    if (!restaurant.latitude || !restaurant.longitude) return false;
    
    const lat = parseFloat(restaurant.latitude.toString());
    const lng = parseFloat(restaurant.longitude.toString());
    
    if (isNaN(lat) || isNaN(lng)) return false;
    
    // Check if coordinates are not zero (invalid coordinates)
    if (lat === 0 && lng === 0) return false;
    
    // Check if coordinates are within reasonable bounds for Miami area
    // Miami area roughly: lat 25.5-26.5, lng -80.5 to -80.0
    if (lat < 24 || lat > 27 || lng < -81 || lng > -79) return false;
    
    return true;
  }).map(restaurant => ({
    ...restaurant,
    latitude: parseFloat(restaurant.latitude!.toString()),
    longitude: parseFloat(restaurant.longitude!.toString())
  }));

  // Load Google Maps API
  useEffect(() => {
    const loadGoogleMapsAPI = () => {
      // Check if script is already loaded
      if (window.google && window.google.maps) {
        setMapLoaded(true);
        return;
      }

      // Check if script is already loading
      if (document.querySelector('script[src*="maps.googleapis.com"]')) {
        return;
      }

      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=${process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY}&libraries=places,geometry&loading=async`;
      script.async = true;
      script.defer = true;
      
      // Load MarkerClusterer library
      const clustererScript = document.createElement('script');
      clustererScript.src = 'https://unpkg.com/@googlemaps/markerclusterer/dist/index.min.js';
      clustererScript.async = true;
      clustererScript.defer = true;
      
      script.onload = () => {
        setMapLoaded(true);
      };
      
      script.onerror = () => {
        setMapError('Failed to load Google Maps API');
      };

      document.head.appendChild(script);
    };

    loadGoogleMapsAPI();
  }, []);

  // Don't request location automatically - wait for user interaction
  // useEffect(() => {
  //   if (navigator.geolocation) {
  //     navigator.geolocation.getCurrentPosition(
  //       (position) => {
  //         setUserLocation({
  //           lat: position.coords.latitude,
  //           lng: position.coords.longitude
  //         });
  //       },
  //       (error) => {
  //         console.log('Geolocation error:', error);
  //       }
  //     );
  //   }
  // }, []);

  // Initialize map when API is loaded
  useEffect(() => {
    if (!mapLoaded || !mapRef.current || restaurantsWithCoords.length === 0 || mapError) return;

    try {
      // Ensure Google Maps API is fully loaded
      if (!window.google || !window.google.maps || !window.google.maps.LatLngBounds) {
        console.log('Waiting for Google Maps API to fully load...');
        return;
      }

      // Clear existing markers
      markersRef.current.forEach(marker => marker.setMap(null));
      markersRef.current = [];

      // Calculate center and bounds
      const bounds = new window.google.maps.LatLngBounds();
      let center = initialCenter;

      if (restaurantsWithCoords.length > 0) {
        restaurantsWithCoords.forEach(restaurant => {
          bounds.extend(new window.google.maps.LatLng(restaurant.latitude, restaurant.longitude));
        });
        const boundsCenter = bounds.getCenter();
        center = { lat: boundsCenter.lat(), lng: boundsCenter.lng() };
      }

      // Create map with clean, professional styling
      const map = new window.google.maps.Map(mapRef.current, {
        center: center,
        zoom: initialZoom,
        mapTypeId: window.google.maps.MapTypeId.ROADMAP,
        styles: [
          // Keep POI labels but make them subtle
          {
            featureType: 'poi',
            elementType: 'labels',
            stylers: [{ visibility: 'simplified' }]
          },
          // Keep transit but make it subtle
          {
            featureType: 'transit',
            elementType: 'labels',
            stylers: [{ visibility: 'simplified' }]
          },
          // Enhance water features
          {
            featureType: 'water',
            elementType: 'geometry',
            stylers: [{ color: '#e3f2fd' }]
          },
          // Enhance parks
          {
            featureType: 'poi.park',
            elementType: 'geometry',
            stylers: [{ color: '#e8f5e8' }]
          },
          // Make roads more visible
          {
            featureType: 'road',
            elementType: 'geometry',
            stylers: [{ color: '#ffffff' }]
          },
          {
            featureType: 'road.highway',
            elementType: 'geometry',
            stylers: [{ color: '#f5f5f5' }]
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

      // Fit bounds if we have multiple restaurants
      if (restaurantsWithCoords.length > 1) {
        map.fitBounds(bounds);
        // Add some padding to the bounds
        const listener = window.google.maps.event.addListenerOnce(map, 'bounds_changed', () => {
          const bounds = map.getBounds();
          if (bounds) {
            bounds.extend(new window.google.maps.LatLng(bounds.getNorthEast().lat() + 0.01, bounds.getNorthEast().lng() + 0.01));
            bounds.extend(new window.google.maps.LatLng(bounds.getSouthWest().lat() - 0.01, bounds.getSouthWest().lng() - 0.01));
            map.fitBounds(bounds);
          }
        });
      }

      // Create info window
      infoWindowRef.current = new window.google.maps.InfoWindow();

      // Create markers with custom styling
      restaurantsWithCoords.forEach(restaurant => {
        const position = new window.google.maps.LatLng(restaurant.latitude, restaurant.longitude);
        const markerColor = createCustomMarkerIcon(restaurant.kosher_category);

        let marker;
        
        // Check if AdvancedMarkerElement is available
        if (window.google.maps.marker && window.google.maps.marker.AdvancedMarkerElement) {
          // Create marker with enhanced styling
          const markerElement = document.createElement('div');
          markerElement.innerHTML = `
            <div style="
              background: ${markerColor};
              border: 2px solid white;
              border-radius: 50%;
              width: 24px;
              height: 24px;
              display: flex;
              align-items: center;
              justify-content: center;
              box-shadow: 0 2px 6px rgba(0,0,0,0.3);
              cursor: pointer;
              transition: all 0.2s ease;
            ">
              <div style="
                background: white;
                border-radius: 50%;
                width: 8px;
                height: 8px;
              "></div>
            </div>
          `;

          marker = new window.google.maps.marker.AdvancedMarkerElement({
            position: position,
            map: map,
            content: markerElement,
            title: restaurant.name
          });

          // Add hover effects for AdvancedMarkerElement
          marker.addListener('mouseover', () => {
            markerElement.style.transform = 'scale(1.2)';
          });

          marker.addListener('mouseout', () => {
            markerElement.style.transform = 'scale(1)';
          });
        } else {
          // Fallback to regular Marker
          marker = new window.google.maps.Marker({
            position: position,
            map: map,
            title: restaurant.name,
            icon: {
              path: window.google.maps.SymbolPath.CIRCLE,
              scale: 12,
              fillColor: markerColor,
              fillOpacity: 0.9,
              strokeColor: 'white',
              strokeWeight: 2
            },
            animation: window.google.maps.Animation.DROP
          });
        }

        // Add click listener
        marker.addListener('click', () => {
          if (infoWindowRef.current) {
            infoWindowRef.current.setContent(createInfoWindowContent(restaurant));
            infoWindowRef.current.open(map, marker);
          }
          if (onRestaurantSelect) {
            onRestaurantSelect(restaurant);
          }
        });

        markersRef.current.push(marker);
      });

      // Initialize MarkerClusterer if available
      if ((window as any).MarkerClusterer && markersRef.current.length > 0) {
        // Clear existing clusterer
        if (clustererRef.current) {
          clustererRef.current.clearMarkers();
        }

        // Create new clusterer
        clustererRef.current = new (window as any).MarkerClusterer({
          map: map,
          markers: markersRef.current,
          algorithm: new (window as any).MarkerClusterer.GridAlgorithm({
            maxZoom: 15,
            gridSize: 60
          }),
          renderer: {
            render: ({ count, position }: { count: number; position: any }) => {
              const clusterElement = document.createElement('div');
              clusterElement.innerHTML = `
                <div style="
                  background: #3B82F6;
                  border: 3px solid white;
                  border-radius: 50%;
                  width: 40px;
                  height: 40px;
                  display: flex;
                  align-items: center;
                  justify-content: center;
                  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                  cursor: pointer;
                  font-weight: bold;
                  color: white;
                  font-size: 14px;
                ">
                  ${count}
                </div>
              `;

              return new window.google.maps.marker.AdvancedMarkerElement({
                position: position,
                content: clusterElement
              });
            }
          }
        });
      }

      setMapLoaded(true);

    } catch (error) {
      console.error('Error initializing map:', error);
      setMapError('Failed to initialize map');
    }
  }, [mapLoaded, restaurantsWithCoords, initialCenter, initialZoom, mapError, onRestaurantSelect]);

  const createCustomMarkerIcon = (kosherCategory?: string) => {
    const colors = {
      'meat': '#ef4444', // Red for meat
      'dairy': '#3b82f6', // Blue for dairy
      'pareve': '#10b981', // Green for pareve
      'default': '#6b7280' // Gray for unknown
    };

    const color = colors[kosherCategory?.toLowerCase() as keyof typeof colors] || colors.default;

    return color;
  };

  const createInfoWindowContent = (restaurant: Restaurant) => {
    const kosherColors = {
      'meat': '#ef4444',
      'dairy': '#3b82f6',
      'pareve': '#10b981',
      'default': '#6b7280'
    };

    const kosherColor = kosherColors[restaurant.kosher_category?.toLowerCase() as keyof typeof kosherColors] || kosherColors.default;

    return `
      <div style="padding: 16px; max-width: 300px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <h3 style="margin: 0 0 8px 0; font-weight: 600; color: #1f2937; font-size: 16px; line-height: 1.3;">${restaurant.name}</h3>
        <p style="margin: 0 0 12px 0; color: #6b7280; font-size: 14px; line-height: 1.4;">
          📍 ${restaurant.address}${restaurant.city ? `, ${restaurant.city}` : ''}${restaurant.state ? `, ${restaurant.state}` : ''}
        </p>
        ${restaurant.phone_number ? `<p style="margin: 0 0 12px 0; color: #6b7280; font-size: 14px;">📞 ${restaurant.phone_number}</p>` : ''}
        <div style="display: flex; gap: 6px; margin-bottom: 16px; flex-wrap: wrap;">
          ${restaurant.certifying_agency ? `<span style="background-color: #f3f4f6; color: #6b7280; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 500;">${restaurant.certifying_agency}</span>` : ''}
          ${restaurant.kosher_category ? `<span style="background-color: ${kosherColor}20; color: ${kosherColor}; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 500;">${restaurant.kosher_category}</span>` : ''}
        </div>
        <div style="display: flex; gap: 8px;">
          <button onclick="window.open('https://www.google.com/maps/dir/?api=1&destination=${restaurant.latitude},${restaurant.longitude}', '_blank')" style="background-color: #3b82f6; color: white; border: none; padding: 8px 16px; border-radius: 8px; font-size: 13px; cursor: pointer; font-weight: 500; flex: 1;">🗺️ Directions</button>
          <button onclick="window.location.href='/restaurant/${restaurant.id}'" style="background-color: #6b7280; color: white; border: none; padding: 8px 16px; border-radius: 8px; font-size: 13px; cursor: pointer; font-weight: 500; flex: 1;">📋 Details</button>
        </div>
      </div>
    `;
  };

  const handleRestaurantClick = useCallback((restaurant: Restaurant) => {
    setSelectedRestaurant(restaurant);
    if (onRestaurantSelect) {
      onRestaurantSelect(restaurant);
    }
  }, [onRestaurantSelect]);

  const handleGetDirections = (restaurant: Restaurant) => {
    const url = `https://www.google.com/maps/dir/?api=1&destination=${restaurant.latitude},${restaurant.longitude}`;
    window.open(url, '_blank');
  };

  const handleViewDetails = (restaurant: Restaurant) => {
    window.location.href = `/restaurant/${restaurant.id}`;
  };

  const handleCenterOnUser = () => {
    if (userLocation && mapInstanceRef.current) {
      mapInstanceRef.current.setCenter(userLocation);
      mapInstanceRef.current.setZoom(14);
    }
  };

  const handleCenterOnRestaurants = () => {
    if (mapInstanceRef.current && restaurantsWithCoords.length > 0) {
      const bounds = new window.google.maps.LatLngBounds();
      restaurantsWithCoords.forEach(restaurant => {
        bounds.extend(new window.google.maps.LatLng(restaurant.latitude, restaurant.longitude));
      });
      mapInstanceRef.current.fitBounds(bounds);
    }
  };

  // Show loading state
  if (!mapLoaded && !mapError) {
    return (
      <div className="w-full h-full bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-jewgo-primary mx-auto mb-4"></div>
          <p className="text-gray-600">Loading map...</p>
        </div>
      </div>
    );
  }

  // Show error state
  if (mapError) {
    return (
      <div className="w-full h-full bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Map Loading Error</h3>
          <p className="text-gray-600 mb-4">{mapError}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="bg-jewgo-primary text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (restaurantsWithCoords.length === 0) {
    return (
      <div className="w-full h-full bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="text-gray-400 text-6xl mb-4">🗺️</div>
          <p className="text-gray-600 mb-2">No restaurants with location data</p>
          <p className="text-gray-500 text-sm">Try adjusting your search or filters</p>
        </div>
      </div>
    );
  }

  return (
    <div className="relative h-full">
      {/* Map Controls */}
      <div className="absolute top-4 right-4 z-[1000] flex flex-col gap-2">
        {userLocation && (
          <button
            onClick={handleCenterOnUser}
            className="p-3 bg-white/95 backdrop-blur-sm rounded-lg shadow-lg border border-gray-200 hover:bg-white transition-colors"
            title="Center on My Location"
          >
            📍
          </button>
        )}
        
        <button
          onClick={handleCenterOnRestaurants}
          className="p-3 bg-white/95 backdrop-blur-sm rounded-lg shadow-lg border border-gray-200 hover:bg-white transition-colors"
          title="Show All Restaurants"
        >
          🎯
        </button>
      </div>

      {/* Legend */}
      <div className="absolute top-4 left-4 z-[1000]">
        <div className="bg-white/95 backdrop-blur-sm rounded-lg shadow-lg p-4">
          <h4 className="font-semibold text-sm mb-3">Kosher Types</h4>
          <div className="space-y-2 text-xs">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#A70000' }}></div>
              <span>Meat</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#ADD8E6' }}></div>
              <span>Dairy</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#FFCE6D' }}></div>
              <span>Pareve</span>
            </div>
          </div>
        </div>
      </div>

      {/* Google Maps Container */}
      <div 
        ref={mapRef} 
        className="w-full h-full"
        style={{ minHeight: '400px' }}
      />

      {/* Restaurant Info Panel */}
      {selectedRestaurant && (
        <div className="absolute bottom-4 left-4 right-4 z-[1000] bg-white rounded-lg shadow-xl p-4 animate-fade-in-up">
          <div className="flex items-start justify-between mb-3">
            <div className="flex-1">
              <h3 className="font-bold text-lg text-gray-900">{selectedRestaurant.name}</h3>
              <p className="text-gray-600 text-sm mt-1">
                📍 {selectedRestaurant.address}
                {selectedRestaurant.city && `, ${selectedRestaurant.city}`}
                {selectedRestaurant.state && `, ${selectedRestaurant.state}`}
              </p>
            </div>
            <button
              onClick={() => setSelectedRestaurant(null)}
              className="text-gray-400 hover:text-gray-600 ml-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {selectedRestaurant.phone_number && (
            <p className="text-gray-600 text-sm mb-3">
              📞 {selectedRestaurant.phone_number}
            </p>
          )}

          <div className="flex items-center space-x-2 mb-3">
            {selectedRestaurant.certifying_agency && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                {selectedRestaurant.certifying_agency}
              </span>
            )}
            {selectedRestaurant.kosher_category && (
              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                selectedRestaurant.kosher_category === 'meat' ? 'bg-red-50 text-red-900 border border-red-200' :
                selectedRestaurant.kosher_category === 'dairy' ? 'bg-blue-50 text-blue-900 border border-blue-200' :
                selectedRestaurant.kosher_category === 'pareve' ? 'bg-yellow-50 text-yellow-900 border border-yellow-200' :
                'bg-gray-100 text-gray-800'
              }`}>
                {selectedRestaurant.kosher_category}
              </span>
            )}
          </div>

          <div className="flex space-x-2">
            <button
              onClick={() => handleGetDirections(selectedRestaurant)}
              className="flex-1 bg-jewgo-primary text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
            >
              Get Directions
            </button>
            <button
              onClick={() => handleViewDetails(selectedRestaurant)}
              className="flex-1 bg-gray-100 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors"
            >
              View Details
            </button>
          </div>
        </div>
      )}

      {/* Status Bar */}
      <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 z-[1000] bg-white/95 backdrop-blur-sm rounded-lg shadow-lg px-4 py-2">
        <p className="text-xs text-gray-600 text-center">
          {restaurantsWithCoords.length} restaurants • Click markers for details
        </p>
      </div>
    </div>
  );
} 