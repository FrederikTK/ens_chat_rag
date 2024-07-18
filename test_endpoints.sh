#!/bin/bash

# Build and run the Docker container
docker-compose up --build -d

# Wait for the container to start
sleep 10

# Run tests
echo "Testing /chat endpoint..."
curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d '{"message": "Hello, how are you?"}'

echo -e "\nTesting /extract-urls endpoint..."
curl -X POST "http://localhost:8000/extract-urls"

echo -e "\nTesting /scrape endpoint..."
curl -X POST "http://localhost:8000/scrape" -H "Content-Type: application/json" -d '{"url": "https://sparenergi.dk/, "content": "This is example content."}'

echo -e "\nTesting /summarize endpoint..."
curl -X POST "http://localhost:8000/summarize" -H "Content-Type: application/json" -d '{"url": "https://sparenergi.dk/", "content": "This is some example content to summarize."}'

echo -e "\nTesting /process endpoint..."
curl -X POST "http://localhost:8000/process" -H "Content-Type: application/json" -d '{"document_ids": ["1", "2", "3"]}'

# Stop the Docker container
docker-compose down
