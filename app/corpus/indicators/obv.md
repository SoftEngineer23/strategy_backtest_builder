# OBV

## Overview
On Balance Volume

## pandas-ta Usage
```python
result = df.ta.obv()
```

## Parameters
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.obv()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on OBV values

    return signals
```
