"""Performance metrics for backtesting."""

import pandas as pd
import numpy as np


def calculate_metrics(df, signals):
  """
  Calculate performance metrics from signals.

  Args:
      df: OHLCV DataFrame
      signals: Series of 1 (long), -1 (short), 0 (flat)

  Returns:
      dict of performance metrics
  """
  # Calculate daily returns
  df = df.copy()
  df['returns'] = df['Close'].pct_change()

  # Strategy returns = signal * next day's return (we enter at close, see result next day)
  df['signal'] = signals.shift(1)  # Shift to avoid look-ahead bias
  df['strategy_returns'] = df['signal'] * df['returns']

  # Drop NaN rows
  df = df.dropna()

  if len(df) == 0:
      return _empty_metrics()

  # Calculate metrics
  strategy_returns = df['strategy_returns']

  # Total return
  total_return = (1 + strategy_returns).prod() - 1

  # CAGR (annualized return)
  years = len(df) / 252
  if years > 0 and total_return > -1:
      cagr = (1 + total_return) ** (1 / years) - 1
  else:
      cagr = 0

  # Sharpe ratio (annualized)
  if strategy_returns.std() > 0:
      sharpe = (strategy_returns.mean() / strategy_returns.std()) * np.sqrt(252)
  else:
      sharpe = 0

  # Max drawdown
  cumulative = (1 + strategy_returns).cumprod()
  rolling_max = cumulative.expanding().max()
  drawdowns = cumulative / rolling_max - 1
  max_drawdown = drawdowns.min()

  # Win rate
  trades = df[df['signal'] != 0]['strategy_returns']
  if len(trades) > 0:
      win_rate = (trades > 0).sum() / len(trades)
  else:
      win_rate = 0

  # Number of trades (signal changes)
  signal_changes = (df['signal'].diff() != 0).sum()
  num_trades = int(signal_changes)

  # Average trade return
  if len(trades) > 0:
      avg_trade_return = trades.mean()
  else:
      avg_trade_return = 0

  # Profit factor
  gross_profits = trades[trades > 0].sum()
  gross_losses = abs(trades[trades < 0].sum())
  if gross_losses > 0:
      profit_factor = gross_profits / gross_losses
  else:
      profit_factor = float('inf') if gross_profits > 0 else 0

  return {
      'total_return': round(total_return * 100, 2),
      'cagr': round(cagr * 100, 2),
      'sharpe_ratio': round(sharpe, 2),
      'max_drawdown': round(max_drawdown * 100, 2),
      'win_rate': round(win_rate * 100, 2),
      'num_trades': num_trades,
      'avg_trade_return': round(avg_trade_return * 100, 4),
      'profit_factor': round(profit_factor, 2) if profit_factor != float('inf') else 'inf'
  }


def calculate_equity_curve(df, signals):
  """
  Calculate equity curve for visualization.

  Returns list of {date, value} points.
  """
  df = df.copy()
  df['returns'] = df['Close'].pct_change()
  df['signal'] = signals.shift(1)
  df['strategy_returns'] = df['signal'] * df['returns']
  df = df.dropna()

  cumulative = (1 + df['strategy_returns']).cumprod()

  equity_curve = []
  for date, value in cumulative.items():
      equity_curve.append({
          'date': date.strftime('%Y-%m-%d'),
          'value': round(value, 4)
      })

  return equity_curve


def _empty_metrics():
  """Return empty metrics when calculation fails."""
  return {
      'total_return': 0,
      'cagr': 0,
      'sharpe_ratio': 0,
      'max_drawdown': 0,
      'win_rate': 0,
      'num_trades': 0,
      'avg_trade_return': 0,
      'profit_factor': 0
  }