# RSI

## Overview
Relative Strength Index

## pandas-ta Usage
```python
result = df.ta.rsi()
```

## Parameters
- length (default: None)
- scalar (default: None)
- mamode (default: None)
- talib (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.rsi()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on RSI values

    return signals
```
