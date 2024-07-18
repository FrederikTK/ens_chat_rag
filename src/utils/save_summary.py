# src/utils/save_summary.py
import json
import os

def save_summary(summary, filename):
    """Saves a single summary to a JSON file with UTF-8 encoding and non-ASCII characters."""
    os.makedirs('data/processed/json_files/', exist_ok=True)  # Ensure directory exists
    file_path = os.path.join('data/processed/json_files/', f'{filename}.json')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=4, ensure_ascii=False)
