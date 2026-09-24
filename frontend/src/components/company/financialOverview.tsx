"use client";

import { formatCurrency } from "@/lib/formater";
import { IncomeStatementList } from "@/types/financial";

type FinOverviewProps = {
    incomeStatement: IncomeStatementList;
    period: string;
    symbol: string;
};

function FinancialOverview({
    incomeStatement,
    period,
    symbol,
}: FinOverviewProps) {
    const statements = [...incomeStatement.income_statements]
        .filter(
            (statement) =>
                statement.report_type.toLowerCase() === period.toLowerCase()
        )
        .sort(
            (a, b) =>
                new Date(b.fiscal_date_ending).getTime() -
                new Date(a.fiscal_date_ending).getTime()
        );

    const latest = statements[0];
    const previous = statements[1];

    if (!latest) return null;

    const metrics = [
        ["Revenue", latest.revenue, previous?.revenue],
        ["Net Income", latest.net_income, previous?.net_income],
        ["Operating Income", latest.operating_income, previous?.operating_income],
        ["EBITDA", latest.ebitda, previous?.ebitda],
    ] as const;

    return (
        <section className="rounded-2xl border border-gray-800 bg-gray-900 p-4 shadow-lg">
            <div className="mb-5">
                <h3 className="text-xl font-semibold text-white">Overview</h3>
                <p className="mt-1 text-sm text-gray-500">
                    {symbol} · {latest.fiscal_date_ending}
                </p>
            </div>

            <div className="grid grid-cols-1 gap-3">
                {metrics.map(([label, value, previousValue]) => {
                    const growth =
                        previousValue != null && previousValue !== 0
                            ? ((value - previousValue) /
                                  Math.abs(previousValue)) *
                              100
                            : null;

                    return (
                        <div
                            key={label}
                            className="rounded-xl border border-gray-800 bg-gray-950 p-3"
                        >
                            <p className="text-sm text-gray-400">{label}</p>

                            <p className="mt-2 text-lg font-semibold text-white">
                                {formatCurrency(value)}
                            </p>

                            <p
                                className={`mt-2 text-sm font-medium ${
                                    growth == null
                                        ? "text-gray-500"
                                        : growth >= 0
                                          ? "text-[#2E8B57]"
                                          : "text-red-400"
                                }`}
                            >
                                {growth == null
                                    ? "—"
                                    : `${growth >= 0 ? "↑" : "↓"} ${Math.abs(
                                          growth
                                      ).toFixed(1)}% YoY`}
                            </p>
                        </div>
                    );
                })}
            </div>
        </section>
    );
}

export default FinancialOverview;