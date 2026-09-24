from fastapi import APIRouter, HTTPException, Query
from typing import Optional
 
from app.services.company_service import CompanyServices
from app.models.company import Company, CompanyList, IndustryList

router = APIRouter(
    prefix="/api/v1/companies",
    tags = ["Companies"]
)

company_service = CompanyServices()

@router.get(
    "/",
    summary="Get companies",
    description="Returns companies with optional search and filters.",
    response_model=CompanyList,
)
def get_companies(
    search: Optional[str] = Query(
        default=None,
        description="Search companies by name or symbol",
    ),
    industry: Optional[str] = Query(
        default=None,
        description="Filter by industry",
    ),
    sector: Optional[str] = Query(
        default=None,
        description="Filter by sector",
    ),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
):
    return company_service.get_all_companies(
        search=search,
        industry=industry,
        sector=sector,
        skip=skip,
        limit=limit,
    )

@router.get("/industries",
        summary="Get all industries",
        description="Returns all available industries with their respective sector name.", 
        response_model=IndustryList
)
async def get_all_industries():
    industry = company_service.get_all_industry()

    return {"industries": industry}

@router.get("/{symbol}",
    summary="Get a company by symbol",
    description="Returns the company's information.",
    response_model=Company)
async def get_company(symbol: str):
    company = company_service.get_company_by_symbol(symbol)
    if not company:
        raise HTTPException(
            status_code=404,
            detail=f"Company with symbol '{symbol}' was not found.",
        )
    return company




