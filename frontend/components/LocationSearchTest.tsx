'use client';

import { useState } from 'react';
import UnifiedSearchBar from './UnifiedSearchBar';

interface UserLocation {
  latitude: number;
  longitude: number;
  accuracy?: number;
}

export default function LocationSearchTest() {
  const [searchLog, setSearchLog] = useState<string[]>([]);
  const [userLocation, setUserLocation] = useState<UserLocation | null>(null);

  const handleRestaurantSearch = (query: string) => {
    const log = `🍽️ Restaurant search: "${query}"`;
    setSearchLog(prev => [log, ...prev.slice(0, 9)]);
    console.log(log);
  };

  const handleLocationSearch = (location: UserLocation, address: string) => {
    const log = `📍 Location search: "${address}" -> ${location.latitude.toFixed(6)}, ${location.longitude.toFixed(6)}`;
    setSearchLog(prev => [log, ...prev.slice(0, 9)]);
    setUserLocation(location);
    console.log(log);
  };

  const handleUseCurrentLocation = () => {
    const log = '📍 Use current location clicked';
    setSearchLog(prev => [log, ...prev.slice(0, 9)]);
    console.log(log);
  };

  const mockRestaurants = [
    { id: 1, name: 'Pizza Place', address: '123 Main St', city: 'Miami' },
    { id: 2, name: 'Sushi Bar', address: '456 Oak Ave', city: 'Miami Beach' },
    { id: 3, name: 'Burger Joint', address: '789 Pine Rd', city: 'Hollywood' }
  ];

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">📍 Location Search Test</h1>
      
      <div className="mb-6">
        <UnifiedSearchBar
          onRestaurantSearch={handleRestaurantSearch}
          onLocationSearch={handleLocationSearch}
          onUseCurrentLocation={handleUseCurrentLocation}
          restaurants={mockRestaurants}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h2 className="text-lg font-semibold mb-3">🔍 Search Log</h2>
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

        <div className="space-y-6">
          <div>
            <h2 className="text-lg font-semibold mb-3">📍 Current Location</h2>
            <div className="bg-gray-50 p-4 rounded-lg">
              {userLocation ? (
                <div>
                  <p><strong>Latitude:</strong> {userLocation.latitude.toFixed(6)}</p>
                  <p><strong>Longitude:</strong> {userLocation.longitude.toFixed(6)}</p>
                  {userLocation.accuracy && (
                    <p><strong>Accuracy:</strong> {userLocation.accuracy}m</p>
                  )}
                  <div className="mt-3">
                    <a 
                      href={`https://www.google.com/maps?q=${userLocation.latitude},${userLocation.longitude}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800 text-sm"
                    >
                      🔗 View on Google Maps
                    </a>
                  </div>
                </div>
              ) : (
                <p className="text-gray-500">No location set</p>
              )}
            </div>
          </div>

          <div>
            <h2 className="text-lg font-semibold mb-3">🧪 Test Examples</h2>
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="text-sm font-semibold mb-2">Try these location searches:</p>
              <ul className="text-sm space-y-1">
                <li>• <strong>Zip Codes:</strong> &quot;33139&quot;, &quot;33019&quot;, &quot;33487&quot;</li>
                <li>• <strong>Cities:</strong> &quot;Miami Beach, FL&quot;, &quot;Boca Raton&quot;, &quot;Hollywood&quot;</li>
                <li>• <strong>Addresses:</strong> &quot;123 Main St&quot;, &quot;456 Oak Avenue&quot;</li>
                <li>• <strong>Any Location:</strong> Type any address or place name</li>
              </ul>
              
              <p className="text-sm font-semibold mt-3 mb-2">Restaurant searches:</p>
              <ul className="text-sm space-y-1">
                <li>• <strong>Names:</strong> &quot;Pizza&quot;, &quot;Sushi&quot;, &quot;Burger&quot;</li>
                <li>• <strong>Filters:</strong> &quot;ORB Certified&quot;, &quot;Meat Restaurants&quot;</li>
              </ul>
            </div>
          </div>

          <div>
            <h2 className="text-lg font-semibold mb-3">✨ New Features</h2>
            <div className="bg-green-50 p-4 rounded-lg">
              <ul className="text-sm space-y-1">
                <li>✅ <strong>Google Places Autocomplete:</strong> Real-time location suggestions</li>
                <li>✅ <strong>Smart Detection:</strong> Automatically detects location vs restaurant searches</li>
                <li>✅ <strong>Dynamic Search:</strong> "Search for any location" option appears for unknown places</li>
                <li>✅ <strong>Enhanced Suggestions:</strong> More cities, zip codes, and popular locations</li>
                <li>✅ <strong>Real-time Geocoding:</strong> Converts addresses to coordinates instantly</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 