"""
Restaurant Status Calculation Module

This module provides dynamic restaurant status calculation based on business hours
and current time, with proper timezone support. The status is calculated in real-time
rather than stored in the database, as per user requirements.

Features:
- Timezone-aware status calculation
- Support for various business hours formats
- Graceful handling of missing or invalid hours data
- Caching for performance optimization
- Comprehensive logging for debugging
"""

import re
import logging
from datetime import datetime, time, timedelta
from typing import Dict, Optional, Tuple, List
import pytz
from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta

# Configure logging
logger = logging.getLogger(__name__)

class RestaurantStatusCalculator:
    """
    Calculates restaurant open/closed status based on business hours and current time.
    
    This class handles:
    - Timezone conversion based on restaurant location
    - Parsing various business hours formats
    - Real-time status calculation
    - Caching for performance
    """
    
    def __init__(self):
        """Initialize the status calculator."""
        self._cache = {}
        self._cache_ttl = 300  # 5 minutes cache TTL
        
    def get_restaurant_status(self, restaurant_data: Dict) -> Dict[str, any]:
        """
        Calculate the current status of a restaurant based on business hours.
        
        Args:
            restaurant_data: Dictionary containing restaurant information including
                           hours_open, hours, latitude, longitude, city, state
        
        Returns:
            Dictionary with status information:
            {
                'is_open': bool,
                'status': str,  # 'open', 'closed', 'unknown'
                'next_open_time': str,  # ISO format or None
                'current_time_local': str,  # ISO format
                'timezone': str,
                'hours_parsed': bool,
                'status_reason': str
            }
        """
        try:
            # Extract restaurant information
            hours_data = restaurant_data.get('hours_open') or restaurant_data.get('hours')
            latitude = restaurant_data.get('latitude')
            longitude = restaurant_data.get('longitude')
            city = restaurant_data.get('city')
            state = restaurant_data.get('state')
            
            # Determine timezone
            timezone_str = self._get_timezone(latitude, longitude, city, state)
            
            # Get current time in restaurant's timezone
            current_time_local = self._get_current_time_in_timezone(timezone_str)
            
            # Parse business hours
            hours_parsed, parsed_hours = self._parse_business_hours(hours_data)
            
            if not hours_parsed:
                return {
                    'is_open': False,
                    'status': 'unknown',
                    'next_open_time': None,
                    'current_time_local': current_time_local.isoformat(),
                    'timezone': timezone_str,
                    'hours_parsed': False,
                    'status_reason': 'Unable to parse business hours'
                }
            
            # Check if restaurant is currently open
            is_open, next_open_time, status_reason = self._check_if_open(
                parsed_hours, current_time_local
            )
            
            status = 'open' if is_open else 'closed'
            
            return {
                'is_open': is_open,
                'status': status,
                'next_open_time': next_open_time.isoformat() if next_open_time else None,
                'current_time_local': current_time_local.isoformat(),
                'timezone': timezone_str,
                'hours_parsed': True,
                'status_reason': status_reason
            }
            
        except Exception as e:
            logger.error(f"Error calculating restaurant status: {e}")
            return {
                'is_open': False,
                'status': 'unknown',
                'next_open_time': None,
                'current_time_local': datetime.now().isoformat(),
                'timezone': 'UTC',
                'hours_parsed': False,
                'status_reason': f'Error calculating status: {str(e)}'
            }
    
    def _get_timezone(self, latitude: Optional[float], longitude: Optional[float], 
                     city: Optional[str], state: Optional[str]) -> str:
        """
        Determine the timezone for a restaurant based on location.
        
        Args:
            latitude: Restaurant latitude
            longitude: Restaurant longitude
            city: Restaurant city
            state: Restaurant state
            
        Returns:
            Timezone string (e.g., 'America/New_York')
        """
        # If we have coordinates, we could use a geocoding service to get timezone
        # For now, we'll use a simple mapping based on state
        if state and state.strip():
            state_timezones = {
                'NY': 'America/New_York',
                'CA': 'America/Los_Angeles',
                'TX': 'America/Chicago',
                'FL': 'America/New_York',  # Most of Florida is Eastern Time
                'IL': 'America/Chicago',
                'PA': 'America/New_York',
                'OH': 'America/New_York',
                'GA': 'America/New_York',
                'NC': 'America/New_York',
                'MI': 'America/New_York',
                'NJ': 'America/New_York',
                'VA': 'America/New_York',
                'WA': 'America/Los_Angeles',
                'AZ': 'America/Phoenix',
                'CO': 'America/Denver',
                'TN': 'America/Chicago',
                'IN': 'America/New_York',
                'MA': 'America/New_York',
                'MO': 'America/Chicago',
                'MD': 'America/New_York',
                'MN': 'America/Chicago',
                'WI': 'America/Chicago',
                'LA': 'America/Chicago',
                'AL': 'America/Chicago',
                'SC': 'America/New_York',
                'KY': 'America/New_York',
                'OR': 'America/Los_Angeles',
                'CT': 'America/New_York',
                'IA': 'America/Chicago',
                'OK': 'America/Chicago',
                'UT': 'America/Denver',
                'NV': 'America/Los_Angeles',
                'AR': 'America/Chicago',
                'MS': 'America/Chicago',
                'KS': 'America/Chicago',
                'NE': 'America/Chicago',
                'ID': 'America/Boise',
                'NM': 'America/Denver',
                'WV': 'America/New_York',
                'NH': 'America/New_York',
                'ME': 'America/New_York',
                'HI': 'Pacific/Honolulu',
                'RI': 'America/New_York',
                'MT': 'America/Denver',
                'DE': 'America/New_York',
                'SD': 'America/Chicago',
                'ND': 'America/Chicago',
                'AK': 'America/Anchorage',
                'VT': 'America/New_York',
                'WY': 'America/Denver'
            }
            
            timezone = state_timezones.get(state.upper().strip())
            if timezone:
                return timezone
        
        # Default to UTC if we can't determine timezone
        if city or state:
            logger.warning(f"Could not determine timezone for location: {city or 'unknown'}, {state or 'unknown'}")
        return 'UTC'
    
    def _get_current_time_in_timezone(self, timezone_str: str) -> datetime:
        """
        Get current time in the specified timezone.
        
        Args:
            timezone_str: Timezone string (e.g., 'America/New_York')
            
        Returns:
            Current datetime in the specified timezone
        """
        try:
            tz = pytz.timezone(timezone_str)
            return datetime.now(tz)
        except Exception as e:
            logger.error(f"Error getting time in timezone {timezone_str}: {e}")
            return datetime.now(pytz.UTC)
    
    def _parse_business_hours(self, hours_data: Optional[str]) -> Tuple[bool, List[Dict]]:
        """
        Parse business hours from various formats.
        
        Args:
            hours_data: String containing business hours information
            
        Returns:
            Tuple of (success, parsed_hours_list)
        """
        if not hours_data:
            return False, []
        
        try:
            # Common patterns for business hours
            patterns = [
                # Pattern: "Daily: 24 hours" or "24 hours" (check this first)
                r'(Daily|24\s*hours?|Open\s*24\s*hours?)',
                # Pattern: "Monday: 9:00 AM - 10:00 PM"
                r'(\w+):\s*(\d{1,2}):(\d{2})\s*(AM|PM)\s*-\s*(\d{1,2}):(\d{2})\s*(AM|PM)',
                # Pattern: "Mon 9AM-10PM"
                r'(\w{3})\s*(\d{1,2})(AM|PM)-(\d{1,2})(AM|PM)',
                # Pattern: "Monday 9:00-22:00"
                r'(\w+)\s*(\d{1,2}):(\d{2})-(\d{1,2}):(\d{2})',
                # Pattern: "Mon-Fri 9AM-5PM"
                r'(\w{3})-(\w{3})\s*(\d{1,2})(AM|PM)-(\d{1,2})(AM|PM)',
            ]
            
            parsed_hours = []
            
            for i, pattern in enumerate(patterns):
                matches = re.findall(pattern, hours_data, re.IGNORECASE)
                if matches:
                    for match in matches:
                        # Handle 24-hour pattern separately
                        if i == 0:  # First pattern is 24-hour pattern
                            day_info = [{'day': 'daily', 'start': time(0, 0), 'end': time(23, 59)}]
                        else:
                            day_info = self._parse_day_hours(match, pattern)
                        
                        if day_info:
                            parsed_hours.extend(day_info)
            
            if parsed_hours:
                return True, parsed_hours
            
            # If no patterns matched, try to extract any time-like information
            return self._fallback_hours_parsing(hours_data)
            
        except Exception as e:
            logger.error(f"Error parsing business hours: {e}")
            return False, []
    
    def _parse_day_hours(self, match: tuple, pattern: str) -> List[Dict]:
        """
        Parse hours for specific day(s) from regex match.
        
        Args:
            match: Regex match tuple
            pattern: Pattern that was matched
            
        Returns:
            List of day-hour dictionaries
        """
        try:
            if len(match) == 7:  # Pattern 1: "Monday: 9:00 AM - 10:00 PM"
                day, start_hour, start_min, start_ampm, end_hour, end_min, end_ampm = match
                start_time = self._time_from_components(start_hour, start_min, start_ampm)
                end_time = self._time_from_components(end_hour, end_min, end_ampm)
                return [{'day': day.lower(), 'start': start_time, 'end': end_time}]
                
            elif len(match) == 5:  # Pattern 2: "Mon 9AM-10PM"
                day, start_hour, start_ampm, end_hour, end_ampm = match
                start_time = self._time_from_components(start_hour, '00', start_ampm)
                end_time = self._time_from_components(end_hour, '00', end_ampm)
                return [{'day': day.lower(), 'start': start_time, 'end': end_time}]
                
            elif len(match) == 5:  # Pattern 3: "Monday 9:00-22:00"
                day, start_hour, start_min, end_hour, end_min = match
                start_time = time(int(start_hour), int(start_min))
                end_time = time(int(end_hour), int(end_min))
                return [{'day': day.lower(), 'start': start_time, 'end': end_time}]
                
            elif len(match) == 6:  # Pattern 4: "Mon-Fri 9AM-5PM"
                start_day, end_day, start_hour, start_ampm, end_hour, end_ampm = match
                start_time = self._time_from_components(start_hour, '00', start_ampm)
                end_time = self._time_from_components(end_hour, '00', end_ampm)
                
                # Generate days between start_day and end_day
                days = self._get_days_between(start_day, end_day)
                return [{'day': day, 'start': start_time, 'end': end_time} for day in days]
                
            elif len(match) == 1:  # Pattern 5: "Daily: 24 hours"
                # 24-hour restaurant
                return [{'day': 'daily', 'start': time(0, 0), 'end': time(23, 59)}]
                
        except Exception as e:
            logger.error(f"Error parsing day hours: {e}")
            
        return []
    
    def _time_from_components(self, hour: str, minute: str, ampm: str) -> time:
        """
        Create time object from hour, minute, and AM/PM components.
        
        Args:
            hour: Hour string
            minute: Minute string
            ampm: AM or PM string
            
        Returns:
            time object
        """
        hour_int = int(hour)
        minute_int = int(minute)
        
        if ampm.upper() == 'PM' and hour_int != 12:
            hour_int += 12
        elif ampm.upper() == 'AM' and hour_int == 12:
            hour_int = 0
            
        return time(hour_int, minute_int)
    
    def _get_days_between(self, start_day: str, end_day: str) -> List[str]:
        """
        Get list of days between start_day and end_day.
        
        Args:
            start_day: Start day abbreviation
            end_day: End day abbreviation
            
        Returns:
            List of day names
        """
        days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        day_map = {
            'mon': 'monday', 'tue': 'tuesday', 'wed': 'wednesday',
            'thu': 'thursday', 'fri': 'friday', 'sat': 'saturday', 'sun': 'sunday'
        }
        
        try:
            start_idx = days.index(start_day.lower())
            end_idx = days.index(end_day.lower())
            
            if start_idx <= end_idx:
                day_range = days[start_idx:end_idx + 1]
            else:
                # Handle wrap-around (e.g., Fri-Mon)
                day_range = days[start_idx:] + days[:end_idx + 1]
                
            return [day_map[day] for day in day_range]
        except ValueError:
            return []
    
    def _fallback_hours_parsing(self, hours_data: str) -> Tuple[bool, List[Dict]]:
        """
        Fallback method for parsing hours when standard patterns don't match.
        
        Args:
            hours_data: Raw hours string
            
        Returns:
            Tuple of (success, parsed_hours_list)
        """
        try:
            # Look for any time-like patterns
            time_pattern = r'(\d{1,2}):(\d{2})\s*(AM|PM)'
            times = re.findall(time_pattern, hours_data, re.IGNORECASE)
            
            if len(times) >= 2:
                # Assume first time is opening, second is closing
                start_hour, start_min, start_ampm = times[0]
                end_hour, end_min, end_ampm = times[1]
                
                start_time = self._time_from_components(start_hour, start_min, start_ampm)
                end_time = self._time_from_components(end_hour, end_min, end_ampm)
                
                # Assume daily hours if we can't determine specific days
                return True, [{'day': 'daily', 'start': start_time, 'end': end_time}]
                
        except Exception as e:
            logger.error(f"Error in fallback hours parsing: {e}")
            
        return False, []
    
    def _check_if_open(self, parsed_hours: List[Dict], current_time: datetime) -> Tuple[bool, Optional[datetime], str]:
        """
        Check if restaurant is currently open based on parsed hours.
        
        Args:
            parsed_hours: List of parsed hour dictionaries
            current_time: Current time in restaurant's timezone
            
        Returns:
            Tuple of (is_open, next_open_time, reason)
        """
        try:
            current_weekday = current_time.strftime('%A').lower()
            current_time_only = current_time.time()
            
            # Find today's hours
            today_hours = None
            for hours in parsed_hours:
                if hours['day'] in [current_weekday, 'daily']:
                    today_hours = hours
                    break
            
            if not today_hours:
                return False, None, f"Closed on {current_weekday}"
            
            start_time = today_hours['start']
            end_time = today_hours['end']
            
            # Handle overnight hours (e.g., 10 PM - 2 AM)
            if end_time < start_time:
                # Restaurant is open if current time is after start OR before end
                if current_time_only >= start_time or current_time_only <= end_time:
                    return True, None, "Currently open (overnight hours)"
                else:
                    # Calculate next open time
                    next_open = self._calculate_next_open_time(parsed_hours, current_time)
                    return False, next_open, "Currently closed (overnight hours)"
            else:
                # Normal hours
                if start_time <= current_time_only <= end_time:
                    return True, None, "Currently open"
                else:
                    next_open = self._calculate_next_open_time(parsed_hours, current_time)
                    if current_time_only < start_time:
                        return False, next_open, f"Opens at {start_time.strftime('%I:%M %p')}"
                    else:
                        return False, next_open, f"Closed at {end_time.strftime('%I:%M %p')}"
                        
        except Exception as e:
            logger.error(f"Error checking if open: {e}")
            return False, None, f"Error determining status: {str(e)}"
    
    def _calculate_next_open_time(self, parsed_hours: List[Dict], current_time: datetime) -> Optional[datetime]:
        """
        Calculate the next time the restaurant will be open.
        
        Args:
            parsed_hours: List of parsed hour dictionaries
            current_time: Current time in restaurant's timezone
            
        Returns:
            Next open datetime or None
        """
        try:
            # Check remaining hours today
            current_weekday = current_time.strftime('%A').lower()
            current_time_only = current_time.time()
            
            for hours in parsed_hours:
                if hours['day'] in [current_weekday, 'daily']:
                    start_time = hours['start']
                    if current_time_only < start_time:
                        # Restaurant opens later today
                        next_open = current_time.replace(
                            hour=start_time.hour,
                            minute=start_time.minute,
                            second=0,
                            microsecond=0
                        )
                        return next_open
            
            # Check next days
            for i in range(1, 8):  # Check next 7 days
                next_date = current_time + timedelta(days=i)
                next_weekday = next_date.strftime('%A').lower()
                
                for hours in parsed_hours:
                    if hours['day'] in [next_weekday, 'daily']:
                        start_time = hours['start']
                        next_open = next_date.replace(
                            hour=start_time.hour,
                            minute=start_time.minute,
                            second=0,
                            microsecond=0
                        )
                        return next_open
            
            return None
            
        except Exception as e:
            logger.error(f"Error calculating next open time: {e}")
            return None

# Global instance for caching
_status_calculator = RestaurantStatusCalculator()

def get_restaurant_status(restaurant_data: Dict) -> Dict[str, any]:
    """
    Get the current status of a restaurant.
    
    This is the main function to be used by the application.
    
    Args:
        restaurant_data: Restaurant data dictionary
        
    Returns:
        Status information dictionary
    """
    return _status_calculator.get_restaurant_status(restaurant_data)

def is_restaurant_open(restaurant_data: Dict) -> bool:
    """
    Simple function to check if restaurant is currently open.
    
    Args:
        restaurant_data: Restaurant data dictionary
        
    Returns:
        True if restaurant is open, False otherwise
    """
    status_info = get_restaurant_status(restaurant_data)
    return status_info.get('is_open', False) 