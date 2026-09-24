"use client";

import { getCompanies } from "@/lib/api/companies";
import { Company } from "@/types/company";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function HeroSearch() {
    const [query, setQuery] = useState("");
    const [companies, setCompanies] = useState<Company[]>([]);
    const [loading, setLoading] = useState(false);
    const router = useRouter();
    useEffect(()=>{
        if (query.trim().length < 2) {
          return;
        }
        const timeout = setTimeout(async () => {
      try {
        setLoading(true);
        const search = query.toLowerCase();
        const data = await getCompanies(search)
        
        setCompanies(data.companies.slice(0, 8));
      } catch (error) {
        console.error("Company not found:", error);
        setCompanies([]);
      } finally {
        setLoading(false);
      }
    }, 300);

    return () => clearTimeout(timeout);
    }, [query])
  
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);

    if (value.trim().length < 2) {
      setCompanies([]);
    }

  };
  const handleSelect  = (symbol: string) =>{
    setQuery("");
    setCompanies([]);
    router.push(`/companies/${symbol}`);
  }

  return (
    <section className="py-30">
      
        <div className="flex flex-col items-center justify-center">
          
          <h2 className="mt-5 mb-4 text-4xl text-center font-black tracking-tight text-white sm:text-5xl lg:text-6xl">
            Financial Intelligence
          </h2>
          <p className="mt-3 text-2xl text-center text-gray-300 font-medium">Understand markets. Discover opportunities.</p>

          <div className="relative">
              <label className="relative block mt-10 border-2 w-screen max-w-xl bg-white rounded-4xl overflow-hidden">
              <input
                    type="text"
                    value={query}
                    onChange={handleSearchChange}
                    placeholder="Search companies, stocks or symbols"
                    className="w-full bg-transparent text-2xl py-3 px-6 text-black placeholder:text-slate-500 focus:outline-none"
                  />

                <div
                  className="absolute flex items-center justify-center w-12.5 h-12.5 top-0.75 right-0 rounded-full bg-black text-white"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="h-5 w-5 text-slate-500">
                    <circle cx="11" cy="11" r="6" />
                    <path d="m16 16 5 5" />
                  </svg>
                </div>
              </label>
              {loading && query.trim().length >= 2 && (
                <div className="dropcontainer absolute z-10 mt-2 w-full px-5 py-4 text-sm text-gray-500">
                  Searching...
                </div>
              )}
              {!loading && query.trim().length >= 2 &&
                  companies.length === 0 && (
                <div className="dropcontainer absolute z-10 mt-2 w-full px-5 py-4 text-sm text-gray-500">
                  No companies found
                </div>
              )}
              {!loading && query.trim().length >= 2 && companies.length > 0 && (
    <div className="dropcontainer absolute z-10 mt-2 w-full overflow-hidden rounded-lg bg-gray-800 shadow-lg">
        {companies.map((company) => (
            <button
                key={company.symbol}
                type="button"
                onClick={() => handleSelect(company.symbol)}
                className="flex w-full items-center justify-between px-5 py-3 text-left hover:bg-gray-700"
            >
                <div>
                    <p className="font-medium text-gray-100">
                        {company.company_name}
                    </p>
                    <p className="text-sm text-gray-300">
                        {company.symbol}
                    </p>
                </div>

                <span className="text-sm text-gray-400">
                    {company.exchange}
                </span>
            </button>
        ))}
    </div>
)}
          </div>
        </div>
    </section>
  );
}
