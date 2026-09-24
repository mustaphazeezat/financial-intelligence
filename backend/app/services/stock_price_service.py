from datetime import datetime, timedelta
from app.services.market_calendar import get_latest_market_date, seconds_until_market_close
from app.db.stock_price_repository import get_company_performance_db, get_latest_stock_price_date, get_stock_prices_from_db, save_stock_prices
from app.db.company_repository import get_company_id
from app.clients.fmp import FMPClient
from app.db.redis import redis_client
import json

from app.clients.alpha_vantage import AlphaVantageClient
from app.clients.massive import MassiveClient
from app.helpers import is_in_symbol, normalize_massive_prices, percentage_change
from app.services.company_service import CompanyServices


class StockPriceService:

    def __init__(self):
        self.fmp = FMPClient()
        self.alpha_vantage = AlphaVantageClient()
        self.massive = MassiveClient()
        self.company_service = CompanyServices()


    def get_stock_prices(self, symbol: str):
        company = self.company_service.get_company_by_symbol(symbol)

        if not company:
            return None

        company_id = company["id"]

        cache_key = f"stock_prices:{company_id}"

        #Check Redis 
        cached_data = redis_client.get(cache_key)

        if cached_data:
            return json.loads(cached_data)

        #Get latest market date
        latest_market_date = get_latest_market_date()

        #Get latest date we have in DB
        latest_db_date = get_latest_stock_price_date(company_id)

       
        if (latest_db_date is None or latest_db_date < latest_market_date):
            if is_in_symbol(symbol):
                # FMP supports this symbol
                data = self.fmp.get_stock_prices(symbol)
                if data:
                    save_stock_prices(data, company_id, "fmp")
            else:
                # Use Massive 
                data = self.massive.get_stock_prices(symbol)
                if data:
                    normalize_data = normalize_massive_prices(data["results"])
                    save_stock_prices(normalize_data, company_id, "massive")

        #Get one year of prices from DB
        start_date = latest_market_date - timedelta(days=365)

        price_list = get_stock_prices_from_db(
            company_id,
            start_date,
            latest_market_date
        )

        if not price_list:
            return []

        price_list = [dict(price) for price in price_list]

        #Cache until next market close
        ttl = seconds_until_market_close()

        if ttl:
            redis_client.set(
                cache_key,
                json.dumps(price_list, default=str),
                ex=ttl
            )

        return price_list

    def get_company_performance(self, symbol: str):

        company = self.company_service.get_company_by_symbol(symbol)

        if not company:
            return None

        company_id = company["id"]
        cache_key = f"price_performance:{company_id}"
        
        #Check Redis 
        cached_data = redis_client.get(cache_key)

        if cached_data:
            return json.loads(cached_data)

        result = get_company_performance_db(company_id)

        if not result:
            return None

        latest_close = result["close"]

        price_performance = {
            "symbol": symbol.upper(),

            "performance": {
                "1d": percentage_change(
                    result["previous_close"], latest_close
                ),
                "1m": percentage_change(
                    result["month_ago_close"], latest_close
                ),
                "3m": percentage_change(
                    result["three_months_ago_close"], latest_close
                ),
                "6m": percentage_change(
                    result["six_months_ago_close"], latest_close
                ),
                "1y": percentage_change(
                    result["year_ago_close"], latest_close
                )
            },

            "trading_activity": {
                "volume": result["volume"],
                "vwap": result["vwap"]
            }
        }
        #Cache until next market close
        ttl = seconds_until_market_close()

        if ttl:
            redis_client.set(
                cache_key,
                json.dumps(price_performance, default=str),
                ex=ttl
            )

        return price_performance

