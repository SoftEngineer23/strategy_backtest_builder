# VP

## Overview
Volume Profile

## pandas-ta Usage
```python
result = df.ta.vp()
```

## Parameters
- width (default: None)
- sort (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.vp()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on VP values

    return signals
```
