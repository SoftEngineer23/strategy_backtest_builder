# PVT

## Overview
Price-Volume Trend

## pandas-ta Usage
```python
result = df.ta.pvt()
```

## Parameters
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.pvt()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on PVT values

    return signals
```
