import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { vi, describe, it, expect, beforeEach } from "vitest";
import CompaniesTable from "@/components/company/companiesTable";
import { getCompanies } from "@/lib/api/companies";

vi.mock("next/link", () => ({
    default: ({
        href,
        children,
        ...props
    }: React.AnchorHTMLAttributes<HTMLAnchorElement> & {
        href: string;
        children: React.ReactNode;
    }) => (
        <a href={href} {...props}>
            {children}
        </a>
    ),
}));

vi.mock("@/lib/api/companies", () => ({
    getCompanies: vi.fn(),
}));

describe("CompaniesTable", () => {
    const companyData = {
        companies: [
            {
                id: 1,
                symbol: "AAPL",
                company_name: "Apple Inc.",
                exchange: "NASDAQ",
                sector_name: "Technology",
                industry_name: "Consumer Electronics",
                country: "USA",
                website: "",
                description: ""
            },
            {  id: 2,
                symbol: "MSFT",
                company_name: "Microsoft Corporation",
                exchange: "NASDAQ",
                sector_name: "Technology",
                industry_name: "Software - Infrastructure",
                country: "United States",
                website: "",
                description: ""
            },
        ],
        total: 2,
        current_page: 1,
        has_next_page: false,
    };

    const industryData = [
        {id: 1, sector_name: "Technology", industry_name: "Consumer Electronics" },
        {id: 2, sector_name: "Technology", industry_name: "Software - Infrastructure" },
    ];

    beforeEach(() => {
        vi.clearAllMocks();
    });

    it("calls getCompanies with the selected sector and current industry", async () => {
        vi.mocked(getCompanies).mockResolvedValue({
            companies: [companyData.companies[0]],
            total: 2,
            current_page: 1,
            has_next_page: false,
        });

        render(
            <CompaniesTable
                companyData={companyData}
                industryData={industryData}
            />
        );

        const selects = screen.getAllByRole("combobox");
        fireEvent.change(selects[1], { target: { value: "Technology" } });

        await waitFor(() => {
            expect(getCompanies).toHaveBeenCalledWith(
                undefined,
                0,
                10,
                "",
                "Technology"
            );
        });
    });

    it("calls getCompanies with the selected industry and current sector", async () => {
        vi.mocked(getCompanies).mockResolvedValue({
            companies: [companyData.companies[0]],
            total: 1,
            current_page: 1,
            has_next_page: false,
        });

        render(
            <CompaniesTable
                companyData={companyData}
                industryData={industryData}
            />
        );

        const selects = screen.getAllByRole("combobox");
        fireEvent.change(selects[2], {
            target: { value: "Consumer Electronics" },
        });

        await waitFor(() => {
            expect(getCompanies).toHaveBeenCalledWith(
                undefined,
                0,
                10,
                "Consumer Electronics",
                ""
            );
        });
    });
});