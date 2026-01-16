# COPPOCK

## Overview
Coppock Curve

## pandas-ta Usage
```python
result = df.ta.coppock()
```

## Parameters
- length (default: None)
- fast (default: None)
- slow (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.coppock()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on COPPOCK values

    return signals
```
