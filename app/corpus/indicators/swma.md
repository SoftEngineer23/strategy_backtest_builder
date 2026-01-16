# SWMA

## Overview
Symmetric Weighted Moving Average

## pandas-ta Usage
```python
result = df.ta.swma()
```

## Parameters
- length (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.swma()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on SWMA values

    return signals
```
