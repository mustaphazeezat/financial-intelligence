"use client";

import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import { useTransition } from "react";

interface FinancialTabsProps {
    symbol: string;
    period: string;
}

export default function FinancialTabs({
    symbol,
    period,
}: FinancialTabsProps) {
    const pathname = usePathname();
    const searchParams = useSearchParams();
    const [isPending, startTransition] = useTransition();

    const periods = ["quarter", "annual"];

    return (
        <div className="flex rounded-lg bg-gray-800 p-1">
            {periods.map((item) => {
                const params = new URLSearchParams(searchParams.toString());
                params.set("period", item);

                return (
                    <Link
                        key={item}
                        href={`${pathname}?${params.toString()}`}
                        onClick={() => startTransition(() => {})}
                        scroll={false}
                        className={`rounded-md px-3 py-2 text-sm capitalize ${
                            period === item
                                ? "bg-[#2E8B57] text-white"
                                : "text-gray-400 hover:text-white"
                        }`}
                    >
                        {isPending && period !== item ? "Loading..." : item}
                    </Link>
                );
            })}
        </div>
    );
}