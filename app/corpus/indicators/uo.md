# UO

## Overview
Ultimate Oscillator

## pandas-ta Usage
```python
result = df.ta.uo()
```

## Parameters
- fast (default: None)
- medium (default: None)
- slow (default: None)
- fast_w (default: None)
- medium_w (default: None)
- slow_w (default: None)
- talib (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.uo()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on UO values

    return signals
```
