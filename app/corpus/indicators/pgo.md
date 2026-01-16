# PGO

## Overview
Pretty Good Oscillator

## pandas-ta Usage
```python
result = df.ta.pgo()
```

## Parameters
- length (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.pgo()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on PGO values

    return signals
```
