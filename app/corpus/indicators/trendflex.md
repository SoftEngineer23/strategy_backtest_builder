# TRENDFLEX

## Overview
Trendflex

## pandas-ta Usage
```python
result = df.ta.trendflex()
```

## Parameters
- length (default: None)
- smooth (default: None)
- alpha (default: None)
- pi (default: None)
- sqrt2 (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.trendflex()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on TRENDFLEX values

    return signals
```
