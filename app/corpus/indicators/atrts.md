# ATRTS

## Overview
ATR Trailing Stop

## pandas-ta Usage
```python
result = df.ta.atrts()
```

## Parameters
- length (default: None)
- ma_length (default: None)
- k (default: None)
- mamode (default: None)
- talib (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.atrts()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on ATRTS values

    return signals
```
