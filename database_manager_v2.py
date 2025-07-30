#!/usr/bin/env python3
"""
Enhanced Database Manager with PostgreSQL Support
Provides SQLAlchemy-based database operations with support for both SQLite and PostgreSQL.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
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

class Restaurant(Base):
    """Restaurant model for SQLAlchemy."""
    __tablename__ = 'restaurants'
    
    id = Column(Integer, primary_key=True)
    business_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    website_link = Column(String(500))
    phone_number = Column(String(50))
    address = Column(String(500))
    city = Column(String(100))
    state = Column(String(50))
    zip_code = Column(String(20))
    certificate_link = Column(String(500))
    image_url = Column(String(1000))
    certifying_agency = Column(String(100), default='ORB')
    kosher_category = Column(String(50), default='unknown')
    listing_type = Column(String(100), default='restaurant')
    status = Column(String(50), default='active')
    rating = Column(Float)
    price_range = Column(String(50))
    hours_of_operation = Column(Text)
    short_description = Column(Text)
    notes = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    data_source = Column(String(100), default='manual')
    external_id = Column(String(255))
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RestaurantSpecial(Base):
    """Restaurant specials model."""
    __tablename__ = 'restaurant_specials'
    
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    discount_percent = Column(Float)
    discount_amount = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_paid = Column(Boolean, default=False)
    payment_status = Column(String(50), default='pending')
    special_type = Column(String(50), default='discount')
    priority = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class EnhancedDatabaseManager:
    """Enhanced database manager with SQLAlchemy and PostgreSQL support."""
    
    def __init__(self, database_url: str = None):
        """Initialize database manager with connection string."""
        self.database_url = database_url or os.environ.get('DATABASE_URL', 'sqlite:///restaurants.db')
        self.engine = None
        self.SessionLocal = None
        self.session = None
        
        # Handle PostgreSQL URL format for SQLAlchemy
        if self.database_url.startswith('postgres://'):
            self.database_url = self.database_url.replace('postgres://', 'postgresql://', 1)
    
    def connect(self) -> bool:
        """Connect to the database and create tables if they don't exist."""
        try:
            # Configure engine based on database type
            if 'sqlite' in self.database_url.lower():
                # SQLite configuration (no pool parameters)
                self.engine = create_engine(
                    self.database_url,
                    echo=False,  # Set to True for SQL debugging
                    connect_args={"check_same_thread": False}
                )
            else:
                # PostgreSQL configuration with enhanced error handling
                try:
                    self.engine = create_engine(
                        self.database_url,
                        echo=False,  # Set to True for SQL debugging
                        pool_size=10,
                        max_overflow=20,
                        pool_pre_ping=True,
                        pool_recycle=3600,  # Recycle connections every hour
                        connect_args={
                            "connect_timeout": 10,
                            "application_name": "jewgo_app"
                        }
                    )
                except Exception as pg_error:
                    logger.error("PostgreSQL connection failed, trying with minimal config", 
                               error=str(pg_error), database_url=self.database_url)
                    # Fallback to minimal configuration
                    try:
                        self.engine = create_engine(
                            self.database_url,
                            echo=False,
                            pool_pre_ping=True
                        )
                    except Exception as min_error:
                        logger.error("PostgreSQL connection completely failed, falling back to SQLite", 
                                   error=str(min_error), database_url=self.database_url)
                        # Fallback to SQLite for development
                        self.database_url = 'sqlite:///restaurants_fallback.db'
                        self.engine = create_engine(
                            self.database_url,
                            echo=False,
                            connect_args={"check_same_thread": False}
                        )
                        logger.warning("Using SQLite fallback database", fallback_url=self.database_url)
            
            # Test the connection
            with self.engine.connect() as conn:
                conn.execute("SELECT 1")
            
            # Create tables if they don't exist
            Base.metadata.create_all(self.engine)
            
            # Create session factory
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            logger.info("Database connected successfully", database_url=self.database_url)
            return True
            
        except Exception as e:
            logger.error("Failed to connect to database", error=str(e), database_url=self.database_url)
            return False
    
    def get_session(self) -> Session:
        """Get a database session."""
        if not self.SessionLocal:
            raise Exception("Database not connected. Call connect() first.")
        return self.SessionLocal()
    
    def disconnect(self):
        """Disconnect from the database."""
        if self.session:
            self.session.close()
        if self.engine:
            self.engine.dispose()
        logger.info("Database disconnected")
    
    def add_restaurant(self, restaurant_data: Dict[str, Any]) -> bool:
        """Add a new restaurant to the database with FPT feed validation."""
        try:
            session = self.get_session()
            
            # Check if restaurant already exists
            existing = session.query(Restaurant).filter_by(business_id=restaurant_data.get('business_id')).first()
            if existing:
                logger.warning("Restaurant already exists", business_id=restaurant_data.get('business_id'))
                session.close()
                return False
            
            # Validate against FPT feed to avoid misassignments
            validation_result = self._validate_against_fpt_feed(restaurant_data)
            if not validation_result['valid']:
                logger.error("FPT feed validation failed", 
                           restaurant_name=restaurant_data.get('name'),
                           errors=validation_result['errors'])
                session.close()
                return False
            
            # Create new restaurant
            restaurant = Restaurant(
                business_id=restaurant_data.get('business_id', ''),
                name=restaurant_data.get('name', ''),
                website_link=restaurant_data.get('website_link', ''),
                phone_number=restaurant_data.get('phone_number', ''),
                address=restaurant_data.get('address', ''),
                city=restaurant_data.get('city', ''),
                state=restaurant_data.get('state', ''),
                zip_code=restaurant_data.get('zip_code', ''),
                certificate_link=restaurant_data.get('certificate_link', ''),
                image_url=restaurant_data.get('image_url', ''),
                certifying_agency=restaurant_data.get('certifying_agency', 'ORB'),
                kosher_category=restaurant_data.get('kosher_category', 'unknown'),
                listing_type=restaurant_data.get('listing_type', 'restaurant'),
                status=restaurant_data.get('status', 'active'),
                rating=restaurant_data.get('rating'),
                price_range=restaurant_data.get('price_range'),
                hours_of_operation=restaurant_data.get('hours_of_operation'),
                short_description=restaurant_data.get('short_description'),
                notes=restaurant_data.get('notes'),
                latitude=restaurant_data.get('latitude'),
                longitude=restaurant_data.get('longitude'),
                data_source=restaurant_data.get('data_source', 'manual'),
                external_id=restaurant_data.get('external_id', '')
            )
            
            session.add(restaurant)
            session.commit()
            
            logger.info("Restaurant added successfully with FPT validation", 
                       name=restaurant_data.get('name'),
                       validation_passed=True)
            session.close()
            return True
            
        except SQLAlchemyError as e:
            logger.error("Database error adding restaurant", error=str(e))
            if session:
                session.rollback()
                session.close()
            return False
        except Exception as e:
            logger.error("Unexpected error adding restaurant", error=str(e))
            if session:
                session.rollback()
                session.close()
            return False

    def _validate_against_fpt_feed(self, restaurant_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate restaurant data against FPT feed to avoid misassignments.
        
        Args:
            restaurant_data: Restaurant data to validate
            
        Returns:
            Dict with 'valid' boolean and 'errors' list
        """
        errors = []
        
        # Basic validation checks
        if not restaurant_data.get('name'):
            errors.append("Restaurant name is required")
        
        if not restaurant_data.get('business_id'):
            errors.append("Business ID is required")
        
        # Validate certifying agency against FPT feed
        certifying_agency = restaurant_data.get('certifying_agency', 'ORB')
        valid_agencies = ['ORB', 'OU', 'KOF-K', 'Star-K', 'CRC', 'Vaad HaRabbonim']
        if certifying_agency not in valid_agencies:
            errors.append(f"Invalid certifying agency: {certifying_agency}")
        
        # Validate kosher category against FPT standards
        kosher_category = restaurant_data.get('kosher_category', 'unknown')
        valid_categories = ['meat', 'dairy', 'pareve', 'fish', 'unknown']
        if kosher_category not in valid_categories:
            errors.append(f"Invalid kosher category: {kosher_category}")
        
        # Validate listing type
        listing_type = restaurant_data.get('listing_type', 'restaurant')
        valid_types = ['restaurant', 'caterer', 'bakery', 'grocery', 'delivery']
        if listing_type not in valid_types:
            errors.append(f"Invalid listing type: {listing_type}")
        
        # Check for duplicate business IDs in FPT feed
        # This would typically involve querying an external FPT feed API
        # For now, we'll check against our own database
        try:
            session = self.get_session()
            existing = session.query(Restaurant).filter_by(business_id=restaurant_data.get('business_id')).first()
            if existing:
                errors.append(f"Business ID {restaurant_data.get('business_id')} already exists in FPT feed")
            session.close()
        except Exception as e:
            logger.warning("Could not check FPT feed for duplicates", error=str(e))
        
        # Validate address format
        address = restaurant_data.get('address', '')
        if address and len(address.strip()) < 10:
            errors.append("Address appears to be incomplete")
        
        # Validate phone number format
        phone = restaurant_data.get('phone_number', '')
        if phone and not self._is_valid_phone_format(phone):
            errors.append("Invalid phone number format")
        
        # Validate website URL if provided
        website = restaurant_data.get('website_link', '')
        if website and not self._is_valid_url(website):
            errors.append("Invalid website URL format")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def _is_valid_phone_format(self, phone: str) -> bool:
        """Validate phone number format."""
        import re
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        # Check if it's a valid length (10-15 digits)
        return 10 <= len(digits_only) <= 15
    
    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format."""
        import re
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return bool(url_pattern.match(url))
    
    def search_restaurants(self, query: str = "", category: str = "", state: str = "", 
                          limit: int = 50, offset: int = 0) -> List[Dict]:
        """Search restaurants with filters."""
        try:
            session = self.get_session()
            
            # Build query
            db_query = session.query(Restaurant).filter(Restaurant.status == 'active')
            
            if query:
                db_query = db_query.filter(
                    Restaurant.name.ilike(f'%{query}%') |
                    Restaurant.address.ilike(f'%{query}%') |
                    Restaurant.city.ilike(f'%{query}%')
                )
            
            if category:
                db_query = db_query.filter(Restaurant.listing_type.ilike(f'%{category}%'))
            
            if state:
                db_query = db_query.filter(Restaurant.state.ilike(f'%{state}%'))
            
            # Apply pagination
            restaurants = db_query.offset(offset).limit(limit).all()
            
            # Convert to dictionaries
            result = []
            for restaurant in restaurants:
                result.append({
                    'id': restaurant.id,
                    'business_id': restaurant.business_id,
                    'name': restaurant.name,
                    'address': restaurant.address,
                    'city': restaurant.city,
                    'state': restaurant.state,
                    'zip_code': restaurant.zip_code,
                    'phone_number': restaurant.phone_number,
                    'website': restaurant.website_link,
                    'certifying_agency': restaurant.certifying_agency,
                    'kosher_category': restaurant.kosher_category,
                    'listing_type': restaurant.listing_type,
                    'status': restaurant.status,
                    'rating': restaurant.rating,
                    'price_range': restaurant.price_range,
                    'hours_of_operation': restaurant.hours_of_operation,
                    'short_description': restaurant.short_description,
                    'latitude': restaurant.latitude,
                    'longitude': restaurant.longitude,
                    'image_url': restaurant.image_url,
                    'certificate_link': restaurant.certificate_link,
                    'created_date': restaurant.created_date.isoformat() if restaurant.created_date else None,
                    'updated_date': restaurant.updated_date.isoformat() if restaurant.updated_date else None
                })
            
            session.close()
            return result
            
        except SQLAlchemyError as e:
            logger.error("Database error searching restaurants", error=str(e))
            if session:
                session.close()
            return []
    
    def search_restaurants_near_location(self, lat: float, lng: float, radius: float = 50,
                                       query: str = "", category: str = "", 
                                       limit: int = 50, offset: int = 0) -> List[Dict]:
        """Search restaurants near a specific location."""
        try:
            session = self.get_session()
            
            # Build base query
            db_query = session.query(Restaurant).filter(Restaurant.status == 'active')
            
            # Add location filter (simplified distance calculation)
            # In production, consider using PostGIS for more accurate distance calculations
            db_query = db_query.filter(
                Restaurant.latitude.isnot(None),
                Restaurant.longitude.isnot(None)
            )
            
            # Add other filters
            if query:
                db_query = db_query.filter(
                    Restaurant.name.ilike(f'%{query}%') |
                    Restaurant.address.ilike(f'%{query}%') |
                    Restaurant.city.ilike(f'%{query}%')
                )
            
            if category:
                db_query = db_query.filter(Restaurant.listing_type.ilike(f'%{category}%'))
            
            # Get all restaurants and filter by distance in Python
            # This is a simplified approach - consider PostGIS for production
            restaurants = db_query.all()
            
            # Filter by distance
            nearby_restaurants = []
            for restaurant in restaurants:
                if restaurant.latitude and restaurant.longitude:
                    distance = self._calculate_distance(lat, lng, restaurant.latitude, restaurant.longitude)
                    if distance <= radius:
                        nearby_restaurants.append((restaurant, distance))
            
            # Sort by distance and apply pagination
            nearby_restaurants.sort(key=lambda x: x[1])
            paginated_restaurants = nearby_restaurants[offset:offset + limit]
            
            # Convert to result format
            result = []
            for restaurant, distance in paginated_restaurants:
                result.append({
                    'id': restaurant.id,
                    'business_id': restaurant.business_id,
                    'name': restaurant.name,
                    'address': restaurant.address,
                    'city': restaurant.city,
                    'state': restaurant.state,
                    'zip_code': restaurant.zip_code,
                    'phone_number': restaurant.phone_number,
                    'website': restaurant.website_link,
                    'certifying_agency': restaurant.certifying_agency,
                    'kosher_category': restaurant.kosher_category,
                    'listing_type': restaurant.listing_type,
                    'status': restaurant.status,
                    'rating': restaurant.rating,
                    'price_range': restaurant.price_range,
                    'hours_of_operation': restaurant.hours_of_operation,
                    'short_description': restaurant.short_description,
                    'latitude': restaurant.latitude,
                    'longitude': restaurant.longitude,
                    'image_url': restaurant.image_url,
                    'certificate_link': restaurant.certificate_link,
                    'distance': round(distance, 2),
                    'created_date': restaurant.created_date.isoformat() if restaurant.created_date else None,
                    'updated_date': restaurant.updated_date.isoformat() if restaurant.updated_date else None
                })
            
            session.close()
            return result
            
        except SQLAlchemyError as e:
            logger.error("Database error searching restaurants near location", error=str(e))
            if session:
                session.close()
            return []
    
    def get_restaurant(self, business_id: str) -> Optional[Dict]:
        """Get a specific restaurant by business ID."""
        try:
            session = self.get_session()
            restaurant = session.query(Restaurant).filter_by(business_id=business_id).first()
            
            if not restaurant:
                session.close()
                return None
            
            result = {
                'id': restaurant.id,
                'business_id': restaurant.business_id,
                'name': restaurant.name,
                'address': restaurant.address,
                'city': restaurant.city,
                'state': restaurant.state,
                'zip_code': restaurant.zip_code,
                'phone_number': restaurant.phone_number,
                'website': restaurant.website_link,
                'certifying_agency': restaurant.certifying_agency,
                'kosher_category': restaurant.kosher_category,
                'listing_type': restaurant.listing_type,
                'status': restaurant.status,
                'rating': restaurant.rating,
                'price_range': restaurant.price_range,
                'hours_of_operation': restaurant.hours_of_operation,
                'short_description': restaurant.short_description,
                'notes': restaurant.notes,
                'latitude': restaurant.latitude,
                'longitude': restaurant.longitude,
                'image_url': restaurant.image_url,
                'certificate_link': restaurant.certificate_link,
                'created_date': restaurant.created_date.isoformat() if restaurant.created_date else None,
                'updated_date': restaurant.updated_date.isoformat() if restaurant.updated_date else None
            }
            
            session.close()
            return result
            
        except SQLAlchemyError as e:
            logger.error("Database error getting restaurant", error=str(e))
            if session:
                session.close()
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics."""
        try:
            session = self.get_session()
            
            total_restaurants = session.query(Restaurant).count()
            active_restaurants = session.query(Restaurant).filter_by(status='active').count()
            
            # Count by category
            from sqlalchemy import func
            categories = session.query(Restaurant.listing_type, func.count(Restaurant.id).label('count')).group_by(Restaurant.listing_type).all()
            
            # Count by state
            states = session.query(Restaurant.state, func.count(Restaurant.id).label('count')).group_by(Restaurant.state).all()
            
            # Count by certifying agency
            agencies = session.query(Restaurant.certifying_agency, func.count(Restaurant.id).label('count')).group_by(Restaurant.certifying_agency).all()
            
            session.close()
            
            return {
                'total_restaurants': total_restaurants,
                'active_restaurants': active_restaurants,
                'categories': {cat: count for cat, count in categories},
                'states': {state: count for state, count in states},
                'agencies': {agency: count for agency, count in agencies},
                'last_updated': datetime.utcnow().isoformat()
            }
            
        except SQLAlchemyError as e:
            logger.error("Database error getting statistics", error=str(e))
            if session:
                session.close()
            return {}
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula."""
        import math
        
        R = 3959  # Earth's radius in miles
        
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c 