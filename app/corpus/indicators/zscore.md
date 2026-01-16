# ZSCORE

## Overview
Rolling Z Score

## pandas-ta Usage
```python
result = df.ta.zscore()
```

## Parameters
- length (default: None)
- std (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.zscore()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on ZSCORE values

    return signals
```
