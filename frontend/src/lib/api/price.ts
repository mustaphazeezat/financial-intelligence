import { CompanyPerformance, Price } from "@/types/price";

const API_URL = process.env.NEXT_PUBLIC_API_URL;



export async function getStockPrice(symbol?: string): Promise<Price[]> {
    const url = `${API_URL}/api/v1/companies/${symbol}/price`;
    const response = await fetch(url, {cache: "no-store"});

    if (response.status === 404) {
        return [];
    }

    if (!response.ok) {
        const error = await response.text();
        console.log("API error:", error);
        throw new Error("Failed to fetch companies");
    }

    const data = await response.json();

    return data.prices;
}

export async function getPricePerformance(
    symbol?: string
): Promise<CompanyPerformance | null> {
    if (!symbol) return null;

    const url = `${API_URL}/api/v1/companies/${encodeURIComponent(
        symbol
    )}/price_performance`;

    const response = await fetch(url);

    if (response.status === 404) {
        return null;
    }

    if (!response.ok) {
        const error = await response.text();
        console.error("API error:", error);
        throw new Error("Failed to fetch price performance");
    }

    const data = await response.json();

    return data;
}
