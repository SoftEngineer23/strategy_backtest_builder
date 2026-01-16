# SMMA

## Overview
SMoothed Moving Average

## pandas-ta Usage
```python
result = df.ta.smma()
```

## Parameters
- length (default: None)
- mamode (default: None)
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.smma()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on SMMA values

    return signals
```
