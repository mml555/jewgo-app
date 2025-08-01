

export async function fetchPlaceDetails(place_id: string): Promise<{
  hoursText: string,
  hoursJson: any[],
  timezone: string
}> {
  // Validate place_id parameter
  if (!place_id || typeof place_id !== 'string' || place_id.trim() === '') {
    console.warn('Invalid place_id provided to fetchPlaceDetails:', place_id);
    return {
      hoursText: '',
      hoursJson: [],
      timezone: 'UTC'
    };
  }

  const res = await fetch(
    `https://maps.googleapis.com/maps/api/place/details/json?place_id=${place_id.trim()}&fields=opening_hours,utc_offset_minutes&key=${process.env.GOOGLE_API_KEY}`
  );
  const data = await res.json();
  const periods = data.result.opening_hours?.periods || [];
  const weekdayText = data.result.opening_hours?.weekday_text || [];
  const offset = data.result.utc_offset_minutes;

  return {
    hoursText: weekdayText.join("\n"),
    hoursJson: periods,
    timezone: offsetToTimezone(offset)
  };
}

function offsetToTimezone(offset: number): string {
  // Simple mapping for common US timezones
  switch (offset) {
    case -300: return 'America/New_York';
    case -360: return 'America/Chicago';
    case -420: return 'America/Denver';
    case -480: return 'America/Los_Angeles';
    default: return 'UTC';
  }
}

// Modern Google Places API wrapper using the new Place API
export class ModernGooglePlacesAPI {
  private static instance: ModernGooglePlacesAPI;
  private isInitialized = false;
  private initPromise: Promise<void> | null = null;
  private lastInitAttempt = 0;
  private readonly INIT_RETRY_DELAY = 60000; // 1 minute between retry attempts
  private cache = new Map<string, { data: any; timestamp: number; ttl: number }>();
  private readonly DEFAULT_CACHE_TTL = 300000; // 5 minutes default cache time

  static getInstance(): ModernGooglePlacesAPI {
    if (!ModernGooglePlacesAPI.instance) {
      ModernGooglePlacesAPI.instance = new ModernGooglePlacesAPI();
    }
    return ModernGooglePlacesAPI.instance;
  }

  // Get cached data if still valid
  private getCachedData(key: string): any | null {
    const cached = this.cache.get(key);
    if (cached && Date.now() - cached.timestamp < cached.ttl) {
      return cached.data;
    }
    if (cached) {
      this.cache.delete(key); // Remove expired cache
    }
    return null;
  }

  // Set cache data
  private setCachedData(key: string, data: any, ttl: number = this.DEFAULT_CACHE_TTL): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl
    });
  }

  // Clear expired cache entries
  private cleanupCache(): void {
    const now = Date.now();
    const keysToDelete: string[] = [];
    
    this.cache.forEach((cached, key) => {
      if (now - cached.timestamp > cached.ttl) {
        keysToDelete.push(key);
      }
    });
    
    keysToDelete.forEach(key => {
      this.cache.delete(key);
    });
  }

  async initialize(): Promise<void> {
    // If already initialized, return immediately
    if (this.isInitialized) {
      console.log('Google Places API already initialized, skipping...');
      return;
    }
    
    // If there's an ongoing initialization, return that promise
    if (this.initPromise) {
      console.log('Google Places API initialization already in progress, waiting...');
      return this.initPromise;
    }

    // Check if we should retry initialization (avoid too frequent attempts)
    const now = Date.now();
    if (now - this.lastInitAttempt < this.INIT_RETRY_DELAY) {
      console.log('Google Places API initialization retry too soon, skipping...');
      return;
    }

    this.lastInitAttempt = now;
    console.log('Initializing Google Places API...');

    this.initPromise = new Promise((resolve, reject) => {
      let checkCount = 0;
      const maxChecks = 300; // 30 seconds with 100ms intervals
      
      const checkGoogleMaps = () => {
        checkCount++;
        
        if (window.google && window.google.maps && window.google.maps.places) {
          this.isInitialized = true;
          console.log('Google Places API initialized successfully');
          resolve();
          return;
        }
        
        if (checkCount >= maxChecks) {
          const error = 'Google Maps failed to load within 30 seconds. Please check your internet connection and try again.';
          console.error(error);
          reject(new Error(error));
          return;
        }
        
        // Continue checking
        setTimeout(checkGoogleMaps, 100);
      };

      // Check if API key is available
      const apiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;
      if (!apiKey) {
        const error = 'Google Maps API key is missing. Please set NEXT_PUBLIC_GOOGLE_MAPS_API_KEY in your environment variables.';
        console.error(error);
        reject(new Error(error));
        return;
      }

      // Start checking for Google Maps availability
      checkGoogleMaps();
    });

    try {
      await this.initPromise;
    } catch (error) {
      // Reset initialization state on error so it can be retried
      this.isInitialized = false;
      this.initPromise = null;
      throw error;
    }

    return this.initPromise;
  }

  // Method to reset initialization state (useful for testing or manual refresh)
  resetInitialization(): void {
    this.isInitialized = false;
    this.initPromise = null;
    this.lastInitAttempt = 0;
    console.log('Google Places API initialization state reset');
  }

  // Method to check if API is ready
  isReady(): boolean {
    return this.isInitialized && !!(window.google && window.google.maps && window.google.maps.places);
  }

  // Method to clear cache
  clearCache(): void {
    this.cache.clear();
    console.log('Google Places API cache cleared');
  }

  // Method to get cache statistics
  getCacheStats(): { size: number; keys: string[] } {
    this.cleanupCache();
    return {
      size: this.cache.size,
      keys: Array.from(this.cache.keys())
    };
  }

  async searchPlaces(query: string, options: {
    location?: { lat: number; lng: number };
    radius?: number;
    types?: string[];
    limit?: number;
  } = {}): Promise<any[]> {
    await this.initialize();

    // Validate query parameter
    if (!query || typeof query !== 'string' || query.trim() === '') {
      console.warn('Invalid query provided to searchPlaces:', query);
      return [];
    }

    try {
      // Create cache key based on search parameters
      const cacheKey = `search:${query}:${JSON.stringify(options)}`;
      
      // Check cache first
      const cachedResult = this.getCachedData(cacheKey);
      if (cachedResult) {
        console.log('Using cached search result for:', query);
        return cachedResult;
      }

      // Use the new Place API for text search
      const request: google.maps.places.TextSearchRequest = {
        query: query.trim(),
        location: options.location ? new google.maps.LatLng(options.location.lat, options.location.lng) : undefined,
        radius: options.radius,
        types: options.types
      };

      const results = await new Promise<any[]>((resolve, reject) => {
        // Create a dummy div for the service (required by Google Maps API)
        const dummyDiv = document.createElement('div');
        
        // Use the new Place API if available, fallback to PlacesService
        if (window.google.maps.places.Place) {
          // Modern approach - use Place API
          const placeService = new window.google.maps.places.Place(dummyDiv);
          placeService.textSearch(request, (results, status) => {
            if (status === window.google.maps.places.PlacesServiceStatus.OK && results) {
              resolve(results.slice(0, options.limit || 20));
            } else {
              resolve([]);
            }
          });
        } else {
          // Fallback to PlacesService (deprecated but still works)
          const placesService = new window.google.maps.places.PlacesService(dummyDiv);
          placesService.textSearch(request, (results, status) => {
            if (status === window.google.maps.places.PlacesServiceStatus.OK && results) {
              resolve(results.slice(0, options.limit || 20));
            } else {
              resolve([]);
            }
          });
        }
      });

      // Cache the results
      this.setCachedData(cacheKey, results, 300000); // Cache for 5 minutes
      console.log('Cached search result for:', query);

      return results;
    } catch (error) {
      console.error('Error searching places:', error);
      return [];
    }
  }

  async getPlacePredictions(input: string, options: {
    types?: string[];
    location?: { lat: number; lng: number };
    radius?: number;
    country?: string;
  } = {}): Promise<google.maps.places.AutocompletePrediction[]> {
    await this.initialize();

    // Validate input parameter
    if (!input || typeof input !== 'string' || input.trim() === '') {
      console.warn('Invalid input provided to getPlacePredictions:', input);
      return [];
    }

    try {
      const request: google.maps.places.AutocompletionRequest = {
        input: input.trim(),
        types: options.types || ['establishment'],
        location: options.location ? new google.maps.LatLng(options.location.lat, options.location.lng) : undefined,
        radius: options.radius,
        componentRestrictions: options.country ? { country: options.country } : undefined
      };

      return new Promise((resolve, reject) => {
        // Use AutocompleteSuggestion if available (newer API)
        if (window.google.maps.places.AutocompleteSuggestion) {
          const autocompleteService = new window.google.maps.places.AutocompleteSuggestion();
          autocompleteService.getPlacePredictions(request)
            .then((response) => {
              resolve(response.predictions || []);
            })
            .catch((error) => {
              console.error('AutocompleteSuggestion error:', error);
              resolve([]);
            });
        } else if (window.google.maps.places.AutocompleteService) {
          // Fallback to AutocompleteService
          const autocompleteService = new window.google.maps.places.AutocompleteService();
          autocompleteService.getPlacePredictions(request, (predictions, status) => {
            if (status === window.google.maps.places.PlacesServiceStatus.OK && predictions) {
              resolve(predictions);
            } else {
              resolve([]);
            }
          });
        } else {
          resolve([]);
        }
      });
    } catch (error) {
      console.error('Error getting place predictions:', error);
      return [];
    }
  }

  async getPlaceDetails(placeId: string, fields: string[] = ['name', 'formatted_address', 'geometry', 'rating', 'user_ratings_total', 'photos', 'opening_hours', 'website', 'formatted_phone_number', 'price_level']): Promise<any> {
    await this.initialize();

    // Validate placeId parameter
    if (!placeId || typeof placeId !== 'string' || placeId.trim() === '') {
      console.warn('Invalid placeId provided to getPlaceDetails:', placeId);
      return null;
    }

    try {
      const request: google.maps.places.PlaceDetailsRequest = {
        placeId: placeId.trim(),
        fields
      };

      return new Promise((resolve, reject) => {
        const dummyDiv = document.createElement('div');
        
        // Use Place API if available, fallback to PlacesService
        if (window.google.maps.places.Place) {
          const placeService = new window.google.maps.places.Place(dummyDiv);
          placeService.getDetails(request, (result, status) => {
            if (status === window.google.maps.places.PlacesServiceStatus.OK && result) {
              resolve(result);
            } else {
              resolve(null);
            }
          });
        } else {
          const placesService = new window.google.maps.places.PlacesService(dummyDiv);
          placesService.getDetails(request, (result, status) => {
            if (status === window.google.maps.places.PlacesServiceStatus.OK && result) {
              resolve(result);
            } else {
              resolve(null);
            }
          });
        }
      });
    } catch (error) {
      console.error('Error getting place details:', error);
      return null;
    }
  }
}

// Export a singleton instance
export const googlePlacesAPI = ModernGooglePlacesAPI.getInstance();

// Legacy function for backward compatibility
export async function searchGooglePlaces(query: string, options: {
  location?: { lat: number; lng: number };
  radius?: number;
  types?: string[];
  limit?: number;
} = {}): Promise<any[]> {
  return googlePlacesAPI.searchPlaces(query, options);
}