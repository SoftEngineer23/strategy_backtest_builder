# SINWMA

## Overview
Sine Weighted Moving Average

## pandas-ta Usage
```python
result = df.ta.sinwma()
```

## Parameters
- length (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.sinwma()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on SINWMA values

    return signals
```
