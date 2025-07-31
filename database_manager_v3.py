#!/usr/bin/env python3
"""
Enhanced Database Manager for JewGo App v3
Handles PostgreSQL database operations with SQLAlchemy 1.4
Consolidated to use restaurants table only
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
    """Restaurant model for SQLAlchemy (consolidated table)."""
    __tablename__ = 'restaurants'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address = Column(String(500))
    city = Column(String(100))
    state = Column(String(50))
    zip_code = Column(String(20))
    phone = Column(String(50))
    website = Column(String(500))
    cuisine_type = Column(String(100))
    price_range = Column(String(20))
    rating = Column(Float)
    review_count = Column(Integer)
    # Google Reviews fields
    google_rating = Column(Float)
    google_review_count = Column(Integer)
    google_reviews = Column(Text)  # JSON string of review data
    latitude = Column(Float)
    longitude = Column(Float)
    hours = Column(Text)
    description = Column(Text)
    image_url = Column(String(500))
    is_kosher = Column(Boolean, default=False)
    is_glatt = Column(Boolean, default=False)
    is_cholov_yisroel = Column(Boolean, default=False)
    is_pas_yisroel = Column(Boolean, default=False)
    is_bishul_yisroel = Column(Boolean, default=False)
    is_mehadrin = Column(Boolean, default=False)
    is_hechsher = Column(Boolean, default=False)
    hechsher_details = Column(String(500))
    kosher_type = Column(String(100))  # dairy, meat, pareve
    # Consolidated fields from kosher_places
    kosher_cert_link = Column(String(500))
    detail_url = Column(String(500))
    short_description = Column(Text)
    email = Column(String(255))
    google_listing_url = Column(String(500))
    hours_open = Column(Text)
    category = Column(String(100), default='restaurant')
    status = Column(String(50), default='approved')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
                result = conn.execute("SELECT 1")
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
                restaurant_query = restaurant_query.filter(Restaurant.cuisine_type.ilike(f'%{category}%'))
            if state:
                restaurant_query = restaurant_query.filter(Restaurant.state.ilike(f'%{state}%'))
            if is_kosher is not None:
                restaurant_query = restaurant_query.filter(Restaurant.is_kosher == is_kosher)
            
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
                    Restaurant.description.ilike(f'%{query}%')
                )
            
            if category:
                query_obj = query_obj.filter(Restaurant.cuisine_type.ilike(f'%{category}%'))
            
            # Get all restaurants and filter by distance (simplified approach)
            restaurants = query_obj.limit(limit * 2).offset(offset).all()  # Get more to account for distance filtering
            
            # Filter by distance (simplified - in production you'd use PostGIS or similar)
            nearby_restaurants = []
            for restaurant in restaurants:
                if restaurant.latitude and restaurant.longitude:
                    # Simple distance calculation (Haversine formula would be better)
                    distance = ((restaurant.latitude - lat) ** 2 + (restaurant.longitude - lng) ** 2) ** 0.5
                    if distance <= radius / 69:  # Rough conversion: 1 degree ≈ 69 miles
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
        """Convert Restaurant object to unified dictionary format."""
        return {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'city': restaurant.city,
            'state': restaurant.state,
            'zip_code': restaurant.zip_code,
            'phone_number': restaurant.phone,
            'website': restaurant.website,
            'certifying_agency': restaurant.hechsher_details or 'Unknown',
            'kosher_category': restaurant.kosher_type or restaurant.cuisine_type or 'restaurant',
            'listing_type': restaurant.category or 'restaurant',
            'status': restaurant.status or 'active',
            'hours_of_operation': restaurant.hours_open or restaurant.hours,
            'hours_open': restaurant.hours_open or restaurant.hours,
            'short_description': restaurant.short_description or restaurant.description,
            'price_range': restaurant.price_range,
            'image_url': restaurant.image_url,
            'latitude': restaurant.latitude,
            'longitude': restaurant.longitude,
            'rating': restaurant.rating,
            'review_count': restaurant.review_count,
            'google_rating': restaurant.google_rating or restaurant.rating,
            'google_review_count': restaurant.google_review_count or restaurant.review_count,
            'google_reviews': restaurant.google_reviews,
            'specials': [],
            'is_kosher': restaurant.is_kosher,
            'is_glatt': restaurant.is_glatt,
            'is_cholov_yisroel': restaurant.is_cholov_yisroel,
            'is_pas_yisroel': restaurant.is_pas_yisroel,
            'is_bishul_yisroel': restaurant.is_bishul_yisroel,
            'is_mehadrin': restaurant.is_mehadrin,
            'is_hechsher': restaurant.is_hechsher,
            'kosher_type': restaurant.kosher_type,
            'kosher_cert_link': restaurant.kosher_cert_link,
            'detail_url': restaurant.detail_url,
            'email': restaurant.email,
            'google_listing_url': restaurant.google_listing_url,
            'created_at': restaurant.created_at.isoformat() if restaurant.created_at else None,
            'updated_at': restaurant.updated_at.isoformat() if restaurant.updated_at else None
        } 
    
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
    
    def update_restaurant_orb_data(self, restaurant_id: int, address: str, kosher_type: str, certifying_agency: str, extra_kosher_info: str = None) -> bool:
        """Update restaurant with ORB data."""
        try:
            session = self.get_session()
            restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
            if restaurant:
                restaurant.address = address
                restaurant.kosher_type = kosher_type
                restaurant.hechsher_details = certifying_agency
                
                # Update extra kosher information
                if extra_kosher_info:
                    # Parse extra kosher info and update boolean fields
                    extra_info_lower = extra_kosher_info.lower()
                    restaurant.is_cholov_yisroel = 'cholov yisroel' in extra_info_lower
                    restaurant.is_pas_yisroel = 'pas yisroel' in extra_info_lower
                    restaurant.is_bishul_yisroel = 'bishul yisroel' in extra_info_lower
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
                      kosher_type: str = None, certifying_agency: str = None, extra_kosher_info: str = None, source: str = 'orb') -> bool:
        """Add a new restaurant with basic information (simplified version)."""
        try:
            session = self.get_session()
            restaurant = Restaurant(
                name=name,
                address=address,
                phone=phone_number,
                kosher_type=kosher_type,
                hechsher_details=certifying_agency,
                is_kosher=True,
                is_hechsher=True
            )
            
            # Set extra kosher information
            if extra_kosher_info:
                extra_info_lower = extra_kosher_info.lower()
                restaurant.is_cholov_yisroel = 'cholov yisroel' in extra_info_lower
                restaurant.is_pas_yisroel = 'pas yisroel' in extra_info_lower
                restaurant.is_bishul_yisroel = 'bishul yisroel' in extra_info_lower
                # Note: Cholov Stam is the default when Cholov Yisroel is not specified
                if 'cholov stam' in extra_info_lower:
                    restaurant.is_cholov_yisroel = False
            
            session.add(restaurant)
            session.commit()
            logger.info(f"Added new restaurant: {name}")
            return True
        except Exception as e:
            logger.error(f"Error adding restaurant {name}: {e}")
            session.rollback()
            return False
        finally:
            session.close()
    
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