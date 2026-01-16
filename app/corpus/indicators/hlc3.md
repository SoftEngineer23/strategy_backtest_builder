# HLC3

## Overview
HLC3

## pandas-ta Usage
```python
result = df.ta.hlc3()
```

## Parameters
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.hlc3()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on HLC3 values

    return signals
```
