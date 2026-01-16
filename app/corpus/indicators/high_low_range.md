# HIGH_LOW_RANGE

## Overview
High Low Range

## pandas-ta Usage
```python
result = df.ta.high_low_range()
```

## Parameters
- No configurable parameters

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.high_low_range()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on HIGH_LOW_RANGE values

    return signals
```
