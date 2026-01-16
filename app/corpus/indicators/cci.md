# CCI

## Overview
Commodity Channel Index

## pandas-ta Usage
```python
result = df.ta.cci()
```

## Parameters
- length (default: None)
- c (default: None)
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.cci()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on CCI values

    return signals
```
