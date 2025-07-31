'use client';

import { useState } from 'react';
import UnifiedSearchBar from './UnifiedSearchBar';

interface UserLocation {
  latitude: number;
  longitude: number;
  accuracy?: number;
}

export default function SearchTest() {
  const [searchLog, setSearchLog] = useState<string[]>([]);
  const [userLocation, setUserLocation] = useState<UserLocation | null>(null);

  const handleRestaurantSearch = (query: string) => {
    const log = `Restaurant search: "${query}"`;
    setSearchLog(prev => [log, ...prev.slice(0, 9)]);
    console.log(log);
  };

  const handleLocationSearch = (location: UserLocation, address: string) => {
    const log = `Location search: "${address}" -> ${location.latitude}, ${location.longitude}`;
    setSearchLog(prev => [log, ...prev.slice(0, 9)]);
    setUserLocation(location);
    console.log(log);
  };

  const handleUseCurrentLocation = () => {
    const log = 'Use current location clicked';
    setSearchLog(prev => [log, ...prev.slice(0, 9)]);
    console.log(log);
  };

  const mockRestaurants = [
    { id: 1, name: 'Pizza Place', address: '123 Main St', city: 'Miami' },
    { id: 2, name: 'Sushi Bar', address: '456 Oak Ave', city: 'Miami Beach' },
    { id: 3, name: 'Burger Joint', address: '789 Pine Rd', city: 'Hollywood' }
  ];

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Search Functionality Test</h1>
      
      <div className="mb-6">
        <UnifiedSearchBar
          onRestaurantSearch={handleRestaurantSearch}
          onLocationSearch={handleLocationSearch}
          onUseCurrentLocation={handleUseCurrentLocation}
          restaurants={mockRestaurants}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h2 className="text-lg font-semibold mb-3">Search Log</h2>
          <div className="bg-gray-50 p-4 rounded-lg h-64 overflow-y-auto">
            {searchLog.length === 0 ? (
              <p className="text-gray-500">No searches yet. Try searching for something!</p>
            ) : (
              <div className="space-y-2">
                {searchLog.map((log, index) => (
                  <div key={index} className="text-sm bg-white p-2 rounded border">
                    {log}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div>
          <h2 className="text-lg font-semibold mb-3">Current Location</h2>
          <div className="bg-gray-50 p-4 rounded-lg">
            {userLocation ? (
              <div>
                <p><strong>Latitude:</strong> {userLocation.latitude}</p>
                <p><strong>Longitude:</strong> {userLocation.longitude}</p>
                {userLocation.accuracy && (
                  <p><strong>Accuracy:</strong> {userLocation.accuracy}m</p>
                )}
              </div>
            ) : (
              <p className="text-gray-500">No location set</p>
            )}
          </div>

          <h2 className="text-lg font-semibold mb-3 mt-6">Test Examples</h2>
          <div className="bg-blue-50 p-4 rounded-lg">
            <p className="text-sm font-semibold mb-2">Try these searches:</p>
            <ul className="text-sm space-y-1">
              <li>• <strong>Location:</strong> "33139", "Miami Beach", "123 Main St"</li>
              <li>• <strong>Restaurant:</strong> "Pizza", "Sushi", "Burger"</li>
              <li>• <strong>City:</strong> "Hollywood, FL", "Boca Raton"</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
} 