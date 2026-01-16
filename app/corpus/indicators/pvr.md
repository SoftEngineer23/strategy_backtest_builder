# PVR

## Overview
Price Volume Rank

## pandas-ta Usage
```python
result = df.ta.pvr()
```

## Parameters
- drift (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.pvr()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on PVR values

    return signals
```
