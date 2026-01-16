# INERTIA

## Overview
Inertia

## pandas-ta Usage
```python
result = df.ta.inertia()
```

## Parameters
- length (default: None)
- rvi_length (default: None)
- scalar (default: None)
- refined (default: None)
- thirds (default: None)
- drift (default: None)
- mamode (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.inertia()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on INERTIA values

    return signals
```
