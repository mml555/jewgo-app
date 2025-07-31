#!/usr/bin/env python3
"""
Setup script for ORB Kosher Scraper
Installs dependencies and initializes the scraper environment.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major != 3 or version.minor != 11:
        logger.error(f"Python 3.11 required, but found {version.major}.{version.minor}")
        return False
    logger.info(f"Python version {version.major}.{version.minor} is compatible")
    return True

def install_requirements():
    """Install required packages."""
    try:
        logger.info("Installing requirements...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "orb_scraper_requirements.txt"
        ])
        logger.info("Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install requirements: {e}")
        return False

def install_playwright_browsers():
    """Install Playwright browsers."""
    try:
        logger.info("Installing Playwright browsers...")
        subprocess.check_call([
            sys.executable, "-m", "playwright", "install", "chromium"
        ])
        logger.info("Playwright browsers installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install Playwright browsers: {e}")
        return False

def check_env_file():
    """Check if .env file exists and has required variables."""
    env_file = Path(".env")
    if not env_file.exists():
        logger.warning(".env file not found")
        logger.info("Please create a .env file with your DATABASE_URL")
        return False
    
    # Load and check environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        logger.error("DATABASE_URL not found in .env file")
        return False
    
    logger.info("Environment variables loaded successfully")
    return True

def test_database_connection():
    """Test database connection."""
    try:
        from dotenv import load_dotenv
        import psycopg2
        
        load_dotenv()
        database_url = os.getenv("DATABASE_URL")
        
        if not database_url:
            logger.error("DATABASE_URL not set")
            return False
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        
        logger.info("Database connection test successful")
        return True
        
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False

def create_env_template():
    """Create .env template file."""
    env_template = """# ORB Kosher Scraper Environment Variables
# Copy this file to .env and fill in your values

# Neon PostgreSQL Database URL
DATABASE_URL=postgresql://username:password@ep-something.neon.tech/dbname?sslmode=require

# Optional: Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO
"""
    
    with open(".env.template", "w") as f:
        f.write(env_template)
    
    logger.info("Created .env.template file")

def main():
    """Main setup function."""
    logger.info("Starting ORB Kosher Scraper setup...")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Install Playwright browsers
    if not install_playwright_browsers():
        sys.exit(1)
    
    # Create .env template if it doesn't exist
    if not Path(".env").exists():
        create_env_template()
        logger.info("Please configure your .env file and run setup again")
        sys.exit(0)
    
    # Check environment variables
    if not check_env_file():
        sys.exit(1)
    
    # Test database connection
    if not test_database_connection():
        sys.exit(1)
    
    logger.info("ORB Kosher Scraper setup completed successfully!")
    logger.info("You can now run: python orb_scraper.py")

if __name__ == "__main__":
    main() 