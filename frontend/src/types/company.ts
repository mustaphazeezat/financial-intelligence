export interface Company {
  id: number;
  symbol: string;
  company_name: string;
  exchange: string;
  industry_name?: string | null;
  sector_name?: string | null;
  website: string;
  country: string;
  description: string;
}

export interface Companies {
  companies: Company[]
  total: number
  current_page: number
  has_next_page: boolean

}

export interface Industry {
  id: number;
  industry_name: string | null;
  sector_name: string | null;
}

