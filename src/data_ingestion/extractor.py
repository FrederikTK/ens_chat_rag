# src/data_ingestion/extractor.py
import requests
import pandas as pd
from src.utils.logging import log_extraction
from config.config import get_api_credentials_siteimprove, get_api_parameters_siteimprove

def fetch_data(page, page_size):
    api_user, api_key = get_api_credentials_siteimprove()
    base_api_url, params = get_api_parameters_siteimprove(page, page_size)
    api_url = f"{base_api_url}{params['mid']}{params['page']}&{params['page_size']}&{params['period']}&{params['param']}"
    response = requests.get(api_url, auth=(api_user, api_key))
    response.raise_for_status()

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame.from_dict(data.get('items'))
        df['last_visited'] = df['last_visited'].str[:10]
        df.to_csv(f'data/raw/site_improve_top{page_size}_page{page}_urls.csv', index=False)
        log_extraction(df['url'].tolist())
        return df
    return None

def main():
    for page in range(1, 2):  # Adjust range as needed for more pages
        fetch_data(page, 1000)

if __name__ == "__main__":
    main()
