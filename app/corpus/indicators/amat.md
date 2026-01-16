# AMAT

## Overview
Archer Moving Averages Trends

## pandas-ta Usage
```python
result = df.ta.amat()
```

## Parameters
- fast (default: None)
- slow (default: None)
- lookback (default: None)
- mamode (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.amat()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on AMAT values

    return signals
```
