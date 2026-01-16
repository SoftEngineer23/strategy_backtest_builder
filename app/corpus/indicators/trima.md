# TRIMA

## Overview
Triangular Moving Average

## pandas-ta Usage
```python
result = df.ta.trima()
```

## Parameters
- length (default: None)
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.trima()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on TRIMA values

    return signals
```
