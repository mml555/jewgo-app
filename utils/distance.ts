export interface Location {
  latitude: number;
  longitude: number;
}

export interface RestaurantWithDistance {
  restaurant: any;
  distance: number;
}

// Calculate distance between two points using Haversine formula
export function calculateDistance(
  lat1: number,
  lon1: number,
  lat2: number,
  lon2: number
): number {
  const R = 6371; // Radius of the Earth in kilometers
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
    Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  const distance = R * c; // Distance in kilometers
  return distance;
}

// Sort restaurants by distance from user location
export function sortRestaurantsByDistance(
  restaurants: any[],
  userLocation: Location | null
): any[] {
  if (!userLocation) return restaurants;

  const restaurantsWithDistance: RestaurantWithDistance[] = restaurants
    .filter(restaurant => restaurant.latitude && restaurant.longitude)
    .map(restaurant => ({
      restaurant,
      distance: calculateDistance(
        userLocation.latitude,
        userLocation.longitude,
        parseFloat(restaurant.latitude.toString()),
        parseFloat(restaurant.longitude.toString())
      )
    }))
    .sort((a, b) => a.distance - b.distance);

  return restaurantsWithDistance.map(item => item.restaurant);
}

// Format distance for display (in miles for US market)
export function formatDistance(distance: number): string {
  // Convert km to miles
  const miles = distance * 0.621371;
  
  if (miles < 0.1) {
    return `${Math.round(miles * 5280)}ft`; // Convert to feet
  } else if (miles < 1) {
    return `${Math.round(miles * 10) / 10}mi`; // Show as 0.1, 0.2, etc.
  } else if (miles < 10) {
    return `${miles.toFixed(1)}mi`; // Show as 1.2mi, 2.5mi, etc.
  } else {
    return `${Math.round(miles)}mi`; // Show as 12mi, 25mi, etc.
  }
}

// Calculate distance for a single restaurant
export function getRestaurantDistance(
  restaurant: any,
  userLocation: Location | null
): number | null {
  if (!userLocation || !restaurant.latitude || !restaurant.longitude) {
    return null;
  }
  
  return calculateDistance(
    userLocation.latitude,
    userLocation.longitude,
    parseFloat(restaurant.latitude.toString()),
    parseFloat(restaurant.longitude.toString())
  );
}

// Get restaurants within a certain radius
export function getRestaurantsWithinRadius(
  restaurants: any[],
  userLocation: Location,
  radiusKm: number
): any[] {
  return restaurants.filter(restaurant => {
    if (!restaurant.latitude || !restaurant.longitude) return false;
    
    const distance = calculateDistance(
      userLocation.latitude,
      userLocation.longitude,
      parseFloat(restaurant.latitude.toString()),
      parseFloat(restaurant.longitude.toString())
    );
    
    return distance <= radiusKm;
  });
} 