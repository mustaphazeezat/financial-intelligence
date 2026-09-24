import FinancialCards from "@/components/company/financialCards";
import FinancialOverview from "@/components/company/financialOverview";
import FinancialPerformance from "@/components/company/financialPerformance";
import FinancialTabs from "@/components/company/FinancialTabs";

import { getFinancialPerformance } from "@/lib/api/financial";

export default async function FinancialSection({
  symbol,
  period,
}: {
  symbol: string;
  period: "quarter" | "annual";
}) {
  const [financialPerformanceResult, financialHealthResult] =
    await Promise.allSettled([
      getFinancialPerformance(
        symbol,
        "income_statement",
        period
      ),
      getFinancialPerformance(
        symbol,
        "financial_health",
        period
      ),
    ]);

  const financialPerformance =
    financialPerformanceResult.status === "fulfilled"
      ? financialPerformanceResult.value
      : null;

  const financialHealth =
    financialHealthResult.status === "fulfilled"
      ? financialHealthResult.value
      : null;

  return (
    <>
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-2xl font-semibold text-white">
          Financials
        </h2>

        <FinancialTabs
          symbol={symbol}
          period={period}
        />
      </div>

      <div className="flex flex-col gap-6 lg:flex-row">
        {financialPerformance && (
          <div className="w-full shrink-0 lg:w-80">
            <FinancialOverview
              incomeStatement={financialPerformance}
              period={period}
              symbol={symbol}
            />
          </div>
        )}

        {financialPerformance && (
          <div className="min-w-0 flex-1">
            <FinancialPerformance
              incomeStatement={financialPerformance}
              period={period}
              symbol={symbol}
            />
          </div>
        )}
      </div>

      <div className="py-6">
        {financialHealth && (
          <FinancialCards financialHealth={financialHealth} />
        )}
      </div>
    </>
  );
}