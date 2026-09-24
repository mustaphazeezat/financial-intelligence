"use client";

import dynamic from "next/dynamic";
import { Price } from "@/types/price";
import { useState } from "react";

const Plot = dynamic(() => import("react-plotly.js"), {
    ssr: false,
});

type PricePerformanceProps = {
    priceList: Price[];
};

function PricePerform({ priceList }: PricePerformanceProps) {
    const [chartType, setChartType] = useState<"line" | "candlestick">("line");
    const sortedPrices = [...priceList].sort(
        (a, b) =>
            new Date(a.date).getTime() - new Date(b.date).getTime()
    );

    return (
        <div className="flex h-full min-h-105 flex-col rounded-xl border border-gray-800 bg-gray-900 p-4 sm:p-6">
            <div className="mb-4 flex items-center justify-between">
                <h2 className="text-xl font-semibold text-white">
                    Price History
                </h2>

                <div className="flex rounded-lg bg-gray-800 p-1">
                    {(["line", "candlestick"] as const).map((type) => (
                        <button
                            key={type}
                            type="button"
                            onClick={() => setChartType(type)}
                            className={`rounded-md px-3 py-1.5 text-sm font-medium capitalize transition ${
                                chartType === type
                                    ? "bg-[#2E8B57] text-white"
                                    : "text-gray-400 hover:text-white"
                            }`}
                        >
                            {type === "line" ? "Line" : "Candlestick"}
                        </button>
                    ))}
                </div>
            </div>

            {chartType === "line" ? (
                <Plot
                    data={[
                        {
                            x: sortedPrices.map((price) => price.date),
                            y: sortedPrices.map((price) => Number(price.close)),
                            type: "scatter",
                            mode: "lines",
                            name: "Close",

                            line: {
                                color: "#2E8B57",
                                width: 2,
                            },

                            hovertemplate:
                                "<b>%{x}</b><br>" +
                                "Close: $%{y:.2f}" +
                                "<extra></extra>",
                        },
                    ]}
                    layout={{
                        autosize: true,
                        paper_bgcolor: "#000",
                        plot_bgcolor: "transparent",
                        font: {
                            color: "#d1d5db",
                        },
                        showlegend: false,
                        margin: {
                            t: 20,
                            r: 20,
                            b: 40,
                            l: 65,
                        },

                        xaxis: {
                            type: "date",

                            showgrid: false,
                            zeroline: false,

                            rangeslider: {
                                visible: false,
                            },

                            rangeselector: {
                                bgcolor: "#1f2937",      
                                activecolor: "#2E8B57", 
                                font: {
                                    color: "#d1d5db",
                                },
                                buttons: [
                                    {
                                        count: 1,
                                        label: "1M",
                                        step: "month",
                                        stepmode: "backward",
                                    },
                                    {
                                        count: 3,
                                        label: "3M",
                                        step: "month",
                                        stepmode: "backward",
                                    },
                                    {
                                        count: 6,
                                        label: "6M",
                                        step: "month",
                                        stepmode: "backward",
                                    },
                                    {
                                        step: "year",
                                        stepmode: "todate",
                                        label: "YTD",
                                    },
                                    {
                                        count: 1,
                                        label: "1Y",
                                        step: "year",
                                        stepmode: "backward",
                                    },
                                    {
                                        step: "all",
                                        label: "All",
                                    },
                                ],
                            },
                        },

                        yaxis: {
                            title: "",

                            tickprefix: "$",
                            tickformat: ",.2f",

                            gridcolor: "#374151",
                            zeroline: false,

                            fixedrange: false,
                        },

                        hovermode: "x",
                    }}

                    config={{
                        responsive: true,
                        displaylogo: false,
                        displayModeBar: false,
                        modeBarButtonsToRemove: [
                            "zoom2d",
                            "pan2d",
                            "select2d",
                            "lasso2d",
                            "zoomIn2d",
                            "zoomOut2d",
                            "autoScale2d",
                            "resetScale2d",
                        ],
                    }}

                    style={{ width: "100%", height: "100%" }}
                    useResizeHandler
                /> 
            ) : (
               <Plot
                    data={[
                        {
                            x: sortedPrices.map((price) => price.date),
                            open: sortedPrices.map((price) => Number(price.open)),
                            high: sortedPrices.map((price) => Number(price.high)),
                            low: sortedPrices.map((price) => Number(price.low)),
                            close: sortedPrices.map((price) => Number(price.close)),

                            type: "candlestick",

                            name: "Price",

                            increasing: {
                                line: {
                                    color: "#2E8B57",
                                },
                            },

                            decreasing: {
                                line: {
                                    color: "#ef4444",
                                },
                            },

                            hovertemplate:
                                "<b>%{x}</b><br>" +
                                "Open: $%{open:.2f}<br>" +
                                "High: $%{high:.2f}<br>" +
                                "Low: $%{low:.2f}<br>" +
                                "Close: $%{close:.2f}" +
                                "<extra></extra>",
                        },
                    ]}
                    layout={{
                        autosize: true,
                        showlegend: false,
                        paper_bgcolor: "#000",
                        plot_bgcolor: "transparent",

                        font: {
                            color: "#d1d5db",
                        },

                        margin: {
                            t: 10,
                            r: 20,
                            b: 40,
                            l: 60,
                        },

                        xaxis: {
                            type: "date",

                            gridcolor: "#374151",
                            zeroline: false,

                            rangeslider: {
                                visible: true,
                                thickness: 0.08,
                            },

                            rangeselector: {
                                bgcolor: "#1f2937",      
                                activecolor: "#2E8B57", 
                                font: {
                                    color: "#d1d5db",
                                },
                                buttons: [
                                    {
                                        count: 1,
                                        label: "1M",
                                        step: "month",
                                        stepmode: "backward",
                                    },
                                    {
                                        count: 3,
                                        label: "3M",
                                        step: "month",
                                        stepmode: "backward",
                                    },
                                    {
                                        count: 6,
                                        label: "6M",
                                        step: "month",
                                        stepmode: "backward",
                                    },
                                    {
                                        step: "year",
                                        stepmode: "todate",
                                        label: "YTD",
                                    },
                                    {
                                        count: 1,
                                        label: "1Y",
                                        step: "year",
                                        stepmode: "backward",
                                    },
                                    {
                                        step: "all",
                                        label: "All",
                                    },
                                ],
                            },

                            showgrid: false,
                        },

                        yaxis: {
                            tickprefix: "$",
                            tickformat: ",.2f",

                            gridcolor: "#374151",
                            zeroline: false,

                            fixedrange: false,
                        },

                        hovermode: "x unified",

                       
                    }}

                    config={{
                        responsive: true,
                        displaylogo: false,
                        displayModeBar: false,
                        modeBarButtonsToRemove: [
                            "zoom2d",
                            "pan2d",
                            "select2d",
                            "lasso2d",
                            "zoomIn2d",
                            "zoomOut2d",
                            "autoScale2d",
                            "resetScale2d",
                        ],
                    }}

                    style={{ width: "100%", height: "100%" }}
                    useResizeHandler
                />
            )}
        </div>
    );
}

export default PricePerform;