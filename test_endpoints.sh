#!/bin/bash

BASE_URL="http://app:8000"

# Function to test an endpoint
test_endpoint() {
    endpoint=$1
    method=$2
    data=$3
    echo "Testing $endpoint..."
    response=$(curl -s -X $method "$BASE_URL$endpoint" \
                -H "Content-Type: application/json" \
                -d "$data")
    echo "Response: $response"
    echo
}

# Test endpoints
test_endpoint "/chat" "POST" '{"message": "Hello, how are you?"}'
test_endpoint "/extract-urls" "POST" '{}'
test_endpoint "/scrape" "POST" '{"url": "https://sparenergi.dk/privat/spar-energi-i-hverdagen", "content": "Sample content"}'
test_endpoint "/summarize" "POST" '{"url": "https://sparenergi.dk/privat/spar-energi-i-hverdagen", "content": "This is a long text that needs summarization."}'
test_endpoint "/process-and-index" "POST" '{"url": "https://sparenergi.dk/privat/spar-energi-i-hverdagen", "content": "This is a sample document to be processed and indexed."}'
test_endpoint "/search" "POST" '{"query": "gi mig gode råd"}'

echo "All tests completed."