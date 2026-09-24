CREATE TABLE sectors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE industries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) UNIQUE NOT NULL,
    sector_id INTEGER NOT NULL REFERENCES sectors(id)
);

CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) UNIQUE NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    exchange VARCHAR(50),
    industry_id INTEGER REFERENCES industries(id),
    country VARCHAR(100),
    website TEXT,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE stock_prices (
    id BIGSERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id),
    date DATE NOT NULL,
    open NUMERIC(12, 4),
    high NUMERIC(12, 4),
    low NUMERIC(12, 4),
    close NUMERIC(12, 4),
    volume BIGINT,
    change NUMERIC(12, 4),
    change_percent NUMERIC(12, 6),
    vwap NUMERIC(12, 4),
    source VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(company_id, date)
);



CREATE TABLE economic_indicators (
    id BIGSERIAL PRIMARY KEY,
    indicator VARCHAR(100) NOT NULL,
    value NUMERIC(18, 6),
    unit VARCHAR(50),
    source VARCHAR(50),
    date DATE NOT NULL,

    UNIQUE(indicator, date, source)
);

CREATE TABLE market_movers (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    category VARCHAR(20) NOT NULL,
    price NUMERIC,
    change_amount NUMERIC,
    change_percentage NUMERIC,
    volume BIGINT,
    snapshot_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE income_statements (
    id BIGSERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id),

    fiscal_date_ending DATE NOT NULL,
    report_type VARCHAR(20) NOT NULL,
    reported_currency VARCHAR(10) NOT NULL,

    revenue NUMERIC,
    gross_profit NUMERIC,
    operating_income NUMERIC,
    operating_expenses NUMERIC,
    net_income NUMERIC,

    ebit NUMERIC,
    ebitda NUMERIC,

    research_and_development NUMERIC,
    sga_expense NUMERIC,

    income_before_tax NUMERIC,
    income_tax_expense NUMERIC,
    interest_expense NUMERIC,
    depreciation_amortization NUMERIC,

    source VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(company_id, fiscal_date_ending, report_type, source)
);

CREATE TABLE balance_sheets (
    id BIGSERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id),

    fiscal_date_ending DATE NOT NULL,
    report_type VARCHAR(20) NOT NULL,
    reported_currency VARCHAR(10) NOT NULL,

    total_assets NUMERIC,
    total_current_assets NUMERIC,
    cash_and_equivalents NUMERIC,
    cash_and_short_term_investments NUMERIC,
    inventory NUMERIC,
    current_receivables NUMERIC,

    property_plant_equipment NUMERIC,
    intangible_assets NUMERIC,
    goodwill NUMERIC,
    short_term_investments NUMERIC,

    total_liabilities NUMERIC,
    total_current_liabilities NUMERIC,
    short_term_debt NUMERIC,
    long_term_debt NUMERIC,
    total_debt NUMERIC,
    total_non_current_liabilities NUMERIC,

    total_shareholder_equity NUMERIC,
    retained_earnings NUMERIC,
    shares_outstanding NUMERIC,

    source VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(company_id, fiscal_date_ending, report_type, source)
);

CREATE TABLE cash_flow_statements (
    id BIGSERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id),

    fiscal_date_ending DATE NOT NULL,
    report_type VARCHAR(20) NOT NULL,
    reported_currency VARCHAR(10) NOT NULL,
    
    operating_cash_flow NUMERIC,
    capital_expenditures NUMERIC,
    investing_cash_flow NUMERIC,
    financing_cash_flow NUMERIC,

    dividend_payout NUMERIC,
    stock_based_compensation NUMERIC,
    net_income NUMERIC,

    source VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(company_id, fiscal_date_ending, report_type, source)
);
