export interface Price {
    date: string
    open: number;
    high: number;
    low: number;
    close: number;
    volume: number;
    change: number;
    change_percent: number;
    vwap: number;
}

export interface PerformancePeriods {
  "1d": number | null;
  "1m": number | null;
  "3m": number | null;
  "6m": number | null;
  "1y": number | null;
}

export interface TradingActivity {
  volume: number | null;
  vwap: number | null;
}

export interface CompanyPerformance {
  symbol: string;
  performance: PerformancePeriods;
  trading_activity: TradingActivity;
}
