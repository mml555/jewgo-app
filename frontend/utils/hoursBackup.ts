/**
 * Hours Backup Utilities
 * =====================
 * 
 * Frontend utilities for fetching restaurant hours using Google Places API
 * as a backup when hours data is missing from the database.
 */

export interface HoursFetchResponse {
  success: boolean;
  message: string;
  hours?: string;
  restaurant_id?: number;
  restaurant_name?: string;
  error?: string;
}

export interface BulkHoursFetchResponse {
  success: boolean;
  message: string;
  updated?: number;
  total_checked?: number;
  limit_used?: number;
  error?: string;
}

/**
 * Fetch hours for a specific restaurant using Google Places API
 */
export async function fetchRestaurantHours(restaurantId: number): Promise<HoursFetchResponse> {
  try {
    const response = await fetch(`/api/restaurants/${restaurantId}/fetch-hours`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();

    if (response.ok) {
      return {
        success: true,
        message: data.message,
        hours: data.hours,
        restaurant_id: data.restaurant_id,
        restaurant_name: data.restaurant_name,
      };
    } else {
      return {
        success: false,
        message: data.message || 'Failed to fetch hours',
        error: data.error,
        restaurant_id: restaurantId,
      };
    }
  } catch (error) {
    console.error('Error fetching restaurant hours:', error);
    return {
      success: false,
      message: 'Network error while fetching hours',
      error: error instanceof Error ? error.message : 'Unknown error',
      restaurant_id: restaurantId,
    };
  }
}

/**
 * Fetch hours for multiple restaurants that don't have them
 */
export async function fetchMissingHours(limit: number = 10): Promise<BulkHoursFetchResponse> {
  try {
    const response = await fetch('/api/restaurants/fetch-missing-hours', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ limit }),
    });

    const data = await response.json();

    if (response.ok) {
      return {
        success: true,
        message: data.message,
        updated: data.updated,
        total_checked: data.total_checked,
        limit_used: data.limit_used,
      };
    } else {
      return {
        success: false,
        message: data.message || 'Failed to fetch missing hours',
        error: data.error,
      };
    }
  } catch (error) {
    console.error('Error fetching missing hours:', error);
    return {
      success: false,
      message: 'Network error while fetching missing hours',
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

/**
 * Ensure restaurant has hours data, fetching from Google Places if missing
 */
export async function ensureRestaurantHours(restaurant: any): Promise<string | null> {
  try {
    // If restaurant already has hours, return them
    if (restaurant.hours_open && restaurant.hours_open.length > 10) {
      return restaurant.hours_open;
    }

    // If restaurant has hours_of_operation but not hours_open, use that
    if (restaurant.hours_of_operation && restaurant.hours_of_operation.length > 10) {
      return restaurant.hours_of_operation;
    }

    // Try to fetch hours from Google Places API
    const result = await fetchRestaurantHours(restaurant.id);
    
    if (result.success && result.hours) {
      return result.hours;
    }

    return null;
  } catch (error) {
    console.error('Error ensuring restaurant hours:', error);
    return null;
  }
}

/**
 * Get a fallback hours display when no hours are available
 */
export function getFallbackHoursDisplay(restaurant: any): string {
  // Check if we have any hours data
  if (restaurant.hours_open && restaurant.hours_open.length > 10) {
    return restaurant.hours_open;
  }
  
  if (restaurant.hours_of_operation && restaurant.hours_of_operation.length > 10) {
    return restaurant.hours_of_operation;
  }
  
  // Return a default message
  return 'Hours not available';
}

/**
 * Format hours for display
 */
export function formatHoursForDisplay(hours: string): string {
  if (!hours || hours.length < 10) {
    return 'Hours not available';
  }
  
  // Clean up the hours string
  return hours.trim();
}

/**
 * Check if restaurant is currently open (basic implementation)
 * This is a simplified check - for production, you'd want more sophisticated logic
 */
export function isRestaurantOpen(hours: string): boolean | null {
  if (!hours || hours.length < 10) {
    return null; // Unknown
  }
  
  try {
    const now = new Date();
    const currentDay = now.toLocaleDateString('en-US', { weekday: 'long' });
    const currentTime = now.toLocaleTimeString('en-US', { 
      hour12: false, 
      hour: '2-digit', 
      minute: '2-digit' 
    });
    
    // Parse hours string to find current day
    const dayMapping: { [key: string]: string } = {
      'Monday': 'Mon',
      'Tuesday': 'Tue',
      'Wednesday': 'Wed',
      'Thursday': 'Thu',
      'Friday': 'Fri',
      'Saturday': 'Sat',
      'Sunday': 'Sun'
    };
    
    const shortDay = dayMapping[currentDay];
    if (!shortDay) return null;
    
    // Find the current day in the hours string
    const dayPattern = new RegExp(`${shortDay}\\s+([^-]+)\\s*-\\s*([^-]+)`, 'i');
    const match = hours.match(dayPattern);
    
    if (!match) return null;
    
    const openTime = match[1].trim();
    const closeTime = match[2].trim();
    
    // Simple time comparison (this is basic - production would need more sophisticated parsing)
    const currentTimeMinutes = parseInt(currentTime.split(':')[0]) * 60 + parseInt(currentTime.split(':')[1]);
    
    // Convert open/close times to minutes (simplified)
    const openMinutes = parseTimeToMinutes(openTime);
    const closeMinutes = parseTimeToMinutes(closeTime);
    
    if (openMinutes === null || closeMinutes === null) return null;
    
    return currentTimeMinutes >= openMinutes && currentTimeMinutes <= closeMinutes;
    
  } catch (error) {
    console.error('Error checking if restaurant is open:', error);
    return null;
  }
}

/**
 * Helper function to parse time string to minutes
 */
function parseTimeToMinutes(timeStr: string): number | null {
  try {
    // Handle various time formats: "11:00 AM", "11:00", "11 AM", etc.
    const cleanTime = timeStr.trim().toLowerCase();
    
    // Remove AM/PM and convert to 24-hour format
    let isPM = cleanTime.includes('pm');
    let timeWithoutAMPM = cleanTime.replace(/[ap]m/g, '').trim();
    
    let hours: number;
    let minutes: number;
    
    if (timeWithoutAMPM.includes(':')) {
      const [hourStr, minuteStr] = timeWithoutAMPM.split(':');
      hours = parseInt(hourStr);
      minutes = parseInt(minuteStr);
    } else {
      hours = parseInt(timeWithoutAMPM);
      minutes = 0;
    }
    
    if (isNaN(hours) || isNaN(minutes)) return null;
    
    // Convert to 24-hour format
    if (isPM && hours !== 12) {
      hours += 12;
    } else if (!isPM && hours === 12) {
      hours = 0;
    }
    
    return hours * 60 + minutes;
    
  } catch (error) {
    console.error('Error parsing time:', timeStr, error);
    return null;
  }
} 