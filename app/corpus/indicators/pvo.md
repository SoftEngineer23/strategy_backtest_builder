# PVO

## Overview
Percentage Volume Oscillator

## pandas-ta Usage
```python
result = df.ta.pvo()
```

## Parameters
- fast (default: None)
- slow (default: None)
- signal (default: None)
- scalar (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.pvo()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on PVO values

    return signals
```
