# CFO

## Overview
Chande Forcast Oscillator

## pandas-ta Usage
```python
result = df.ta.cfo()
```

## Parameters
- length (default: None)
- scalar (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.cfo()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on CFO values

    return signals
```
