from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Price(BaseModel):
    date: date
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[int] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None
    vwap: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class PriceList(BaseModel):
    prices: list[Price]

    model_config = ConfigDict(from_attributes=True)


class PerformancePeriods(BaseModel):
    one_day: Optional[float] = None
    one_month: Optional[float] = None
    three_months: Optional[float] = None
    six_months: Optional[float] = None
    one_year: Optional[float] = None


class TradingActivity(BaseModel):
    volume: Optional[float] = None
    vwap: Optional[float] = None


class CompanyPerformanceResponse(BaseModel):
    symbol: str
    performance: PerformancePeriods
    trading_activity: TradingActivity

class PricePerformance(BaseModel):
    symbol: str

    performance: dict[str, Optional[float]]

    trading_activity: dict[str, Optional[float]]