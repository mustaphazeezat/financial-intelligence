from app.constants import SUPPORTED_SYMBOLS
from app.constants import summm
from app.clients.fmp import FMPClient
from app.clients.alpha_vantage import AlphaVantageClient
from app.db.industry_repository import (
    get_or_create_sector,
    get_or_create_industry
)
from app.db.company_repository import save_company, get_company_id
from app.db.markets_repository import save_movers, delete_movers_data
from app.db.stock_price_repository import save_stock_prices
from app.db.finance_repository import save_income_statements, save_balance_sheet, save_cash_flow


class IngestionService:
    def __init__(self):
        self.fmp = FMPClient()
        self.alpha_vantage = AlphaVantageClient()

    def ingest_company_data(self):
        for symbol in summm:
            print(f"Fetching {symbol}...")
            profile = self.fmp.get_company_profile(symbol)

            company = profile[0]
            sector_name = company.get("sector")
            industry_name = company.get("industry")

            if not sector_name or not industry_name:
                print(
                    f"Missing sector/industry for {symbol}"
                )
                continue
            sector_id = get_or_create_sector(sector_name)
            industry_id = get_or_create_industry(industry_name, sector_id)

            save_company(company=company, industry_id=industry_id)

    def ingest_movers_data(self):
        movers_data = self.alpha_vantage.get_top_stock_gainers_losers()

        delete_movers_data()

        top_gainers = movers_data["top_gainers"]
        top_loosers = movers_data["top_losers"]
        actively_traded = movers_data["most_actively_traded"]

        save_movers(top_gainers, "gainers")
        save_movers(top_loosers, "losers")
        save_movers(actively_traded, "active")

    def ingest_stock_price_data(self):
        for symbol in summm:
            print(f"Fetching {symbol}...")
            prices = self.fmp.get_stock_prices(symbol)
            company_id = get_company_id(symbol)
            save_stock_prices(prices, company_id, "fmp")

    def ingest_income_statements_data(self, symbol):
        data = self.alpha_vantage.get_income_statement(symbol)
        company_id = get_company_id(symbol)

        save_income_statements(data["annualReports"], company_id, "annual")
        save_income_statements(data["quarterlyReports"], company_id, "quarter")

    def ingest_balance_sheet_data(self, symbol):
        data = self.alpha_vantage.get_balance_sheet(symbol)
        company_id = get_company_id(symbol)

        save_balance_sheet(data["annualReports"], company_id, "annual")
        save_balance_sheet(data["quarterlyReports"], company_id, "quarter")

    def ingest_cash_flow_data(self, symbol):
        data = self.alpha_vantage.get_cash_flow(symbol)
        company_id = get_company_id(symbol)

        save_cash_flow(data["annualReports"], company_id, "annual")
        save_cash_flow(data["quarterlyReports"], company_id, "quarter")