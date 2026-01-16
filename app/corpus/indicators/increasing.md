# INCREASING

## Overview
Increasing

## pandas-ta Usage
```python
result = df.ta.increasing()
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
    indicator = df.ta.increasing()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on INCREASING values

    return signals
```
