from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Financial Intelligence Platform API"}


def test_get_companies_success(monkeypatch):
    from app.api.routers import companies as companies_router

    monkeypatch.setattr(
        companies_router,
        "get_all_companies",
        lambda: [{"id": 1, "symbol": "AAPL", "company_name": "Apple Inc."}],
    )

    response = client.get("/api/v1/companies/")

    assert response.status_code == 200
    assert response.json()["companies"][0]["symbol"] == "AAPL"


def test_get_companies_empty(monkeypatch):
    from app.api.routers import companies as companies_router

    monkeypatch.setattr(companies_router, "get_all_companies", lambda: [])

    response = client.get("/api/v1/companies/")

    assert response.status_code == 404
    assert response.json()["detail"] == "No companies found in the database."


def test_get_company_by_symbol_success(monkeypatch):
    from app.api.routers import companies as companies_router

    monkeypatch.setattr(
        companies_router,
        "get_company_by_symbol",
        lambda symbol: {"id": 1, "symbol": symbol, "company_name": "Apple Inc."},
    )

    response = client.get("/api/v1/companies/AAPL")

    assert response.status_code == 200
    assert response.json()["symbol"] == "AAPL"


def test_get_company_by_symbol_not_found(monkeypatch):
    from app.api.routers import companies as companies_router

    monkeypatch.setattr(companies_router, "get_company_by_symbol", lambda symbol: None)

    response = client.get("/api/v1/companies/ZZZ")

    assert response.status_code == 404
    assert response.json()["detail"] == "Company with symbol 'ZZZ' was not found."


def test_get_company_price_success(monkeypatch):
    from app.api.routers import prices as prices_router

    monkeypatch.setattr(
        prices_router.stock_service,
        "get_stock_prices",
        lambda symbol: [{
            "company_id": 1,
            "date": "2024-01-02",
            "close": 125.5,
            "source": "fmp",
        }],
    )

    response = client.get("/api/v1/companies/AAPL/price")

    assert response.status_code == 200
    assert response.json()["prices"][0]["close"] == 125.5


def test_get_company_price_not_found(monkeypatch):
    from app.api.routers import prices as prices_router

    monkeypatch.setattr(prices_router.stock_service, "get_stock_prices", lambda symbol: [])

    response = client.get("/api/v1/companies/ZZZ/price")

    assert response.status_code == 404
    assert response.json()["detail"] == "Company with symbol 'ZZZ' was not found."


def test_get_market_movers_success(monkeypatch):
    from app.api.routers import markets as markets_router

    monkeypatch.setattr(
        markets_router.market_services,
        "get_market_movers_data",
        lambda movers_type: [{"symbol": "AAPL", "category": "gainers"}],
    )

    response = client.get("/api/v1/market_movers/?movers_type=gainers")

    assert response.status_code == 200
    assert response.json()["category"] == "gainers"
    assert response.json()["movers"][0]["symbol"] == "AAPL"


def test_get_market_movers_empty(monkeypatch):
    from app.api.routers import markets as markets_router

    monkeypatch.setattr(markets_router.market_services, "get_market_movers_data", lambda movers_type: [])

    response = client.get("/api/v1/market_movers/?movers_type=losers")

    assert response.status_code == 404
    assert "There are currently no information" in response.json()["detail"]


def test_get_income_statements_success(monkeypatch):
    from app.api.routers import finances as finances_router

    monkeypatch.setattr(
        finances_router.financial_service,
        "get_income_statement",
        lambda symbol, financial_report_type: [{
            "company_id": 1,
            "fiscal_date_ending": "2024-01-31",
            "report_type": "annual",
            "reported_currency": "USD",
            "revenue": 1000.0,
            "net_income": 200.0,
            "source": "alpha_vantage",
        }],
    )

    response = client.get("/api/v1/financial_statements/income_statement/AAPL/annual")

    assert response.status_code == 200
    assert response.json()["income_statements"][0]["revenue"] == 1000.0


def test_get_balance_sheets_success(monkeypatch):
    from app.api.routers import finances as finances_router

    monkeypatch.setattr(
        finances_router.financial_service,
        "get_balance_sheet",
        lambda symbol, financial_report_type: [{
            "company_id": 1,
            "fiscal_date_ending": "2024-01-31",
            "report_type": "annual",
            "reported_currency": "USD",
            "total_assets": 5000.0,
            "total_liabilities": 2000.0,
            "source": "alpha_vantage",
        }],
    )

    response = client.get("/api/v1/financial_statements/balance_sheets/AAPL/annual")

    assert response.status_code == 200
    assert response.json()["balance_sheets"][0]["total_assets"] == 5000.0


def test_get_cash_flows_success(monkeypatch):
    from app.api.routers import finances as finances_router

    monkeypatch.setattr(
        finances_router.financial_service,
        "get_cash_flow",
        lambda symbol, financial_report_type: [{
            "company_id": 1,
            "fiscal_date_ending": "2024-01-31",
            "report_type": "annual",
            "reported_currency": "USD",
            "operating_cash_flow": 1000.0,
            "source": "alpha_vantage",
        }],
    )

    response = client.get("/api/v1/financial_statements/cash_flows/AAPL/annual")

    assert response.status_code == 200
    assert response.json()["cash_flow_statements"][0]["operating_cash_flow"] == 1000.0
