# RMA

## Overview
wildeR's Moving Average

## pandas-ta Usage
```python
result = df.ta.rma()
```

## Parameters
- length (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.rma()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on RMA values

    return signals
```
