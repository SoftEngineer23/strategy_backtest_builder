# SUM_SIGNED_ROLLING_DELTAS

## Overview
Sum of Signed Rolling Series Deltas

## pandas-ta Usage
```python
result = df.ta.sum_signed_rolling_deltas()
```

## Parameters
- length (default: required)
- exclusive (default: True)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.sum_signed_rolling_deltas()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on SUM_SIGNED_ROLLING_DELTAS values

    return signals
```
