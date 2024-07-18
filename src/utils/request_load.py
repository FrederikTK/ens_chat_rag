import pandas as pd
import glob
import logging
from utils.beautify_url import beautify_url

logger = logging.getLogger(__name__)

def request_and_load_urls(csv_file_pattern, limit=None):
    """Load URLs from CSV files matching a pattern, make web requests, and prepare metadata."""
    logger.debug(f"Starting request_and_load_urls with pattern: {csv_file_pattern}")
    urls_metadata = []
    csv_files = glob.glob(csv_file_pattern)
    logger.debug(f"Found {len(csv_files)} CSV files")
    for csv_file in csv_files:
        logger.debug(f"Processing file: {csv_file}")
        try:
            df = pd.read_csv(csv_file)
            logger.debug(f"Read {len(df)} rows from {csv_file}")
            for index, row in df.iterrows():
                if limit is not None and len(urls_metadata) >= limit:
                    break
                logger.debug(f"Processing row {index}")
                metadata = beautify_url(row)
                urls_metadata.append(metadata)
                logger.debug(f"Added metadata for URL: {metadata.get('url', 'Unknown URL')}")
            if limit is not None and len(urls_metadata) >= limit:
                break
        except Exception as e:
            logger.error(f"Error processing {csv_file}: {str(e)}")
    logger.debug(f"Finished request_and_load_urls, returning {len(urls_metadata)} items")
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