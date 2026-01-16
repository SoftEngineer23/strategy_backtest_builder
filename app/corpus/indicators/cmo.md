# CMO

## Overview
Chande Momentum Oscillator

## pandas-ta Usage
```python
result = df.ta.cmo()
```

## Parameters
- length (default: None)
- scalar (default: None)
- talib (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.cmo()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on CMO values

    return signals
```
