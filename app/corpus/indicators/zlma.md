# ZLMA

## Overview
Zero Lag Moving Average

## pandas-ta Usage
```python
result = df.ta.zlma()
```

## Parameters
- length (default: None)
- mamode (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.zlma()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on ZLMA values

    return signals
```
