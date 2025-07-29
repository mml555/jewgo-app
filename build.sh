#!/bin/bash
set -e

echo "Building JewGo app..."
cd jewgo-frontend
npm install
npm run build
echo "Build completed successfully!" 