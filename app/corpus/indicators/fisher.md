# FISHER

## Overview
Fisher Transform

## pandas-ta Usage
```python
result = df.ta.fisher()
```

## Parameters
- length (default: None)
- signal (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.fisher()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on FISHER values

    return signals
```
