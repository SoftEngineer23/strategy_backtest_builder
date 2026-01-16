# ZIGZAG

## Overview
Zigzag

## pandas-ta Usage
```python
result = df.ta.zigzag()
```

## Parameters
- legs (default: None)
- deviation (default: None)
- backtest (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.zigzag()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on ZIGZAG values

    return signals
```
