
import CompaniesTable from "@/components/company/companiesTable";
import SectionWrapper from "@/components/sectionWrapper";
import { getCompanies, getIndustries } from "@/lib/api/companies";

const LIMIT = 10;

export default async function Companies({
  searchParams,
}: {
  searchParams: Promise<{ page?: string }>;
})  {
    
   const { page = "1" } = await searchParams;
    const currentPage = Math.max(Number(page) || 1, 1);
    const skip = (currentPage - 1) * LIMIT;

    const companies = await getCompanies(undefined, skip, LIMIT);
    const industries = await getIndustries()
  

    return (
      <SectionWrapper>
        <div className="space-y-8">
            <div>
                <h1 className="text-2xl font-semibold text-white">
                    Companies
                </h1>
                <p className="mt-1 text-sm text-gray-400">
                    Browse all listed companies.
                </p>
            </div>

           <CompaniesTable companyData={companies} industryData={industries} />
        </div>
      </SectionWrapper>
    );
}