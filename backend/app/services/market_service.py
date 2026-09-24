from datetime import datetime, timedelta, timezone
import json

from app.clients.alpha_vantage import AlphaVantageClient
from app.services.market_calendar import get_latest_market_date, seconds_until_market_close
from app.db.markets_repository import delete_movers_data, get_latest_movers_date, get_market_movers_from_db, save_movers
from app.db.redis import redis_client



class MarketService:
    def __init__(self):
            self.alpha_vantage = AlphaVantageClient()
        
    
    def get_market_movers_data(self, moversType: str):

        cache_key = f"market_movers:{moversType}"
        cached_data = redis_client.get(cache_key)

        if cached_data:
            return json.loads(cached_data)

        latest_market_date = get_latest_market_date()
        latest_db_date = get_latest_movers_date()
        
        
        if (latest_db_date is None or latest_db_date.date() < latest_market_date):
            movers_data = self.alpha_vantage.get_top_stock_gainers_losers()
            if movers_data is None:
                return None
            delete_movers_data()
            top_gainers = movers_data["top_gainers"]
            top_loosers = movers_data["top_losers"]
            actively_traded = movers_data["most_actively_traded"]
    
            save_movers(top_gainers, "gainers")
            save_movers(top_loosers, "losers")
            save_movers(actively_traded, "active")
            redis_client.delete(
                "market_movers:gainers",
                "market_movers:losers",
                "market_movers:active"
            )
            
        movers_list  = get_market_movers_from_db(moversType)
        if not movers_list:
            return []

        movers_list = [dict(mover) for mover in movers_list]
        ttl = seconds_until_market_close()

        if ttl:
            redis_client.set(
                cache_key,
                json.dumps(movers_list, default=str),
                ex=ttl
            )
        return movers_list
    