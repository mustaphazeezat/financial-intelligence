"use client";

import SectionWrapper from "../sectionWrapper"
import { Mover } from "@/types/movers";
import { formatChange, formatPercentage, formatPrice, formatVolume } from "@/lib/formater";
import Link from "next/link";

type MoversSectionProps = {
  gainers: Mover[];
  losers: Mover[];
  mostActive: Mover[];
};

function MoversSection({
  gainers,
  losers,
  mostActive,
}: MoversSectionProps) {

   const tableHeaders = (
        <thead className="border-b border-gray-700 bg-gray-800/70">
            <tr>
                {["Company", "Price", "Change", "% Change", "Volume"].map(
                    (header) => (
                        <th
                            key={header}
                            className="whitespace-nowrap px-3 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-400"
                        >
                            {header}
                        </th>
                    )
                )}
            </tr>
        </thead>
    );

    const renderRows = (movers: Mover[]) =>
        movers.map((mover, index) => (
            <tr
                key={`${mover.symbol}${index}`}
                className="relative border-b border-gray-800 transition-colors hover:bg-gray-800/50"
            >
                <td className="px-3 py-3 text-sm font-medium text-white">
                    <Link
                        href={`/companies/${mover.symbol}`}
                        className="absolute inset-0 z-10"
                        aria-label={`View ${mover.symbol}`}
                    />

                    <span className="relative">
                        {mover.symbol}
                    </span>
                </td>
                <td className="px-3 py-3 text-sm text-gray-300">
                    {formatPrice(mover.price)}
                </td>
                <td className="px-3 py-3 text-sm text-gray-300">
                    { formatChange(mover.change_amount)}
                </td>
                <td className={`px-3 py-3 text-sm font-medium ${
                        mover.change_percentage > 0
                            ? "text-[#2E8B57]"
                            : mover.change_amount < 0
                              ? "text-red-400"
                              : "text-gray-300"
                    }`}>
                    {formatPercentage(mover.change_percentage)}
                </td>
                <td className="px-3 py-3 text-sm text-gray-300">
                    {formatVolume(mover.volume)}
                </td>
            </tr>
        ));

    return (
        <section className="py-6">
            <SectionWrapper>
                <h2 className="mb-9 text-2xl font-semibold text-white">
                    Top movers in the US market
                </h2>

                

                
                    <div>
                         <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                        <div className="min-w-0 rounded-lg border border-gray-800 bg-gray-900 p-4">
                            <h3 className="mb-4 text-base font-semibold text-white">
                                Top Gainers
                            </h3>
                            {gainers &&  (

                                <div className="overflow-x-auto">
                                <table className="w-full min-w-[560px] text-left">
                                    {tableHeaders}
                                    <tbody>{renderRows(gainers)}</tbody>
                                </table>
                            </div>
                            )}
                            
                        </div>

                        <div className="min-w-0 rounded-lg border border-gray-800 bg-gray-900 p-4">
                            <h3 className="mb-4 text-base font-semibold text-white">
                                Top Losers
                            </h3>
                            {losers &&  (

                                <div className="overflow-x-auto">
                                <table className="w-full min-w-[560px] text-left">
                                    {tableHeaders}
                                    <tbody>{renderRows(losers)}</tbody>
                                </table>
                            </div>
                            )}
                            
                        </div>
                    </div>
                    <div className="most-active rounded-lg border border-gray-950 bg-gray-900 p-4 mt-20">
                         <h3 className="mb-4 text-base font-semibold text-white">
                            Most actively traded
                        </h3>
                        {mostActive &&  (

                                <div className="overflow-x-auto">
                                <table className="w-full min-w-[560px] text-left">
                                    {tableHeaders}
                                    <tbody>{renderRows(mostActive)}</tbody>
                                </table>
                            </div>
                            )}  
                    </div>
                    </div>
            </SectionWrapper>
        </section>
    );
}

export default MoversSection