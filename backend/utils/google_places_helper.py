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