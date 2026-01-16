# CHANDELIER_EXIT

## Overview
Chandelier Exit

## pandas-ta Usage
```python
result = df.ta.chandelier_exit()
```

## Parameters
- high_length (default: None)
- low_length (default: None)
- atr_length (default: None)
- multiplier (default: None)
- mamode (default: None)
- talib (default: None)
- use_close (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.chandelier_exit()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on CHANDELIER_EXIT values

    return signals
```
