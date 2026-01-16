# SMI

## Overview
SMI Ergodic Indicator

## pandas-ta Usage
```python
result = df.ta.smi()
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
    indicator = df.ta.smi()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on SMI values

    return signals
```
