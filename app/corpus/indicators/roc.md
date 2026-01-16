# ROC

## Overview
Rate of Change

## pandas-ta Usage
```python
result = df.ta.roc()
```

## Parameters
- length (default: None)
- scalar (default: None)
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.roc()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on ROC values

    return signals
```
