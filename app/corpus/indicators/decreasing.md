# DECREASING

## Overview
Decreasing

## pandas-ta Usage
```python
result = df.ta.decreasing()
```

## Parameters
- length (default: None)
- strict (default: None)
- asint (default: None)
- percent (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.decreasing()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on DECREASING values

    return signals
```
