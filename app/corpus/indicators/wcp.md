# WCP

## Overview
Weighted Closing Price

## pandas-ta Usage
```python
result = df.ta.wcp()
```

## Parameters
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.wcp()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on WCP values

    return signals
```
