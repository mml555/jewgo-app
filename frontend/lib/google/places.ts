export async function fetchPlaceDetails(place_id: string): Promise<{
  hoursText: string,
  hoursJson: any[],
  timezone: string
}> {
  const res = await fetch(
    `https://maps.googleapis.com/maps/api/place/details/json?place_id=${place_id}&fields=opening_hours,utc_offset_minutes&key=${process.env.GOOGLE_API_KEY}`
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

  static getInstance(): ModernGooglePlacesAPI {
    if (!ModernGooglePlacesAPI.instance) {
      ModernGooglePlacesAPI.instance = new ModernGooglePlacesAPI();
    }
    return ModernGooglePlacesAPI.instance;
  }

  async initialize(): Promise<void> {
    if (this.isInitialized) return;
    
    if (this.initPromise) return this.initPromise;

    this.initPromise = new Promise((resolve, reject) => {
      const checkGoogleMaps = () => {
        if (window.google && window.google.maps && window.google.maps.places) {
          this.isInitialized = true;
          resolve();
        } else {
          setTimeout(checkGoogleMaps, 100);
        }
      };

      // Timeout after 10 seconds
      const timeout = setTimeout(() => {
        reject(new Error('Google Maps failed to load within 10 seconds'));
      }, 10000);

      checkGoogleMaps();
    });

    return this.initPromise;
  }

  async searchPlaces(query: string, options: {
    location?: { lat: number; lng: number };
    radius?: number;
    types?: string[];
    limit?: number;
  } = {}): Promise<any[]> {
    await this.initialize();

    try {
      // Use the new Place API for text search
      const request: google.maps.places.TextSearchRequest = {
        query,
        ...options
      };

      return new Promise((resolve, reject) => {
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

    try {
      const request: google.maps.places.AutocompletionRequest = {
        input,
        types: options.types || ['establishment'],
        location: options.location ? new window.google.maps.LatLng(options.location.lat, options.location.lng) : undefined,
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

    try {
      const request: google.maps.places.PlaceDetailsRequest = {
        placeId,
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