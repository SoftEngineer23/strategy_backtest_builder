# AROON

## Overview
Aroon & Aroon Oscillator

## pandas-ta Usage
```python
result = df.ta.aroon()
```

## Parameters
- length (default: None)
- scalar (default: None)
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.aroon()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on AROON values

    return signals
```
