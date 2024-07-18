import pandas as pd
import glob
from utils.beautify_url import beautify_url

def request_and_load_urls(csv_file_pattern):
    """Load URLs from CSV files matching a pattern, make web requests, and prepare metadata."""
    urls_metadata = []
    for csv_file in glob.glob(csv_file_pattern):
        df = pd.read_csv(csv_file)
        for index, row in df.iterrows():
            metadata = beautify_url(row)
            urls_metadata.append(metadata)
    return urls_metadata

def request_and_load_urls_test(csv_file_pattern, search_ids=['1954729275902597002']):
    """Load only rows for specific ids filter in CSV file found for testing."""
    csv_file = next(iter(glob.glob(csv_file_pattern)), None)
    if csv_file:
        df = pd.read_csv(csv_file)
        # Ensure IDs in DataFrame are treated as strings for comparison
        df['id'] = df['id'].astype(str)
        # Filter rows where 'id' is in the list of search_ids
        mask = df['id'].isin([str(id) for id in search_ids])  # Convert search_ids to string if necessary
        specific_searches = df[mask]
        if not specific_searches.empty:
            # Process each matched row
            metadata = [beautify_url(row) for index, row in specific_searches.iterrows()]
            return metadata
    return []