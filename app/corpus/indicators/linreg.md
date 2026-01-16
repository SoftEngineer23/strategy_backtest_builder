# LINREG

## Overview
Linear Regression Moving Average

## pandas-ta Usage
```python
result = df.ta.linreg()
```

## Parameters
- length (default: None)
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.linreg()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on LINREG values

    return signals
```
