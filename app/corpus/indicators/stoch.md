# STOCH

## Overview
Stochastic

## pandas-ta Usage
```python
result = df.ta.stoch()
```

## Parameters
- k (default: None)
- d (default: None)
- smooth_k (default: None)
- mamode (default: None)
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.stoch()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on STOCH values

    return signals
```
