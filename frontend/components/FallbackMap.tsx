'use client';

import { useState } from 'react';
import { Restaurant } from '@/types/restaurant';
import Link from 'next/link';
import { safeFilter } from '@/utils/validation';

interface FallbackMapProps {
  restaurants: Restaurant[];
  onRestaurantSelect?: (restaurant: Restaurant) => void;
}

export default function FallbackMap({ restaurants, onRestaurantSelect }: FallbackMapProps) {
  const [selectedRestaurant, setSelectedRestaurant] = useState<Restaurant | null>(null);

  // Filter restaurants with coordinates
  const restaurantsWithCoords = safeFilter(restaurants, restaurant => 
    Boolean(restaurant.latitude) && Boolean(restaurant.longitude) &&
    restaurant.latitude !== 0 && restaurant.longitude !== 0
  );

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

  if (restaurantsWithCoords.length === 0) {
    return (
      <div className="w-full h-full bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="text-gray-400 text-6xl mb-4">🗺️</div>
          <p className="text-gray-600 mb-2">No restaurants with location data available</p>
          <p className="text-gray-500 text-sm">Try viewing the restaurant list instead</p>
        </div>
      </div>
    );
  }

  return (
    <div className="relative h-full bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b p-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Restaurant Locations</h3>
            <p className="text-sm text-gray-600">
              {restaurantsWithCoords.length} restaurants with location data
            </p>
          </div>
          <Link 
            href="/"
            className="bg-jewgo-primary text-white px-3 py-1 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
          >
            View List
          </Link>
        </div>
      </div>

      {/* Map Placeholder */}
      <div className="relative h-64 bg-gradient-to-br from-blue-50 to-indigo-100 border-b">
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <div className="text-blue-400 text-6xl mb-4">🗺️</div>
            <h4 className="text-lg font-semibold text-gray-800 mb-2">Interactive Map</h4>
            <p className="text-gray-600 mb-4">
              {restaurantsWithCoords.length} restaurants in your area
            </p>
            <div className="flex justify-center space-x-2">
              <div className="flex items-center space-x-1">
                <div className="w-3 h-3 rounded-full bg-blue-600"></div>
                <span className="text-xs text-gray-600">ORB</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-3 h-3 rounded-full bg-green-600"></div>
                <span className="text-xs text-gray-600">KM</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-3 h-3 rounded-full bg-yellow-600"></div>
                <span className="text-xs text-gray-600">KDM</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Restaurant List */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="space-y-3">
          {restaurantsWithCoords.slice(0, 20).map((restaurant) => (
            <div
              key={restaurant.id}
              className="bg-white rounded-lg border border-gray-200 p-4 hover:border-blue-300 cursor-pointer transition-all duration-200 hover:shadow-md"
              onClick={() => handleRestaurantClick(restaurant)}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h4 className="font-semibold text-gray-900 mb-1">{restaurant.name}</h4>
                  <p className="text-sm text-gray-600 mb-2">
                    📍 {restaurant.address}
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
                    title="Get Directions"
                  >
                    🗺️
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleViewDetails(restaurant);
                    }}
                    className="bg-gray-500 text-white px-2 py-1 rounded text-xs hover:bg-gray-600 transition-colors"
                    title="View Details"
                  >
                    📋
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        {restaurantsWithCoords.length > 20 && (
          <div className="mt-4 text-center">
            <p className="text-sm text-gray-500">
              Showing first 20 restaurants. View all {restaurantsWithCoords.length} restaurants in the list.
            </p>
            <Link 
              href="/"
              className="inline-block mt-2 bg-jewgo-primary text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
            >
              View All Restaurants
            </Link>
          </div>
        )}
      </div>

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

      {/* Status Bar */}
      <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 z-[1000] bg-white/95 backdrop-blur-sm rounded-lg shadow-lg px-4 py-2">
        <p className="text-xs text-gray-600 text-center">
          Restaurant Locations • {restaurantsWithCoords.length} restaurants • Click for details
        </p>
      </div>
    </div>
  );
} 