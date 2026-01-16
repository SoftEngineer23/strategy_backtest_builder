# MACD

## Overview
Moving Average Convergence Divergence - trend-following momentum indicator.

## pandas-ta Usage
```python
macd_df = df.ta.macd(fast=12, slow=26, signal=9)
```

## Return Value
Returns a **DataFrame** with the following columns:
- `MACD_12_26_9` - MACD Line (fast EMA - slow EMA)
- `MACDh_12_26_9` - MACD Histogram (MACD Line - Signal Line)
- `MACDs_12_26_9` - Signal Line (EMA of MACD Line)

Note: Column names include the fast, slow, and signal parameters.

## Parameters
- fast: Fast EMA period (default: 12)
- slow: Slow EMA period (default: 26)
- signal: Signal line EMA period (default: 9)
- offset: Offset the result (default: 0)

## Example Strategy
```python
def strategy(df):
    # Get MACD - returns a DataFrame
    macd_df = df.ta.macd(fast=12, slow=26, signal=9)

    # Extract individual components and fill NaN values
    macd_line = macd_df['MACD_12_26_9'].fillna(0)
    signal_line = macd_df['MACDs_12_26_9'].fillna(0)
    histogram = macd_df['MACDh_12_26_9'].fillna(0)

    signals = pd.Series(0, index=df.index)

    # Buy when MACD crosses above signal line (bullish crossover)
    signals[(macd_line > signal_line) & (macd_line.shift(1) <= signal_line.shift(1))] = 1

    # Sell when MACD crosses below signal line (bearish crossover)
    signals[(macd_line < signal_line) & (macd_line.shift(1) >= signal_line.shift(1))] = -1

    return signals
```
