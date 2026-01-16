# VORTEX

## Overview
Vortex

## pandas-ta Usage
```python
result = df.ta.vortex()
```

## Parameters
- length (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.vortex()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on VORTEX values

    return signals
```
