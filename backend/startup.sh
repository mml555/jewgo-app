#!/bin/bash

# Install Playwright browsers with dependencies
echo "Installing Playwright browsers..."
playwright install chromium --with-deps

# Start the application
echo "Starting Gunicorn..."
gunicorn --config config/gunicorn.conf.py app:app 