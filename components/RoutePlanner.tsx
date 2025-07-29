'use client';

import { useState, useEffect, useRef } from 'react';
import { Restaurant } from '@/types/restaurant';

interface RoutePlannerProps {
  restaurant: Restaurant;
  userLocation: { lat: number; lng: number } | null;
  onClose: () => void;
  isOpen: boolean;
}

interface RouteInfo {
  distance: string;
  duration: string;
  steps: string[];
  polyline: any;
}

export default function RoutePlanner({
  restaurant,
  userLocation,
  onClose,
  isOpen
}: RoutePlannerProps) {
  const [routeInfo, setRouteInfo] = useState<RouteInfo | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [transportMode, setTransportMode] = useState<'driving' | 'walking' | 'transit'>('driving');
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<any>(null);
  const directionsRendererRef = useRef<any>(null);

  useEffect(() => {
    if (isOpen && userLocation && restaurant.latitude && restaurant.longitude) {
      calculateRoute();
    }
  }, [isOpen, userLocation, restaurant, transportMode]);

  const calculateRoute = async () => {
    if (!userLocation || !restaurant.latitude || !restaurant.longitude) return;

    setIsLoading(true);
    setError(null);

    try {
      const directionsService = new window.google.maps.DirectionsService();
      
      const result = await directionsService.route({
        origin: new window.google.maps.LatLng(userLocation.lat, userLocation.lng),
        destination: new window.google.maps.LatLng(
          parseFloat(restaurant.latitude.toString()),
          parseFloat(restaurant.longitude.toString())
        ),
        travelMode: window.google.maps.TravelMode[transportMode.toUpperCase() as keyof typeof window.google.maps.TravelMode],
        unitSystem: window.google.maps.UnitSystem.METRIC
      });

      if (result.routes[0]) {
        const route = result.routes[0];
        const leg = route.legs[0];
        
        setRouteInfo({
          distance: leg.distance?.text || '',
          duration: leg.duration?.text || '',
          steps: leg.steps?.map(step => step.instructions) || [],
          polyline: route.overview_polyline
        });

        // Render route on map
        if (directionsRendererRef.current) {
          directionsRendererRef.current.setDirections(result);
        }
      }
    } catch (err) {
      console.error('Error calculating route:', err);
      setError('Failed to calculate route. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const initializeMap = () => {
    if (!mapRef.current || !window.google?.maps) return;

    const map = new window.google.maps.Map(mapRef.current, {
      center: { lat: 25.7617, lng: -80.1918 },
      zoom: 12,
      mapTypeId: window.google.maps.MapTypeId.ROADMAP,
      styles: [
        {
          featureType: 'poi',
          elementType: 'labels',
          stylers: [{ visibility: 'simplified' }]
        }
      ]
    });

    mapInstanceRef.current = map;

    // Initialize directions renderer
    directionsRendererRef.current = new window.google.maps.DirectionsRenderer({
      map: map,
      suppressMarkers: false,
      polylineOptions: {
        strokeColor: '#3B82F6',
        strokeWeight: 4,
        strokeOpacity: 0.8
      }
    });
  };

  const handleOpenInMaps = () => {
    if (!userLocation || !restaurant.latitude || !restaurant.longitude) return;

    const origin = `${userLocation.lat},${userLocation.lng}`;
    const destination = `${restaurant.latitude},${restaurant.longitude}`;
    const url = `https://www.google.com/maps/dir/${origin}/${destination}`;
    window.open(url, '_blank');
  };

  const handleShareRoute = () => {
    if (!userLocation || !restaurant.latitude || !restaurant.longitude) return;

    const origin = `${userLocation.lat},${userLocation.lng}`;
    const destination = `${restaurant.latitude},${restaurant.longitude}`;
    const url = `https://www.google.com/maps/dir/${origin}/${destination}`;
    
    if (navigator.share) {
      navigator.share({
        title: `Route to ${restaurant.name}`,
        text: `Get directions to ${restaurant.name}`,
        url: url
      });
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(url);
      alert('Route URL copied to clipboard!');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="p-6 border-b border-gray-200">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-xl font-bold text-gray-900">Route to {restaurant.name}</h2>
                <p className="text-gray-600 mt-1">{restaurant.address}</p>
              </div>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          {/* Transport Mode Selector */}
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex space-x-4">
              {(['driving', 'walking', 'transit'] as const).map((mode) => (
                <button
                  key={mode}
                  onClick={() => setTransportMode(mode)}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                    transportMode === mode
                      ? 'bg-jewgo-primary text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {mode === 'driving' && '🚗 Driving'}
                  {mode === 'walking' && '🚶 Walking'}
                  {mode === 'transit' && '🚌 Transit'}
                </button>
              ))}
            </div>
          </div>

          <div className="flex flex-1 overflow-hidden">
            {/* Map */}
            <div className="flex-1 relative">
              <div
                ref={mapRef}
                className="w-full h-full"
                onLoad={initializeMap}
              />
              {isLoading && (
                <div className="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center">
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-jewgo-primary mx-auto"></div>
                    <p className="mt-2 text-gray-600">Calculating route...</p>
                  </div>
                </div>
              )}
            </div>

            {/* Route Details */}
            <div className="w-80 border-l border-gray-200 overflow-y-auto">
              <div className="p-6">
                {error ? (
                  <div className="text-red-600 text-center py-4">
                    <p>{error}</p>
                    <button
                      onClick={calculateRoute}
                      className="mt-2 px-4 py-2 bg-jewgo-primary text-white rounded-lg hover:bg-jewgo-primary-dark transition-colors"
                    >
                      Try Again
                    </button>
                  </div>
                ) : routeInfo ? (
                  <div>
                    {/* Route Summary */}
                    <div className="bg-gray-50 rounded-lg p-4 mb-4">
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm text-gray-600">Distance</span>
                        <span className="font-semibold">{routeInfo.distance}</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Duration</span>
                        <span className="font-semibold">{routeInfo.duration}</span>
                      </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="space-y-3 mb-6">
                      <button
                        onClick={handleOpenInMaps}
                        className="w-full px-4 py-2 bg-jewgo-primary text-white rounded-lg hover:bg-jewgo-primary-dark transition-colors"
                      >
                        Open in Google Maps
                      </button>
                      <button
                        onClick={handleShareRoute}
                        className="w-full px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                      >
                        Share Route
                      </button>
                    </div>

                    {/* Route Steps */}
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-3">Directions</h3>
                      <div className="space-y-2">
                        {routeInfo.steps.map((step, index) => (
                          <div key={index} className="flex items-start space-x-3">
                            <div className="flex-shrink-0 w-6 h-6 bg-jewgo-primary text-white rounded-full flex items-center justify-center text-xs font-bold">
                              {index + 1}
                            </div>
                            <p className="text-sm text-gray-700 leading-relaxed">
                              {step.replace(/<[^>]*>/g, '')}
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-8 text-gray-500">
                    <p>Enter your location to get directions</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 