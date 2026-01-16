# VARIANCE

## Overview
Rolling Variance

## pandas-ta Usage
```python
result = df.ta.variance()
```

## Parameters
- length (default: None)
- ddof (default: None)
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.variance()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on VARIANCE values

    return signals
```
