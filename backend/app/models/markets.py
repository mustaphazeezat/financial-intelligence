from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

class MarketMoversType(str, Enum):
    gainers = "gainers"
    losers = "losers"
    most_active = "active"

class MarketMover(BaseModel):
    symbol: str
    category: str
    price: Optional[float] = None
    change_amount: Optional[float] = None
    change_percentage: Optional[float] = None
    volume: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class MarketMoversResponse(BaseModel):
    category: MarketMoversType
    movers: List[MarketMover] = []

    model_config = ConfigDict(from_attributes=True)
