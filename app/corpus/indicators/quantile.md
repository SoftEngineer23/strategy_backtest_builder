# QUANTILE

## Overview
Rolling Quantile

## pandas-ta Usage
```python
result = df.ta.quantile()
```

## Parameters
- length (default: None)
- q (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.quantile()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on QUANTILE values

    return signals
```
