import { useState } from 'react';

interface Props {
  onGenerate: (description: string) => void;
  isLoading: boolean;
  useAgent: boolean;
  onToggleAgent: (value: boolean) => void;
}

export function StrategyInput({ onGenerate, isLoading, useAgent, onToggleAgent }: Props) {
  const [description, setDescription] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (description.trim()) {
      onGenerate(description.trim());
    }
  };

  const examples = [
    { label: "RSI Reversal", description: "Buy when RSI crosses below 30, sell when above 70" },
    { label: "EMA Crossover", description: "Go long when 10 EMA crosses above 50 EMA" },
    { label: "Bollinger Bounce", description: "Mean reversion using Bollinger Bands - buy at lower band, sell at upper" },
    { label: "MACD Crossover", description: "MACD crossover strategy - buy on bullish cross, sell on bearish" },
  ];

  return (
    <div className="strategy-input">
      <h2>Describe Your Strategy</h2>

      <form onSubmit={handleSubmit}>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Example: Go long when the 20-day EMA crosses above the 50-day EMA, exit when it crosses back below"
          rows={4}
          disabled={isLoading}
        />

        <div className="generation-options">
          <label className="toggle-label">
            <input
              type="checkbox"
              checked={useAgent}
              onChange={(e) => onToggleAgent(e.target.checked)}
              disabled={isLoading}
            />
            <span className="toggle-switch"></span>
            <span className="toggle-text">
              Agentic Mode
              <span className="toggle-hint">
                {useAgent ? '(multi-step with self-critique)' : '(single-shot)'}
              </span>
            </span>
          </label>
        </div>

        <button type="submit" disabled={isLoading || !description.trim()}>
          {isLoading ? (useAgent ? 'Generating (this may take a minute)...' : 'Generating...') : 'Generate Strategy'}
        </button>
      </form>

      <div className="examples">
        <span>Try:</span>
        {examples.map((ex, i) => (
          <button
            key={i}
            className="example-btn"
            onClick={() => setDescription(ex.description)}
            disabled={isLoading}
          >
            {ex.label}
          </button>
        ))}
      </div>
    </div>
  );
}
