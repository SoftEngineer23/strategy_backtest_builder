# TEMA

## Overview
Triple Exponential Moving Average

## pandas-ta Usage
```python
result = df.ta.tema()
```

## Parameters
- length (default: None)
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.tema()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on TEMA values

    return signals
```
