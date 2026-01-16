# STDEV

## Overview
Rolling Standard Deviation

## pandas-ta Usage
```python
result = df.ta.stdev()
```

## Parameters
- length (default: None)
- ddof (default: None)
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.stdev()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on STDEV values

    return signals
```
