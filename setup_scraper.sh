#!/bin/bash

echo "Setting up ORB Kosher Scraper..."
echo "=================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

echo "Python 3 found: $(python3 --version)"

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r scraper_requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
python3 -m playwright install chromium

echo "Setup complete!"
echo ""
echo "To test the scraper, run:"
echo "python3 test_scraper.py"
echo ""
echo "To run the full scraper, run:"
echo "python3 orb_kosher_scraper.py" 