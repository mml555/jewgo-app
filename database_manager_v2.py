#!/usr/bin/env python3
"""
Enhanced Database Manager for JewGo App
Handles PostgreSQL database operations with SQLAlchemy 1.4
"""

import os
import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
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
    """Restaurant model for SQLAlchemy."""
    __tablename__ = 'restaurants'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address = Column(String(500))
    city = Column(String(100))
    state = Column(String(50))
    zip_code = Column(String(20))
    phone = Column(String(50))
    website = Column(String(500))
    description = Column(Text)
    cuisine_type = Column(String(100))
    price_range = Column(String(20))
    rating = Column(Float)
    review_count = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    hours = Column(Text)  # JSON string
    images = Column(Text)  # JSON string
    menu_items = Column(Text)  # JSON string
    specials = Column(Text)  # JSON string
    is_kosher = Column(Boolean, default=False)
    is_vegetarian_friendly = Column(Boolean, default=False)
    is_vegan_friendly = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class EnhancedDatabaseManager:
    """Enhanced database manager with SQLAlchemy 1.4."""
    
    def __init__(self, database_url: str = None):
        """Initialize database manager with connection string."""
        self.database_url = database_url or os.environ.get('DATABASE_URL')
        
        # Validate that DATABASE_URL is provided
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is required")
        
        # Handle PostgreSQL URL format for SQLAlchemy 1.4
        if self.database_url.startswith('postgres://'):
            self.database_url = self.database_url.replace('postgres://', 'postgresql://', 1)
        
        logger.info("Database manager initialized", database_url=self.database_url[:50] + "...")
        
        # Initialize SQLAlchemy components
        self.engine = None
        self.SessionLocal = None
        self.session = None
    
    def connect(self) -> bool:
        """Connect to the database and create tables if they don't exist."""
        try:
            # Create the engine with standard SQLAlchemy 1.4 + psycopg2-binary
            self.engine = create_engine(self.database_url, echo=False)
            
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
            logger.error("Failed to connect to database", error=str(e), database_url=self.database_url)
            return False
    
    def get_session(self) -> Session:
        """Get a database session."""
        if not self.SessionLocal:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.SessionLocal()
    
    def add_restaurant(self, restaurant_data: Dict[str, Any]) -> bool:
        """Add a restaurant to the database."""
        session = None
        try:
            # Validate against FPT feed
            validated_data = self._validate_against_fpt_feed(restaurant_data)
            
            # Create restaurant object
            restaurant = Restaurant(**validated_data)
            
            # Get session and add restaurant
            session = self.get_session()
            session.add(restaurant)
            session.commit()
            
            logger.info("Restaurant added successfully", restaurant_id=restaurant.id, name=restaurant.name)
            return True
            
        except Exception as e:
            logger.error("Failed to add restaurant", error=str(e))
            if session:
                session.rollback()
            return False
        finally:
            if session:
                session.close()
    
    def get_restaurant(self, restaurant_id: int) -> Optional[Restaurant]:
        """Get a restaurant by ID."""
        session = None
        try:
            session = self.get_session()
            restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
            return restaurant
        except Exception as e:
            logger.error("Failed to get restaurant", error=str(e), restaurant_id=restaurant_id)
            return None
        finally:
            if session:
                session.close()
    
    def get_all_restaurants(self) -> List[Restaurant]:
        """Get all restaurants."""
        session = None
        try:
            session = self.get_session()
            restaurants = session.query(Restaurant).all()
            return restaurants
        except Exception as e:
            logger.error("Failed to get all restaurants", error=str(e))
            return []
        finally:
            if session:
                session.close()
    
    def search_restaurants(self, query: str) -> List[Restaurant]:
        """Search restaurants by name or description."""
        session = None
        try:
            session = self.get_session()
            restaurants = session.query(Restaurant).filter(
                Restaurant.name.ilike(f'%{query}%') | 
                Restaurant.description.ilike(f'%{query}%')
            ).all()
            return restaurants
        except Exception as e:
            logger.error("Failed to search restaurants", error=str(e), query=query)
            return []
        finally:
            if session:
                session.close()
    
    def update_restaurant(self, restaurant_id: int, update_data: Dict[str, Any]) -> bool:
        """Update a restaurant."""
        session = None
        try:
            session = self.get_session()
            restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
            
            if not restaurant:
                logger.warning("Restaurant not found for update", restaurant_id=restaurant_id)
                return False
            
            # Update fields
            for key, value in update_data.items():
                if hasattr(restaurant, key):
                    setattr(restaurant, key, value)
            
            restaurant.updated_at = datetime.utcnow()
            session.commit()
            
            logger.info("Restaurant updated successfully", restaurant_id=restaurant_id)
            return True
            
        except Exception as e:
            logger.error("Failed to update restaurant", error=str(e), restaurant_id=restaurant_id)
            if session:
                session.rollback()
            return False
        finally:
            if session:
                session.close()
    
    def delete_restaurant(self, restaurant_id: int) -> bool:
        """Delete a restaurant."""
        session = None
        try:
            session = self.get_session()
            restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
            
            if not restaurant:
                logger.warning("Restaurant not found for deletion", restaurant_id=restaurant_id)
                return False
            
            session.delete(restaurant)
            session.commit()
            
            logger.info("Restaurant deleted successfully", restaurant_id=restaurant_id)
            return True
            
        except Exception as e:
            logger.error("Failed to delete restaurant", error=str(e), restaurant_id=restaurant_id)
            if session:
                session.rollback()
            return False
        finally:
            if session:
                session.close()
    
    def get_restaurant_stats(self) -> Dict[str, Any]:
        """Get restaurant statistics."""
        session = None
        try:
            session = self.get_session()
            
            total_restaurants = session.query(Restaurant).count()
            kosher_restaurants = session.query(Restaurant).filter(Restaurant.is_kosher == True).count()
            vegetarian_restaurants = session.query(Restaurant).filter(Restaurant.is_vegetarian_friendly == True).count()
            vegan_restaurants = session.query(Restaurant).filter(Restaurant.is_vegan_friendly == True).count()
            
            return {
                'total_restaurants': total_restaurants,
                'kosher_restaurants': kosher_restaurants,
                'vegetarian_restaurants': vegetarian_restaurants,
                'vegan_restaurants': vegan_restaurants
            }
            
        except Exception as e:
            logger.error("Failed to get restaurant stats", error=str(e))
            return {}
        finally:
            if session:
                session.close()
    
    def _validate_against_fpt_feed(self, restaurant_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate restaurant data against FPT feed to avoid misassignments.
        This is a placeholder for the actual FPT validation logic.
        """
        # TODO: Implement actual FPT feed validation
        # For now, just return the data as-is
        return restaurant_data 