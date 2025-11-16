#!/bin/bash

# FastAPI CRUD Service - Run Script

echo "FastAPI CRUD Service - Quick Start"
echo "=================================="
echo ""

# Check if Docker is available
if command -v docker-compose &> /dev/null; then
    echo "Starting service with Docker Compose..."
    docker-compose up --build
else
    echo "Docker Compose not found. Starting locally..."
    echo ""
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    echo "Installing dependencies..."
    pip install -r requirements.txt
    
    # Run the application
    echo ""
    echo "Starting FastAPI application..."
    echo "API will be available at: http://localhost:8000"
    echo "API docs will be available at: http://localhost:8000/docs"
    echo ""
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
fi

