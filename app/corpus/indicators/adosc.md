# ADOSC

## Overview
Accumulation/Distribution Oscillator

## pandas-ta Usage
```python
result = df.ta.adosc()
```

## Parameters
- fast (default: None)
- slow (default: None)
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.adosc()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on ADOSC values

    return signals
```
