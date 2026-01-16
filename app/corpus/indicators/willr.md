# WILLR

## Overview
William's Percent R

## pandas-ta Usage
```python
result = df.ta.willr()
```

## Parameters
- length (default: None)
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.willr()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on WILLR values

    return signals
```
