'use client';

import { useState, useEffect } from 'react';

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

interface SimpleRealMapProps {
  restaurants: Restaurant[];
  onRestaurantSelect?: (restaurant: Restaurant) => void;
}

export default function SimpleRealMap({ restaurants, onRestaurantSelect }: SimpleRealMapProps) {
  const [selectedRestaurant, setSelectedRestaurant] = useState<Restaurant | null>(null);
  const [mapCenter, setMapCenter] = useState<{ lat: number; lng: number }>({ lat: 25.7617, lng: -80.1918 });

  // Calculate center based on restaurants
  useEffect(() => {
    if (restaurants.length > 0) {
      const totalLat = restaurants.reduce((sum, r) => sum + r.latitude, 0);
      const totalLng = restaurants.reduce((sum, r) => sum + r.longitude, 0);
      setMapCenter({
        lat: totalLat / restaurants.length,
        lng: totalLng / restaurants.length
      });
    }
  }, [restaurants]);

  const handleRestaurantClick = (restaurant: Restaurant) => {
    setSelectedRestaurant(restaurant);
    if (onRestaurantSelect) {
      onRestaurantSelect(restaurant);
    }
  };

  const handleGetDirections = (restaurant: Restaurant) => {
    const url = `https://www.google.com/maps/dir/?api=1&destination=${restaurant.latitude},${restaurant.longitude}`;
    window.open(url, '_blank');
  };

  const handleViewDetails = (restaurant: Restaurant) => {
    window.location.href = `/restaurant/${restaurant.id}`;
  };

  // Create Google Maps URL with markers
  const createMapUrl = () => {
    if (restaurants.length === 0) {
      return `https://www.google.com/maps/embed/v1/view?key=AIzaSyDHgNdax5xsC0bMFyh0xp11rLWa12N7THE&center=${mapCenter.lat},${mapCenter.lng}&zoom=12`;
    }

    const markers = restaurants.map(r => `${r.latitude},${r.longitude}`).join('|');
    return `https://www.google.com/maps/embed/v1/view?key=AIzaSyDHgNdax5xsC0bMFyh0xp11rLWa12N7THE&center=${mapCenter.lat},${mapCenter.lng}&zoom=11&maptype=roadmap`;
  };

  return (
    <div className="relative h-full">
      {/* Real Google Maps Embed */}
      <div className="w-full h-full">
        <iframe
          src={createMapUrl()}
          width="100%"
          height="100%"
          style={{ border: 0 }}
          allowFullScreen
          loading="lazy"
          referrerPolicy="no-referrer-when-downgrade"
          title="Kosher Restaurants Map"
        ></iframe>
      </div>

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
              Showing first 10 restaurants. Use search to find more.
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
          Real Google Maps • Click restaurants for details • Use 🗺️ for directions
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