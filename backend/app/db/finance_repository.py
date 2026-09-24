from app.db.normalise_data import normalize_alpha_vantage_balance_sheet, normalize_alpha_vantage_cash_flow, normalize_alpha_vantage_income_statement, normalize_fmp_balance_sheet, normalize_fmp_cash_flow, normalize_fmp_income_statement
from sqlalchemy import text
from datetime import datetime, timezone
from app.db.database import engine
from app.helpers import to_number

ALLOWED_FINANCIAL_TABLES = {
    "income_statements",
    "balance_sheets",
    "cash_flow_statements",
}
def save_income_statements(statements:list, company_id:int, report_type:str, source: str):
    query = text("""
        INSERT INTO income_statements (
            company_id,
            fiscal_date_ending,
            report_type,
            reported_currency,
            revenue,
            gross_profit,
            operating_income,
            operating_expenses,
            net_income,
            ebit,
            ebitda,
            research_and_development,
            sga_expense,
            income_before_tax,
            income_tax_expense,
            interest_expense,
            depreciation_amortization,
            source
        )
        VALUES (
            :company_id,
            :fiscal_date_ending,
            :report_type,
            :reported_currency,
            :revenue,
            :gross_profit,
            :operating_income,
            :operating_expenses,
            :net_income,
            :ebit,
            :ebitda,
            :research_and_development,
            :sga_expense,
            :income_before_tax,
            :income_tax_expense,
            :interest_expense,
            :depreciation_amortization,
            :source
        )
        ON CONFLICT (company_id, fiscal_date_ending, report_type, source)
        DO UPDATE SET
            reported_currency = EXCLUDED.reported_currency,
            revenue = EXCLUDED.revenue,
            gross_profit = EXCLUDED.gross_profit,
            operating_income = EXCLUDED.operating_income,
            operating_expenses = EXCLUDED.operating_expenses,
            net_income = EXCLUDED.net_income,
            ebit = EXCLUDED.ebit,
            ebitda = EXCLUDED.ebitda,
            research_and_development = EXCLUDED.research_and_development,
            sga_expense = EXCLUDED.sga_expense,
            income_before_tax = EXCLUDED.income_before_tax,
            income_tax_expense = EXCLUDED.income_tax_expense,
            interest_expense = EXCLUDED.interest_expense,
            depreciation_amortization = EXCLUDED.depreciation_amortization
    """)
    if source == "fmp":
        records = [
            normalize_fmp_income_statement(statement, company_id, report_type)
            for statement in statements
        ]
    elif source == "alpha_vantage":
        records = [
            normalize_alpha_vantage_income_statement(statement, company_id, report_type)
            for statement in statements
        ]

    with engine.begin() as connection:
        connection.execute(query, records)

def get_latest_income_statement_date(company_id, report_type):
    query = text("""
        SELECT MAX(fiscal_date_ending)
        FROM income_statements
        WHERE company_id = :company_id
          AND report_type = :report_type
    """)

    with engine.connect() as connection:
        return connection.execute(
            query,
            {
                "company_id": company_id,
                "report_type": report_type
            }
        ).scalar_one_or_none()

def get_latest_income_statement_updated_at(company_id, report_type):
    query = text("""
        SELECT MAX(created_at) AS last_updated
        FROM income_statements
        WHERE company_id = :company_id
          AND report_type = :report_type
    """)

    with engine.connect() as connection:
        return connection.execute(
            query,
            {
                "company_id": company_id,
                "report_type": report_type
            }
        ).scalar()

def get_latest_financial_statement(company_id, report_type, table_name):
    if table_name not in ALLOWED_FINANCIAL_TABLES:
        raise ValueError(f"Invalid financial statement table: {table_name}")

    query = text(f"""
        SELECT MAX(created_at) AS last_updated
        FROM {table_name}
        WHERE company_id = :company_id
          AND report_type = :report_type
    """)

    with engine.connect() as connection:
        return connection.execute(
            query,
            {
                "company_id": company_id,
                "report_type": report_type
            }
        ).scalar()

def get_income_statement_from_db(company_id: int, report_type: str):
    query = text("""
        SELECT *
        FROM income_statements
        WHERE company_id = :company_id
            AND report_type = :report_type
        ORDER BY fiscal_date_ending DESC
        LIMIT 5
    """)
    with engine.connect() as connection:
        result = connection.execute(
            query,
            {
                "company_id": company_id,
                "report_type": report_type
            }
        ).mappings().all()
    return result


def save_balance_sheet(balance_sheets:list, company_id:int, report_type:str, source: str):
    query = text("""
        INSERT INTO balance_sheets (
            company_id,
            fiscal_date_ending,
            report_type,
            reported_currency,
            total_assets,
            total_current_assets,
            cash_and_equivalents,
            cash_and_short_term_investments,
            inventory,
            current_receivables,
            property_plant_equipment,
            intangible_assets,
            goodwill,
            short_term_investments,
            total_liabilities,
            total_current_liabilities,
            short_term_debt,
            long_term_debt,
            total_debt,
            total_non_current_liabilities,
            total_shareholder_equity,
            retained_earnings,
            shares_outstanding,
            source
        )
        VALUES (
            :company_id,
            :fiscal_date_ending,
            :report_type,
            :reported_currency,
            :total_assets,
            :total_current_assets,
            :cash_and_equivalents,
            :cash_and_short_term_investments,
            :inventory,
            :current_receivables,
            :property_plant_equipment,
            :intangible_assets,
            :goodwill,
            :short_term_investments,
            :total_liabilities,
            :total_current_liabilities,
            :short_term_debt,
            :long_term_debt,
            :total_debt,
            :total_non_current_liabilities,
            :total_shareholder_equity,
            :retained_earnings,
            :shares_outstanding,
            :source
        )
        ON CONFLICT (company_id, fiscal_date_ending, report_type, source)
        DO UPDATE SET
            reported_currency = EXCLUDED.reported_currency,
            total_assets = EXCLUDED.total_assets,
            total_current_assets = EXCLUDED.total_current_assets,
            cash_and_equivalents = EXCLUDED.cash_and_equivalents,
            cash_and_short_term_investments = EXCLUDED.cash_and_short_term_investments,
            inventory = EXCLUDED.inventory,
            current_receivables = EXCLUDED.current_receivables,
            property_plant_equipment = EXCLUDED.property_plant_equipment,
            intangible_assets = EXCLUDED.intangible_assets,
            goodwill = EXCLUDED.goodwill,
            short_term_investments = EXCLUDED.short_term_investments,
            total_liabilities = EXCLUDED.total_liabilities,
            total_current_liabilities = EXCLUDED.total_current_liabilities,
            short_term_debt = EXCLUDED.short_term_debt,
            long_term_debt = EXCLUDED.long_term_debt,
            total_debt = EXCLUDED.total_debt,
            total_non_current_liabilities = EXCLUDED.total_non_current_liabilities,
            total_shareholder_equity = EXCLUDED.total_shareholder_equity,
            retained_earnings = EXCLUDED.retained_earnings,
            shares_outstanding = EXCLUDED.shares_outstanding
    """)
    if source == "fmp":
        records = [
            normalize_fmp_balance_sheet(sheet, company_id, report_type)
            for sheet in balance_sheets
        ]
    elif source == "alpha_vantage":
        records = [
            normalize_alpha_vantage_balance_sheet(sheet, company_id, report_type)
            for sheet in balance_sheets
        ]

    with engine.begin() as connection:
        connection.execute(query, records)

def get_latest_balance_sheets_date(company_id: int, report_type: str):
    query = text("""
        SELECT MAX(fiscal_date_ending)
        FROM balance_sheets
        WHERE company_id = :company_id
          AND report_type = :report_type
    """)

    with engine.connect() as connection:
        return connection.execute(
            query,
            {
                "company_id": company_id,
                "report_type": report_type
            }
        ).scalar_one_or_none()

def get_balance_sheets_from_db(company_id: int, report_type: str):
    query = text("""
        SELECT *
        FROM balance_sheets 
        WHERE company_id = :company_id
            AND report_type = :report_type
        ORDER BY fiscal_date_ending DESC
        LIMIT 5
    """)
    with engine.connect() as connection:
        result = connection.execute(
            query,
            {
                "company_id": company_id,
                "report_type": report_type
            }
        ).mappings().all()
    return result

def save_cash_flow(cash_flows, company_id:int, report_type:str, source:str):
    query = text("""
        INSERT INTO cash_flow_statements (
            company_id,
            fiscal_date_ending,
            report_type,
            reported_currency,
            operating_cash_flow,
            capital_expenditures,
            investing_cash_flow,
            financing_cash_flow,
            dividend_payout,
            stock_based_compensation,
            net_income,
            source
        )
        VALUES (
            :company_id,
            :fiscal_date_ending,
            :report_type,
            :reported_currency,
            :operating_cash_flow,
            :capital_expenditures,
            :investing_cash_flow,
            :financing_cash_flow,
            :dividend_payout,
            :stock_based_compensation,
            :net_income,
            :source
        )
        ON CONFLICT (company_id, fiscal_date_ending, report_type, source)
        DO UPDATE SET
            reported_currency = EXCLUDED.reported_currency,
            operating_cash_flow = EXCLUDED.operating_cash_flow,
            capital_expenditures = EXCLUDED.capital_expenditures,
            investing_cash_flow = EXCLUDED.investing_cash_flow,
            financing_cash_flow = EXCLUDED.financing_cash_flow,
            dividend_payout = EXCLUDED.dividend_payout,
            stock_based_compensation = EXCLUDED.stock_based_compensation,
            net_income = EXCLUDED.net_income
    """)

    if source == "fmp":
        records = [
            normalize_fmp_cash_flow(cash_flow, company_id, report_type)
            for cash_flow in cash_flows
        ]
    elif source == "alpha_vantage":
        records = [
            normalize_alpha_vantage_cash_flow(cash_flow, company_id, report_type)
            for cash_flow in cash_flows
        ]

    with engine.begin() as connection:
        connection.execute(query, records)

def get_latest_cash_flow_statements_date(company_id: int, report_type: str):
    query = text("""
        SELECT MAX(fiscal_date_ending)
        FROM cash_flow_statements
        WHERE company_id = :company_id
          AND report_type = :report_type
    """)

    with engine.connect() as connection:
        return connection.execute(
            query,
            {
                "company_id": company_id,
                "report_type": report_type
            }
        ).scalar_one_or_none()

def get_cash_flow_statements_from_db(company_id: int, report_type: str):
    query = text("""
        SELECT *
        FROM cash_flow_statements
        WHERE company_id = :company_id
            AND report_type = :report_type
        ORDER BY fiscal_date_ending DESC
        LIMIT 5
    """)
    with engine.connect() as connection:
        result = connection.execute(
            query,
            {
                "company_id": company_id,
                "report_type": report_type
            }
        ).mappings().all()
    return result