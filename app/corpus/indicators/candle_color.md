# CANDLE_COLOR

## Overview
Candle Change

## pandas-ta Usage
```python
result = df.ta.candle_color()
```

## Parameters
- No configurable parameters

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.candle_color()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on CANDLE_COLOR values

    return signals
```
