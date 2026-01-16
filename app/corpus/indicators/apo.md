# APO

## Overview
Absolute Price Oscillator

## pandas-ta Usage
```python
result = df.ta.apo()
```

## Parameters
- fast (default: None)
- slow (default: None)
- mamode (default: None)
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.apo()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on APO values

    return signals
```
