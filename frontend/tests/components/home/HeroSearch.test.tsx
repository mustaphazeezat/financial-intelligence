import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

import HeroSearch from "@/components/home/HeroSearch";
import { getCompanies } from "@/lib/api/companies";
import { useRouter } from "next/navigation";
import type { Company, Companies } from "@/types/company";

vi.mock("@/lib/api/companies", () => ({
  getCompanies: vi.fn(),
}));

vi.mock("next/navigation", () => ({
  useRouter: vi.fn(),
}));

const mockGetCompanies = vi.mocked(getCompanies);
const mockPush = vi.fn();

const companies: Company[] = [
  {
    id: 1,
    symbol: "AAPL",
    company_name: "Apple Inc.",
    exchange: "NASDAQ",
    industry_name: "Technology",
    sector_name: "Technology",
    website: "https://www.apple.com",
    country: "United States",
    description:
      "Apple Inc. designs and manufactures consumer technology products.",
  },
  {
    id: 2,
    symbol: "AMZN",
    company_name: "Amazon.com Inc.",
    exchange: "NASDAQ",
    industry_name: "Internet Retail",
    sector_name: "Consumer Cyclical",
    website: "https://www.amazon.com",
    country: "United States",
    description:
      "Amazon.com Inc. operates an online marketplace and cloud services.",
  },
];

const mockCompaniesResponse: Companies = {
  companies,
  total: 2,
  current_page: 1,
  has_next_page: false,
};

describe("HeroSearch", () => {
  beforeEach(() => {
    vi.clearAllMocks();

    vi.mocked(useRouter).mockReturnValue({
        push: mockPush,
    } as unknown as ReturnType<typeof useRouter>);
  });

  it("renders the search input", () => {
    render(<HeroSearch />);

    expect(
      screen.getByPlaceholderText("Search companies, stocks or symbols")
    ).toBeInTheDocument();
  });

  it("does not search when the query has fewer than 2 characters", async () => {
    const user = userEvent.setup();

    render(<HeroSearch />);

    const input = screen.getByPlaceholderText(
      "Search companies, stocks or symbols"
    );

    await user.type(input, "A");

    await new Promise((resolve) => setTimeout(resolve, 350));

    expect(mockGetCompanies).not.toHaveBeenCalled();
  });

  it("searches for companies after typing at least 2 characters", async () => {
    const user = userEvent.setup();

    mockGetCompanies.mockResolvedValue(mockCompaniesResponse);

    render(<HeroSearch />);

    const input = screen.getByPlaceholderText(
      "Search companies, stocks or symbols"
    );

    await user.type(input, "App");

    await waitFor(
      () => {
        expect(mockGetCompanies).toHaveBeenCalledWith("app");
      },
      { timeout: 1000 }
    );
  });

  it("displays searching while the request is loading", async () => {
    const user = userEvent.setup();

    let resolveRequest!: (value: Companies) => void;

    mockGetCompanies.mockReturnValue(
      new Promise<Companies>((resolve) => {
        resolveRequest = resolve;
      })
    );

    render(<HeroSearch />);

    const input = screen.getByPlaceholderText(
      "Search companies, stocks or symbols"
    );

    await user.type(input, "App");

    expect(await screen.findByText("Searching...")).toBeInTheDocument();

    resolveRequest(mockCompaniesResponse);

    await waitFor(() => {
      expect(screen.queryByText("Searching...")).not.toBeInTheDocument();
    });
  });

  it("displays company search results", async () => {
  const user = userEvent.setup();

  mockGetCompanies.mockResolvedValue(mockCompaniesResponse);

  render(<HeroSearch />);

  const input = screen.getByPlaceholderText(
    "Search companies, stocks or symbols"
  );

  await user.type(input, "App");

  expect(await screen.findByText("Apple Inc.")).toBeInTheDocument();

  expect(screen.getByText("AAPL")).toBeInTheDocument();

  expect(screen.getAllByText("NASDAQ")).toHaveLength(2);
});

  it("displays no companies found when the search returns no results", async () => {
    const user = userEvent.setup();

    mockGetCompanies.mockResolvedValue({
      companies: [],
      total: 0,
      current_page: 1,
      has_next_page: false,
    });

    render(<HeroSearch />);

    const input = screen.getByPlaceholderText(
      "Search companies, stocks or symbols"
    );

    await user.type(input, "XYZ");

    expect(
      await screen.findByText("No companies found")
    ).toBeInTheDocument();
  });

  it("clears results when the query becomes shorter than 2 characters", async () => {
    const user = userEvent.setup();

    mockGetCompanies.mockResolvedValue(mockCompaniesResponse);

    render(<HeroSearch />);

    const input = screen.getByPlaceholderText(
      "Search companies, stocks or symbols"
    );

    await user.type(input, "App");

    expect(await screen.findByText("Apple Inc.")).toBeInTheDocument();

    await user.clear(input);
    await user.type(input, "A");

    expect(screen.queryByText("Apple Inc.")).not.toBeInTheDocument();
  });

  it("navigates to the selected company", async () => {
    const user = userEvent.setup();

    mockGetCompanies.mockResolvedValue(mockCompaniesResponse);

    render(<HeroSearch />);

    const input = screen.getByPlaceholderText(
      "Search companies, stocks or symbols"
    );

    await user.type(input, "App");

    const apple = await screen.findByRole("button", {
      name: /Apple Inc.*AAPL.*NASDAQ/i,
    });

    await user.click(apple);

    expect(mockPush).toHaveBeenCalledWith("/companies/AAPL");
  });

  it("clears the results when a company is selected", async () => {
    const user = userEvent.setup();

    mockGetCompanies.mockResolvedValue(mockCompaniesResponse);

    render(<HeroSearch />);

    const input = screen.getByPlaceholderText(
      "Search companies, stocks or symbols"
    );

    await user.type(input, "App");

    const apple = await screen.findByRole("button", {
      name: /Apple Inc.*AAPL.*NASDAQ/i,
    });

    await user.click(apple);

    expect(input).toHaveValue("");
    expect(screen.queryByText("Apple Inc.")).not.toBeInTheDocument();
  });

  it("handles API errors", async () => {
    const user = userEvent.setup();

    const consoleError = vi
      .spyOn(console, "error")
      .mockImplementation(() => {});

    mockGetCompanies.mockRejectedValue(new Error("API error"));

    render(<HeroSearch />);

    const input = screen.getByPlaceholderText(
      "Search companies, stocks or symbols"
    );

    await user.type(input, "App");

    await waitFor(
      () => {
        expect(consoleError).toHaveBeenCalledWith(
          "Company not found:",
          expect.any(Error)
        );
      },
      { timeout: 1000 }
    );

    expect(
      await screen.findByText("No companies found")
    ).toBeInTheDocument();

    consoleError.mockRestore();
  });
});