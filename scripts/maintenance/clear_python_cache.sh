#!/bin/bash

# Script to clear all Python __pycache__ directories and .pyc files

echo "Clearing all Python __pycache__ directories and .pyc files..."

# Remove all __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} +

# Remove all .pyc files
find . -type f -name "*.pyc" -delete

echo "Python bytecode cache cleared."
echo "If you use a process manager (systemd, pm2, gunicorn, etc.), restart your backend now."