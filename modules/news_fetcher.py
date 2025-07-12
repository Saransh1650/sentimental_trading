from dotenv import load_dotenv
import requests
import os

load_dotenv()

def get_crypto_news(coin):
    """
    Fetches crypto news from the Coindesk API and returns a list of article bodies.
    """
    api_key = os.getenv("COIN_DESK_API_KEY")
    if not api_key:
        raise ValueError("COIN_DESK_API_KEY not found in environment variables.")

    try:
        response = requests.get(
            'https://data-api.coindesk.com/news/v1/article/list',
            params={"lang": "EN", "limit": 20, "api_key": api_key, "categories": coin},
            headers={"Content-type": "application/json; charset=UTF-8"}
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        json_response = response.json()
        
        articles = json_response.get('Data', [])
        bodies = [article['BODY'] for article in articles if 'BODY' in article and article['BODY']]
        
        print(bodies)
        return bodies

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news from Coindesk API: {e}")
        return []
