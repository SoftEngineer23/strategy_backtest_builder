# EOM

## Overview
Ease of Movement

## pandas-ta Usage
```python
result = df.ta.eom()
```

## Parameters
- length (default: None)
- divisor (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.eom()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on EOM values

    return signals
```
