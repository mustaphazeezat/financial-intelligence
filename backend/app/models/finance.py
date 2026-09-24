from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict

class FinancialReportType(str, Enum):
    annual = "annual"
    quarter = "quarter"
    
class IncomeStatement(BaseModel):
    fiscal_date_ending: date
    report_type: str
    reported_currency: str
    revenue: Optional[float] = None
    gross_profit: Optional[float] = None
    operating_income: Optional[float] = None
    operating_expenses: Optional[float] = None
    net_income: Optional[float] = None
    ebit: Optional[float] = None
    ebitda: Optional[float] = None
    research_and_development: Optional[float] = None
    sga_expense: Optional[float] = None
    income_before_tax: Optional[float] = None
    income_tax_expense: Optional[float] = None
    interest_expense: Optional[float] = None
    depreciation_amortization: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)

class IncomeStatementsList(BaseModel):
    income_statements: list[IncomeStatement]
    
    model_config = ConfigDict(from_attributes=True)

class BalanceSheet(BaseModel):
    fiscal_date_ending: date
    report_type: str
    reported_currency: str
    total_assets: Optional[float] = None
    total_current_assets: Optional[float] = None
    cash_and_equivalents: Optional[float] = None
    cash_and_short_term_investments: Optional[float] = None
    inventory: Optional[float] = None
    current_receivables: Optional[float] = None
    property_plant_equipment: Optional[float] = None
    intangible_assets: Optional[float] = None
    goodwill: Optional[float] = None
    short_term_investments: Optional[float] = None
    total_liabilities: Optional[float] = None
    total_current_liabilities: Optional[float] = None
    short_term_debt: Optional[float] = None
    long_term_debt: Optional[float] = None
    total_debt: Optional[float] = None
    total_non_current_liabilities: Optional[float] = None
    total_shareholder_equity: Optional[float] = None
    retained_earnings: Optional[float] = None
    shares_outstanding: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)

class BalanceSheetsList(BaseModel):
    balance_sheets: list[BalanceSheet]
    
    model_config = ConfigDict(from_attributes=True)

class CashFlowStatement(BaseModel):
    fiscal_date_ending: date
    report_type: str
    reported_currency: str
    operating_cash_flow: Optional[float] = None
    capital_expenditures: Optional[float] = None
    investing_cash_flow: Optional[float] = None
    financing_cash_flow: Optional[float] = None
    dividend_payout: Optional[float] = None
    stock_based_compensation: Optional[float] = None
    net_income: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)

class CashFlowStatementsList(BaseModel):
    cash_flow_statements: list[CashFlowStatement]
    
    model_config = ConfigDict(from_attributes=True)


class Profitability(BaseModel):
    gross_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    net_margin: Optional[float] = None


class FinancialHealth(BaseModel):
    cash: Optional[float] = None
    debt: Optional[float] = None
    equity: Optional[float] = None
    debt_to_equity: Optional[float] = None


class CashFlow(BaseModel):
    operating_cash_flow: Optional[float] = None
    capital_expenditure: Optional[float] = None
    free_cash_flow: Optional[float] = None


class FinancialHealthResponse(BaseModel):
    profitability: Profitability
    financial_health: FinancialHealth
    cash_flow: CashFlow