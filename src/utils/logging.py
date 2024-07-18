from datetime import datetime
import json

def log_extraction(urls):
    """Log the extraction time for each URL."""
    try:
        with open('data/logs/extraction_log.json', 'r') as file:
            logs = json.load(file)
    except FileNotFoundError:
        logs = {}

    now = datetime.now().isoformat()
    for url in urls:
        logs[url] = now

    with open('data/logs/extraction_log.json', 'w') as file:
        json.dump(logs, file, indent=4)