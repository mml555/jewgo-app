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
echo "Build output directory: $(pwd)/.next"
ls -la .next/ 2>/dev/null || echo "No .next directory found"

echo "=== Creating out directory for Cloudflare Pages ==="
mkdir -p out

# Copy static files from .next to out
if [ -d ".next/static" ]; then
    echo "Copying static files..."
    cp -r .next/static out/
fi

if [ -d ".next/server" ]; then
    echo "Copying server files..."
    cp -r .next/server out/
fi

if [ -d ".next/trace" ]; then
    echo "Copying trace files..."
    cp -r .next/trace out/
fi

# Copy any other necessary files
if [ -f ".next/BUILD_ID" ]; then
    cp .next/BUILD_ID out/
fi

echo "Build output prepared in: $(pwd)/out"
ls -la out/ 2>/dev/null || echo "No out directory found" 