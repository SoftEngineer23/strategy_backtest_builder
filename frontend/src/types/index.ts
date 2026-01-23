export interface StrategyDetails {
  name: string;
  description: string;
  strategy_type: string;
  entry_rules: string[];
  exit_rules: string[];
  risk_management: string[];
}

export interface GenerateResponse {
  success: boolean;
  code: string | null;
  error: string | null;
  strategy?: StrategyDetails;
  request_id?: string;
  warnings?: string[];
}

export interface BacktestMetrics {
  total_return: number;
  cagr: number;
  sharpe_ratio: number;
  max_drawdown: number;
  win_rate: number;
  num_trades: number;
  avg_trade_return: number;
  profit_factor: number | string;
}

export interface EquityPoint {
  date: string;
  value: number;
}

export interface BacktestResponse {
  success: boolean;
  metrics: BacktestMetrics | null;
  equity_curve: EquityPoint[] | null;
  error: string | null;
  data_points?: number;
  date_range?: {
    start: string;
    end: string;
  };
}

export interface BacktestConfig {
  ticker: string;
  start: string;
  end: string;
}
