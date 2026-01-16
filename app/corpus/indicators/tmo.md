# TMO

## Overview
True Momentum Oscillator

## pandas-ta Usage
```python
result = df.ta.tmo()
```

## Parameters
- tmo_length (default: None)
- calc_length (default: None)
- smooth_length (default: None)
- momentum (default: None)
- normalize (default: None)
- exclusive (default: None)
- mamode (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.tmo()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on TMO values

    return signals
```
