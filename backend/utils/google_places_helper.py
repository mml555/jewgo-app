#!/usr/bin/env python3
"""
Google Places Helper
===================

Helper functions for Google Places API integration.
Used to fetch website links as backup when restaurants don't have them.

Author: JewGo Development Team
Version: 1.0
"""

import os
import requests
import time
import structlog

logger = structlog.get_logger()

def search_google_places_website(restaurant_name: str, address: str) -> str:
    """
    Search Google Places API for a restaurant's website.
    Returns the website URL if found, empty string otherwise.
    """
    try:
        api_key = os.environ.get('GOOGLE_PLACES_API_KEY')
        if not api_key:
            logger.warning("GOOGLE_PLACES_API_KEY not set")
            return ""
        
        # Build search query
        query = f"{restaurant_name} {address}"
        
        # Search for the place
        search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        search_params = {
            'query': query,
            'key': api_key,
            'type': 'restaurant'
        }
        
        logger.info(f"Searching Google Places for: {query}")
        response = requests.get(search_url, params=search_params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data['status'] == 'OK' and data['results']:
            place_id = data['results'][0]['place_id']
            
            # Get place details
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                'place_id': place_id,
                'fields': 'website',
                'key': api_key
            }
            
            logger.info(f"Getting place details for place_id: {place_id}")
            details_response = requests.get(details_url, params=details_params, timeout=10)
            details_response.raise_for_status()
            
            details_data = details_response.json()
            
            if details_data['status'] == 'OK' and 'result' in details_data:
                website = details_data['result'].get('website', '')
                if website:
                    logger.info(f"Found website for {restaurant_name}: {website}")
                    return website
            
            logger.warning(f"No website found for {restaurant_name}")
            return ""
        else:
            logger.warning(f"No place found for: {query}")
            return ""
            
    except Exception as e:
        logger.error(f"Error searching Google Places for {restaurant_name}: {e}")
        return ""

def validate_website_url(url: str) -> bool:
    """
    Validate if a website URL is accessible and properly formatted.
    """
    try:
        # Basic URL validation
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Test if website is accessible (with shorter timeout for efficiency)
        response = requests.head(url, timeout=3, allow_redirects=True)
        is_valid = response.status_code == 200
        logger.debug(f"Website validation", url=url, status_code=response.status_code, is_valid=is_valid)
        return is_valid
        
    except Exception as e:
        logger.debug(f"Website validation failed", url=url, error=str(e))
        return False

def search_google_places_hours(restaurant_name: str, address: str) -> str:
    """
    Search Google Places API for a restaurant's opening hours.
    Returns the formatted hours string if found, empty string otherwise.
    """
    try:
        api_key = os.environ.get('GOOGLE_PLACES_API_KEY')
        if not api_key:
            logger.warning("GOOGLE_PLACES_API_KEY not set")
            return ""
        
        # Build search query
        query = f"{restaurant_name} {address}"
        
        # Search for the place
        search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        search_params = {
            'query': query,
            'key': api_key,
            'type': 'restaurant'
        }
        
        logger.info(f"Searching Google Places for hours: {query}")
        response = requests.get(search_url, params=search_params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data['status'] == 'OK' and data['results']:
            place_id = data['results'][0]['place_id']
            
            # Get place details
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                'place_id': place_id,
                'fields': 'opening_hours',
                'key': api_key
            }
            
            logger.info(f"Getting place details for hours, place_id: {place_id}")
            details_response = requests.get(details_url, params=details_params, timeout=10)
            details_response.raise_for_status()
            
            details_data = details_response.json()
            
            if details_data['status'] == 'OK' and 'result' in details_data:
                opening_hours = details_data['result'].get('opening_hours')
                if opening_hours and 'weekday_text' in opening_hours:
                    hours_formatted = format_hours_from_places_api(opening_hours)
                    if hours_formatted:
                        logger.info(f"Found hours for {restaurant_name}: {hours_formatted}")
                        return hours_formatted
            
            logger.warning(f"No hours found for {restaurant_name}")
            return ""
        else:
            logger.warning(f"No place found for hours: {query}")
            return ""
            
    except Exception as e:
        logger.error(f"Error searching Google Places for hours {restaurant_name}: {e}")
        return ""

def format_hours_from_places_api(opening_hours: dict) -> str:
    """
    Format opening hours from Google Places API format to our database format.
    """
    if not opening_hours or 'weekday_text' not in opening_hours:
        return ""
        
    # Google Places API provides weekday_text as a list of formatted strings
    # e.g., ["Monday: 11:00 AM – 10:00 PM", "Tuesday: 11:00 AM – 10:00 PM", ...]
    weekday_text = opening_hours['weekday_text']
    
    # Convert to our format: "Mon 11:00 AM – 10:00 PM, Tue 11:00 AM – 10:00 PM, ..."
    day_mapping = {
        'Monday': 'Mon',
        'Tuesday': 'Tue', 
        'Wednesday': 'Wed',
        'Thursday': 'Thu',
        'Friday': 'Fri',
        'Saturday': 'Sat',
        'Sunday': 'Sun'
    }
    
    formatted_hours = []
    for day_text in weekday_text:
        # Parse "Monday: 11:00 AM – 10:00 PM"
        if ': ' in day_text:
            day, hours = day_text.split(': ', 1)
            short_day = day_mapping.get(day, day[:3])
            formatted_hours.append(f"{short_day} {hours}")
    
    return ', '.join(formatted_hours) 