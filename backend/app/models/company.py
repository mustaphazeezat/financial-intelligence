from typing import Optional

from pydantic import BaseModel, ConfigDict


class Company(BaseModel):
    id: int
    symbol: str
    company_name: str
    exchange: Optional[str] = None
    industry_name:  Optional[str] = None
    sector_name: Optional[str] = None
    country: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyList(BaseModel):
    companies: list[Company]
    total: int
    current_page: int
    has_next_page: bool

    model_config = ConfigDict(from_attributes=True)


class Industry(BaseModel):
    id: int
    industry_name: str
    sector_name: str

class IndustryList(BaseModel):
    industries: list[Industry]
