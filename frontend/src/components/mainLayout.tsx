"use client";

import type { ReactNode } from "react";
import { usePathname } from "next/navigation";
import Header from "./header";
import CompanyPageHeader from "./company/companyPageHeader";


type MainLayoutProps = {
    children: ReactNode;
};

export default function MainLayout({ children }: MainLayoutProps) {
    const pathname = usePathname();
    const segments = pathname.split("/").filter(Boolean);

    const isCompanyPage =
        segments[0] === "companies" && segments.length === 2;

    const symbol = isCompanyPage
        ? decodeURIComponent(segments[1]).toUpperCase()
        : "";

    return (
        <div className="min-h-screen">
            {isCompanyPage ? (
                <CompanyPageHeader symbol={symbol} />
            ) : (
                <Header />
            )}

            <main className="min-h-screen px-4 py-8 sm:px-6 lg:px-8">
                {children}
            </main>

            <footer className="border-t border-slate-200">
                <div className="mx-auto max-w-7xl px-4 py-6 text-center text-sm text-slate-500 sm:px-6 lg:px-8">
                    © {new Date().getFullYear()} Finance
                </div>
            </footer>
        </div>
    );
}