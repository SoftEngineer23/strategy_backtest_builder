# OHLC4

## Overview
OHLC4

## pandas-ta Usage
```python
result = df.ta.ohlc4()
```

## Parameters
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.ohlc4()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on OHLC4 values

    return signals
```
