'use client';

import { useState, useEffect, useRef } from 'react';
import { googlePlacesAPI } from '@/lib/google/places';
import { safeFilter } from '@/utils/validation';

interface SearchBarProps {
  onSearch: (query: string) => void;
  placeholder?: string;
}

interface PlaceSuggestion {
  place_id: string;
  description: string;
  structured_formatting: {
    main_text: string;
    secondary_text: string;
  };
  types: string[];
}

export default function SearchBar({ onSearch, placeholder = "Search restaurants, agencies, or dietary preferences..." }: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [placeSuggestions, setPlaceSuggestions] = useState<PlaceSuggestion[]>([]);
  const [isLoadingPlaces, setIsLoadingPlaces] = useState(false);
  const [placesApiError, setPlacesApiError] = useState<string | null>(null);
  const [searchError, setSearchError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);
  const searchTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const placesTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const autocompleteServiceRef = useRef<any>(null);
  const placesServiceRef = useRef<any>(null);

  // Initialize Google Places services
  useEffect(() => {
    const initializeGooglePlaces = async () => {
      try {
        await googlePlacesAPI.initialize();
        setPlacesApiError(null);
      } catch (error) {
        console.error('Error initializing Google Places:', error);
        setPlacesApiError('Failed to initialize Places API');
      }
    };

    initializeGooglePlaces();
  }, []);

  // Debounced search for restaurants and other content
  useEffect(() => {
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }

    searchTimeoutRef.current = setTimeout(() => {
      onSearch(query);
    }, 300);

    return () => {
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }
    };
  }, [query]); // Removed onSearch from dependencies since it should be stable

  // Debounced Google Places autocomplete
  useEffect(() => {
    if (placesTimeoutRef.current) {
      clearTimeout(placesTimeoutRef.current);
    }

    if (query.length > 2 && autocompleteServiceRef.current && !placesApiError) {
      setIsLoadingPlaces(true);
      setPlaceSuggestions([]);
      placesTimeoutRef.current = setTimeout(() => {
        fetchPlaceSuggestions(query);
      }, 500);
    } else {
      setPlaceSuggestions([]);
      setIsLoadingPlaces(false);
    }

    return () => {
      if (placesTimeoutRef.current) {
        clearTimeout(placesTimeoutRef.current);
      }
    };
  }, [query, placesApiError]);

  const fetchPlaceSuggestions = async (searchQuery: string) => {
    setIsLoadingPlaces(true);
    setPlacesApiError(null);

    try {
      const predictions = await googlePlacesAPI.getPlacePredictions(searchQuery, {
        types: ['establishment', 'geocode', 'address'],
        country: 'us'
      });
      
      setIsLoadingPlaces(false);
      setPlaceSuggestions(predictions);
      setRetryCount(0); // Reset retry count on success
    } catch (error) {
      console.error('Error fetching place suggestions:', error);
      setIsLoadingPlaces(false);
      setPlaceSuggestions([]);
      
      // Enhanced error handling with retry logic
      const errorMessage = error instanceof Error ? error.message : 'Failed to fetch suggestions';
      setPlacesApiError(errorMessage);
      
      // Auto-retry logic for network errors
      if (retryCount < 2 && errorMessage.includes('network')) {
        setRetryCount(prev => prev + 1);
        setTimeout(() => {
          fetchPlaceSuggestions(searchQuery);
        }, 1000 * (retryCount + 1)); // Exponential backoff
      }
    }
  };

  const handleClear = () => {
    setQuery('');
    onSearch('');
    setPlaceSuggestions([]);
    setPlacesApiError(null);
    setSearchError(null);
    setRetryCount(0);
    inputRef.current?.focus();
  };

  const handleSuggestionClick = (suggestion: string) => {
    setQuery(suggestion);
    onSearch(suggestion);
    setShowSuggestions(false);
    setPlaceSuggestions([]);
    inputRef.current?.focus();
  };

  const handlePlaceSuggestionClick = (place: PlaceSuggestion) => {
    const fullDescription = place.description;
    setQuery(fullDescription);
    onSearch(fullDescription);
    setShowSuggestions(false);
    setPlaceSuggestions([]);
    inputRef.current?.focus();
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    setShowSuggestions(value.length > 0);
    setPlacesApiError(null); // Clear error when user types
  };

  const handleFocus = () => {
    setIsFocused(true);
    if (query.length > 0) {
      setShowSuggestions(true);
    }
  };

  const handleBlur = () => {
    setIsFocused(false);
    // Delay hiding suggestions to allow for clicks
    setTimeout(() => {
      setShowSuggestions(false);
      setPlaceSuggestions([]);
    }, 200);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      setShowSuggestions(false);
      setPlaceSuggestions([]);
      inputRef.current?.blur();
    }
  };

  const searchSuggestions = [
    { label: 'ORB Certified', value: 'ORB', icon: '✓', color: 'bg-agency-orb' },
    { label: 'KM Certified', value: 'KM', icon: '🥛', color: 'bg-agency-km' },
    { label: 'KDM Certified', value: 'KDM', icon: '🍽️', color: 'bg-agency-kdm' },
    { label: 'Diamond K', value: 'Diamond K', icon: '💎', color: 'bg-agency-diamond-k' },
    { label: 'Meat Restaurants', value: 'meat', icon: '🥩', color: 'bg-kosher-meat' },
    { label: 'Dairy Restaurants', value: 'dairy', icon: '🥛', color: 'bg-kosher-dairy' },
    { label: 'Pareve Restaurants', value: 'pareve', icon: '🥬', color: 'bg-kosher-pareve' },
    { label: 'Miami Beach', value: 'Miami Beach', icon: '🏖️', color: 'bg-accent-blue' },
    { label: 'Hollywood FL', value: 'Hollywood', icon: '🎬', color: 'bg-accent-orange' },
    { label: 'Boca Raton', value: 'Boca', icon: '🌴', color: 'bg-accent-green' }
  ];

  const filteredSuggestions = safeFilter(searchSuggestions, (suggestion: any) =>
    suggestion.label.toLowerCase().includes(query.toLowerCase()) ||
    suggestion.value.toLowerCase().includes(query.toLowerCase())
  );

  const hasPlaceSuggestions = placeSuggestions.length > 0;
  const hasSearchSuggestions = filteredSuggestions.length > 0;
  const showSuggestionsPanel = showSuggestions && (query.length > 0 || isFocused);

  return (
    <div className="relative">
      <form onSubmit={(e) => e.preventDefault()}>
        <div className="relative">
          {/* Search Icon */}
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <svg className={`h-5 w-5 transition-colors duration-200 ${isFocused ? 'text-green-500' : 'text-gray-500'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </div>

          {/* Search Input */}
          <input
            ref={inputRef}
            type="text"
            placeholder="Find your Eatery"
            value={query}
            onChange={handleInputChange}
            onFocus={handleFocus}
            onBlur={handleBlur}
            onKeyDown={handleKeyDown}
            className="w-full pl-12 pr-12 py-3 rounded-full bg-white border border-gray-200 focus:border-green-500 focus:ring-green-500/20 focus:outline-none transition-all duration-200 shadow-md text-base"
            autoComplete="off"
          />

          {/* Right Side Actions */}
          <div className="absolute inset-y-0 right-0 pr-4 flex items-center">
            {query && (
              <button
                type="button"
                onClick={handleClear}
                className="p-1 text-gray-400 hover:text-green-500 transition-colors duration-200"
                title="Clear search"
              >
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            )}
            {/* Filter Icon */}
            <button
              type="button"
              className="p-1 text-gray-500 hover:text-green-500 transition-colors duration-200 ml-2"
              title="Filters"
            >
              <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4"></path>
              </svg>
            </button>
          </div>
        </div>
      </form>

      {/* Enhanced Search Suggestions with Google Places */}
      {showSuggestionsPanel && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-neutral-200 rounded-xl shadow-strong z-50 animate-fade-in-up max-h-80 overflow-y-auto">
          <div className="p-2">
            {query.length > 0 && (
              <div className="text-xs text-neutral-500 px-3 py-1 border-b border-neutral-100 mb-2">
                Search suggestions for "{query}"
              </div>
            )}
            
            {/* Google Places Suggestions */}
            {hasPlaceSuggestions && (
              <div className="mb-3">
                <div className="text-xs text-neutral-500 px-3 py-1 mb-2 flex items-center">
                  <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  </svg>
                  Locations & Places
                </div>
                <div className="space-y-1">
                  {placeSuggestions.slice(0, 5).map((place) => (
                    <button
                      key={place.place_id}
                      onClick={() => handlePlaceSuggestionClick(place)}
                      className="w-full text-left px-3 py-2 text-sm text-neutral-700 hover:bg-neutral-50 rounded-lg transition-colors duration-200 flex items-center space-x-3"
                    >
                      <span className="w-2 h-2 bg-accent-blue rounded-full flex-shrink-0"></span>
                      <span className="text-sm">📍</span>
                      <div className="flex-1">
                        <div className="font-medium">{place.structured_formatting.main_text}</div>
                        <div className="text-xs text-neutral-500">{place.structured_formatting.secondary_text}</div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Places API Error */}
            {placesApiError && (
              <div className="px-3 py-2 text-sm text-status-error bg-status-error-light rounded-lg mb-2">
                <div className="flex items-center">
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  {placesApiError}
                </div>
              </div>
            )}

            {/* Loading indicator for places */}
            {isLoadingPlaces && (
              <div className="px-3 py-2 text-sm text-neutral-500 flex items-center">
                <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-jewgo-400 mr-2"></div>
                Searching locations...
              </div>
            )}
            
            {/* Search Suggestions */}
            {hasSearchSuggestions && (
              <div>
                <div className="text-xs text-neutral-500 px-3 py-1 mb-2 flex items-center">
                  <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                  </svg>
                  Quick Searches
                </div>
                <div className="space-y-1">
                  {filteredSuggestions.map((suggestion, index) => (
                    <button
                      key={index}
                      onClick={() => handleSuggestionClick(suggestion.value)}
                      className="w-full text-left px-3 py-2 text-sm text-neutral-700 hover:bg-neutral-50 rounded-lg transition-colors duration-200 flex items-center space-x-3"
                    >
                      <span className={`w-2 h-2 ${suggestion.color} rounded-full flex-shrink-0`}></span>
                      <span className="text-sm">{suggestion.icon}</span>
                      <span className="flex-1">{suggestion.label}</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* No results */}
            {!hasPlaceSuggestions && !hasSearchSuggestions && !isLoadingPlaces && !placesApiError && query.length > 0 && (
              <div className="px-3 py-2 text-sm text-neutral-500">
                No suggestions found for "{query}"
              </div>
            )}

            {/* Popular searches when no query */}
            {!query && !hasPlaceSuggestions && !hasSearchSuggestions && !placesApiError && (
              <div className="space-y-1">
                <div className="text-xs text-neutral-500 px-3 py-1">Popular searches</div>
                {searchSuggestions.slice(0, 5).map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => handleSuggestionClick(suggestion.value)}
                    className="w-full text-left px-3 py-2 text-sm text-neutral-700 hover:bg-neutral-50 rounded-lg transition-colors duration-200 flex items-center space-x-3"
                  >
                    <span className={`w-2 h-2 ${suggestion.color} rounded-full flex-shrink-0`}></span>
                    <span className="text-sm">{suggestion.icon}</span>
                    <span className="flex-1">{suggestion.label}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
} 