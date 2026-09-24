
from typing import Optional

from app.db.industry_repository import get_industry_by_id_db, get_or_create_industry, get_or_create_sector
from app.db.company_repository import get_all_companies_db, get_all_industries_db, get_all_sectors_db, get_company_by_symbol_db, save_company, save_company_AV
from app.clients.alpha_vantage import AlphaVantageClient
from app.clients.fmp import FMPClient
from app.helpers import is_in_symbol, normalize_name
from app.clients.massive import MassiveClient
from app.db.normalise_data import normalise_massive_comp


class CompanyServices:
    def __init__(self):
        self.alpha_vantage = AlphaVantageClient()
        self.fmp = FMPClient()
        self.massive = MassiveClient()

    def get_all_companies(
        self,
        search: Optional[str] = None,
        industry: Optional[str] = None,
        sector: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ):
        skip = max(skip, 0)
        limit = min(max(limit, 1), 100)

        result = get_all_companies_db(
            search=search,
            skip=0,
            limit=1000,
        )

        companies = result["companies"]

        if industry:
            industry_name = industry.strip().lower()
            companies = [
                company
                for company in companies
                if (company.get("industry_name") or "").strip().lower() == industry_name
            ]

        if sector:
            sector_name = sector.strip().lower()
            companies = [
                company
                for company in companies
                if (company.get("sector_name") or "").strip().lower() == sector_name
            ]

        total = len(companies)
        paginated = companies[skip: skip + limit]

        return {
            "companies": paginated,
            "total": total,
            "current_page": (skip // limit) + 1 if limit else 1,
            "has_next_page": skip + limit < total,
        }
    def get_all_industry(self):
        return get_all_industries_db()

    def get_all_sectors(self):
        return get_all_sectors_db()

    def get_company_by_symbol(self, symbol: str):
        symbol = symbol.upper()

        # Check database first
        company = get_company_by_symbol_db(symbol.lower())

        if company is not None:
            return company

        # FMP

        if is_in_symbol(symbol):
            try:
                profile = self.fmp.get_company_profile(symbol)

                if profile:
                    company = profile[0]

                    sector_name = normalize_name(
                        company.get("sector")
                    )

                    industry_name = normalize_name(
                        company.get("industry")
                    )

                    sector_id = None
                    industry_id = None

                    if sector_name:
                        sector_id = get_or_create_sector(
                            sector_name
                        )

                    if industry_name and sector_id:
                        industry_id = get_or_create_industry(
                            industry_name,
                            sector_id
                        )

                    if not sector_name or not industry_name:
                        print(
                            f"Missing sector/industry for {symbol}"
                        )

                    save_company(
                        company=company,
                        industry_id=industry_id
                    )

                    return get_company_by_symbol_db(
                        symbol.lower()
                    )

            except Exception as e:
                print(f"FMP failed for {symbol}: {e}")

        # Massive

        try:
            print(symbol)
            company = self.massive.get_company_profile(symbol)

            if company:
                sector_name = normalize_name(
                    company.get("Sector")
                )

                industry_name = normalize_name(
                    company.get("sic_description")
                )

                sector_id = None
                industry_id = None

                if sector_name:
                    sector_id = get_or_create_sector(
                        sector_name
                    )

                if industry_name and sector_id:
                    industry_id = get_or_create_industry(
                        industry_name,
                        sector_id
                    )

                if not sector_name or not industry_name:
                    print(
                        f"Missing sector/industry for {symbol}"
                    )
                normalise_company = normalise_massive_comp(company)
                save_company(
                    company=normalise_company,
                    industry_id=industry_id
                )
                return get_company_by_symbol_db(
                    symbol.lower()
                )

        except Exception as e:
            print(f"Massive failed for {symbol}: {e}")

        # Alpha Vantage fallback

        try:
            company = self.alpha_vantage.get_company_profile(
                symbol
            )

            if company:
                sector_name = normalize_name(
                    company.get("Sector")
                )

                industry_name = normalize_name(
                    company.get("Industry")
                )

                sector_id = None
                industry_id = None

                if sector_name:
                    sector_id = get_or_create_sector(
                        sector_name
                    )

                if industry_name and sector_id:
                    industry_id = get_or_create_industry(
                        industry_name,
                        sector_id
                    )

                if not sector_name or not industry_name:
                    print(
                        f"Missing sector/industry for {symbol}"
                    )

                save_company_AV(
                    company=company,
                    industry_id=industry_id
                )

                return get_company_by_symbol_db(
                    symbol.lower()
                )

        except Exception as e:
            print(
                f"Alpha Vantage failed for {symbol}: {e}"
            )

        # ----------------------------------------
        # 5. Nothing worked
        # ----------------------------------------

        return None

    def get_industry_by_id(id: int):
        industry =  get_industry_by_id_db(id)
