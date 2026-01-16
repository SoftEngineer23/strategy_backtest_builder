# EMA

## Overview
Exponential Moving Average

## pandas-ta Usage
```python
result = df.ta.ema()
```

## Parameters
- length (default: None)
- talib (default: None)
- presma (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.ema()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on EMA values

    return signals
```
