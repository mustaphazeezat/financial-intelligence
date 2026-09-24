import { Companies, Company, Industry } from "@/types/company";

const API_URL = process.env.NEXT_PUBLIC_API_URL;


export async function getCompanies(
    search?: string,
    skip = 0,
    limit = 10,
    industry?: string,
    sector?: string
): Promise<Companies> {
    const params = new URLSearchParams({
        skip: String(Math.max(skip, 0)),
        limit: String(Math.min(Math.max(limit, 1), 100)),
    });

    if (search?.trim()) {
        params.set("search", search.trim());
    }

    if (industry?.trim()) {
        params.set("industry", industry.trim());
    }

    if (sector?.trim()) {
        params.set("sector", sector.trim());
    }

    const response = await fetch(`${API_URL}/api/v1/companies?${params.toString()}`);

    if (!response.ok) {
        if (response.status === 404) {
            return {
                companies: [],
                total: 0,
                current_page: 1,
                has_next_page: false,
            };
        }

        throw new Error("Failed to fetch companies");
    }

    const data = await response.json();

    return data ?? {
        companies: [],
        total: 0,
        current_page: 1,
        has_next_page: false,
    };
}

export async function getCompanyBySymbol(symbol?: string): Promise<Company | null> {
 

  const url = `${API_URL}/api/v1/companies/${symbol}`;


  const response = await fetch(url);

  if (response.status === 404) {
    return null;
  }

  if (!response.ok) {
    const error = await response.text();
    console.log("API error:", error);
    throw new Error("Failed to fetch companies");
  }

  const data = await response.json();

  return data;
}

type IndustryData = {
  "industries": Industry[]
} 

export async function getIndustries(): Promise<IndustryData> {
    const url = `${API_URL}/api/v1/companies/industries`;
    const response = await fetch(url);

    if (response.status === 404) {
        return {"industries": []};
    }

    if (!response.ok) {
        const error = await response.text();
        console.log("API error:", error);
        throw new Error("Failed to fetch industry data");
    }

    const data = await response.json();

    return data.industries;
}
