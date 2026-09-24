from fastapi import APIRouter, HTTPException

from app.models.prices import Price, PriceList, PricePerformance
from app.services.stock_price_service import StockPriceService

router = APIRouter(
    prefix="/api/v1/companies",
    tags = ["Stock Prices"]
)
stock_service = StockPriceService()


@router.get("/{symbol}/price", response_model=PriceList)
async def get_company_price(symbol: str):
    prices = stock_service.get_stock_prices(symbol)
    if not prices:
        raise HTTPException(
            status_code=404,
            detail=f"Company with symbol '{symbol}' was not found.",
        )
    return {"prices": prices}

@router.get("/{symbol}/price_performance", response_model=PricePerformance)
async def get_company_price_performance(symbol: str):
    performance = stock_service.get_company_performance(symbol)
    if not performance:
        raise HTTPException(
            status_code=404,
            detail=f"There is no data for this '{symbol}'.",
        )
    return performance