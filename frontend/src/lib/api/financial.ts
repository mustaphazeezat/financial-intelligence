import { IncomeStatementList } from "@/types/financial";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function getFinancialPerformance(
    symbol: string,
    financial_report_type: string,
    report_period: string
): Promise<IncomeStatementList | null> {
    if (!symbol) return null;

    const url = `${API_URL}/api/v1/financial_statements/${financial_report_type}/${encodeURIComponent(
        symbol
    )}/${report_period}`;

    const response = await fetch(url);

    if (response.status === 404) {
        return null;
    }

    if (!response.ok) {
        const error = await response.text();
        console.error("API error:", error);
        throw new Error("Failed to fetch Comapny financial report");
    }

    const data = await response.json();

    return data;
}