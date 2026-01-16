# AOBV

## Overview
Archer On Balance Volume

## pandas-ta Usage
```python
result = df.ta.aobv()
```

## Parameters
- fast (default: None)
- slow (default: None)
- max_lookback (default: None)
- min_lookback (default: None)
- mamode (default: None)
- run_length (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.aobv()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on AOBV values

    return signals
```
