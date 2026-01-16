# BIAS

## Overview
Bias

## pandas-ta Usage
```python
result = df.ta.bias()
```

## Parameters
- length (default: None)
- mamode (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.bias()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on BIAS values

    return signals
```
