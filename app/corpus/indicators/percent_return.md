# PERCENT_RETURN

## Overview
Percent Return

## pandas-ta Usage
```python
result = df.ta.percent_return()
```

## Parameters
- length (default: None)
- cumulative (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.percent_return()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on PERCENT_RETURN values

    return signals
```
