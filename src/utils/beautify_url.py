import requests
from datetime import datetime
from bs4 import BeautifulSoup
from utils.num_tokens import num_tokens_from_string

def beautify_url(row):
    """Helper function to process each URL and handle web requests, using BeautifulSoup for HTML parsing."""
    url = row['url']
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        page_content = " ".join([p.text for p in soup.find_all("p")])

        error = None
    except requests.RequestException as e:
        page_content = ""
        error = str(e)

    return {
        "id": row['id'],
        "url": url,
        "title": row['title'],
        "time_requested": datetime.now().isoformat(),
        "content": page_content,
        "error": error,
        "num_tokens": num_tokens_from_string(page_content, "cl100k_base"),
    }
