'use client';

import { useState, useEffect, useRef } from 'react';
import { Restaurant } from '@/types/restaurant';
import Link from 'next/link';

interface SimpleMapEmbedProps {
  restaurants: Restaurant[];
  maxRestaurants?: number;
}



export default function SimpleMapEmbed({ restaurants, maxRestaurants = 50 }: SimpleMapEmbedProps) {
  const [mapLoaded, setMapLoaded] = useState(false);
  const [mapError, setMapError] = useState<string | null>(null);
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<any>(null);
  const markersRef = useRef<any[]>([]);
  const [apiLoaded, setApiLoaded] = useState(false);

  // Filter restaurants with coordinates
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
  })).slice(0, maxRestaurants);

  // Load Google Maps API
  useEffect(() => {
    const loadGoogleMapsAPI = () => {
      // Check if script is already loaded
      if (window.google && window.google.maps) {
        setApiLoaded(true);
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
      
      script.onload = () => {
        setApiLoaded(true);
      };
      
      script.onerror = () => {
        setMapError('Failed to load Google Maps API');
      };

      document.head.appendChild(script);
    };

    loadGoogleMapsAPI();
  }, []);

  useEffect(() => {
    if (!apiLoaded || !mapRef.current || restaurantsWithCoords.length === 0 || mapError) return;

    try {
      // Clear existing markers
      markersRef.current.forEach(marker => marker.setMap(null));
      markersRef.current = [];

      // Calculate center and bounds
      const bounds = new window.google.maps.LatLngBounds();
      let center = { lat: 25.7617, lng: -80.1918 }; // Miami default

      if (restaurantsWithCoords.length > 0) {
        restaurantsWithCoords.forEach(restaurant => {
          bounds.extend(new window.google.maps.LatLng(restaurant.latitude, restaurant.longitude));
        });
        const boundsCenter = bounds.getCenter();
        center = { lat: boundsCenter.lat(), lng: boundsCenter.lng() };
      }

      // Create map with clean styling
      const map = new window.google.maps.Map(mapRef.current, {
        center: center,
        zoom: 10,
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
          }
        ],
        zoomControl: false,
        mapTypeControl: false,
        scaleControl: false,
        streetViewControl: false,
        rotateControl: false,
        fullscreenControl: false,
        gestureHandling: 'cooperative'
      });

      mapInstanceRef.current = map;

      // Fit bounds if we have multiple restaurants
      if (restaurantsWithCoords.length > 1) {
        map.fitBounds(bounds);
      }

      // Create markers
      restaurantsWithCoords.forEach(restaurant => {
        const position = new window.google.maps.LatLng(restaurant.latitude, restaurant.longitude);
        const markerColor = createCustomMarkerIcon(restaurant.certifying_agency);

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
              width: 20px;
              height: 20px;
              display: flex;
              align-items: center;
              justify-content: center;
              box-shadow: 0 2px 4px rgba(0,0,0,0.2);
              cursor: pointer;
            ">
              <div style="
                background: white;
                border-radius: 50%;
                width: 6px;
                height: 6px;
              "></div>
            </div>
          `;

          marker = new window.google.maps.marker.AdvancedMarkerElement({
            position: position,
            map: map,
            content: markerElement,
            title: restaurant.name
          });
        } else {
          // Fallback to regular Marker
          marker = new window.google.maps.Marker({
            position: position,
            map: map,
            title: restaurant.name,
            icon: {
              path: window.google.maps.SymbolPath.CIRCLE,
              scale: 8,
              fillColor: markerColor,
              fillOpacity: 0.8,
              strokeColor: 'white',
              strokeWeight: 1
            }
          });
        }

        markersRef.current.push(marker);
      });

    } catch (error) {
      console.error('Error initializing map:', error);
      setMapError('Failed to initialize map');
    }

  }, [apiLoaded, restaurantsWithCoords, mapError]);

  const createCustomMarkerIcon = (certifyingAgency?: string) => {
    const colors = {
      'ORB': '#FF6B6B',
      'KM': '#4ECDC4', 
      'KDM': '#45B7D1',
      'Diamond K': '#96CEB4',
      'default': '#95A5A6'
    };

    const color = colors[certifyingAgency as keyof typeof colors] || colors.default;

    return color;
  };

  // Show loading state
  if (!apiLoaded && !mapError) {
    return (
      <div className="bg-gray-100 rounded-lg p-8 text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-jewgo-primary mx-auto mb-4"></div>
        <p className="text-gray-600">Loading map preview...</p>
      </div>
    );
  }

  // Show error state
  if (mapError) {
    return (
      <div className="bg-gray-100 rounded-lg p-8 text-center">
        <div className="text-red-500 text-4xl mb-4">⚠️</div>
        <h3 className="text-lg font-semibold text-gray-800 mb-2">Map Preview Error</h3>
        <p className="text-gray-600 mb-4">{mapError}</p>
        <Link 
          href="/live-map"
          className="inline-flex items-center px-4 py-2 bg-jewgo-primary text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          View Full Map
        </Link>
      </div>
    );
  }

  if (restaurantsWithCoords.length === 0) {
    return (
      <div className="bg-gray-100 rounded-lg p-8 text-center">
        <div className="text-gray-400 text-4xl mb-4">🗺️</div>
        <h3 className="text-lg font-semibold text-gray-800 mb-2">Map Preview</h3>
        <p className="text-gray-600 mb-4">No restaurants with location data available</p>
        <Link 
          href="/live-map"
          className="inline-flex items-center px-4 py-2 bg-jewgo-primary text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          View Full Map
        </Link>
      </div>
    );
  }

  return (
    <div className="relative bg-white rounded-lg shadow-lg overflow-hidden">
      {/* Map Header */}
      <div className="bg-gradient-to-r from-jewgo-primary to-blue-600 text-white p-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold">Interactive Map</h3>
            <p className="text-blue-100 text-sm">
              {restaurantsWithCoords.length} restaurants with location data
            </p>
          </div>
          <Link 
            href="/live-map"
            className="bg-white/20 hover:bg-white/30 text-white px-3 py-1 rounded-lg text-sm font-medium transition-colors"
          >
            View Full Map
          </Link>
        </div>
      </div>

      {/* Map Container */}
      <div className="relative">
        <div 
          ref={mapRef} 
          className="w-full h-64"
        />

        {/* Legend */}
        <div className="absolute top-2 right-2 bg-white/90 backdrop-blur-sm rounded-lg p-2 shadow-lg">
          <div className="text-xs font-medium text-gray-700 mb-1">Agencies</div>
          <div className="flex space-x-2">
            <div className="flex items-center space-x-1">
              <div className="w-2 h-2 rounded-full bg-blue-600"></div>
              <span className="text-xs">ORB</span>
            </div>
            <div className="flex items-center space-x-1">
              <div className="w-2 h-2 rounded-full bg-green-600"></div>
              <span className="text-xs">KM</span>
            </div>
            <div className="flex items-center space-x-1">
              <div className="w-2 h-2 rounded-full bg-yellow-600"></div>
              <span className="text-xs">KDM</span>
            </div>
          </div>
        </div>
      </div>

      {/* Map Footer */}
      <div className="bg-gray-50 px-4 py-3 border-t">
        <div className="flex items-center justify-between text-sm text-gray-600">
          <span>Click markers to see restaurant details</span>
          <span>{restaurantsWithCoords.length} locations</span>
        </div>
      </div>
    </div>
  );
} 