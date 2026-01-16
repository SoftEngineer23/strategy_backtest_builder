# TSI

## Overview
True Strength Index

## pandas-ta Usage
```python
result = df.ta.tsi()
```

## Parameters
- fast (default: None)
- slow (default: None)
- signal (default: None)
- scalar (default: None)
- mamode (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.tsi()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on TSI values

    return signals
```
