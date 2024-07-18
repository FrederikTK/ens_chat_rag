#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    COLOR=$1
    MESSAGE=$2
    echo -e "${COLOR}${MESSAGE}${NC}"
}

# Function to run a test and check its output
run_test() {
    ENDPOINT=$1
    METHOD=$2
    DATA=$3
    EXPECTED=$4
    
    print_color $YELLOW "\nTesting ${ENDPOINT} endpoint..."
    RESPONSE=$(curl -s -X ${METHOD} "http://localhost:8000${ENDPOINT}" \
               -H "Content-Type: application/json" \
               -d "${DATA}")
    
    if echo "$RESPONSE" | grep -q "$EXPECTED"; then
        print_color $GREEN "Test passed for ${ENDPOINT}"
    else
        print_color $RED "Test failed for ${ENDPOINT}"
        echo "Expected to find: $EXPECTED"
        echo "Got: $RESPONSE"
    fi
}

# Build and run the Docker container
print_color $YELLOW "Building and starting Docker containers..."
docker-compose up --build -d

# Wait for the container to start
print_color $YELLOW "Waiting for containers to initialize..."
sleep 15

# Run tests
run_test "/chat" "POST" '{"message": "Hello, how are you?"}' '"response":'
run_test "/extract-urls" "POST" '{}' '"urls":'
run_test "/scrape" "POST" '{"url": "https://sparenergi.dk/", "content": "This is example content."}' '"scraped_data":'
run_test "/summarize" "POST" '{"url": "https://sparenergi.dk/", "content": "This is some example content to summarize."}' '"summary":'
run_test "/process" "POST" '{"document_ids": ["1", "2", "3"]}' '"processed_count":'

# Test vector store functionality
print_color $YELLOW "\nTesting vector store functionality..."
EMBED_RESPONSE=$(curl -s -X POST "http://localhost:8000/embed" \
                 -H "Content-Type: application/json" \
                 -d '{"text": "This is a test document"}')

if echo "$EMBED_RESPONSE" | grep -q '"embedding":'; then
    print_color $GREEN "Embedding test passed"
else
    print_color $RED "Embedding test failed"
    echo "Response: $EMBED_RESPONSE"
fi

SEARCH_RESPONSE=$(curl -s -X POST "http://localhost:8000/search" \
                  -H "Content-Type: application/json" \
                  -d '{"query": "test document"}')

if echo "$SEARCH_RESPONSE" | grep -q '"results":'; then
    print_color $GREEN "Search test passed"
else
    print_color $RED "Search test failed"
    echo "Response: $SEARCH_RESPONSE"
fi

# Stop the Docker container
print_color $YELLOW "\nStopping Docker containers..."
docker-compose down

print_color $GREEN "\nAll tests completed."