# HL2

## Overview
HL2

## pandas-ta Usage
```python
result = df.ta.hl2()
```

## Parameters
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.hl2()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on HL2 values

    return signals
```
