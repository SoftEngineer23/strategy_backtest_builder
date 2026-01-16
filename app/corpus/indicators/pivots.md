# PIVOTS

## Overview
Pivot Points

## pandas-ta Usage
```python
result = df.ta.pivots()
```

## Parameters
- method (default: None)
- anchor (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.pivots()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on PIVOTS values

    return signals
```
