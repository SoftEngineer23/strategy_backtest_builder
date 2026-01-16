# REAL_BODY

## Overview
Body Range

## pandas-ta Usage
```python
result = df.ta.real_body()
```

## Parameters
- No configurable parameters

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.real_body()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on REAL_BODY values

    return signals
```
