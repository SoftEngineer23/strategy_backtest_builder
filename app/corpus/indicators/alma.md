# ALMA

## Overview
Arnaud Legoux Moving Average

## pandas-ta Usage
```python
result = df.ta.alma()
```

## Parameters
- length (default: None)
- sigma (default: None)
- dist_offset (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.alma()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on ALMA values

    return signals
```
