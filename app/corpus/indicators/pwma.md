# PWMA

## Overview
Pascal's Weighted Moving Average

## pandas-ta Usage
```python
result = df.ta.pwma()
```

## Parameters
- length (default: None)
- asc (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.pwma()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on PWMA values

    return signals
```
