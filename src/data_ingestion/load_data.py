import sys
import os
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.process_urls import process_urls
from utils.request_load import request_and_load_urls, request_and_load_urls_test
from utils.beautify_url import beautify_url

def scrape_url(url: str) -> Dict[str, Any]:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        content = " ".join([p.text for p in soup.find_all("p")])
        return {"url": url, "content": content}
    except requests.RequestException as e:
        print(f"Error scraping {url}: {str(e)}")
        return None

def scrape_urls(urls: List[str]) -> List[Dict[str, Any]]:
    return [result for url in urls if (result := scrape_url(url)) is not None]

def process_data(prod: bool = True, llm_type: str = "gpt3") -> None:
    print("Running the full URL processing and summarization pipeline...")

    url_pattern = 'data/raw/*.csv'
    urls_metadata = request_and_load_urls(url_pattern) if prod else request_and_load_urls_test(url_pattern)

    for metadata in urls_metadata:
        if 'content' not in metadata or not metadata['content']:
            scraped_data = beautify_url(metadata)
            if scraped_data:
                metadata.update(scraped_data)

    process_urls(llm_type, urls_metadata)
    print(f"Summaries processed and saved using {llm_type}.")

if __name__ == "__main__":
    prod_mode = True
    llm_type = "gpt3"

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.lower() == 'false':
                prod_mode = False
            elif arg.lower() in ["gpt4", "gpt3", "sagemaker", "llama3_8b", "llama3_70b", "munin7b"]:
                llm_type = arg.lower()

    process_data(prod=prod_mode, llm_type=llm_type)
