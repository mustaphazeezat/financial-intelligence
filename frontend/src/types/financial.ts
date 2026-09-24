export type IncomeStatement = {
    fiscal_date_ending: string;
    report_type: string;
    reported_currency: string;
    revenue: number;
    gross_profit: number;
    operating_income: number;
    operating_expenses: number;
    net_income: number;
    ebit: number;
    ebitda: number;
    research_and_development: number;
    sga_expense: number;
    income_before_tax: number;
    income_tax_expense: number;
    interest_expense: number;
    depreciation_amortization: number;
};

export type IncomeStatementList = {
    income_statements: IncomeStatement[];
};
export type Profitability  = {
    gross_margin?: number | null;
    operating_margin?: number | null;
    net_margin?: number | null;
}
export type Health ={
    cash?: number | null;
    debt?: number | null;
    equity?: number | null;
    debt_to_equity?: number | null;
}
export type CashFlow ={
    capital_expenditure?: number | null;
    free_cash_flow?: number | null;
    operating_cash_flow?: number | null;
}

export type FinancialHealth = {
    profitability: Profitability;
    financial_health: Health; 
    cash_flow: CashFlow;
};