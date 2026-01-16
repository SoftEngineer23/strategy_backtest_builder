# ABERRATION

## Overview
Aberration

## pandas-ta Usage
```python
result = df.ta.aberration()
```

## Parameters
- length (default: None)
- atr_length (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.aberration()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on ABERRATION values

    return signals
```
