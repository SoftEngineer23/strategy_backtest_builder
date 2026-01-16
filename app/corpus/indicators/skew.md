# SKEW

## Overview
Rolling Skew

## pandas-ta Usage
```python
result = df.ta.skew()
```

## Parameters
- length (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.skew()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on SKEW values

    return signals
```
