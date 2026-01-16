# MEDIAN

## Overview
Rolling Median

## pandas-ta Usage
```python
result = df.ta.median()
```

## Parameters
- length (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.median()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on MEDIAN values

    return signals
```
