import { Restaurant } from '@/types/restaurant';

const FAVORITES_KEY = 'jewgo_favorites';

export interface FavoriteRestaurant extends Restaurant {
  addedAt: string;
  notes?: string;
}

// Get all favorites from localStorage
export function getFavorites(): FavoriteRestaurant[] {
  if (typeof window === 'undefined') return [];
  
  try {
    const stored = localStorage.getItem(FAVORITES_KEY);
    return stored ? JSON.parse(stored) : [];
  } catch (error) {
    console.error('Error reading favorites from localStorage:', error);
    return [];
  }
}

// Add a restaurant to favorites
export function addToFavorites(restaurant: Restaurant, notes?: string): boolean {
  try {
    const favorites = getFavorites();
    const existingIndex = favorites.findIndex(fav => fav.id === restaurant.id);
    
    if (existingIndex >= 0) {
      // Update existing favorite
      favorites[existingIndex] = {
        ...restaurant,
        addedAt: new Date().toISOString(),
        notes: notes || favorites[existingIndex].notes
      };
    } else {
      // Add new favorite
      favorites.push({
        ...restaurant,
        addedAt: new Date().toISOString(),
        notes
      });
    }
    
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(favorites));
    return true;
  } catch (error) {
    console.error('Error adding to favorites:', error);
    return false;
  }
}

// Remove a restaurant from favorites
export function removeFromFavorites(restaurantId: number): boolean {
  try {
    const favorites = getFavorites();
    const filtered = favorites.filter(fav => fav.id !== restaurantId);
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(filtered));
    return true;
  } catch (error) {
    console.error('Error removing from favorites:', error);
    return false;
  }
}

// Check if a restaurant is in favorites
export function isFavorite(restaurantId: number): boolean {
  const favorites = getFavorites();
  return favorites.some(fav => fav.id === restaurantId);
}

// Update notes for a favorite
export function updateFavoriteNotes(restaurantId: number, notes: string): boolean {
  try {
    const favorites = getFavorites();
    const index = favorites.findIndex(fav => fav.id === restaurantId);
    
    if (index >= 0) {
      favorites[index].notes = notes;
      localStorage.setItem(FAVORITES_KEY, JSON.stringify(favorites));
      return true;
    }
    return false;
  } catch (error) {
    console.error('Error updating favorite notes:', error);
    return false;
  }
}

// Clear all favorites
export function clearAllFavorites(): boolean {
  try {
    localStorage.removeItem(FAVORITES_KEY);
    return true;
  } catch (error) {
    console.error('Error clearing favorites:', error);
    return false;
  }
}

// Export favorites as JSON
export function exportFavorites(): string {
  const favorites = getFavorites();
  return JSON.stringify(favorites, null, 2);
}

// Import favorites from JSON
export function importFavorites(jsonData: string): boolean {
  try {
    const favorites = JSON.parse(jsonData);
    if (Array.isArray(favorites)) {
      localStorage.setItem(FAVORITES_KEY, JSON.stringify(favorites));
      return true;
    }
    return false;
  } catch (error) {
    console.error('Error importing favorites:', error);
    return false;
  }
}

// Get favorites count
export function getFavoritesCount(): number {
  return getFavorites().length;
}

// Search favorites by name or notes
export function searchFavorites(query: string): FavoriteRestaurant[] {
  const favorites = getFavorites();
  const lowerQuery = query.toLowerCase();
  
  return favorites.filter(fav => 
    fav.name.toLowerCase().includes(lowerQuery) ||
    fav.address?.toLowerCase().includes(lowerQuery) ||
    fav.city?.toLowerCase().includes(lowerQuery) ||
    fav.notes?.toLowerCase().includes(lowerQuery)
  );
}

// Get favorites sorted by different criteria
export function getFavoritesSorted(sortBy: 'name' | 'addedAt' | 'distance' = 'addedAt', userLocation?: { lat: number; lng: number }): FavoriteRestaurant[] {
  const favorites = getFavorites();
  
  switch (sortBy) {
    case 'name':
      return favorites.sort((a, b) => a.name.localeCompare(b.name));
    case 'addedAt':
      return favorites.sort((a, b) => new Date(b.addedAt).getTime() - new Date(a.addedAt).getTime());
    case 'distance':
      if (!userLocation) return favorites;
      
      return favorites.sort((a, b) => {
        const distA = calculateDistance(
          userLocation.lat,
          userLocation.lng,
          parseFloat(a.latitude?.toString() || '0'),
          parseFloat(a.longitude?.toString() || '0')
        );
        const distB = calculateDistance(
          userLocation.lat,
          userLocation.lng,
          parseFloat(b.latitude?.toString() || '0'),
          parseFloat(b.longitude?.toString() || '0')
        );
        return distA - distB;
      });
    default:
      return favorites;
  }
}

// Calculate distance between two points (Haversine formula)
function calculateDistance(lat1: number, lon1: number, lat2: number, lon2: number): number {
  const R = 6371; // Radius of the Earth in kilometers
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
    Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
} 