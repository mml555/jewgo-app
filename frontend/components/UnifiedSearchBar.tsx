'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Search, MapPin, X } from 'lucide-react';
import { safeFilter } from '@/utils/validation';

interface UserLocation {
  latitude: number;
  longitude: number;
  accuracy?: number;
}

interface UnifiedSearchBarProps {
  onRestaurantSearch: (query: string) => void;
  onLocationSearch: (location: UserLocation, address: string) => void;
  onUseCurrentLocation: () => void;
  placeholder?: string;
  restaurants?: any[];
}

export default function UnifiedSearchBar({ 
  onRestaurantSearch, 
  onLocationSearch, 
  onUseCurrentLocation,
  placeholder = "Search restaurants, locations, cities, or zip codes...",
  restaurants = []
}: UnifiedSearchBarProps) {
  const [query, setQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);

  // Check if Google Maps API is loaded
  const isGoogleMapsLoaded = () => {
    return typeof window !== 'undefined' && 
           window.google && 
           window.google.maps && 
           window.google.maps.Geocoder;
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    
    // Generate suggestions based on input
    if (value.trim().length > 2) {
      const filteredSuggestions = safeFilter(restaurants, (restaurant: any) => 
        (restaurant.name?.toLowerCase().includes(value.toLowerCase()) || false) ||
        (restaurant.address?.toLowerCase().includes(value.toLowerCase()) || false) ||
        (restaurant.city?.toLowerCase().includes(value.toLowerCase()) || false)
      )
        .map(restaurant => restaurant.name || 'Unknown Restaurant')
        .slice(0, 5);
      
      setSuggestions(filteredSuggestions);
      setShowSuggestions(true);
    } else {
      setShowSuggestions(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      if (query.trim()) {
        handleSmartSearch();
      }
    }
  };

  const handleLocationSearch = async () => {
    if (!query.trim()) return;
    
    console.log('Starting location search for:', query);
    setIsSearching(true);
    
    try {
      if (!isGoogleMapsLoaded()) {
        console.error('Google Maps API not loaded');
        // Fallback: just search restaurants
        onRestaurantSearch(query);
        return;
      }
      
      const geocoder = new window.google.maps.Geocoder();
      console.log('Geocoding address:', query);
      const result = await geocoder.geocode({ address: query });
      
      console.log('Geocoding result:', result);
      
      if (result.results[0]) {
        const location = result.results[0].geometry.location;
        const userLocation: UserLocation = {
          latitude: location.lat(),
          longitude: location.lng()
        };
        console.log('Location found:', userLocation);
        onLocationSearch(userLocation, query);
      } else {
        console.log('No results found for address:', query);
        // Fallback: search restaurants
        onRestaurantSearch(query);
      }
    } catch (error) {
      console.error('Error in location search:', error);
      // Fallback: search restaurants
      onRestaurantSearch(query);
    } finally {
      setIsSearching(false);
      setShowSuggestions(false);
    }
  };

  const handleSmartSearch = () => {
    if (!query.trim()) return;
    
    // Check if it looks like a location (contains common location keywords)
    const locationKeywords = ['street', 'avenue', 'road', 'drive', 'lane', 'boulevard', 'way', 'plaza', 'square', 'park'];
    const isLocationQuery = locationKeywords.some(keyword => 
      query.toLowerCase().includes(keyword)
    ) || /\d/.test(query); // Contains numbers (like addresses)
    
    if (isLocationQuery && isGoogleMapsLoaded()) {
      handleLocationSearch();
    } else {
      onRestaurantSearch(query);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setQuery(suggestion);
    setShowSuggestions(false);
    onRestaurantSearch(suggestion);
  };

  const handleClear = () => {
    setQuery('');
    setShowSuggestions(false);
    setSuggestions([]);
    if (inputRef.current) {
      inputRef.current.focus();
    }
  };

  return (
    <div className="relative w-full">
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Search className="h-5 w-5 text-gray-400" />
        </div>
        
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          className="block w-full pl-10 pr-20 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent bg-white shadow-sm"
        />
        
        {query && (
          <button
            onClick={handleClear}
            className="absolute inset-y-0 right-16 pr-3 flex items-center"
          >
            <X className="h-5 w-5 text-gray-400 hover:text-gray-600" />
          </button>
        )}
        
        <button
          onClick={onUseCurrentLocation}
          className="absolute inset-y-0 right-0 pr-3 flex items-center"
          title="Use current location"
        >
          <MapPin className="h-5 w-5 text-jewgo-primary hover:text-jewgo-primary-dark" />
        </button>
      </div>

      {/* Suggestions dropdown */}
      {showSuggestions && suggestions.length > 0 && (
        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
          {suggestions.map((suggestion, index) => (
            <button
              key={index}
              onClick={() => handleSuggestionClick(suggestion)}
              className="w-full px-4 py-2 text-left hover:bg-gray-100 focus:bg-gray-100 focus:outline-none"
            >
              {suggestion}
            </button>
          ))}
        </div>
      )}

      {/* Loading indicator */}
      {isSearching && (
        <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-75 rounded-lg">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-jewgo-primary"></div>
        </div>
      )}
    </div>
  );
} 