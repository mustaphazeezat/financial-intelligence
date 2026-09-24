import json
from datetime import date, datetime

import app.services.stock_price_service as stock_price_service_module
import app.services.market_service as market_service_module


class DummyRedis:
    def __init__(self):
        self.store = {}

    def get(self, key):
        return self.store.get(key)

    def set(self, key, value, ex=None):
        self.store[key] = value

    def delete(self, *keys):
        for key in keys:
            self.store.pop(key, None)


class DummyResponse:
    def __init__(self, payload):
        self.payload = payload

    def __iter__(self):
        return iter(self.payload)


def test_stock_price_service_returns_none_when_company_missing(monkeypatch):
    service = stock_price_service_module.StockPriceService()

    monkeypatch.setattr(
        stock_price_service_module,
        "get_company_id",
        lambda symbol: None,
    )

    assert service.get_stock_prices("AAPL") is None


def test_stock_price_service_uses_cache_when_present(monkeypatch):
    service = stock_price_service_module.StockPriceService()
    cached_payload = [{"date": "2024-01-02", "close": 123.45}]

    redis = DummyRedis()
    redis.set("stock_prices:42", json.dumps(cached_payload))

    monkeypatch.setattr(stock_price_service_module, "get_company_id", lambda symbol: 42)
    monkeypatch.setattr(stock_price_service_module, "redis_client", redis)

    result = service.get_stock_prices("AAPL")

    assert result == cached_payload


def test_stock_price_service_refreshes_prices_when_stale(monkeypatch):
    service = stock_price_service_module.StockPriceService()
    redis = DummyRedis()

    monkeypatch.setattr(stock_price_service_module, "get_company_id", lambda symbol: 42)
    monkeypatch.setattr(stock_price_service_module, "redis_client", redis)
    monkeypatch.setattr(stock_price_service_module, "get_latest_market_date", lambda: date(2024, 6, 3))
    monkeypatch.setattr(stock_price_service_module, "get_latest_stock_price_date", lambda company_id: date(2024, 5, 1))

    saved = []
    monkeypatch.setattr(
        stock_price_service_module,
        "save_stock_prices",
        lambda data, company_id, source: saved.append((data, company_id, source)),
    )

    monkeypatch.setattr(
        stock_price_service_module,
        "get_stock_prices_from_db",
        lambda company_id, start_date, end_date: [
            {"date": "2024-06-01", "close": 110.0},
            {"date": "2024-06-02", "close": 120.0},
        ],
    )
    monkeypatch.setattr(stock_price_service_module, "seconds_until_market_close", lambda: 300)

    service.fmp = type("FMP", (), {"get_stock_prices": lambda self, symbol: [{"date": "2024-06-02", "close": 125.0}]})()

    result = service.get_stock_prices("AAPL")

    assert result[0]["close"] == 110.0
    assert saved == [([{"date": "2024-06-02", "close": 125.0}], 42, "fmp")]


def test_market_service_returns_cache_when_present(monkeypatch):
    service = market_service_module.MarketService()
    redis = DummyRedis()
    cached_payload = [{"symbol": "AAPL", "category": "gainers"}]
    redis.set("market_movers:gainers", json.dumps(cached_payload))

    monkeypatch.setattr(market_service_module, "redis_client", redis)

    result = service.get_market_movers_data("gainers")

    assert result == cached_payload


def test_market_service_refreshes_movers_when_stale(monkeypatch):
    service = market_service_module.MarketService()
    redis = DummyRedis()

    monkeypatch.setattr(market_service_module, "redis_client", redis)
    monkeypatch.setattr(market_service_module, "get_latest_market_date", lambda: date(2024, 6, 3))
    monkeypatch.setattr(market_service_module, "get_latest_movers_date", lambda: datetime(2024, 5, 31, 12, 0, 0))

    saved_calls = []
    monkeypatch.setattr(
        market_service_module,
        "delete_movers_data",
        lambda: saved_calls.append("delete"),
    )
    monkeypatch.setattr(
        market_service_module,
        "save_movers",
        lambda movers, category: saved_calls.append((movers, category)),
    )

    monkeypatch.setattr(
        market_service_module,
        "get_market_movers_from_db",
        lambda category: [{"symbol": "AAPL", "category": category}],
    )
    monkeypatch.setattr(market_service_module, "seconds_until_market_close", lambda: 300)

    service.alpha_vantage = type(
        "AV",
        (),
        {
            "get_top_stock_gainers_losers": lambda self: {
                "top_gainers": [{"ticker": "AAPL", "price": "100", "change_amount": "2", "change_percentage": "+2%", "volume": "1000"}],
                "top_losers": [{"ticker": "MSFT", "price": "200", "change_amount": "-1", "change_percentage": "-1%", "volume": "2000"}],
                "most_actively_traded": [{"ticker": "NVDA", "price": "300", "change_amount": "3", "change_percentage": "+3%", "volume": "5000"}],
            }
        },
    )()

    result = service.get_market_movers_data("gainers")

    assert result[0]["symbol"] == "AAPL"
    assert saved_calls[0] == "delete"


def test_market_service_returns_empty_list_when_no_movers_found(monkeypatch):
    service = market_service_module.MarketService()
    redis = DummyRedis()

    monkeypatch.setattr(market_service_module, "redis_client", redis)
    monkeypatch.setattr(market_service_module, "get_latest_market_date", lambda: date(2024, 6, 3))
    monkeypatch.setattr(market_service_module, "get_latest_movers_date", lambda: datetime(2024, 6, 3, 12, 0, 0))
    monkeypatch.setattr(market_service_module, "get_market_movers_from_db", lambda category: [])
    monkeypatch.setattr(market_service_module, "seconds_until_market_close", lambda: 300)

    assert service.get_market_movers_data("losers") == []
