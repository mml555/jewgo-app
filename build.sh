#!/bin/bash
set -e

echo "=== Starting JewGo build process ==="
echo "Current directory: $(pwd)"
echo "Listing contents:"
ls -la

echo "=== Changing to jewgo-frontend directory ==="
cd jewgo-frontend
echo "Current directory: $(pwd)"
echo "Listing contents:"
ls -la

echo "=== Installing dependencies ==="
npm install

echo "=== Building the application ==="
npm run build

echo "=== Build completed successfully! ==="
echo "Build output directory: $(pwd)/out"
ls -la out/ 2>/dev/null || echo "No out directory found, checking .next:"
ls -la .next/ 2>/dev/null || echo "No .next directory found" 