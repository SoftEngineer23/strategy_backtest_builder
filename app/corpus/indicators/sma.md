# SMA

## Overview
Simple Moving Average

## pandas-ta Usage
```python
result = df.ta.sma()
```

## Parameters
- length (default: None)
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.sma()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on SMA values

    return signals
```
