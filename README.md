# Financial Intelligence Platform [Live Demo](https://financial-intelligence-three.vercel.app) [Backend docs](https://financial-intelligence-5g87.onrender.com/docs)

A full-stack financial data platform for exploring companies, stock prices, market movers, financial statements, and financial performance.

## Overview

Financial Intelligence Platform is a web application that aggregates financial market data from external providers, processes and stores the data, and presents it through an interactive dashboard.

The platform combines a **Next.js frontend**, **FastAPI backend**, **PostgreSQL database**, and **Redis caching layer** to provide a responsive experience for exploring financial data.

## Features

- **Company Search** — Search and explore available publicly traded companies.
- **Company Profiles** — View company information, industry, sector, description, and other metadata.
- **Stock Prices** — View historical and current stock price information.
- **Market Movers** — Explore daily gainers, losers, and most-active stocks.
- **Financial Statements** — Access income statements, balance sheets, and cash flow data.
- **Financial Performance** — Compare quarterly and annual financial performance.
- **Financial Health** — View profitability, cash, debt, equity, and other financial metrics.
- **Trading Activity** — View trading volume, VWAP, and price performance.
- **Data Caching** — Redis is used to cache frequently accessed market and price data.

## Data Pipeline

The application includes an ETL/data ingestion layer for collecting and processing financial data from external APIs.

```text
Financial Data Providers
          ↓
       Extract
          ↓
      Transform
          ↓
       Validate
          ↓
      PostgreSQL
          ↓
        FastAPI
          ↓
       Next.js
          ↓
     Web Dashboard
```

Redis is used as a caching layer for frequently accessed data to reduce unnecessary external API requests and improve response times.

### Data Ingestion

The ingestion services handle:

- Company information
- Historical stock prices
- Market movers
- Income statements
- Balance sheets
- Cash flow statements

Financial data is transformed into application-specific structures before being persisted in PostgreSQL.

## Architecture

```text
┌──────────────────────┐
│       Next.js        │
│    React / TypeScript│
│        Vercel        │
└──────────┬───────────┘
           │ REST API
           ▼
┌──────────────────────┐
│       FastAPI        │
│        Python        │
│        Render        │
└───────┬────────┬─────┘
        │        │
        ▼        ▼
┌────────────┐ ┌────────────┐
│ PostgreSQL │ │   Redis    │
│  Supabase  │ │   Cache    │
└────────────┘ └────────────┘
```

## Technology Stack

### Frontend

- TypeScript
- Next.js
- React
- Tailwind CSS
- Data visualization

### Backend

- Python
- FastAPI
- SQLAlchemy
- REST APIs

### Data & Infrastructure

- PostgreSQL
- Redis
- Supabase
- Vercel
- Render

### External Data Providers

The application integrates with financial market data providers to retrieve company, market, stock price, and financial statement data.

## Database

PostgreSQL is used as the primary persistent data store.

Key data entities include:

- Companies
- Industries
- Sectors
- Stock prices
- Market movers
- Income statements
- Balance sheets
- Cash flows

Historical stock prices and financial information are persisted in the database so that the application does not need to retrieve all historical data from external providers for every request.

## API

The FastAPI backend exposes REST endpoints for the frontend.

Examples include:

```text
GET /api/v1/companies
GET /api/v1/companies/{symbol}
GET /api/v1/companies/{symbol}/price_performance
GET /api/v1/market_movers/
GET /api/v1/financial_statements/...
```

The API handles data retrieval, database queries, financial data processing, and communication with external providers.

## Deployment

The application is deployed using:

| Component | Platform |
|---|---|
| Frontend | Vercel |
| Backend | Render |
| PostgreSQL | Supabase |
| Redis | Hosted Redis |

The frontend communicates with the production FastAPI backend through REST APIs, while the backend connects to PostgreSQL and Redis.

Production configuration includes environment-based API URLs, database credentials, provider API keys, Redis credentials, and CORS configuration.

## Getting Started

### Prerequisites

- Node.js
- Python
- PostgreSQL
- Redis
- Financial data API credentials

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/financial-intelligence.git
cd financial-intelligence
```

### Backend

```bash
cd backend

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
DATABASE_URL=your_database_url
REDIS_URL=your_redis_url

FMP_API_KEY=your_fmp_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
MASSIVE_API_KEY=your_massive_api_key

FRONTEND_URL=http://localhost:3000
```

Start the API:

```bash
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend

npm install
```

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:3000
```

## Project Structure

```text
financial-intelligence/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── db/
│   │   ├── services/
│   │   ├── models/
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── package.json
│
└── README.md
```

## Project Goals

The project was built to explore the design and implementation of a production-style financial data platform, combining:

- Full-stack web development
- Data ingestion and ETL
- REST API development
- Relational database design
- Financial data processing
- Data visualization
- Caching
- Cloud deployment

## Status

The application is currently deployed and operational.

Future improvements may include additional financial metrics, enhanced data visualizations, portfolio functionality, and AI-assisted financial analysis.
