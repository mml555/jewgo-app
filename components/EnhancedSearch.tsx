'use client';

import { useState, useEffect, useRef } from 'react';
import { Restaurant } from '@/types/restaurant';

interface EnhancedSearchProps {
  onSearch: (query: string) => void;
  onResultsUpdate: (results: Restaurant[]) => void;
  placeholder?: string;
}

interface GooglePlace {
  place_id: string;
  name: string;
  formatted_address: string;
  geometry: {
    location: {
      lat: number;
      lng: number;
    };
  };
  types: string[];
  rating?: number;
  user_ratings_total?: number;
  photos?: Array<{
    photo_reference: string;
    height: number;
    width: number;
  }>;
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

export default function EnhancedSearch({ 
  onSearch, 
  onResultsUpdate, 
  placeholder = "Search restaurants, agencies, or dietary preferences..." 
}: EnhancedSearchProps) {
  const [query, setQuery] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [placeSuggestions, setPlaceSuggestions] = useState<PlaceSuggestion[]>([]);
  const [isLoadingPlaces, setIsLoadingPlaces] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const [placesApiError, setPlacesApiError] = useState<string | null>(null);
  const [searchError, setSearchError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);
  const searchTimeoutRef = useRef<NodeJS.Timeout>();
  const placesTimeoutRef = useRef<NodeJS.Timeout>();
  const inputRef = useRef<HTMLInputElement>(null);
  const autocompleteServiceRef = useRef<any>(null);
  const placesServiceRef = useRef<any>(null);

  // Initialize Google Places services
  useEffect(() => {
    const initializeGooglePlaces = () => {
      if (window.google && window.google.maps && window.google.maps.places) {
        try {
          // Try to use the newer AutocompleteSuggestion if available
          if (window.google.maps.places.AutocompleteSuggestion) {
            autocompleteServiceRef.current = new window.google.maps.places.AutocompleteSuggestion();
          } else if (window.google.maps.places.AutocompleteService) {
            // Fallback to AutocompleteService (deprecated but still works)
            autocompleteServiceRef.current = new window.google.maps.places.AutocompleteService();
          } else {
            console.warn('Google Places API not available');
            setPlacesApiError('Places API not available');
            return;
          }
          
          // Create a dummy div for PlacesService (required by Google Maps API)
          const dummyDiv = document.createElement('div');
          placesServiceRef.current = new window.google.maps.places.PlacesService(dummyDiv);
        } catch (error) {
          console.error('Error initializing Google Places:', error);
          setPlacesApiError('Failed to initialize Places API');
        }
      }
    };

    // Check if Google Maps is already loaded
    if (window.google && window.google.maps) {
      initializeGooglePlaces();
    } else {
      // Wait for Google Maps to load
      const checkGoogleMaps = setInterval(() => {
        if (window.google && window.google.maps) {
          initializeGooglePlaces();
          clearInterval(checkGoogleMaps);
        }
      }, 100);

      // Cleanup interval after 10 seconds
      setTimeout(() => {
        clearInterval(checkGoogleMaps);
        if (!autocompleteServiceRef.current) {
          setPlacesApiError('Google Maps failed to load');
        }
      }, 10000);
    }
  }, []);

  // Enhanced search function that combines database and Google Places
  const performEnhancedSearch = async (searchQuery: string) => {
    setIsSearching(true);
    setSearchError(null);
    
    try {
      // 1. Search your database first
      const dbResponse = await fetch(`/api/restaurants?search=${encodeURIComponent(searchQuery)}&limit=50`);
      
      let dbResults: Restaurant[] = [];
      if (dbResponse.ok) {
        const dbData = await dbResponse.json();
        dbResults = dbData.data || [];
      }

      // 2. Search Google Places API for additional restaurants
      let googleResults: Restaurant[] = [];
      if (placesServiceRef.current && searchQuery.length > 2) {
        try {
          const googlePlaces = await searchGooglePlaces(searchQuery);
          googleResults = googlePlaces.map(place => convertGooglePlaceToRestaurant(place));
        } catch (error) {
          console.warn('Google Places search failed:', error);
          // Continue with database results only
        }
      }

      // 3. Combine and deduplicate results
      const combinedResults = combineResults(dbResults, googleResults);
      
      // 4. Update results
      onResultsUpdate(combinedResults);
      
    } catch (error) {
      console.error('Enhanced search error:', error);
      setSearchError('Search failed. Please try again.');
    } finally {
      setIsSearching(false);
    }
  };

  // Search Google Places API
  const searchGooglePlaces = async (searchQuery: string): Promise<GooglePlace[]> => {
    return new Promise((resolve, reject) => {
      if (!placesServiceRef.current) {
        reject(new Error('Places service not available'));
        return;
      }

      const request = {
        query: searchQuery + ' restaurant',
        type: 'restaurant',
        fields: ['place_id', 'name', 'formatted_address', 'geometry', 'types', 'rating', 'user_ratings_total', 'photos']
      };

      placesServiceRef.current.textSearch(request, (results: GooglePlace[], status: any) => {
        if (status === window.google.maps.places.PlacesServiceStatus.OK && results) {
          resolve(results.slice(0, 10)); // Limit to 10 results
        } else {
          reject(new Error(`Places search failed: ${status}`));
        }
      });
    });
  };

  // Convert Google Place to Restaurant format
  const convertGooglePlaceToRestaurant = (place: GooglePlace): Restaurant => {
    return {
      id: parseInt(place.place_id.replace(/\D/g, '')) || Math.floor(Math.random() * 1000000),
      name: place.name,
      address: place.formatted_address,
      city: extractCityFromAddress(place.formatted_address),
      state: extractStateFromAddress(place.formatted_address),
      zip_code: extractZipFromAddress(place.formatted_address),
      phone_number: '',
      website: '',
      certificate_link: '',
      image_url: place.photos && place.photos.length > 0 
        ? `https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=${place.photos[0].photo_reference}&key=${process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY}`
        : '',
      google_listing_url: `https://maps.google.com/?cid=${place.place_id}`,
      certifying_agency: 'Unknown', // Will need to be determined
      kosher_category: 'pareve', // Default to pareve for external restaurants
      is_cholov_yisroel: null,
      is_pas_yisroel: null,
      listing_type: 'restaurant',
      status: 'external',
      hours_of_operation: '',
      hours_open: '',
      short_description: `Restaurant found via Google Places`,
      price_range: '',
      avg_price: '',
      menu_pricing: {},
      min_avg_meal_cost: 0,
      max_avg_meal_cost: 0,
      notes: 'External restaurant - kosher status unknown',
      latitude: place.geometry.location.lat,
      longitude: place.geometry.location.lng,
      specials: [],
      rating: place.rating || 0,
      star_rating: place.rating || 0,
      quality_rating: 0,
      review_count: place.user_ratings_total || 0,
      google_rating: place.rating || 0,
      google_review_count: place.user_ratings_total || 0,
      google_reviews: '[]'
    };
  };

  // Helper functions to extract address components
  const extractCityFromAddress = (address: string): string => {
    const parts = address.split(',');
    return parts.length > 1 ? parts[1].trim() : '';
  };

  const extractStateFromAddress = (address: string): string => {
    const parts = address.split(',');
    if (parts.length > 2) {
      const stateZip = parts[2].trim().split(' ');
      return stateZip[0] || '';
    }
    return '';
  };

  const extractZipFromAddress = (address: string): string => {
    const parts = address.split(',');
    if (parts.length > 2) {
      const stateZip = parts[2].trim().split(' ');
      return stateZip[1] || '';
    }
    return '';
  };

  // Combine and deduplicate results
  const combineResults = (dbResults: Restaurant[], googleResults: Restaurant[]): Restaurant[] => {
    const combined = [...dbResults];
    
    // Add Google results that aren't already in database
    googleResults.forEach(googleRestaurant => {
      const isDuplicate = dbResults.some(dbRestaurant => 
        dbRestaurant.name.toLowerCase() === googleRestaurant.name.toLowerCase() &&
        dbRestaurant.address.toLowerCase() === googleRestaurant.address.toLowerCase()
      );
      
      if (!isDuplicate) {
        combined.push(googleRestaurant);
      }
    });
    
    return combined;
  };

  // Debounced search for restaurants and other content
  useEffect(() => {
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }

    if (query.trim()) {
      searchTimeoutRef.current = setTimeout(() => {
        performEnhancedSearch(query);
        onSearch(query);
      }, 500);
    } else {
      onSearch('');
      onResultsUpdate([]);
    }

    return () => {
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }
    };
  }, [query, onSearch, onResultsUpdate]);

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
    if (!autocompleteServiceRef.current) return;

    setIsLoadingPlaces(true);
    setPlacesApiError(null);

    try {
      // Check if we're using the newer API
      if (autocompleteServiceRef.current.getPlacePredictions) {
        // Use the newer AutocompleteSuggestion API
        const request = {
          input: searchQuery,
          types: ['establishment', 'geocode', 'address'],
          componentRestrictions: { country: 'us' },
        };

        const response = await autocompleteServiceRef.current.getPlacePredictions(request);
        setIsLoadingPlaces(false);
        
        if (response && response.predictions) {
          setPlaceSuggestions(response.predictions);
        } else {
          setPlaceSuggestions([]);
        }
      } else {
        // Fallback to older API
        const request: any = {
          input: searchQuery,
          types: ['establishment', 'geocode', 'address'],
          componentRestrictions: { country: 'us' },
        };

        autocompleteServiceRef.current.getPlacePredictions(request, (predictions: any, status: any) => {
          setIsLoadingPlaces(false);
          if (status === window.google.maps.places.PlacesServiceStatus.OK && predictions) {
            setPlaceSuggestions(predictions);
          } else {
            setPlaceSuggestions([]);
          }
        });
      }
      
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
    onResultsUpdate([]);
    setPlaceSuggestions([]);
    setPlacesApiError(null);
    setSearchError(null);
    setRetryCount(0);
    inputRef.current?.focus();
  };

  const handleSuggestionClick = (suggestion: string) => {
    setQuery(suggestion);
    setShowSuggestions(false);
    setPlaceSuggestions([]);
    inputRef.current?.focus();
  };

  const handlePlaceSuggestionClick = (place: PlaceSuggestion) => {
    const fullDescription = place.description;
    setQuery(fullDescription);
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

  const filteredSuggestions = searchSuggestions.filter(suggestion =>
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
          <div className="absolute inset-y-0 left-0 pl-3 sm:pl-4 flex items-center pointer-events-none">
            <svg className={`h-5 w-5 transition-colors duration-200 ${isFocused ? 'text-jewgo-400' : 'text-neutral-400'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </div>

          {/* Search Input */}
          <input
            ref={inputRef}
            type="text"
            placeholder={placeholder}
            value={query}
            onChange={handleInputChange}
            onFocus={handleFocus}
            onBlur={handleBlur}
            onKeyDown={handleKeyDown}
            className="w-full pl-12 pr-12 py-2.5 sm:py-3 rounded-xl bg-white border border-neutral-300 focus:border-jewgo-400 focus:ring-jewgo-400/20 focus:outline-none transition-all duration-200 shadow-soft text-base"
            autoComplete="off"
          />

          {/* Right Side Actions */}
          <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
            {isSearching && (
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-jewgo-400 mr-2"></div>
            )}
            {query && (
              <button
                type="button"
                onClick={handleClear}
                className="p-1 text-neutral-400 hover:text-jewgo-400 transition-colors duration-200"
                title="Clear search"
              >
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            )}
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

      {/* Search Error */}
      {searchError && (
        <div className="absolute top-full left-0 right-0 mt-1 px-3 py-2 text-sm text-status-error bg-status-error-light rounded-lg border border-status-error">
          {searchError}
        </div>
      )}
    </div>
  );
} 