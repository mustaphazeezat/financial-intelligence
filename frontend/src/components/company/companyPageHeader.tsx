import Link from "next/link";
import { useState } from "react";

type CompanyPageHeaderProps = {
    symbol: string;
};

function CompanyPageHeader({ symbol }: CompanyPageHeaderProps) {
    const [menuOpen, setMenuOpen] = useState(false);

    return (
        <header className="sticky top-0 z-50 border-b border-slate-900 bg-slate-950/80 backdrop-blur-sm">
            <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3 sm:px-6 lg:px-8">
                <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-black text-white">
                        <span className="text-lg font-black italic">FIP</span>
                    </div>

                    <div>
                        <p className="text-[10px] font-medium uppercase tracking-[0.22em] text-slate-500">
                            Finance
                        </p>
                        <Link
                            href="/"
                            className="text-lg font-semibold tracking-tight text-gray-50"
                        >
                            MarketPulse
                        </Link>
                    </div>
                </div>

                <nav
                    aria-label="Company page navigation"
                    className="hidden items-center gap-2 text-sm md:flex"
                >

                    <a
                        href="#overview"
                        className="rounded-full px-3 py-2 text-sm font-medium text-gray-50 transition hover:bg-slate-100 hover:text-black"
                    >
                        Overview
                    </a>

                    <a
                        href="#price-performance"
                        className="rounded-full px-3 py-2 text-sm font-medium text-gray-50 transition hover:bg-slate-100 hover:text-black"
                    >
                        Price performance
                    </a>

                    <a
                        href="#financials"
                        className="rounded-full px-3 py-2 text-sm font-medium text-gray-50 transition hover:bg-slate-100 hover:text-black"
                    >
                        Financials
                    </a>
                </nav>

                <div className="flex items-center gap-3">
                    <Link
                        href="/search"
                        className="hidden rounded-full border border-slate-300 bg-slate-100 px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-200 sm:inline-flex"
                    >
                        Search
                    </Link>

                    <button
                        type="button"
                        aria-label="Toggle menu"
                        aria-expanded={menuOpen}
                        onClick={() => setMenuOpen((value) => !value)}
                        className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-slate-700 bg-slate-900 text-slate-100 md:hidden"
                    >
                        <span className="sr-only">Open menu</span>
                        <div className="flex flex-col gap-1.5">
                            <span className="block h-0.5 w-5 rounded-full bg-current" />
                            <span className="block h-0.5 w-5 rounded-full bg-current" />
                            <span className="block h-0.5 w-5 rounded-full bg-current" />
                        </div>
                    </button>
                </div>
            </div>

            {menuOpen && (
                <nav
                    aria-label="Mobile navigation"
                    className="border-t border-slate-800 bg-slate-950 px-4 py-3 md:hidden"
                >
                    <div className="flex flex-col gap-2">
                        <Link
                            href="/"
                            onClick={() => setMenuOpen(false)}
                            className="rounded-xl px-3 py-2 text-sm font-medium text-gray-50 transition hover:bg-slate-800"
                        >
                            Search
                        </Link>

                        <a
                            href="#overview"
                            onClick={() => setMenuOpen(false)}
                            className="rounded-xl px-3 py-2 text-sm font-medium text-gray-50 transition hover:bg-slate-800"
                        >
                            Overview
                        </a>

                        <a
                            href="#price-performance"
                            onClick={() => setMenuOpen(false)}
                            className="rounded-xl px-3 py-2 text-sm font-medium text-gray-50 transition hover:bg-slate-800"
                        >
                            Price performance
                        </a>

                        <a
                            href="#financials"
                            onClick={() => setMenuOpen(false)}
                            className="rounded-xl px-3 py-2 text-sm font-medium text-gray-50 transition hover:bg-slate-800"
                        >
                            Financials
                        </a>
                    </div>
                </nav>
            )}
        </header>
    );
}

export default CompanyPageHeader;