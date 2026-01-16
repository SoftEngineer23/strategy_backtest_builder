# DEMA

## Overview
Double Exponential Moving Average

## pandas-ta Usage
```python
result = df.ta.dema()
```

## Parameters
- length (default: None)
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.dema()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on DEMA values

    return signals
```
