import { useState } from 'react';
import { StrategyInput } from './components/StrategyInput';
import { CodeDisplay } from './components/CodeDisplay';
import { BacktestConfig } from './components/BacktestConfig';
import { MetricsDisplay } from './components/MetricsDisplay';
import { EquityChart } from './components/EquityChart';
import { generateStrategy, runBacktest } from './services/api';
import type { BacktestMetrics, EquityPoint, BacktestConfig as Config, StrategyDetails } from './types';
import './App.css';

function App() {
  const [description, setDescription] = useState('');
  const [code, setCode] = useState<string | null>(null);
  const [strategyDetails, setStrategyDetails] = useState<StrategyDetails | null>(null);
  const [metrics, setMetrics] = useState<BacktestMetrics | null>(null);
  const [equityCurve, setEquityCurve] = useState<EquityPoint[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [isGenerating, setIsGenerating] = useState(false);
  const [isBacktesting, setIsBacktesting] = useState(false);
  const [useAgent, setUseAgent] = useState(true);

  const handleGenerate = async (desc: string) => {
    setDescription(desc);
    setIsGenerating(true);
    setError(null);
    setMetrics(null);
    setEquityCurve(null);
    setStrategyDetails(null);

    const result = await generateStrategy(desc, { useAgent });

    setIsGenerating(false);

    if (result.success && result.code) {
      setCode(result.code);
      if (result.strategy) {
        setStrategyDetails(result.strategy);
      }
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
            useAgent={useAgent}
            onToggleAgent={setUseAgent}
          />
        </section>

        {strategyDetails && (
          <section className="strategy-details">
            <h2>{strategyDetails.name}</h2>
            <p className="strategy-description">{strategyDetails.description}</p>
            <span className="strategy-type-badge">{strategyDetails.strategy_type}</span>

            <div className="rules-grid">
              <div className="rules-section">
                <h3>Entry Rules</h3>
                <ul>
                  {strategyDetails.entry_rules.map((rule, i) => (
                    <li key={i}>{rule}</li>
                  ))}
                </ul>
              </div>

              <div className="rules-section">
                <h3>Exit Rules</h3>
                <ul>
                  {strategyDetails.exit_rules.map((rule, i) => (
                    <li key={i}>{rule}</li>
                  ))}
                </ul>
              </div>

              <div className="rules-section">
                <h3>Risk Management</h3>
                <ul>
                  {strategyDetails.risk_management.map((rule, i) => (
                    <li key={i}>{rule}</li>
                  ))}
                </ul>
              </div>
            </div>
          </section>
        )}

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
      </footer>
    </div>
  );
}

export default App;
