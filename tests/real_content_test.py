import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.data_ingestion.load_data import scrape_url, scrape_urls
from src.utils.request_load import request_and_load_urls
from src.utils.process_urls import process_urls

import requests
import json
import time

import logging
import traceback

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

BASE_URL = "http://app:8000"

def call_endpoint(endpoint, method, data):
    response = requests.request(
        method,
        f"{BASE_URL}{endpoint}",
        headers={"Content-Type": "application/json"},
        data=json.dumps(data)
    )
    return response.json()

def test_extraction(limit=5):
    print("Testing URL extraction...")
    logger.debug("Starting URL extraction")
    url_pattern = 'data/raw/*.csv'
    try:
        logger.debug(f"Calling request_and_load_urls with pattern: {url_pattern}")
        urls_metadata = request_and_load_urls(url_pattern, limit)
        logger.debug(f"request_and_load_urls returned {len(urls_metadata)} items")
        print(f"Extracted {len(urls_metadata)} URLs")
        return urls_metadata  # No need to slice here as limit is applied in request_and_load_urls
    except Exception as e:
        logger.error(f"Error in test_extraction: {str(e)}")
        logger.error(traceback.format_exc())
        return []

# In the main function:
urls_metadata = test_extraction(5)  # Limit to 5 URLs

def test_scraping(urls_metadata):
    print("Testing web scraping...")
    scraped_content = []
    for metadata in urls_metadata:
        result = scrape_url(metadata['url'])
        if result:
            scraped_content.append(result)
            print(f"Scraped content from {metadata['url']}")
    return scraped_content

def test_summarization(scraped_content):
    print("Testing summarization...")
    summaries = []
    for content in scraped_content:
        if content and 'content' in content:
            result = call_endpoint("/summarize", "POST", {"url": content['url'], "content": content['content']})
            summaries.append({"url": content['url'], "summary": result.get('summary', '')})
            print(f"Generated summary for {content['url']}")
        else:
            print(f"Skipping invalid content: {content}")
    return summaries

def test_indexing(summaries):
    print("Testing indexing...")
    for summary in summaries:
        result = call_endpoint("/process-and-index", "POST", {"content": summary['summary'], "url": summary['url']})
        print(f"Indexed content for {summary['url']}: {result}")
    time.sleep(5)  # Allow some time for indexing to complete

def test_search():
    print("Testing search functionality...")
    queries = [
        "Kan du give mig nogle tips til at spare på energien i hjemmet?",
        "Hvad er de mest energieffektive hvidevarer?",
        "Hvordan kan jeg reducere mit CO2-fodaftryk?"
    ]
    for query in queries:
        result = call_endpoint("/search", "POST", {"query": query})
        print(f"Search results for '{query}':")
        for item in result.get('results', []):
            print(f"  - Content: {item['content'][:100]}...")
            print(f"    URL: {item['url']}")
            print(f"    Score: {item['score']}")
        print()

def test_chat():
    print("Testing chat functionality...")
    questions = [
        "Kan du give mig nogle tips til at spare på energien i hjemmet?",
        "Hvad er de mest energieffektive hvidevarer?",
        "Hvordan kan jeg reducere mit CO2-fodaftryk?"
    ]
    for question in questions:
        result = call_endpoint("/chat", "POST", {"message": question})
        print(f"Chat response for '{question}':")
        print(result.get('response', ''))
        print()

def main():
    urls_metadata = test_extraction()
    scraped_content = test_scraping(urls_metadata)
    summaries = test_summarization(scraped_content)
    test_indexing(summaries)
    test_search()
    test_chat()

if __name__ == "__main__":
    main()


