# ALPHATREND

## Overview
Alpha Trend

## pandas-ta Usage
```python
result = df.ta.alphatrend()
```

## Parameters
- src (default: None)
- length (default: None)
- multiplier (default: None)
- threshold (default: None)
- lag (default: None)
- mamode (default: None)
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.alphatrend()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on ALPHATREND values

    return signals
```
