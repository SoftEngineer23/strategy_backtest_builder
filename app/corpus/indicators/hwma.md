# HWMA

## Overview
Holt-Winter Moving Average

## pandas-ta Usage
```python
result = df.ta.hwma()
```

## Parameters
- na (default: None)
- nb (default: None)
- nc (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.hwma()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on HWMA values

    return signals
```
