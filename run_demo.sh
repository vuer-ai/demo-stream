#!/bin/bash

# Run the robot streaming demo

echo "Robot Data Streaming Demo"
echo "========================="
echo ""

# Install dependencies with uv
echo "Installing dependencies with uv..."
cd client
uv sync
cd ..

# Check if datalake is running
if ! curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "Warning: data-manager server is not running on port 8080"
    echo "Please start it with: cd ../data-manager && pnpm dev"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create data directory if it doesn't exist
mkdir -p data

# Run the simulator
echo "Starting robot simulators..."
echo "Press Ctrl+C to stop"
echo ""

cd client && uv run python robot_simulator.py --robots 3 --duration 300 --server ws://localhost:8080/ws

echo ""
echo "Demo complete!"
echo "Data saved to: ./data/"