import CompanyHeader from "@/components/company/companyHeader";
import FinancialSection from "@/components/company/financialSection";
import FinancialSectionSkeleton from "@/components/company/financialSectionSkeleton";
import PricePerform from "@/components/company/priceHistory";
import PricePerformance from "@/components/company/pricePerformance";
import SectionWrapper from "@/components/sectionWrapper";

import { getCompanyBySymbol } from "@/lib/api/companies";
import { getPricePerformance, getStockPrice } from "@/lib/api/price";

import { notFound } from "next/navigation";
import { Suspense } from "react";


export default async function Company({
  params,
  searchParams,
}: {
  params: Promise<{ symbol: string }>;
  searchParams: Promise<{ period?: string }>;
}) {
  const { symbol } = await params;
  const { period = "quarter" } = await searchParams;

  const selectedPeriod = period === "annual" ? "annual" : "quarter";

  const [company, priceList, pricePerformance] = await Promise.all([
    getCompanyBySymbol(symbol),
    getStockPrice(symbol),
    getPricePerformance(symbol),
  ]);

  if (!company) {
    notFound();
  }

  return (
    <div className="space-y-8">
      <section id="overview">
        <SectionWrapper>
          <CompanyHeader company={company} />
        </SectionWrapper>
      </section>

      <section id="price-performance">
        <SectionWrapper className="py-10">
          <h2 className="mb-4 text-2xl font-semibold text-white">
            Price Performance
          </h2>

          <div className="flex flex-col gap-6 lg:flex-row">
            {priceList.length > 0 && (
              <>
                <div
                  id="performance"
                  className="w-full shrink-0 lg:w-80"
                >
                  <PricePerformance data={pricePerformance} />
                </div>

                <div className="min-w-0 flex-1">
                  <PricePerform priceList={priceList} />
                </div>
              </>
            )}
          </div>
        </SectionWrapper>
      </section>

      <section id="financials">
        <SectionWrapper>
          <Suspense fallback={<FinancialSectionSkeleton />}>
            <FinancialSection
              symbol={symbol}
              period={selectedPeriod}
            />
          </Suspense>
        </SectionWrapper>
      </section>
    </div>
  );
}