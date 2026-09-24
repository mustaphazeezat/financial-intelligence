import { FinancialHealth, IncomeStatementList } from "@/types/financial";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function getFinancialPerformance(
  symbol: string,
  financial_report_type: "income_statement",
  report_period: "quarter" | "annual"
): Promise<IncomeStatementList | null>;

export async function getFinancialPerformance(
  symbol: string,
  financial_report_type: "financial_health",
  report_period: "quarter" | "annual"
): Promise<FinancialHealth | null>;

export async function getFinancialPerformance(
  symbol: string,
  financial_report_type: "income_statement" | "financial_health",
  report_period: "quarter" | "annual"
): Promise<IncomeStatementList | FinancialHealth | null> {
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
    throw new Error("Failed to fetch Company financial report");
  }

  const data = await response.json();

  return data;
}