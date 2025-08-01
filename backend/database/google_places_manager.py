#!/usr/bin/env python3
"""
Google Places Data Manager
==========================

This module manages Google Places data storage and periodic updates.
It stores Google Places information in the database and periodically
checks for updates to reduce API calls and improve performance.

Features:
- Store Google Places data in database
- Periodic updates with configurable intervals
- Cache management and cleanup
- API quota management
- Error handling and retry logic

Author: JewGo Development Team
Version: 1.0
Last Updated: 2024
"""

import os
import json
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# SQLAlchemy Base
Base = declarative_base()

class GooglePlacesData(Base):
    """
    Google Places data storage table.
    
    Stores Google Places information for restaurants to reduce API calls
    and improve performance. Data is periodically updated.
    """
    __tablename__ = 'google_places_data'
    
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, nullable=False, index=True)  # Foreign key to restaurants table
    google_place_id = Column(String(255), unique=True, index=True)  # Google's place_id
    
    # Basic information
    name = Column(String(255))
    formatted_address = Column(String(500))
    phone_number = Column(String(50))
    website = Column(String(500))
    rating = Column(Float)
    user_ratings_total = Column(Integer)
    price_level = Column(Integer)  # 0-4 scale
    
    # Location data
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Hours and business info
    hours_json = Column(JSON)  # Structured hours data
    hours_text = Column(Text)  # Human-readable hours
    timezone = Column(String(50))
    
    # Photos and media
    photos_json = Column(JSON)  # Photo references and metadata
    primary_photo_url = Column(String(500))
    
    # Additional data
    types_json = Column(JSON)  # Business types
    opening_hours_json = Column(JSON)  # Raw opening hours data
    reviews_json = Column(JSON)  # Recent reviews (limited)
    
    # Metadata
    last_updated = Column(DateTime, default=datetime.utcnow, nullable=False)
    next_update = Column(DateTime, nullable=False)  # When to check for updates
    update_frequency_hours = Column(Integer, default=168)  # Default: 1 week
    is_active = Column(Boolean, default=True)  # Whether this place is still active
    error_count = Column(Integer, default=0)  # Track API errors
    last_error = Column(Text)  # Last error message
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class GooglePlacesManager:
    """
    Manages Google Places data storage and periodic updates.
    """
    
    def __init__(self, database_url: str = None):
        """Initialize the Google Places manager."""
        self.database_url = database_url or os.getenv('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is required")
        
        self.api_key = os.getenv('GOOGLE_PLACES_API_KEY')
        if not self.api_key:
            logger.warning("GOOGLE_PLACES_API_KEY not set - some features will be limited")
        
        self.engine = None
        self.SessionLocal = None
        self.connect()
        
        # Configuration
        self.default_update_frequency = 168  # 1 week in hours
        self.max_retries = 3
        self.retry_delay = 5  # seconds
        
    def connect(self) -> bool:
        """Connect to the database."""
        try:
            self.engine = create_engine(self.database_url)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            # Create tables if they don't exist
            Base.metadata.create_all(bind=self.engine)
            
            logger.info("Connected to database successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False
    
    def get_session(self) -> Session:
        """Get a database session."""
        return self.SessionLocal()
    
    def store_place_data(self, restaurant_id: int, place_data: Dict[str, Any], 
                        google_place_id: str = None) -> bool:
        """
        Store Google Places data for a restaurant.
        
        Args:
            restaurant_id: ID of the restaurant in the main restaurants table
            place_data: Google Places API response data
            google_place_id: Google's place_id (if not in place_data)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            session = self.get_session()
            
            # Extract place_id
            place_id = google_place_id or place_data.get('place_id')
            if not place_id:
                logger.error("No place_id provided or found in place_data")
                return False
            
            # Check if data already exists
            existing = session.query(GooglePlacesData).filter_by(
                google_place_id=place_id
            ).first()
            
            if existing:
                # Update existing record
                self._update_place_data(existing, place_data)
                logger.info(f"Updated Google Places data for restaurant {restaurant_id}")
            else:
                # Create new record
                new_data = self._create_place_data(restaurant_id, place_id, place_data)
                session.add(new_data)
                logger.info(f"Stored new Google Places data for restaurant {restaurant_id}")
            
            session.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error storing place data for restaurant {restaurant_id}: {e}")
            if session:
                session.rollback()
            return False
        finally:
            if session:
                session.close()
    
    def _create_place_data(self, restaurant_id: int, place_id: str, 
                          place_data: Dict[str, Any]) -> GooglePlacesData:
        """Create a new GooglePlacesData record."""
        result = place_data.get('result', place_data)
        
        # Calculate next update time
        next_update = datetime.utcnow() + timedelta(hours=self.default_update_frequency)
        
        return GooglePlacesData(
            restaurant_id=restaurant_id,
            google_place_id=place_id,
            name=result.get('name'),
            formatted_address=result.get('formatted_address'),
            phone_number=result.get('formatted_phone_number'),
            website=result.get('website'),
            rating=result.get('rating'),
            user_ratings_total=result.get('user_ratings_total'),
            price_level=result.get('price_level'),
            latitude=result.get('geometry', {}).get('location', {}).get('lat'),
            longitude=result.get('geometry', {}).get('location', {}).get('lng'),
            hours_json=result.get('opening_hours'),
            hours_text=self._format_hours_text(result.get('opening_hours')),
            timezone=result.get('utc_offset'),
            photos_json=result.get('photos'),
            primary_photo_url=self._get_primary_photo_url(result.get('photos')),
            types_json=result.get('types'),
            opening_hours_json=result.get('opening_hours'),
            reviews_json=result.get('reviews'),
            next_update=next_update,
            update_frequency_hours=self.default_update_frequency
        )
    
    def _update_place_data(self, existing_data: GooglePlacesData, 
                          place_data: Dict[str, Any]) -> None:
        """Update existing GooglePlacesData record."""
        result = place_data.get('result', place_data)
        
        # Update fields
        existing_data.name = result.get('name', existing_data.name)
        existing_data.formatted_address = result.get('formatted_address', existing_data.formatted_address)
        existing_data.phone_number = result.get('formatted_phone_number', existing_data.phone_number)
        existing_data.website = result.get('website', existing_data.website)
        existing_data.rating = result.get('rating', existing_data.rating)
        existing_data.user_ratings_total = result.get('user_ratings_total', existing_data.user_ratings_total)
        existing_data.price_level = result.get('price_level', existing_data.price_level)
        
        # Update location if available
        if 'geometry' in result and 'location' in result['geometry']:
            existing_data.latitude = result['geometry']['location'].get('lat', existing_data.latitude)
            existing_data.longitude = result['geometry']['location'].get('lng', existing_data.longitude)
        
        # Update hours
        if 'opening_hours' in result:
            existing_data.hours_json = result['opening_hours']
            existing_data.hours_text = self._format_hours_text(result['opening_hours'])
        
        # Update other fields
        existing_data.timezone = result.get('utc_offset', existing_data.timezone)
        existing_data.photos_json = result.get('photos', existing_data.photos_json)
        existing_data.primary_photo_url = self._get_primary_photo_url(result.get('photos')) or existing_data.primary_photo_url
        existing_data.types_json = result.get('types', existing_data.types_json)
        existing_data.opening_hours_json = result.get('opening_hours', existing_data.opening_hours_json)
        existing_data.reviews_json = result.get('reviews', existing_data.reviews_json)
        
        # Update metadata
        existing_data.last_updated = datetime.utcnow()
        existing_data.next_update = datetime.utcnow() + timedelta(hours=existing_data.update_frequency_hours)
        existing_data.error_count = 0  # Reset error count on successful update
        existing_data.last_error = None
    
    def _format_hours_text(self, opening_hours: Dict[str, Any]) -> str:
        """Format opening hours into human-readable text."""
        if not opening_hours or 'weekday_text' not in opening_hours:
            return ""
        
        return "\n".join(opening_hours['weekday_text'])
    
    def _get_primary_photo_url(self, photos: List[Dict[str, Any]]) -> str:
        """Get the primary photo URL from photos array."""
        if not photos:
            return ""
        
        # Get the first photo reference
        photo_ref = photos[0].get('photo_reference')
        if not photo_ref:
            return ""
        
        # Build photo URL
        return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_ref}&key={self.api_key}"
    
    def get_place_data(self, restaurant_id: int) -> Optional[Dict[str, Any]]:
        """
        Get stored Google Places data for a restaurant.
        
        Args:
            restaurant_id: ID of the restaurant
            
        Returns:
            Dict containing the place data or None if not found
        """
        try:
            session = self.get_session()
            place_data = session.query(GooglePlacesData).filter_by(
                restaurant_id=restaurant_id,
                is_active=True
            ).first()
            
            if place_data:
                return self._place_data_to_dict(place_data)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting place data for restaurant {restaurant_id}: {e}")
            return None
        finally:
            if session:
                session.close()
    
    def _place_data_to_dict(self, place_data: GooglePlacesData) -> Dict[str, Any]:
        """Convert GooglePlacesData object to dictionary."""
        return {
            'id': place_data.id,
            'restaurant_id': place_data.restaurant_id,
            'google_place_id': place_data.google_place_id,
            'name': place_data.name,
            'formatted_address': place_data.formatted_address,
            'phone_number': place_data.phone_number,
            'website': place_data.website,
            'rating': place_data.rating,
            'user_ratings_total': place_data.user_ratings_total,
            'price_level': place_data.price_level,
            'latitude': place_data.latitude,
            'longitude': place_data.longitude,
            'hours_json': place_data.hours_json,
            'hours_text': place_data.hours_text,
            'timezone': place_data.timezone,
            'photos_json': place_data.photos_json,
            'primary_photo_url': place_data.primary_photo_url,
            'types_json': place_data.types_json,
            'opening_hours_json': place_data.opening_hours_json,
            'reviews_json': place_data.reviews_json,
            'last_updated': place_data.last_updated.isoformat() if place_data.last_updated else None,
            'next_update': place_data.next_update.isoformat() if place_data.next_update else None,
            'is_active': place_data.is_active,
            'error_count': place_data.error_count
        }
    
    def get_places_needing_update(self, limit: int = 50) -> List[GooglePlacesData]:
        """
        Get places that need to be updated.
        
        Args:
            limit: Maximum number of places to return
            
        Returns:
            List of GooglePlacesData objects needing updates
        """
        try:
            session = self.get_session()
            now = datetime.utcnow()
            
            places = session.query(GooglePlacesData).filter(
                GooglePlacesData.is_active == True,
                GooglePlacesData.next_update <= now
            ).limit(limit).all()
            
            return places
            
        except Exception as e:
            logger.error(f"Error getting places needing update: {e}")
            return []
        finally:
            if session:
                session.close()
    
    def update_place_from_api(self, place_data: GooglePlacesData) -> bool:
        """
        Update place data from Google Places API.
        
        Args:
            place_data: GooglePlacesData object to update
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.api_key:
            logger.warning("No API key available for Google Places update")
            return False
        
        try:
            # Get place details from Google Places API
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            params = {
                'place_id': place_data.google_place_id,
                'fields': 'name,formatted_address,formatted_phone_number,website,rating,user_ratings_total,price_level,geometry,opening_hours,utc_offset,photos,types,reviews',
                'key': self.api_key
            }
            
            response = requests.get(details_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'OK':
                # Update the place data
                session = self.get_session()
                self._update_place_data(place_data, data)
                session.commit()
                session.close()
                
                logger.info(f"Successfully updated Google Places data for {place_data.google_place_id}")
                return True
            else:
                # Handle API errors
                place_data.error_count += 1
                place_data.last_error = f"API Error: {data.get('status')} - {data.get('error_message', 'Unknown error')}"
                
                # Increase update interval on repeated errors
                if place_data.error_count > 3:
                    place_data.update_frequency_hours = min(place_data.update_frequency_hours * 2, 1680)  # Max 1 week
                
                session = self.get_session()
                session.commit()
                session.close()
                
                logger.warning(f"Failed to update Google Places data for {place_data.google_place_id}: {data.get('status')}")
                return False
                
        except Exception as e:
            # Handle other errors
            place_data.error_count += 1
            place_data.last_error = str(e)
            
            session = self.get_session()
            session.commit()
            session.close()
            
            logger.error(f"Error updating Google Places data for {place_data.google_place_id}: {e}")
            return False
    
    def run_periodic_updates(self, batch_size: int = 10) -> Dict[str, Any]:
        """
        Run periodic updates for places that need updating.
        
        Args:
            batch_size: Number of places to update in this batch
            
        Returns:
            Dict with update statistics
        """
        stats = {
            'total_processed': 0,
            'successful_updates': 0,
            'failed_updates': 0,
            'skipped_updates': 0
        }
        
        try:
            places_to_update = self.get_places_needing_update(batch_size)
            stats['total_processed'] = len(places_to_update)
            
            for place_data in places_to_update:
                # Skip if too many errors
                if place_data.error_count > 5:
                    stats['skipped_updates'] += 1
                    logger.warning(f"Skipping update for {place_data.google_place_id} due to high error count")
                    continue
                
                # Update the place
                if self.update_place_from_api(place_data):
                    stats['successful_updates'] += 1
                else:
                    stats['failed_updates'] += 1
                
                # Add delay between API calls to respect rate limits
                time.sleep(0.1)
            
            logger.info("Periodic update completed", **stats)
            return stats
            
        except Exception as e:
            logger.error(f"Error running periodic updates: {e}")
            return stats
    
    def cleanup_old_data(self, days_old: int = 7) -> int:
        """
        Clean up old Google Places data.
        
        Args:
            days_old: Remove data older than this many days
            
        Returns:
            int: Number of records removed
        """
        try:
            session = self.get_session()
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            
            # Mark old inactive records as inactive
            result = session.query(GooglePlacesData).filter(
                GooglePlacesData.last_updated < cutoff_date,
                GooglePlacesData.is_active == True
            ).update({'is_active': False})
            
            session.commit()
            session.close()
            
            logger.info(f"Marked {result} old Google Places records as inactive")
            return result
            
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
            return 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about stored Google Places data."""
        try:
            session = self.get_session()
            
            total_records = session.query(GooglePlacesData).count()
            active_records = session.query(GooglePlacesData).filter_by(is_active=True).count()
            records_needing_update = session.query(GooglePlacesData).filter(
                GooglePlacesData.is_active == True,
                GooglePlacesData.next_update <= datetime.utcnow()
            ).count()
            
            # Get error statistics
            error_records = session.query(GooglePlacesData).filter(
                GooglePlacesData.error_count > 0
            ).count()
            
            session.close()
            
            return {
                'total_records': total_records,
                'active_records': active_records,
                'records_needing_update': records_needing_update,
                'error_records': error_records,
                'last_updated': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}
    
    def disconnect(self):
        """Disconnect from the database."""
        if self.engine:
            self.engine.dispose()
            logger.info("Disconnected from database") 