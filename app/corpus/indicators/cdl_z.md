# CDL_Z

## Overview
Z Candles

## pandas-ta Usage
```python
result = df.ta.cdl_z()
```

## Parameters
- length (default: None)
- full (default: None)
- ddof (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.cdl_z()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on CDL_Z values

    return signals
```
