"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { getCompanies } from "@/lib/api/companies";
import { Companies, Industry } from "@/types/company";
import { normalize } from "@/lib/formater";

type CompaniesTableProps = {
    companyData: Companies;
    industryData: Industry[];
};

function getUniqueValues(values: Array<string | null | undefined>): string[] {
    const unique = new Map<string, string>();

    values.forEach((value) => {
        if (!value?.trim()) return;

        const key = normalize(value);

        if (!unique.has(key)) {
            unique.set(key, value.trim());
        }
    });

    return [...unique.values()].sort((a, b) => a.localeCompare(b));
}

export default function CompaniesTable({
    companyData,
    industryData,
}: CompaniesTableProps) {
    const [exchange, setExchange] = useState("");
    const [sector, setSector] = useState("");
    const [industry, setIndustry] = useState("");
    const [tableData, setTableData] = useState<Companies>(companyData);
    const [isLoading, setIsLoading] = useState(false);

    const companies = tableData.companies;

    const exchanges = useMemo(
        () => getUniqueValues(companies.map((company) => company.exchange)),
        [companies]
    );

    const sectors = useMemo(
        () =>
            getUniqueValues(
                industryData.map((item) => item.sector_name )
            ),
        [industryData]
    );

    const industries = useMemo(
        () =>
            getUniqueValues(
                industryData.map((item) => item.industry_name)
            ),
        [industryData]
    );

    const filteredCompanies = useMemo(
        () =>
            companies.filter(
                (company) =>
                    (!exchange ||
                        normalize(company.exchange) === normalize(exchange)) &&
                    (!sector ||
                        normalize(company.sector_name) === normalize(sector)) &&
                    (!industry ||
                        normalize(company.industry_name) === normalize(industry))
            ),
        [companies, exchange, sector, industry]
    );

    const fetchByFilter = async (
        nextSector?: string,
        nextIndustry?: string
    ) => {
        setIsLoading(true);

        try {
            const result = await getCompanies(
                undefined,
                0,
                10,
                nextIndustry,
                nextSector
            );

            setTableData(result);
        } catch (error) {
            console.error("Filter request failed", error);
            setTableData(companyData);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSectorChange = async (value: string) => {
        setSector(value);
        await fetchByFilter(value, industry);
    };

    const handleIndustryChange = async (value: string) => {
        setIndustry(value);
        await fetchByFilter(sector, value);
    };

    const clearFilters = async () => {
        setExchange("");
        setSector("");
        setIndustry("");
        setTableData(companyData);
    };

    return (
        <div className="space-y-5">
            <div className="flex flex-wrap gap-3">
                <select
                    value={exchange}
                    onChange={(event) => setExchange(event.target.value)}
                    className="rounded-lg border border-gray-700 bg-gray-800 px-3 py-2 text-sm text-white"
                >
                    <option value="">All exchanges</option>
                    {exchanges.map((item) => (
                        <option key={item} value={item}>
                            {item}
                        </option>
                    ))}
                </select>

                <select
                    value={sector}
                    onChange={(event) => handleSectorChange(event.target.value)}
                    className="rounded-lg border border-gray-700 bg-gray-800 px-3 py-2 text-sm text-white"
                >
                    <option value="">All sectors</option>
                    {sectors.map((item) => (
                        <option key={item} value={item}>
                            {item}
                        </option>
                    ))}
                </select>

                <select
                    value={industry}
                    onChange={(event) => handleIndustryChange(event.target.value)}
                    className="rounded-lg border border-gray-700 bg-gray-800 px-3 py-2 text-sm text-white"
                >
                    <option value="">All industries</option>
                    {industries.map((item) => (
                        <option key={item} value={item}>
                            {item}
                        </option>
                    ))}
                </select>

                {(exchange || sector || industry) && (
                    <button
                        type="button"
                        onClick={clearFilters}
                        className="text-sm text-gray-400 hover:text-white"
                    >
                        Clear filters
                    </button>
                )}
            </div>

            {isLoading && (
                <div className="rounded-lg border border-gray-800 bg-gray-900 p-4 text-sm text-gray-400">
                    Loading companies...
                </div>
            )}

            <div className="overflow-hidden rounded-xl border border-gray-800 bg-gray-900">
                <div className="overflow-x-auto">
                    <table className="w-full min-w-[700px] text-left">
                        <thead className="border-b border-gray-800 bg-gray-800/60">
                            <tr>
                                {[
                                    "Company",
                                    "Symbol",
                                    "Exchange",
                                    "Sector",
                                    "Industry",
                                    "Country",
                                ].map((heading) => (
                                    <th
                                        key={heading}
                                        className="px-5 py-4 text-xs font-semibold uppercase tracking-wide text-gray-400"
                                    >
                                        {heading}
                                    </th>
                                ))}
                            </tr>
                        </thead>

                        <tbody>
                            {filteredCompanies.map((company) => (
                                <tr
                                    key={company.symbol}
                                    className="relative border-b border-gray-800 last:border-0 hover:bg-gray-800/50"
                                >
                                    <td className="px-5 py-4 text-sm font-medium text-white">
                                        <Link
                                            href={`/companies/${company.symbol}`}
                                            className="absolute inset-0 z-10"
                                            aria-label={`View ${company.symbol}`}
                                        />
                                        <span className="relative">
                                            {company.company_name}
                                        </span>
                                    </td>

                                    <td className="px-5 py-4 text-sm text-white">
                                        {company.symbol}
                                    </td>

                                    <td className="px-5 py-4 text-sm text-gray-400">
                                        {company.exchange?.trim() || "—"}
                                    </td>

                                    <td className="px-5 py-4 text-sm text-gray-400">
                                        {company.sector_name?.trim() || "—"}
                                    </td>

                                    <td className="px-5 py-4 text-sm text-gray-400">
                                        {company.industry_name?.trim() || "—"}
                                    </td>

                                    <td className="px-5 py-4 text-sm text-gray-400">
                                        {company.country?.trim() || "—"}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {filteredCompanies.length === 0 && !isLoading && (
                    <p className="p-6 text-center text-sm text-gray-400">
                        No companies found.
                    </p>
                )}

                <div className="flex items-center justify-between border-t border-gray-800 px-5 py-4">
                    <span className="text-sm text-gray-400">
                        Page {tableData.current_page} · {tableData.total} companies
                    </span>

                    <div className="flex gap-2">
                        <button
                            type="button"
                            disabled={tableData.current_page === 1}
                            onClick={async () => {
                                const nextPage =
                                    Math.max(tableData.current_page - 1, 1);

                                const result = await getCompanies(
                                    undefined,
                                    (nextPage - 1) * 10,
                                    10,
                                    industry || undefined,
                                    sector || undefined
                                );

                                setTableData(result);
                            }}
                            className="rounded-lg border border-gray-700 px-3 py-2 text-sm text-gray-300 disabled:opacity-40"
                        >
                            Previous
                        </button>

                        <button
                            type="button"
                            disabled={!tableData.has_next_page}
                            onClick={async () => {
                                const nextPage = tableData.current_page + 1;

                                const result = await getCompanies(
                                    undefined,
                                    (nextPage - 1) * 10,
                                    10,
                                    industry || undefined,
                                    sector || undefined
                                );

                                setTableData(result);
                            }}
                            className="rounded-lg border border-gray-700 px-3 py-2 text-sm text-gray-300 disabled:opacity-40"
                        >
                            Next
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}