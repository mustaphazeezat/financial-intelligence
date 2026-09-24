import Link from "next/link";

type CompanyPageHeaderProps = {
    symbol: string;
};

function CompanyPageHeader({ symbol }: CompanyPageHeaderProps) {
    return (
        <header className="sticky top-0 z-50 border-b border-slate-900 backdrop-blur-sm">
            <div className="mx-auto flex max-w-7xl items-center justify-between gap-6  px-4 py-3 sm:px-6 lg:px-8">
                <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-black text-white">
                        <span className="text-lg font-black italic">FIP</span>
                    </div>

                    <div>
                        <p className="text-[10px] font-medium uppercase tracking-[0.22em] text-slate-500">
                        Finance
                        </p>
                        <Link href="/" className="text-lg font-semibold tracking-tight text-gray-50">
                        MarketPulse
                        </Link>
                    </div>
                </div>

                <nav className="hidden items-center gap-6 text-sm md:flex">
                    <Link
                        href="/companies"
                        className="rounded-full px-3 py-2 text-sm font-medium text-gray-50 transition hover:bg-slate-100 hover:text-black"
                    >
                        Company List
                    </Link>

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
                    <a href="#financials"
                        className="rounded-full px-3 py-2 text-sm font-medium text-gray-50 transition hover:bg-slate-100 hover:text-black"
                    >
                        Financials
                    </a>
                </nav>

                <span className="rounded-md bg-gray-800 px-3 py-1.5 text-sm font-semibold text-gray-200">
                    {symbol}
                </span>
            </div>
        </header>
    );
}


export default CompanyPageHeader;