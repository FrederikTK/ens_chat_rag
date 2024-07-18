import requests
import pandas as pd
import numpy as np
from src.utils.logging import log_extraction
from config.config import get_api_credentials_siteimprove, get_api_parameters_siteimprove

def fetch_data(page, page_size):
    api_user, api_key = get_api_credentials_siteimprove()
    base_api_url, params = get_api_parameters_siteimprove(page, page_size)
    api_url = f"{base_api_url}{params['mid']}{params['page']}&{params['page_size']}&{params['period']}&{params['param']}"
    
    try:
        response = requests.get(api_url, auth=(api_user, api_key))
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame.from_dict(data.get('items', []))
        if not df.empty:
            df['last_visited'] = df['last_visited'].str[:10]
            df.to_csv(f'data/raw/site_improve_top{page_size}_page{page}_urls.csv', index=False)
            log_extraction(df['url'].tolist())
            
            # Convert DataFrame to a list of dictionaries and handle numpy types
            result = df.replace({np.nan: None}).to_dict('records')
            return result
        return []
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def main():
    for page in range(1, 2):  # Adjust range as needed for more pages
        fetch_data(page, 1000)

if __name__ == "__main__":
    main()

