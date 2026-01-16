# VWAP

## Overview
Volume Weighted Average Price

## pandas-ta Usage
```python
result = df.ta.vwap()
```

## Parameters
- anchor (default: None)
- bands (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.vwap()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on VWAP values

    return signals
```
