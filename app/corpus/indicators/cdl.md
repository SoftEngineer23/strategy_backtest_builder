# CDL

## Overview
Candle Pattern

## pandas-ta Usage
```python
result = df.ta.cdl()
```

## Parameters
- name (default: all)
- scalar (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.cdl()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on CDL values

    return signals
```
