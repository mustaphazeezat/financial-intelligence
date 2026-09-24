import requests
from datetime import date
from app.config import settings

class MassiveClient:
    def __init__(self):
        self.BASE_URL = "https://api.massive.com"
        self.api_key = settings.massive_api_key

    def get_company_profile(self, symbol: str):
        url = f"{self.BASE_URL}/v3/reference/tickers/{symbol}?apiKey={self.api_key}"
        try:
            response =  requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return data.get('results')
            else:
                print(f"Error: Received status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def get_stock_prices(self, symbol):
        today = date.today()
        one_year_ago = today.replace(year=today.year - 1)
        
        url = f"{self.BASE_URL}/v2/aggs/ticker/{symbol}/range/1/day/{one_year_ago}/{today}?adjusted=true&sort=asc&apikey={self.api_key}"
        try:
            response =  requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Error: Received status code {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")