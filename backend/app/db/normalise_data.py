from datetime import datetime,timezone
from app.helpers import to_number

def normalize_fmp_income_statement(statement, company_id, report_type):
    return {
        "company_id": company_id,
        "fiscal_date_ending": statement.get("date"),
        "report_type": report_type,
        "reported_currency": statement.get("reportedCurrency"),

        "revenue": to_number(statement.get("revenue")),
        "gross_profit": to_number(statement.get("grossProfit")),
        "operating_income": to_number(statement.get("operatingIncome")),
        "operating_expenses": to_number(statement.get("operatingExpenses")),
        "net_income": to_number(statement.get("netIncome")),

        "ebit": to_number(statement.get("ebit")),
        "ebitda": to_number(statement.get("ebitda")),

        "research_and_development":
            to_number(statement.get("researchAndDevelopmentExpenses")),

        "sga_expense":
            to_number(statement.get("sellingGeneralAndAdministrativeExpenses")),

        "income_before_tax":
            to_number(statement.get("incomeBeforeTax")),

        "income_tax_expense":
            to_number(statement.get("incomeTaxExpense")),

        "interest_expense":
            to_number(statement.get("interestExpense")),

        "depreciation_amortization":
            to_number(statement.get("depreciationAndAmortization")),

        "source": "fmp",
        "created_at": datetime.now(timezone.utc)
    }
def normalize_alpha_vantage_income_statement(statement, company_id, report_type):
    return {
        "company_id": company_id,
        "fiscal_date_ending": statement.get("fiscalDateEnding"),
        "report_type": report_type,
        "reported_currency": statement.get("reportedCurrency"),

        "revenue": to_number(statement.get("totalRevenue")),
        "gross_profit": to_number(statement.get("grossProfit")),
        "operating_income": to_number(statement.get("operatingIncome")),
        "operating_expenses": to_number(statement.get("operatingExpenses")),
        "net_income": to_number(statement.get("netIncome")),

        "ebit": to_number(statement.get("ebit")),
        "ebitda": to_number(statement.get("ebitda")),

        "research_and_development":
            to_number(statement.get("researchAndDevelopment")),

        "sga_expense":
            to_number(statement.get("sellingGeneralAndAdministrative")),

        "income_before_tax":
            to_number(statement.get("incomeBeforeTax")),

        "income_tax_expense":
            to_number(statement.get("incomeTaxExpense")),

        "interest_expense":
            to_number(statement.get("interestExpense")),

        "depreciation_amortization":
            to_number(statement.get("depreciationAndAmortization")),

        "source": "alpha_vantage",
        "created_at": datetime.now(timezone.utc)
    }



def normalize_fmp_balance_sheet(
    sheet,
    company_id,
    report_type
):
    return {
        "company_id": company_id,

        "fiscal_date_ending": sheet.get("date"),

        "report_type": report_type,

        "reported_currency": sheet.get("reportedCurrency"),

        "total_assets":
            to_number(sheet.get("totalAssets")),

        "total_current_assets":
            to_number(sheet.get("totalCurrentAssets")),

        "cash_and_equivalents":
            to_number(sheet.get("cashAndCashEquivalents")),

        "cash_and_short_term_investments":
            to_number(sheet.get("cashAndShortTermInvestments")),

        "inventory":
            to_number(sheet.get("inventory")),

        "current_receivables":
            to_number(sheet.get("netReceivables")),

        "property_plant_equipment":
            to_number(sheet.get("propertyPlantEquipmentNet")),

        "intangible_assets":
            to_number(sheet.get("intangibleAssets")),

        "goodwill":
            to_number(sheet.get("goodwill")),

        "short_term_investments":
            to_number(sheet.get("shortTermInvestments")),

        "total_liabilities":
            to_number(sheet.get("totalLiabilities")),

        "total_current_liabilities":
            to_number(sheet.get("totalCurrentLiabilities")),

        "short_term_debt":
            to_number(sheet.get("shortTermDebt")),

        "long_term_debt":
            to_number(sheet.get("longTermDebt")),

        "total_debt":
            to_number(sheet.get("totalDebt")),

        "total_non_current_liabilities":
            to_number(sheet.get("totalNonCurrentLiabilities")),

        "total_shareholder_equity":
            to_number(sheet.get("totalStockholdersEquity")),

        "retained_earnings":
            to_number(sheet.get("retainedEarnings")),

        # FMP does not provide the equivalent field
        # in this response
        "shares_outstanding": None,

        "source": "fmp",
        "created_at": datetime.now(timezone.utc)
    }



def normalize_alpha_vantage_balance_sheet(
    sheet,
    company_id,
    report_type
):
    return {
        "company_id": company_id,
        "fiscal_date_ending": sheet.get("fiscalDateEnding"),
        "report_type": report_type,
        "reported_currency": sheet.get("reportedCurrency"),

        "total_assets": to_number(sheet.get("totalAssets")),
        "total_current_assets": to_number(
            sheet.get("totalCurrentAssets")
        ),
        "cash_and_equivalents": to_number(
            sheet.get("cashAndCashEquivalentsAtCarryingValue")
        ),
        "cash_and_short_term_investments": to_number(
            sheet.get("cashAndShortTermInvestments")
        ),
        "inventory": to_number(sheet.get("inventory")),
        "current_receivables": to_number(
            sheet.get("currentNetReceivables")
        ),
        "property_plant_equipment": to_number(
            sheet.get("propertyPlantEquipmentNet")
        ),
        "intangible_assets": to_number(
            sheet.get("intangibleAssets")
        ),
        "goodwill": to_number(sheet.get("goodwill")),
        "short_term_investments": to_number(
            sheet.get("shortTermInvestments")
        ),

        "total_liabilities": to_number(
            sheet.get("totalLiabilities")
        ),
        "total_current_liabilities": to_number(
            sheet.get("totalCurrentLiabilities")
        ),
        "short_term_debt": to_number(
            sheet.get("shortTermDebt")
        ),
        "long_term_debt": to_number(
            sheet.get("longTermDebt")
        ),
        "total_debt": to_number(
            sheet.get("totalDebt")
        ),
        "total_non_current_liabilities": to_number(
            sheet.get("totalNonCurrentLiabilities")
        ),

        "total_shareholder_equity": to_number(
            sheet.get("totalShareholderEquity")
        ),
        "retained_earnings": to_number(
            sheet.get("retainedEarnings")
        ),
        "shares_outstanding": to_number(
            sheet.get("commonStockSharesOutstanding")
        ),

        "source": "alpha_vantage",
        "created_at": datetime.now(timezone.utc)
    }

def normalize_fmp_cash_flow(
    cash_flow,
    company_id,
    report_type
):
    capital_expenditures = to_number(
        cash_flow.get("capitalExpenditure")
    )

    return {
        "company_id": company_id,
        "fiscal_date_ending": cash_flow.get("date"),
        "report_type": report_type,
        "reported_currency": cash_flow.get("reportedCurrency"),

        "operating_cash_flow": to_number(
            cash_flow.get("operatingCashFlow")
        ),

        "capital_expenditures": (
            abs(capital_expenditures)
            if capital_expenditures is not None
            else None
        ),

        "investing_cash_flow": to_number(
            cash_flow.get(
                "netCashProvidedByInvestingActivities"
            )
        ),

        "financing_cash_flow": to_number(
            cash_flow.get(
                "netCashProvidedByFinancingActivities"
            )
        ),

        "dividend_payout": to_number(
            cash_flow.get("netDividendsPaid")
        ),

        "stock_based_compensation": to_number(
            cash_flow.get("stockBasedCompensation")
        ),

        "net_income": to_number(
            cash_flow.get("netIncome")
        ),

        "source": "fmp",
        "created_at": datetime.now(timezone.utc)
    }
def normalize_alpha_vantage_cash_flow(  cash_flow,
    company_id,
    report_type):
    return {
        "company_id": company_id,
        "fiscal_date_ending": cash_flow.get("fiscalDateEnding"),
        "report_type": report_type,
        "reported_currency": cash_flow.get("reportedCurrency"),
        "operating_cash_flow": to_number(cash_flow.get("operatingCashflow")),
        "capital_expenditures": to_number(cash_flow.get("capitalExpenditures")),
        "investing_cash_flow": to_number(cash_flow.get("cashflowFromInvestment")),
        "financing_cash_flow": to_number(cash_flow.get("cashflowFromFinancing")),
        "dividend_payout": to_number(cash_flow.get("dividendPayout")),
        "stock_based_compensation": to_number(cash_flow.get("stockBasedCompensation")),
        "net_income": to_number(cash_flow.get("netIncome")),
        "source": "alpha_vantage" ,"created_at": datetime.now(timezone.utc)}


def normalise_massive_comp(company:str):
    return {
        "symbol": company["ticker"],
        "companyName": company["name"],
        "exchange": company.get("primary_exchange"),
        "country": company.get("locale"),
        "website": company.get("homepage_url"),
        "description": company.get("description")
    }