# ATR

## Overview
Average True Range

## pandas-ta Usage
```python
result = df.ta.atr()
```

## Parameters
- length (default: None)
- mamode (default: None)
- talib (default: None)
- prenan (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.atr()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on ATR values

    return signals
```
