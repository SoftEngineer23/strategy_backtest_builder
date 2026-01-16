# RWI

## Overview
Random Walk Index

## pandas-ta Usage
```python
result = df.ta.rwi()
```

## Parameters
- length (default: None)
- mamode (default: None)
- talib (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.rwi()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on RWI values

    return signals
```
