# BOP

## Overview
Balance of Power

## pandas-ta Usage
```python
result = df.ta.bop()
```

## Parameters
- scalar (default: None)
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.bop()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on BOP values

    return signals
```
