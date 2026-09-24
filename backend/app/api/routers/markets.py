from fastapi import APIRouter, HTTPException

from app.services.market_service import MarketService
from app.models.markets import MarketMoversResponse, MarketMoversType
from typing import Optional

router = APIRouter(
    prefix="/api/v1/market_movers",
    tags = ["Market movers"]
)

market_services = MarketService()

@router.get("/", response_model=MarketMoversResponse)
def get_market_movers_by_tpe(movers_type: Optional[MarketMoversType] = None):
    market_movers = market_services.get_market_movers_data(movers_type)
    if not market_movers:
        raise HTTPException(
            status_code=404,
            detail=f"There are currently no information. Try again some other time",
        )
    return {"category": movers_type, "movers": market_movers }
