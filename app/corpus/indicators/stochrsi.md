# STOCHRSI

## Overview
Stochastic RSI

## pandas-ta Usage
```python
result = df.ta.stochrsi()
```

## Parameters
- length (default: None)
- rsi_length (default: None)
- k (default: None)
- d (default: None)
- mamode (default: None)
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.stochrsi()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on STOCHRSI values

    return signals
```
