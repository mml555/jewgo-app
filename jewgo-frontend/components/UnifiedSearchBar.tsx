'use client';

import { useState, useEffect, useRef } from 'react';

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
  const inputRef = useRef<HTMLInputElement>(null);
  const autocompleteRef = useRef<any>(null);

  // Initialize Google Places Autocomplete
  useEffect(() => {
    const initializeWhenReady = () => {
      if (typeof window !== 'undefined' && window.google && window.google.maps && window.google.maps.places && inputRef.current) {
        initializePlacesAutocomplete();
      } else {
        // Retry after a short delay if Google Maps API is not yet loaded
        setTimeout(initializeWhenReady, 100);
      }
    };

    initializeWhenReady();
  }, []);

  // Initialize Google Places Autocomplete for location search
  const initializePlacesAutocomplete = () => {
    if (!window.google || !window.google.maps || !window.google.maps.places) {
      console.log('Google Places API not loaded');
      return;
    }

    try {
      if (!inputRef.current) {
        console.log('Input ref not available');
        return;
      }

      // Store reference to autocomplete
      autocompleteRef.current = new window.google.maps.places.Autocomplete(inputRef.current, {
        types: ['geocode', 'establishment'],
        componentRestrictions: { country: 'us' },
        fields: ['formatted_address', 'geometry', 'name', 'place_id']
      });

      autocompleteRef.current.addListener('place_changed', () => {
        const place = autocompleteRef.current.getPlace();
        console.log('Google Places place selected:', place);
        
        if (place.geometry && place.geometry.location) {
          const location: UserLocation = {
            latitude: place.geometry.location.lat(),
            longitude: place.geometry.location.lng()
          };
          
          console.log('Calling onLocationSearch with:', location, place.formatted_address);
          onLocationSearch(location, place.formatted_address || place.name || '');
          setQuery(place.formatted_address || place.name || '');
        }
      });

      console.log('Google Places Autocomplete initialized');
    } catch (error) {
      console.error('Error initializing Google Places Autocomplete:', error);
    }
  };

  // Check if Google Maps API is loaded
  const isGoogleMapsLoaded = () => {
    return typeof window !== 'undefined' && 
           window.google && 
           window.google.maps && 
           window.google.maps.Geocoder &&
           window.google.maps.places;
  };







  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
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
      if (!window.google || !window.google.maps || !window.google.maps.Geocoder) {
        console.error('Google Maps API not loaded');
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
      }
    } catch (error) {
      console.error('Geocoding error:', error);
    } finally {
      setIsSearching(false);
    }
  };

  const handleSmartSearch = () => {
    if (!query.trim()) return;
    
    console.log('Search button clicked with query:', query);
    
    // Check if it looks like a location search (zip code, city, address)
    const isLocationSearch = 
      query.match(/^\d{5}$/) || // 5-digit zip code
      query.match(/^\d{3}\s\d{2}$/) || // 3+2 zip code format
      query.includes(',') || // Contains comma (city, state)
      query.match(/^(street|avenue|road|drive|lane|blvd|st|ave|rd|dr|ln|blvd|way|plaza|circle|court|ct)/i) || // Street address
      query.match(/^(miami|hollywood|boca|fort lauderdale|aventura|doral|kendall|hialeah|coral gables|south beach|north beach|mid beach|brickell|wynwood|design district|little havana|coconut grove|key biscayne|sunny isles|bal harbour|surfside|bay harbor|north miami|north miami beach|miami gardens|op locka|miami lakes|weston|plantation|tamarac|pembroke pines|miramar|sunrise|lauderdale lakes|lauderhill|margate|coral springs|parkland|lighthouse point|deerfield beach|delray beach|boynton beach|lake worth|west palm beach|palm beach gardens|jupiter|tequesta|palm city|stuart|port st lucie|vero beach|melbourne|orlando|tampa|naples|fort myers|sarasota|bradenton|clearwater|st petersburg|gainesville|jacksonville|tallahassee|pensacola|panama city|destin|fort walton beach|daytona beach|cocoa beach|space coast|treasure coast|gold coast)/i) || // Common Florida cities
      query.match(/^\d+\s+[a-zA-Z]/) || // Number followed by street name
      query.match(/^(north|south|east|west|n|s|e|w)\s+[a-zA-Z]/i) || // Directional addresses
      query.match(/^(fl|florida)$/i); // State abbreviation
    
    console.log('Is location search:', isLocationSearch);
    
    if (isLocationSearch) {
      console.log('Executing location search...');
      handleLocationSearch();
    } else {
      console.log('Executing restaurant search...');
      // Treat as restaurant search
      onRestaurantSearch(query);
    }
  };



  const handleClear = () => {
    setQuery('');
    onRestaurantSearch('');
    inputRef.current?.focus();
  };

  return (
    <div className="relative">
      <div className="relative">
        {/* Search Icon */}
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
        </div>

        {/* Search Input */}
        <input
          ref={inputRef}
          type="text"
          placeholder={isGoogleMapsLoaded() ? placeholder : "Loading maps..."}
          value={query}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          className="w-full pl-12 pr-24 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent transition-all duration-200"
          autoComplete="off"
          disabled={!isGoogleMapsLoaded()}
        />

        {/* Right Side Actions */}
        <div className="absolute inset-y-0 right-0 pr-3 flex items-center space-x-2">
          {query && (
            <button
              type="button"
              onClick={handleClear}
              className="p-1 text-gray-400 hover:text-jewgo-primary transition-colors duration-200"
              title="Clear search"
            >
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          )}
          
          {/* Location Button */}
          <button
            type="button"
            onClick={onUseCurrentLocation}
            className="p-1 text-green-600 hover:text-green-800 transition-colors duration-200"
            title="Use current location"
          >
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </button>

          {/* Search Button */}
          <button
            type="button"
            onClick={() => query.trim() && handleSmartSearch()}
            disabled={isSearching || !query.trim() || !isGoogleMapsLoaded()}
            className="p-1 text-gray-400 hover:text-jewgo-primary transition-colors duration-200 disabled:text-gray-300"
            title={!isGoogleMapsLoaded() ? "Loading maps..." : "Search"}
          >
            {isSearching ? (
              <svg className="h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            ) : !isGoogleMapsLoaded() ? (
              <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            ) : (
              <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            )}
          </button>
        </div>
      </div>


    </div>
  );
} 