import type { BacktestMetrics } from '../types';

interface Props {
	metrics: BacktestMetrics;
}

export function MetricsDisplay({ metrics }: Props) {
	const formatValue = (key: string, value: number | string): string => {
		if (value === 'inf') return 'Inf';

		const num = value as number;

		switch (key) {
			case 'total_return':
			case 'cagr':
			case 'max_drawdown':
			case 'win_rate':
			case 'avg_trade_return':
				return `${num >= 0 ? '+' : ''}${num.toFixed(2)}%`;
			case 'sharpe_ratio':
			case 'profit_factor':
				return num.toFixed(2);
			case 'num_trades':
				return num.toString();
			default:
				return String(value);
		}
	};

	const getColor = (key: string, value: number | string): string => {
		if (value === 'inf') return 'var(--color-positive)';

		const num = value as number;

		switch (key) {
			case 'total_return':
			case 'cagr':
			case 'avg_trade_return':
				return num >= 0 ? 'var(--color-positive)' : 'var(--color-negative)';
			case 'max_drawdown':
				return num > -10 ? 'var(--color-positive)' :
							 num > -25 ? 'var(--color-neutral)' : 'var(--color-negative)';
			case 'sharpe_ratio':
				return num > 1 ? 'var(--color-positive)' :
							 num > 0 ? 'var(--color-neutral)' : 'var(--color-negative)';
			case 'win_rate':
				return num > 50 ? 'var(--color-positive)' : 'var(--color-neutral)';
			default:
				return 'inherit';
		}
	};

	const metricLabels: Record<string, string> = {
		total_return: 'Total Return',
		cagr: 'CAGR',
		sharpe_ratio: 'Sharpe Ratio',
		max_drawdown: 'Max Drawdown',
		win_rate: 'Win Rate',
		num_trades: 'Total Trades',
		avg_trade_return: 'Avg Trade',
		profit_factor: 'Profit Factor',
	};

	return (
		<div className="metrics-display">
			<h3>Performance Metrics</h3>

			<div className="metrics-grid">
				{Object.entries(metrics).map(([key, value]) => (
					<div key={key} className="metric-card">
						<span className="metric-label">{metricLabels[key] || key}</span>
						<span
							className="metric-value"
							style={{ color: getColor(key, value) }}
						>
							{formatValue(key, value)}
						</span>
					</div>
				))}
			</div>
		</div>
	);
}