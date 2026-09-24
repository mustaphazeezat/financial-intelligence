from datetime import date

import requests
from app.config import settings

class AlphaVantageClient:
    def __init__(self):
        self.BASE_URL = "https://www.alphavantage.co/query?"
        self.api_key = settings.alpha_api_key

    def get_company_profile(self, symbol: str):
        url = f"{self.BASE_URL}function=OVERVIEW&symbol={symbol}&apikey={self.api_key}"
        try:
            response =  requests.get(url)
            if response.status_code == 200:
                
                data = response.json()
                print(f"Successfully fetched data: {data}")
                
                return data
            else:
                print(f"Error: Received status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def get_top_stock_gainers_losers(self):
        url = f"{self.BASE_URL}function=TOP_GAINERS_LOSERS&apikey={self.api_key}"
        try:
            response =  requests.get(url)
            if response.status_code == 200:
                # Parse the JSON response into a dictionary
                data = response.json()
                return data
            else:
                print(f"Error: Received status code {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def get_stock_prices(self, symbol):
        today = date.today()
        one_year_ago = today.replace(year=today.year - 1)
        print(today, one_year_ago)
        
        url = f"{self.BASE_URL}/stable/historical-price-eod/full?symbol={symbol}&from={one_year_ago}&to={today}&apikey={self.api_key}"
        try:
            response =  requests.get(url)
            if response.status_code == 200:
                # Parse the JSON response into a dictionary
                data = response.json()
                return data
            else:
                print(f"Error: Received status code {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
        
    def get_income_statement(self, symbol:str):
        url = f"{self.BASE_URL}function=INCOME_STATEMENT&symbol={symbol}&apikey={self.api_key}"
        try:
            response =  requests.get(url)
            if response.status_code == 200:
               
                data = response.json()
                return data
            else:
                print(f"Error: Received status code {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def get_balance_sheet(self, symbol):
        url = f"{self.BASE_URL}function=BALANCE_SHEET&symbol={symbol}&apikey={self.api_key}"
        try:
            response =  requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Error: Received status code {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def get_cash_flow(self, symbol):
        url = f"{self.BASE_URL}function=CASH_FLOW&symbol={symbol}&apikey={self.api_key}"
        try:
            response =  requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Error: Received status code {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")