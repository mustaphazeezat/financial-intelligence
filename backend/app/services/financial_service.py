from datetime import datetime
import time

from app.db.finance_repository import get_balance_sheets_from_db, get_cash_flow_statements_from_db, get_income_statement_from_db, get_latest_financial_statement, save_balance_sheet, save_cash_flow, save_income_statements
from app.services.market_calendar import should_refresh_financial_data
from app.clients.alpha_vantage import AlphaVantageClient
from app.services.company_service import CompanyServices
from app.helpers import is_in_symbol
from app.clients.fmp import FMPClient



class FinancialServices:
    def __init__(self):
        self.alpha_vantage = AlphaVantageClient()
        self.fmp = FMPClient()
        self.company = CompanyServices()

    def get_income_statement(self, symbol:str, reportType: str = "quarter"):
        company = self.company.get_company_by_symbol(symbol)
        
        company_id = company.id
        
        last_updated = get_latest_financial_statement(
            company_id,
            reportType,
            "income_statements"
        )
        
       
        if not should_refresh_financial_data(last_updated,reportType):
            return get_income_statement_from_db(
                company_id,
                reportType
            )
        if is_in_symbol(symbol):
            try:
                quarter_statements = self.fmp.get_income_statement(symbol, "quarter")
                annual_statements = self.fmp.get_income_statement(symbol, "annual")
                if quarter_statements or annual_statements:
                    save_income_statements(quarter_statements, company_id, "quarter", "fmp")
                    save_income_statements(annual_statements, company_id, "annual", "fmp")

                return get_income_statement_from_db(
                                        company_id,
                                        reportType
                                    )
            except Exception as e:
                print(f"fmp failed: {e}")
        else:
            try:
                data = self.alpha_vantage.get_income_statement(symbol)

                # Alpha Vantage returned an error / rate-limit response
                if not data or "Information" in data or "Error Message" in data:
                    print("Alpha Vantage unavailable or rate limit reached.")
                else:
                    quarter_statements = data.get(
                        "quarterlyReports",
                        []
                    )

                    annual_statements = data.get(
                        "annualReports",
                        []
                    )

                    if quarter_statements or annual_statements:
                        save_income_statements(
                            quarter_statements,
                            company_id,
                            "quarter",
                            "alpha_vantage"
                        )

                        save_income_statements(
                            annual_statements,
                            company_id,
                            "annual",
                            "alpha_vantage"
                        )

                        return get_income_statement_from_db(
                            company_id,
                            reportType
                        )

            except Exception as e:
                print(f"Alpha Vantage failed: {e}")

        # If both fail, get whatever in DB
        return get_income_statement_from_db(
            company_id,
            reportType
        )


    def get_balance_sheet(self, symbol: str, reportType: str = "quarter"):
        company = self.company.get_company_by_symbol(symbol)
        company_id = company.id

        last_updated = get_latest_financial_statement(
            company_id,
            reportType,
            "balance_sheets"
        )
        if not should_refresh_financial_data(last_updated,reportType):
            return  get_balance_sheets_from_db(company_id, reportType)

        if is_in_symbol(symbol):
            try:
                quarter_statements = self.fmp.get_balance_sheet(symbol, "quarter")
                annual_statements = self.fmp.get_balance_sheet(symbol, "annual")
                if quarter_statements or annual_statements:
                    save_balance_sheet(quarter_statements, company_id, "quarter", "fmp")
                    save_balance_sheet(annual_statements, company_id, "annual", "fmp")
            except Exception as e:
                print(f"fmp failed: {e}")
        else:
            try:
                data = self.alpha_vantage.get_balance_sheet(symbol)

                if data:
                    statements = data.get("quarterlyReports", [])
                    statements = data.get("annualReports", [])
                else:
                    return None
                if statements:
                    save_balance_sheet(statements, company_id, reportType, "alpha_vantage")

                    return get_balance_sheets_from_db(
                        company_id,
                        reportType
                    )
                
            except Exception as e:
                print(f"Alpha Vantage failed: {e}")

        # If both fail, get whatever in DB
        return get_income_statement_from_db(
            company_id,
            reportType
        )

    def get_cash_flow(self, symbol: str, reportType: str):
        company = self.company.get_company_by_symbol(symbol)
        company_id = company.id
        if not company_id:
            return None
        last_updated = get_latest_financial_statement(
            company_id,
            reportType,
            "cash_flow_statements"
        )
        if not should_refresh_financial_data(last_updated,reportType):
            return  get_cash_flow_statements_from_db(company_id, reportType)
        if is_in_symbol(symbol):
            try:
                quarter_statements = self.fmp.get_cash_flow(symbol, "quarter")
                annual_statements = self.fmp.get_cash_flow(symbol, "annual")
                if quarter_statements or annual_statements:
                    save_cash_flow(quarter_statements, company_id, "quarter", "fmp")
                    save_cash_flow(annual_statements, company_id, "annual", "fmp")
            except Exception as e:
                print(f"fmp failed: {e}")
        else:
            try:
                data = self.alpha_vantage.get_cash_flow(symbol)
            
                if reportType == "quarter":
                    statements = data.get("quarterlyReports", [])
                elif reportType == "annual":
                    statements = data.get("annualReports", [])
                else:
                    return None
                if statements:
                    save_cash_flow(statements, company_id, reportType, "alpha_vantage")
    
                    return get_cash_flow_statements_from_db(company_id, reportType)
                
            except Exception as e:
                print(f"Alpha Vantage failed: {e}")
        
        # If both fail, get whatever in DB
        return get_cash_flow_statements_from_db(company_id, reportType)


    def get_financial_health(
        self,
        symbol: str,
        reportType: str = "quarter"
    ):
        company = self.company.get_company_by_symbol(symbol)

        if not company:
            return None

        company_id = company["id"]

        # Get statements
        income_statements = self.get_income_statement(
            symbol,
            reportType
        )

        balance_sheets = self.get_balance_sheet(
            symbol,
            reportType
        )

        cash_flow_statements = self.get_cash_flow(
            symbol,
            reportType
        )

        income_statement = (
            income_statements[0]
            if income_statements
            else None
        )

        balance_sheet = (
            balance_sheets[0]
            if balance_sheets
            else None
        )

        cash_flow_statement = (
            cash_flow_statements[0]
            if cash_flow_statements
            else None
        )

        profitability = {
            "gross_margin": None,
            "operating_margin": None,
            "net_margin": None
        }

        if income_statement:
            revenue = income_statement["revenue"]

            if revenue:
                profitability = {
                    "gross_margin": (
                        income_statement["gross_profit"] / revenue * 100
                        if income_statement["gross_profit"] is not None
                        else None
                    ),

                    "operating_margin": (
                        income_statement["operating_income"] / revenue * 100
                        if income_statement["operating_income"] is not None
                        else None
                    ),

                    "net_margin": (
                        income_statement["net_income"] / revenue * 100
                        if income_statement["net_income"] is not None
                        else None
                    )
                }

        financial_health = {
            "cash": None,
            "debt": None,
            "equity": None,
            "debt_to_equity": None
        }

        if balance_sheet:
            short_term_debt = balance_sheet["short_term_debt"] or 0
            long_term_debt = balance_sheet["long_term_debt"] or 0

            debt = balance_sheet["total_debt"]

            if debt is None:
                debt = short_term_debt + long_term_debt

            equity = balance_sheet["total_shareholder_equity"]

            financial_health = {
                "cash": balance_sheet["cash_and_equivalents"],
                "debt": debt,
                "equity": equity,
                "debt_to_equity": (
                    debt / equity * 100
                    if debt is not None and equity
                    else None
                )
            }

        cash_flow = {
            "operating_cash_flow": None,
            "capital_expenditure": None,
            "free_cash_flow": None
        }

        if cash_flow_statement:
            operating_cash_flow = (
                cash_flow_statement["operating_cash_flow"]
            )

            capital_expenditure = (
                cash_flow_statement["capital_expenditures"]
            )

            free_cash_flow = None

            if (
                operating_cash_flow is not None
                and capital_expenditure is not None
            ):
                free_cash_flow = (
                    operating_cash_flow - capital_expenditure
                )

            cash_flow = {
                "operating_cash_flow": operating_cash_flow,
                "capital_expenditure": capital_expenditure,
                "free_cash_flow": free_cash_flow
            }

        return {
            "profitability": profitability,
            "financial_health": financial_health,
            "cash_flow": cash_flow
        }