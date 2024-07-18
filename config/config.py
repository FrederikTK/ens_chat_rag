# description: API configuration file
import os
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()

def get_api_credentials_siteimprove():
    api_user = os.getenv('SITE_IMPROVE_USER')
    api_key = os.getenv('SITE_IMPROVE_API_KEY')
    return api_user, api_key

def get_api_parameters_siteimprove(page=1, page_size=1000):
    from_time = "20220401"
    today = date.today()
    yesterday = today - timedelta(days=1)
    yesterday_format = yesterday.strftime("%Y%m%d")
    too_time = str(yesterday_format)
    time = from_time + "_" + too_time

    base_api_url = 'https://api.eu.siteimprove.com/v2/sites/29932207338/'
    params = {
        'mid': 'analytics/content/most_popular_pages?',
        'page': f'page={page}',
        'page_size': f'page_size={page_size}',
        'period': f'period={time}',
        'param': 'search_in=url'
    }
    return base_api_url, params

def get_llm_config(llm_type):
    if llm_type == "gpt4":
        return {
            "service": "openai",
            "model": "gpt4-turbo",
            "max_tokens": 1000,
            "temperature": 0.3,
            "prompt": "Skriv et detaljeret resumé af den tilgængelige information, så den kan gemmes som dokumentation og kan forespørges senere, SKRIV PÅ DANSK",
        }
    elif llm_type == "gpt3":
        return {
            "service": "openai",
            "model": "gpt-3.5-turbo",
            "max_tokens": 1000,
            "temperature": 0.3,
            "prompt": "Skriv et detaljeret resumé af den tilgængelige information, så den kan gemmes som dokumentation og kan forespørges senere, SKRIV PÅ DANSK",
        }
    elif llm_type == "gpt4o":
        return {
            "service": "openai",
            "model": "gpt-4o",
            "max_tokens": 1000,
            "temperature": 0.3,
            "prompt": "Skriv et detaljeret resumé af den tilgængelige information, så den kan gemmes som dokumentation og kan forespørges senere, SKRIV PÅ DANSK",
        }
    elif llm_type == "llama3_8b":
        return {
            "service": "localhost",
            "model": "TheBloke/Llama-3-8B-Instruct-GGUF",
            "temperature": 0.3,
            "prompt": "Skriv et detaljeret resumé af den tilgængelige information, så den kan gemmes som dokumentation og kan forespørges senere, SKRIV PÅ DANSK",
        }
    elif llm_type == "llama3_70b":
        return {
            "service": "localhost",
            "model": "MaziyarPanahi/Meta-Llama-3-70B-Instruct-GGUF",
            "temperature": 0.3,
            "prompt": "Skriv et detaljeret resumé af den tilgængelige information, så den kan gemmes som dokumentation og kan forespørges senere, SKRIV PÅ DANSK",
        }
    elif llm_type == "munin7b":
        return {
            "service": "localhost",
            "model": "RJuro/munin-neuralbeagle-7b-GGUF",
            "temperature": 0.2,
            "prompt": "Skriv et detaljeret resumé af den tilgængelige information, så den kan gemmes som dokumentation og kan forespørges senere, SKRIV PÅ DANSK",
        }
    elif llm_type == "sagemaker":
        return {
            "service": "sagemaker",
            "endpoint_url": os.getenv("SAGEMAKER_ENDPOINT_URL"),
            "api_key": os.getenv("SAGEMAKER_API_KEY")  # Assuming API key is needed
        }
    