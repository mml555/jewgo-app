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
    cuisine_type = Column(String(100))
    price_range = Column(String(20))
    rating = Column(Float)
    review_count = Column(Integer)
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
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class EnhancedDatabaseManager:
    """Enhanced database manager with SQLAlchemy 1.4 support."""
    
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
                session.close()
            return False
    
    def _validate_against_fpt_feed(self, restaurant_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate restaurant data against FPT feed to avoid misassignments.
        This is a placeholder for the actual FPT feed validation logic.
        """
        # TODO: Implement actual FPT feed validation
        # For now, return the data as-is
        return restaurant_data
    
    def get_restaurants(self, limit: int = 100, offset: int = 0) -> List[Restaurant]:
        """Get restaurants from the database."""
        try:
            session = self.get_session()
            restaurants = session.query(Restaurant).limit(limit).offset(offset).all()
            session.close()
            return restaurants
        except Exception as e:
            logger.error("Failed to get restaurants", error=str(e))
            return []
    
    def search_restaurants(self, query: str, limit: int = 50) -> List[Restaurant]:
        """Search restaurants by name or description."""
        try:
            session = self.get_session()
            restaurants = session.query(Restaurant).filter(
                Restaurant.name.ilike(f'%{query}%') | 
                Restaurant.description.ilike(f'%{query}%')
            ).limit(limit).all()
            session.close()
            return restaurants
        except Exception as e:
            logger.error("Failed to search restaurants", error=str(e))
            return []
    
    def get_restaurant_by_id(self, restaurant_id: int) -> Optional[Restaurant]:
        """Get a restaurant by ID."""
        try:
            session = self.get_session()
            restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
            session.close()
            return restaurant
        except Exception as e:
            logger.error("Failed to get restaurant by ID", error=str(e), restaurant_id=restaurant_id)
            return None
    
    def update_restaurant(self, restaurant_id: int, update_data: Dict[str, Any]) -> bool:
        """Update a restaurant in the database."""
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
                session.close()
            return False
    
    def delete_restaurant(self, restaurant_id: int) -> bool:
        """Delete a restaurant from the database."""
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
                session.close()
            return False
    
    def close(self):
        """Close database connections."""
        if self.session:
            self.session.close()
        if self.engine:
            self.engine.dispose()
        logger.info("Database connections closed") 