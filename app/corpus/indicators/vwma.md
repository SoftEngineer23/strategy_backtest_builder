# VWMA

## Overview
Volume Weighted Moving Average

## pandas-ta Usage
```python
result = df.ta.vwma()
```

## Parameters
- length (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.vwma()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on VWMA values

    return signals
```
