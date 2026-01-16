# NATR

## Overview
Normalized Average True Range

## pandas-ta Usage
```python
result = df.ta.natr()
```

## Parameters
- length (default: None)
- scalar (default: None)
- mamode (default: None)
- talib (default: None)
- prenan (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.natr()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on NATR values

    return signals
```
