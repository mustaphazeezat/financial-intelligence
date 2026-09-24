import requests
from datetime import date
from app.config import settings
from app.helpers import to_number

class FMPClient:
    def __init__(self):
        self.BASE_URL = "https://financialmodelingprep.com/stable/"
        self.api_key = settings.fmp_api_key

    def get_company_profile(self, symbol):
        url = f"{self.BASE_URL}profile?symbol={symbol}&apikey={self.api_key}"
        try:
            response =  requests.get(url)
            if response.status_code == 200:
                # Parse the JSON response into a dictionary
                data = response.json()
                print(f"Successfully fetched data: {data}")
                return data
            else:
                print(f"Error: Received status code {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def get_stock_prices(self, symbol):
        today = date.today()
        one_year_ago = today.replace(year=today.year - 1)
        
        url = f"{self.BASE_URL}historical-price-eod/full?symbol={symbol}&from={one_year_ago}&to={today}&apikey={self.api_key}"
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

    def get_income_statement(self, symbol,period):
        url = f"{self.BASE_URL}income-statement?symbol={symbol}&period={period}&limit=5&apikey={self.api_key}"
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

    def get_balance_sheet(self, symbol:str, period:str):
        url = f"{self.BASE_URL}balance-sheet-statement?symbol={symbol}&apikey={self.api_key}&period={period}&limit=5"
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
    def get_cash_flow(self, symbol, period:str):
        url = f"{self.BASE_URL}cash-flow-statement?symbol={symbol}&apikey={self.api_key}&period={period}&limit=5"
        try:
            response =  requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Error: Received status code {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    


