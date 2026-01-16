import { useState } from 'react';
import { StrategyInput } from './components/StrategyInput';
import { CodeDisplay } from './components/CodeDisplay';
import { BacktestConfig } from './components/BacktestConfig';
import { MetricsDisplay } from './components/MetricsDisplay';
import { EquityChart } from './components/EquityChart';
import { generateStrategy, runBacktest } from './services/api';
import type { BacktestMetrics, EquityPoint, BacktestConfig as Config } from './types';
import './App.css';

function App() {
  const [description, setDescription] = useState('');
  const [code, setCode] = useState<string | null>(null);
  const [metrics, setMetrics] = useState<BacktestMetrics | null>(null);
  const [equityCurve, setEquityCurve] = useState<EquityPoint[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [isGenerating, setIsGenerating] = useState(false);
  const [isBacktesting, setIsBacktesting] = useState(false);

  const handleGenerate = async (desc: string) => {
    setDescription(desc);
    setIsGenerating(true);
    setError(null);
    setMetrics(null);
    setEquityCurve(null);

    const result = await generateStrategy(desc);

    setIsGenerating(false);

    if (result.success && result.code) {
      setCode(result.code);
    } else {
      setError(result.error || 'Failed to generate strategy');
    }
  };

  const handleRegenerate = () => {
    if (description) {
      handleGenerate(description);
    }
  };

  const handleBacktest = async (config: Config) => {
    if (!code) return;

    setIsBacktesting(true);
    setError(null);

    const result = await runBacktest(code, config);

    setIsBacktesting(false);

    if (result.success) {
      setMetrics(result.metrics);
      setEquityCurve(result.equity_curve);
    } else {
      setError(result.error || 'Backtest failed');
    }
  };

  return (
    <div className="app">
      <header>
        <h1>Strategy Builder</h1>
        <p>Generate and backtest trading strategies with AI</p>
      </header>

      <main>
        <section className="input-section">
          <StrategyInput
            onGenerate={handleGenerate}
            isLoading={isGenerating}
          />
        </section>

        {code && (
          <section className="code-section">
            <CodeDisplay
              code={code}
              onRegenerate={handleRegenerate}
            />

            <BacktestConfig
              onRunBacktest={handleBacktest}
              isLoading={isBacktesting}
            />

            {error && (
              <div className="error-message">
                {error}
              </div>
            )}
          </section>
        )}

        {metrics && equityCurve && (
          <section className="results-section">
            <MetricsDisplay metrics={metrics} />
            <EquityChart data={equityCurve} />
          </section>
        )}
      </main>

      <footer>
        <p>For educational purposes only. Not financial advice. Past performance does not guarantee future results.</p>
        <p>Built with Claude API, React, pandas-ta, and RAG-enhanced code generation</p>
      </footer>
    </div>
  );
}

export default App;
