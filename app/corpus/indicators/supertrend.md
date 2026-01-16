# SUPERTREND

## Overview
Supertrend

## pandas-ta Usage
```python
result = df.ta.supertrend()
```

## Parameters
- length (default: None)
- atr_length (default: None)
- multiplier (default: None)
- atr_mamode (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.supertrend()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on SUPERTREND values

    return signals
```
