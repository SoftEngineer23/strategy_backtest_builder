# DM

## Overview
Directional Movement

## pandas-ta Usage
```python
result = df.ta.dm()
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
    indicator = df.ta.dm()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on DM values

    return signals
```
