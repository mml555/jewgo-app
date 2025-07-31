#!/usr/bin/env python3
"""
Enhanced Database Manager for JewGo App v3
==========================================

This module provides a comprehensive database management system for the JewGo application,
handling all PostgreSQL database operations with SQLAlchemy 1.4. The system is designed
to work with a consolidated restaurants table that contains all kosher restaurant data.

Key Features:
- SQLAlchemy 1.4 compatibility with PostgreSQL
- Structured logging with structlog
- Comprehensive restaurant data management
- Kosher supervision categorization
- Search and filtering capabilities
- Geographic location support
- Statistics and reporting

Database Schema:
- 28 optimized columns for restaurant data
- Kosher supervision flags (Chalav Yisroel, Pas Yisroel, etc.)
- ORB certification information
- Contact and location details
- Timestamps for tracking changes

Author: JewGo Development Team
Version: 3.0
Last Updated: 2024
"""

import os
import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import structlog
from typing import Dict, Any, List, Optional
from datetime import datetime

# Import the dynamic status calculation module
try:
    from utils.restaurant_status import get_restaurant_status, is_restaurant_open
except ImportError:
    # Fallback for when utils module is not available
    def get_restaurant_status(restaurant_data):
        return {'is_open': False, 'status': 'unknown', 'status_reason': 'Status calculation not available'}
    
    def is_restaurant_open(restaurant_data):
        return False

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

class Restaurant(Base):
    """
    Optimized Restaurant model for SQLAlchemy (consolidated table).
    
    This model represents the main restaurants table in the JewGo database.
    It contains all kosher restaurant information including contact details,
    kosher supervision status, and ORB certification information.
    
    Schema Design:
    - Optimized for kosher restaurant data
    - Supports multiple kosher supervision levels
    - Includes ORB certification details
    - Maintains audit trail with timestamps
    
    Current Data:
    - 107 total restaurants
    - 99 dairy restaurants, 8 pareve restaurants
    - 104 Chalav Yisroel, 3 Chalav Stam
    - 22 Pas Yisroel restaurants
    """
    __tablename__ = 'restaurants'
    
    # 🔒 System-Generated / Controlled
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    current_time_local = Column(DateTime)  # System-generated (local time snapshot)
    hours_parsed = Column(Boolean, default=False)  # Internal flag — OK to keep
    
    # 🧾 Required (updated via ORB scrape every 3 weeks)
    name = Column(String(255), nullable=False)  # Restaurant name (required)
    address = Column(String(500), nullable=False)  # Street address
    city = Column(String(100), nullable=False)  # City name
    state = Column(String(50), nullable=False)  # State abbreviation
    zip_code = Column(String(20), nullable=False)  # ZIP code
    phone_number = Column(String(50), nullable=False)  # Phone number
    website = Column(String(500))  # Website URL
    certifying_agency = Column(String(100), default='ORB', nullable=False)  # Auto-filled = "ORB"
    kosher_category = Column('kosher_category', String(20), nullable=False)  # ENUM('meat', 'dairy', 'pareve')
    listing_type = Column(String(100), nullable=False)  # Business category
    
    # 📍 Enriched via Google Places API (on creation or scheduled)
    google_listing_url = Column(String(500))  # Optional (1-time fetch)
    price_range = Column(String(20))  # Optional
    short_description = Column(Text)  # Optional (e.g. from GMB or internal AI)
    hours_of_operation = Column(Text)  # Optional (check every 7 days)
    hours_json = Column(Text)  # JSONB for structured hours data
    hours_last_updated = Column(DateTime)  # Track when hours were last updated
    timezone = Column(String(50))  # Based on geolocation or ORB data
    latitude = Column(Float)  # Based on geocoded address
    longitude = Column(Float)  # Based on geocoded address
    
    # 🧼 Kosher Details Source ORB data
    is_cholov_yisroel = Column(Boolean)  # Optional (only if dairy)
    is_pas_yisroel = Column(Boolean)  # Optional (only if meat/pareve)
    
    # 🖼️ Display/UX
    image_url = Column(String(500))  # Optional — fallback to placeholder
    specials = Column(Text)  # JSONB[] or child table - Admin-managed only, frontend only
    
    # 🗑️ Removed Fields (commented out for reference)
    # detail_url = Column(String(500))  # ❌ delete
    # email = Column(String(255))  # ❌ delete
    # kosher_cert_link = Column(String(500))  # ❌ delete
    # next_open_time = Column(DateTime)  # ❌ delete (calculate in logic)
    # is_open = Column(Boolean)  # ❌ move to function, not DB
    # status_reason = Column(String(255))  # ❌ internal only, not DB
    
    # ❓ Field Needing Clarification
    # status = Column(String(50), default='approved')  # Should be enum: ["pending", "approved", "rejected"] or remove if unused

class EnhancedDatabaseManager:
    """Enhanced database manager with SQLAlchemy 1.4 support for consolidated restaurants table."""
    
    def __init__(self, database_url: str = None):
        """Initialize database manager with connection string."""
        self.database_url = database_url or os.environ.get('DATABASE_URL')
        
        # Validate that DATABASE_URL is provided
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is required")
        
        # Initialize SQLAlchemy components
        self.engine = None
        self.SessionLocal = None
        self.session = None
        
        logger.info("Database manager initialized", database_url=self.database_url[:50] + "...")
    
    def connect(self) -> bool:
        """Connect to the database and create tables if they don't exist."""
        try:
            # Create the engine with SQLAlchemy 1.4 + psycopg2-binary
            self.engine = create_engine(
                self.database_url,
                echo=False
            )
            
            # Test the connection
            with self.engine.connect() as conn:
                from sqlalchemy import text
                result = conn.execute(text("SELECT 1"))
                result.fetchone()  # Consume the result
                logger.info("Database connection successful")
            
            # Create session factory
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            # Create tables if they don't exist
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created/verified")
            
            return True
            
        except Exception as e:
            logger.error("Failed to connect to database", error=str(e), database_url=self.database_url[:50] + "...")
            return False
    
    def get_session(self) -> Session:
        """Get a new database session."""
        if not self.SessionLocal:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.SessionLocal()
    
    def add_restaurant(self, restaurant_data: Dict[str, Any]) -> bool:
        """Add a new restaurant to the database."""
        try:
            session = self.get_session()
            
            # Validate required fields
            required_fields = ['name', 'address', 'city', 'state', 'zip_code', 'phone_number', 'kosher_category', 'listing_type']
            for field in required_fields:
                if not restaurant_data.get(field):
                    logger.error(f"Missing required field: {field}")
                    return False
            
            # Set default values for required fields
            restaurant_data.setdefault('certifying_agency', 'ORB')
            restaurant_data.setdefault('created_at', datetime.utcnow())
            restaurant_data.setdefault('updated_at', datetime.utcnow())
            restaurant_data.setdefault('hours_parsed', False)
            
            # Handle specials field (convert to JSON string if it's a list)
            if 'specials' in restaurant_data and isinstance(restaurant_data['specials'], list):
                import json
                restaurant_data['specials'] = json.dumps(restaurant_data['specials'])
            
            # Create new restaurant object
            restaurant = Restaurant(**restaurant_data)
            session.add(restaurant)
            session.commit()
            
            logger.info("Restaurant added successfully", restaurant_id=restaurant.id, name=restaurant.name)
            return True
            
        except Exception as e:
            logger.error("Failed to add restaurant", error=str(e), restaurant_data=restaurant_data)
            if session:
                session.rollback()
            return False
        finally:
            if session:
                session.close()
    
    def get_restaurants(self, limit: int = 100, offset: int = 0) -> List[Restaurant]:
        """Get restaurants from the consolidated table."""
        try:
            session = self.get_session()
            restaurants = session.query(Restaurant).limit(limit).offset(offset).all()
            return restaurants
        except Exception as e:
            logger.error("Failed to get restaurants", error=str(e))
            return []
        finally:
            if session:
                session.close()
    
    def get_all_places(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all places from the consolidated restaurants table."""
        try:
            session = self.get_session()
            restaurants = session.query(Restaurant).limit(limit).offset(offset).all()
            
            # Convert to unified format
            all_places = []
            for restaurant in restaurants:
                place_dict = self._restaurant_to_unified_dict(restaurant)
                all_places.append(place_dict)
            
            # Sort by name
            all_places.sort(key=lambda x: x['name'])
            return all_places
            
        except Exception as e:
            logger.error("Failed to get all places", error=str(e))
            return []
        finally:
            if session:
                session.close()
    
    def search_places(self, query: str = None, category: str = None, state: str = None, 
                     limit: int = 50, offset: int = 0, is_kosher: bool = None) -> List[Dict[str, Any]]:
        """Search places from the consolidated restaurants table."""
        try:
            session = self.get_session()
            restaurant_query = session.query(Restaurant)
            
            if query:
                restaurant_query = restaurant_query.filter(Restaurant.name.ilike(f'%{query}%'))
            if category:
                restaurant_query = restaurant_query.filter(Restaurant.listing_type.ilike(f'%{category}%'))
            if state:
                restaurant_query = restaurant_query.filter(Restaurant.state.ilike(f'%{state}%'))
            if is_kosher is not None:
                # All restaurants in our database are kosher, so this filter is not needed
                pass
            
            restaurants = restaurant_query.limit(limit).offset(offset).all()
            
            # Convert to unified format
            all_places = []
            for restaurant in restaurants:
                place_dict = self._restaurant_to_unified_dict(restaurant)
                all_places.append(place_dict)
            
            return all_places
            
        except Exception as e:
            logger.error("Failed to search places", error=str(e))
            return []
        finally:
            if session:
                session.close()
    
    def search_restaurants_near_location(self, lat: float, lng: float, radius: float = 50, 
                                       query: str = None, category: str = None, limit: int = 50, offset: int = 0) -> List[Restaurant]:
        """Search restaurants near a specific location using distance calculation."""
        try:
            session = self.get_session()
            query_obj = session.query(Restaurant)
            
            # Apply basic filters first
            if query:
                query_obj = query_obj.filter(
                    Restaurant.name.ilike(f'%{query}%') | 
                    Restaurant.short_description.ilike(f'%{query}%')
                )
            
            if category:
                query_obj = query_obj.filter(Restaurant.cuisine_type.ilike(f'%{category}%'))
            
            # Get all restaurants and filter by distance (simplified approach)
            restaurants = query_obj.limit(limit * 2).offset(offset).all()  # Get more to account for distance filtering
            
            # Filter by distance (simplified - in production you'd use PostGIS or similar)
            nearby_restaurants = []
            for restaurant in restaurants:
                if restaurant.latitude is not None and restaurant.longitude is not None:
                    # Simple distance calculation (Haversine formula would be better)
                    distance = ((restaurant.latitude - lat) ** 2 + (restaurant.longitude - lng) ** 2) ** 0.5
                    if distance <= radius / 69:  # Rough conversion: 1 degree ≈ 69 miles
                        nearby_restaurants.append(restaurant)
                        if len(nearby_restaurants) >= limit:
                            break
                else:
                    # If no coordinates, include the restaurant anyway (fallback behavior)
                    nearby_restaurants.append(restaurant)
                    if len(nearby_restaurants) >= limit:
                        break
            
            return nearby_restaurants[:limit]
            
        except Exception as e:
            logger.error("Failed to search restaurants near location", error=str(e))
            return []
        finally:
            if session:
                session.close()
    
    def get_place_by_id(self, place_id: int) -> Optional[Dict[str, Any]]:
        """Get a place by ID from the consolidated restaurants table."""
        try:
            session = self.get_session()
            restaurant = session.query(Restaurant).filter(Restaurant.id == place_id).first()
            if restaurant:
                place_dict = self._restaurant_to_unified_dict(restaurant)
                return place_dict
            return None
            
        except Exception as e:
            logger.error("Failed to get place by ID", error=str(e), place_id=place_id)
            return None
        finally:
            if session:
                session.close()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics from the consolidated restaurants table."""
        try:
            session = self.get_session()
            
            # Count total restaurants
            total_count = session.query(Restaurant).count()
            
            # Count kosher restaurants
            kosher_count = session.query(Restaurant).filter(Restaurant.is_kosher == True).count()
            
            # Get unique states
            states = session.query(Restaurant.state).distinct().filter(Restaurant.state.isnot(None)).all()
            state_list = [state[0] for state in states if state[0]]
            
            # Get unique categories
            categories = session.query(Restaurant.cuisine_type).distinct().filter(Restaurant.cuisine_type.isnot(None)).all()
            category_list = [cat[0] for cat in categories if cat[0]]
            
            return {
                'total_restaurants': total_count,
                'total_kosher_restaurants': kosher_count,
                'states': state_list,
                'categories': category_list,
                'last_updated': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error("Failed to get statistics", error=str(e))
            return {}
        finally:
            if session:
                session.close()
    
    def _restaurant_to_unified_dict(self, restaurant: Restaurant) -> Dict[str, Any]:
        """Convert restaurant object to unified dictionary format."""
        # Create base restaurant data dictionary
        restaurant_data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'city': restaurant.city,
            'state': restaurant.state,
            'zip_code': restaurant.zip_code,
            'phone_number': restaurant.phone_number,
            'website': restaurant.website,
            'kosher_category': restaurant.kosher_category,
            'listing_type': restaurant.listing_type,
            'hours_of_operation': restaurant.hours_of_operation,
            'hours_json': restaurant.hours_json,
            'hours_last_updated': restaurant.hours_last_updated.isoformat() if restaurant.hours_last_updated else None,
            'short_description': restaurant.short_description,
            'price_range': restaurant.price_range,
            'image_url': restaurant.image_url,
            'latitude': restaurant.latitude,
            'longitude': restaurant.longitude,
            'specials': restaurant.specials or [],
            'is_cholov_yisroel': restaurant.is_cholov_yisroel,
            'is_pas_yisroel': restaurant.is_pas_yisroel,
            'certifying_agency': restaurant.certifying_agency,
            'google_listing_url': restaurant.google_listing_url,
            'created_at': restaurant.created_at.isoformat() if restaurant.created_at else None,
            'updated_at': restaurant.updated_at.isoformat() if restaurant.updated_at else None,
            'current_time_local': restaurant.current_time_local.isoformat() if restaurant.current_time_local else None,
            'timezone': restaurant.timezone,
            'hours_parsed': restaurant.hours_parsed
        }
        
        # Calculate dynamic status based on business hours and current time
        try:
            status_info = get_restaurant_status(restaurant_data)
            restaurant_data.update({
                'status': status_info.get('status', 'unknown'),
                'is_open': status_info.get('is_open', False),
                'status_reason': status_info.get('status_reason', 'Status calculation failed'),
                'next_open_time': status_info.get('next_open_time'),
                'current_time_local': status_info.get('current_time_local'),
                'timezone': status_info.get('timezone', 'UTC'),
                'hours_parsed': status_info.get('hours_parsed', False)
            })
        except Exception as e:
            logger.error(f"Error calculating dynamic status for restaurant {restaurant.name}: {e}")
            # Fallback to stored status if dynamic calculation fails
            restaurant_data.update({
                'status': 'unknown',
                'is_open': False,
                'status_reason': f'Dynamic status calculation failed: {str(e)}',
                'next_open_time': None,
                'current_time_local': None,
                'timezone': 'UTC',
                'hours_parsed': False
            })
        
        return restaurant_data
    
    def get_restaurant_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get restaurant by name."""
        try:
            session = self.get_session()
            restaurant = session.query(Restaurant).filter(Restaurant.name == name).first()
            if restaurant:
                return self._restaurant_to_unified_dict(restaurant)
            return None
        except Exception as e:
            logger.error(f"Error getting restaurant by name {name}: {e}")
            return None
        finally:
            session.close()
    
    def update_restaurant_orb_data(self, restaurant_id: int, address: str, kosher_category: str, certifying_agency: str, extra_kosher_info: str = None) -> bool:
        """Update restaurant with ORB data."""
        try:
            session = self.get_session()
            restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
            if restaurant:
                restaurant.address = address
                restaurant.kosher_category = kosher_category
                restaurant.certifying_agency = certifying_agency
                
                # Update extra kosher information
                if extra_kosher_info:
                    # Parse extra kosher info and update boolean fields
                    extra_info_lower = extra_kosher_info.lower()
                    restaurant.is_cholov_yisroel = 'cholov yisroel' in extra_info_lower
                    restaurant.is_pas_yisroel = 'pas yisroel' in extra_info_lower
                    # Note: Cholov Stam is the default when Cholov Yisroel is not specified
                    if 'cholov stam' in extra_info_lower:
                        restaurant.is_cholov_yisroel = False
                
                restaurant.updated_at = datetime.utcnow()
                session.commit()
                logger.info(f"Updated restaurant {restaurant_id} with ORB data")
                return True
            return False
        except Exception as e:
            logger.error(f"Error updating restaurant {restaurant_id} with ORB data: {e}")
            session.rollback()
            return False
        finally:
            session.close()
    
    def add_restaurant_simple(self, name: str, address: str = None, phone_number: str = None, 
                      kosher_category: str = None, certifying_agency: str = None, extra_kosher_info: str = None, source: str = 'orb') -> bool:
        """Add a new restaurant with basic information (simplified version)."""
        try:
            # Validate required fields
            if not name:
                logger.error("Restaurant name is required")
                return False
            
            # Set default values for required fields
            restaurant_data = {
                'name': name,
                'address': address or 'Address not provided',
                'city': 'City not provided',
                'state': 'State not provided',
                'zip_code': 'ZIP not provided',
                'phone_number': phone_number or 'Phone not provided',
                'kosher_category': kosher_category or 'pareve',
                'listing_type': 'restaurant',
                'certifying_agency': certifying_agency or 'ORB',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                'hours_parsed': False
            }
            
            # Set extra kosher information
            if extra_kosher_info:
                extra_info_lower = extra_kosher_info.lower()
                restaurant_data['is_cholov_yisroel'] = 'cholov yisroel' in extra_info_lower
                restaurant_data['is_pas_yisroel'] = 'pas yisroel' in extra_info_lower
                # Note: Cholov Stam is the default when Cholov Yisroel is not specified
                if 'cholov stam' in extra_info_lower:
                    restaurant_data['is_cholov_yisroel'] = False
            
            return self.add_restaurant(restaurant_data)
            
        except Exception as e:
            logger.error(f"Error adding restaurant {name}: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the database."""
        if self.session:
            self.session.close()
        if self.engine:
            self.engine.dispose()
        logger.info("Database disconnected")
    
    def close(self):
        """Alias for disconnect."""
        self.disconnect() 