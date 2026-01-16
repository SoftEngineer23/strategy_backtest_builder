# PDIST

## Overview
Price Distance

## pandas-ta Usage
```python
result = df.ta.pdist()
```

## Parameters
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.pdist()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on PDIST values

    return signals
```
