'use client';

import { useState, useEffect, useRef } from 'react';

interface Restaurant {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  address: string;
  city?: string;
  state?: string;
  certifying_agency?: string;
  kosher_category?: string;
  phone_number?: string;
}

interface InteractiveGoogleMapProps {
  restaurants: Restaurant[];
  onRestaurantSelect?: (restaurant: Restaurant) => void;
}



export default function InteractiveGoogleMap({ restaurants, onRestaurantSelect }: InteractiveGoogleMapProps) {
  const [selectedRestaurant, setSelectedRestaurant] = useState<Restaurant | null>(null);
  const [mapLoaded, setMapLoaded] = useState(false);
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<any>(null);
  const markersRef = useRef<any[]>([]);
  const infoWindowRef = useRef<any>(null);

  // Load Google Maps API
  useEffect(() => {
    const loadGoogleMaps = () => {
      if (window.google && window.google.maps) {
        setMapLoaded(true);
        return;
      }

      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyDHgNdax5xsC0bMFyh0xp11rLWa12N7THE&libraries=places`;
      script.async = true;
      script.defer = true;
      script.onload = () => setMapLoaded(true);
      document.head.appendChild(script);
    };

    loadGoogleMaps();
  }, []);

  // Initialize map
  useEffect(() => {
    if (!mapLoaded || !mapRef.current || restaurants.length === 0) return;

    // Calculate center based on restaurants
    const bounds = new window.google.maps.LatLngBounds();
    restaurants.forEach(restaurant => {
      bounds.extend(new window.google.maps.LatLng(restaurant.latitude, restaurant.longitude));
    });

    // Create map
    const map = new window.google.maps.Map(mapRef.current, {
      center: bounds.getCenter(),
      zoom: 12,
      mapTypeId: window.google.maps.MapTypeId.ROADMAP,
      styles: [
        {
          featureType: 'poi',
          elementType: 'labels',
          stylers: [{ visibility: 'off' }]
        }
      ]
    });

    mapInstanceRef.current = map;
    map.fitBounds(bounds);

    // Create info window
    infoWindowRef.current = new window.google.maps.InfoWindow();

    // Clear existing markers
    markersRef.current.forEach(marker => marker.setMap(null));
    markersRef.current = [];

    // Create markers for each restaurant
    restaurants.forEach(restaurant => {
      const marker = new window.google.maps.Marker({
        position: { lat: restaurant.latitude, lng: restaurant.longitude },
        map: map,
        title: restaurant.name,
        icon: createCustomMarkerIcon(restaurant.certifying_agency)
      });

      // Add click listener
      marker.addListener('click', () => {
        setSelectedRestaurant(restaurant);
        if (onRestaurantSelect) {
          onRestaurantSelect(restaurant);
        }

        // Show info window
        const content = `
          <div style="padding: 10px; max-width: 250px;">
            <h3 style="margin: 0 0 8px 0; font-size: 16px; font-weight: bold;">${restaurant.name}</h3>
            <p style="margin: 0 0 8px 0; font-size: 12px; color: #666;">${restaurant.address}</p>
            ${restaurant.phone_number ? `<p style="margin: 0 0 8px 0; font-size: 12px;">📞 ${restaurant.phone_number}</p>` : ''}
            <div style="display: flex; gap: 4px; margin-bottom: 8px;">
              ${restaurant.certifying_agency ? `<span style="background: ${getAgencyColor(restaurant.certifying_agency)}; color: white; padding: 2px 6px; border-radius: 10px; font-size: 10px;">${restaurant.certifying_agency}</span>` : ''}
              ${restaurant.kosher_category ? `<span style="background: #f3f4f6; color: #374151; padding: 2px 6px; border-radius: 10px; font-size: 10px;">${restaurant.kosher_category}</span>` : ''}
            </div>
            <div style="display: flex; gap: 4px;">
              <button onclick="window.open('https://www.google.com/maps/dir/?api=1&destination=${restaurant.latitude},${restaurant.longitude}', '_blank')" style="background: #3b82f6; color: white; border: none; padding: 4px 8px; border-radius: 4px; font-size: 10px; cursor: pointer;">Directions</button>
              <button onclick="window.location.href='/restaurant/${restaurant.id}'" style="background: #6b7280; color: white; border: none; padding: 4px 8px; border-radius: 4px; font-size: 10px; cursor: pointer;">Details</button>
            </div>
          </div>
        `;

        infoWindowRef.current.setContent(content);
        infoWindowRef.current.open(map, marker);
      });

      markersRef.current.push(marker);
    });
  }, [mapLoaded, restaurants, onRestaurantSelect]);

  const createCustomMarkerIcon = (certifyingAgency?: string) => {
    const colors = {
      'ORB': '#3B82F6',
      'KM': '#10B981',
      'KDM': '#F59E0B',
      'Diamond K': '#8B5CF6',
      'default': '#6B7280'
    };

    const color = colors[certifyingAgency as keyof typeof colors] || colors.default;
    const label = certifyingAgency === 'ORB' ? 'O' : 
                  certifyingAgency === 'KM' ? 'K' :
                  certifyingAgency === 'KDM' ? 'D' : 
                  certifyingAgency === 'Diamond K' ? 'DK' : 'R';

    return {
      path: window.google.maps.SymbolPath.CIRCLE,
      fillColor: color,
      fillOpacity: 1,
      strokeColor: 'white',
      strokeWeight: 2,
      scale: 12,
      label: {
        text: label,
        color: 'white',
        fontSize: '10px',
        fontWeight: 'bold'
      }
    };
  };

  const getAgencyColor = (certifyingAgency?: string) => {
    const colors = {
      'ORB': '#3B82F6',
      'KM': '#10B981',
      'KDM': '#F59E0B',
      'Diamond K': '#8B5CF6',
      'default': '#6B7280'
    };
    return colors[certifyingAgency as keyof typeof colors] || colors.default;
  };

  const handleRestaurantClick = (restaurant: Restaurant) => {
    setSelectedRestaurant(restaurant);
    if (onRestaurantSelect) {
      onRestaurantSelect(restaurant);
    }

    // Pan to marker
    if (mapInstanceRef.current) {
      mapInstanceRef.current.panTo({ lat: restaurant.latitude, lng: restaurant.longitude });
      mapInstanceRef.current.setZoom(15);
    }
  };

  const handleGetDirections = (restaurant: Restaurant) => {
    const url = `https://www.google.com/maps/dir/?api=1&destination=${restaurant.latitude},${restaurant.longitude}`;
    window.open(url, '_blank');
  };

  const handleViewDetails = (restaurant: Restaurant) => {
    window.location.href = `/restaurant/${restaurant.id}`;
  };

  return (
    <div className="relative h-full">
      {/* Google Maps Container */}
      <div ref={mapRef} className="w-full h-full" />

      {/* Restaurant List Overlay */}
      <div className="absolute top-4 left-4 z-10 max-w-sm">
        <div className="bg-white/95 backdrop-blur-sm rounded-lg shadow-lg p-4 max-h-96 overflow-y-auto">
          <h3 className="font-semibold text-lg text-gray-800 mb-3">Kosher Restaurants</h3>
          <p className="text-sm text-gray-600 mb-3">
            <strong>{restaurants.length}</strong> restaurants found
          </p>
          
          <div className="space-y-2">
            {restaurants.slice(0, 10).map((restaurant) => (
              <div
                key={restaurant.id}
                className="p-3 bg-white rounded-lg border border-gray-200 hover:border-blue-300 cursor-pointer transition-all duration-200 hover:shadow-md"
                onClick={() => handleRestaurantClick(restaurant)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h4 className="font-medium text-sm text-gray-900 mb-1">{restaurant.name}</h4>
                    <p className="text-xs text-gray-600 mb-2">
                      {restaurant.address}
                      {restaurant.city && `, ${restaurant.city}`}
                      {restaurant.state && `, ${restaurant.state}`}
                    </p>
                    <div className="flex items-center space-x-2">
                      {restaurant.certifying_agency && (
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                          restaurant.certifying_agency === 'ORB' ? 'bg-blue-100 text-blue-800' :
                          restaurant.certifying_agency === 'KM' ? 'bg-green-100 text-green-800' :
                          restaurant.certifying_agency === 'KDM' ? 'bg-yellow-100 text-yellow-800' :
                          restaurant.certifying_agency === 'Diamond K' ? 'bg-purple-100 text-purple-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {restaurant.certifying_agency}
                        </span>
                      )}
                      {restaurant.kosher_category && (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                          {restaurant.kosher_category}
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="flex flex-col space-y-1 ml-2">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleGetDirections(restaurant);
                      }}
                      className="bg-blue-500 text-white px-2 py-1 rounded text-xs hover:bg-blue-600 transition-colors"
                    >
                      🗺️
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleViewDetails(restaurant);
                      }}
                      className="bg-gray-500 text-white px-2 py-1 rounded text-xs hover:bg-gray-600 transition-colors"
                    >
                      📋
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          {restaurants.length > 10 && (
            <p className="text-xs text-gray-500 mt-2 text-center">
              Showing first 10 restaurants. Click to see more on map.
            </p>
          )}
        </div>
      </div>

      {/* Legend */}
      <div className="absolute top-4 right-4 z-10">
        <div className="bg-white/95 backdrop-blur-sm rounded-lg shadow-lg p-3">
          <h4 className="font-semibold text-sm mb-2">Certification</h4>
          <div className="space-y-1 text-xs">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded-full bg-blue-600"></div>
              <span>ORB</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded-full bg-green-600"></div>
              <span>KM</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded-full bg-yellow-600"></div>
              <span>KDM</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded-full bg-purple-600"></div>
              <span>Diamond K</span>
            </div>
          </div>
        </div>
      </div>

      {/* Instructions */}
      <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 z-10 bg-white/95 backdrop-blur-sm rounded-lg shadow-lg px-4 py-2">
        <p className="text-xs text-gray-600 text-center">
          Interactive Google Maps • Click markers for details • Use list to navigate
        </p>
      </div>

      {/* Restaurant Info Panel */}
      {selectedRestaurant && (
        <div className="absolute bottom-4 left-4 right-4 z-10 bg-white rounded-lg shadow-xl p-4 animate-fade-in-up">
          <div className="flex items-start justify-between mb-3">
            <div className="flex-1">
              <h3 className="font-bold text-lg text-gray-900">{selectedRestaurant.name}</h3>
              <p className="text-gray-600 text-sm mt-1">
                {selectedRestaurant.address}
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
              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                selectedRestaurant.certifying_agency === 'ORB' ? 'bg-blue-100 text-blue-800' :
                selectedRestaurant.certifying_agency === 'KM' ? 'bg-green-100 text-green-800' :
                selectedRestaurant.certifying_agency === 'KDM' ? 'bg-yellow-100 text-yellow-800' :
                selectedRestaurant.certifying_agency === 'Diamond K' ? 'bg-purple-100 text-purple-800' :
                'bg-gray-100 text-gray-800'
              }`}>
                {selectedRestaurant.certifying_agency}
              </span>
            )}
            {selectedRestaurant.kosher_category && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
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
    </div>
  );
} 