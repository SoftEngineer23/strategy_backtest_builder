import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    ReferenceLine,
  } from 'recharts';
import type { EquityPoint } from '../types';

interface Props {
	data: EquityPoint[];
}

export function EquityChart({ data }: Props) {
	const chartData = data.map((point) => ({
		...point,
		return: ((point.value - 1) * 100).toFixed(2),
	}));

	return (
		<div className="equity-chart">
			<h3>Equity Curve</h3>

			<ResponsiveContainer width="100%" height={400}>
				<LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
					<CartesianGrid strokeDasharray="3 3" stroke="#333" />

					<XAxis
						dataKey="date"
						tick={{ fill: '#888', fontSize: 12 }}
						tickFormatter={(date) => {
							const d = new Date(date);
							return `${d.getMonth() + 1}/${d.getFullYear().toString().slice(2)}`;
						}}
						interval="preserveStartEnd"
					/>

					<YAxis
						tick={{ fill: '#888', fontSize: 12 }}
						tickFormatter={(val) => `${val}%`}
						domain={['auto', 'auto']}
					/>

					<Tooltip
						contentStyle={{
							backgroundColor: '#1a1a1a',
							border: '1px solid #333',
							borderRadius: '8px',
						}}
						labelStyle={{ color: '#888' }}
						formatter={(value: number) => [`${value}%`, 'Return']}
						labelFormatter={(date) => new Date(date).toLocaleDateString()}
					/>

					<ReferenceLine y={0} stroke="#555" strokeDasharray="3 3" />

					<Line
						type="monotone"
						dataKey="return"
						stroke="#4a9eff"
						strokeWidth={2}
						dot={false}
						activeDot={{ r: 4, fill: '#4a9eff' }}
					/>
				</LineChart>
			</ResponsiveContainer>
		</div>
	);
}