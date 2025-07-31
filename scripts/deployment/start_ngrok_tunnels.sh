#!/bin/bash

# Start ngrok tunnel for frontend (port 3000)
echo "Starting ngrok tunnel for frontend (port 3000)..."
ngrok http 3000 --log=stdout &
FRONTEND_PID=$!

# Wait a moment for the first tunnel to establish
sleep 3

# Start ngrok tunnel for backend (port 8082)
echo "Starting ngrok tunnel for backend (port 8082)..."
ngrok http 8082 --log=stdout &
BACKEND_PID=$!

# Wait for both tunnels to establish
sleep 5

# Get tunnel URLs
echo "Getting tunnel URLs..."
curl -s http://localhost:4040/api/tunnels | python3 -m json.tool

echo ""
echo "Tunnels started! Check http://localhost:4040 for the dashboard"
echo "Press Ctrl+C to stop all tunnels"

# Wait for user to stop
wait 