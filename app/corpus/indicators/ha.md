# HA

## Overview
Heikin Ashi Candles

## pandas-ta Usage
```python
result = df.ta.ha()
```

## Parameters
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.ha()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on HA values

    return signals
```
