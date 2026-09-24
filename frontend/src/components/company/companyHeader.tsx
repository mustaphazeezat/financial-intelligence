import { Company } from "@/types/company";

type CompanyHeaderProps = {
    company: Company;
};

function CompanyHeader({ company }: CompanyHeaderProps) {
    return (
        <header className="rounded-xl border border-gray-800 bg-gray-900 p-6">
            <div className="flex flex-col gap-5 sm:flex-row sm:items-start sm:justify-between">
                <div>
                    <div className="mb-2 flex items-center gap-3">
                        <h1 className="text-2xl font-bold text-white sm:text-3xl">
                            {company.company_name}
                        </h1>

                        <span className="rounded-md bg-gray-800 px-2 py-1 text-sm font-semibold text-gray-300">
                            {company.symbol.toUpperCase()}
                        </span>
                    </div>

                    <div className="flex flex-wrap gap-x-4 gap-y-2 text-sm text-gray-400">
                        {company.exchange && <span>{company.exchange}</span>}
                        {company.country && <span>{company.country.toUpperCase()}</span>}
                        {company.sector_name && <span>{company.sector_name}</span>}
                        {company.industry_name && <span>{company.industry_name}</span>}
                    </div>
                </div>

                {company.website && (
                    <a
                        href={company.website}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="w-fit rounded-lg border border-gray-700 px-4 py-2 text-sm font-medium text-gray-300 transition hover:border-white hover:text-white"
                    >
                        Visit website
                    </a>
                )}
            </div>

            {company.description && (
                <p className="mt-6 max-w-4xl text-sm leading-6 text-gray-400">
                    {company.description}
                </p>
            )}
        </header>
    );
}

export default CompanyHeader;