from app.services.financial_service import FinancialServices
from fastapi import APIRouter, HTTPException


from app.models.finance import BalanceSheetsList, CashFlowStatementsList, FinancialHealthResponse, IncomeStatementsList, FinancialReportType
from typing import Optional

router = APIRouter(
    prefix="/api/v1/financial_statements",
    tags = ["Financial statements"],
)

financial_service = FinancialServices()


@router.get("/income_statement/{symbol}/{financial_report_type}", response_model=IncomeStatementsList)
async def get_income_statements(symbol: str, financial_report_type: Optional[FinancialReportType] = None):
    statements = financial_service.get_income_statement(symbol, financial_report_type)
    
    if not statements:
        raise HTTPException(
            status_code=404,
            detail=f"Company with symbol '{symbol}' was not found.",
        )
    return {"income_statements": statements}


@router.get("/balance_sheets/{symbol}/{financial_report_type}", response_model=BalanceSheetsList)

async def get_balance_sheets(symbol: str, financial_report_type: FinancialReportType):
    statements = financial_service.get_balance_sheet(symbol, financial_report_type)
    if not statements:
        raise HTTPException(
            status_code=404,
            detail=f"Company with symbol '{symbol}' was not found.",
        )
    return {"balance_sheets": statements}

@router.get("/financial_health/{symbol}/{financial_report_type}", response_model=FinancialHealthResponse)

async def get_financial_health( symbol: str, financial_report_type: FinancialReportType):
    health = financial_service.get_financial_health(symbol, financial_report_type)

    if not health:
        raise HTTPException(
            status_code=404,
            detail=f"Could not fetch financial health of '{symbol}'",
        )
    return health

@router.get("/cash_flows/{symbol}/{financial_report_type}", response_model=CashFlowStatementsList)
async def get_cash_flows(symbol: str, financial_report_type: FinancialReportType):
    statements = financial_service.get_cash_flow(symbol, financial_report_type)
    if not statements:
        raise HTTPException(
            status_code=404,
            detail=f"Company with symbol '{symbol}' was not found.",
        )
    return {"cash_flow_statements": statements}