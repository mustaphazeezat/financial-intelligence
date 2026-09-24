from typing import Optional

from sqlalchemy import text
import datetime
from app.db.database import engine
from app.helpers import to_number


def save_company(company:str, industry_id: int):

    query = text("""
        INSERT INTO companies (
            symbol,
            company_name,
            exchange,
            industry_id,
            country,
            website,
            description
        )
        VALUES (
            :symbol,
            :company_name,
            :exchange,
            :industry_id,
            :country,
            :website,
            :description
        )
        ON CONFLICT (symbol)
        DO UPDATE SET
            company_name = EXCLUDED.company_name,
            exchange = EXCLUDED.exchange,
            industry_id = EXCLUDED.industry_id,
            country = EXCLUDED.country,
            website = EXCLUDED.website,
            description = EXCLUDED.description
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "symbol": company["symbol"],
                "company_name": company["companyName"],
                "exchange": company.get("exchange"),
                "industry_id": industry_id,
                "country": company.get("country"),
                "website": company.get("website"),
                "description": company.get("description"),
            }
        )

def save_company_AV(company:str, industry_id: int):

    query = text("""
        INSERT INTO companies (
            symbol,
            company_name,
            exchange,
            industry_id,
            country,
            website,
            description
        )
        VALUES (
            :symbol,
            :company_name,
            :exchange,
            :industry_id,
            :country,
            :website,
            :description
        )
        ON CONFLICT (symbol)
        DO UPDATE SET
            company_name = EXCLUDED.company_name,
            exchange = EXCLUDED.exchange,
            industry_id = EXCLUDED.industry_id,
            country = EXCLUDED.country,
            website = EXCLUDED.website,
            description = EXCLUDED.description
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "symbol": company["Symbol"],
                "company_name": company["Name"],
                "exchange": company.get("Exchange"),
                "industry_id": industry_id,
                "country": company.get("Country"),
                "website": company.get("OfficialSite"),
                "description": company.get("Description"),
            }
        )

def get_company_id(symbol: str):
    
    query = text("""
        SELECT id FROM companies 
        WHERE LOWER(symbol) = LOWER(:symbol)
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"symbol": symbol}
        ).scalar_one_or_none()
    return result

from typing import Optional
from sqlalchemy import text


def get_all_companies_db(
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 15,
):
    search_value = (
        f"%{search.strip()}%"
        if search and search.strip()
        else None
    )

    query = text("""
        SELECT
            c.*,
            i.name AS industry_name,
            s.name AS sector_name
        FROM companies c
        LEFT JOIN industries i
            ON c.industry_id = i.id
        LEFT JOIN sectors s
            ON i.sector_id = s.id
        WHERE (
            CAST(:search AS TEXT) IS NULL
            OR LOWER(c.company_name) LIKE LOWER(:search)
            OR LOWER(c.symbol) LIKE LOWER(:search)
        )
        ORDER BY c.symbol
        LIMIT :limit
        OFFSET :skip
    """)

    count_query = text("""
        SELECT COUNT(*)
        FROM companies c
        WHERE (
            CAST(:search AS TEXT) IS NULL
            OR LOWER(c.company_name) LIKE LOWER(:search)
            OR LOWER(c.symbol) LIKE LOWER(:search)
        )
    """)

    params = {
        "search": search_value,
        "skip": skip,
        "limit": limit,
    }

    with engine.connect() as connection:
        companies = connection.execute(
            query,
            params
        ).mappings().all()

        total = connection.execute(
            count_query,
            {"search": search_value}
        ).scalar_one()

    return {
        "companies": [dict(company) for company in companies],
        "total": total,
    }

def get_all_industries_db():
    query = text("""
        SELECT
            i.id,
            i.name AS industry_name,
            s.name AS sector_name
        FROM industries i
        LEFT JOIN sectors s ON i.sector_id = s.id
        ORDER BY s.name, i.name
    """)

    with engine.connect() as connection:
        rows = connection.execute(query).mappings().all()
        return [dict(row) for row in rows]


def get_all_sectors_db():
    query = text("""
        SELECT
            id,
            name
        FROM sectors
        ORDER BY name
    """)

    with engine.connect() as connection:
        rows = connection.execute(query).mappings().all()
        return [dict(row) for row in rows]

def get_company_by_symbol_db(symbol: str):
    query = text("""
        SELECT
            c.*,
            i.name AS industry_name,
            s.name AS sector_name
        FROM companies c
        LEFT JOIN industries i
            ON c.industry_id = i.id
        LEFT JOIN sectors s
            ON i.sector_id = s.id
        WHERE LOWER(c.symbol) = :symbol
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"symbol": symbol}
        ).mappings().one_or_none()
    return result
