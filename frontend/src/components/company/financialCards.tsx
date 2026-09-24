import { formatCurrency, formatPercentage } from "@/lib/formater";
import { FinancialHealth } from "@/types/financial";

type FinancialCardsProps = {
    financialHealth: FinancialHealth;
};

function Metric({
    label,
    value,
    numericValue,
}: {
    label: string;
    value: string;
    numericValue?: number | null;
}) {
    const valueColor =
    numericValue == null || numericValue === 0
        ? "text-white"
        : numericValue < 0
          ? "text-red-400"
          : "text-[#2E8B57]";

    return (
        <div className="flex items-center justify-between gap-4 border-b border-gray-800 py-3 last:border-0">
            <span className="text-sm text-gray-400">{label}</span>
            <span className={`text-sm font-semibold ${valueColor}`}>
                {value}
            </span>
        </div>
    );
}

export default function FinancialCards({
    financialHealth,
}: FinancialCardsProps) {

        const profitability = financialHealth.profitability
        const health = financialHealth.financial_health
        const cashFlow = financialHealth.cash_flow

    return (
        <div className="flex flex-col gap-6 lg:flex-row">
            <div className="rounded-2xl border border-gray-800 bg-gray-900 p-5">
                <h2 className="mb-3 text-sm font-semibold uppercase tracking-wider text-gray-400">
                    Profitability
                </h2>

                <Metric
                    label="Gross Margin"
                    value={formatPercentage(profitability.gross_margin)}
                    numericValue={profitability.gross_margin}
                />

                <Metric
                    label="Operating Margin"
                    value={formatPercentage(profitability.operating_margin)}
                    numericValue={profitability.operating_margin}
                />

                <Metric
                    label="Net Margin"
                    value={formatPercentage(profitability.net_margin)}
                    numericValue={profitability.net_margin}
                />
            </div>

            <div className="rounded-2xl border border-gray-800 bg-gray-900 p-5">
                <h2 className="mb-3 text-sm font-semibold uppercase tracking-wider text-gray-400">
                    Financial Health
                </h2>

                <Metric
                    label="Cash"
                    value={formatCurrency(health.cash)}
                    numericValue={health.cash}
                />

                <Metric
                    label="Debt"
                    value={formatCurrency(health.debt)}
                    numericValue={health.debt}
                />

                <Metric
                    label="Equity"
                    value={formatCurrency(health.equity)}
                    numericValue={health.equity}
                />

                <Metric
                    label="Debt / Equity"
                    value={formatPercentage(health.debt_to_equity)}
                    numericValue={health.debt_to_equity}
                />
            </div>
             <div className="rounded-2xl border border-gray-800 bg-gray-900 p-5">
                <h2 className="mb-3 text-sm font-semibold uppercase tracking-wider text-gray-400">
                    Cash Flow
                </h2>

                <Metric
                    label="Capital Expenditure"
                    value={formatCurrency(cashFlow.capital_expenditure)}
                    numericValue={cashFlow.capital_expenditure}
                />

                <Metric
                    label="Operating Cash Flow"
                    value={formatCurrency(cashFlow.operating_cash_flow)}
                    numericValue={cashFlow.operating_cash_flow}
                />

                <Metric
                    label="Free Cash Flow"
                    value={formatCurrency(cashFlow.free_cash_flow)}
                    numericValue={cashFlow.free_cash_flow}
                />
            </div>
        </div>
    );
}