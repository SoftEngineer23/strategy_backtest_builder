# PVOL

## Overview
Price-Volume

## pandas-ta Usage
```python
result = df.ta.pvol()
```

## Parameters
- signed (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.pvol()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on PVOL values

    return signals
```
