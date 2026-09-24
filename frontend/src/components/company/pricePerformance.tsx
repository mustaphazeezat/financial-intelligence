import { formatCurrency, formatPercentage, formatVolume } from "@/lib/formater";
import { CompanyPerformance } from "@/types/price";

type PricePerformanceProps = {
    data: CompanyPerformance | null ;
};

const periods = [
    ["1D", "1d"],
    ["1M", "1m"],
    ["3M", "3m"],
    ["6M", "6m"],
    ["1Y", "1y"],
] as const;

export default function PricePerformance({
    data,
}: PricePerformanceProps) {
    
    return (
        <div className="space-y-6">
            <div className="rounded-2xl border border-gray-800 bg-gray-900 p-5 shadow-lg">
                <h2 className="mb-5 text-sm font-semibold uppercase tracking-wider text-gray-400">
                    Performance
                </h2>

                <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-1">
                    {periods.map(([label, key]) => {
                        const value = data?.performance?.[key];

                        return (
                            <div
                                key={label}
                                className="rounded-xl border border-gray-800 bg-gray-950 p-2"
                            >
                                <p className="text-xs font-medium text-gray-300">
                                    {label}
                                </p>
                                <p
                                    
                                    className={`mt-1 text-base font-semibold ${
                                        value != null && value < 0
                                            ? "text-red-400"
                                            : "text-emerald-400"
                                    }`}
                                >
                                    {formatPercentage(value)}
                                </p>
                            </div>
                        );
                    })}
                </div>
            </div>

            <div className="rounded-2xl border border-gray-800 bg-gray-900 p-5 shadow-lg">
                <h2 className="mb-5 text-sm font-semibold uppercase tracking-wider text-gray-400">
                    Trading Activity
                </h2>

                <div className="space-y-3">
                    <div className="flex items-center justify-between rounded-xl bg-gray-950 p-4">
                        <span className="text-sm text-gray-300">Volume</span>
                        <span className="font-semibold text-white">
                            {formatVolume(data?.trading_activity?.volume)}
                        </span>
                    </div>

                    <div className="flex items-center justify-between rounded-xl bg-gray-950 p-4">
                        <span className="text-sm text-gray-300">VWAP</span>
                        <span className="font-semibold text-white">
                            {formatCurrency(data?.trading_activity?.vwap)}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    );
}