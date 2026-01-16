import { useState } from 'react';
import type { BacktestConfig as Config } from '../types';

interface Props {
	onRunBacktest: (config: Config) => void;
	isLoading: boolean;
}

export function BacktestConfig({ onRunBacktest, isLoading }: Props) {
	const [config, setConfig] = useState<Config>({
		ticker: 'SPY',
		start: '2020-01-01',
		end: new Date().toISOString().split('T')[0],
	});

	const handleSubmit = (e: React.FormEvent) => {
		e.preventDefault();
		onRunBacktest(config);
	};

	const presets = [
		{ label: '1Y', years: 1 },
		{ label: '3Y', years: 3 },
		{ label: '5Y', years: 5 },
	];

	const setPreset = (years: number) => {
		const end = new Date();
		const start = new Date();
		start.setFullYear(end.getFullYear() - years);

		setConfig({
			...config,
			start: start.toISOString().split('T')[0],
			end: end.toISOString().split('T')[0],
		});
	};

	return (
		<div className="backtest-config">
			<h3>Backtest Configuration</h3>

			<form onSubmit={handleSubmit}>
				<div className="form-row">
					<label>
						Ticker
						<input
							type="text"
							value={config.ticker}
							onChange={(e) => setConfig({ ...config, ticker: e.target.value.toUpperCase() })}
							maxLength={5}
						/>
					</label>
				</div>

				<div className="form-row dates">
					<label>
						Start Date
						<input
							type="date"
							value={config.start}
							onChange={(e) => setConfig({ ...config, start: e.target.value })}
						/>
					</label>

					<label>
						End Date
						<input
							type="date"
							value={config.end}
							onChange={(e) => setConfig({ ...config, end: e.target.value })}
						/>
					</label>
				</div>

				<div className="presets">
					{presets.map((p) => (
						<button
							key={p.label}
							type="button"
							onClick={() => setPreset(p.years)}
							className="preset-btn"
						>
							{p.label}
						</button>
					))}
				</div>

				<button type="submit" disabled={isLoading} className="run-btn">
					{isLoading ? 'Running Backtest...' : 'Run Backtest'}
				</button>
			</form>
		</div>
	);
}