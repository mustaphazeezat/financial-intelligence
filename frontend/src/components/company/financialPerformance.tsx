"use client";

import { useMemo, useState } from "react";
import dynamic from "next/dynamic";
import { Listbox, ListboxOption, ListboxOptions } from "@headlessui/react";
import { IncomeStatementList } from "@/types/financial";

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

type FinPerformanceProps = {
    incomeStatement: IncomeStatementList;
    period: string;
    symbol: string;
};

const metrics = [
    { label: "Revenue", key: "revenue" },
    { label: "Net Income", key: "net_income" },
    { label: "Operating Income", key: "operating_income" },
    { label: "EBITDA", key: "ebitda" },
] as const;

function FinancialPerformance({
    incomeStatement,
}: FinPerformanceProps) {
    const [selectedMetric, setSelectedMetric] = useState(metrics[0]);

    const statements = useMemo(
        () =>
            [...incomeStatement.income_statements].sort(
                (a, b) =>
                    new Date(a.fiscal_date_ending).getTime() -
                    new Date(b.fiscal_date_ending).getTime()
            ),
        [incomeStatement]
    );

    return (
        <div className="flex h-full min-h-[420px] flex-col rounded-xl border border-gray-800 bg-gray-900 p-4 sm:p-6">
            <div className="mb-4 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                    <p className="text-xs uppercase tracking-wider text-gray-500">
                        Financial performance
                    </p>
                    <h3 className="mt-1 text-xl font-semibold text-white">
                        {selectedMetric.label}
                    </h3>
                </div>

                <Listbox value={selectedMetric} onChange={setSelectedMetric}>
                    <div className="relative w-full sm:w-56">
                        <Listbox.Button className="flex w-full items-center justify-between rounded-lg border border-gray-700 bg-gray-800 px-4 py-2 text-left text-sm text-white">
                            {selectedMetric.label}
                            <span className="text-gray-400">⌄</span>
                        </Listbox.Button>

                        <ListboxOptions className="absolute z-10 mt-2 w-full rounded-lg border border-gray-700 bg-gray-800 p-1 shadow-xl">
                            {metrics.map((metric) => (
                                <ListboxOption
                                    key={metric.key}
                                    value={metric}
                                    className={({ active }) =>
                                        `cursor-pointer rounded-md px-3 py-2 text-sm ${
                                            active
                                                ? "bg-gray-700 text-white"
                                                : "text-gray-300"
                                        }`
                                    }
                                >
                                    {metric.label}
                                </ListboxOption>
                            ))}
                        </ListboxOptions>
                    </div>
                </Listbox>
            </div>

            <div className="min-h-0 flex-1">
                <Plot
                    data={[
                        {
                            x: statements.map(
                                (statement) => statement.fiscal_date_ending
                            ),
                            y: statements.map(
                                (statement) => statement[selectedMetric.key] / 1_000_000_000
                            ),
                            type: "scatter",
                            mode: "lines+markers",
                            line: { color: "#2E8B57", width: 3 },
                            marker: { color: "#2E8B57" },
                            hovertemplate:
                                "<b>%{x}</b><br>$%{y:,.2f}B<extra></extra>",
                        },
                    ]}
                    layout={{
                        autosize: true,
                        paper_bgcolor: "transparent",
                        plot_bgcolor: "transparent",
                        font: { color: "#d1d5db" },
                        margin: { t: 10, r: 10, b: 50, l: 70 },
                        xaxis: { gridcolor: "#374151" },
                        yaxis: {
                            gridcolor: "#374151",
                            tickprefix: "$",
                            ticksuffix: "B",
                        },
                    }}
                    config={{
                        responsive: true,
                        displaylogo: false,
                    }}
                    useResizeHandler
                    style={{ width: "100%", height: "100%" }}
                />
            </div>
        </div>
    );
}

export default FinancialPerformance;